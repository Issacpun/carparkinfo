import scrapy
import logging
import urllib
import zlib
import os
import time
from scrapy.selector import Selector
from scrapy.spider import Spider  
from scrapy.contrib.spiders import CrawlSpider
from scrapy.contrib.linkextractors import LinkExtractor
from bs4 import BeautifulSoup
from scrapy.crawler import CrawlerProcess

class dsatCamSpider(scrapy.Spider):
    name = "carpark"
    #url =   ['http://m.dsat.gov.mo/cam.aspx']
    #allowed_domains = ['http://m.dsat.gov.mo/cam.aspx']
    #start_urls = ['http://m.dsat.gov.mo/cam.aspx']
    
    

    def start_requests(self):
        urls = ['http://m.dsat.gov.mo/carpark.aspx?data=dsat']
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)


    def parse(self, response):  
        #content =response.xpath("//div[@id='carpark_data']//tr").extract()
        content=response.body

        soup = BeautifulSoup(content,'html5lib')

        #content=soup.find_all('div',id='carpark_data')
        content=soup.find_all('tr')


        #text=content
        text=[]

        

        for i in content:
        	text.append(i.text.replace('\n','').replace('\t',''))
        	print(i.text)
        	print('-------------------------------')
        #print(text)

        target=[]
        for i in text:
        	if '宋玉生廣場' in i:
        		target=i.split(' ')
        target=list(filter(lambda x:x != '',target))
        print(target)


        #info=content[0].toStrint().split('div')

       # print(""+content[0])

        if len(text) < 1:
            self.log('=====================extract info. error===========================')
            return
        document = 'C:\\Users\\Issac\\Desktop\\parking'
        exists = os.path.exists(document)
        if not exists:
            self.log('create document: ')
            os.makedirs(document)
    	#命名
        name = 'carpark'
    	# 图片保存到本地
        fp = open(document+"\\"+name+'.txt','wb')
        print("================================save===================================")
        fp.seek(0,0)
        

        for i in text:
        	if '宋玉生廣場' in i:
        		target=i.split(' ')
        		fp.write(i.encode("UTF-8"))
        fp.close
    '''
        fp = open(name, "wb")
        fp.write(text)
        fp.close
    '''
    '''    
    def save_img(self, text):
    	print('==============================print====================================')
        #保存的文件夹
    	document = 'C:\\Users\\Issac\\Desktop\\parking'
        
        # 文件命名
    	path=document
    	exists = os.path.exists(path)
    	if not exists:
    		self.log('create document: ')
    		os.makedirs(path)

        #命名
    	pic_name = 'car park'+'.html'
	

        
    	try:
    		url = "http://m.dsat.gov.mo/carpark.aspx?data=dsat"
    		user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    		headers = { 'User-Agent' : user_agent }

    		req = urllib.request.Request(url, headers=headers)
    		response = urllib.request.urlopen(req, timeout=30)
    		
    		
            # 请求返回到的数据
    		data = response.read()

            # 若返回数据为压缩数据需要先进行解压
    		if response.info().get('Content-Encoding') == 'gzip':
        		data = zlib.decompress(data, 16 + zlib.MAX_WBITS)
            

            # 图片保存到本地
    		fp = open(pic_name, "wb")
    		fp.write(data)
    		fp.close

    		self.log('save image finished:' + pic_name)
    	except Exception as e:
    		self.log('save image error.')
    		self.log(e)
    '''
       