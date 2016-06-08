# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import json
import codecs

class SearchxuetangPipeline(object):
	def __init__(self):
		#self.file = codecs.open('xuetang_courses.json', 'wb', encoding='utf-8')
		#self.countfile = codecs.open('count.txt', 'wb', encoding='utf-8')
		pass
		
	def process_item(self, item, spider):
		line = json.dumps(dict(item)) + ',\n'
		self.file.write(line)
		#self.countfile.write(str(item['count']) + '\n')
		return item
		
	def open_spider(self, spider):
		#if spider.name == "searchxuetang":
		spider.file = codecs.open('xuetang_courses_tmp.json', 'wb', encoding='utf-8')
		self.file = codecs.open('xuetang_courses.json', 'wb', encoding='utf-8')
		self.file.write("[\n")
		
	def close_spider(self, spider):
		self.file.write("]")
		self.file.close()
		spider.file.close()
		#file = open('count.txt', 'wb')
		#file.write(self.count)
		#self.file.close()
		#file.close()
		
class SearchcourseraPipeline(object):
	def __init__(self):
		#self.file = codecs.open('coursera_courses.json', 'wb', encoding='utf-8')
		#self.countfile = codecs.open('count.txt', 'wb', encoding='utf-8')
		pass
		
	def process_item(self, item, spider):
		line = json.dumps(dict(item)) + ',\n'
		self.file.write(line)
		#self.countfile.write(str(item['count']) + '\n')
		return item
		
	def open_spider(self, spider):	
		#if spider.name == "searchcoursera":
		self.file = codecs.open('coursera_courses.json', 'wb', encoding='utf-8')
		self.file.write("[\n")
		
	def close_spider(self, spider):
		self.file.write("]")
		self.file.close()
		#file = open('count.txt', 'wb')
		#file.write(self.count)
		#self.file.close()
		#file.close()
		
class SearchclasscentralPipeline(object):
	def __init__(self):
		#self.file = codecs.open('coursera_courses.json', 'wb', encoding='utf-8')
		#self.countfile = codecs.open('count.txt', 'wb', encoding='utf-8')
		pass
		
	def process_item(self, item, spider):
		line = json.dumps(dict(item)) + ',\n'
		self.file.write(line)
		#self.countfile.write(str(item['count']) + '\n')
		return item
		
	def open_spider(self, spider):	
		#if spider.name == "searchcoursera":
		self.file = codecs.open('classcentral_courses.json', 'wb', encoding='utf-8')
		self.file.write("[\n")
		
	def close_spider(self, spider):
		self.file.write("]")
		self.file.close()
		#file = open('count.txt', 'wb')
		#file.write(self.count)
		#self.file.close()
		#file.close()