import pandas as pd


class OptionsWrangler:
    def __init__(self, data):
        if type(data) == str:
            data = pd.read_csv(data)
        self.data = data


    def get_expo_chain(self):
        
#
#
#
#
#
#
#
#
#
#
#
# wrangler = OptionsWrangler(data=options_data)
# ## HAS A SUBCLASS: OPTION
#     ### it's essentially a row of a dataframe, except it grabs the daily data for itself
#     ### it's the string of the bucket, so to speak
#     Option((delta or strike) and trade_date and expo, months_out=None, weeks_out=None,)
# # returns the the expiration for an option
# wrangler.get_expo_chain(expo_chain, trade_date) # throws not valid expo, not in dataset (before, after)
# # returns the the expiration for an option
# wrangler.get_option_expo(option)
# wrangler.get_option_history(strike, expo, dtarting_trade_date) # throws no such option, not in dataset
# wrangler.get_days_historical_chain() # throws not in data set
# wrangler.get_imp_vol(expo, trade_date, strike)
# wrangler.get_call_value(expo, trade_date, strike) # throws not in dataset
# wrangler.get_put_value(expo, trade_date, strike) # throws not in dataset
# wrangler.get_market(expo, trade_date, strike) # throws not in dataset