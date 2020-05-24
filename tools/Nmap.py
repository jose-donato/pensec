from tools.Tool import Tool
from utils.Command import execute
from utils.Files import parsexmlfile
from pathlib import Path
import json
from mdutils.mdutils import MdUtils


class Nmap(Tool):
    PROGRAM = "nmap"
    OPTIONS = Tool.Options([
        Tool.Option("Detect Versions (default)", "-sV"),
        Tool.Option("Detect Versions and Vulnerabilities", "-sV --script nmap-vulners,vulscan --script-args vulscandb=scipvuldb.csv"),
    ])
    OPTIONS_PROMPT = OPTIONS.prompt()
    REQUIRES = []
    PROVIDES = [Tool.Dependencies.NMAP_SERVICES]
    
    # ter vários Nmaps cada um executado com opções diferentes
    def __init__(self, options):
        if options.isdigit(): # umas das opcoes built in
            options = Nmap.OPTIONS.selected(options) or ''
        self.files = []
        if not options:
            options = "-sV"
        super().__init__("nmap", options)

    '''
    def run_search_cve(self):
        # discover current path
        target = self.target.hostname
        ports = self.target.target_ports
        #port = self.target.port  # or common_ports and loop through
        files = []
        for port in ports:
            outfile = f"'{self.outdir}/{self.name}_{self.options}_{port}_cve_detection.xml'"
            files.append(outfile[1:-1])
            scripts = "--script nmap-vulners,vulscan --script-args vulscandb=scipvuldb.csv"
            port_command = f"-p {port}"
            command = f"nmap {self.options} --datadir {self.assetdir} {scripts} {port_command} {target} -oX {outfile}"
            self.logger.info(f"Running Nmap with CVE detection scripts for port {port}: {command}")
        return files, ""

    
    def run_and_return_json(self):
        target = self.target.hostname
        outfile = f"'{self.outdir}/{self.name}_{self.options}.xml'"
        command = f"nmap {self.options} {target} -oX {outfile}"
        self.logger.info(f"Running Nmap: {command}")
        out, err = execute(command)
        file_path = str(Path().absolute())+"/"+outfile[1:-1]
        xml_dict = parsexmlfile(file_path)
        result = json.dumps(xml_dict)
        return result, err

    def run(self):
        target = self.target.hostname
        outfile = f"'{self.outdir}/{self.name}_{self.options}.xml'"
        command = f"nmap {self.options} {target} -oX {outfile}"
        self.logger.info(f"Running Nmap: {command}")
        out, err = execute(command)
        file_path = str(Path().absolute())+"/"+outfile[1:-1]
        return file_path, err
        '''
        
    def run(self):
        target = self.target.hostname
        if "--script nmap-vulners,vulscan --script-args vulscandb=scipvuldb.csv" in self.options:
            ports = self.target.target_ports
            #port = self.target.port  # or common_ports and loop through
            files = []
            for port in ports:
                outfile = f"'{self.outdir}/{self.name}_{port}_cve_detection.xml'"
                files.append(str(Path().absolute())+"/"+outfile[1:-1])
                port_command = f"-p {port}"
                command = f"nmap --datadir {self.assetdir} {self.options} {port_command} {target} -oX {outfile[1:-1]}"
                self.logger.info(f"Running Nmap with CVE detection scripts for port {port}: {command}")
            self.files = files 
            return files, ""
        else: 
            outfile = f"'{self.outdir}/{self.name}_{self.options}.xml'"
            command = f"nmap {self.options} {target} -oX {outfile}"
            self.logger.info(f"Running Nmap: {command}")
            out, err = execute(command)
            file_path = str(Path().absolute())+"/"+outfile[1:-1]
            self.files = [file_path]
            return [file_path], err
    
    def report(self):
        xml_dict = parsexmlfile(self.files[0])
        result = json.dumps(xml_dict)
        nmap_results = json.loads(result)
        ports = nmap_results["nmaprun"]["host"]["ports"]
        if 'port' in ports:
            open_ports = ports["port"]
        else:
            open_ports = []
        self.logger.info("Creating report for "+self.name)
        outfile = f"{self.reportdir}/{self.name}.md"
        title= f"PENSEC - {self.name.capitalize()} Report"
        reportfile = MdUtils(file_name=outfile, title=title)
        reportfile.new_header(level=1, title="Common Statistics")
        reportfile.new_paragraph(f"{len(open_ports)} open ports\n")
        if len(open_ports) > 0:
            reportfile.new_header(level=2, title="Open Ports")
            #list with open ports, cpe, etc
        reportfile.create_md_file()
        self.logger.info("Report saved in "+outfile)
        
