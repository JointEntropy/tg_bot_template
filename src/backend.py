from loguru import logger
import pandas as pd
from db.entities import Posts, Users, Scores


def find_post_by_tg_message(session, tg_message_id):
    logger.debug('')
    query = session.query(Posts).filter(Posts.tg_message_id == tg_message_id)
    post = pd.read_sql(query.statement, session.bind).to_dict(orient='records')
    return post[0]


def get_or_create_user(session, username):
    logger.debug('')
    query = session.query(Users).filter(Users.telegram_username == username)
    data = pd.read_sql(query.statement, session.bind)
    if data.shape[0] == 0:
        user = Users(telegram_username=username)
        session.add(user)
        session.commit()
        query = session.query(Users).filter(Users.telegram_username == username)
        data = pd.read_sql(query.statement, session.bind)
    user = data.to_dict(orient='records')[0]
    return user


def add_post(session, tg_message_id, chat_id):
    logger.debug('')
    new_post = Posts(tg_message_id=tg_message_id, chat_id=chat_id)
    session.add(new_post)
    session.commit()
    return new_post.id


def add_score(session, value, user_id, post_id):
    logger.debug('')
    score_instance = Scores(
        value=value,
        user_id=user_id,
        post_id=post_id,
    )
    session.add(score_instance)
    session.commit()


def get_post_scores_values(session, post_id):
    logger.debug('')
    query = session.query(Scores).filter(Scores.post_id == post_id)
    scores = pd.read_sql(query.statement, session.bind)
    return scores['value'].value_counts().to_dict()


def delete_score(session, post_id, user_id):
    logger.debug('')
    session.query(Scores).filter(Scores.post_id == post_id, Scores.user_id == user_id).delete()
    session.commit()

