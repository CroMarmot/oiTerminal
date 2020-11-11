from functools import wraps


def Singleton(cls):
    __instances = {}

    @wraps(cls)
    def get_instance(*args, **kwargs):
        if cls not in __instances:
            __instances[cls] = cls(*args, **kwargs)
        return __instances[cls]

    return get_instance
