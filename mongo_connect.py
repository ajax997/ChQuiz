from pymongo import MongoClient
from pymongo.server_api import ServerApi
def test_mongo_connection():
    uri = "mongodb://nnguyen231dxc_db_user:E0JR83lvL8NlsqWy@ac-wao3gsf-shard-00-00.i7cibfp.mongodb.net:27017,ac-wao3gsf-shard-00-01.i7cibfp.mongodb.net:27017,ac-wao3gsf-shard-00-02.i7cibfp.mongodb.net:27017/?ssl=true&replicaSet=atlas-103t1s-shard-0&authSource=admin&appName=Cluster0"
    # Create a new client and connect to the server
    client = MongoClient(uri, server_api=ServerApi('1'))
    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        return "Pinged your deployment. You successfully connected to MongoDB!"
    except Exception as e:
        print(e)
