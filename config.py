from dotenv import load_dotenv
import os
import MySQLdb

load_dotenv()

user = os.environ['MYSQL_USER']
host = os.environ['MYSQL_HOST']
database = os.environ['MYSQL_DB']

oluser = os.environ['MYSQLONLINE_USER']
olhost = os.environ['MYSQLONLINE_HOST']
olpassword = os.environ['MYSQLONLINE_PASSWORD']
oldatabase = os.environ['MYSQLONLINE_DB']

MAILPASSW = os.environ['MAILPASSW']
MAILADDR  = os.environ['MAILADDR']


local_uri  = f'mysql://{user}:@{host}/{database}'
online_uri = f'mysql://{oluser}:{olpassword}@{olhost}/{oldatabase}'

DATA_BASE_CONNECTION_URI = local_uri


print(DATA_BASE_CONNECTION_URI)
