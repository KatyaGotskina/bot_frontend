import logging.config
from contextvars import ContextVar

import yaml

from core.config import settings

with open('logging.conf.yml', 'r') as f:
    LOGGING_CONFIG = yaml.full_load(f)


class ConsoleFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        try:
            correlation_id = correlation_id_ctx.get()
            return '[%s] %s' % (correlation_id, super().format(record))
        except LookupError:
            return super().format(record)


correlation_id_ctx: ContextVar[str] = ContextVar('correlation_id_ctx')
logger = logging.getLogger('time_management_bot')


def setup_logger() -> None:
    logging.config.dictConfig(LOGGING_CONFIG)

    if settings.LOG_LEVEL == 'debug':
        logger.setLevel(logging.DEBUG)
