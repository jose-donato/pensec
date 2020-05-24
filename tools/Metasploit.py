from tools.Tool import Tool

class Metasploit(Tool):
    def __init__(self, options=""):
        super().__init__("Metaploit", options)
        
    def run(self):
        raise NotImplementedError