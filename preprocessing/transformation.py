from sklearn.base import BaseEstimator, TransformerMixin
import re
import pandas as pd
import numpy as np

class Transformation(BaseEstimator, TransformerMixin):
    """
    Description: Transform price feature to numerical values
                 Exracts maximum clock speed
                 Extracts RAM capacity from RAM feature
                 Fill nan values in Graphic Memory with 0. Also extracts numerical values from Graphic Memory
                 Fill nan values in Graphic Card with NO_GRAPHIC_CARD. Maps graphic cards as DEDICATED or INTEGRATED
                 Extract screen size in CM.
                 Fill null values in SSD_CAPACITY with NO_SSD and replace 16 GB with 512 GB
    """
    def fit(self, X, y=None):
        return self
    
    def transform(self, X):
        try:
            data = X.copy()
            data['price'] = data['price'].map(lambda x: float(x.replace(',','')))

            data['Clock_Speed'] = data['Clock_Speed'].map(self.extract_max)

            data['RAM'] = data['RAM'].map(lambda x: int(x.split(' ')[0]))

            data['Graphic_Memory'].fillna('0 GB', inplace=True)
            data['Graphic_Memory'] = data['Graphic_Memory'].map(lambda x: int(x.split(' ')[0]))


            data['Graphic_Processor'].fillna('NO_GRAPHIC_CARD', inplace=True)
            category_map = {}
            for processor in data['Graphic_Processor'].unique():
                zeroes = data[(data.Graphic_Processor == processor)&(data.Graphic_Memory == 0)].shape[0]
                non_zeroes = data[(data.Graphic_Processor == processor)&(data.Graphic_Memory != 0)].shape[0]
                percent = (zeroes)/(zeroes + non_zeroes)
    
                if percent > 0.8:
                    category_map[processor] = 'INTEGRATED'

                else:
                    category_map[processor] = 'DEDICATED'
  
            data['Graphic_Processor'] = data['Graphic_Processor'].map(lambda x: category_map[x])

            data['Screen_Size'] = data['Screen_Size'].map(self.extract_cm_value)
            data = self.impute_outliers_cm(data)

            data.loc[data.Screen_Resolution == '1080p pixel', 'Screen_Resolution']= '1080 x 1920'
            data.loc[data.Screen_Resolution == '1080 pixel', 'Screen_Resolution']= '1080 x 1920'
            data['Screen_Resolution'] = data['Screen_Resolution'].map(self.find_total_pixel)

            data['SSD_Capacity'] = data['SSD_Capacity'].fillna('NO_SSD')
            data.loc[(data.SSD_Capacity == '16 GB')|(data.SSD_Capacity == '8 GB'), 'SSD_Capacity'] = '512 GB'

            return data

        except Exception as e:
            raise Exception(f"Inside Transformation object:  inside transform function: {e}")





    def extract_max(self, string):
        """
        Description: Extract the maximum GHz value from string having CPU clock speeds values
                     The method is used in the feature Clock_Speed 
        Parameter: string = the feature string
        Return: float number 
        Example: extract_max('3.3 GHz upto max turbo frequency at 4.4 Ghz') returns 4.4
        """
       
        try:
            string = string.lower()
            pattern = r'[0-9]\.*[0-9]*(?=\s*ghz)'
            result = re.findall(pattern, string)
            result = [float(i) for i in result]
            return max(result)
        except:
            try:
                return float(string)
            except:
                return None

    def extract_cm_value(self, string):
        """
        Description: Extract the CM value of Screen Size
        Paramater: string = the feature string
        Return: cm value as float no.
        Example: extract_cm_value('90.32 cm (35.56 cm)') returns 35.56
        """
        try:
            pattern = r'[0-9]+\.*[0-9]*(?=\s*cm)'
            res = re.findall(pattern=pattern, string=string)
            res = pd.Series(res)
            res = res.map(lambda x: float(x))
            return min(res)

        except Exception as e:
            raise Exception(f"In Transformation.py: inside extract_cm_value: {e}")
        
    def impute_outliers_cm(self, data):
        """
        Description: Impute lower outliers with lower fence
        """
        X = data.copy()
        q1, q3 = np.quantile(X['Screen_Size'], q=[0.25, 0.75])
        IQR = q3 - q1
        lower = q1 - 1.5*IQR
        X.loc[X.Screen_Size < lower, 'Screen_Size'] = lower
        return X
    
    def find_total_pixel(self, string):
        """
        Description: Extracts total pixels from a screen resolution text
        Parameter: string = the feature string
        Return: Total pixel value in integer format
        Example: find_total_pixel('1920 x 1200 Pixel') returns 2304000 
                 If the data format is wrong it will return None
                 It will be imputed at later stage
        """
        try:
            pattern = r'([0-9]{3,4})[^0-9]+([0-9]{3,4})'
            res = re.findall(pattern, string)
            res = res[0]
            return int(res[0])*int(res[1])

        except Exception as e:
            return None

