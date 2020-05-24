import re
import subprocess
import shlex
import json
import requests
from progress.bar import Bar


def unquote(cpe):
    return re.compile('%([0-9a-fA-F]{2})', re.M).sub(lambda m: "\\" + chr(int(m.group(1), 16)), cpe)


def toStringFormattedCPE(cpe, autofill=False):
    cpe = cpe.strip()
    if not cpe.startswith('cpe:2.3:'):
        if not cpe.startswith('cpe:/'):
            return False
        cpe = cpe.replace('cpe:/', 'cpe:2.3:')
        cpe = cpe.replace('::', ':-:')
        cpe = cpe.replace('~-', '~')
        cpe = cpe.replace('~', ':-:')
        cpe = cpe.replace('::', ':')
        cpe = cpe.strip(':-')
        cpe = unquote(cpe)
    if autofill:
        e = cpe.split(':')
        for x in range(0, 13-len(e)):
            cpe += ':-'
    return cpe


#return true if a certain program is installed, false otherwise
def check_program_is_installed(program):
    cmd = shlex.split('{} --version'.format(program))
    try:
        result = subprocess.run(cmd, capture_output=True)
    except:
        return False
    else:
        return True
    #if "not found" in result.stdout.decode("utf-8"):
    #    return False
    #return True

dependencies = ["nmap", "searchsploit", "msfconsole"]

#return true if all dependencies are installed, false otherwise
def check_dependencies(dependencies):
    bar = Bar('Processing', max=len(dependencies))
    for dependency in dependencies:
        if not check_program_is_installed(dependency):
            #sys.stdout.write('{} is not installed in the system'.format(dependency))
            return False
        bar.next()
    bar.finish()
    return True


#search exploits from keywords, return JSON object with results, None otherwise 
def search_exploits(keywords):
    cmd = shlex.split('searchsploit {} -j'.format(keywords))
    try:
        result = subprocess.run(cmd, capture_output=True)
        output = result.stdout.decode("utf-8")
        return json.loads(output)
    except:
        return None


#cve_id = CVE-2010-3333
#try to grab cve info, returns json in success, None otherwise
def get_cve_info_id(cve_id):
    if re.match(r"CVE-[0-9]{4}-[0-9]+", cve_id.upper()): #check if valid cve id
        try:
            response = requests.get('https://cve.circl.lu/api/cve/{}'.format(cve_id))
            return response.json()
        except:
            return None
    return None

#get_cve_info_id("cve-2010-3333")

#print(search_exploits("linux ssh"))

#a = toStringFormattedCPE("cpe:/h:tp-link:wpa4220")
#print(a)

#print(check_dependencies(dependencies))

#print(check_program_is_installed("nmap1"))