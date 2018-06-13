
# pylint: disable=invalid-name
# pylint: disable=missing-docstring

import json
import tweepy 
from tweepy_conf import init

from pprint import pprint

import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords

from collections import Counter

def get_user_tags(api, user_id):
  list_names = []
  list_descriptions = []

  for listobj in tweepy.Cursor(api.lists_memberships, user_id=user_id, count=100).items():
    list_names.append(listobj.name)
    #list_descriptions.append(listobj.description)
  
  print("List names count", len(list_names))
  
  #seperate words from numbers, min 3 chars/digits 
  tokenizer = RegexpTokenizer('[A-ZÄÖÜa-zäöüß]{3,}|\d{3,}')
  tokens = tokenizer.tokenize(' '.join(list_names + list_descriptions))
  tokens = [w.lower() for w in tokens]

  #nltk.download('stopwords') Download only once!
  
  stop_words = stopwords.words('german') + stopwords.words('english')

  custom_stopwords = ['tweet', 'twitter', 'twitterer', 'twitternd', 'twitternde', 'twitternden', 'tweeting', 'tweets', 'tweetdeck', 'twit', 'folgen', 'follow', 'user', 'list', \
                      'liste', 'alle', 'alles', 'test', 'www', 'http', 'biz', 'com', 'non', 'faves', 'fave', 'spam', 'shit', 'innen', 'interesting', 'interessant', \
                      'what', 'mitglied', 'wichtig', 'wichtige', 'allgemein' ]

  tokens_cleaned = [w for w in tokens if not w in (stop_words + custom_stopwords)]

  try:
    n = max(1, round(len(tokens_cleaned) / 100))
    most_common_tokens = Counter(tokens_cleaned).most_common()

    list_tags = [{'text': key,'value': value} for key, value in most_common_tokens if value > n]

    return list_tags
  except ZeroDivisionError:
    return []