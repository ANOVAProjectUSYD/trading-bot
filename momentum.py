import time
import sys, getopt
import datetime
import poloniex
from poloniex import Poloniex
from main import connect_api # from other file.

def view_balances(conn):
	'''Allows you to view ETH and BTC Balance.'''
	balance = conn.returnBalances()
	print("ETH balance is %s!" % balance['ETH'])
	print("BTC balance is %s!" % balance['BTC'])


def trade_momentum():
	'''Runs a momentum strategy.'''
	period = 30
	print("The data points will be updated at %d second intervals" % period)
	pair = input("Please input the crypto pair, e.g BTC_ETH: \n")
	prices = []
	conn = connect_api() # from mainv2 file.
	view_balances(conn)

	while True:
	    currentValues = conn.returnTicker()[pair]
	    lastPairPrice = float(currentValues["last"])
	    dataDate = datetime.datetime.now()

	    if len(prices)>=4:
	        if  prices[-2]<prices[-1] and prices[-2]<prices[-3]<prices[-4]:
	            print("Upwards momentum trend. Buy.")
	            orderNumber = conn.buy(pair,lastPairPrice,.1)
	            del prices[0]
	        elif prices[-2]>prices[-1] and prices[-2]>prices[-3]>prices[-4]:
	            print("Downwards momentum trend. Sell.")
	            orderNumber = conn.sell(pair,lastPairPrice,.1)
	            del prices[0]
	        else:
	            del prices[0]

	    prices.append(float(lastPairPrice))
	    print("{}  Past 4 price data points - {}".format(dataDate,prices))
	    time.sleep(int(period))


def main():
	trade_momentum()

if __name__ == "__main__":
    main()
