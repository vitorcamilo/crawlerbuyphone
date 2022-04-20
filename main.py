from dataclasses import replace
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.proxy import *
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from webdriver_manager.firefox import GeckoDriverManager
import os
import requests
import json


class webcrawl():


    def __init__(self):
        Opptions = Options()
        Opptions.headless = True
        Opptions.binary_location = os.environ.get('GECKODRIVER_BINARY')
        Opptions.add_argument("--disable-dev-shm-usage")
        Opptions.add_argument("--no-sandbox")
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options = Opptions)


    def iniciarcrawler(self):
        while True:
            sendtelegram = 'Lá vamos nós novamente.... Crawler iniciado!'
            self.telegramresponse(sendtelegram)
            iphones = self.apirequest()
            dados = iphones["data"]
            if dados :
                for dado in dados:
                    try:
                        idiphone = dado['id']
                        coriphone = dado['color']
                        # skumagalu = dado['magalu_sku']
                        casasbahiasku = dado['casasbahia_sku']
                        americanassku = dado['americanas_sku']
                        # precomagalu = self.magalu(skumagalu, coriphone)
                        if casasbahiasku == None or americanassku == None:
                            pass
                        else:
                            precoamericanas = self.americanas(americanassku)
                            precocasasbahia = self.casasbahia(casasbahiasku)
                            urlamericanas = f'''https://pedidos.buyphone.com.br/api/products/{idiphone}/americanas/{precoamericanas}'''
                            urlcasasbahia = f'''https://pedidos.buyphone.com.br/api/products/{idiphone}/casasbahia/{precocasasbahia}'''
                            self.pricereturn(urlamericanas)
                            self.pricereturn(urlcasasbahia)
                            
                        self.driver.close()

                        if idiphone == 73:
                            sendtelegram = 'Phewwww... finalmente! O Crawler terminou seu trabalho por hoje!'
                            self.telegramresponse(sendtelegram)
                            time.sleep(86400)
                            

                    except Exception as e:
                        print(e)
                        sendtelegram = 'O Crawler encontrou um problema! Hora de olhar o que está acontecendo....'
                        self.telegramresponse(sendtelegram)




    # def magalu(self, SKU, color):
    #     self.driver.get(f'''https://www.magazineluiza.com.br/busca/{SKU}''')
    #     precosmagalu = self.driver.find_elements(By.XPATH, value ="(//p[contains(@class,'sc-hKwDye dWfgMa')])[1]")
    #     for iphone in precosmagalu:
    #         if color in iphone.text:
    #             return iphone.text

    def americanas(self, SKU):
        self.driver.get(f'''https://www.americanas.com.br/busca/{SKU}''')
        americanas0=self.driver.find_element(By.XPATH, value="//span[contains(@class,'src__Text-sc-154pg0p-0 price__PromotionalPrice-sc-h6xgft-1')]")
        americanas1 = americanas0.text
        americanas2 = americanas1.replace("R$","")
        americanas3 = americanas2.replace(",","")
        americanasfinal = americanas3.replace(".","")
        #print(magalufinalprice)
        return americanasfinal

    def casasbahia(self, SKU):
        self.driver.get(f'''https://www.casasbahia.com.br/{SKU}/b''')
        cb0 = self.driver.find_element(By.XPATH, value="//span[@class='ProductPrice__PriceValue-sc-1tzw2we-6 kBYiGY']")
        cb1 = cb0.text
        cb2 = cb1.replace("R$","")
        cb3 = cb2.replace(",","")
        cbfinalprice = cb3.replace(".","")
        #print(cbfinalprice)
        return cbfinalprice


    def apirequest(self):
        url = "https://pedidos.buyphone.com.br/api/products"
        headers = {
        'token': 'ef7223f0-55b4-49a7-9eed-f4b4ef14b2f1'
        }
        response = requests.get(url, headers=headers)
        return json.loads(response.content)

    def pricereturn(self,url):
        headers = {
        'token': 'ef7223f0-55b4-49a7-9eed-f4b4ef14b2f1'
        }
        requests.post(url, headers=headers)

    def telegramresponse(self, text):
        url = f'''https://api.telegram.org/bot5098238913:AAHvT080O9ifLyIdB5ICE_MoE16nsAcEoNE/sendMessage?chat_id=-574442548&text={text}'''
        requests.get(url)

crawl = webcrawl()
crawl.iniciarcrawler()