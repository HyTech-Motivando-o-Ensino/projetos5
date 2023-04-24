import xmltodict
import json

doc = dict()

with open('curriculos/cesar-franca.xml') as fd:
    doc = xmltodict.parse(fd.read())

with open('cv.json', 'w') as output:
    json.dump(doc, output)

print(doc)