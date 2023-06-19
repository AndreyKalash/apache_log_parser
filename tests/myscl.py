from sqlalchemy import create_engine
import configparser
from sqlalchemy import MetaData, Table, String, Integer, Column, Text, DateTime, Boolean
from datetime import datetime



config = configparser.ConfigParser()
config.read('config.ini')

config = config['Database']

engine = create_engine(f"mysql+mysqlconnector://{config['username']}:{config['password']}@{config['host']}:{config['port']}/", echo=True)



metadata = MetaData()
blog = Table('blog', metadata, 
    Column('id', Integer(), primary_key=True),
    Column('post_title', String(200), nullable=False),
    Column('post_slug', String(200),  nullable=False),
    Column('content', Text(), nullable=False),
    Column('published', Boolean(), default=False),
    Column('created_on', DateTime(), default=datetime.now),
    Column('updated_on', DateTime(), default=datetime.now, onupdate=datetime.now)
)