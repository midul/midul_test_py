import sys
import os
import datetime
import jsonpickle
import time

from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, AppAuthHandler
from tweepy import Stream, API
from tweepy import TweepError

# TODO - add code to filter only the tweets that have location
# TODO - add code to send json stream to socket


class TweetExtractor:

    def __init__(self, eoi):

        # set the Event of Interest (EOI)
        self.event = eoi
        self.event = 'eoi'

        # Twitter Credentials
        self.access_token = '150194396-hoWDep11Iqc2TedC7vhmybVp9tLC8zClOC5osxSc'
        self.access_token_secret = 'EsRxMGpBQwXGmpvX5RXHsKPBiGPy1Xj5KjkshXX8LwaED'
        self.consumer_key = 'Wme6rpo4DGkBTNHQfpNSnAu39'
        self.consumer_secret = '08hZBiNnDAAIk2SMp6IzRKD85ceC4RLxf3hNxlx2xWNtd36CyB'

        # Directory for storing raw twitter data
        self.tweets_data_path = None

        # Socket to send data
        self.client_socket = None
        self.abs_filename = None

    def set_destination(self, dest_name, dest_type='file'):

        if dest_type == 'file':
            self.tweets_data_path = dest_name
        elif dest_type == 'socket':
            self.client_socket = dest_name
        else:
            print("Invalid destination for data")
            sys.exit(-1)

    class LiveTweetListener(StreamListener):

        def __init__(self, out_file_name=None, out_socket=None):
            super().__init__()

            # If the output should be saved, pass the filename
            if out_file_name :
                self.output_file_name = out_file_name
            elif out_socket:
                self.output_socket = out_socket

            # Count of fetched live tweets
            self.tweet_count = 0

        def on_data(self, data):

            try:

                # Write tweets to file or socket
                if self.output_file_name:
                    with open(self.output_file_name, 'a') as out_file:
                        out_file.write(data)
                elif self.output_socket:
                    self.output_socket.send(data)

                self.tweet_count += 1

                if self.tweet_count % 100 == 0:
                    print("Downloaded {0} tweets".format(self.tweet_count))

                return True
            except BaseException as e:
                print('Error while getting data from twitter stream', str(e))
                time.sleep(5)
            return True

        def on_error(self, status_code):
            print('Error while listening to tweet: Status =', status_code)

    def abs_filename_return(self):
        return self.abs_filename

    def extract_live_tweets(self, keywords):

        if self.tweets_data_path:
            # Create output file name for storing raw twitter data
            current_date = datetime.datetime.today().strftime('%Y-%m-%d')
            output_dir = self.tweets_data_path + '/' + self.event + '/'
            output_file = output_dir + 'data_live.json'
            self.abs_filename = output_file
            try:
                os.makedirs(output_dir)
            except FileExistsError:
                pass

            # This handles Twitter authentication and the connection to Twitter Streaming API
            listener = self.LiveTweetListener(out_file_name=output_file)

        elif self.client_socket:

            # This handles Twitter authentication and the connection to Twitter Streaming API
            listener = self.LiveTweetListener(out_socket=self.client_socket)

        auth = OAuthHandler(self.consumer_key, self.consumer_secret)
        auth.set_access_token(self.access_token, self.access_token_secret)
        stream = Stream(auth, listener)

        # This line filter Twitter Streams to capture data by the keywords
        stream.filter(track=keywords)

    def extract_historic_tweets(self, keywords):

        # Get twitter handle
        auth = AppAuthHandler(self.consumer_key, self.consumer_secret)
        api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        if not api:
            print("Error while authenticating with twitter")
            sys.exit(-1)

        # Form search query from the keywords
        search_query = ' OR '.join(keywords)

        if self.tweets_data_path:
            # Create output file name for storing raw twitter data
            current_date = datetime.datetime.today().strftime('%Y-%m-%d')
            output_dir = self.tweets_data_path + '/' + self.event + '/'
            output_file = output_dir + 'data_historic.json'
            try:
                os.makedirs(output_dir)
            except FileExistsError:
                pass

        # Set query params
        max_tweets = 1000000000  # Some arbitrary large number
        tweets_per_query = 100  # this is the max the API permits

        '''
           params for maintaining context/continuity across the entire query
           
           1. If results from a specific ID onwards are required, set since_id to that ID.
           else default to no lower limit, go as far back as API allows
        
           2. If results only below a specific ID are, set max_id to that ID.
           else default to no upper limit, start from the most recent tweet matching the search query.
        
        '''
        since_id = None
        max_id = -1

        # Execute the search query (tweets_per_query at a time)
        tweet_count = 0
        with open(output_file, 'w') as out_file:
            while tweet_count < max_tweets:
                try:
                    if max_id <= 0:
                        if not since_id:
                            new_tweets = api.search(q=search_query,
                                                    count=tweets_per_query)
                        else:
                            new_tweets = api.search(q=search_query,
                                                    count=tweets_per_query,
                                                    since_id=since_id)
                    else:
                        if not since_id:
                            new_tweets = api.search(q=search_query,
                                                    count=tweets_per_query,
                                                    max_id=str(max_id - 1))
                        else:
                            new_tweets = api.search(q=search_query,
                                                    count=tweets_per_query,
                                                    max_id=str(max_id - 1),
                                                    since_id=since_id)
                    if not new_tweets:
                        print("No more tweets found")
                        break

                    # Write tweets to file or socket
                    for tweet in new_tweets:
                        if self.tweets_data_path:
                            out_file.write(jsonpickle.encode(tweet._json, unpicklable=False))
                            out_file.write('\n')
                        elif self.client_socket:
                            self.client_socket.send(tweet)

                    tweet_count += len(new_tweets)
                    print("Downloaded {0} tweets".format(tweet_count))
                    max_id = new_tweets[-1].id
                except TweepError as e:
                    # Just exit if any error
                    print("some error : " + str(e))
                    break

        print("Downloaded {0} tweets, Saved to {1}".format(tweet_count, output_file))


def follow(thefile):
    thefile.seek(0, 2)
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.1)
            continue
        yield line


if __name__ == '__main__':

    # Set the EOI here
    eoi = 'TRUMP'

    # Add your keywords defining EOI
    keywords = ['donald trump', 'trump', 'us president', 'potus']

    # Set the output directory name for twitter data
    twitter_raw_data_path = 'C:/Users/midul/Documents/Twitter_Data'

    tweet_extractor = TweetExtractor(eoi)

    # Save the fetched twitter data to a file or sent to a socket
    tweet_extractor.set_destination(twitter_raw_data_path, dest_type='file')

    # Run either extract_live_tweets (blocking call) OR extract_historic_tweets

    tweet_extractor.extract_live_tweets(keywords)

    # tweet_extractor.extract_historic_tweets(keywords)
    file = tweet_extractor.abs_filename()

    logfile = open(file, "r")
    loglines = follow(logfile)
    for line in loglines:
        print (line)