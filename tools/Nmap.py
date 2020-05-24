from tools.Tool import Tool
from utils.Command import execute
from utils.Files import parsexmlfile
from pathlib import Path
import json


class Nmap(Tool):
    PROGRAM = "nmap"
    OPTIONS_PROMPT = "Options (default: -sV)\n>> "
    # ter vários Nmaps cada um executado com opções diferentes

    def __init__(self, options):
        if not options:
            options = "-sV"
        super().__init__("nmap", options)

    def run_search_cve(self):
        # discover current path
        target = self.target.hostname
        #port = self.target.port  # or common_ports and loop through
        outfile = f"'{self.outdir}/{self.name}_{self.options}_cve_detection.xml'"
        scripts = "--script nmap-vulners,vulscan --script-args vulscandb=scipvuldb.csv"
        port_command = f"-p {80}"
        command = f"nmap {self.options} --datadir {self.assetdir} {scripts} {port_command} {target} -oX {outfile}"
        self.logger.info(f"Running Nmap with CVE detection scripts: {command}")
        return execute(command)

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
