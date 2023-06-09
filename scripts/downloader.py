import mysql.connector
import os
from xml.etree import ElementTree as ET
from datetime import datetime

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
        # tree = ET.parse(f"../curriculos/{file}")
        # tree = ET.parse(f"./curriculos/{file}")
        with open(f"./curriculos/{file}", "rb") as f:
            root = ET.fromstring(f.read())
            tree = ET.ElementTree(root)

        xml_string = ET.tostring(tree.getroot(), encoding='utf-8')
        # print("[DEBUG]", xml_string)

        query = "INSERT INTO arquivos_xml (created_at, updated_at, payload, status_extracao) VALUES (%s, %s, %s, %s)"
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        values = (now, now, xml_string, 0)

        cur.execute(query, values)

    conn.commit()
except Exception as e:
    print(e)
    conn.rollback()
finally:
    print("[DEBUG] Finished executing downloader.py statements")
    cur.close()
    conn.close()

