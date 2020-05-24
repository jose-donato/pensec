import xmltodict

def parsexmlfile(filename):
    with open(filename) as f:
        xml = xmltodict.parse(f)
    return xml
