from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, TIMESTAMP, ForeignKey, Text
import datetime
from sqlalchemy.schema import MetaData
from db.utils import engine
from common_utils import read_json_dict
from loguru import logger

config = read_json_dict('config.json')
SCHEMA_NAME = config['postgres']['schema']
Base = declarative_base(metadata=MetaData(schema=SCHEMA_NAME))


class Posts(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True, autoincrement=True)
    create_ts = Column(TIMESTAMP, default=datetime.datetime.utcnow)
    tg_message_id = Column(Integer, nullable=False, unique=True)
    chat_id = Column(Integer, nullable=False)
    post_text = Column(Text, nullable=False)
    user_id = Column(Text, nullable=False)


class Users(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    telegram_username = Column(String, nullable=False, unique=True, )
    update_ts = Column(TIMESTAMP, default=datetime.datetime.utcnow, nullable=False)


class Scores(Base):
    __tablename__ = 'scores'
    id = Column(Integer, primary_key=True, autoincrement=True)
    value = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    create_ts = Column(TIMESTAMP, default=datetime.datetime.utcnow, nullable=False)
    post_id = Column(Integer, ForeignKey('posts.id'), nullable=False)


def init_schema():
    logger.debug('')
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


if __name__ == '__main__':
    init_schema()
