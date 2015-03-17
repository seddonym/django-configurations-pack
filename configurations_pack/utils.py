import importlib


def settings_from_module(module_string):
    "Returns settings defined in a module as a dictionary."

    module = importlib.import_module(module_string)
    return dict([(i, getattr(module, i)) for i in dir(module) \
                                                        if i[0:2] != '__'])

class classproperty(object):
    """Decorator to provide class properties.
    
    Usage:
        class MyConfiguration(Configuration):
        
            @classproperty
            def FOO(cls):
                return [cls.BAR]
    
    """
    def __init__(self, fget):
        self.fget = fget

    def __get__(self, owner_self, owner_cls):
        return self.fget(owner_cls)
