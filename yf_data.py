import yfinance as yf
import pandas as pd

def get_sp500_constituents():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    tables = pd.read_html(url)
    sp500_table = tables[0]
    sp500_constituents = sp500_table[['Symbol', 'Security']]
    return sp500_constituents.to_dict('list')

def get_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

def get_data_df(ticker, start_date, end_date):
    
    data = yf.download(ticker, start=start_date, end=end_date)
    data = data.reset_index()
    data = data.rename(columns={'Date':'date', 'Open':'open', 'High':'high', 'Low':'low', 'Close':'close', 'Adj Close':'adj_close', 'Volume':'volume'})
    return data

def get_data_df2(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    data = data.reset_index()
    data = data.rename(columns={'Date':'date', 'Open':'open', 'High':'high', 'Low':'low', 'Close':'close', 'Adj Close':'adj_close', 'Volume':'volume'})
    data['date'] = data['date'].dt.strftime('%Y-%m-%d')
    return data

if __name__ == '__main__':
    sp500_constituents = get_sp500_constituents()
    print(sp500_constituents)