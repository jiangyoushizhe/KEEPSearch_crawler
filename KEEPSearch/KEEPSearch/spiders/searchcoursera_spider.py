import scrapy
import json
import datetime
import codecs

from KEEPSearch.items import KeepsearchItem

class SearchcourseraSpider(scrapy.Spider):
	name = "searchcoursera"
	allowed_domains = ["coursera.org"]
	start_urls = [
		"https://api.coursera.org/api/courses.v1?limit=100&fields=photoUrl,description,startDate,previewLink,instructorIds,partnerIds,workload,primaryLanguages,subtitleLanguages,workload,domainTypes&start=0"
	]
	ins_q = "?field=prefixName,firstName,middleName,lastName,suffixName,title"
	ins_head = "https://api.coursera.org/api/instructors.v1/"
	par_head = "https://api.coursera.org/api/partners.v1/"
	
	def parse(self, response):
		jsonstr = response.text
		#file = codecs.open('test.txt', 'wb', encoding='utf-8')
		#file.write(jsonstr)
		#file.close()
		#dict = {}
		dict = json.loads(jsonstr)
		for course in dict['elements']:
		#courses = []
		#for course in courses:
			item = KeepsearchItem()
			
			title = course.get('name')
			if title != None:
				item['title'] = title
			else:
				item['title'] = ''
			
			img = course.get('photoUrl')
			if img != None:
				item['cover_url'] = img
			else:
				item['cover_url'] = ''
				
			desc = course.get('description')
			if desc != None:
				item['description'] = desc
			else:
				item['description'] = ''
				
			cate = course.get('domainTypes')
			if cate != None and cate:
				item['subject_name'] = [cate[0]['domainId']]
				item['topic_name'] = [cate[0]['subdomainId']]
			else:
				item['subject_name'] = []
				item['topic_name'] = []
				
			#url = course.get('previewLink')
			#if url != None:
			#	item['course_url'] = url
			#else:
			#	item['course_url'] = ''
			slug = course.get('slug')
			if slug != None:
				if course['courseType'] == "v1.session":
					url = "https://zh.coursera.org/course/" + slug
				else:
					url = "https://zh.coursera.org/learn/" + slug
			else:
				url = ''
			item['course_url'] = url
				
			start = course.get('startDate')
			if start != None:
				#item['start_time'] = (datetime.datetime.fromtimestamp(start)).strftime("%Y-%m-%d %H:%M:%S")
				item['start_date'] = start
			else:
				item['start_date'] = ''
				
			item['end_date'] = ''
			
			workload = course.get('workload')
			if workload:
				item['commitment'] = workload
			else:
				item['commitment'] = ""
			
			lang = course.get('primaryLanguages')
			item['language_name'] = lang
			
			item['provider_name'] = "coursera"
			
			ins_set = course.get('instructorIds')
			if ins_set != None and ins_set:
				item['instructors'] = []
				request = scrapy.Request(self.ins_head + ins_set[0] + self.ins_q, callback=self.parse_ins, dont_filter=True)
				request.meta['item'] = item
				request.meta['course'] = course
				request.meta['i'] = 0
				request.meta['ins_set'] = ins_set
				yield request
			else:
				item['instructors'] = []
				par_set = course.get('partnerIds')
				if par_set != None and par_set:
					item['institution_name'] = []
					request = scrapy.Request(self.par_head + par_set[0], callback=self.parse_par, dont_filter=True)
					request.meta['item'] = item
					request.meta['i'] = 0
					request.meta['par_set'] = par_set
					yield request
				else:
					item['institution_name'] = []
					if not item['instructors']:
						item['instructors'] = ''
					else:
						string = ''
						flag = False
						for e in item['instructors']:
							if flag == False:
								string += e
							else:
								string += ', ' + e
							flag = True
						item['instructors'] = string
					yield item
					
		next = dict['paging'].get('next')
		if next == None:
			print response.url
			return
		else:
			yield scrapy.Request("https://api.coursera.org/api/courses.v1?limit=100&fields=photoUrl,description,startDate,previewLink,categories,instructorIds,partnerIds&start=" + next, callback=self.parse)
					
	def parse_ins(self, response):
		item = response.meta['item']
		course = response.meta['course']
		i = response.meta['i']
		ins_set = response.meta['ins_set']
		jsonstr = response.text
		dict = json.loads(jsonstr)
		
		for ins in dict['elements']:
			name = ins['fullName']
			if name == '':
				name = ins['id']
			item['instructors'].append(name)
		
		i += 1
		if i <= len(ins_set) - 1:
			request = scrapy.Request(self.ins_head + ins_set[i] + self.ins_q, callback=self.parse_ins, dont_filter=True)
			request.meta['item'] = item
			request.meta['course'] = course
			request.meta['i'] = i
			request.meta['ins_set'] = ins_set
			yield request
		else:
			par_set = course.get('partnerIds')
			if par_set != None and par_set:
				item['institution_name'] = []
				request = scrapy.Request(self.par_head + par_set[0], callback=self.parse_par, dont_filter=True)
				request.meta['item'] = item
				request.meta['i'] = 0
				request.meta['par_set'] = par_set
				yield request
			else:
				item['institution_name'] = []
				if not item['instructors']:
					item['instructors'] = ''
				else:
					string = ''
					flag = False
					for e in item['instructors']:
						if flag == False:
							string += e
						else:
							string += ', ' + e
						flag = True
					item['instructors'] = string
				yield item
			
	def parse_par(self, response):
		item = response.meta['item']
		i = response.meta['i']
		par_set = response.meta['par_set']
		jsonstr = response.text
		dict = json.loads(jsonstr)
		
		for par in dict['elements']:
			name = par['name']
			if name != '':
				item['institution_name'].append(name)
			#shortName = par['shortName']
			#if shortName != '':
			#	item['institution'].append(shortName)
		
		i += 1
		if i <= len(par_set) - 1:
			request = scrapy.Request(self.par_head + par_set[i], callback=self.parse_par, dont_filter=True)
			request.meta['item'] = item
			request.meta['i'] = i
			request.meta['par_set'] = par_set
			yield request
		else:
			if not item['instructors']:
				item['instructors'] = ''
			else:
				string = ''
				flag = False
				for e in item['instructors']:
					if flag == False:
						string += e
					else:
						string += ', ' + e
					flag = True
				item['instructors'] = string
			yield item