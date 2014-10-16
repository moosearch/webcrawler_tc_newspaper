from scrapy.spider import Spider
from scrapy.selector import Selector
from tcpaper.items import TCArticleItem
import re

class TCSpider(Spider):
	name = "tc"
	allowed_domains = ["http://www.timescolonist.com/"]
	start_urls = [
		#"http://www.timescolonist.com/news",
		#"http://www.timescolonist.com/business",
		#"http://www.timescolonist.com/entertainment"
		"http://www.timescolonist.com/news/local/victoria-police-seek-witnesses-in-corvette-taxi-crash-1.1427291"
	]

	def date(self, response):
		"""
		Processes the date field for TCArticleItem
		
		arguments:
		response: a response object from Scrapy.Response
		"""
		x = response.xpath("//div[@class='wrapper appendbottom-10']/div/p/text()")[-1].re('(\w+)')
		return x

	def body(self, response):
		"""
		This method will process the body field for a TCArticleItem. It will
		strip the characters"\r\n\t" from the beginning of each string from the 
		list extracted from the xpath expression and return that list.

		arguments:
		response: a response object from Scrapy.Response
		"""	
		x = response.xpath("//div[@class='story-content row-fluid']/p/text()").extract()

		for i in range(0,len(x)):
			x[i] = x[i].strip("\r\n\t")
		return x		

	def parse(self, response):
		"""
		Parses HTML for a TC news article for its name, url, date, description,
		article body, and any tags used
		"""
		tc = TCArticleItem()
		tc['name'] = response.xpath("//meta[@name='title']/@content").extract()
		tc['url'] = response.url
		tc['date'] = self.date(response)
		tc['description'] = response.xpath("//meta[@name='description']/@content").extract()
		tc['body'] = self.body(response)		
		tc['tags'] = response.xpath("//meta[@name='keywords'][2]/@content").re('(\w+)')
		return tc
	'''	
    name = scrapy.Field()
    url = scrapy.Field()
    date = scrapy.Field()
    description = scrapy.Field()
    body = scrapy.Field()
    tags = scrapy.Field()		
'''
