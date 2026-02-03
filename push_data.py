import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL=os.getenv("MONGO_DB_URL")
print(MONGO_DB_URL)

# certifi provides a trusted list of SSL certificates that Python uses to verify secure connections.
# When your Python app connects to MongoDB Atlas, it must:
# Confirm the server is really MongoDB and not a fake/malicious server
import certifi
ca=certifi.where() #Get the file path of the trusted certificate bundle that certifi provide


import pandas as pd
import numpy as np
import pymongo
from networksecurity.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    def __init__(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_to_json_convertor(self, file_path):
        try:
            data = pd.read_csv(file_path)
            records = data.to_dict(orient="records")
            return records
        except Exception as e:
            raise NetworkSecurityException(e, sys)

        
    def insert_data_mongodb(self,records,database,collection):
        try:
            # Store method parameters as class attributes
            self.database=database
            self.collection=collection
            self.records=records

             # Create MongoDB client using connection URL
            self.mongo_client=pymongo.MongoClient(MONGO_DB_URL)
            # Access the specified database
            self.database=self.mongo_client[self.database]
             # Access the specified collection
            self.collection=self.database[self.collection]
             # Insert multiple records into the collection
            self.collection.insert_many(self.records)
            return(len(self.records))
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
if __name__=="__main__":
    FILE_PATH="Network_Data\\phisingData.csv"
    DATABASE="ARSHDEEP"
    Collection="NetworkData"
    networkobj=NetworkDataExtract()
    records=networkobj.csv_to_json_convertor(file_path=FILE_PATH)
    print(records)
    no_of_records=networkobj.insert_data_mongodb(records,DATABASE,Collection)
    print(no_of_records)
