import mysql.connector
from xml.etree import ElementTree as ET
from Levenshtein import distance
from typing import List, Dict, Tuple

conn = mysql.connector.connect(
    # host="localhost",
    host="db",
    user="root",
    password="password",
    database="pj5data",
    buffered=True
)

cur = conn.cursor(buffered=True)

SQL_INSERTS = {
    "insert_author": "INSERT INTO autores (nome_completo, resumo_cv, colaborador_cesar) VALUES (%s, %s, %s)",
    "insert_article": "INSERT INTO artigos (natureza, titulo, ano, idioma, doi, periodico_revista_issn, pdf_file, sequencia_producao) VALUES(%s, %s, %s, %s, %s, %s, %s, %s);",
    "insert_author_article": "INSERT INTO autores_artigos (autor_id, artigo_id) VALUES(%s, %s)",
    "insert_supervision": "INSERT INTO orientacoes (titulo, ano, natureza, curso, instituicao, orientador_id) VALUES (%s, %s, %s, %s, %s, %s)",
}

def etree_extraction():
    global cur
    global conn
    # add articles already in the database
    ALL_ARTICLES: Dict[int, List[Tuple[int, int, str]]] = {}
    # add supervisions already in the database
    ALL_SUPERVISIONS: Dict[int, List[Tuple[int, str]]] = {}

    query = '''
    SELECT * FROM arquivos_xml t
    WHERE t.status_extracao = 0'''

    cur.execute(query)

    for (id, created, updated, payload, status) in cur:
        SQL_DATA = {
            "arquivo_id": id,
            "author_id": 0,
            "article_id": 0,
            "supervision_id": 0,
        }

        doc = ET.fromstring(payload, ET.XMLParser(encoding='ISO-8859-1'))
        full_name = doc.find("./DADOS-GERAIS").attrib["NOME-COMPLETO"]
        cv_description = doc.find("./DADOS-GERAIS/RESUMO-CV").attrib["TEXTO-RESUMO-CV-RH"]
        articles = doc.find("./PRODUCAO-BIBLIOGRAFICA/ARTIGOS-PUBLICADOS").findall("ARTIGO-PUBLICADO")
        supervisions = doc.find("./OUTRA-PRODUCAO/ORIENTACOES-CONCLUIDAS")

        print(f"[DEBUG] Autor: {full_name}")
        # print(f"Resumo CV: {cv_description}")
        
        tuple_author = (full_name, cv_description, 1)
        newcur = conn.cursor(buffered=True)
        newcur.execute(SQL_INSERTS["insert_author"], tuple_author)
        conn.commit()
        SQL_DATA["author_id"] = newcur.lastrowid
        # print("id do autor:", SQL_DATA["author_id"])

        for article in articles:
            MAX_TITLE_LENGTH = 200
            production_sequence = article.attrib["SEQUENCIA-PRODUCAO"]
            basic_data_tag = article.find("./DADOS-BASICOS-DO-ARTIGO")
            details_tag = article.find("./DETALHAMENTO-DO-ARTIGO")

            title = basic_data_tag.attrib["TITULO-DO-ARTIGO"]
            title = title[:MAX_TITLE_LENGTH] if len(title) > MAX_TITLE_LENGTH else title
            year = basic_data_tag.attrib["ANO-DO-ARTIGO"]
            language = basic_data_tag.attrib["IDIOMA"]
            article_type = basic_data_tag.attrib["NATUREZA"]
            doi = basic_data_tag.attrib["DOI"]
            # periodical = details_tag.attrib["TITULO-DO-PERIODICO-OU-REVISTA"]
            issn = details_tag.attrib["ISSN"]
            dash_pos = issn.find("-")
            if dash_pos != -1:
                issn = issn[:dash_pos] + issn[dash_pos + 1:]

            # authors = article.findall("AUTORES")
            # print("--------- ARTIGO ---------")
            # print("Titulo:", title)
            # print("Tamanho do titulo: ", len(title))
            # print("Ano:", year)
            # print("Idioma:", language)
            # print("Natureza:", article_type)
            # print("DOI:", doi)
            # print("Periodico:", periodical)
            # print("ISSN do periodico:", issn)
            # print("Autores: ", [author.attrib["NOME-COMPLETO-DO-AUTOR"] for author in authors])
            # print("--------------------------")

            tuple_article = (article_type, title, year, language, doi, issn, None, production_sequence)

            if not is_production_sequence_in(ALL_ARTICLES, production_sequence, year):

                if year not in ALL_ARTICLES:
                    ALL_ARTICLES[year] = []

                    newcur.execute(SQL_INSERTS["insert_article"], tuple_article)
                    conn.commit()

                    SQL_DATA["article_id"] = newcur.lastrowid
                    ALL_ARTICLES[year].append((SQL_DATA["article_id"], production_sequence, title))

                    newcur.execute(SQL_INSERTS["insert_author_article"], (SQL_DATA["author_id"], SQL_DATA["article_id"])) 
                    conn.commit()
                else:
                    duplicate = False
                    for article_id, prod_seq, article_title in ALL_ARTICLES[year]:
                        # Levenshtein
                        edit_distance = distance(title, article_title, processor=lambda s: s.strip().lower())
                        # Duplicate article
                        if edit_distance <= 5 and not duplicate:
                            print(f"[DEBUG] Duplicate article found: {title}")
                            newcur.execute(SQL_INSERTS["insert_author_article"], (SQL_DATA["author_id"], article_id)) 
                            conn.commit()
                            duplicate = True

                    if not duplicate:
                        newcur.execute(SQL_INSERTS["insert_article"], tuple_article)
                        conn.commit()

                        SQL_DATA["article_id"] = newcur.lastrowid
                        ALL_ARTICLES[year].append((SQL_DATA["article_id"], production_sequence, title))

                        newcur.execute(SQL_INSERTS["insert_author_article"], (SQL_DATA["author_id"], SQL_DATA["article_id"])) 
                        conn.commit()
            else:
                print(f"[DEBUG] Production sequence {production_sequence} already on articles list")

        if supervisions:
            MASTERS_SUP = "ORIENTACOES-CONCLUIDAS-PARA-MESTRADO"
            PHD_SUP = "ORIENTACOES-CONCLUIDAS-PARA-DOUTORADO"
            OTHER_SUP = "OUTRAS-ORIENTACOES-CONCLUIDAS"
            # CESAR_ID = "091400000001"

            for supervision in supervisions:
                if supervision.tag == MASTERS_SUP:
                    basic_data_tag = supervision.find("./DADOS-BASICOS-DE-" + MASTERS_SUP)
                    details_tag = supervision.find("./DETALHAMENTO-DE-" + MASTERS_SUP)
                    # print("--------- ORIENTAÇÃO DE MESTRADO ---------")

                elif supervision.tag == PHD_SUP:
                    basic_data_tag = supervision.find("./DADOS-BASICOS-DE-" + PHD_SUP)
                    details_tag = supervision.find("./DETALHAMENTO-DE-" + PHD_SUP)
                    # print("--------- ORIENTAÇÃO DE DOUTORADO ---------")

                elif supervision.tag == OTHER_SUP:
                    basic_data_tag = supervision.find("./DADOS-BASICOS-DE-" + OTHER_SUP)
                    details_tag = supervision.find("./DETALHAMENTO-DE-" + OTHER_SUP)
                    # print("--------- OUTRA ORIENTAÇÃO ---------")
                
                sup_title = basic_data_tag.attrib["TITULO"]
                sup_title = sup_title[:MAX_TITLE_LENGTH] if len(sup_title) > MAX_TITLE_LENGTH else sup_title
                sup_year = basic_data_tag.attrib["ANO"]
                sup_type = basic_data_tag.attrib["NATUREZA"]
                # student = details_tag.attrib["NOME-DO-ORIENTADO"]
                institution = details_tag.attrib["NOME-DA-INSTITUICAO"]

                course = details_tag.attrib["NOME-DO-CURSO"]

                # print("Titulo:", sup_title)
                # print("Ano:", sup_year)
                # print("Natureza:", sup_type)
                # print("Orientado:", student)
                # print("Instituição:", institution)
                # print("Curso:", course)

                supervision_tuple = (sup_title, sup_year, sup_type, course, institution, SQL_DATA["author_id"])

                newcur.execute(SQL_INSERTS["insert_supervision"], supervision_tuple) 

                if sup_year not in ALL_SUPERVISIONS:
                    ALL_SUPERVISIONS[sup_year] = []

                    newcur.execute(SQL_INSERTS["insert_supervision"], supervision_tuple)
                    conn.commit()

                    SQL_DATA["supervision_id"] = newcur.lastrowid
                    ALL_SUPERVISIONS[sup_year].append((SQL_DATA["supervision_id"], sup_title))

                else:
                    duplicate = False
                    for supervision_id, supervision_title in ALL_SUPERVISIONS[sup_year]:
                        if (sup_title == supervision_title or
                            sup_title in supervision_title or
                            supervision_title in sup_title):
                            print("[DEBUG] supervision already in database")
                            print(f"[DEBUG] current supervision: {sup_title}")
                            print(f"[DEBUG] supervision in database: {supervision_title} | id {supervision_id}")
                            print("------------------------------------------------")
                            duplicate = True

                    if not duplicate:
                        newcur.execute(SQL_INSERTS["insert_supervision"], supervision_tuple)
                        conn.commit()

                        SQL_DATA["supervision_id"] = newcur.lastrowid
                        ALL_SUPERVISIONS[sup_year].append((SQL_DATA["supervision_id"], title))

                # print("--------------------------")

        query = "UPDATE arquivos_xml t SET status_extracao = %s WHERE t.id = %s"
        newcur.execute(query, (1, SQL_DATA["arquivo_id"]))
        conn.commit()

def is_production_sequence_in(grouped_productions: Dict[int, List[Tuple[int, int, str]]],
    production_sequence: int,
    year: int) -> bool:
    prod_keys = list(grouped_productions.keys())

    if len(prod_keys) > 0 and year in prod_keys:
        for _, prod_seq, _ in grouped_productions[year]:
            if prod_seq == production_sequence:
                return True

    return False

etree_extraction()
print("[DEBUG] Finished executing extractor.py statements")

cur.close()
conn.close()