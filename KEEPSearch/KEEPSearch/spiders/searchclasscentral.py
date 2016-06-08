import scrapy
import json
import re
from KEEPSearch.items import KeepsearchItem

class SearchclasscentralSpider(scrapy.Spider):
	name = "searchclasscentral"
	allowed_domain = ["class-central.com"]
	start_urls = {
		"https://www.class-central.com/subjects"
	}
	
	def parse(self, response):
		subject_set = response.xpath("//div[@class='subjects']/ \
					div[@class='row border-wrap']/ \
					div[@class='single-category col-xs-6 col-md-4']")
		for subject in subject_set:
			url = response.urljoin(subject.xpath("div[@class='category-header']/ \
					a/@href").extract()[0])
			name = subject.xpath("div[@class='category-header']/a/span/text()").extract()[0]
			yield scrapy.Request(url, callback=parse_list)
			print url
			print name
			print "\n"
	
	def parse_list(self, response):
		