import scrapy
import re
import json
from KEEPSearch.items import KeepsearchItem

class SearchxuetangSpider(scrapy.Spider):
	name = "searchxuetang"
	allowed_domains = ["xuetangx.com"]
	start_urls = {
		"http://www.xuetangx.com/courses"
	}
	file = None
	url_dict = {}
	#course_count = 0
	#item_count = 0
	
	def parse(self, response):
		course_set = response.xpath("//div[@class='list_inner cf']")
		if not course_set :
			"""
			file = open("xuetang_courses_tmp.json")
			line = file.readline()
			while line:
				data = json.loads(line)
				item = KeepsearchItem()
				item['title'] = data['title']
				item['image'] = data['image']
				item['instructor'] = data['instructor']
				item['description'] = data['description']
				item['start_time'] = data['start_time']
				item['end_time'] = data['end_time']
				item['category'] = data['category']
				item['course_url'] = data['course_url']
				item['institution'] = data['institution']
				request = scrapy.Request(item['course_url'], callback=self.parse1)
				request.meta['item'] = item
				yield request
				line = file.readline()
			"""
			return
		
		flag = False
		for course in course_set:
			course_link = response.urljoin(course.xpath("div[@class='img fl']/a/@href").extract()[0])
			i = self.url_dict.get(course_link)
			if i != None:
				flag = True
				break
		if flag == True:
			yield scrapy.Request(response.url, callback=self.parse, dont_filter=True)
		else:
			for course in course_set:
				item = KeepsearchItem()
				
				imgurl = response.urljoin(\
						(course.xpath("div[@class='img fl']/a/img/@src").extract())[0])
				item['cover_url'] = imgurl
				
				title = (course.xpath("div[@class='fl list_inner_right cf']\
						/div[@class='coursename']/a/h2").re(r'<.*>(.*)<.*>'))[0]
				item['title'] = title
				
				instructor = (course.xpath("div[@class='fl list_inner_right cf']\
						/div[@class='coursename']/div[@class='cf teacher']\
						/div[@class='fl name']/p/span[1]").re(r'<.*>(.*)<.*>'))[0]
				#instructor_list = []
				#instructor_list.append(instructor)
				item['instructors'] = instructor
				
				string = course.xpath("div[@class='fl list_inner_right cf']\
						/div[@class='coursename']/div[3]").extract()[0]
				#matchobj = re.match(r'[\s\S]*<div.*>[\s\S]*<p.*><span.*>([\s\S]*)</span>([\s\S]*)</p>[\s\S]* \
				#		<p[\s\S]*><span[\s\S]*>([\s\S]*)</span>([\s\S]*)</p>[\s\S]*', string)
				matchobj = re.match(r'<div.*>[\s\S]*<p.*><span.*>([\s\S]*)</span>([\s\S]*)</p>[\s\S]*<p.*><span.*>([\s\S]*)</span>([\s\S]*)</p>', string)
				if matchobj != None:
					desc = matchobj.group(1) + ': ' + matchobj.group(2) + '\n\n' \
							+ matchobj.group(3) + ': ' + matchobj.group(4)
				else:
					matchobj = re.match(r'<div.*>[\s\S]*<p.*><span.*>([\s\S]*)</span>([\s\S]*)</p>', string)
					if matchobj != None:
						desc = matchobj.group(1) + ': ' + matchobj.group(2)
					else:
						desc = ""
				item['description'] = desc
				
				start = course.xpath("div[@class='fl list_inner_right cf']\
						/div[@class='coursename']/p/span[2]/@data-start").extract()
				if start:
					start = start[0]
				else:
					start = ""
				item['start_date'] = start
				
				end = course.xpath("div[@class='fl list_inner_right cf']\
						/div[@class='coursename']/p/span[2]/@data-end").extract()
				if end:
					end = end[0]
				else:
					end = ""
				item['end_date'] = end
				
				cate = []
				cate_set = course.xpath("div[@class='fl list_inner_right cf']\
						/div[@class='coursename']/div[@class='coursename_ref']/span")
				for cate_obj in cate_set:
					cate_e = cate_obj.xpath("a/text()").extract()[0]
					cate.append(cate_e)
				item['subject_name'] = cate
				
				course_link = response.urljoin(course.xpath("div[@class='img fl']/a/@href").extract()[0])
				item['course_url'] = course_link
				self.url_dict[course_link] = 1
				
				institution = []
				"""
				ins_set = course.xpath("div[@class='fl list_inner_right cf']\
						/div[@class='coursename']/div[@class='cf teacher']\
						/div[@class='fl name']/p/span")
				flag = False
				for ins_obj in ins_set:
					if flag == True:
						ins_e = ins_obj.xpath("text()").extract()
						if ins_e:
							institution.append(ins_e[0])
					flag = True
				"""
				item['institution_name'] = institution
				
				item['provider_name'] = ['xuetang']
				
				#self.course_count += 1
				#item['count'] = self.course_count
				
				request = scrapy.Request(course_link, meta={'item':item}, callback=self.parse1)
				yield request
				#line = json.dumps(dict(item)) + '\n'
				#self.file.write(line)
				#yield item
				
			url = response.url
			matchobj = re.match(r'.*page(.*)', url)
			if not matchobj :
				next_url = url + "?page=2"
				yield scrapy.Request(next_url, callback=self.parse)
			else:
				strr = url.split('page=')
				page_num = int(strr[1])
				page_num += 1
				next_url = strr[0] + 'page=' + str(page_num)
				yield scrapy.Request(next_url, callback=self.parse)
	
	def err_deal(self, response):
		yield response.meta['item']
	
	def parse1(self, response):
		item = response.meta['item']
		
		start_time = response.xpath("//div[@class='course_info']/@data-start").extract()
		if start_time:
			item['start_date'] = start_time[0]
		
		end_time = response.xpath("//div[@class='course_info']/@data-end").extract()
		if end_time:
			item['end_date'] = end_time[0]
		
		ins_e = response.xpath("//p[@class='courseabout_text']/a[1]/text()").extract()
		if ins_e:
			item['institution_name'].append(ins_e[0])
			
		commitment = response.xpath("//div[@class='course_info']/@data-duration").extract()[0]
		commitment = re.sub(r"<span>", "", commitment)
		commitment = re.sub(r"</span>", "", commitment)
		item['commitment'] = commitment
		
		#self.item_count += 1
		
		return item