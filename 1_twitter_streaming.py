# Step 1: tweet collection #

import datetime
import time
import sys
import os
from threading import Timer

#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream

# Import variables that contains the user credentials to access Twitter API
# - access_token
# - access_token
# - consumer_key
# - consumer_secret
# Write the above variables into twitter_config.py
from twitter_config import *

folder = "tweets"

#This is a basic listener that just prints received tweets to stdout.
class OutputListener(StreamListener):
    def __init__(self):
        self.filename = ""

    def update_filename(self):
        now = datetime.datetime.now()
        self.filename = now.strftime('%Y%m%d_%H')+'.txt'
        print '[%s]write file: %s' % ((now.strftime('%Y%m%d_%H%M%S'),self.filename))

    def on_data(self, data):
        if not os.path.exists(folder):
            os.makedirs(folder)

        with open(os.path.join(folder, self.filename),'a') as tf:
            tf.write(data)
        return True

    def on_error(self, status):
        print status

def run_timer(listener):
    listener.update_filename()
    Timer(60, run_timer, [listener]).start()

def main():
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    # #This handles Twitter authetification and the connection to Twitter Streaming API
    l = OutputListener()
    run_timer(l)
    stream = Stream(auth, l)

    while True:
        try:
            #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
            stream.filter(
                track=['attack', 'bomb', 'gun', 'kill', 'new year', 'xmas', 'christmas',
                    'holiday', 'celebrate', 'celebration'])
        except: # catch *all* exceptions
            e = sys.exc_info()[0]
            print e

if __name__ == '__main__':
    main()
