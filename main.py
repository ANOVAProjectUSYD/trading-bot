import os, argparse
import datetime
import time
from poloniex import Poloniex


def clean_arguments():
    '''Parses correct time and ticker pair.'''
    try:
        parser =  argparse.ArgumentParser() # creates parser object to read parse
        parser.add_argument("period", help="time period")
        parser.add_argument("ticker", help="ticker_pair")
        args = parser.parse_args()
        # checks if period specified is correct
        period = 0
        if int(args.period) in [300,900,1800,7200,14400,86400]:
            period = int(args.period)
        else:
            print("Issue with time argument.")
            quit()
    except:
        print("Error with arguments.")
        exit()

    return period, args.ticker


def connect_api(ticker):
    '''Easiest way to connect to Poloniex API.'''
    api_key = 'TSOM80FK-VIYJV705-6E27F6P3-IL92VWCF'
    secret = '6bd7cf3f563edded66f6f73782fed44d0e9cc0b345d5a290a4abf60f7c9713e32a718f94a665237bc2d444320bb33bf98e3911dd547d2c7acdf7a464bc37ae53'
    polo = Poloniex(api_key, secret) # connects to API with key

    return polo


def stream_data(polo, ticker, ticker_time):
    '''Streams data regarding cryptocurrency.'''
    while True:
        polo_data = polo.returnTicker()[ticker] # gets data about cryptocurrency
        # polo_data is a dictionary containing info about the ticker

        date = datetime.datetime.now()
        last_price = polo_data['last'] # gets the last price
        # read documentation section in README file to see other data we can get

        print("Time: {date}  Last price: {last_price}".format(date = date,
                                                              last_price=last_price))
        new_time = float("." + str(ticker_time))

        time.sleep(new_time) # pauses program and then grabs price after some time


def main():

    time_period, ticker = clean_arguments() # gives us cleaned parameters

    api_obj = connect_api(ticker) # connects to Poloniex API

    stream_data(api_obj, ticker, time_period) # streams data in

# this executes the main method
if __name__ == "__main__":
    main()
