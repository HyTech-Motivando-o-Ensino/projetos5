import mysql.connector
import os
from xml.etree import ElementTree as ET

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="pj5data"
)

cur = conn.cursor()

try:
    for file in os.listdir("../curriculos"):
        tree = ET.parse(f"../curriculos/{file}")
        xml_string = ET.tostring(tree.getroot(), encoding='unicode')
        print(xml_string)

        query = "INSERT INTO arquivos_xml (payload, status_extracao) VALUES (%s, %s)"
        values = (xml_string, 0)

        cur.execute(query, values)

    conn.commit()
except:
    conn.rollback()
finally:
    cur.close()
    conn.close()

