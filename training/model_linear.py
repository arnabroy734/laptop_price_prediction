import pandas as pd
from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score, median_absolute_error, max_error, mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from sklearn.pipeline import Pipeline
from logs.logger import App_Logger
from urls_and_paths.path import TRAIN_LOGS, MODELS
import pickle

class LinearReg:
  def __init__(self):
    """
    Description:
    Initialise the Ridge Model, Grid search CV and parameters, MinMaxscaler
    """
    params = {
        'alpha': [0.001, 0.005, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 50, 100, 500]
    }
    self.grid_search = GridSearchCV(estimator=Ridge(), param_grid=params, cv=5, scoring='r2', verbose=3)
    self.scaler = MinMaxScaler()

    

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
    
    # Normalise
    X_train = self.scaler.fit_transform(X_train)
    
    # Tune
    self.grid_search.fit(X_train, y_train)

    # CV score
    self.cv_score = self.grid_search.best_score_

    # Best model
    self.best_model = Pipeline([
        ('scaler', self.scaler),
        ('model', self.grid_search.best_estimator_)
    ])

    # Test score
    y_pred = self.best_model.predict(X_test)
    self.test_score = r2_score(y_test, y_pred)

    # Save the training logs
    App_Logger().log(module="training", msg_type='success', message=f"Linear Ridge: Best Model: {self.best_model}")
    App_Logger().log(module="training", msg_type='success', message=f"Linear Ridge: CV R2 Score: {self.cv_score}")
    App_Logger().log(module="training", msg_type='success', message=f"Linear Ridge: Test R2 Score: {self.test_score}")

   

    # Save the model to ./models folder
    with open(MODELS['linear'], 'wb') as f:
      pickle.dump(self.best_model, f)
      f.close()
      App_Logger().log(module="training", msg_type='success', message=f"Linear Ridge: Model Saved: {MODELS['linear']}")




