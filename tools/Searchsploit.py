from tools.Tool import Tool
from utils.Command import execute

class Searchsploit(Tool):
    PROGRAM = "searchsploit"
    OPTIONS_PROMPT = "Options (default: None)\n>> "

    def __init__(self, options=""):
        super().__init__("searchsploit", options)

    def run(self, keywords):
        # ciclo para cada serviço passado pelo nmap
        outfile = f"'{self.outdir}/{self.name}_{self.options}.json'"
        command = f"searchsploit {self.options} {keywords} > {outfile}"
        self.logger.info(f"Running Searchsploit: {command}")
        return execute(command)
