from pymongo import MongoClient

username = "nnguyen231dxc_db_user"
password = ""

uri = (
    f"mongodb+srv://nnguyen231dxc_db_user:E0JR83lvL8NlsqWy@cluster0.i7cibfp.mongodb.net/?appName=Cluster0"
)

client = MongoClient(uri)

db = client["ChQuiz"]
collection = db["QuizDataSet"]

for doc in collection.find():
    print(doc)
