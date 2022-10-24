import requests
from lxml import etree
import io


def scrap_milks_html(data,list_xpath,title_xpath,price_xpath,pager=None):
    res = requests.get(data["url"])
    html_doc = io.StringIO(res.text)
    parser = etree.HTMLParser()
    tree = etree.parse(html_doc, parser)
    for p in tree.xpath(list_xpath):
        title = p.xpath(title_xpath)
        price = p.xpath(price_xpath)
        #categoria = clasificador(p)
        #subir_data()

    if pager is not None:
        for page in tree.xpath(pager["pager_xpath"]):
            page_url = page.xpath(pager["url_xpath"])
            scrap_milks_html({"url":page_url[0]},list_xpath,title_xpath,price_xpath)

    # tirar los valores a la base

