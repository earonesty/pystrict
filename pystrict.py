# pylint: disable=protected-access

"""
## strict

Using @strict on classes can prevent serious errors by raising an
exception when an instance has a variable created outside of init.

"""

__version__ = "1.2"

import inspect, itertools, functools

__all__ = ['strict', 'StrictError']


class StrictError(TypeError):
    pass

def _check_args(func, *, checkret):
    info = inspect.getfullargspec(func)

    for k in itertools.chain(info.args, info.kwonlyargs):
        if k != "self" and k not in func.__annotations__:
            raise StrictError("%s argument %s is missing type specifier" % (func.__name__, k))

    if checkret:
        if "return" not in func.__annotations__:
            raise StrictError("%s missing return type specifier" % func.__name__)


def _init_decorator(func):
    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        self._x_frozen += 1
        func(self, *args, **kwargs)
        self._x_frozen -= 1
    return wrapper

def strict(thing):
    thing.__strict__ = True
    if inspect.isfunction(thing):
        func = thing
        _check_args(func, checkret=True)
        return func
    else:
        cls = thing

        def frozen_setattr(self, key, value):
            if not self._x_frozen and not hasattr(self, key):
                raise StrictError("Class %s is frozen. Cannot set '%s'." % (cls.__name__, key))
            cls._x_setter(self, key, value)

        cls._x_frozen = 0
        cls._x_setter = getattr(cls, "__setattr__", object.__setattr__)
        cls.__setattr__ = frozen_setattr
        _check_args(cls.__init__, checkret=False)
        cls.__init__ = _init_decorator(cls.__init__)
    return cls
