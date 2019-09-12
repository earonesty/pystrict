# pylint: disable=protected-access

import inspect, itertools, functools

__all__ = ['strict', 'StrictError']

class StrictError(TypeError):
    pass

def _check_args(func):
    info = inspect.getfullargspec(func)

    for k in itertools.chain(info.args, info.kwonlyargs):
        if k != "self" and k not in func.__annotations__:
            raise StrictError("%s missing type specifier in __init__" % k)

def _init_decorator(func):
    _check_args(func)

    @functools.wraps(func)
    def wrapper(self, *args, **kwargs):
        func(self, *args, **kwargs)
        self._x_frozen = True
    return wrapper

def strict(thing):
    if inspect.isfunction(thing):
        func = thing
        _check_args(func)
        return func
    else:
        cls = thing

        def frozen_setattr(self, key, value):
            if self._x_frozen and not hasattr(self, key):
                raise StrictError("Class %s is frozen. Cannot set '%s'." % (cls.__name__, key))
            cls._x_setter(self, key, value)

        cls._x_frozen = False
        cls._x_setter = getattr(cls, "__setattr__", object.__setattr__)
        cls.__setattr__ = frozen_setattr
        cls.__init__ = _init_decorator(cls.__init__)
    return cls
