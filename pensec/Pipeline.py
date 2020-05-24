import os,re
from datetime import datetime
from pensec.Config import Config
from pensec.Target import Target
from utils.Logger import Logger
from utils.Dependencies import check_dependencies
from utils.Terminal import acknowledge
from tools.list import TOOLS
from pathlib import Path


class Pipeline(object):
    def __init__(self, hostname="scanme.nmap.org", config=None):
        self.config = Config.from_file(config) if config else Config()
        self.target = Target(hostname)
        self.tools = []
        self.outdir = self.make_outdir()
        self.assetdir =  self.get_assetdir()
        self.logger = Logger(self.config, f"{self.outdir}/logs")   

        self.check_dependencies()
        self.logger.info(f"Pipeline initialized for target: {hostname}")

    def add_tool(self, tool):
        self.logger.info(f"Adding {tool}")
        for t in self.tools:
            if tool == t: # same tool with same options...
                self.logger.info(f"Duplicate")
                return
        tool.set_logger(self.logger)
        tool.set_target(self.target)
        tool.set_outdir(f"{self.outdir}/commands")
        tool.set_assetdir(self.assetdir)
        self.tools.append(tool)
        self.logger.info(f"Success")
        return -1 # "só" ficar uniforme com o comportamento do remove_tool

    def remove_tool(self, tool):
        self.logger.info(f"Removing {tool}")
        for t in self.tools:
            if tool == t: # same tool with same options...
                self.tools.remove(t)
                self.logger.info(f"Success")
                return -1 # só para sair do menu... (forçar a atualizar)   
        self.logger.info(f"Not found")
        
    # def update_target(self, hostname):
        # self.target.set_target(hostname)
        # need to update for each tool? maybe refactor?


    def run(self):
        if len(self.tools) == 0:
            self.logger.error("Must add tools...")
            return
        
        # TODO:
        # verificar que não falta dependência
        # ordenar tools segundo dependências
        # obter output dos runs, passar para REPORTING e TOOLS subsequentes
        last_out = None
        last_tool_name = None
        for tool in self.tools:
            if last_tool_name == "nmap" and tool.name == "searchsploit":
                out, err = tool.run(last_out)
            else:
                out, err = tool.run()
            last_out = out
            last_tool_name = tool.name
            if err:
                self.logger.error(err.decode('ascii'))
            else:
                self.logger.info("Output saved")

    def check_dependencies(self):
        self.logger.info("Checking dependencies...")
        dependencies = TOOLS
        self.available = check_dependencies(dependencies, self.logger)
        if len(dependencies) != len(self.available):
            acknowledge()
    
    def make_outdir(self):
        hostname = self.target.hostname
        timestamp = re.sub(r'[/:]', '-', datetime.now().strftime('%x_%X'))
        outdir = f"{self.config.OUTPUT_DIRECTORY}/{hostname}/{timestamp}"
        os.makedirs(outdir)
        subdirs = ["logs", "commands", "reports"]
        for sd in subdirs:
            os.mkdir(f"{outdir}/{sd}")
        return outdir
    
    def get_assetdir(self):
        path = Path().absolute()
        return str(path)+"/assets/" 
