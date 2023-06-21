 # Laptop Price Prediction
 ## Table of contents
  - [Problem statement](#problem-statement)
  - [Approach to solve the problem](#approach-to-solve-the-problem)
    1. [Data collection](#1-collecting-data)
    2. [Data preprocessing](#2-cleaning-analysing-and-preprocessing-the-data)
    3. [Regression model](#3-building-and-tuning-model-to-solve-the-price-prediction-problem)
    4. [Recommendation system](#4-build-a-simple-recommendation-system-to-recommend-similar-laptops)
  - [Project description and architecture](#project-architecture)
    - [Module webcrawler](#webcrawler)
    - [Module validation](#validation)
    - [Module preprocessing](#preprocessing)
    - [Module training](#training)
    - [Module recommendation](#recommendation)
    - [Module prediction](#prediction)
    - [Module logs](#logs)
 - [Technologies used](#technologies-used)
    
 5. How to run this project</a></p>
 6. Sample test results</a></p>
 
&nbsp;

 ## Problem Statement
 1. Suppose someone is planning to buy a laptop for his personal use and he has already decided the hardware configuration. Now the question is **what is the tentative budget he should consider**.
 2. Suppose he wants to buy a laptop with i3 processor with 32 GB RAM. But **such combination may not be available in the market.**
 
 In this project we will build a system which will predict expected price of a laptop based on hardware configuration and also recommend laptops having similar configuration available in the market.     
 
 &nbsp;
 
 ## Approach to solve the problem
 ### 1. Collecting data
 There are some datasets available on the internet to solve this problem, but the those datasets do not reflect the current price trend. As we know that price of any commodity varies with ups and down in the market it is always recommended to collect latest data to solve any commodity price prediction problem. **That is why we scraped data of available laptops from an e-commerce website**.
 
 ### 2. Cleaning, analysing and preprocessing the data
 The raw data collected looks like this - 
 
 ![image](https://github.com/arnabroy734/laptop_price_prediction/assets/86049035/423e4cca-03d6-4fa0-9500-d935923469b2)
 
 The data is cleaned first by extracting useful information (e.g., the maximum clock speed, screen size, resolution etc.). In this dataset our target variable is price of laptop, so relationships of different features with the target variable are also explored. After data cleaning the categorical variables are encoded to numerical forms by [target oriented feature encoding](https://medium.com/@aryamohapatra/target-encoding-create-some-relation-between-target-variable-and-the-encoded-labels-2ed0d172fceb).
 
 **Please refer the [EDA notebook](notebooks/EDA_On_Raw_Data.ipynb) for more details.**
 
 ### 3. Building and tuning model to solve the price prediction problem
 After preprocessing the data looks like this - 
 
 ![image](https://github.com/arnabroy734/laptop_price_prediction/assets/86049035/23df7dfb-aa81-4c25-9cff-6e7963c949c4)

We used the the dataset to build a regression model to predict price using the available features. We have done hyperparameter tuning on different models and saved the model as the best one which gives gives performance score. **We used [R2 score](https://benjaminobi.medium.com/what-really-is-r2-score-in-linear-regression-20cafdf5b87c) as performance metric.**

### 4. Build a simple recommendation system to recommend similar laptops
We have built a simple recommendation system which will recommend top 5 laptops having similarity with the configuration selected by the user. It is buit on [Nearest Neighbour](https://scikit-learn.org/stable/modules/neighbors.html) using [cosine similarity](https://en.wikipedia.org/wiki/Cosine_similarity)

&nbsp;

## Project Architecture
The project is divided into several modules where each module performs a predefined job. Below is the brief description of each module - 

### 1. webcrawler
The module scrapes data from e-commerce website in two steps - 
 - In step 1 the all the product urls and ids will be collected and saved in one file ([**productlinks.csv**](webcrawler/productlinks.csv))
 - In step 2 product specific details (e.g., processor name, SSD_Capacity) will be collected for each product url found in step 1. The data will be saved as [**raw.csv**](data/raw.csv).

### 2. validation
The module has two purposes.
 - [**validation_raw_data.py**](validation/validation_raw_data.py) validates the data from raw.csv file. It checks whether nan values are present in certain columns. If nan value is found the validation fails.
 - [**validation_prediction.py**](validation/validation_prediction.py) checks the input data for prediction. It checks the column names, ordering of the columns, data type for each column, presence of new category for categorical features. If either of the checks goes wrong the validated fails.
 
### 3. preprocessing
In this module separate classes are defined for separate purposed. For example, **DropDuplicates** class inside [**data_cleaning.py**](preprocessing/data_cleaning.py) drops all duplicate columns in the dataset. Each class is extention of **BaseEstimator, TransformerMixin**. So, each class has its own fit and transform method. This is done to create customised pipelines. 

There are three pipelines defined inside [**preprocessor_main.py**](preprocessing/preprocessor_main.py) - 
  - **DataCleaningPipeline** : to remove duplicate columns, to drop columns that are not required for model builing, extract numerical values from string data (e.g., extract screen size, clock speed, screen resolution), fill nan values in Graphics_Memory and SSD_Capacity columns
  - **EncodingPipeline**: to encode categorical values (Processor Name, SSD, GPU and Touchscreen) to numerical. The encoder model will be saved as **models/encoder.pkl** because it will be required during prediction.
  - **ImputerPipeline**: there will be some nan values in Clock_Speed and Screen_Resolution columns. Those values are imputed using [**KNN Imputer**](https://scikit-learn.org/stable/modules/generated/sklearn.impute.KNNImputer.html) technique.

After running all the pipelines the output data will be stored as [**preprocessed.csv**](data/preprocessed.csv)

### 4. training
In this module separate classes are created to build separate models. In each class the workflow is as follows - 
 - The parameters are defined for that model.
 - The preprocessed data is read, the data is then split in train and test
 - Hyperparameter tuning is done on the train data using [**grid search cv**](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.GridSearchCV.html)
 - The performance metric used is R2 score
 - The R2 score on test data is checked and the score is saved in application logs
 - The best model is also saved inside [**/models**](models)

Inside class **TrainBestModel** four mododels (**[Linear Model](https://scikit-learn.org/stable/modules/generated/sklearn.linear_model.Ridge.html), [Decision Tree](https://scikit-learn.org/stable/modules/generated/sklearn.tree.DecisionTreeRegressor.html), [Random Forest](https://scikit-learn.org/stable/modules/generated/sklearn.ensemble.RandomForestRegressor.html), [XGBoost](https://xgboost.readthedocs.io/en/stable/parameter.html)**) are used for hyperparameter tuning and the model having highest test score is chosed as the best one. The best model insformation is saved to application logs and the best model itself is saved inside [**/models**](models).

**As per latest training result XGBoost was selected as best model with test R2 score around 90%.** 

### 5. recommendation
The steps of building recommendation system are as follows:
 - dataset saved after **DataCleaningPipeline** is used for buiding recommendation system. 
 - Clock speed and screen size features are not used in recommendation system, so those columns are dropped. 
 - Every feature is converted to Categorical and then One Hot Encoding is done. 
 - The encoded data is then fit to [**NearestNeighbour**](https://scikit-learn.org/stable/modules/generated/sklearn.neighbors.NearestNeighbors.html#sklearn.neighbors.NearestNeighbors) model. Cosine similarity is used to find as the metric.
 - The Recommendation object is then saved inside [**/models**](models).

### 6. prediction
This module is used during runtime. Two separate classes are created inside this module - 
 - **PredictionPipeline** : de-serialises the encoder and best model objects, input data is first passed to encoder and then to best model for prediction.
 - **RecommendationPipeline** : de-serialises the Recommendation object, input data is fed to recommender and top five results are returned. 

### 7. logs
The purpose of this module is to save logs to database. Each log has a module name (e.g., training or preprocessing), timestamp, type (success or failure) and log message. During development the logs were stored as plain text file but it was migrated to MongoDB Atlas afterwards. The connection url is saved inside .env file which is not shared for security purpose.

## Technologies Used
#### 1. Web Scraping
<img src="https://scrapy.org/img/scrapylogo.png" width=300>
 
#### 2. Data preprocessing
<img src="https://pandas.pydata.org/static/img/pandas.svg" width=300>

#### 3. Data visualisation
<img src="https://matplotlib.org/stable/_images/sphx_glr_logos2_003.png" width=300>
<img src="https://seaborn.pydata.org/_images/logo-wide-lightbg.svg" width=300>
<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/8/8a/Plotly-logo.png/800px-Plotly-logo.png?20220718173326" width=300>

#### 4. ML model building
<img src="https://scikit-learn.org/stable/_static/scikit-learn-logo-small.png" width=300>
<img src="https://upload.wikimedia.org/wikipedia/commons/6/69/XGBoost_logo.png?20190625122704" width=300>

#### 5. Web application
<img src="https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.png" width=300>


 
 
