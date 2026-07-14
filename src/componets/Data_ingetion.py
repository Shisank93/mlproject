# Built-in modules
import os              # Used for creating folders and working with file paths
import sys             # Used to capture detailed exception information

# Custom modules
from src.exception import customException   # Custom exception class for better error handling
from src.logger import logging              # Custom logger to record execution steps

# Third-party libraries
import pandas as pd                        # Used to read and manipulate datasets

# Function used to split data into train and test sets
from sklearn.model_selection import train_test_split

# Used to automatically create class variables (__init__)
from dataclasses import dataclass

from src.componets.Data_transformation import DataTransformation , DataTransformationConfig

# Configuration class that stores all file paths
@dataclass
class DataIngestionConfig:
    # Location where training data will be stored
    train_data_path: str = os.path.join('artifacts', 'train.csv')

    # Location where testing data will be stored
    test_data_path: str = os.path.join('artifacts', 'test.csv')

    # Location where the original dataset will be stored
    raw_data_path: str = os.path.join('artifacts', 'data.csv')


class DataIngestion:

    # Constructor
    def __init__(self):
        # Create an object containing all file paths
        self.ingestion_config = DataIngestionConfig()

    # Main function responsible for reading and splitting the dataset
    def initiate_data_ingestion(self):

        # Log that data ingestion has started
        logging.info("Entered the data ingestion method or component")

        try:
            # Read the CSV dataset into a pandas DataFrame
            df = pd.read_csv('notebook/data/stud.csv')

            # Log successful reading
            logging.info('Read the dataset as dataframe')

            # Create the artifacts directory if it doesn't already exist
            os.makedirs(
                os.path.dirname(self.ingestion_config.train_data_path),
                exist_ok=True
            )

            # Save the complete dataset as raw data
            df.to_csv(
                self.ingestion_config.raw_data_path,
                index=False,
                header=True
            )

            # Log before splitting
            logging.info("train test split initiated")

            # Split the dataset into 80% training and 20% testing
            train_set, test_set = train_test_split(
                df,
                test_size=0.2,
                random_state=42
            )

            # Save training dataset
            train_set.to_csv(
                self.ingestion_config.train_data_path,
                index=False,
                header=True
            )

            # Save testing dataset
            test_set.to_csv(
                self.ingestion_config.test_data_path,
                index=False,
                header=True
            )

            # Log completion
            logging.info("ingestion of the data is completed")

            # Return the paths of the saved train and test files
            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            # Convert any exception into a custom exception with traceback
            raise customException(e, sys)


# This block runs only when this file is executed directly
if __name__ == "__main__":

    # Create DataIngestion object
    obj = DataIngestion()

    # Execute the ingestion pipeline
    train_data  , test_data=obj.initiate_data_ingestion()

    obj2 = DataTransformation()
    obj2.initiate_data_transformation(train_data , test_data)