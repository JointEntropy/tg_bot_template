from loguru import logger
from telegram.error import (TelegramError, Unauthorized, BadRequest,
                            TimedOut, ChatMigrated, NetworkError)
from telegram import ParseMode
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from tg.utils.handler_decorators import prepare_connection
import backend


@prepare_connection
def mention_handler(bot, update, conn):
    logger.debug('')
    chat_id = '@' + update.effective_user.username
    selected_theme_name = backend.get_user_theme_name(conn, chat_id)
    message = get_random_poetry_rf(selected_theme_name)

    # keyboard = [[InlineKeyboardButton('👍', callback_data=1),
    #              InlineKeyboardButton("👎", callback_data=-1)],
    # ]
    # reply_markup = InlineKeyboardMarkup(keyboard)
    response = bot.send_message(
        chat_id=update.effective_chat.id,
        text=message,
        parse_mode=ParseMode.HTML,
        # reply_markup=reply_markup
    )
    # Сохраняем сообщение в базу
    tg_message_id = response.message_id
    backend.add_post(conn, tg_message_id=tg_message_id, chat_id=update.effective_chat.id)






@prepare_connection
def select_theme(bot, update, conn):
    logger.debug('')
    themes = backend.get_themes(conn)
    keyboard = [
        [InlineKeyboardButton(theme['name'], callback_data=theme['id']) for i, theme in themes.iterrows()]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(
        chat_id=update.effective_chat.id,
        text='Выберите тему:',
        parse_mode=ParseMode.HTML,
        reply_markup=reply_markup
    )


@prepare_connection
def button_set_theme(bot, update, conn):
    logger.debug('')
    query = update.callback_query
    action_user_name = update.effective_user.name
    t = "Selected option: {} by user {}".format(query.data, action_user_name)
    logger.debug(t)
    query.answer()
    user_id = backend.get_or_create_user(conn, action_user_name)['id']
    # post_id = backend.find_post_by_tg_message(conn, update.effective_message['message_id'])['id']
    backend.set_user_theme(
        session=conn,
        user_id=user_id,
        theme_id=query.data
    )
    # reply_markup = query.message.reply_markup
    # for b in reply_markup.inline_keyboard[0]:
    #     b.text = '{}{}'.format(agg_post_scores.get(int(b.callback_data), 0), b.text[-1])
    # # query.edit_message_reply_markup(reply_markup)


@prepare_connection
def button_add_score(bot, update, conn):
    logger.debug('')
    query = update.callback_query
    action_user_name = update.effective_user.name
    t = "Selected option: {} by user {}".format(query.data, action_user_name)
    logger.debug(t)
    query.answer()
    post_id = backend.find_post_by_tg_message(conn, update.effective_message['message_id'])['id']
    user_id = backend.get_or_create_user(conn, action_user_name)['id']

    backend.add_score(session=conn, user_id=user_id, post_id=post_id, value=query.data)
    agg_post_scores = backend.get_post_scores_values(conn, post_id)
    reply_markup = query.message.reply_markup
    for b in reply_markup.inline_keyboard[0]:
        b.text = '{}{}'.format(agg_post_scores.get(int(b.callback_data), 0), b.text[-1])
    query.edit_message_reply_markup(reply_markup)


def error(bot, update, error):
    """
    Логировнаие непредвиденных ошибки.
    Args:
        bot: инстанст бота
        update: апдейты
        error: пойманная ошибка

    """
    try:
        raise error
    except (Unauthorized, BadRequest, TimedOut, \
            NetworkError, ChatMigrated, TelegramError) as e:
            # the chat_id of a group has changed, use e.new_chat_id instead
        logger.warning(f'Telegram related error occured: {e}')
        # handle all other telegram related errors
    except Exception as e:
        # print(traceback.extract_stack())
        logger.warning(f'Non telegram related error occured: {e}.')
