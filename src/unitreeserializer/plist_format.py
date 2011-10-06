import plistlib
from format import Format


@Format.register
class PlistFormat(Format):
    extensions = ("plist",)
    description = "Plist"


    @classmethod
    def dumps(cls, data):
        return plistlib.writePlistToString(data)

    @classmethod
    def loads(cls, data_st):
        return plistlib.readPlistFromString(data_st)
    
    @classmethod
    def initialize(cls):
        try:
            import plistlib
            return True
        except ImportError:
            return False