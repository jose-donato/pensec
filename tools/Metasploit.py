from tools.Tool import Tool

class Metasploit(Tool):
    PROGRAM = "msfconsole"
    def __init__(self, options=""):
        super().__init__("msfconsole", options)
        
    def run(self):
        raise NotImplementedError