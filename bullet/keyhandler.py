from .charDef import *
from . import utils

def register(key):
    '''
    Mark the function with the key code that it handles so
    that it can found by _KeyHandlerRegisterer.
    '''
    def wrap(func):
        setattr(func, '_handle_key', key)
        return func
    return wrap

def init(cls):
    ''' Rewrite the class to include the _KeyHandlerRegisterer metaclass. '''
    return _KeyHandlerRegisterer(cls.__name__, cls.__bases__, cls.__dict__.copy())

class _KeyHandlerRegisterer(type):
    def __new__(cls, name, bases, classdict):
        result = super().__new__(cls, name, bases, classdict)
        setattr(result, 'key_handler', {})
        setattr(result, 'handle_input', _KeyHandlerRegisterer.handle_input)

        for value in classdict.values():
            handled_key = getattr(value, '_handle_key', None)
            if handled_key is not None:
                result.key_handler[handled_key] = value

        return result

    @staticmethod
    def handle_input(self):
        c = utils.getchar()
        i = c if c == UNDEFINED_KEY else ord(c)
        handler = self.key_handler.get(i)
        if handler is not None:
            return handler(self)
        else:
            return None
