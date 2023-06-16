import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score, median_absolute_error, max_error, mean_squared_error
from sklearn.tree import DecisionTreeRegressor
from sklearn.pipeline import Pipeline
from logs.logger import App_Logger
from urls_and_paths.path import TRAIN_LOGS, MODELS
import pickle

class Decision:
  def __init__(self):
    """
    Description:
    Initialise the Decision Tree Regressor, Grid Search CV and params
    """
    params = {
        'max_depth' : range(10,500,5),
        'min_samples_split' : range(2,30,1)

    }
    self.grid_search = GridSearchCV(estimator=DecisionTreeRegressor(), param_grid=params, cv=5, scoring='r2')

    

  def tune_parameter(self, data):
    """
    Description:
    1. Do train test split and tune hyperparameter by grid search
    2. Save CV score
    3. Save Test Score
    
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
    App_Logger().log(file_path=TRAIN_LOGS, log_message=f"Decision Tree: Best Model: {self.best_model}")
    App_Logger().log(file_path=TRAIN_LOGS, log_message=f"Decision Tree: CV Score: {self.cv_score}")
    App_Logger().log(file_path=TRAIN_LOGS, log_message=f"Decision Tree: Test Score: {self.test_score}")

    # Save the model to ./models folder
    with open(MODELS['decision'], 'wb') as f:
      pickle.dump(self.best_model, f)
      f.close()
      App_Logger().log(file_path=TRAIN_LOGS, log_message=f"Decision Tree: Model Saved: {MODELS['decision']}")




