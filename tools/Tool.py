from datetime import datetime

class Tool(object):
    OPTIONS_PROMPT = "Options:\n>> "
    def __init__(self, name, options):
        self.name = name
        self.options = options
    
    def __str__(self):
        return f"Tool: {self.name}, Options: {self.options}"

    def __eq__(self, other):
        if isinstance(other, Tool):
            return  self.name == other.name and\
                    self.options == other.options
        return False

    def set_logger(self, logger):
        self.logger = logger
    def set_target(self, target):
        self.target = target
    def set_outdir(self, outdir):
        self.outdir = outdir

    def run(self):
        raise NotImplementedError