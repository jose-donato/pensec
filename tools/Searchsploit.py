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
    PROVIDES = []

    def __init__(self, options=""):
        self.files = []
        super().__init__("searchsploit", options)

    def run(self, xml_files):
        i=0
        files = []
        for xml_file in xml_files:
            command = f"searchsploit {self.options} --colour -v --nmap {xml_file} --json"
            self.logger.info(f"Running Searchsploit: {command}")
            out, err = execute(command)
            outfile = f"{self.outdir}/{self.name}_{self.options}_fromNmapXml_{i}.txt"
            files.append(str(Path().absolute())+"/"+outfile])
            i+=1
            with open(outfile, "a") as f:
                f.write(out.decode("utf-8"))
        self.files = files 
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

    def report(self):
        self.logger.info("Creating report for "+self.name)
        for f in self.files:
            with open(f, "r") as scanfile:
                scan = json.loads(scanfile.read())
                print(scan)
        outfile = f"{self.reportdir}/{self.name}.md"
        title= f"PENSEC - {self.name.capitalize()} Report"
        reportfile = MdUtils(file_name=outfile, title=title)
        reportfile.new_header(level=1, title="Common Statistics")
        reportfile.new_paragraph(f"X exploits found\n")
        reportfile.create_md_file()
        self.logger.info("Report saved in "+outfile)
