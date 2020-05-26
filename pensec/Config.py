# Adapted from https://github.com/jlamma/inv_proj/blob/master/config.py
import copy

"""
cfg = Config()
# override defaults
cfg = Config(OPTION=<something>)
cfg = Config.from_file('config/stealthy.txt')
"""
class Config(object):
    DEFAULTS_FILENAME = "defaults.txt"
    defaults = {}

    def __init__(self, **kwargs):
        if not Config.defaults:
            Config.defaults = Config.params_from_file(Config.DEFAULTS_FILENAME)
        for k, v in Config.defaults.items():
            # so adicionar tools default se nao estamos a carregar outro ficheiro (ie. temos kwargs)
            if not kwargs or not k.startswith("TOOL_"):
                setattr(self, k, v)

        for k, v in kwargs.items():
            setattr(self, k, v)
        self._initialized = True

    @classmethod
    def from_file(cls, filename):
        params = cls.params_from_file(filename)
        return cls(**params)

    @classmethod
    def params_from_file(cls, filename):
        params = copy.deepcopy(cls.defaults)
        with open(f"config/{filename}", "r") as fp:
            for line in fp:
                if len(line.strip()) == 0 or line.strip()[0] == '#':
                    continue
                k, *v = map(lambda s: s.strip(), line.split("="))
                v = '='.join(v)
                params[k] = eval(v)
        return params

    def tools(self):
        return [(k, getattr(self, k)) for k in self.__dict__ if k.startswith("TOOL")]

    def items(self):
        return ((k, getattr(self, k)) for k in self.__dict__ if not k.startswith("_"))

    def __setattr__(self, key, value):
        super.__setattr__(self, key, value)

    # será preciso quando removermos tool
    # def __delattr__(self, item):
    #    raise AttributeError("Cannot delete params.")

    def __str__(self):
        params = []
        for k,v in self.items():
            if type(v) is str:
                params.append("{} = '{}'".format(k,v))
            else:
                params.append("{} = {}".format(k,v))
        return '\n'.join(params)


