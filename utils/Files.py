import xmltodict

def parsexmlfile(filename):
    f = open(filename)
    xml = f.read()
    f.close()
    return xmltodict.parse(xml)
    #with open(filename) as f:
    #    xml = xmltodict.parse(f)
    #return xml
