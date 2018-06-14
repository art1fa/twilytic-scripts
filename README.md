Twilytic (Scripts)
============

Scripts to monitor Twitter and manage Tweet and User data.

## Installation

If not already present, install [RethinkDB](https://www.rethinkdb.com/docs/install/).

Install also the needed dependencies for the scripts to work.

```bash
pip3 install -r requirements.txt
```

## Configuration

Register your application at [apps.twitter.com](https://apps.twitter.com/) to get your API keys needed to communicate with the Twitter API.

Edit `tweepy_conf.py` and paste your application keys and secrets.

`db_conf.py` stores the database config. Edit if you need to.

## Usage

Make sure your RethinkDB database server is running and your database and tables are properly configured. Run the [server part of Twilytic](https://github.com/art1fa/twilytic-server) once to have the database, tables and indexes automatically created.

Run the scripts with Python 3.

### Fetch users and monitor them in real time

#### get_mdb_users.py

Fetches all German parliament representatives based on the Twitter lists of the official party accounts.
Secondly, classify them with keywords included in the processed Twitter lists the individual users are listed in.
Write them finally into the database.

#### streaming.py

Connect to Twitter's Streaming API, monitor the collected users and write Tweets into the database.

### Manage data

#### update_tweet_data.py

Update like and retweet counts from Tweets in the database. Edit the `minuteCount` variable to update all Tweets that were posted `minuteCount` from now.

#### update_user_data.py

Update user data from users in the database. Fields such as profile picture, description, name etc. will be updated.

#### delete_old_tweets.py

Delete all Tweets older than 30 days.

## Note 

To make Twilytic work, you also need to install, configure and run [twilytic-server](https://github.com/art1fa/twilytic-server) and [twilytic-client](https://github.com/art1fa/twilytic-client).


## About

Twilytic is the outcome of my Master's thesis at the Technical University of Munich. The thesis was issued and supervised by Prof. Dr. Jürgen Pfeffer from the chair of Computational Social Science and Big Data. Thank you so much!