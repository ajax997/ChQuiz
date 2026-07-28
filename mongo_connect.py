from pymongo import MongoClient
def test_mongo_connection():
    uri = (
        f"mongodb+srv://nnguyen231dxc_db_user:E0JR83lvL8NlsqWy@cluster0.i7cibfp.mongodb.net/?appName=Cluster0"
    )
    
    client = MongoClient(uri)
    
    db = client["ChQuiz"]
    collection = db["QuizDataSet"]
    a = []
    for doc in collection.find():
        a.append(str(doc))
    return a
