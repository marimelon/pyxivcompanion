import datetime

def http_date_to_datetime(http_date, obs_date=False) -> datetime.datetime:
    strptime = datetime.datetime.strptime
    if not obs_date:
        return strptime(http_date, '%a, %d %b %Y %H:%M:%S %Z')
    time_formats = ('%a, %d %b %Y %H:%M:%S %Z',
                    '%a, %d-%b-%Y %H:%M:%S %Z',
                    '%A, %d-%b-%y %H:%M:%S %Z',
                    '%a %b %d %H:%M:%S %Y')
    for time_format in time_formats:
        try:
            return strptime(http_date, time_format)
        except ValueError:
            continue
    raise ValueError('time data %r does not match known formats' % http_date)

class ClassPropertyDescriptor(object):

    def __init__(self, fget, fset=None):
        self.fget = fget
        self.fset = fset

    def __get__(self, obj, klass=None):
        if klass is None:
            klass = type(obj)
        return self.fget.__get__(obj, klass)()

    def __set__(self, obj, value):
        if not self.fset:
            raise AttributeError("can't set attribute")
        type_ = type(obj)
        return self.fset.__get__(obj, type_)(value)

    def setter(self, func):
        if not isinstance(func, (classmethod, staticmethod)):
            func = classmethod(func)
        self.fset = func
        return self

def classproperty(func):
    if not isinstance(func, (classmethod, staticmethod)):
        func = classmethod(func)

    return ClassPropertyDescriptor(func)