import json, os, time, sys
from datetime import datetime, timezone
from concurrent.futures import ThreadPoolExecutor, as_completed
from openai import OpenAI
from google.cloud import firestore
from google.cloud import secretmanager

MODEL = "text-embedding-3-small"
DIMS = 1536
PROJECT = "regal-scholar-453620-r7"

def get_openai_api_key():
    key = (os.getenv("OPENAI_API_KEY") or "").strip()
    if key:
        return key
    sm = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT}/secrets/openai-api-key/versions/latest"
    return sm.access_secret_version(request={"name": name}).payload.data.decode("UTF-8").strip()

client = OpenAI(api_key=get_openai_api_key())
db = firestore.Client(project=PROJECT, database="copernicusai")
col = db.collection("research_papers")

def now_iso():
    return datetime.now(timezone.utc).isoformat()

def build_text(d):
    parts = []
    if d.get("title"):
        parts.append(d["title"])
    if d.get("abstract"):
        parts.append(d["abstract"])
    if d.get("keywords"):
        parts.append(" ".join(d["keywords"]))
    return "\n".join(parts)

def embed_one(text):
    for attempt in range(3):
        try:
            resp = client.embeddings.create(model=MODEL, input=text)
            d = resp.data
            if len(d) != 1:
                raise RuntimeError(f"expected 1 embedding got {len(d)}")
            vec = list(d[0].embedding)
            if len(vec) != DIMS:
                raise RuntimeError(f"dim mismatch {len(vec)}")
            return vec
        except Exception as e:
            if attempt == 2:
                raise
            time.sleep(1.5 * (attempt + 1))

# pin: find all glmp-f1-scoped docs missing embedding
q = col.where("question_scope_ids", "array_contains", "glmp-f1")
unembedded = []
for snap in q.stream():
    d = snap.to_dict()
    if d.get("embedding") is None:
        unembedded.append((snap.id, d))
print(f"pin: {len(unembedded)} glmp-f1 docs missing embedding")

mode = sys.argv[1] if len(sys.argv) > 1 else "dry-run"

if mode == "dry-run":
    print(f"dry-run: would embed {len(unembedded)}, 0 errors expected")
    sys.exit(0)

if mode == "pilot":
    targets = unembedded[:5]
elif mode == "full":
    targets = unembedded
else:
    raise SystemExit(f"unknown mode {mode}")

def work(doc_id, d):
    text = build_text(d)
    vec = embed_one(text)
    return doc_id, vec

ok, fail = 0, 0
with ThreadPoolExecutor(max_workers=16) as ex:
    futures = {ex.submit(work, doc_id, d): doc_id for doc_id, d in targets}
    for fut in as_completed(futures):
        doc_id = futures[fut]
        try:
            doc_id_r, vec = fut.result()
            col.document(doc_id_r).update({
                "embedding": vec,
                "embedding_model": MODEL,
                "embedding_updated": now_iso(),
            })
            ok += 1
        except Exception as e:
            print(f"  FAIL {doc_id}: {e}")
            fail += 1
        if ok % 50 == 0 and ok > 0:
            print(f"  progress: {ok}/{len(targets)}")

print(f"DONE ({mode}). ok={ok} failed={fail}")
