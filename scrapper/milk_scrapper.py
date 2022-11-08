import requests
from lxml import etree
from google.cloud import bigquery
from google.cloud.exceptions import NotFound
import io
import re

def create_table_bigquery(client,table_id) -> None:
    schema = [
            bigquery.SchemaField("title", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("seller", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("price", "INTEGER", mode="REQUIRED"),
            bigquery.SchemaField("category", "STRING", mode="REQUIRED"),
            bigquery.SchemaField("location", "STRING", mode="REQUIRED"),
            ]

    table = bigquery.Table(table_id, schema=schema)
    table = client.create_table(table)
    print(
        "Created table {}.{}.{}".format(table.project, table.dataset_id, table.table_id)
    )

def add_row_bigquery(row:dict) -> None:
    PROJECT = "alumnos-sandbox"
    DATASET = "precios_productos"
    TABLE = "grupo_3"
    client = bigquery.Client(project=PROJECT)
    table_id = f"{PROJECT}.{DATASET}.{TABLE}"
    table = None
    try:
        table = client.get_table(table_id)
    except NotFound:
        create_table_bigquery(client,table_id)
        table = client.get_table(table_id)


    errors = client.insert_rows_json(table, row)
    if errors == []:
        print("Success")


def clasificador(titulo:str) -> list:
    """"""
    categoria_final = []
    titulo = titulo[0]
    categorias = {"Polvo":      r"polvo","Vegetal":r"(vegetal|almendras|planta|a base de)",
                  "Descremada": r"descremada",
                  "Entera":     r"entera","Infantil":r"(bebe|infantil|bebé)",
                  "Larga Vida": r"larga vida",
                  "Sachet":     r"sachet",
                  "Saborizadas":r"(chocolatada|chocolate)"
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
    res = requests.get(data["url"])
    html_doc = io.StringIO(res.text)
    parser = etree.HTMLParser()
    tree = etree.parse(html_doc, parser)

    for p in tree.xpath(list_xpath):
        title = p.xpath(title_xpath)
        price = p.xpath(price_xpath)
        categoria = clasificador(title)
        add_row_bigquery({"title":      title[0],"brand":"",
                          "seller":     data["name"],
                          "price":      int(float(price[0].replace("$","").replace(",",""))),
                          "category":   categoria[0],
                          "location":   data["location"]})

    if pager is not None:
        for page in tree.xpath(pager["pager_xpath"]):
            page_url = page.xpath(pager["url_xpath"])
            data["url"] = page_url[0]
            scrap_milks_html(data,list_xpath,title_xpath,price_xpath,writer)


