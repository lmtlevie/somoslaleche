from requests import get
from lxml import etree
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import io
import re
from price_parser import Price
from json import loads
from datetime import date

def create_table_bigquery(client,table_id) -> None:
    schema = [
            bigquery.SchemaField("title", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("seller", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("price", "FLOAT", mode="REQUIRED"),
            bigquery.SchemaField("category", "STRING", mode="REPEATED"),
            bigquery.SchemaField("location", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("created_at","DATE",mode="REQUIRED")
            ]

    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)
    print(
        "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    )

def add_row_bigquery(row:dict) -> None:
    print(row)
    PROJECT = "alumnos-sandbox"
    DATASET = "precios_productos"
    TABLE = "grupo_3_V2"
    client = bigquery.Client(project=PROJECT)
    table_id = f"{PROJECT}.{DATASET}.{TABLE}"
    table = None
    row[0]["created_at"]= row[0]["created_at"].strftime("%Y-%m-%d")
    try:
        table = client.get_table(table_id)
    except NotFound:
        create_table_bigquery(client,table_id)
        table = client.get_table(table_id)


    errors = client.insert_rows_json(table, row)
    if errors == []:
        print("Success")
    else:
        print(errors)


def clasificador(titulo:str) -> list:
    """"""
    categoria_final = []
    categorias = {"Polvo":r"polvo","Vegetal":r"(vegetal|almendras|planta|a base de)",
                  "Descremada":r"descremada",
                  "Entera":r"entera","Infantil":r"(bebe|infantil|bebé|Bebé)",
                  "Larga Vida":r"larga vida",
                  "Sachet":r"sachet",
                  "Saborizadas":r"(chocolatada|chocolate|CHOCOLATADA)"
                }

    for categoria,regex in categorias.items():

        match = re.search(regex,titulo,re.IGNORECASE)
        if(match):
            categoria_final.append(categoria)

    if(len(categoria_final) == 0):
        categoria_final.append("Otro")

    return categoria_final

def scrap_milks_html(data:dict,list_xpath:str,title_xpath:str,price_xpath:str,pager:dict=None) -> None:
    """"""
    res = get(data["url"])
    html_doc = io.StringIO(res.text)
    parser = etree.HTMLParser()
    tree = etree.parse(html_doc, parser)

    for p in tree.xpath(list_xpath):
        title = p.xpath(title_xpath)
        price = p.xpath(price_xpath)
        categoria = clasificador(title[0])
        product ={"title":title[0],
                 "seller":data["name"],
                 "price":float(Price.fromstring(price[0]).amount),
                 "category":categoria,
                 "location":data["location"],
                 "created_at": date.today()}
        add_row_bigquery([product])

    if pager is not None:
        for page in tree.xpath(pager["pager_xpath"]):
            page_url = page.xpath(pager["url_xpath"])
            data["url"] = page_url[0]
            if "host" in pager.keys():
                data["url"] = pager["host"] + data["url"]
            scrap_milks_html(data,list_xpath,title_xpath,price_xpath)


def scrap_milks_JS(data,page):
    res = get(data["url"])
    json_res = loads(res.text)

    if(res.status_code == 400):
        return

    for item in json_res:

        title = item["productName"]

        try:
            categoria = item["Variedad"]
        except:
            categoria = clasificador(title)

        price = item["items"][0]["sellers"][0]["commertialOffer"]["Price"]
        product ={"title":title,
                 "seller":data["name"],
                 "price":price,
                 "category":categoria,
                 "location":data["location"],
                 "created_at":date.fromisoformat(item["releaseDate"].split("T")[0])}

        add_row_bigquery([product])
        print(product)

    prox_url = f"https://www.hiperlibertad.com.ar/api/catalog_system/pub/products/search/lacteos/leches?O=OrderByTopSaleDESC&_from={page*23}&_to={(page+1)*23}&ft&sc={data['suc']}"
    data["url"] = prox_url
    scrap_milks_JS(data,page+1)


