
import sqlalchemy 
import psycopg2
from config import tokens  # This is from our config.py containing our credentials.
import time
import requests
import logging
import logging.config

logging.basicConfig(level = logging.DEBUG,
		    filename = 'log-test.log',
		    format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

logger = logging.getLogger(__name__)

# postgres db definitions. HEADS UP: outsource these credentials and don't push to github.
USERNAME_PG = tokens['username']
PASSWORD_PG = tokens['password']
HOST_PG = 'postgresdb'  # postgresdb is the hostname (= service in yml file)
PORT_PG = 5432
DATABASE_NAME_PG = 'reddits_pgdb'

conn_string_pg = f"postgresql://{USERNAME_PG}:{PASSWORD_PG}@{HOST_PG}:{PORT_PG}/{DATABASE_NAME_PG}"

pg = sqlalchemy.create_engine(conn_string_pg)

webhook_url = tokens['webhook_url']

query = sqlalchemy.text("SELECT text,compound FROM reddits;")
result = pg.execute(query)

logger.info(f"Fetching data from Postgres")

# send each message to the webhook
for row in result:
    time.sleep(60)
    
    data = {
        "text": row["text"],
        "sentiment": str(row["compound"])
        }
    requests.post(url=webhook_url, json=data)
logger.debug("Slack Bot Data processed successfully")



    



