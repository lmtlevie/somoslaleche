import requests
from lxml import etree
import io


url = f"https://superelcondor.com.ar/categoria-producto/lacteos/leches"





def get_values(url, first_page=None):
    res = requests.get(url)
    html_doc = io.StringIO(res.text)
    parser = etree.HTMLParser()
    tree = etree.parse(html_doc, parser)
    for p in tree.xpath("//li[.//h2[@class='woocommerce-loop-product__title']]"):
        title = p.xpath(".//h2/text()")
        price = p.xpath(".//span[@class='price']//bdi/text()")
        print(f"{title}  {price}")

    if first_page is True:
        for page in tree.xpath("//ul[@class='page-numbers']/li"):
            url = page.xpath("./a/@href")
            print(url)

    # tirar los valores a la base y devolver las url del paginado

get_values(url,True)

