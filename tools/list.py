from tools.Nmap import Nmap
from tools.Metasploit import Metasploit
from tools.Searchsploit import Searchsploit

# Adapted from https://github.com/algofairness/fairness-comparison/blob/master/fairness/data/objects/list.py
TOOLS = [
    Nmap,
    Searchsploit,
    Metasploit,
]

def get_tools_providing(tools, requirement):
    return [T for T in tools if requirement in T.PROVIDES]

# call before running pipeline
def missing_tool_dependencies(tools):
    missing = ''
    for t in tools:
        for r in t.REQUIRES:
            if len(get_tools_providing(tools, r)) == 0:
                tools_providing = list(map(lambda T: T.__name__, get_tools_providing(TOOLS, r)))
                missing += f"Tool {t.__class__.__name__} requires {r.value} (provided by: {', '.join(tools_providing)})"
    return missing

def sortby_dependencies(tools):
    pass

