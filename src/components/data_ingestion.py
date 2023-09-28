import os
import sys
sys.path.append(os.getcwd())
from src.exception import CustomException
from src.logger import logging
import pandas as pd
from sklearn.model_selection import train_test_split
from dataclasses import dataclass
from src.components.data_transformation import DataTransformation


## Initialize the Data Ingestion Configuration

@dataclass
class DataIngestionConfig:

    train_data_path:str = os.path.join('artifacts', 'train.csv')
    test_data_path:str = os.path.join('artifacts', 'test.csv')
    raw_data_path:str = os.path.join('artifacts', 'raw.csv')


## Class for Data Ingestion

class DataIngestion:

    def __init__(self):
        self.ingestion_config = DataIngestionConfig()

    def initiate_data_ingestion(self):

        logging.info('Data Ingestion method starts')

        try:

            df = pd.read_csv(os.path.join('./notebooks/data', 'gemstone.csv'))

            logging.info('Dataset read as pandas DataFrame')

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)

            df.to_csv(self.ingestion_config.raw_data_path, index=False)

            logging.info('Train Test Split')

            train_set, test_set = train_test_split(df, test_size=0.30)

            train_set.to_csv(self.ingestion_config.train_data_path, index=False, header=True)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False, header=True)

            logging.info('Data Ingestion is completed')

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
            
        except Exception as e:

            logging.info('Exception occured at Data Ingestion stage')

            raise CustomException(e, sys)

if __name__ == '__main__':

    obj = DataIngestion()
    train_data, test_data = obj.initiate_data_ingestion()
    data_transforamtion = DataTransformation()
    data_transforamtion.initiate_data_transformation(train_data, test_data)