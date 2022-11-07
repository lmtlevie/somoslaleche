import requests
from lxml import etree
import io
import re


def clasificador(titulo:str) -> list:
    categoria_final = []
    titulo = titulo[0]
    categorias = {"Polvo":r"polvo","Vegetal":r"(vegetal|almendras|planta|a base de)",
                  "Descremada":r"descremada",
                  "Entera":r"entera","Infantil":r"(bebe|infantil|bebé)",
                  "Larga Vida":r"larga vida",
                  "Sachet":r"sachet",
                  "Saborizadas":r"(chocolatada|chocolate)"
                }

    for categoria,regex in categorias.items():
        match = re.search(regex,titulo,re.IGNORECASE)
        if(match):
            categoria_final.append(categoria)

    if(len(categoria_final) == 0):
        categoria_final.append("Otro")

    return categoria_final

def scrap_milks_html(data:dict,list_xpath:str,title_xpath:str,price_xpath:str,writer,pager:dict=None) -> None:
    res = requests.get(data["url"])
    html_doc = io.StringIO(res.text)
    parser = etree.HTMLParser()
    tree = etree.parse(html_doc, parser)

    for p in tree.xpath(list_xpath):
        title = p.xpath(title_xpath)
        price = p.xpath(price_xpath)
        categoria = clasificador(title)
        writer.writerow([title[0],"",data["name"],int(float(price[0].replace("$","").replace(",",""))),categoria[0]])

    if pager is not None:
        for page in tree.xpath(pager["pager_xpath"]):
            page_url = page.xpath(pager["url_xpath"])
            scrap_milks_html({"url":page_url[0],"name":data["name"]},list_xpath,title_xpath,price_xpath,writer)


