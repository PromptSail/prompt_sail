import importlib
import inspect
from collections import OrderedDict, defaultdict
from functools import partial
from typing import Any

from utils import OrderedSet


def get_function_arguments(func):
    handler_signature = inspect.signature(func)
    kwargs_iterator = iter(handler_signature.parameters.items())
    parameters = OrderedDict()
    for name, param in kwargs_iterator:
        parameters[name] = param.annotation
    return parameters


def get_handler_arguments(func):
    """Handlers can have multiple arguments, but only the first of them can be a command, query or event."""
    parameters = get_function_arguments(func)
    kwargs_iterator = iter(parameters.items())
    _, first_parameter = next(kwargs_iterator)
    remaining_parameters = {}
    for name, param in kwargs_iterator:
        remaining_parameters[name] = param

    return first_parameter, remaining_parameters


class DependencyProvider:
    """Basic dependency provider that uses a dictionary to store and inject dependencies"""

    def __init__(self, **kwargs):
        self.dependencies = kwargs

    def register_dependency(self, identifier, dependency_instance):
        self.dependencies[identifier] = dependency_instance

    def get_dependency(self, identifier):
        return self.dependencies[identifier]

    def _resolve_arguments(self, handler_parameters, overrides) -> dict:
        """Match handler_parameters with dependencies"""

        def _resolve(identifier, overrides):
            if identifier in overrides:
                return overrides[identifier]
            return self.get_dependency(identifier)

        kwargs = {}
        for param_name, param_type in handler_parameters.items():
            # first, try to resolve by type
            if param_type is not inspect._empty:
                try:
                    kwargs[param_name] = _resolve(param_type, overrides)
                    continue
                except (ValueError, KeyError):
                    pass
            # then, try to resolve by name
            try:
                kwargs[param_name] = _resolve(param_name, overrides)
                continue
            except (ValueError, KeyError):
                pass

        return kwargs

    def get_function_kwargs(self, func, overrides=None):
        func_parameters = get_function_arguments(func)
        kwargs = self._resolve_arguments(func_parameters, overrides or {})
        return kwargs

    def get_handler_kwargs(self, func, overrides=None):
        _, handler_parameters = get_handler_arguments(func)
        kwargs = self._resolve_arguments(handler_parameters, overrides or {})
        return kwargs

    def __getitem__(self, key):
        return self.get_dependency(key)

    def __setitem__(self, key, value):
        self.register_dependency(key, value)


class TransactionContext:
    """A context spanning a single transaction for execution of a function"""

    def __init__(self, app, **overrides):
        self.app = app
        self.overrides = overrides
        self.dependency_provider = app.dependency_provider

    def __enter__(self):
        """Should be used to start a transaction"""
        self.app._on_enter_transaction_context(self)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Should be used to commit/end a transaction"""
        self.app._on_exit_transaction_context(self, exc_type, exc_val, exc_tb)

    def _wrap_with_middlewares(self, handler_func):
        p = handler_func
        for middleware in self.app._transaction_middlewares:
            p = partial(middleware, self, p)
        return p

    def _get_overrides(self, **kwargs):
        overrides = dict(ctx=self)
        overrides.update(self.overrides)
        overrides.update(kwargs)

        type_match = defaultdict(list)
        for name, value in overrides.items():
            type_match[type(value)].append(value)
        with_unique_type = dict((k, v[0]) for k, v in type_match.items() if len(v) == 1)

        overrides.update(with_unique_type)

        return overrides

    def call(self, handler_func, **kwargs):
        overrides = self._get_overrides(**kwargs)
        handler_kwargs = self.dependency_provider.get_function_kwargs(
            handler_func, overrides
        )
        p = partial(handler_func, **handler_kwargs)
        wrapped_handler = self._wrap_with_middlewares(p)
        result = wrapped_handler()
        return result

    def get_dependency(self, identifier: Any) -> Any:
        """Get a dependency from the dependency provider"""
        return self.dependency_provider.get_dependency(identifier)

    def __getitem__(self, item) -> Any:
        return self.get_dependency(item)


class ApplicationModule:
    def __init__(self, name, version=1.0):
        self.name = name
        self.version = version
        self.command_handlers = {}
        self.query_handlers = {}
        self.event_handlers = defaultdict(OrderedSet)

    def import_from(self, module_name):
        importlib.import_module(module_name)

    def __repr__(self):
        return f"<{self.name} v{self.version} {object.__repr__(self)}>"


class Application(ApplicationModule):
    def __init__(self, name=__name__, version=1.0, dependency_provider=None, **kwargs):
        super().__init__(name, version)
        self.dependency_provider = dependency_provider or DependencyProvider(**kwargs)
        self._transaction_middlewares = []
        self._on_enter_transaction_context = lambda ctx: None
        self._on_exit_transaction_context = lambda ctx, exc_type, exc_val, exc_tb: None
        self._modules = set([self])

    def include_module(self, a_module):
        assert isinstance(
            a_module, ApplicationModule
        ), "Can only include ApplicationModule instances"
        self._modules.add(a_module)

    def on_enter_transaction_context(self, func):
        self._on_enter_transaction_context = func
        return func

    def on_exit_transaction_context(self, func):
        self._on_exit_transaction_context = func
        return func

    def transaction_middleware(self, middleware_func):
        """Middleware for processing transaction boundaries (i.e. running a command or query)"""
        self._transaction_middlewares.insert(0, middleware_func)
        return middleware_func

    def transaction_context(self, **dependencies):
        return TransactionContext(self, **dependencies)
