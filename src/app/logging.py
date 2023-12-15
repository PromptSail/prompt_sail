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
        cid = str(logging_context.correlation_id or "")
        # make cid first 4 characters and 4 last characters visible
        record.correlation_id = f"{cid[:4]}...{cid[-4:]}" if cid else ""
        return True


formatter = logging.Formatter("%(asctime)-15s %(name)-5s %(levelname)-8s %(correlation_id)s %(message)s")
handler = logging.StreamHandler()
handler.setFormatter(formatter)
context_filter = ContextFilter()
logger = logging.getLogger("app")
logger.addFilter(context_filter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

logger.info("Hello World!")
