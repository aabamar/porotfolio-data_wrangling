import numpy as np
import pandas as pd

'''
Case:
- You are a data analyst in a movie industry
- The product team ask you to recommend something new for a user to watch.
- You easily think of recommending the unwatched movies for a specific user Id.
- To recommend the unwatched movies nicely in the website, the engineering team needs you to return 3 things
  - `movieId`
  - `title`
  - `genres`
- Your task is to **create a function** to return the unwatched movies from a specific user id based on engineering team requirements.
-Data information:
  - `ratings.csv` contains the user activity after watching movies, i.e. give a rating to each movie they watched.
  - `movies.csv` contains the movie metadata (movie ID, title, and genre)
- The dataset originally comes from **MovieLens**
'''

def get_unwatched_movie(userId, config):
    '''
  Function to get unwatched movie from specific movie

  Parameters
  ----------
  userId (int)  :   The targeted user ID
  config (dict) :   The configuration files where the engineering team store
                    the user-data and movie metadata

  Returns
  --------
  unwatched_movie_df :  pandas DataFrame type with movieId as an index
                        and two columns of title and genres

    '''

    user_data_df = pd.read_csv(config['path']['user_data'], index_col='userId') # create user_data dataframe
    metadata_df = pd.read_csv(config['path']['metadata'], index_col='movieId')  # create metadata dataframe

    # create list of watched movie by specific user
    watched_movie_list = (user_data_df.loc[userId][['movieId']])['movieId'].values.tolist()

    # delete list of watched movie and remain the unwatched movie
    unwatched_movie_df = metadata_df.drop(watched_movie_list)
    return unwatched_movie_df # return data

'Input Example'
# Define CONFIG variable
CONFIG = {
    'path': {
        'user_data': 'ratings.csv',
        'metadata': 'movies.csv'
    }
}

unwatched_data = get_unwatched_movie(userId = 10,
                                     config = CONFIG)

print('Data shape:', unwatched_data.shape)
unwatched_data.sample(n=5, random_state=42)