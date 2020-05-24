# Adapted from https://github.com/algofairness/fairness-comparison/blob/master/fairness/data/objects/list.py

from tools.Nmap import Nmap
from tools.Metasploit import Metasploit
from tools.Searchsploit import Searchsploit

TOOLS = [
    Nmap,
    Metasploit,
    Searchsploit
]