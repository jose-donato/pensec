from subprocess import Popen, PIPE
import shlex

def execute(command):
    with Popen(shlex.split(command), stdout=PIPE, stderr=PIPE ) as p:
        out = p.stdout.read()
        err = p.stderr.read()
    # out.decode('ascii')
    # err.decode('ascii')
    return out, err