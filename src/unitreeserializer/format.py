class Format(object):
    extensions = ("---",)
    description = "Some Format"
    __available_formats = {}
    __formats = {}
    _dump_func = lambda data: None
    _load_func = lambda data_st: None

    @classmethod
    def loads(cls, data_st):
        return cls._load_func(data_st)

    @classmethod
    def dumps(cls, data):
        return cls._dump_func(data)

    @classmethod
    def initialize(cls):
        return False

    @classmethod
    def get_formats(cls):
        if not cls.__available_formats:
            for format_exts, format in cls.__formats.iteritems():
                if format.initialize():
                    cls.__available_formats[format_exts] = format
        return cls.__available_formats.values()


    @classmethod
    def register(cls, format_class):
        if not issubclass(format_class, cls):
            raise NotImplementedError
        cls.__formats[format_class.extensions] = format_class
        return format_class