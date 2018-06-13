import tweepy

def init():
    consumer_key = 'xxx'
    consumer_secret = 'yyy'

    access_token = 'zzz'
    access_token_secret = 'xyz'

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=20, \
                    retry_delay=10, retry_errors=[500, 502, 503, 504])

    return api
