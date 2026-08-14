import json, os, time, sys
import requests
import xml.etree.ElementTree as ET

BASE = r"C:\Users\garyw\glmp\docs\open-questions\glmp-f1-workingdata-2026-08-14"
IN = os.path.join(BASE, "f1_pmids_raw.json")
OUT = os.path.join(BASE, "f1_metadata.json")
EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
EMAIL = "gary@copernicusai.fyi"
BATCH_SIZE = 100

def atomic_write(path, obj):
    tmp = path + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2, ensure_ascii=False)
    os.replace(tmp, path)

def load_checkpoint():
    if os.path.exists(OUT):
        try:
            with open(OUT, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return {"papers": {}, "failed": []}
    return {"papers": {}, "failed": []}

def text_of(el):
    if el is None:
        return ""
    return "".join(el.itertext()).strip()

def parse_article(article_el):
    medline = article_el.find("MedlineCitation")
    pubmed_data = article_el.find("PubmedData")
    if medline is None:
        return None
    pmid_el = medline.find("PMID")
    pmid = text_of(pmid_el)
    art = medline.find("Article")
    if art is None:
        return None
    title = text_of(art.find("ArticleTitle"))
    if not title:
        return None
    abstract_parts = []
    abst = art.find("Abstract")
    if abst is not None:
        for ab in abst.findall("AbstractText"):
            abstract_parts.append(text_of(ab))
    abstract = " ".join(abstract_parts)

    authors = []
    al = art.find("AuthorList")
    if al is not None:
        for author in al.findall("Author"):
            last = text_of(author.find("LastName"))
            fore = text_of(author.find("ForeName"))
            coll = text_of(author.find("CollectiveName"))
            if last and fore:
                authors.append(f"{last}, {fore}")
            elif last:
                authors.append(last)
            elif coll:
                authors.append(coll)

    journal_el = art.find("Journal")
    journal_title = ""
    journal_iso = ""
    year = ""
    if journal_el is not None:
        jt = journal_el.find("Title")
        if jt is not None:
            journal_title = text_of(jt)
        ji = journal_el.find("ISOAbbreviation")
        if ji is not None:
            journal_iso = text_of(ji)
        pubdate = journal_el.find("JournalIssue/PubDate")
        if pubdate is not None:
            y = pubdate.find("Year")
            if y is not None:
                year = text_of(y)
            else:
                md = pubdate.find("MedlineDate")
                if md is not None:
                    mdt = text_of(md)
                    if len(mdt) >= 4 and mdt[:4].isdigit():
                        year = mdt[:4]

    doi = None
    if pubmed_data is not None:
        idlist = pubmed_data.find("ArticleIdList")
        if idlist is not None:
            for aid in idlist.findall("ArticleId"):
                if aid.get("IdType") == "doi":
                    doi = text_of(aid)
                    break

    keywords = []
    for kwlist in medline.findall("KeywordList"):
        for kw in kwlist.findall("Keyword"):
            t = text_of(kw)
            if t:
                keywords.append(t)

    return {
        "id": f"pubmed_{pmid}",
        "pmid": pmid,
        "title": title,
        "authors": authors,
        "author_string": ", ".join(authors[:5]) + (" et al." if len(authors) > 5 else ""),
        "journal": journal_iso or journal_title,
        "journal_full": journal_title,
        "year": year,
        "doi": doi,
        "abstract": abstract,
        "keywords": keywords,
        "source": "pubmed",
        "category": "biology",
        "discipline": "biology",
    }

def main():
    with open(IN, encoding="utf-8") as f:
        raw = json.load(f)
    all_pmids = raw["union_pmids"]
    print(f"total candidate PMIDs: {len(all_pmids)}")

    ckpt = load_checkpoint()
    done = set(ckpt["papers"].keys())
    failed_set = set(ckpt.get("failed", []))
    remaining = [p for p in all_pmids if p not in done and p not in failed_set]
    print(f"already done: {len(done)}  already failed: {len(failed_set)}  remaining: {len(remaining)}")

    for i in range(0, len(remaining), BATCH_SIZE):
        batch = remaining[i:i+BATCH_SIZE]
        params = {
            "db": "pubmed",
            "id": ",".join(batch),
            "rettype": "abstract",
            "retmode": "xml",
            "email": EMAIL,
        }
        try:
            r = requests.get(EFETCH, params=params, timeout=60)
            r.raise_for_status()
            root = ET.fromstring(r.content)
            found_pmids = set()
            for art in root.findall("PubmedArticle"):
                parsed = parse_article(art)
                if parsed:
                    ckpt["papers"][parsed["pmid"]] = parsed
                    found_pmids.add(parsed["pmid"])
            for p in batch:
                if p not in found_pmids:
                    ckpt["failed"].append(p)
        except Exception as e:
            print(f"  batch error at {i}: {e}")
            for p in batch:
                ckpt["failed"].append(p)

        if (i // BATCH_SIZE) % 5 == 0:
            atomic_write(OUT, ckpt)
            print(f"  progress: {len(ckpt['papers'])} papers, {len(ckpt['failed'])} failed (batch {i//BATCH_SIZE+1}/{(len(remaining)+BATCH_SIZE-1)//BATCH_SIZE})")
        time.sleep(0.34)

    atomic_write(OUT, ckpt)
    print(f"DONE. total papers={len(ckpt['papers'])} failed={len(ckpt['failed'])}")

if __name__ == "__main__":
    main()
