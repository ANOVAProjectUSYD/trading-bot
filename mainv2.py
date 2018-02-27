import os, argparse
import datetime
import time
from poloniex import Poloniex

def read_ticker(): #should add a check to see if user input is in the list of valid options
    ticker = input("Enter the ticker pair, e.g. BTC_ETH \n")
    return ticker
def continueOption(): #user is able to view option menu again
    cont = input("Would you like to see the options again? Please enter yes or no \n")
    if cont.lower() == "yes":
        operating = True
    elif cont.lower() == "no":
        operating = False
    else:
        print("Invalid option. Terminating program.")
        quit()
    return operating

def clean_arguments(time_period): #validates if time period is allowed
    if int(time_period) in [300,900,1800,7200,14400,86400]:
        validPeriod = time_period
    else:
        print("Issue with time argument. Program terminating.")
        quit()
    return validPeriod

def connect_api(ticker):
    '''Easiest way to connect to Poloniex API.'''
    api_key = 'TSOM80FK-VIYJV705-6E27F6P3-IL92VWCF' #it doesn't need this to stream prices?
    secret = '6bd7cf3f563edded66f6f73782fed44d0e9cc0b345d5a290a4abf60f7c9713e32a718f94a665237bc2d444320bb33bf98e3911dd547d2c7acdf7a464bc37ae53'
    polo = Poloniex(api_key, secret) # connects to API with key
    return polo

def option(result, api_obj, ticker):
        rdict = {'1': 'You chose to view live prices', '2': 'You chose to view 24 hour volume', '3': 'You chose to view Percentage change', '4': 'You chose to view 24 hour high/low', '5':'Program terminating'}
        print (rdict[result])
        if  result == '1':
            time_period = input("Enter the time period. Valid time periods are 300, 900, 1800, 7200, 14400 and 86400. Press Control-Z to terminate. \n")
            validPeriod = clean_arguments(time_period)
            stream_data(api_obj, ticker, validPeriod)
        elif result == '2':
            get24HourVolume(api_obj, ticker)
            operating = continueOption()
            return(operating)
        elif result == '3':
            getPercentageChange(api_obj,ticker)
            operating = continueOption()
            return(operating)

        elif result == '4':
            getHighLow(api_obj,ticker)
            operating = continueOption()
            return(operating)

        elif result == '5':
            quit()
        else:
            print("Please enter a valid number")

def get24HourVolume(polo, ticker):
    polo_data = polo.returnTicker()[ticker]
    volume = polo_data['baseVolume']
    print("The 24 hour volume is {} BTC".format(volume))

def getPercentageChange(polo, ticker):
    polo_data = polo.returnTicker()[ticker]
    percentageChange = polo_data['percentChange']
    print("The 24 hour percentage change is {}".format(percentageChange))

def getHighLow(polo, ticker):
    polo_data = polo.returnTicker()[ticker]
    high = polo_data['high24hr']
    low = polo_data['low24hr']
    print("The 24 hour high is {} and the 24 hour low is {}".format(high,low))

def stream_data(polo, ticker, ticker_time):
    '''Streams data regarding cryptocurrency.'''
    while True:
        polo_data = polo.returnTicker()[ticker] # polo_data is a dictionary containing info about the ticker
        #print(type polo_data) or #print(polo_data.keys())
        date = datetime.datetime.now()
        last_price = polo_data['last']  # read documentation section in README file to see other data we can get
        print("Time: {date}  Last price: {last_price}".format(date = date, last_price=last_price))
        new_time = float("." + str(ticker_time))
        time.sleep(new_time) # pauses program and then grabs price after some time

def main():
    print("Please enter a trading pair, e.g. BTC_ETH")
    ticker = read_ticker()
    operating = True
    api_obj = connect_api(ticker)
    while operating: #made this while loop so user gets the choice to see options again
        result = input("""
        Please enter one of the following number options:

        1 Check live prices
        2 Check 24 hour volume
        3 Check 24 hour percentage change
        4 Check 24 hour high/low
        5 exit \n
        """)

        operating = option(result, api_obj, ticker)


# this executes the main method
if __name__ == "__main__":
    main()
