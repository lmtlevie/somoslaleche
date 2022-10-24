from milk_scrapper import scrap_milks_html
import json

with open('fonts.json') as f:
   data = json.load(f)

scrap_milks_html(data["Condor"],"//li[.//h2[@class='woocommerce-loop-product__title']]",".//h2/text()",".//span[@class='price']//bdi/text()",{"pager_xpath":"//ul[@class='page-numbers']/li[./a[@class='page-numbers']]","url_xpath":"./a/@href"})

scrap_milks_html(data["Tu Almacen"],"//div[@class='item']","./p/text()","./div[@class='precio']/text()")

scrap_milks_html(data["Alvear"],"//div[@class='product-small box ']","./div[@class='title-wrapper']//a/text()")
