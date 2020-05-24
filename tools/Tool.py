from datetime import datetime
from enum import Enum

class Tool(object):
    OPTIONS_PROMPT = "Options:\n>> "
    IGNORE_STDERR = False

    class Dependencies(Enum):
        NMAP_SERVICES = auto()

    def __init__(self, name, options):
        self.name = name
        self.options = options
    
    def __str__(self):
        return f"Tool: {self.name}, Options: {self.options}"
    def __repr__(self): # usada para representar tools na config
        return f"{self.__class__.__name__};{self.options}"

    def __eq__(self, other):
        if isinstance(other, Tool):
            return  self.name == other.name and\
                    self.options == other.options
        return False
    
    def get_name(self):
        return self.name

    def set_logger(self, logger):
        self.logger = logger
    def set_target(self, target):
        self.target = target
    def set_outdir(self, outdir):
        self.outdir = outdir
    def set_reportdir(self, reportdir):
        self.reportdir = reportdir
    def set_assetdir(self, assetdir):
        self.assetdir = assetdir

    def run(self):
        raise NotImplementedError

    def report(self):
        raise NotImplementedError