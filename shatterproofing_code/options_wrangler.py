import pandas as pd


class OptionsWrangler:
    def __init__(self, data):
        if type(data) == str:
            data = pd.read_csv(data)
        elif type(data) is type(pd.DataFrame()):
            pass
        else:
            raise TypeError(f"Unsupported data type. Got {type(data)}, expected str or pd.DataFrame.")
        self.data = data.set_index(['trade_date', 'expirDate', 'strike'])

    def get_expo_chain(self, trade_date, expiration=None):
        if expiration:
            # check expo
            if expiration not in self.data.index.get_level_values('expirDate').values:
                raise IndexError(f"{expiration} not contained in expirations available in data.")

            query_for_chain = f"trade_date == '{trade_date}' and expirDate == '{expiration}'"

        else:
            query_for_chain = f"trade_date == '{trade_date}'"

        raw_chain = self.data.query(query_for_chain)

        # check trade_date
        if trade_date not in raw_chain.index.get_level_values('trade_date').values:
            raise IndexError(f"{trade_date} not contained in tradeable dates available in data.")

        return raw_chain.reset_index('strike')


#
#
# wrangler = OptionsWrangler(data=options_data)
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