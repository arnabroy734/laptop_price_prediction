from sklearn.base import BaseEstimator, TransformerMixin

class ProcessorEncoding(BaseEstimator, TransformerMixin):
  """
  Description: 
  1. Here the processor name will be encoded as per target.
  2. The processor having low average price will be assigned a lower rank
  3. The processor having high average price will be assigned a higher rank
  """
  def fit(self, X, y=None):
    ascending_index = list(X.groupby('Processor_Name')['price'].median().sort_values().index)
    self.encoding = {}
    for idx, processor in enumerate(ascending_index):
      self.encoding[processor] = idx + 1
    return self

  def transform(self, X):
    X_copy = X.copy()
    X_copy['Processor_Name'] = X_copy['Processor_Name'].map(lambda x: self.encoding[x])
    return X_copy


class SSD_Encoding (BaseEstimator, TransformerMixin):
  """
  Description: 
  1. Here the SSD capacity will be encoded as per target.
  2. The SSD having low average price will be assigned a lower rank
  3. The SSD having high average price will be assigned a higher rank
  """
  def fit(self, X, y=None):

    ascending_index = list(X.groupby('SSD_Capacity')['price'].median().sort_values().index)
    self.encoding = {}
    for idx, SSD in enumerate(ascending_index):
      self.encoding[SSD] = idx + 1
    return self

  def transform(self, X):
    X_copy = X.copy()
    X_copy['SSD_Capacity'] = X_copy['SSD_Capacity'].map(lambda x: self.encoding[x])
    return X_copy


class GPUEncoding (BaseEstimator, TransformerMixin):
  def fit(self, X, y=None):
    self.encoding = {
        "INTEGRATED" : 0,
        "DEDICATED" : 1
    }

    return self

  def transform(self, X):
    X_copy = X.copy()
    X_copy['Graphic_Processor'] = X_copy['Graphic_Processor'].map(lambda x: self.encoding[x])
    return X_copy


class TouchscreenEncoding (BaseEstimator, TransformerMixin):
  def fit(self, X, y=None):
    self.encoding = {
        "Yes" : 1,
        "No" : 0
    }

    return self

  def transform(self, X):
    X_copy = X.copy()
    X_copy['Touchscreen'] = X_copy['Touchscreen'].map(lambda x: self.encoding[x])
    return X_copy