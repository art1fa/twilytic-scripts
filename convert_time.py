import datetime

def to_iso8601(twitter_timestamp):
    return datetime.datetime.strptime(twitter_timestamp,'%a %b %d %H:%M:%S %z %Y').isoformat()

def date(iso_timestamp):
    return iso_timestamp[0:10]

def hour(iso_timestamp):
    return iso_timestamp[11:13]