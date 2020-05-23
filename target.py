import json
import xmltodict
import subprocess
import shlex
class Target:
    def __init__(self, url):
        self.url = url

    def update_url(self, url):
        self.url = url

    def scan(self):
        print("performing nmap")
        cmd=shlex.split('nmap -sV -oX nmap_output.xml {}'.format(self.url))
        subprocess.check_call(cmd)

    def convert_to_json(self):
        print("converting xml to json")
        f = open("nmap_output.xml")
        xml_content = f.read()
        f.close()
        f=open("nmap_output.json","w+")
        f.write(json.dumps(xmltodict.parse(xml_content), indent=4, sort_keys=True))
        f.close()
        print("result in nmap_output.json")
