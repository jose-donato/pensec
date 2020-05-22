import json
import xmltodict
import subprocess
import shlex
url = input("URL to scan: ")
print("performing nmap")
cmd=shlex.split('nmap -sV -oX nmap_output.xml {}'.format(url))
subprocess.check_call(cmd)
print("converting xml to json")
f = open("nmap_output.xml")
xml_content = f.read()
f.close()
f=open("nmap_output.json","w+")
f.write(json.dumps(xmltodict.parse(xml_content), indent=4, sort_keys=True))
f.close()
print("result in nmap_output.json")
