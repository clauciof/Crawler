import bs4
import requests
import pandas as pd
import csv
import threading
import pymysql
import sqlalchemy

class Crawler:
    
    def start(self, links):
        #cria dataframe para os dados adquiridos
        COLUNAS = ['Produto', 'Preco', 'Site', 'Link']
        dataframe = pd.DataFrame(columns=COLUNAS)
        dataframe.to_csv('dados.csv', index=False)
        self.df = dataframe
        for link in links:
            try:
                res = requests.get(link ,timeout=2, headers={'User-Agent': 'Mozilla/5.0'})
                res.encoding = 'utf8'
                html = res.text
                self.read_html(html,link)
            except Exception as exc:
                print('Erro no request no link ', link)

    def read_html(self,html,link):
        try:
            soup = bs4.BeautifulSoup(html, 'html.parser')
        except Exception as exc:
            print('Erro ao ler arquivo')

        if "mercadolivre" in link:
            titulo = soup.select('.item-title__primary')
            titulo_pdp = soup.select('.ui-pdp-title')
            preco_inteiro = soup.select('.price-tag-fraction')
            preco_decimal = soup.find_all('span', class_='price-tag-cents')

            if titulo == [] and titulo_pdp != []:  #ifs que tratam alguns casos de erro 
                titulo = titulo_pdp

            if preco_inteiro==[]:
                preco_inteiro = '0'
                preco = preco_inteiro+'.'+'00'
                titulo = titulo[0].getText().replace('\n\t\t', '')
                self.df = self.df.append({'Produto':titulo,'Preco':float(preco), 'Site':'Mercado Livre', 'Link':link}, ignore_index=True)
                return

            preco_inteiro = preco_inteiro[0].getText()
            preco_inteiro = preco_inteiro.replace('.', '')

            if preco_decimal==[]:
                preco_decimal = '00'
                preco = preco_inteiro+'.'+preco_decimal
                titulo = titulo[0].getText().replace('\n\t\t', '')
                self.df = self.df.append({'Produto':titulo,'Preco':float(preco), 'Site':'Mercado Livre','Link':link}, ignore_index=True)
                return

            if preco_decimal[0].getText() == '':
                preco_decimal = '00'
                preco = preco_inteiro+'.'+preco_decimal
                titulo = titulo[0].getText().replace('\n\t\t', '')
                self.df = self.df.append({'Produto':titulo,'Preco':float(preco), 'Site':'Mercado Livre','Link':link}, ignore_index=True)
                return
                
            #salvando os dados capturados em um dataframe e salvando um arquivo .csv
            preco = preco_inteiro+'.'+preco_decimal[0].getText()
            titulo = titulo[0].getText().replace('\n\t\t', '')
            self.df = self.df.append({'Produto':titulo,'Preco':float(preco), 'Site':'Mercado Livre','Link':link}, ignore_index=True)
            return
            
        if "magazineluiza" in link:
            titulo = soup.select('.header-product__title')
            preco = soup.select('.price-template__text')
            titulo_indisponivel = soup.select('.header-product__title--unavailable')
            
            #ifs que tratam alguns casos de erro #
            if titulo == []:
                return
                
            if titulo_indisponivel != []:
                titulo = titulo_indisponivel
                preco = '0.0'
                titulo = titulo[0].getText().rstrip()
                self.df = self.df.append({'Produto':titulo,'Preco':float(preco), 'Site':'Magazine Luiza','Link':link}, ignore_index=True)
                return

            #salvando os dados capturados em um dataframe e salvando um arquivo .csv
            titulo = titulo[0].getText().rstrip()
            preco =  preco[0].getText().rstrip().replace('.','')
            preco = preco.replace(',','.')
            #print(titulo, preco)
            self.df = self.df.append({'Produto':titulo,'Preco':float(preco), 'Site':'Magazine Luiza','Link':link}, ignore_index=True)
            return

        if "casasbahia" in link:
            titulo = soup.find_all(class_='fn name')
            preco = soup.find_all(class_='sale price')
            titulo = titulo[0].getText().rstrip()
            preco =  preco[0].getText().rstrip().replace('.','')
            preco = preco.replace(',','.')
            self.df = self.df.append({'Produto':titulo,'Preco':float(preco), 'Site':'Casas Bahia','Link':link}, ignore_index=True)
            return
            
    def insert_db(self):
        try:    
            engine = sqlalchemy.create_engine('mysql+pymysql://root:@localhost/etl')
            self.df.to_sql('dados', con = engine, if_exists='replace', index=False)
        except Exception as exc:
                print('Erro ao salvar no banco')        
        return

        
if __name__ == "__main__":
     #le data frame
    links = pd.read_csv('offers.csv', names=['Link'])
    links = links['Link'].values.tolist()

    crawler = Crawler()
    t1 = threading.Thread(target=crawler.start, args=(links[0:10000],)) 
    t2 = threading.Thread(target=crawler.start, args=(links[10000:20000],)) 
    t3 = threading.Thread(target=crawler.start, args=(links[20000:30000],)) 
    t4 = threading.Thread(target=crawler.start, args=(links[30000:40000],)) 
   
    t1.start() 
    t2.start()
    t3.start()
    t4.start() 

    t1.join()
    t2.join()
    t3.join()
    t4.join()

    crawler.df.to_csv('dados.csv', index=False)
    crawler.insert_db()

    print("Scrapy feito!")
