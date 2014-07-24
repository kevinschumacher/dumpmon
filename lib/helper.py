'''
helper.py - provides misc. helper functions
Author: Jordan

'''

import requests
from time import sleep, strftime
import logging

MAX_TWEET_LENGTH = 140

r = requests.Session()


def download(url, headers=None):
    if not headers:
        headers = None
    if headers:
        r.headers.update(headers)
    try:
        response = r.get(url).text
    except requests.ConnectionError:
        logging.warn('[!] Critical Error - Cannot connect to site')
        sleep(5)
        logging.warn('[!] Retrying...')
        response = download(url)
    return response




def build_tweet(paste):
    '''
    build_tweet(url, paste) - Determines if the paste is interesting and, if so, builds and returns the tweet accordingly

    '''
    tweet = None
    if paste.match():
        tweet = paste.url
        if paste.type == 'db_dump':
            if paste.num_emails > 0:
                tweet += ' Emails: ' + str(paste.num_emails)
            if paste.num_hashes > 0:
                tweet += ' Hashes: ' + str(paste.num_hashes)
            if paste.num_hashes > 0 and paste.num_emails > 0:
                tweet += ' E/H: ' + str(round(
                    paste.num_emails / float(paste.num_hashes), 2))
            tweet += ' Keywords: ' + str(paste.db_keywords)
        elif paste.type == 'google_api':
            tweet += ' Found possible Google API key(s)'
        elif paste.type in ['cisco', 'juniper']:
            tweet += ' Possible ' + paste.type + ' configuration'
        elif paste.type == 'ssh_private':
            tweet += ' Possible SSH private key'
        elif paste.type == 'honeypot':
            tweet += ' Dionaea Honeypot Log'
        elif paste.type == 'keywords':
            tweet += ' Keywords: ' + str(len(paste.keywords)) + ' '
            # actually add the keywords to the tweet (make sure you protect your tweets!):
            tweet_kw = '|'.join(paste.keywords)
            tweet += tweet_kw
            # put an elipsis if tweet too long
            if len(tweet) > MAX_TWEET_LENGTH:
                tweet = tweet[:MAX_TWEET_LENGTH-3]+'...'
            
            
    return tweet
