from loguru import logger
from db.utils import get_session


def prepare_connection(handler):
    logger.debug('')

    def pass_connection(*args, **kwargs):
        logger.debug('')
        handler(*args, **kwargs, conn=get_session())
    return pass_connection
