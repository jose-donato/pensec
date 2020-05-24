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
    tools_with_requirements = list(filter(lambda t: len(t.REQUIRES)!=0, tools))
    sorted_tools = list(filter(lambda t: len(t.REQUIRES)==0, tools))

    # como tornar um problema P em (quase) NP :')
    while(len(tools_with_requirements)>0):
        # percorrer tools por ordenar
        for i,t in enumerate(tools_with_requirements):
            fulfilled_requirements = 0
            for r in t.REQUIRES:
                if len(get_tools_providing(sorted_tools, r)) > 0:
                    fulfilled_requirements += 1
            # se sorted_tools dao todos os requirements
            if fulfilled_requirements == len(t.REQUIRES):
                t = tools_with_requirements.pop(i)
                sorted_tools.append(t)
    return sorted_tools




