import numpy as np
import pandas as pd

'''
Case:
- Assumed you are a data analyst in Amazon.
- Your supervisor ask you to export a promising state sales data based on its market share to a .csv files, thus each state representatives can analyst the sales data further.
- A promising state is a state that has its market share bigger or equal to a specified threshold.
- The market share of a specific state is defined as number of order on a specific state / total order.
- Write a function to help your supervisor!
'''

def export_promising_state(config_file, thresh):
  '''
  export a promising state sales data based on its market share to a .csv files,
  thus each state representatives can analyst the sales data further.

  Parameters
  ----------
  config_file (dict) : contains the input and output path
  thresh (float)     : contains the given market share threshold.

  Returns
  --------
  none
  '''

  data = pd.read_csv(config_file['path']['input'], index_col='index') # import data

  data['ship-state'] = data['ship-state'].str.lower() # remove inconsistency value from 'ship-state' column

  # define promising state by calculate each state market share and create alist contain
  # promising state (state with market share above thresh value)
  states_sales_data = data[['ship-state', 'Order ID']].groupby('ship-state').count()
  states_sales_data['market-share'] = states_sales_data['Order ID'] / states_sales_data['Order ID'].sum()
  promising_state_data = states_sales_data[states_sales_data['market-share'] >= thresh].reset_index()
  promising_state = list(promising_state_data['ship-state'])

  if len(promising_state) == 0:
    print('No promising state') # print message if no state had market share value above thresh
  else:
    for state in promising_state: # export each promising state separatedly into designated folder
      file_name = state + '-sales-reports.csv'
      path_file = config_file['path']['output'] + file_name
      state_data = data[data['ship-state'] == state]
      state_data = state_data.drop(['Unnamed: 22'], axis=1)
      state_data.to_csv(path_file.lower(), index=False)

      # calculate each market share in percentage
      state_market_share = (states_sales_data.loc[state]['market-share'])*100
      state_market_share = round(state_market_share, 2)

      # print message contain state data shape & state market share if file succesfully exported
      print(f'Data of state "{state.lower()}" was successfully exported into "{path_file.lower()}"')
      print(f'  - State market share :  {state_market_share} %')
      print(f'  - Data shape         :  {state_data.shape}\n')

'Input Example'
# Define CONFIG variable
config_file = {
    'path': {
        'input': 'Amazon Sale Report.csv',
        'output': 'sales_data/'
    }
}

export_promising_state(config_file = config_file,
                       thresh = 0.10)