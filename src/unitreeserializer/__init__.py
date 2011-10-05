__author__ = 'darvin'
import imp
formats = ["json", "plist"]
available_formats = []
print __name__
for format_name in formats:
#    try:
        format = imp.find_module(__name__+".{}_format".format(format_name))
#        format = __import__("unitreeserializer.{}_format".format(format_name))
#    except ImportError:
#        pass
#    else:
        available_formats.append(format)

class FormatNotAvailableError(Exception):
    pass


def loads(data_st, format):
    if format not in available_formats:
        raise FormatNotAvailableError
    else:
        return format.loads(data_st)

def dumps(data, format):
    if format not in available_formats:
        raise FormatNotAvailableError
    else:
        return format.dumps(data)
    
