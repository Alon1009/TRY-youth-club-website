from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Make_account(Base):
    __tablename__ = 'sign up'
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    email = Column(String)
    password = Column(String)
    admin = Column(Boolean)


class Create_workshop(Base):
	__tablename__ = 'add_workshop'
	id = Column(Integer, primary_key=True)
	workshop_name = Column(String)
	details = Column(String)
	pictures = Column(String)



class Registered_users(Base):
	__tablename__ = 'people_ids'
	id = Column(Integer, primary_key=True)
	workshop_id = Column(Integer)
	user_id = Column(Integer)


class Create_news(Base):
	__tablename__ = 'add_news'
	id = Column(Integer, primary_key=True)
	news_title = Column(String)
	details = Column(String)
	pictures = Column(String)
		