import json, os, math, time
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI
from google.cloud import firestore

BASE = r"C:\Users\garyw\AppData\Local\Temp\claude\C--Users-garyw-glmp\917cae92-4c16-4f2f-9e46-409f794b52a0\scratchpad"
META = os.path.join(BASE, "q9_metadata.json")
DEDUPE = os.path.join(BASE, "q9_dedupe.json")
OUT = os.path.join(BASE, "q9_scored.json")
MODEL = "text-embedding-3-small"
DIMS = 1536
QUESTION_TEXT = "What regulatory logic governs developmental commitment and cell-fate decisions, and how is the decision made irreversible?"

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
db = firestore.Client(project="regal-scholar-453620-r7", database="copernicusai")

def atomic_write(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)

def build_text(paper):
    parts = []
    if paper.get("title"):
        parts.append(paper["title"])
    if paper.get("abstract"):
        parts.append(paper["abstract"])
    if paper.get("keywords"):
        parts.append(" ".join(paper["keywords"]))
    return "\n".join(parts)

def cosine(a, b):
    dot = sum(x*y for x, y in zip(a, b))
    na = math.sqrt(sum(x*x for x in a))
    nb = math.sqrt(sum(x*x for x in b))
    if na == 0 or nb == 0:
        return 0.0
    return dot / (na * nb)

def embed_one(text):
    for attempt in range(3):
        try:
            resp = client.embeddings.create(model=MODEL, input=text)
            d = resp.data
            if len(d) != 1:
                raise RuntimeError(f"expected 1 embedding got {len(d)}")
            if not str(resp.model).startswith(MODEL):
                raise RuntimeError(f"model mismatch {resp.model}")
            vec = list(d[0].embedding)
            if len(vec) != DIMS:
                raise RuntimeError(f"dim mismatch {len(vec)}")
            return vec
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(1.5 * (attempt + 1))

def main():
    with open(META, encoding="utf-8") as f:
        meta = json.load(f)
    with open(DEDUPE, encoding="utf-8") as f:
        dedupe = json.load(f)
    existing_ids = dedupe["existing"]  # keyed by "pubmed_<pmid>"

    papers = meta["papers"]  # keyed by pmid (no prefix)
    print(f"total fetched metadata: {len(papers)}")

    # question embedding
    q_vec = embed_one(QUESTION_TEXT)
    print("question embedding: ok, dims", len(q_vec))

    # load existing checkpoint if present
    if os.path.exists(OUT):
        with open(OUT, encoding="utf-8") as f:
            scored = json.load(f)
    else:
        scored = {}

    already_corpus_pmids = {k[len("pubmed_"):]: v for k, v in existing_ids.items()}

    # split into: needs fresh embed (new papers) vs reuse existing embedding (corpus papers)
    to_embed = []
    to_reuse = []
    for pmid, paper in papers.items():
        if pmid in scored:
            continue
        if pmid in already_corpus_pmids:
            to_reuse.append(pmid)
        else:
            to_embed.append(pmid)

    print(f"already scored: {len(scored)}  need fresh embed: {len(to_embed)}  need reuse (corpus): {len(to_reuse)}")

    # reuse existing embeddings from Firestore for already-corpus papers
    col = db.collection("research_papers")
    CHUNK = 300
    for i in range(0, len(to_reuse), CHUNK):
        chunk = to_reuse[i:i+CHUNK]
        refs = [col.document(f"pubmed_{p}") for p in chunk]
        for snap in db.get_all(refs):
            if not snap.exists:
                continue
            data = snap.to_dict()
            emb = data.get("embedding")
            pmid = snap.id[len("pubmed_"):]
            if emb is not None:
                sim = cosine(q_vec, list(emb))
                scored[pmid] = {"score": sim, "reused_embedding": True}
        print(f"  reuse-embed progress: {min(i+CHUNK, len(to_reuse))}/{len(to_reuse)}")
    atomic_write(OUT, scored)

    # fresh-embed new papers, concurrently
    def work(pmid):
        paper = papers[pmid]
        text = build_text(paper)
        if not text.strip():
            return pmid, None
        vec = embed_one(text)
        sim = cosine(q_vec, vec)
        return pmid, sim

    done_count = 0
    with ThreadPoolExecutor(max_workers=16) as ex:
        futures = {ex.submit(work, pmid): pmid for pmid in to_embed}
        for fut in as_completed(futures):
            pmid = futures[fut]
            try:
                pmid_r, sim = fut.result()
                if sim is not None:
                    scored[pmid_r] = {"score": sim, "reused_embedding": False}
                else:
                    scored[pmid_r] = {"score": None, "error": "empty_text"}
            except Exception as e:
                scored[pmid] = {"score": None, "error": str(e)}
            done_count += 1
            if done_count % 250 == 0:
                atomic_write(OUT, scored)
                print(f"  fresh-embed progress: {done_count}/{len(to_embed)}")

    atomic_write(OUT, scored)
    ok = sum(1 for v in scored.values() if v.get("score") is not None)
    err = sum(1 for v in scored.values() if v.get("score") is None)
    print(f"DONE. scored={ok} errors={err} total={len(scored)}")

if __name__ == "__main__":
    main()
