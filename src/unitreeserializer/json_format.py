from format import Format

class JsonFormat(Format):
    extensions = ["---"]
    description = "Some Format"

    @classmethod
    def loads(cls, data_st):
        raise NotImplementedError

    @classmethod
    def dumps(cls, data):
        raise NotImplementedError

    @classmethod
    def is_available(cls):
        return False