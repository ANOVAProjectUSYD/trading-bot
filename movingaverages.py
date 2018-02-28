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
	period = input("Please input the number of seconds between data points e.g. 2 : \n") #amount of seconds between live data points
	pair = "BTC_ETH" #default
	pair = input("Please input the crypto pair, e.g BTC_ETH: \n")
	prices = [] #list
	currentMovingAverage = 0
	lengthOfMA = 0
	startTime = False
	endTime = False
	historicalData = False
	tradePlaced = False
	typeOfTrade = False
	dataDate = ""
	orderNumber = ""

	api_key = 'TSOM80FK-VIYJV705-6E27F6P3-IL92VWCF' #it doesn't need this to stream prices?
	secret = '6bd7cf3f563edded66f6f73782fed44d0e9cc0b345d5a290a4abf60f7c9713e32a718f94a665237bc2d444320bb33bf98e3911dd547d2c7acdf7a464bc37ae53'
	conn = poloniex.Poloniex(api_key, secret) #this method is from API for python3, different to Python2
	#print(conn('returnTicker')['BTC_ETH'])

	viewBalances(conn)


	while True:
		# if (startTime and historicalData):
		# 	nextDataPoint = historicalData.pop(0)
		# 	lastPairPrice = nextDataPoint['weightedAverage']
		# 	dataDate = datetime.datetime.fromtimestamp(int(nextDataPoint['date'])).strftime('%Y-%m-%d %H:%M:%S')
		# elif(startTime and not historicalData):
		# 	exit()
		# else:
		currentValues = conn.returnTicker()[pair] #retrieves the dictionary of data
		lastPairPrice = float(currentValues["last"]) #the key is last
		dataDate = datetime.datetime.now()

		if (len(prices) > 0):
			currentMovingAverage = sum(prices) / float(len(prices))
			previousPrice = prices[-1]
			if (not tradePlaced):
				if ( (lastPairPrice > currentMovingAverage) and (lastPairPrice < previousPrice) ): #price is greater than moving average and starting to fall
					print ("SELL ORDER")
					orderNumber = conn.sell(pair,lastPairPrice,.001)
					tradePlaced = True
					typeOfTrade = "short"
				elif ( (lastPairPrice < currentMovingAverage) and (lastPairPrice > previousPrice) ): #price is below moving average and starting to rise
					print ("BUY ORDER")
					orderNumber = conn.buy(pair,lastPairPrice,.001)
					tradePlaced = True
					typeOfTrade = "long"
			elif (typeOfTrade == "short"):
				if ( lastPairPrice < currentMovingAverage ):  #sell order has already been placed, but the price falls below moving average
					print ("EXIT TRADE")
					conn.cancel(pair,orderNumber)
					tradePlaced = False
					typeOfTrade = False
			elif (typeOfTrade == "long"):
				if ( lastPairPrice > currentMovingAverage ): #buy order has already been placed, but the price rises above moving average. How to tell if trade has already been executed?
					print ("EXIT TRADE")
					conn.cancel(pair,orderNumber)
					tradePlaced = False
					typeOfTrade = False
		else:
			previousPrice = 0

		print ("%s Period: %ss %s: %s Moving Average: %s" % (dataDate,period,pair,lastPairPrice,currentMovingAverage))

		prices.append(float(lastPairPrice)) #adds it to the prices list
		#print(len(prices))
		#prices = prices[-lengthOfMA:]
		time.sleep(int(period)) #pauses the while loop for specified number of seconds before next iteration


if __name__ == "__main__":
	main()
