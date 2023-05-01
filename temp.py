import xmltodict

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