from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.preprocessing import MinMaxScaler
from sklearn.impute import KNNImputer
import pandas as pd



class CloclSpeedNanImputer (BaseEstimator, TransformerMixin):
  def fit(self, X, y=None):
    return self

  def transform(self, X):
    scaler = MinMaxScaler()
    data_transformed  = scaler.fit_transform(X)
    imputer = KNNImputer()
    data_transformed = imputer.fit_transform(data_transformed)
    data_original = scaler.inverse_transform(data_transformed)
    data_original = pd.DataFrame(data_original, columns=X.columns)
    return data_original