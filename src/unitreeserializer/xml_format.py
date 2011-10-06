from format import Format

@Format.register
class XmlFormat(Format):
    extensions = ("xml",)
    description = "XML"

    @classmethod
    def loads(cls, data_st):
        raise NotImplementedError

    @classmethod
    def dumps(cls, data):
        raise NotImplementedError

    @classmethod
    def initialize(cls):
        return False