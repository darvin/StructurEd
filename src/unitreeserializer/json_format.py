import json
from format import Format


@Format.register
class JsonFormat(Format):
    extensions = ("json",)
    description = "JSON"

    @classmethod
    def dumps(cls, data):
        return json.dumps(data)

    @classmethod
    def loads(cls, data_st):
        return json.loads(data_st)

    @classmethod
    def initialize(cls):
        try:
            import json
            return True
        except ImportError:
            return False