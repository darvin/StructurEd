import os
from format import Format
available_formats = []
try:
    from json_format import JsonFormat
    available_formats.append(JsonFormat)
except ImportError:
    pass

try:
    from plist_format import PlistFormat
    available_formats.append(PlistFormat)
except ImportError:
    pass
#
#try:
#    from xml_format import XmlFormat
#    available_formats.append(XmlFormat)
#except ImportError:
#    pass

try:
    from yaml_format import YamlFormat
    available_formats.append(YamlFormat)
except ImportError:
    pass


Format.register_formats(available_formats)

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


def _guess_format_by_filename(filename):
    basename, ext = os.path.splitext(filename)
    ext = ext.lstrip(".")
    try:
        return Format.get_format_by_extension(ext)
    except NotImplementedError:
        raise FormatNotAvailableError

def decode_file(filename):
    f = open(filename)
    return _guess_format_by_filename(filename).loads(f.read())

def encode_file(data, filename):
    f = open(filename, "w")
    f.write(_guess_format_by_filename(filename).dumps(data))

