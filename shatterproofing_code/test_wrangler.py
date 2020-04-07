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
def test_get_option_value_by_strike(uso_wrangler):

    trade_date = '2020-02-14'
    expo = '2020-04-17'
    strike = 10
    side = 'call'
    uso_10_strike_call = uso_wrangler.get_option_value_by_strike(strike, side, trade_date=trade_date, expo=expo)
    assert 1.22 == uso_10_strike_call

    side = 'put'
    uso_10_strike_put = uso_wrangler.get_option_value_by_strike(strike, side, trade_date=trade_date, expo=expo)
    assert .25 == uso_10_strike_put


    # test ing by chain
    sample_chain = uso_wrangler.get_expo_chain(trade_date, expo)
    side = 'put'
    uso_10_strike_put_by_chain = uso_wrangler.get_option_value_by_strike(strike, side, chain=sample_chain)
    assert .25 == uso_10_strike_put_by_chain

    # throws index error
    strike = 1000
    with pytest.raises(AssertionError):
        uso_1000_strike_put = uso_wrangler.get_option_value_by_strike(strike, side, chain=sample_chain)
        assert .25 == uso_1000_strike_put


# gets the value of a call at a particular strike
def test_get_option_value_by_delta(uso_wrangler):

    trade_date = '2020-02-14'
    expo = '2020-04-17'
    delta = .35
    side = 'call'
    uso_35_delta_call = uso_wrangler.get_option_value_by_delta(delta, side, trade_date=trade_date, expo=expo)
    assert 0.36 == uso_35_delta_call

    side = 'put'
    uso_35_delta_put = uso_wrangler.get_option_value_by_delta(delta, side, trade_date=trade_date, expo=expo)
    assert 0.39 == uso_35_delta_put

    # test ing by chain
    sample_chain = uso_wrangler.get_expo_chain(trade_date, expo)
    side = 'put'
    uso_35_delta_put_by_chain = uso_wrangler.get_option_value_by_delta(delta, side, chain=sample_chain)
    assert 0.39 == uso_35_delta_put_by_chain

    # throws index error
    delta = 1000
    with pytest.raises(AssertionError):
        uso_1000_delta_put = uso_wrangler.get_option_value_by_delta(delta, side, chain=sample_chain)
        assert .39 == uso_1000_delta_put

    # test no chain no expo
    delta = .5
    with pytest.raises(TypeError):
        uso_erro_on_no_expo = uso_wrangler.get_option_value_by_delta(delta, side, trade_date=trade_date)
        assert .25 == uso_erro_on_no_expo


# gets the value of a call at a particular strike
def test_get_option_history(uso_wrangler):
    trade_date = '2020-02-14'
    expo = '2020-04-17'
    strike = 10
    side = 'call'
    uso_10_strike_call_history = uso_wrangler.get_option_history(strike=strike, side=side,
                                                                 start_trade_date=trade_date, expiration=expo)

    assert len(uso_10_strike_call_history) == 31

    side = 'put'
    uso_10_strike_put_history = uso_wrangler.get_option_history(strike=strike, side=side,
                                                                start_trade_date=trade_date, expiration=expo)

    assert len(uso_10_strike_put_history) == len(uso_10_strike_call_history)



