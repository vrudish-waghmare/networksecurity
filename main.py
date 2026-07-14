import os 
import sys 
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig



if __name__=='__main__':
    # 1. create an object of TrainingPipelineConfig
    # 2. create an object of DataIngestionConfig
    # 3. create an object of DataIngestion
    # 4. it returns train and test path 
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info('Initiate the data ingestion')
        dataingestionartifacts = data_ingestion.initiate_data_ingestion()
        print(dataingestionartifacts)
        logging.info('Data Initiation Completed')

    except Exception as e:
        raise NetworkSecurityException(e, sys)