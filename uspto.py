# -*- coding: utf-8 -*-
"""
Created on Sun Jun 14 12:19:57 2020

@author: cartola
"""


import scrapy

class UsptoSpider(scrapy.Spider):
    name = 'uspto_spider'
    medicamento = input("Digite um medicamento para busca: ")
    
    start_urls = ['http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&p=1&f=S&l=50&Query=%28%28ttl%2F' + medicamento + '+or+abst%2F' + medicamento + '%29%29&d=PTXT']
    
    def parse(self, response):
        links = response.xpath(
            '//tr/td[@valign="top"][last()]/a/@href').getall()
        for link in links:
            yield scrapy.Request(
                response.urljoin(link),
                callback=self.parse_link
            )
        pages_url = response.xpath('//img[@src="/netaicon/PTO/nextlist.gif"]/parent::a/@href').get()
        yield scrapy.Request(
                response.urljoin(pages_url),
                callback=self.parse
            )            
        print("Teste paginação >>>>>> " + pages_url)
            
        
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
        claim = response.xpath('//center [contains (b, "Claims")]//text()').get()
        yield {
            'number': number,
            'date': date,
            'title': title,
            'abstract': abstract,
            'claim': claim
        }