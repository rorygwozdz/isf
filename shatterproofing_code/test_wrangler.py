import os
import pytest
import pandas as pd
from .options_wrangler import OptionsWrangler as Ow

#  environment variables
uso_data_location = 'shatterproofing_code/csv_data/uso.csv'


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


def test_throws_error_on_bad_type():
    with pytest.raises(TypeError):
        uso = Ow(data=5)


def test_get_expo_chain(uso_wrangler):

    # basic grab
    trade_date = '2020-02-14'
    expo = '2020-04-17'
    april_chain = uso_wrangler.get_expo_chain(trade_date, expo)
    assert 5.0 in april_chain['strike'].values
    assert len(april_chain) < 500

    # bigger grab
    trade_date = '2020-02-13'
    full_chain = uso_wrangler.get_expo_chain(trade_date)
    assert 5.0 in full_chain['strike'].values
    expos = pd.unique(full_chain.index.get_level_values('expirDate').values)
    assert len(expos) > 1
    assert '2020-03-20' in expos
    assert '2020-04-17' in expos
    assert len(full_chain) > 150

    # throw bad expo
    with pytest.raises(IndexError):
        trade_date = '2020-02-15'
        full_chain = uso_wrangler.get_expo_chain(trade_date)

    # throws bad trade_date
    with pytest.raises(IndexError):
        trade_date = '2020-02-14'
        expir_date = '2020-04-18'
        full_chain = uso_wrangler.get_expo_chain(trade_date, expir_date)


# gets the value of a call at a particular strike
def test_get_option_value(uso_wrangler):

    trade_date = '2020-02-14'
    expo = '2020-04-17'
    strike = 10
    side = 'call'
    uso_10_strike_call = uso_wrangler.get_option_value(trade_date, expo, strike, side)
    assert 1.22 == uso_10_strike_call

    side = 'put'
    uso_10_strike_put = uso_wrangler.get_option_value(trade_date, expo, strike, side)
    assert .25 == uso_10_strike_put

    # throws index error
    strike = 1000
    with pytest.raises(IndexError):
        uso_1000_strike_put = uso_wrangler.get_option_value(trade_date, expo, strike, side)
        assert .25 == uso_1000_strike_put





