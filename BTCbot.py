# Elliot Winch - Basic BTCbot - 14th Sept 2017

# Usage: BTCbot.py -p <period> -c <currency>
# Every <period>, will print a timestamp, current price, current moving average
# Using its rudimentary strategy, will trade any Poloniex currency pair

# Improvements: 
# Stopping condition for safety
# Better strategy, possibly with second, shorter CMA 
# Trade varying amounts
# Alert system for extreme circumstances
# More options before / control during runtime

import time
import datetime
import sys, getopt
import PoloniexAPI

def main(argv):
    period = 10
    pair = 'BTC_XMR'
    lengthofMA = 100
    
    prices = []
    tradePlaced = False
    typeOfTrade = ""
    previousPrice = False
    orderNumber = False
    
    #Argument handling
    try:
        opts, args = getopt.getopt(argv,"hp:",["period=",])
    except getopt.GetoptError:
        print 'Usage is: BTCbot.py -p <period> -c <currency>'
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == '-h':
            print 'Usage is: BTCbot.py -p <period> -c <currency>'
            sys.exit()
        elif opt in ("-p", "-period"):
            if(int(arg) in [300,900,1800,7200,14400,86400]):
                period = arg
            else:
                print 'Poloniex requires a period of 300, 900, 1800, 7200, 14400 or 86400'
                sys.exit(2)
        elif opt in ("-c","-currency"):
            pair = arg
                
    poloniexConn = PoloniexAPI.poloniex('keys','values')
    
    while True:
        currentValues = poloniexConn.api_query("returnTicker")
        
        thisPrice = currentValues[pair]["last"]
        
        print "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()) 
        print " Period: %s$ %s; %s" % (period,pair,thisPrice)
        
        if(len(prices) > 0):
            if(len(prices) > lengthofMA):
                del prices[0]
            currentMovingAverage = sum(prices) /float(len(prices))
            print " CMA: %f" % (currentMovingAverage)
            
            previousPrice = prices[-1]
            
            #Trade strategy code
            #Only one trade can be placed at time
            if(not tradePlaced):
                #Price is high but falling
                if( (thisPrice > currentMovingAverage) and (thisPrice < previousPrice) ):
                    print "Sell Order"
                    orderNumber = poloniexConn.sell(pair, thisPrice, .01)
                    tradePlaced = True
                    typeOfTrade = "short"
                #Price is low but rising
                elif( (thisPrice < currentMovingAverage) and (thisPrice > previousPrice) ):
                    orderNumber = poloniexConn.buy(pair, thisPrice, .01)
                    print "Buy Order"
                    tradePlaced = True
                    typeOfTrade = "long"
            #Stop trading
            #Price was high but falls below CMA
            elif (typeOfTrade == "short"):
                if(thisPrice < currentMovingAverage):
                    print "Exit trade"
                    poloniexConn.cancel(pair,orderNumber)
                    tradePlaced = False
                    typeOfTrade = False
            #Price was low but rises above CMA
            elif (typeOfTrade == "long"):
                if(thisPrice > currentMovingAverage):
                    print "Exit trade"
                    poloniexConn.cancel(pair,orderNumber)
                    tradePlaced = False
                    typeOfTrade = False
                    
                    
        prices.append(float(thisPrice))
            
        time.sleep(int(period))

if __name__ == "__main__":
    main(sys.argv[1:])