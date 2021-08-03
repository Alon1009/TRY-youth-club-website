from model import Base, Make_account, Create_workshop, Registered_users

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


engine = create_engine('sqlite:///database.db', connect_args={'check_same_thread':False})
Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()