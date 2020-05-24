from tools.Tool import Tool
from utils.Command import execute
import json


class Searchsploit(Tool):
    PROGRAM = "searchsploit"
    OPTIONS_PROMPT = "Options (default: None)\n>> "

    def __init__(self, options=""):
        super().__init__("searchsploit", options)

    def run(self, xml_file):
        command = f"searchsploit {self.options} --nmap {xml_file}"
        self.logger.info(f"Running Searchsploit: {command}")
        out, err = execute(command)
        outfile = f"{self.outdir}/{self.name}_{self.options}_fromNmapXml.txt"
        with open(outfile, "w+") as f:
            f.write(out.decode("utf-8"))
        return out, err


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
