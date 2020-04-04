import os
import pytest
import pandas as pd
from .options_wrangler import OptionsWrangler as Ow

#  enviroment variables
uso_data_location = 'code/csv_data/uso.csv'


@pytest.fixture(scope="module")
def uso_wrangler():
    return Ow(data=uso_data_location)


def test_takes_in_data_location():
    uso = Ow(data=uso_data_location)
    data = uso.data
    assert 'gamma' in data.columns


def test_takes_in_dataframe():
    uso_df = pd.read_csv(uso_data_location)
    uso = Ow(data=uso_df)
    data = uso.data
    assert 'gamma' in data.columns

def test_get_expo_chain(uso_wrangler):
    trade_date = '2020-03-10'
    expo = '2020-04-17'
    uso = uso_wrangler()
    april_chain = uso.get_expo_chain(trade_date, expo)
    assert 5 in april_chain.strike
    assert len(april_chain) < 500


# # returns the the expiration for an option on a given date
# wrangler.get_expo_chain(expo_chain, trade_date) # throws not valid expo, not in dataset (before, after)
# # returns the the expiration for an option
# wrangler.get_option_expo(option)
# wrangler.get_option_history(strike, expo, starting_trade_date) # throws no such option, not in dataset
# wrangler.get_days_historical_chain() # throws not in data set
# wrangler.get_imp_vol(expo, trade_date, strike)
# wrangler.get_call_value(expo, trade_date, strike) # throws not in dataset
# wrangler.get_put_value(expo, trade_date, strike) # throws not in dataset
# wrangler.get_market(expo, trade_date, strike) # throws not in dataset