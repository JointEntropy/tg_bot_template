from loguru import logger
from tg.api import TelegramInterface


class NotificationPipeline:
    def __init__(self, config):
        logger.debug('')
        self.config = config
        self.telegram = TelegramInterface(config['telegram'])

    def start(self):
        logger.debug('')
        self.telegram.prepare_mention()
        self.telegram.prepare_commands_handlers()
        self.telegram.start()


if __name__ == '__main__':
    # print(get_random_poetry_rf())
    pass