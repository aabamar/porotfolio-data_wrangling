import numpy as np
import pandas as pd
from datetime import date,datetime

import seaborn as sns
import matplotlib.pyplot as plt

'''
Case:
- You are given a dataset of Online Store Retail Orders .
- The dataset contains 2 tables: `orders` and `product supplier`. You can join the tables on `Product ID`
- Your task is answer business questions below.
- But the data is not clean. Please **clean the data** by :
  1. Removing the unconsistency in `Customer Status`
  2. Dropping data with missing value (if any)
  3. Drop duplicates data (if any)
- Then, please **answer these business questions and give recommendations (you can also give some insights if you find something interesting)**:
  1. Which product has the highest profit percentage?
  2. How much profit obtained month over month of every year?
  3. Does the lower the cost, the higher the profit? Does the cheaper the price the more people buy?
  4. Show the top 3 of the most favorite product in the latest year
  5. Find the tendency and the longest of order-to-delivery length for every month in the latest year (please use a proper measure of central tendency). 
  Order-to-delivery length is defined as how much days was taken to deliver from order date of customer.
  6. The owner of store want to give discount promo. But, the promo is only for the active loyal customer. 
  Help the owner find the unique `customer ID` of loyal customers and show the proportion of their status. 
  Definition of active loyal customer is the customer who order more than 3 times and order in 3 latest months.
'''

# input data
data_orders = pd.read_csv('orders.csv')
data_product = pd.read_csv('product_supplier.csv')

# convert column Date Order was placed and Delivery Date into datetime64
data_orders['Date Order was placed'] = pd.to_datetime(data_orders['Date Order was placed'], dayfirst=True)
data_orders['Delivery Date'] = pd.to_datetime(data_orders['Delivery Date'], dayfirst=True)

# combine data based on Product ID
data = pd.merge(data_orders, data_product, on='Product ID')

# remove inconsistency from column Customer Status
replace_map = {
    'SILVER' : 'Silver',
    'GOLD' : 'Gold',
    'PLATINUM' : 'Platinum'
}
data['Customer Status'] = data['Customer Status'].replace(replace_map)

# create new column for Month and Year for help data selection
data['Month'] = data['Date Order was placed'].dt.month
data['Year'] = data['Date Order was placed'].dt.year

# add column unit price from column Total Retail Price for This Order divide by Quantity Ordered
data['Unit Price'] = data['Total Retail Price for This Order'] / data['Quantity Ordered']
# add column unit price from column Unit price minus cost price per unit
data['Profit'] = data['Unit Price'] - data['Cost Price Per Unit']
# add column profit percentage from profit divide by cost price per unit
data['Profit Percentage'] = data['Profit'] / data['Cost Price Per Unit']*100

# show figure for top 5 product category with biggest profit percentage
data_profit_percentage = data[['Product Category', 'Profit Percentage']].groupby('Product Category').mean() # create new dataframe with grouped product category and contain profit percentage
plt.figure(figsize=(8,4)) # create figure size
sns.barplot(data= data_profit_percentage.nlargest(5, 'Profit Percentage'), # create figure with top 5 profit percentage in product category
            x = 'Product Category',
            y = 'Profit Percentage',
            hue= 'Product Category')
x=[]
for y in range(0,201,25): # create sequence number for profit percentage ticks
    x.append(y)
plt.yticks(x)
plt.show()

# show figure for profit obtained month over month of every year

data_profit_MoM = data[['Date Order was placed', 'Profit']]
data_profit_MoM['Date Order was placed'] = data_profit_MoM['Date Order was placed'].dt.strftime('%Y-%m')
data_profit_MoM = data_profit_MoM.groupby('Date Order was placed').sum().reset_index()
data_profit_MoM['Date Order was placed'] = pd.to_datetime(data_profit_MoM['Date Order was placed'], yearfirst=True)

plt.figure(figsize=(6,4))
sns.lineplot(data = data_profit_MoM,
             x = data_profit_MoM['Date Order was placed'].dt.month,
             y = 'Profit',
             hue= data_profit_MoM['Date Order was placed'].dt.year)
plt.xlabel('Month')
plt.ylabel('profit')

plt.show()

# create sub-plots for correlation figure
fig, ax = plt.subplots(nrows = 1, ncols = 2, figsize=(8,4))

# show figure for correlation between cost and profit
sns.scatterplot(data=data,
                x = 'Cost Price Per Unit',
                y = 'Total Retail Price for This Order',
                ax = ax[0])


# show figure for correlation unit price and unit ordered
sns.scatterplot(data=data,
                y = 'Quantity Ordered',
                x = 'Unit Price',
                ax= ax[1])
ax[0].set_ylabel('profit')
plt.show()

# show figure for top 3 product category with most quantity ordered
data_quantity_ordered = data[['Product Category', 'Quantity Ordered']][data['Year'] == 2021].groupby('Product Category').sum()
sns.barplot(data= data_quantity_ordered.nlargest(3, 'Quantity Ordered'),
            x = 'Product Category',
            y = 'Quantity Ordered',
            hue= 'Product Category')
plt.show()

# show figure for order-to-delivery length of every month in the latest year
data_order_delivery = data[['Date Order was placed', 'Delivery Date']][data['Year'] == 2021] # filtering data for the latest year
data_order_delivery['order to delivery length'] = data_order_delivery['Delivery Date'] - data_order_delivery['Date Order was placed'] # create new column contain length time for order to delivery

data_order_delivery['Date Order was placed'] = data_order_delivery['Date Order was placed'].dt.strftime('%m')

data_order_delivery = data_order_delivery[['Date Order was placed', 'order to delivery length']].groupby('Date Order was placed').agg(['median', 'max']).reset_index()

data_order_delivery.columns = ['Month', 'order_to_delivery_length', 'the_longest_order_to_delivery_length']
data_order_delivery.set_index('Month', inplace=True)
display(data_order_delivery)

# Show figure for proportion of active loyal customer and list of active loyal customer

data_customer = data[['Customer ID', 'Customer Status']].loc[(data['Year'] == 2021) & (data['Month'] > 9)] # filtering data for the latest year and last 3 month

# count total orders for each customer
cust_id = data_customer['Customer ID'].value_counts().keys().tolist()
count = data_customer['Customer ID'].value_counts().to_list()
cust_count = {'Customer ID' :  cust_id,
              'Order Count' : count}
order_count = pd.DataFrame(data=cust_count)
data_customer_count = pd.merge(data_customer, order_count, on='Customer ID')

data_customer_count = data_customer_count[['Customer ID', 'Customer Status']].loc[data_customer_count['Order Count'] > 3] # filtering customer with more than 3 total orders

# Create additional column for help define proportion of customer status
data_customer_count['Customer Status (num)'] = data_customer_count['Customer Status']
replace_map = {
    'Silver' : 1,
    'Gold' : 2,
    'Platinum' : 3
}
data_customer_count['Customer Status (num)'] = data_customer_count['Customer Status (num)'].replace(replace_map)

data_customer_count = data_customer_count.groupby('Customer ID').max().reset_index() # group customer with most high customer status for each customer

# create table contain active loyal customer
data_customer = data_customer_count.drop(['Customer Status', 'Customer Status (num)'], axis=1)
display(data_customer)

# count proportion of customer status in active loyal customer
data_customer_proportion = data_customer_count[['Customer Status', 'Customer ID']].groupby('Customer Status').nunique().reset_index()
data_customer_proportion['percentage'] = (data_customer_proportion['Customer ID'] / data_customer_proportion['Customer ID'].sum()) * 100

# create figure for proportion of active loyal customer
sns.barplot(data=data_customer_proportion.sort_values(by=['Customer ID'], ascending=False),
            x= 'Customer Status',
            y = 'percentage',
            hue='Customer Status')