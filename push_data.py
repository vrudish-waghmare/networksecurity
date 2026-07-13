import os 
import sys 
import json

from dotenv import load_dotenv 
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

import certifi
ca = certifi.where()

import pandas as pd 
import numpy as np 
import pymongo
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkDataExtract():
    # algo: 
    # 1. fetch the data from the csv file and convert it into json
    # 2. connect to the mongodb server and push all your data
    def __init__(self):
        try:
            pass 
        except Exception as e: 
            raise NetworkSecurityException(e, sys)
    
    def csv_to_json_converter(self, file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e: 
            raise NetworkSecurityException(e, sys)

    def insert_data_mongodb(self, records, database, collection):
        try:
            self.database = database 
            self.collection= collection 
            self.records = records

            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            self.database = self.mongo_client[self.database]
            self.collection = self.database[self.collection]
            self.collection.insert_many(self.records)
            return f'Inserted {len(self.records)} records to {self.collection.database.collection} successfully.'
        except Exception as e: 
            raise NetworkSecurityException(e, sys)


if __name__=='__main__':
    FILE_PATH = 'Network_Data\phisingData.csv'
    DATABASE = "vrudishdb"
    COLLECTION = 'NetworkData'
    networkobj = NetworkDataExtract()
    records = networkobj.csv_to_json_converter(file_path=FILE_PATH)
    print(networkobj.insert_data_mongodb(records=records, database=DATABASE, collection=COLLECTION))




