import certifi
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

# Load .env file
load_dotenv()

# Get MongoDB URI from environment
uri = os.getenv("MONGO_DB_URL")

if not uri:
    raise ValueError("MMONGO_DB_URL not found in .env file")

# Create client
client = MongoClient(
    uri,
    server_api=ServerApi('1'),
    tls=True,
    tlsCAFile=certifi.where()
)

# Test connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print("Connection error:", e)
