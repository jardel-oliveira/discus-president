import requests
from bs4 import BeautifulSoup as bs

# pegar paginação


def paginas_discuros(pagina):
    pagina_html = requests.get(pagina)
    # análise sintática
    pagina_parser = bs(pagina_html.content, "html.parser")
    # mapeando a última página e o avanço de página para incremento
    ultima_pagina = pagina_parser.find_all("a", {"class", "pagina"})
    for l in ultima_pagina:
        x = int(l.get("href").split("=")[-1])

    avanco_pagina = pagina_parser.find_all("a", {"class", "proximo"})
    for l in avanco_pagina:
        y = int(l.get("href").split("=")[-1])

    # criando uma lista com todas as urls de páginas
    lista_paginacao_discuros = []
    for i in range(x, -1, -y):
        lista_paginacao_discuros.append(
            "https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/discursos?b_start:int={}".format(
                i
            )
        )

    return lista_paginacao_discuros


# pegar todas as urls de discursos


def url_discursos(url):

    lista_url_discursos = []
    for i in url:
        pagina = requests.get(i)

        # validação conexão
        if pagina.status_code == 200:
            print("Conexão bem sucedida", i)
        else:
            print(pagina.status_code)

        # análise sintática
        pagina_parser = bs(pagina.content, "html.parser")
        listas_discuros_html = pagina_parser.find_all("a", {"class", "summary url"})

        # percorrendo as urls de paginação
        for l in listas_discuros_html:
            lista_url_discursos.append(l.get("href"))

    return lista_url_discursos


# pegar os textos dos discuros


def texto_discursos(url):
    discursos = []
    for t in url:
        pagina = requests.get(t)

        # análise sintática
        pagina_parser = bs(pagina.content, "html.parser")
        texto = pagina_parser.find_all("p", {"style": "text-align: justify; "})

        # percorrendo as urls para pegar o discurso
        for t2 in texto:
            discursos.append(t2.text)

    return discursos


# criando um database csv


def discursos_database(url):
    database = []
    for t in url:
        pagina = requests.get(t)

        # análise sintática
        pagina_parser = bs(pagina.content, "html.parser")
        texto = pagina_parser.find_all("p", {"style": "text-align: justify; "})
        publicacao = pagina_parser.find_all("span", {"class": "value"})

        # percorrendo as urls para pegar o discurso
        for p in publicacao:
            for t2 in texto:
                database.append(p.text + " | " + t + " | " + t2.text)

    return database


# salvando um arquivo txt


def salva_discurso(discursos):
    # removendo valores None da lista e criando arquivo
    with open("discursos_presidente.txt", "w", encoding="utf-8") as f:
        for discurso in discursos:
            if discurso != None:
                f.write("%s\n" % discurso)


url = "https://www.gov.br/planalto/pt-br/acompanhe-o-planalto/discursos"
ll = paginas_discuros(url)
uu = url_discursos(ll)
dd = discursos_database(uu)
salva_discurso(dd)
