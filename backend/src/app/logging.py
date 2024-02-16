import logging
from contextvars import ContextVar
from uuid import UUID


class LoggingContext:
    """
    Logging context for managing correlation ID.

    Uses ContextVar to store and retrieve correlation ID.
    """
    _correlation_id = ContextVar("correlation_id", default=None)

    @property
    def correlation_id(self):
        """
        Get the current correlation ID.

        :return: The current correlation ID.
        """
        return self._correlation_id.get()

    @correlation_id.setter
    def correlation_id(self, value: UUID):
        """
        Set the correlation ID.

        :param value: The value to set as the correlation ID.
        """
        self._correlation_id.set(value)


logging_context = LoggingContext()


class ContextFilter(logging.Filter):
    """
    Logging filter for adding correlation ID to log records.

    Inherits from logging.Filter.
    """
    def filter(self, record):
        """
        Filter method to add correlation ID to log records.

        :param record: The log record.
        :return: True to include the record, False to exclude it.
        """
        cid = str(logging_context.correlation_id or "")
        # make cid first 4 characters and 4 last characters visible
        record.correlation_id = f"{cid[:4]}...{cid[-4:]}" if cid else ""
        return True


formatter = logging.Formatter(
    "%(asctime)-15s %(name)-5s %(levelname)-8s %(correlation_id)s %(message)s"
)
handler = logging.StreamHandler()
handler.setFormatter(formatter)
context_filter = ContextFilter()
logger = logging.getLogger("app")
logger.addFilter(context_filter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger.info("Hello World!")
