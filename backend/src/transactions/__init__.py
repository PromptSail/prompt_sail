from importlib import import_module

from lato import ApplicationModule

transactions = ApplicationModule("transactions")

import_module("transactions.use_cases")
import_module("transactions.event_handlers")
