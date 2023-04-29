import xmltodict
import json
import mysql.connector

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="pj5data"
)

mycursor = db.cursor()

# for line in open("minified-ddl.sql"):
#     # print(line)
#     mycursor.execute(line)

doc = dict()

ids = {
    "author_id": None
}
querys = {
    "insert_author": "INSERT INTO autores (nome_completo,resumo_cv,colaborador_cesar) VALUES (%s,%s, %s);"
}

with open('curriculos/cesar-franca.xml') as fd:
    doc = xmltodict.parse(fd.read())

    doc_cv = doc["CURRICULO-VITAE"]
    general_data = doc_cv["DADOS-GERAIS"]
    author_data = (general_data["@NOME-COMPLETO"], general_data["RESUMO-CV"]["@TEXTO-RESUMO-CV-RH"], 1)
    
    cursor = db.cursor()
    cursor.execute(querys["insert_author"], author_data)
    db.commit()

    ids["author_id"] = cursor.lastrowid

print(ids)

