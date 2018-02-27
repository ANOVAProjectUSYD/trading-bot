import time
import sys, getopt
import datetime
import poloniex
from poloniex import Poloniex

def viewBalances(conn):
	balance = conn.returnBalances()
	print("ETH balance is %s!" % balance['ETH'])
	print("BTC balance is %s!" % balance['BTC'])

def main():
    period = 30
    print("The data points will be updated at %d second intervals" % period)
    pair = input("Please input the crypto pair, e.g BTC_ETH: \n")
    prices = []
    api_key = 'TSOM80FK-VIYJV705-6E27F6P3-IL92VWCF'
    secret = '6bd7cf3f563edded66f6f73782fed44d0e9cc0b345d5a290a4abf60f7c9713e32a718f94a665237bc2d444320bb33bf98e3911dd547d2c7acdf7a464bc37ae53'
    conn = poloniex.Poloniex(api_key, secret)
    viewBalances(conn)

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

if __name__ == "__main__":
    main()
