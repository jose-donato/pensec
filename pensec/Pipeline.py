import os,re
from datetime import datetime
from pensec.Config import Config
from pensec.Target import Target
from utils.Logger import Logger
from utils.Dependencies import check_dependencies
from utils.Terminal import acknowledge
from tools.list import TOOLS, missing_tool_dependencies, sortby_dependencies
from pathlib import Path
from mdutils.mdutils import MdUtils
from tools.Tool import Tool

class Pipeline(object):
    def __init__(self, hostname="scanme.nmap.org", config=None):
        self.config = Config.from_file(config) if config else Config()
        self.target = Target(hostname)
        self.tools = []
        self.outdir = self.make_outdir()
        self.assetdir =  self.get_assetdir()
        self.logger = Logger(self.config, f"{self.outdir}/logs")   

        self.available = self.check_dependencies()
        self.load_tools()
        self.logger.info(f"Pipeline initialized for target: {hostname}")

    # load from config
    def load_tools(self):
        for k,v in self.config.tools():
            tool, options = v.split(";")
            Tool = list((T for T in TOOLS if T.__name__==tool and T in self.available))[0]
            self.add_tool(Tool(options), from_config=True)

    def add_tool(self, tool, from_config=False):
        self.logger.info(f"Adding {tool}")
        for t in self.tools:
            if tool == t: # same tool with same options...
                self.logger.info(f"Duplicate")
                return
        tool.set_logger(self.logger)
        tool.set_target(self.target)
        tool.set_outdir(f"{self.outdir}/commands")
        tool.set_reportdir(f"{self.outdir}/reports")
        tool.set_assetdir(self.assetdir)
        self.tools.append(tool)
        if from_config == False:
            if not hasattr(self, "tool_iota"):
                # self.tool_iota = len(self.config.tools())
                tool_indexes = [int(k.split("_")[-1]) for k,v in self.config.tools()]
                self.tool_iota = len(tool_indexes) and max(tool_indexes)
            self.tool_iota += 1
            setattr(self.config, f"TOOL_{self.tool_iota}", f"{repr(tool)}")
        self.logger.info(f"Success")
        return -1 # "só" ficar uniforme com o comportamento do remove_tool

    def remove_tool(self, tool):
        self.logger.info(f"Removing {tool}")
        for t in self.tools:
            if tool == t: # same tool with same options...
                self.tools.remove(t)
                configentry = [v for k,v in self.config.tools()].index(repr(tool))
                delattr(self.config, f"{self.config.tools()[configentry][0]}")
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
        missing = missing_tool_dependencies(self.tools)
        if missing:
            self.logger.error(missing)
            self.logger.error("Did not execute. Please fullfil requirements...")
            return
        sorted_tools = sortby_dependencies(self.tools)
        self.logger.debug(f"Tool order: {','.join([t.__class__.__name__ for t in sorted_tools])}")
        
        outputs = {}
        reports = {}
        report_obj = None
        for tool in sorted_tools:
            out, err = tool.run(outputs)
            for p in tool.PROVIDES:
                outputs[p] = out
            
            
            if err and not tool.IGNORE_STDERR:
                self.logger.error(err.decode('ascii'))
            else:
                self.logger.info("Output saved")
                report_obj = tool.report(reports)
                for p in tool.PROVIDES:
                    reports[p] = report_obj
        self.create_report(reports)

    def create_report(self, reports):
        outfile = f"{self.outdir}/reports/Report.md"
        title= f"PENSEC - Report of {self.target.hostname}"
        reportfile = MdUtils(file_name=outfile, title=title)
        reportfile.new_header(level=3, title="Common Statistics")
        open_ports = reports[Tool.Dependencies.NMAP_SERVICES]["open_ports"]
        searches = reports[Tool.Dependencies.EXPLOITS].items()
        
        #title, path, type, platform
        n_open_ports = len(open_ports)
        n_exploits = 0
        for k,v in searches:
            n_exploits += len(v["exploits"])
        n_items = [f"{n_open_ports} open ports found", f"{n_exploits} exploits found"]
        reportfile.new_list(items=n_items)
        reportfile.new_header(level=3, title="")


        # wiorhuweuirweuirhwie

        reportfile.create_md_file()
        self.logger.info("Report saved in "+outfile)

    def check_dependencies(self):
        self.logger.info("Checking dependencies...")
        dependencies = TOOLS
        available = check_dependencies(dependencies, self.logger)
        if len(dependencies) != len(available):
            acknowledge()
        return available
    
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

    def viewconfig(self):
        self.logger.info(f"Showing current config:")
        self.logger.debug("\n"+str(self.config))
        print("\n")
        acknowledge()

    def saveconfig(self):
        outfile = input("Config name\n>> ")
        with open(f"config/{outfile}", "w+") as f:
            f.write(str(self.config))
        self.logger.info(f"Config saved to {outfile}")
    
    # called on exit from main menu
    def cleanup(self):
        self.logger.end()
        from utils.Menu import Menu
        return Menu.EXIT