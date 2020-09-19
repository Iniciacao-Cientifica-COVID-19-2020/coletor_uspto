# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 12:19:57 2020

@author: cartola
"""


import scrapy
import re

class UsptoSpider(scrapy.Spider):
    name = 'uspto_spider'
    medicamento = input("Digite um medicamento para busca: ")
    
    start_urls = ['http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&p=1&f=S&l=50&Query=%28%28ttl%2F' + medicamento + '+or+abst%2F' + medicamento + '%29%29&d=PTXT']
    
    def parse(self, response):   # Função para parsear os links
        links = response.xpath(
            '//tr/td[@valign="top"][last()]/a/@href').getall()
        for link in links:
            yield scrapy.Request(
                response.urljoin(link),   # urljoin serve para driblar as urls relativas
                callback=self.parse_link
            )
        pages_url = response.xpath('//img[@src="/netaicon/PTO/nextlist.gif"]/parent::a/@href').get()   # Linhas de paginação
        yield scrapy.Request(
                response.urljoin(pages_url),
                callback=self.parse
            )            
        #print("Teste paginação >>>>>> " + pages_url)
            
        
    def parse_link(self, response):
        number = response.xpath('//title/text()').re(r'United States Patent:\s*(.*)')[0]
        date = response.xpath('//table/tr[contains (th, "Filed:")]/td/b/text()').getall()[0]
        title = response.xpath('//font//text()').getall()
        title.pop(0)
        title.pop(0)
        title.pop(0)
        title.pop(0)
        stringA = ''
        for item in title:
            stringA += item
        stringA = " ".join(stringA.split())
        stringA = stringA.replace("**Please see images for: ( Certificate of Correction ) ** ", "")
        stringA = stringA.replace("**Please see images for: ( Certificate of Correction ) ( PTAB Trial Certificate ) ** ", "")        
        title = stringA
        #print("Teste título >>>>> "+ title)
        abstract = ' '.join(response.xpath('//p[1]//text()').getall())
        abstract = " ".join(abstract.split())
        #print("Resumo >>>>> " + abstract)
        #claim = response.xpath('//center [contains (b, "Claims")]//text()').get()
        #stringB = ''
        claim = response.text
        print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        claimFiltrado = re.findall('<CENTER><b><i>Claims</b></i></CENTER>(.*?)<CENTER><b><i>Description</b></i></CENTER>', claim, re.DOTALL)[0]
        claimFiltrado2 = re.findall('[\d].+', claimFiltrado, re.DOTALL)[0]
        claimFiltrado3 = claimFiltrado2.replace("<BR><BR>", "")
        #stringB = ''
        #for itemB in claimFiltrado:
         #   stringB += itemB
        #claim = stringB
        #claim = claim.replace(" <HR> <BR><BR>What is claimed is: <BR><BR>", "")
        #claim = claim.replace(" <HR> ", "")
        #for item in claim:
         #   stringB
        #textPreClaim = response.xpath('//body').getall()
        #claim = textPreClaim.split('<br><br>The invention claimed is: <br><br> ')[1].split(' <hr> <center><b><i>Description</i></b></center> <hr>')[0]
        #print("textPreClaim >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        
        #claim = textPreClaim.partition("<br><br>The invention claimed is: <br><br> ")[43].partition(" <hr> <center><b><i>Description</i></b></center> <hr>")[0]
        #print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
        #claim = re.search(r"(?<=<br><br>The invention claimed is: <br><br> ).*?(?= <hr> <center><b><i>Description</i></b></center> <hr>)", textPreClaim)
        #claim = response.xpath('substring-before(substring-after(//coma, "<hr> <br><br>The invention claimed is: <br><br>"), "<hr> <center><b><i>Description</i></b></center> <hr>")').extract()
        #tudo = response.xpath('//body//text()').getall()
        yield {
            'number': number,
            'date': date,
            'title': title,
            'abstract': abstract,
            'claim': claimFiltrado3,
            #'tudo': tudo
        }