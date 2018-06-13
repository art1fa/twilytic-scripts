# pylint: disable=invalid-name
# pylint: disable=missing-docstring
# pylint: disable=trailing-whitespace
import rethinkdb as r
import tweepy
import time
from datetime import datetime
import json
import logging

from tweepy_conf import init
from convert_time import to_iso8601, date, hour
from db_conf import get_conf


logging.basicConfig(filename='stream.log',level=logging.INFO)

logging.info(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))


rdb_config = get_conf()
api = init()
users = []

class listener(tweepy.StreamListener):

  def on_data(self, data):
    obj = json.loads(data)

    if 'delete' in obj:
      return self.on_delete(obj['delete']['status']['id'], obj['delete']['status']['user_id'])

    elif 'scrub_geo' in obj:
      return self.on_scrub_geo(obj['scrub_geo']['user_id'], obj['scrub_geo']['up_to_status_id'])

    elif 'limit' in obj:
      return self.on_limit(obj['limit']['track'])

    elif 'status_withheld' in obj:
      return self.on_status_withheld(obj['status_withheld']['id'], obj['status_withheld']['user_id'], obj['status_withheld']['withheld_in_countries'])

    elif 'user_withheld' in obj:
      return self.on_user_withheld(obj['user_withheld']['id'], obj['user_withheld']['withheld_in_countries'])

    elif 'disconnect' in obj:
      return self.on_disconnect(obj['disconnect']['code'], obj['disconnect']['stream_name'], obj['disconnect']['reason'])

    elif 'warning' in obj:
      return self.on_stall_warning(obj['warning']['code'], obj['warning']['message'], obj['warning']['percent_full'])

    elif 'text' in obj:
      return self.on_status(obj)
    else:
      return self.on_unknown(obj)

    return True

  def on_status(self, status):
    if status['user']['id_str'] in user_ids:
      logging.info("New status: %s: %s", status['user']['screen_name'], status['text'])
      timestamp = to_iso8601(status['created_at'])
      status['created_at'] = timestamp
      with r.connect(**rdb_config) as conn:
        r.table('tweets').insert(status).run(conn)

  def on_delete(self, status_id, user_id):
      """Called when a delete notice arrives for a status"""
      logging.info("Delete %s received", status_id)
      return True

  def on_scrub_geo(self, user_id, up_to_status_id):
      """Called when geolocated data must be stripped for user_id for statuses before up_to_status_id"""
      logging.warning("Scrub_geo received for user %s", user_id)
      return True

  def on_limit(self, track):
      """Called when a limitation notice arrvies"""
      logging.warning('Limit received for %s', track)
      return True

  def on_status_withheld(self, status_id, user_id, countries):
      """Called when a status is withheld"""
      logging.warning('Status %s withheld for user %s', status_id, user_id)
      return True

  def on_user_withheld(self, user_id, countries):
      """Called when a user is withheld"""
      logging.warning('User %s withheld', user_id)
      return True

  def on_disconnect(self, code, stream_name, reason):
      """Called when a disconnect is received"""
      logging.error('Disconnect message: %s %s %s', code, stream_name, reason)
      return True

  def on_stall_warning(self, code, message, percent_full):
      logging.warning("Stall warning (%s): %s (%s%% full)", code, message, percent_full)
      return True

  def on_error(self, status_code):
      """Called when a non-200 status code is returned"""
      logging.error('Twitter returned error code %s', status_code)
      self.error = status_code
      return False

  def on_unknown(self, entity):
      """Called when an unrecognized object arrives"""
      logging.error('Unknown object received: %s', repr(entity))
      return True

print("get users to monitor...")

with r.connect(**rdb_config) as conn:
  for user in r.table('users').run(conn):
    users.append(user)

user_ids = [user['id_str'] for user in users]

logging.info("Following %i users", len(user_ids))

stream = tweepy.Stream(auth=api.auth, listener=listener())

while True:
  try:
    print("starting stream...")
    stream.filter(follow=user_ids)
  except Exception as e:
    print(e)
    time.sleep(2)