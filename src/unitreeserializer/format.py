class Format(object):
    extensions = ("---",)
    description = "Some Format"
    __available_formats = {}
    initialized = False
    _dump_func = lambda data: None
    _load_func = lambda data_st: None

    @classmethod
    def loads(cls, data_st):
        raise NotImplementedError

    @classmethod
    def dumps(cls, data):
        raise NotImplementedError


    @classmethod
    def get_formats(cls):
        assert (cls.initialized)
        return cls.__available_formats.values()


    @classmethod
    def get_format_by_extension(cls, ext):
        assert (cls.initialized)
        for key, value in cls.__available_formats.iteritems():
            if ext in key:
                return value
        raise NotImplementedError

    @classmethod
    def register_formats(cls, format_list):
        for format in format_list:
            cls.__available_formats[format.extensions] = format
        cls.initialized = True