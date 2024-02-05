import numpy as np
import pandas as pd

'''
Case:
- Given a dataset of sales report by date, **calculate the mont-over-month percentage change in sales**.
- The output should include the year-month date (YYYY-MM) and percentage change, 
rounded to the 2nd decimal point, and sorted by `order-date` in ascending order.
'''

# import data
filename = 'Global_Superstore2.csv'
superstore_data = pd.read_csv(filename,
                                 engine = 'python',
                                 encoding = 'cp1252', parse_dates=['Order Date'])

# conver data in column 'Order Date' (datetime) into 'yyyy-mm' format
superstore_data['Order Date'] = superstore_data['Order Date'].dt.strftime('%Y-%m')

# crate new dataframe contain only column 'Order Date' & 'Sales' which already added up
# for each month
superstore_monthly_sales = superstore_data[['Order Date', 'Sales']].groupby('Order Date').sum().reset_index()

# calculate Month-Over-Month Percentage Change and added it up to new column 'Sales Change'
superstore_monthly_sales['Sales Change'] = round(superstore_monthly_sales['Sales'].pct_change() *100, 2)

print(f"Data shape : {superstore_monthly_sales.shape}") # print message contain data shape
superstore_monthly_sales.head(12) # display 12 first row of data
