from loguru import logger
from notification_pipeline import NotificationPipeline
from utils import read_json_dict

if __name__ == '__main__':
    logger.debug('Read config')
    config = read_json_dict('config.json')
    logger.debug('Running instance...')
    note_pipeline = NotificationPipeline(config)
    note_pipeline.start()
