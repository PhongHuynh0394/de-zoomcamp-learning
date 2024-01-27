import io
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_green_data(*args, **kwargs):
    """
    Template for loading data from API
    """

    url = "https://github.com/DataTalksClub/nyc-tlc-data/releases/download/green/green_tripdata_2019-09.csv.gz"

    parse_dates = ["lpep_pickup_datetime", "lpep_dropoff_datetime"]

    return pd.read_csv(url, dtype={'store_and_fwd_flag': "string"}, 
            sep=',', compression="gzip", 
            parse_dates=parse_dates)


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
