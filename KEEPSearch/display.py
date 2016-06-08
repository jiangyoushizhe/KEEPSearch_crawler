
import json
import codecs

file = open("xuetang_courses_tmp.json")
line = file.readline()
while line:
	dict = json.loads(line)
	print dict
	raw_input(">")
	line = file.readline()