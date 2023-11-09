import logging
from contextvars import ContextVar
from uuid import UUID


class LoggingContext:
    _correlation_id = ContextVar("correlation_id", default=None)

    @property
    def correlation_id(self):
        return self._correlation_id.get()

    @correlation_id.setter
    def correlation_id(self, value: UUID):
        self._correlation_id.set(value)


logging_context = LoggingContext()


class ContextFilter(logging.Filter):
    def filter(self, record):
        cid = str(logging_context.correlation_id) or ""
        # make cid first 4 characters and 4 last characters visible
        record.correlation_id = f"{cid[:4]}...{cid[-4:]}"
        return True


logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)-15s %(name)-5s %(levelname)-8s %(correlation_id)s %(message)s",
)

context_filter = ContextFilter()
logger = logging.getLogger("app")
logger.addFilter(context_filter)

logger.info("Hello World!")
