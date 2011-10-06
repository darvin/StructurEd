import plistlib
from format import Format


class PlistFormat(Format):
    extensions = ("plist",)
    description = "Plist"


    @classmethod
    def dumps(cls, data):
        return plistlib.writePlistToString(data)

    @classmethod
    def loads(cls, data_st):
        return plistlib.readPlistFromString(data_st)
