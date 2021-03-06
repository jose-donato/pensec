from tools.Tool import Tool
from utils.Command import execute
import json
from mdutils.mdutils import MdUtils
from pathlib import Path


class Searchsploit(Tool):
    PROGRAM = "searchsploit"
    OPTIONS_PROMPT = "Options (default: None)\n>> "
    IGNORE_STDERR = True
    REQUIRES = [Tool.Dependencies.NMAP_SERVICES]
    PROVIDES = [Tool.Dependencies.EXPLOITS]

    def __init__(self, options=""):
        self.files = []
        super().__init__("searchsploit", options)

    def run(self, dependencies):
        xml_files = dependencies[Tool.Dependencies.NMAP_SERVICES]
        for i, xml_file in enumerate(xml_files):
            command = f"searchsploit {self.options} --colour -v --nmap {xml_file} --json"
            self.logger.info(f"Running Searchsploit: {command}")
            out, err = execute(command)
            outfile = f"{self.outdir}/{self.name}_{self.options}_fromNmapXml_{i}.txt"
            self.files.append(str(Path().absolute())+"/"+outfile)
            with open(outfile, "a") as f:
                f.write(out.decode("utf-8"))
        return outfile, err
        
        


    '''
    #temp
    def run_custom(self, result_json):
        ports = json.loads(result_json)["nmaprun"]["host"]["ports"]["port"]
        # ciclo para cada serviço passado pelo nmap
        for port in ports:
            try:
                product = port["service"]["@product"]
                #    version = port["service"]["@version"]
                outfile = f"'{self.outdir}/{self.name}_{self.options}_{product}.json'"
                # command = f"searchsploit {self.options} {name} {version} > {outfile[1:-1]}"
                command = f"searchsploit {self.options} {product}"
                self.logger.info(f"Running Searchsploit: {command}")
                out, err = execute(command)
                print(out.decode("utf-8"))
            except:
                self.logger.error("Product not found in service")
        return "", ""
        # return execute(command)
    '''

    def report(self, reports):
        report_dict = reports[Tool.Dependencies.NMAP_SERVICES]
        self.logger.info("Creating report for "+self.name)
        obj = {}
        for f in self.files:
            with open(f, "r") as scanfile:
                for s in scanfile.read().split("\n\n")[:-1]:
                    scan = json.loads(s)
                    if 'RESULTS_EXPLOIT' in scan and 'SEARCH' in scan:
                        obj[scan["SEARCH"]] = {
                            "exploits": scan["RESULTS_EXPLOIT"]
                        }
        #temp
        outfile = f"{self.reportdir}/{self.name}.md"
        title= f"PENSEC - {self.name.capitalize()} Report"
        reportfile = MdUtils(file_name=outfile, title=title)
        reportfile.new_header(level=1, title="Common Statistics")
        reportfile.new_paragraph(f"X exploits found\n")
        reportfile.create_md_file()
        self.logger.info("Report saved in "+outfile)
        #report_dict["searchsploit_info"] = obj
        return obj

    def write_report_summary(self, reportfile, reports):
        searches = reports[Tool.Dependencies.EXPLOITS].items()
        n_exploits = 0
        for k, v in searches:
            n_exploits += len(v["exploits"])
        n_items = [f"{n_exploits} exploits found"]
        reportfile.new_list(items=n_items)


    def write_report(self, reportfile, reports):
        searches = reports[Tool.Dependencies.EXPLOITS].items()
        reportfile.new_header(level=3, title="Exploits")
        for k,v in searches:
            reportfile.new_header(level=5, title=k)
            types = {}
            for e in v["exploits"]:
                if e["Type"] in types:
                    types[e["Type"]].append(e)
                else:
                    types[e["Type"]] = [e]
            for t,exploits in types.items():
                reportfile.new_paragraph(t)
                n_items = [f"{e['Title']} ({e['Path']})"  for e in exploits]
                reportfile.new_list(items=n_items)
