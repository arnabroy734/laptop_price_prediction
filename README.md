 # Laptop Price Prediction
 ## Table of contents
  - [Problem statement](#problem-statement)
  - [Approach to solve the problem](#approach-to-solve-the-problem)
 3. Project description and architecture</a></p>
 4. Technologies used</a></p>
 5. How to run this project</a></p>
 6. Sample test results</a></p>
 
&nbsp;

 ## Problem Statement
 1. Suppose someone is planning to buy a laptop for his personal use and he has already decided the hardware configuration. Now the question is **what is the tentative budget he should consider**.
 2. Suppose he wants to buy a laptop with i3 processor with 32 GB RAM. But **such combination may not be available in the market.**
 
 In this project we will build a system which will predict expected price of a laptop based on hardware configuration and also recommend laptops having similar configuration available in the market.     
 
 ## Approach to solve the problem
 ### 1. Collecting data
 There are some datasets available on the internet to solve this problem, but the those datasets do not reflect the current price trend. As we know that price of any commodity varies with ups and down in the market it is always recommended to collect latest data to solve any commodity price prediction problem. **That is why we scraped data of available laptops from an e-commerce website**.
 
 ### 2. Analysing and cleaning the data
 The raw data collected looks like this - 
 ![image](https://github.com/arnabroy734/laptop_price_prediction/assets/86049035/423e4cca-03d6-4fa0-9500-d935923469b2)
 The data is cleaned first by extracting useful information (e.g., the maximum clock speed, screen size, resolution etc.). In this dataset our target variable is price of laptop, so relationships of different features with the target variable are also explored. After data cleaning the categorical variables are encoded to numerical forms by [target oriented feature encoding](https://medium.com/@aryamohapatra/target-encoding-create-some-relation-between-target-variable-and-the-encoded-labels-2ed0d172fceb).


 
 
