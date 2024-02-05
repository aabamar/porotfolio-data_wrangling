import numpy as np
import pandas as pd

'''
Case:
- Assume you work as a Data Analyst in Travelio.
- The product team request you to give its users housing recommendations based on their current location and housing preferences.
- Please create a function to answer the product team request.
- **Note**: The dataset is scrapped by Pacmann from the Travelio website for educational purposes only.
'''

def haversine(lat1, lon1, lat2, lon2):
    '''
  Function to get distance from two location using
  longitude & latitude value from each location

  Parameters
  ----------
  lat1 (float)  :   first location latitude value
  lon1 (float)  :   first location longitude value
  lat2 (float)  :   second location latitude value
  lon2 (float)  :   ssecond location longitude value

  Returns
  --------
  distance :  distance between two location in kilometer
    '''

    from math import radians, cos, sin, atan2, sqrt

    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2]) # convert value to radian

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    r = 6371 # Radius of earth in kilometers. Use 3956 for miles. Determines return value units.
    return c * r # return distance in kilometers

def get_user_recommendation(n, user_config, data_config):
    '''
  housing recommendation for a specific user location & preferences sorted
  by the nearest distance between user location and house location.

  Parameters
  ----------
  n (int)           : the maximum number of recommendation.
  user_config (dict): the user configuration data. It contains the user
                      preferences and user current location.
  data_config (dict): the data configuration that contains the housing data path.

  Returns
  --------
  data_reccomendation :  dataframe with housing reccomendation by user preference
     '''

    data = pd.read_csv(data_config['path']) # import data

    # define longitude and latitude for haversine formula
    lat_user, lon_user = user_config['location']['latitude'], user_config['location']['longitude']

    dist = [] # create empty list for distance value
    # calculate distance value using haversine formula
    for lat_data, lon_data in zip(list(data['latitude']), list(data['longitude'])):
        dist.append(haversine(lat1 = lat_user, lon1 = lon_user, lat2 = lat_data, lon2 = lon_data))

    data["distance from user"] = dist # import distance value to dataframe
    data.sort_values(by=['distance from user'], inplace=True) # sort data by distance
    data.drop('distance from user',axis=1, inplace=True) # delete distance value from dataframe

    # filtering data using user preference
    for key, value in user_config['preferences'].items():

        if value != None:
            if key == 'property_type' or key == 'is_furnished':
                data = data[data[key] == value]
            elif key == 'size' or key == 'capacity':
                data = data[data[key] >= value]
            elif key == 'yearly_price':
                data = data[data[key] <= value]

    data_reccomendation = data.head(n) # give reccomendation data based on user preference

    return data_reccomendation # return data

'Input Example'
# Define CONFIG variable
user_config = {
    'preferences': {
        'property_type': None,
        'size': 30.0,
        'capacity': 2,
        'is_furnished': 'Full Furnished',
        'yearly_price': 50000000
    },
    'location': {
        # Dekat Bintaro Plaza
        'latitude': -6.2734,
        'longitude': 106.7364
    }
}

data_config = {
    'path': 'travelio_dki_jakarta.csv'
}

# Run the function
user_recommendation = get_user_recommendation(n = 10,
                                              user_config = user_config,
                                              data_config = data_config)

# Validate
print('Data Shape:', user_recommendation.shape)
user_recommendation