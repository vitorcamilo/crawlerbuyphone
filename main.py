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
import schedule
import random


class webcrawl():

    def __init__(self):
        self.Opptions = Options()
        self.Opptions.headless = True
        self.Opptions.binary_location = os.environ.get('FIREFOX_BIN')
        self.Opptions.add_argument("--disable-dev-shm-usage")
        self.Opptions.add_argument("--no-sandbox")
        self.driver = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options = self.Opptions)

  
    def iniciarcrawler(self):
        sendtelegram = 'Lá vamos nós novamente.... Crawler iniciado!'
        self.telegramresponse(sendtelegram)
        iphones = self.apirequest()
        dados = iphones["data"]
        if dados :
            for dado in dados:
                try:
                    #nameiphone = dado['name']
                    #memoryiphone = dado['memory']
                    #coriphone = dado['color']
                    # skumagalu = dado['magalu_sku']
                    # casasbahiasku = dado['casasbahia_sku']
                    # americanassku = dado['americanas_sku']
                    # ptofriosku = dado['ponto_sku']
                    idiphone = dado['id']
                    googleSKU = dado['google_sku']
                    

                    if googleSKU == None:
                        precoamericanas = 0
                        precocasasbahia = 0
                        precomagalu = 0
                        precopontofrio = 0
                    else:
                        self.driver.get(f'''https://www.google.com/shopping/product/{googleSKU}/''')
                        precomagalu = '0'
                        precoamericanas = '0'
                        precocasasbahia = '0'
                        precopontofrio = '0'
                        lojas = self.driver.find_elements(By.XPATH, value= "(//th[text()='Vendido por']/following::a[@class='b5ycib shntl'])")
                        precos = self.driver.find_elements(By.XPATH, value="//a[@class='sh-osd__sort']/following::div[@class='drzWO']")
                        for l, p in zip(lojas, precos):
                            if l.text == "Magazine Luiza" :
                                precomagalu = p.text.replace("R$","").replace(",","").replace(".","").replace(" ","")
                            elif l.text == "Pontofrio.com":
                                precopontofrio = p.text.replace("R$","").replace(",","").replace(".","").replace(" ","")
                            elif l.text == "Americanas.com":
                                precoamericanas = p.text.replace("R$","").replace(",","").replace(".","").replace(" ","")
                            elif l.text == "Casas Bahia":
                                precocasasbahia = p.text.replace("R$","").replace(",","").replace(".","").replace(" ","")
                            
                    
                    urlamericanas = f'''https://pedidos.buyphone.com.br/api/products/{idiphone}/americanas/{precoamericanas}'''
                    urlcasasbahia = f'''https://pedidos.buyphone.com.br/api/products/{idiphone}/casasbahia/{precocasasbahia}'''
                    urlpontofrio = f'''https://pedidos.buyphone.com.br/api/products/{idiphone}/ponto/{precopontofrio}'''
                    urlmagalu = f'''https://pedidos.buyphone.com.br/api/products/{idiphone}/magalu/{precomagalu}'''
                    self.pricereturn(urlamericanas)
                    self.pricereturn(urlcasasbahia)
                    self.pricereturn(urlpontofrio)
                    self.pricereturn(urlmagalu)
                    
                    if idiphone == 87:
                        sendtelegram = 'Pheeew.... O crawler terminou por hoje!.'
                        self.telegramresponse(sendtelegram)


                except Exception as e:
                    print(e)
                    sendtelegram = 'O Crawler encontrou um problema! Hora de olhar o que está acontecendo....'
                    self.telegramresponse(sendtelegram)


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
    

if __name__ == "__main__":
    crawl= webcrawl()
    schedule.every().day.at("01:27").do(crawl.iniciarcrawler)
    while True:
        schedule.run_pending()
        time.sleep(1)
