import numpy as np
import pandas as pd

'''
Case:
- You are given a dataset of guests and hosts of AirBnB.
- This dataset contains the review given by a guest (`id`) to the listing.
- You want to analyze the review given by the guests by `neighborhood group`.
- But the data is not clean.
- Please clean the data by
  1. Dropping data with missing value
  2. Removing the unconsitency in `neighborhood group`
  3. Dropping the listing outliers/anomaly.
    - listing with anomaly rent price (please use IQR method to filter the outlier).
    - listing with anomaly `availability 365` (`availability 365` is defined as an indicator of the total number of days the listing is available for during the year)
  4. Drop duplicates data (if any)
'''

airbnb_data = pd.read_csv("Airbnb_Open_Data.csv") # import data

# delete data in 'neighbourhood group' and 'price' column with missing value
airbnb_data = airbnb_data.dropna(subset=['neighbourhood group', 'price'])

# Removing the unconsitency value in 'neighborhood group'
map_value_ng = {
    'brookln' : 'Brooklyn',
    'manhatan' : 'Brooklyn'
}
airbnb_data['neighbourhood group'] = airbnb_data['neighbourhood group'].replace(map_value_ng)

# convert value in 'price' column into int for handling outlier
airbnb_data['price'] = airbnb_data['price'].str.replace('$', '')
airbnb_data['price'] = airbnb_data['price'].str.replace(',', '')
airbnb_data['price'] = airbnb_data['price'].astype('int')

# handle outlier using IQR method and replace outlier with median value
upper_limit_price = airbnb_data['price'].quantile(q=0.75) * 1.5
median_price = airbnb_data['price'].median()
airbnb_data.loc[airbnb_data['price'] > upper_limit_price, 'price'] = median_price

# handle outlier with delete data in column 'availability 365', value in this column
# has to be in range 0-365
avail_365_condition = airbnb_data[(airbnb_data['availability 365'] > 365) | (airbnb_data['availability 365'] < 0) ].index
airbnb_data.drop(avail_365_condition, inplace=True)
airbnb_data = airbnb_data.dropna(subset=['availability 365'])

# delete duplicates data
airbnb_data = airbnb_data.drop_duplicates(keep='first')

# print message contain shape of cleaned data
print(f'Clean data shape : {airbnb_data.shape}')
