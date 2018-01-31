from poloniex import Poloniex

def connect_api():
    '''Easiest way to connect to Poloniex Public API.'''
    polo = Poloniex()
    ticker = polo.returnTicker()['BTC_ETH']
    print(ticker)

def main():
    # this is the main method in python.
    connect_api()


# this executes the main method.
if __name__ == "__main__":
    main()
