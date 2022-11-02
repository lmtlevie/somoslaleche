from milk_scrapper import scrap_milks_html
import json
import csv

with open('fonts.json') as f:
   data = json.load(f)

with open("result.csv") as res:
   writer = csv.writer(f)


scrap_milks_html(data["Condor"],"//li[.//h2[@class='woocommerce-loop-product__title']]",".//h2/text()",".//span[@class='price']//bdi/text()",writer,{"pager_xpath":"//ul[@class='page-numbers']/li[./a[@class='page-numbers']]","url_xpath":"./a/@href"})

scrap_milks_html(data["Tu Almacen"],"//div[@class='item']","./p/text()","./div[@class='precio']/text()",writer)

scrap_milks_html(data["Alvear"],"//div[@class='product-small box ']","./div[@class='title-wrapper']//a/text()",writer)
