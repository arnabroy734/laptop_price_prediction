import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score, median_absolute_error, max_error, mean_squared_error
from logs.logger import App_Logger
from urls_and_paths.path import TRAIN_LOGS, MODELS
import pickle

class RandomForest:
  def __init__(self):
    """
    Description:
    Initialise the Random Forest Regressor, Grid Search CV and params
    """
    params = {
        'n_estimators' : range(80,200,10),
        # 'min_samples_split' : range(2,20,2),
        'max_features' : [5,6,7,9]

    }
    self.grid_search = GridSearchCV(estimator=RandomForestRegressor(n_jobs=-1), param_grid=params, cv=5, scoring='r2', verbose=3)

    

  def tune_parameter(self, data):
    """
    Description:
    1. Do train test split and tune hyperparameter by grid search
    2. Save CV score
    3. Save Test Score
    4. Serialise the model in .pkl format
    """
    # Split
    y = data['price']
    X = data.drop(['price'], axis=1)
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
    App_Logger().log(file_path=TRAIN_LOGS, log_message=f"Random Forest: Best Model: {self.best_model}")
    App_Logger().log(file_path=TRAIN_LOGS, log_message=f"Random Forest: CV Score: {self.cv_score}")
    App_Logger().log(file_path=TRAIN_LOGS, log_message=f"Random Forest: Test Score: {self.test_score}")

    # Save the model to ./models folder
    with open(MODELS['randomforest'], 'wb') as f:
      pickle.dump(self.best_model, f)
      f.close()
      App_Logger().log(file_path=TRAIN_LOGS, log_message=f"Random Forest: Model Saved: {MODELS['randomforest']}")




