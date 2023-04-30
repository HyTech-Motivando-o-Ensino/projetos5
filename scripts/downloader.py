import mysql.connector
import os
from xml.etree import ElementTree as ET

conn = mysql.connector.connect(
    # host="localhost",
    host="db",
    user="root",
    password="password",
    database="pj5data"
)

cur = conn.cursor()

try:
    # for file in os.listdir("../curriculos"):
    for file in os.listdir("./curriculos"):
        print(file)
        # tree = ET.parse(f"../curriculos/{file}")
        tree = ET.parse(f"./curriculos/{file}")
        xml_string = ET.tostring(tree.getroot(), encoding='unicode')
        # print("[DEBUG]", xml_string)

        query = "INSERT INTO arquivos_xml (payload, status_extracao) VALUES (%s, %s)"
        values = (xml_string, 0)

        cur.execute(query, values)

    conn.commit()
except:
    conn.rollback()
finally:
    cur.close()
    conn.close()
