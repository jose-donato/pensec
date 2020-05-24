# pensec

```
https://github.com/pypa/pipenv#installation
pipenv install
# Nmap's fingerprinting, etc require root privileges
pipenv run sudo python3 pentest.py
```


verify if metasploit, searchsploit, nmap, are installed


https://csrc.nist.gov/CSRC/media/Projects/Security-Content-Automation-Protocol/documents/docs/2008-conf-presentations/scaptutorial/2-enumerations.pdf

cve - vulnerabilities
cpe - platforms
cce - configuration settings

nmap with cve output (long but gives CVE IDs):
https://null-byte.wonderhowto.com/how-to/easily-detect-cves-with-nmap-scripts-0181925/

use https://www.cve-search.org/api/ to search info about the CVE



ideas:
https://security.stackexchange.com/questions/46080/resources-for-determining-if-metasploit-has-exploit-for-given-cve


searchsploit openssh 6.6.1
--------------------------------------------------------------------------------------------------------------------------- ---------------------------------
 Exploit Title                                                                                                             |  Path
--------------------------------------------------------------------------------------------------------------------------- ---------------------------------
OpenSSH 2.3 < 7.7 - Username Enumeration                                                                                   | linux/remote/45233.py
OpenSSH 2.3 < 7.7 - Username Enumeration (PoC)                                                                             | linux/remote/45210.py
OpenSSH < 7.4 - 'UsePrivilegeSeparation Disabled' Forwarded Unix Domain Sockets Privilege Escalation                       | linux/local/40962.txt
OpenSSH < 7.4 - agent Protocol Arbitrary Library Loading                                                                   | linux/remote/40963.txt
OpenSSH < 7.7 - User Enumeration (2)                                                                                       | linux/remote/45939.py
--------------------------------------------------------------------------------------------------------------------------- ---------------------------------
Shellcodes: No Results

