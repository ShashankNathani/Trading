import requests
import pandas as pd
import datetime


def get_sp500_constituents():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    tables = pd.read_html(url)
    sp500_table = tables[0]
    sp500_constituents = sp500_table[['Symbol', 'Security']]
    return sp500_constituents.to_dict('list')


