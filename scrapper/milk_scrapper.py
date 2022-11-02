import requests
from lxml import etree
import io
import re;


def clasificador(leche):
    categoria = [];
    leche = leche[0];
    if(re.match(r"polvo",leche,re.IGNORECASE)):
        categoria.append("Polvo")
    if(re.match(r"(vegetal|almendras|planta|a base de)",leche,re.IGNORECASE)):
        categoria.append("Vegetal")
    if(re.match(r"descremada",leche,re.IGNORECASE)):
        categoria.append("Descremada")
    if(re.match(r"entera",leche,re.IGNORECASE)):
        categoria.append("Entera")
    if(re.match(r"(bebe|infantil|bebé)",leche,re.IGNORECASE)):
        categoria.append("Infantil")
    if(re.match(r"larga vida",leche,re.IGNORECASE)):
        categoria.append("Larga Vida")
    if(re.match(r"sachet",leche,re.IGNORECASE)):
        categoria.append("Sachet")
    if(re.match(r"(chocolatada|chocolate)",leche,re.IGNORECASE)):
        categoria.append("Saborizadas")
    if(len(categoria) == 0):
        categoria.append("Otro")
    return categoria

def scrap_milks_html(data,list_xpath,title_xpath,price_xpath,writer,pager=None):
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

    # tirar los valores a la base

