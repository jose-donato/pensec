import shlex
import subprocess
from progress.bar import Bar
from utils.Command import execute

#return true if a certain program is installed, false otherwise
def check_if_program_is_installed(program):
    try:
        out, err = execute(f'{program} --version')
    except: 
        return False
    return True

#return true if all dependencies are installed, false otherwise
def check_dependencies(dependencies, logger):
    available = []
    bar = Bar('Processing', max=len(dependencies))
    for dependency in dependencies:
        if not check_if_program_is_installed(dependency.PROGRAM):
            logger.warning(f"'{dependency.PROGRAM}' is not installed in the system")
        else:
            available.append(dependency)
        bar.next()
    bar.finish()
    return available