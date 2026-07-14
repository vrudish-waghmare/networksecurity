import os 
import sys 
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact

import pandas as pd 
import pymongo 
import numpy as np 
from typing import List 
from sklearn.model_selection import train_test_split
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self, data_ingestion_config:DataIngestionConfig):
        try: 
            self.data_ingestion_config = data_ingestion_config
            

        except Exception as e: 
            raise NetworkSecurityException(e, sys) 
        
    def export_collection_as_dataframe(self):
        """
        Read data from MongoDB and returns a dataframe
        """
        try:
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]
            df = pd.DataFrame(list(collection.find()))
            if "_id" in df.columns.to_list():
                df = df.drop("_id", axis=1)
            df.replace({"na": np.nan}, inplace=True)
            return df
        except Exception as e: 
            raise NetworkSecurityException(e, sys)

    def export_data_into_feature_store(self, dataframe: pd.DataFrame):
        # steps: 
        # 1. setup the feature store path
        # 2. create a path
        # 3. convert the dataframe into phisingData.csv file 
        # 4. return dataframe
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path, exist_ok=True)

            dataframe.to_csv(feature_store_file_path, index=False, header=True)
            return dataframe 
        except Exception as e: 
            raise NetworkSecurityException(e, sys)



    def split_data_as_train_test(self, dataframe: pd.DataFrame):
        # steps: 
        # 1. split data into train and test split 
        # 2. create a train path and store train.csv file
        # 3. create a test path and stoer test.csv file
        try:
            train_set, test_set = train_test_split(dataframe, test_size=self.data_ingestion_config.train_test_split_ratio) 
            logging.info('Performed train test split on the dataframe')
            logging.info('Exited split_data_as_train_test method of Data_Ingestion class')

            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            os.makedirs(dir_path, exist_ok=True)
            
            logging.info(f'Exporting train and test file path.')

            train_set.to_csv(self.data_ingestion_config.training_file_path, index=False, header=True)
            test_set.to_csv(self.data_ingestion_config.testing_file_path, index=False, header=True)
            
            logging.info(f'Exported train and test file path.')

        except Exception as e: 
            raise NetworkSecurityException(e, sys)



    def initiate_data_ingestion(self):
        # steps: 
        # 1. read the collections from mongo db and create a dataframe
        # 2. create a raw.csv file to store all the data
        # 3. train test split and get train.csv and test.csv
        # 4. return train and test path
        try:
            dataframe = self.export_collection_as_dataframe()
            dataframe = self.export_data_into_feature_store(dataframe)
            self.split_data_as_train_test(dataframe)
            dataingestionartifact = DataIngestionArtifact(trained_file_path=self.data_ingestion_config.training_file_path,
                      test_file_path=self.data_ingestion_config.testing_file_path)
            
            return dataingestionartifact

        except Exception as e: 
            raise NetworkSecurityException(e, sys)
        
