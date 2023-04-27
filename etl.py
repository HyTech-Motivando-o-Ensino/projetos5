import xmltodict
import json
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="pj5data"
)

doc = dict()

with open('curriculos/cesar-franca.xml') as fd:
    doc = xmltodict.parse(fd.read())

with open('cv.json', 'w') as output:
    json.dump(doc, output)

