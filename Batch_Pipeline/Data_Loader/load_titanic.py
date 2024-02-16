import io
import pandas as pd
import requests
from pandas import DataFrame

if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(**kwargs) -> DataFrame:
    """
    Template for loading data from API
    """
    url = 'https://api.github.com/repos/DataTalksClub/zoomcamp-analytics/contents/data/de-zoomcamp-2023'

    # Send a GET request to the GitHub API
    response = requests.get(url)

    # Check if the request was successful
    if response.status_code == 200:
        # Extract the file names from the response JSON
        file_names = [file['name'] for file in response.json()]
        print(file_names)
        # Initialize an empty DataFrame to store all the data
        combined_data = pd.DataFrame()

        # Iterate over each file in the directory
        for file_name in file_names:
            # print(file_name)
            # Construct the URL for the raw CSV file
            file_url = f'https://raw.githubusercontent.com/DataTalksClub/zoomcamp-analytics/main/data/de-zoomcamp-2023/{file_name}'
            
            # dtypes = {
            # 'email': str,
            # 'time_homework': float,
            # 'time_lectures': float,   
            # }
            # Read the CSV data from the URL
            file_data = pd.read_csv(file_url)
            file_data['module']=file_name[:-4]
            # print(file_data.head())
            # Merge the data with the combined DataFrame based on the 'email' column
            if not combined_data.empty:
                combined_data = pd.merge(combined_data, file_data, on='email', how='outer',suffixes=('', f'_{file_name[:-4]}'))
            else:
                combined_data = file_data
        
        # Preview the combined data
        print("Preview of the combined data:")
        
    else:
        print("Failed to fetch file names. Status code:", response.status_code)
        

    return combined_data


@test
def test_output(df) -> None:
    """
    Template code for testing the output of the block.
    """
    assert df is not None, 'The output is undefined'
