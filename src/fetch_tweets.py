import urllib, json
import sys
import tweepy
from tweepy import OAuthHandler


class TwitterFetcher(object):
    """
    Fetches last N Tweets from an specific account.
    """
    def __init__(self, account, consumer_token, consumer_secret, access_token, access_secret, twits_num=200):
        self.account = account
        self.twits_num = twits_num
        self.consumer_token = consumer_token
        self.consumer_secret = consumer_secret
        self.access_token = access_token
        self.access_secret = access_secret

    def grab(self):
        authenticator = tweepy.OAuthHandler(self.consumer_token, self.consumer_secret)
        authenticator.set_access_token(self.access_token, self.access_secret)

        twitter_client = tweepy.API(authenticator)

        twits = []

        # make initial request for most recent tweets (200 is the maximum allowed count)
        new_tweets = twitter_client.user_timeline(screen_name=self.account, count=self.twits_num)

        # save most recent twits
        twits.extend(new_tweets)

        # save the id of the oldest twit
        oldest = twits[-1].id - 1

        # keep grabbing tweets until there are no tweets left to grab
        while len(new_tweets) > 0:
            print("getting tweets before %s" % (oldest))

            # all subsiquent requests use the max_id param to prevent duplicates
            new_tweets = twitter_client.user_timeline(screen_name=self.account, count=200, max_id=oldest)

            # save most recent tweets
            twits.extend(new_tweets)

            # update the id of the oldest tweet less one
            oldest = twits[-1].id - 1

            print("%s tweets fetched" % (len(twits)))

        for status in twits:
            body = (status.text).encode('utf-8')
            with open('twits.txt', 'a', encoding='utf-8') as f:
                f.write(bytes(body).decode('utf-8') + ' ')

if __name__ == '__main__':
    trump_twitter = TwitterFetcher('realDonaldTrump')
    trump_twitter.grab()
