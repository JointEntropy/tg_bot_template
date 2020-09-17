# https://github.com/python-telegram-bot/python-telegram-bot/blob/master/examples/echobot2.py
from telegram.ext import Updater, MessageHandler, BaseFilter
from loguru import logger
from tg import handlers
import json


class MessageFilter(BaseFilter):
    def filter(self, message):
        triggers = set(['ещё!', ])
        message_tokens = set([c.lower() for c in (message.text or '').split(' ')])
        if len(triggers & message_tokens):
            return True
        return False


class TelegramInterface:
    """
    Интерфейс для телеграм бота.

    """
    def __init__(self, config):
        logger.debug(f'Init telegram interface')
        self.config = config
        bot_token = self.config.get('telegram_token', None)
        proxy_url = 'http://{}:{}@{}'.format(config.get('proxy_login'),
                                             config.get('proxy_pass'),
                                             config.get('proxy'))
        self.updater = Updater(bot_token, request_kwargs={'proxy_url': proxy_url})

        logger.info('Add handlers...')
        # Get the dispatcher to register handlers
        dp = self.updater.dispatcher
        dp.add_error_handler(handlers.error)

    def start(self):
        """
        Стартует цикл обработки запросов ботом.
        """
        poll_interval = self.config.get('poll_interval', 1)
        # Start the Bot
        logger.info('Start polling...')
        self.updater.start_polling(poll_interval=poll_interval)
        logger.info('Start idle')
        # Wait for inputs.
        self.updater.idle()

    def prepare_mention(self):
        self.updater.dispatcher.add_handler(MessageHandler(filters=MessageFilter(),
                                                           callback=handlers.mention_handler))

    def prepare_commands_handlers(self):
        pass
        # self.updater.dispatcher.add_handler(CommandHandler("select_theme", handlers.select_theme))
        # self.updater.dispatcher.add_handler(CallbackQueryHandler(handlers.button_set_theme))
        # self.updater.dispatcher.add_handler(CallbackQueryHandler(handlers.button_add_score))


if __name__ == '__main__':
    with open('debug_config.json', 'r') as f:
        config_example = json.load(f)['telegram']
    ti = TelegramInterface(config_example)
