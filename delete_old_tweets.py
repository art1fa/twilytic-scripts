# pylint: disable=invalid-name
# pylint: disable=missing-docstring
# pylint: disable=trailing-whitespace

import rethinkdb as r
import logging
from datetime import datetime

from db_conf import get_conf

logging.basicConfig(filename='delete_old_tweets.log',level=logging.INFO)

logging.info(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

rdb_config = get_conf()

try:
  with r.connect(**rdb_config) as conn:
    q = r.table('tweets').filter(lambda tweet: r.iso8601(tweet['created_at']).lt(r.now().date() - 30*24*60*60)).delete().run(conn)
except Exception as e:
  logging.warning("Error executing query. No old Tweets deleted. Error message: %s", e)
else:
  if q['errors'] != 0:
    logging.warning("There was an error deleting %i Tweets", q['errors'])
  else:
    logging.info("Deleted %i Tweets", q['deleted'])