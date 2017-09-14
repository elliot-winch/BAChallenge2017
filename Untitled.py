import time
import datatime
import sys, getopt

def main(argv):
    period = 1
    
    #Argument handling
    try:
        opts, args = getopt.getopt(argv,"hp:",["period=",])
    except getopt.GetoptError:
        print 'Usage is: BTCbot.py -p <period>'
        sys.exit(2)
        
    for opt, arg in opts:
        if opt == '-h':
            print 'Usage is: BTCbot.py -p <period>'
            sys.exit()
        elif opt in ("-p", "-period"):
            if(int(arg) in [300,900,1800,7200,14400,86400]):
                period = arg
            else:
                print 'Poloniex requires a period of 300, 900, 1800, 7200, 14400 or 86400'
                sys.exit(2)
    
    while True:
        print "{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now())
        time.sleep((int)period)

if __name__ == "__main__":
    main(sys.argv[1:])