from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey
import datetime
from sqlalchemy.schema import MetaData
from db.db_utils import engine


SCHEMA_NAME = 'tests'
Base = declarative_base(metadata=MetaData(schema=SCHEMA_NAME))


class Posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_ts = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    tg_message_id = Column(Integer, nullable=False, unique=True)
    chat_id = Column(Integer, nullable=False)


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_username = Column(String, nullable=False, unique=True, )
    update_ts = Column(TIMESTAMP, default=datetime.datetime.utcnow, nullable=False)
    theme_id = Column(Integer, ForeignKey('themes.id'), nullable=True)


class Scores(Base):
    __tablename__ = 'scores'
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    create_ts = Column(TIMESTAMP, default=datetime.datetime.utcnow, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)


def init_schema():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    init_schema()
