import os
import sys
import json

from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv('MONGO_DB_URL')
print(MONGO_DB_URL)
import certifi
ca = certifi.where()

import pandas as pd
import numpy as np
import pymongo

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logger.logger import logging


class NetworkDataExtract():
    def init(self):
        try:
            pass
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def csv_tojson_converter(self,file_path):
        try:
            data = pd.read_csv(file_path)
            data.reset_index(drop=True,inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            return records
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
    def pushing_data_to_mongodb(self,records,db,collecton):
        try:
            self.db = db
            self.collection = collecton
            self.records = records 

            self.client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=ca)

            self.db = self.client[self.db]
            self.collection = self.db[self.collection]
            self.collection.insert_many(self.records)
            return len(self.records)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
if __name__ == '__main__':
    extract_obj = NetworkDataExtract()
    db = "MlOps"
    collection = "network_data"
    file_path = "./Network_Data/NetworkData.csv"
    records = extract_obj.csv_tojson_converter(file_path)
    extract_obj.pushing_data_to_mongodb(records,db,collection)
    print(records)