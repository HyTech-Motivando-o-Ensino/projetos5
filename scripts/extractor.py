import xmltodict
import mysql.connector
from xml.etree import ElementTree as ET

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="pj5data",
    buffered=True
)

cur = conn.cursor(buffered=True)

SQL_INSERTS = {
    "insert_author": "INSERT INTO autores (nome_completo, resumo_cv, colaborador_cesar) VALUES (%s, %s, %s)",
    "insert_article": "INSERT INTO artigos (natureza, titulo, ano, idioma, doi, periodico_revista_id, pdf_file) VALUES(%s, %s, %s, %s, %s, 0, %s);"
}

def xmltodict_extraction():

    query = '''
    SELECT * FROM arquivos_xml t
    WHERE t.status_extracao = 0'''

    cur.execute(query)

    for (id, created, updated, payload, status) in cur:
        doc = xmltodict.parse(payload, encoding='utf-8')
        # print(doc)
        full_name = doc['CURRICULO-VITAE']['DADOS-GERAIS']['@NOME-COMPLETO']
        cv_description = doc['CURRICULO-VITAE']['DADOS-GERAIS']['RESUMO-CV']['@TEXTO-RESUMO-CV-RH']
        articles = doc['CURRICULO-VITAE']['PRODUCAO-BIBLIOGRAFICA']["ARTIGOS-PUBLICADOS"]["ARTIGO-PUBLICADO"]
        is_employee = True

        print(f"Autor: {full_name}")
        print(f"Resumo CV: {cv_description}")

        if type(articles) == list:
            for article in articles:
                # print(article)
                print("--------- ARTIGO ---------")
                print("Titulo:", article["DADOS-BASICOS-DO-ARTIGO"]["@TITULO-DO-ARTIGO"])
                print("Ano:", article["DADOS-BASICOS-DO-ARTIGO"]["@ANO-DO-ARTIGO"])
                print("Idioma:", article["DADOS-BASICOS-DO-ARTIGO"]["@IDIOMA"])
                print("Natureza:", article["DADOS-BASICOS-DO-ARTIGO"]["@NATUREZA"])
                print("DOI:", article["DADOS-BASICOS-DO-ARTIGO"]["@DOI"])
                print("Periodico:", article["DETALHAMENTO-DO-ARTIGO"]["@TITULO-DO-PERIODICO-OU-REVISTA"])
                print("Autores:")
                print(article["AUTORES"])
                print("--------------------------")

        else:
                print("--------- ARTIGO ---------")
                print("Titulo:", articles["DADOS-BASICOS-DO-ARTIGO"]["@TITULO-DO-ARTIGO"])
                print("Ano:", articles["DADOS-BASICOS-DO-ARTIGO"]["@ANO-DO-ARTIGO"])
                print("Idioma:", articles["DADOS-BASICOS-DO-ARTIGO"]["@IDIOMA"])
                print("Natureza:", articles["DADOS-BASICOS-DO-ARTIGO"]["@NATUREZA"])
                print("DOI:", articles["DADOS-BASICOS-DO-ARTIGO"]["@DOI"])
                print("Periodico:", articles["DETALHAMENTO-DO-ARTIGO"]["@TITULO-DO-PERIODICO-OU-REVISTA"])
                print("Autores:")
                print(article["AUTORES"])
                print("--------------------------")

def etree_extraction():
    global cur
    global conn
    query = '''
    SELECT * FROM arquivos_xml t
    WHERE t.status_extracao = 0'''

    cur.execute(query)

    for (id, created, updated, payload, status) in cur:
        SQL_DATA = {
            "author_id": 0
        }

        doc = ET.fromstring(payload)
        full_name = doc.find("./DADOS-GERAIS").attrib["NOME-COMPLETO"]
        cv_description = doc.find("./DADOS-GERAIS/RESUMO-CV").attrib["TEXTO-RESUMO-CV-RH"]
        articles = doc.find("./PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS").findall("ARTIGO-PUBLICADO")
        supervisions = doc.find("./OUTRA-PRODUCAO/ORIENTACOES-CONCLUIDAS")

        print(f"Autor: {full_name}")
        print(f"Resumo CV: {cv_description}")
        
        tuple_author = (full_name, cv_description, 1)
        newcur = conn.cursor(buffered=True)
        newcur.execute(SQL_INSERTS["insert_author"], tuple_author)
        conn.commit()
        SQL_DATA["author_id"] = cur.lastrowid

        for article in articles:
            basic_data_tag = article.find("./DADOS-BASICOS-DO-ARTIGO")
            details_tag = article.find("./DETALHAMENTO-DO-ARTIGO")
            authors = article.findall("AUTORES")
            print("--------- ARTIGO ---------")
            print("Titulo:", basic_data_tag.attrib["TITULO-DO-ARTIGO"])
            print("Ano:", basic_data_tag.attrib["ANO-DO-ARTIGO"])
            print("Idioma:", basic_data_tag.attrib["IDIOMA"])
            print("Natureza:", basic_data_tag.attrib["NATUREZA"])
            print("DOI:", basic_data_tag.attrib["DOI"])
            print("Periodico:", details_tag.attrib["TITULO-DO-PERIODICO-OU-REVISTA"])
            print("Autores: ", [author.attrib["NOME-COMPLETO-DO-AUTOR"] for author in authors])
            print("--------------------------")
        
        if supervisions:
            MASTERS_SUP = "ORIENTACOES-CONCLUIDAS-PARA-MESTRADO"
            PHD_SUP = "ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO"
            OTHER_SUP = "OUTRAS-ORIENTACOES-CONCLUIDAS"
            CESAR_ID = "091400000001"

            for supervision in supervisions:
                if supervision.tag == MASTERS_SUP:
                    basic_data_tag = supervision.find("./DADOS-BASICOS-DE-" + MASTERS_SUP)
                    details_tag = supervision.find("./DETALHAMENTO-DE-" + MASTERS_SUP)
                    print("--------- ORIENTAÇÃO DE MESTRADO ---------")

                elif supervision.tag == PHD_SUP:
                    basic_data_tag = supervision.find("./DADOS-BASICOS-DE-" + PHD_SUP)
                    details_tag = supervision.find("./DETALHAMENTO-DE-" + PHD_SUP)
                    print("--------- ORIENTAÇÃO DE DOUTORADO ---------")

                elif supervision.tag == OTHER_SUP:
                    basic_data_tag = supervision.find("./DADOS-BASICOS-DE-" + OTHER_SUP)
                    details_tag = supervision.find("./DETALHAMENTO-DE-" + OTHER_SUP)
                    print("--------- OUTRA ORIENTAÇÃO ---------")
                
                sup_title = basic_data_tag.attrib["TITULO"]
                sup_year = basic_data_tag.attrib["ANO"]
                sup_type = basic_data_tag.attrib["NATUREZA"]
                student = details_tag.attrib["NOME-DO-ORIENTADO"]
                institution = details_tag.attrib["NOME-DA-INSTITUICAO"]
                
                course = None
                if details_tag.attrib["CODIGO-INSTITUICAO"] == CESAR_ID:
                    course = details_tag.attrib["NOME-DO-CURSO"]



                print("Titulo:", sup_title)
                print("Ano:", sup_year)
                print("Natureza:", sup_type)
                print("Orientado:", student)
                print("Instituição:", institution)
                if course:
                    print("Curso da CESAR School:", course)

                print("--------------------------")



etree_extraction()

cur.close()
conn.close()