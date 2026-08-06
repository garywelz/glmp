"""
Rollback / audit query for atap-firstpass-20260806. Read-only by default --
pass --delete to actually remove matched docs (never run that without a
fresh go-ahead; this file exists so the query is proven correct BEFORE
the write, per Claude Chat's request, not invented after).
"""
import argparse
from google.cloud import firestore

RUN_ID = "atap-firstpass-20260806"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--delete", action="store_true", help="Actually delete matched docs")
    args = parser.parse_args()

    db = firestore.Client(project="regal-scholar-453620-r7", database="copernicusai")
    col = db.collection("research_papers")
    docs = list(col.where("run_id", "==", RUN_ID).stream())
    print(f"Query: research_papers where run_id == {RUN_ID!r}")
    print(f"Matched: {len(docs)} documents")

    if args.delete:
        batch = db.batch()
        n = 0
        for i, doc in enumerate(docs):
            batch.delete(doc.reference)
            n += 1
            if n % 400 == 0:
                batch.commit()
                batch = db.batch()
        batch.commit()
        print(f"Deleted: {n} documents")


if __name__ == "__main__":
    main()
