import shlex
import subprocess
from progress.bar import Bar


#REFACTOR to use Command 

#return true if a certain program is installed, false otherwise
def check_if_program_is_installed(program):
    cmd = shlex.split('{} --version'.format(program))
    try:
        subprocess.run(cmd, capture_output=True)
    except:
        return False
    else:
        return True


dependencies = ["nmap", "searchsploit", "msfconsole"]

#return true if all dependencies are installed, false otherwise
def check_dependencies(dependencies):
    bar = Bar('Processing', max=len(dependencies))
    for dependency in dependencies:
        if not check_if_program_is_installed(dependency):
            #sys.stdout.write('{} is not installed in the system'.format(dependency))
            return False
        bar.next()
    bar.finish()
    return True