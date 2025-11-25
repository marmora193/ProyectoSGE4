from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine("postgresql+psycopg2://postgres:1234@localhost:5432/oro")

Session = sessionmaker(bind=engine)
session = Session()