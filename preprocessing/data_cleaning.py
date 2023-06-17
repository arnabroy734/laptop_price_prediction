from sklearn.base import BaseEstimator, TransformerMixin
from urls_and_paths.path import PROD_ID_AND_LINK

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
    product_id and product_link columns will be stored in separate file for future use
    """
    def fit(self, X, y=None):
        return self

    def transform(self, X):        
        dropcolumns = ['product_id', 'product_link', 'product_description', 'product_image', 'Processor_Generation', 'Refresh_Rate']
        data_copy = X.copy()
        data_copy[['product_id', 'product_link', 'product_description', 'product_image']].to_csv(PROD_ID_AND_LINK, index=False) # Save product id and link before dropping columns
        data_copy.drop(dropcolumns, inplace=True, axis=1)
        return data_copy
    

