import pandas as pd
from sklearn.model_selection import train_test_split
import xgboost as xgb
from xgboost import XGBRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score, median_absolute_error, max_error, mean_squared_error
from logs.logger import App_Logger
from urls_and_paths.path import TRAIN_LOGS, MODELS
import pickle

class Boosting:
  def __init__(self):
    """
    Description:
    Initialise the XGBoost Regressor, Grid Search CV and params
    """
    params = {

        'subsample' : [0.6, 0.7, 0.9, 1],
        'colsample_bytree' : [0.6, 0.7, 0.9, 1],
        'max_depth' : [5,6,7,8,9,10]

    }
    self.grid_search = GridSearchCV(estimator=XGBRegressor(objective='reg:squarederror', verbosity=0, booster='gbtree', n_estimators = 1000, learning_rate=0.01), 
                                        param_grid=params, cv=5, scoring='r2', verbose=3)

    

  def tune_parameter(self, data):
    """
    Description:
    1. Do train test split and tune hyperparameter by grid search
    2. Save CV score
    3. Save Test Score
    4. Serialise the model in .pkl format
    """
    # Split
    y = data['price'].values
    X = data.drop(['price'], axis=1).values
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=500)
    

    # Tune
    self.grid_search.fit(X_train, y_train)

    # CV score
    self.cv_score = self.grid_search.best_score_

    # Best model
    self.best_model = self.grid_search.best_estimator_

    # Test score
    y_pred = self.best_model.predict(X_test)
    self.test_score = r2_score(y_test, y_pred)

    # Save the training logs
    App_Logger().log(file_path=TRAIN_LOGS, log_message=f"XGBoost Regressor: Best Model: {self.best_model}")
    App_Logger().log(file_path=TRAIN_LOGS, log_message=f"XGBoost Regressor: CV Score: {self.cv_score}")
    App_Logger().log(file_path=TRAIN_LOGS, log_message=f"XGBoost Regressor: Test Score: {self.test_score}")

    # Save the model to ./models folder
    with open(MODELS['boosting'], 'wb') as f:
      pickle.dump(self.best_model, f)
      f.close()
      App_Logger().log(file_path=TRAIN_LOGS, log_message=f"XGBoost Regressor: Model Saved: {MODELS['boosting']}")




