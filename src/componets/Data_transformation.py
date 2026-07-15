# Import the sys module to get exception information
import sys

# Import os module for handling file paths
import os

# dataclass automatically creates constructor (__init__) and other utility methods
from dataclasses import dataclass

# Custom function that saves Python objects (using pickle)
from src.utils import save_object

# NumPy is used for numerical operations and array manipulation
import numpy as np

# Pandas is used to read and manipulate datasets
import pandas as pd

# ColumnTransformer allows applying different preprocessing
# pipelines to different columns.
from sklearn.compose import ColumnTransformer

# SimpleImputer fills missing values in datasets.
from sklearn.impute import SimpleImputer

# Pipeline executes preprocessing steps sequentially.
from sklearn.pipeline import Pipeline

# OneHotEncoder converts categorical values into numerical vectors.
# StandardScaler standardizes numerical features.
from sklearn.preprocessing import OneHotEncoder, StandardScaler

# Custom exception class for better debugging
from src.exception import customException

# Custom logger for logging project events
from src.logger import logging


# -------------------------------------------------------------------------
# Configuration class
# Stores the location where the fitted preprocessing object will be saved.
# -------------------------------------------------------------------------
@dataclass
class DataTransformationConfig:

    # Path where the preprocessing object (preprocessor.pkl) will be stored.
    preprocessor_obj_file_path: str = os.path.join(
        "artifacts",
        "preprocessor.pkl"
    )


# -------------------------------------------------------------------------
# Main Data Transformation Class
# Responsible for preprocessing the dataset.
# -------------------------------------------------------------------------
class DataTransformation:

    # Constructor
    def __init__(self):

        # Create configuration object
        self.data_transformation_config = DataTransformationConfig()


    # ---------------------------------------------------------------------
    # Creates and returns the preprocessing pipeline
    # ---------------------------------------------------------------------
    def get_transformer_obj(self):

        """
        Creates preprocessing pipelines for numerical and
        categorical columns and combines them.
        """

        try:

            # Numerical columns
            numerical_columns = [
                "writing_score",
                "reading_score"
            ]

            # Categorical columns
            categorical_columns = [
                "gender",
                "race_ethnicity",
                "parental_level_of_education",
                "lunch",
                "test_preparation_course"
            ]

            # ---------------------------------------------------------
            # Numerical Pipeline
            # ---------------------------------------------------------
            num_pipeline = Pipeline(

                steps=[

                    # Replace missing values using median
                    ("imputer",
                     SimpleImputer(strategy="median")),

                    # Standardize numerical values
                    ("scaler",
                     StandardScaler())
                ]
            )

            logging.info("Numerical pipeline created.")

            # ---------------------------------------------------------
            # Categorical Pipeline
            # ---------------------------------------------------------
            cat_pipeline = Pipeline(

                steps=[

                    # Fill missing categorical values
                    ("imputer",
                     SimpleImputer(strategy="most_frequent")),

                    # Convert categories into one-hot vectors
                    ("one_hot_encoder",
                     OneHotEncoder()),

                    # Scale encoded values
                    ("scaler",
                     StandardScaler(with_mean=False))
                ]
            )

            logging.info("Categorical pipeline created.")

            # ---------------------------------------------------------
            # Combine numerical and categorical pipelines
            # ---------------------------------------------------------
            preprocessor = ColumnTransformer(

                [

                    # Apply numerical pipeline
                    (
                        "num_pipeline",
                        num_pipeline,
                        numerical_columns
                    ),

                    # Apply categorical pipeline
                    (
                        "cat_pipeline",
                        cat_pipeline,
                        categorical_columns
                    )
                ]
            )

            # Return complete preprocessing object
            return preprocessor

        except Exception as e:

            # Raise custom exception if anything fails
            raise customException(e, sys)


    # ---------------------------------------------------------------------
    # Reads data, preprocesses it and saves the transformer.
    # ---------------------------------------------------------------------
    def initiate_data_transformation(
        self,
        train_path,
        test_path
    ):

        try:

            # Read training dataset
            train_df = pd.read_csv(train_path)

            # Read testing dataset
            test_df = pd.read_csv(test_path)

            logging.info(
                "Reading train and test datasets completed."
            )

            logging.info(
                "Obtaining preprocessing object."
            )

            # Create preprocessing pipeline
            preprocessor_obj = self.get_transformer_obj()

            # Target column (label)
            target_column_name = "math_score"

            # Numerical columns
            numerical_columns = [
                "writing_score",
                "reading_score"
            ]

            # -----------------------------------------------------
            # Separate features and target from training dataset
            # -----------------------------------------------------
            input_feature_train_df = train_df.drop(columns=[target_column_name])

            target_feature_train_df = train_df[target_column_name]

            # -----------------------------------------------------
            # Separate features and target from testing dataset
            # -----------------------------------------------------
            input_feature_test_df = test_df.drop(columns=[target_column_name])

            target_feature_test_df = test_df[target_column_name]

            logging.info(
                "Applying preprocessing on train and test data."
            )

            # -----------------------------------------------------
            # Learn preprocessing parameters from training data
            # and transform it.
            # -----------------------------------------------------
            input_feature_train_arr = (preprocessor_obj.fit_transform(input_feature_train_df))

            # -----------------------------------------------------
            # Apply same learned preprocessing to testing data.
            # DO NOT fit again.
            # -----------------------------------------------------
            input_feature_test_arr = (preprocessor_obj.transform(input_feature_test_df))

            # -----------------------------------------------------
            # Concatenate transformed features with target column.
            # np.c_ joins arrays column-wise.
            # -----------------------------------------------------
            train_arr = np.c_[ input_feature_train_arr,
                np.array(target_feature_train_df)
            ]

            test_arr = np.c_[input_feature_test_arr,
                np.array(target_feature_test_df)
            ]

            logging.info(
                "Saving preprocessing object."
            )

            # Save fitted preprocessor for future prediction
            save_object(
                file_path=self.data_transformation_config
                .preprocessor_obj_file_path,
                obj=preprocessor_obj
            )

            # Return processed train data,
            # processed test data,
            # and saved preprocessor path.
            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )

        except Exception as e:

            raise customException(e, sys)