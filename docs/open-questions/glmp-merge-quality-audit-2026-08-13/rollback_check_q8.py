from google.cloud import firestore

db = firestore.Client(project="regal-scholar-453620-r7", database="copernicusai")
col = db.collection("research_papers")

n = col.where("question_scope_ids", "array_contains", "glmp-q8").count().get()[0][0].value
print(f"docs with glmp-q8 in question_scope_ids: {n}")
