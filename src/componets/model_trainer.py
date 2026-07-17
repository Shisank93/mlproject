import os  , sys 
from dataclasses import dataclass

from catboost import CatBoostRegressor
from sklearn.ensemble import (
    AdaBoostRegressor ,
    GradientBoostingRegressor , 
    RandomForestRegressor
)

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor
from xgboost import XGBRegressor

from src.exception import customException
from src.logger import logging
from src.utils import save_object , evaluate_models

# The dataclass decorator automatically generates special methods like __init__() and __repr__() for the class.
@dataclass

# This class stores configuration values for the model trainer.
class ModelTrainerConfig:
    # Defines the file path where the trained model will be saved.
    train_model_file_path:str = os.path.join('artifacts' , 'model.pkl')


# This class handles the training process and saving of the machine learning model.
class ModelTrainer:
    # Initializes the ModelTrainer with configuration settings.
    def __init__(self):
        # Creates an instance of the configuration class to access config values.
        self.model_trainer_config  = ModelTrainerConfig()

    # Main method responsible for training different models and evaluating their performance.
    def initiate_model_training(self , train_arr , test_arr):
        # Handle exceptions to prevent the program from crashing unexpectedly.
        try:
            # Logging that training and testing data are being prepared (split into features and targets).
            logging.info("splitting training and test input data ")
            # Separating features and target variable from training and testing arrays.
            X_train , y_train , X_test , y_test =(
                train_arr[: , :-1] , 
                train_arr[:,-1] ,
                test_arr[: , :-1] , 
                test_arr[: , -1]
            )

            # Creating multiple regression models for comparison to find the best one.
            models = {
                'Random Forest':RandomForestRegressor() ,  # Ensemble of decision trees using bagging.
                'Decision Tree':DecisionTreeRegressor(),   # Single decision tree model.
                'gradient Boosting':GradientBoostingRegressor() ,  # Boosted trees to reduce errors.
                "Linear Regressor": LinearRegression() ,  # Simple linear relationship model.
                "XGboosting regressor":XGBRegressor() ,  # Gradient boosting optimized for speed.
                "CatBoosting Regressor": CatBoostRegressor() ,  # Gradient boosting with categorical feature support.
                "AdaBoost Regressor": AdaBoostRegressor()  # Boosting that focuses on hard-to-predict samples.
            }
            params={
                "Decision Tree": {
                    'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                    # 'splitter':['best','random'],
                    # 'max_features':['sqrt','log2'],
                },
                "Random Forest":{
                    # 'criterion':['squared_error', 'friedman_mse', 'absolute_error', 'poisson'],
                 
                    # 'max_features':['sqrt','log2',None],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "gradient Boosting":{
                    # 'loss':['squared_error', 'huber', 'absolute_error', 'quantile'],
                    'learning_rate':[.1,.01,.05,.001],
                    'subsample':[0.6,0.7,0.75,0.8,0.85,0.9],
                    # 'criterion':['squared_error', 'friedman_mse'],
                    # 'max_features':['auto','sqrt','log2'],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "Linear Regressor":{},
                "XGboosting regressor":{
                    'learning_rate':[.1,.01,.05,.001],
                    'n_estimators': [8,16,32,64,128,256]
                },
                "CatBoosting Regressor":{
                    'depth': [6,8,10],
                    'learning_rate': [0.01, 0.05, 0.1],
                    'iterations': [30, 50, 100]
                },
                "AdaBoost Regressor":{
                    'learning_rate':[.1,.01,0.5,.001],
                    # 'loss':['linear','square','exponential'],
                    'n_estimators': [8,16,32,64,128,256]
                }
            }

            # Train and evaluate each model, returning a report with their performance scores.
            model_report:dict =  evaluate_models(X_train = X_train , y_train=y_train ,X_test = X_test ,y_test=y_test 
                                                 , models = models , params = params)

            # Select the highest R² score from all evaluated models.
            best_model_score = max(sorted(model_report.values()))

            # Find the model name that corresponds to the best score.
            best_model_name = list(model_report.keys())[
                list(model_report.values()).index(best_model_score)
            ]

            # Retrieve the actual model object based on the best model name.
            best_model = models[best_model_name]

            # Enforce a minimum acceptable performance threshold; raise error if not met.
            if best_model_score<0.6:
                raise customException("NO Best Model Found")
            # Log that the best model has been successfully identified.
            logging.info(f"Best found model on both train and testing dataset")
            # Serialize and save the trained model to disk for future use in predictions.
            save_object(
                file_path=self.model_trainer_config.train_model_file_path , 
                obj = best_model
            )

            # Use the best model to make predictions on the unseen test data.
            predicted=best_model.predict(X_test)

            # Calculate the R² score to measure how well predictions match the true values.
            r2_square = r2_score(y_test , predicted)

            # Return the final evaluation metric to the caller.
            return r2_square

        # Catch any unexpected errors during training or evaluation.
        except Exception as e :
            # Wrap the original exception in the project's custom exception class for better error handling.
            customException(e , sys)