from os import getenv
from sqlalchemy import create_engine
from dotenv import load_dotenv

load_dotenv()
database_uri = getenv('SQLALCHEMY_DATABASE_URI')

engine = create_engine(database_uri, echo=True, future=True)