from loguru import logger
from notification_pipeline import NotificationPipeline
from common_utils import read_json_dict
from db.entities import init_schema

if __name__ == '__main__':
    logger.debug('Read config')
    config = read_json_dict('config.json')
    logger.debug('Running instance...')

    if config['postgres']['init_db']:
        init_schema()
    note_pipeline = NotificationPipeline(config)
    note_pipeline.start()
