# dumpmon.py
# Author: Jordan Wright
# Version: 0.0 (in dev)

# ---------------------------------------------------
# To Do:
#
#	- Refine Regex
#	- Create/Keep track of statistics

from lib.Pastebin import Pastebin
from lib.Slexy import Slexy
from lib.Pastie import Pastie
from time import sleep
from twitter import Twitter, OAuth
from settings import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_TOKEN, ACCESS_TOKEN_SECRET, log_file
import threading
import logging
import sys


def initLogging(log_level):
    logFormatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    rootLogger = logging.getLogger()
    rootLogger.setLevel(log_level)
    
    fileHandler = logging.FileHandler(log_file)
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
    
    consoleHandler = logging.StreamHandler(sys.stderr)
    consoleHandler.setFormatter(logFormatter)
    rootLogger.addHandler(consoleHandler)



def monitor():
    '''
    monitor() - Main function... creates and starts threads

    '''
    import argparse
    parser = argparse.ArgumentParser()
    # arguments to control the log level. Defaults to WARNING, but with -v goes to INFO, -d goes to DEBUG
    parser.add_argument(
        "-d", "--debug", help="Debug output (TONS printed to the console)", 
        action="store_const", dest="loglevel", const=logging.DEBUG, default=logging.WARNING)
    parser.add_argument(
        "-v", "--verbose", help="Verbose output (less than debug)", action="store_const", 
        dest="loglevel", const=logging.INFO)
    
    args = parser.parse_args()
       
    initLogging(args.loglevel)
    
    
    
    logging.info('Monitoring...')
    
    bot = Twitter(
        auth=OAuth(ACCESS_TOKEN, ACCESS_TOKEN_SECRET,
            CONSUMER_KEY, CONSUMER_SECRET)
        )
    # Create lock for tweet action
    tweet_lock = threading.Lock()

    
    pastebin_thread = threading.Thread(
        target=Pastebin().monitor, args=[bot, tweet_lock])
    slexy_thread = threading.Thread(
        target=Slexy().monitor, args=[bot, tweet_lock])
    pastie_thead = threading.Thread(
        target=Pastie().monitor, args=[bot, tweet_lock])

    for thread in (pastebin_thread, slexy_thread, pastie_thead):
        thread.daemon = True
        thread.start()

    # Let threads run
    try:
        while(1):
            sleep(5)
    except KeyboardInterrupt:
        logging.warn('Stopped.')


if __name__ == "__main__":
    monitor()
