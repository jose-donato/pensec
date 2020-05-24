from tools.Tool import Tool
from utils.Command import execute

class Nmap(Tool):
    OPTIONS_PROMPT = "Options (default: -sV)\n>> "
    # ter vários Nmaps cada um executado com opções diferentes
    def __init__(self, options):
        if not options:
            options = "-sV" 
        super().__init__("Nmap", options)

    def run(self):
        target = self.target.hostname
        outfile = f"'{self.outdir}/{self.name}_{self.options}.xml'"
        command = f"nmap {self.options} {target} -oX {outfile}"
        self.logger.info(f"Running Nmap: {command}")
        return execute(command)