from sklearn.base import BaseEstimator, TransformerMixin

class DropDuplicates(BaseEstimator, TransformerMixin):
    """
    Description: This method will drop all the duplicate rows in the dataset
    """
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        
        data_copy = X.copy()
        data_copy.drop_duplicates(inplace=True)
        return data_copy


class DropColumns(BaseEstimator, TransformerMixin):
    """
    Description: Drop rows from Dataframe and return the Dataframe
    Parameters: transform(X) where X is a Dataframe
    Return: Dataframe
    Columns to be dropped: product_id, product_link, Processor_Generation, Refresh_Rate
    """
    def fit(self, X, y=None):
        return self

    def transform(self, X):
        
        dropcolumns = ['product_id', 'product_link', 'Processor_Generation', 'Refresh_Rate']
        data_copy = X.copy()
        data_copy.drop(dropcolumns, inplace=True, axis=1)
        return data_copy
    

