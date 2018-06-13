# pylint: disable=invalid-name
# pylint: disable=missing-docstring
# pylint: disable=trailing-whitespace
import logging
from datetime import datetime
import json
import rethinkdb as r 

import tweepy 
from tweepy_conf import init
from db_conf import get_conf


logging.basicConfig(filename='update_tweet_data.log',level=logging.INFO)

logging.info(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

rdb_config = get_conf()
api = init()

tweet_ids = []
n = 100

#Update all Tweets that were posted minuteCount from now
minuteCount = 60 * 24 * 2

try:
    with r.connect(**rdb_config) as conn:
        tweet_ids = r.table('tweets').between((r.now() - minuteCount * 60).to_iso8601(), r.now().to_iso8601(), index='created_at').filter(lambda tweet: (~tweet.has_fields('retweeted_status'))).get_field('id_str').coerce_to('array').run(conn)
except Exception as e:
  logging.error("Cannot get current Tweets in db. Error message: %s", e)
  raise

chunked_tweet_ids = [tweet_ids[i:i+n] for i in range(0, len(tweet_ids), n)]

try:
    for i in range(len(chunked_tweet_ids)):
        with r.connect(**rdb_config) as conn:
            for tweet in api.statuses_lookup(chunked_tweet_ids[i]):
                r.table('tweets').get(tweet._json['id_str']).update(
                    {
                        'retweet_count': tweet._json['retweet_count'],
                        'favorite_count': tweet._json['favorite_count']
                    }
                ).run(conn)
except Exception as e:
  logging.warning("Error updating Tweets. Error message: %s", e)
else:
    logging.info("Successfully updated %i Tweets",  len(tweet_ids))