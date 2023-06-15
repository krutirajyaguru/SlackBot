"""
This script gets reddits from the reddit api 
and serves as the first step of the dockerized pipeline.

add Mongodb connection with pymongo and insert reddits into Mongodb 
"""


import requests
from requests.auth import HTTPBasicAuth
import sys
from config import tokens  # This is from our config.py containing our credentials.
import datetime
import pymongo
import logging
import logging.config


logging.basicConfig(level = logging.DEBUG,
		    filename = 'log-test.log',
		    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

# PREPARE AUTHENTIFICATION INFORMATION ##
# FOR REQUESTING A TEMPORARY ACCESS TOKEN ##

basic_auth = HTTPBasicAuth(
    username=tokens['client_id'], # the client id
    password=tokens['secret']  # the secret
)


GRANT_INFORMATION = dict(
    grant_type="password",
    username=tokens['username'], # REDDIT USERNAME
    password=tokens['password'] # REDDIT PASSWORD
)

headers = {
    'User-Agent': 'myApp'#name of reddit app
}

### POST REQUEST FOR ACCESS TOKEN

POST_URL = "https://www.reddit.com/api/v1/access_token"

access_post_response = requests.post(
    url=POST_URL,
    headers=headers,
    data=GRANT_INFORMATION,
    auth=basic_auth
).json()

### ADDING TO HEADERS THE Authorization KEY

headers['Authorization'] = access_post_response['token_type'] + ' ' + \
                           access_post_response['access_token']

## Send a get request to download the latest (new) subreddits using the new headers.

topic = 'Germany'
URL = f"https://oauth.reddit.com/r/{topic}/new"  # You could also select ".../hot" to fetch the most popular posts.

response = requests.get(
    url=URL,
    headers=headers  # this request would not work without the access token 
).json()

full_response = response['data']['children']

client = pymongo.MongoClient(host="mongodb", port=27017)
db = client.reddit # 'reddit' is name of db
dbnames = client.list_database_names()
if 'reddit' in dbnames:
    client.drop_database('reddit')# empty the database
# define collection
dbcoll = db.posts # includes database and collection name


for post in full_response:
    _id = post['data']['id']
    subreddit_id = post['data']['subreddit_id']
    time = post['data']['created_utc']  # time in seconds since 1970
    time = datetime.datetime.fromtimestamp(time).strftime('%Y-%m-%d %H:%M:%S')
    #subreddit = post['data']['subreddit']  # the above defined 'topic'
    title = post['data']['title']
    text = post['data']['selftext']  # the actual content
    

    logging.debug("\n---- retrieving reddit  ----\n")
    mongo_input = {'found_reddit' :{'id': _id, 'sub_id': subreddit_id, 'date': time, 'title': title,'text': text}}

    logging.debug("\n---- sending mongo input reddit to database ----\n")
    dbcoll.insert_one(mongo_input) # mongo_input is document

    if dbcoll.find_one(mongo_input):
        logging.debug("\n---- reddit successfully inserted to db ----\n")

 
