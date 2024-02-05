import numpy as np
import pandas as pd

'''
Case:
- Toko Serba Ada has several branches across the country.
- Toko Serba Ada manager wants to merge the transactions data across branches.
- Your task is to create a function to join multiple transaction files.
'''

def import_data(filenames):
    '''
  Function to combine separated data (supported .csv & .xlxs only)

  Parameters
  ----------
  filenames : list
     separated file name

  Returns
  --------
  data : dataframe
      combine data

    '''

    data_csv, data_excel = [], [] # create empty list for collecting data from each format

    for filename in filenames: # collecting data for each format

        if ".csv" in filename:
            data_csv.append(pd.read_csv(filename, sep=';'))
        elif ".xlsx" in filename:
            data_excel.append(pd.read_excel(filename))
        else:
          print('format not available, please use .csv or .xlsx only')

    # combine data for each format
    data_csv = pd.concat(data_csv, ignore_index=True)
    data_excel = pd.concat(data_excel, ignore_index=True)

    # combine for all data available
    data = pd.concat([data_excel, data_csv])
    return data #return data

'Input Example'
filenames = [
    'branch_A.xlsx',
    'branch_B.csv',
    'branch_C.csv'
]

# Import data
data = import_data(filenames = filenames)

# Validasi hasil
print('Data shape:', data.shape)
data.head(5)