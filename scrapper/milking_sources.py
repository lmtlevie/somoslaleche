from milk_scrapper import scrap_milks_html,scrap_milks_JS
import json
import csv

with open('./sources.json') as f:
   data = json.load(f)


   scrap_milks_html(data["condor"],"//li[.//h2[@class='woocommerce-loop-product__title']]",".//h2/text()",".//span[@class='price']//bdi/text()",{"pager_xpath":"//ul[@class='page-numbers']/li[./a[@class='page-numbers']]","url_xpath":"./a/@href"})

   scrap_milks_html(data["tu_almacen"],"//div[@class='item']","./p/text()","./div[@class='precio']/text()")

   scrap_milks_html(data["alvear"],"//div[@class='product-small box ']",".//div[@class='title-wrapper']//a/text()",".//span[@class='price']/del/span/text()")

   scrap_milks_html(data["la_proveduria"],"//div[@class='item']",".//h3/text()",".//div[@class='price']/text()",{"pager_xpath":"//div[@class='btn-group']","url_xpath":".//a/@href","host":"https://www.laproveeduria.ar"})

   for item,page_data in data["libertad"].items():

      scrap_milks_JS(page_data,1)
