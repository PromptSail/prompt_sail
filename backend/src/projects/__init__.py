from importlib import import_module

from lato import ApplicationModule

projects = ApplicationModule("projects")
import_module("projects.use_cases")
