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

logging.basicConfig(filename='update_user_data.log',level=logging.INFO)

logging.info(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

rdb_config = get_conf()
api = init()

user_ids = []
n = 100

try:
    with r.connect(**rdb_config) as conn:
        user_ids = r.table('users').get_field('id_str').coerce_to('array').run(conn)
except Exception as e:
  logging.warning("Cannot get current Users in db. Error message: %s", e)

chunked_user_ids = [user_ids[i:i+n] for i in range(0, len(user_ids), n)]

try:
    with r.connect(**rdb_config) as conn:
        for i in range(len(chunked_user_ids)):
            for user in api.lookup_users(chunked_user_ids[i]):
                r.table('users').get(user._json['id_str']).update({
                        'description': user._json['description'],
                        'entities': user._json['entities'] ,
                        'followers_count': user._json['followers_count'],
                        'friends_count': user._json['friends_count'],
                        'favourites_count': user._json['favourites_count'],
                        'location': user._json['location'],
                        'name': user._json['name'],
                        'profile_image_url': user._json['profile_image_url'],
                        'profile_image_url_https': user._json['profile_image_url_https'],
                        'protected': user._json['protected'],
                        'screen_name': user._json['screen_name'],
                        'statuses_count': user._json['statuses_count'],
                        'verified': user._json['verified'],
                        'url': user._json['url']
                    }).run(conn)
except Exception as e:
  logging.warning("Error updating Users. Error message: %s", e)
else:
    logging.info("Successfully updated %i Users",  len(user_ids))