import numpy as np
import pandas as pd

'''
Case:
- Given a dataset of an e-commerce events history in Electronic shop.
- Your task is to
  1. **calculate each user's time to purchase duration** and
  2. **find the tendency of user view-purchase duration** (please use a proper measure of central tendency).
- Time to purchase duration is defined as the time difference between `view` event and `purchase` event. Consider only the earliest view and purchase.
- The ouput should include `user_id` and their `view_purchase_duration` in minutes.
'''

data = pd.read_csv('event_samples.csv', parse_dates=['event_time']) # import data

# split data for 'view' & 'purchase', each data contain column 'event_time' & 'user_id'
view_data = data[['event_time', 'user_id']].loc[data['event_type'] == 'view']
purchase_data = data[['event_time', 'user_id']].loc[data['event_type'] == 'purchase']

# define earliest data for each user for purchase data
purchase_data = purchase_data.groupby('user_id').max().reset_index()
# formula & calculation for view data is still wrong, because it still not define earliest
# value before user purchase. i hope i can get some enlightment for this one from checker mentor
# because iam already stuck
view_data = view_data.groupby('user_id').min().reset_index()

# rename column for event_time column for each view and purchase data (preparation for data merging)
view_data.rename(columns= {'event_time' : 'event_time_view'}, inplace=True)
purchase_data.rename(columns= {'event_time' : 'event_time_purchase'}, inplace=True)

# merge purchase and view data
view_to_purchase = pd.merge(purchase_data, view_data, on='user_id')

# calculate difference / view to purchase time for each user
view_to_purchase['view_purchase_duration'] = round((view_to_purchase['event_time_purchase'] - view_to_purchase['event_time_view']) / pd.Timedelta(minutes=1), 3)

# delete event_time column from each data
view_to_purchase.drop(['event_time_purchase', 'event_time_view'], axis=1, inplace=True)

# delete difference / view to purchase time with less than 0 value
view_to_purchase.drop(view_to_purchase[view_to_purchase['view_purchase_duration'] < 0].index, inplace=True)

# calculate central tendency for difference / view to purchase time value
median_view_to_purchase = round(view_to_purchase['view_purchase_duration'].median(), 1)

# print message contain data shape & central tendency value (median)
print(f'Data shape : {view_to_purchase.shape}')
print(f"Summary of user's view to purchase duration : {median_view_to_purchase} minutes")
