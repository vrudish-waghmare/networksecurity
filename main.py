import os 
import sys 
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.entity.config_entity import DataIngestionConfig, TrainingPipelineConfig, DataValidatonConfig
from networksecurity.components.data_validation import DataValidation



if __name__=='__main__':
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        data_ingestion = DataIngestion(dataingestionconfig)
        logging.info('Initiate the data ingestion')
        dataingestionartifacts = data_ingestion.initiate_data_ingestion()
        print(dataingestionartifacts)
        logging.info('Data Initiation Completed')
        data_validation_config= DataValidatonConfig(trainingpipelineconfig)
        data_validation = DataValidation(dataingestionartifacts, data_validation_config)
        logging.info("Initiate the data validation")
        data_validation_artifact = data_validation.initiate_data_validation()
        print(data_validation_artifact)
        logging.info("Data Validation completed")

    except Exception as e:
        raise NetworkSecurityException(e, sys)