"""
Example file to simulate an ETL process within a docker pipeline
- Extracts from a mongo db
- Transforms the collections
- Loads the transformed collections to postgres db

To be started by docker (see ../docker-compose.yml)
        
For inspecting that ETL worked out: docker exec -it pipeline_example_my_postgres_1 psql
"""


import pymongo
import sqlalchemy  # use a version prior to 2.0.0 or adjust creating the engine and df.to_sql()
import psycopg2
import time
import logging
import pandas as pd
from config import tokens  # This is from our config.py containing our credentials.
import logging.config
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
#from matplotlib import pyplot as plt
#import seaborn as sns

logging.basicConfig(level = logging.DEBUG,
		    filename = 'log-test.log',
		    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

# mongo db definitions
client = pymongo.MongoClient('mongodb', port=27017)  # mongodb(or any name like, my_mongo) is the hostname (= service in yml file)
db = client.reddit
dbcoll = db.posts


# postgres db definitions. HEADS UP: outsource these credentials and don't push to github.
USERNAME_PG = tokens['username']
PASSWORD_PG = tokens['password']
HOST_PG = 'postgresdb'  # postgresdb is the hostname (= service in yml file)
PORT_PG = 5432
DATABASE_NAME_PG = 'reddits_pgdb'

conn_string_pg = f"postgresql://{USERNAME_PG}:{PASSWORD_PG}@{HOST_PG}:{PORT_PG}/{DATABASE_NAME_PG}"

time.sleep(3)  # safety margine to ensure running postgres server
pg = sqlalchemy.create_engine(conn_string_pg)

# Create the table
create_table_string = sqlalchemy.text("""CREATE TABLE IF NOT EXISTS reddits (
                                         id TEXT,
                                         sub_id TEXT,
                                         date TEXT,
                                         title TEXT,
                                         text TEXT,
                                         compound NUMERIC
                                         );
                                         """)

pg.execute(create_table_string)



def extract():
    """
    reads collections from a mongo database and converts them into a pandas
    dataframe. 

    Returns
    -------
    new_reddits : pandas dataframe

    """

    new_mongo_docs = dbcoll.find()
    new_reddits = pd.DataFrame.from_records(list(new_mongo_docs))
    
    n_reddits = new_reddits.shape[0]

    logging.info(f"\n---- {n_reddits} reddits extracted ----\n")
    return new_reddits


def transform(new_reddits):
    """
    transforms a dataframe containing reddits in a dictionary to a clean
    dataframe and adds a column for the (dummy/length) sentiment of the reddit

    Parameters
    ----------
    new_reddits : unclean pandas dataframe

    Returns
    -------
    new_reddits_df : cleaned pandas dataframe including "sentiments"
    """
    
    new_reddits_df = pd.DataFrame()

    for _, row in new_reddits.iterrows():
        new_reddits_df = new_reddits_df.append(row['found_reddit'], ignore_index=True)
    
    return new_reddits_df

def sentimentAnalysis(new_reddits_df):
    analyser = SentimentIntensityAnalyzer()

    pol_scores = new_reddits_df['text'].apply(analyser.polarity_scores).apply(pd.Series)

    reddits_with_pols = pd.concat([new_reddits_df, pol_scores['compound']], axis=1)

    logging.debug("\n---- transformation completed ----\n")
 
    print(reddits_with_pols[['title','compound']])

    return reddits_with_pols

def load(reddits_with_pols):
    """
    saves cleaned reddits including their sentiments to a postgres database

    Returns
    -------
    None.

    """


    if reddits_with_pols.shape[0] > 0:  # only export if new reddits exist
        reddits_with_pols.to_sql('reddits', pg, if_exists='append', index=False)

    logging.debug("\n---- new reddits loaded to postgres db ----\n")
    
    return None

new_reddits = extract()
new_reddits_df = transform(new_reddits)
reddits_with_pols = sentimentAnalysis(new_reddits_df)
load(reddits_with_pols)
