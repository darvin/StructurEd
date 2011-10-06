import yaml
from format import Format

class YamlFormat(Format):
    extensions = ("yaml",)
    description = "YAML"

    @classmethod
    def loads(cls, data_st):
        return yaml.load(data_st)

    @classmethod
    def dumps(cls, data):
        return yaml.dump(data)