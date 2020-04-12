import pandas as pd


class OptionsWrangler:
    def __init__(self, data):
        if type(data) == str:
            data = pd.read_csv(data)
        elif type(data) is type(pd.DataFrame()):
            pass
        else:
            raise TypeError(f"Unsupported data type. Got {type(data)}, expected str or pd.DataFrame.")
        dedeuped_data = data.drop_duplicates(['trade_date', 'expirDate', 'strike'])
        self.data = dedeuped_data.set_index(['trade_date', 'expirDate', 'strike'])

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

    def get_option_value_by_strike(self, strike, side, *, trade_date=None, expiration=None, chain=pd.DataFrame()):
        # supports getting exactly the option or getting the chain from memory
        if chain.empty:
            chain = self.no_chain_checks(trade_date, expiration)
        else:
            chain_checks(chain)
        assert strike in chain['strike'].values, "Strike not available in chain."
        strike_query = f"strike == {strike}"
        chain_row = chain.query(strike_query)
        if side in ["call", "c"]:
            return chain_row['cValue'].values
        elif side in ["put", "p"]:
            return chain_row['pValue'].values
        else:
            raise NameError(f"Unsupported side type. Got {side}, expected one of: call, c, put, p.")

    def get_option_value_by_delta(self, delta, side, *, trade_date=None, expiration=None, chain=pd.DataFrame()):
        # supports getting exactly the option or getting the chain then the option if given a trade_date and expo
        assert 0 < delta < 1, "Delta not bounded by zero or one."
        if chain.empty:
            chain = self.no_chain_checks(trade_date, expiration)
        else:
            chain_checks(chain)
        if side in ["call", "c"]:
            chain_row = chain.iloc[(chain['delta'] - delta).abs().argsort()[:1]]
            return chain_row['cValue'].values
        elif side in ["put", "p"]:
            chain_row = chain.iloc[(chain['delta'] - (1 - delta)).abs().argsort()[:1]]
            return chain_row['pValue'].values
        else:
            raise NameError(f"Unsupported side type. Got {side}, expected one of: call, c, put, p.")

    def get_option_history(self, *, start_trade_date, expiration, strike, side):
        history_query = f"trade_date >= '{start_trade_date}' and expirDate == '{expiration}' and strike == {strike}"
        relevant_option_history = self.data.query(history_query)
        if side in ["call", "c"]:
            options_history = relevant_option_history[['stkPx', 'cValue', 'cOi']]
            return options_history
        elif side in ["put", "p"]:
            options_history = relevant_option_history[['stkPx', 'pValue', 'pOi']]
            return options_history
        else:
            raise NameError(f"Unsupported side type. Got {side}, expected one of: call, c, put, p.")

    def get_option_value_by_price(self, price, side, *, trade_date=None, expiration=None, chain=pd.DataFrame()):
        # supports getting exactly the option or getting the chain then the option if given a trade_date and expo
        assert 0 < price, "Price less than one."
        if chain.empty:
            chain = self.no_chain_checks(trade_date, expiration)
        else:
            chain_checks(chain)

        if side in ["call", "c"]:
            chain_row = chain.query(f'cValue < {price}').sort_values('cValue', ascending=False)
            return chain_row[['strike', 'stkPx', 'cValue', 'cOi']].iloc[0]
        elif side in ["put", "p"]:
            chain_row = chain.query(f'pValue < {price}').sort_values('pValue', ascending=False)
            return chain_row[['strike', 'stkPx', 'pValue', 'pOi']].iloc[0]

        else:
            raise NameError(f"Unsupported side type. Got {side}, expected one of: call, c, put, p.")

    def no_chain_checks(self, trade_date, expiration):
        if not expiration:
            raise TypeError("Expo can not be None with no chain given.")
        return self.get_expo_chain(trade_date=trade_date, expiration=expiration)


def chain_checks(chain):
    if len(pd.unique(chain.reset_index()['expirDate'])) > 1:
        raise TypeError("Can't have more than one expiration in passed through chain.")



# wrangler.get_imp_vol(expo, trade_date)