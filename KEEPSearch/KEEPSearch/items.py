# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KeepsearchItem(scrapy.Item):
	cover_url = scrapy.Field()
	commitment = scrapy.Field()
	title = scrapy.Field()
	end_date = scrapy.Field()
	duration = scrapy.Field()
	price = scrapy.Field()
	description = scrapy.Field()
	course_url = scrapy.Field()
	instructors = scrapy.Field()
	start_date = scrapy.Field()
	institution_name = scrapy.Field()
	topic_name = scrapy.Field()
	subject_name = scrapy.Field()
	provider_name = scrapy.Field()
	language_name = scrapy.Field()
	#count = scrapy.Field()