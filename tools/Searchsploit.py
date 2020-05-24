from tools.Tool import Tool

class Searchsploit(Tool):
    def __init__(self, options=""):
        super().__init__("searchsploit", options)
        
    def run(self):
        raise NotImplementedError