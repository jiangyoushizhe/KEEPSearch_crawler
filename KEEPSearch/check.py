file = open("count.txt", 'r')
out = open('check.txt', 'w')

vis = []

while True:
	string = file.readline()
	if string == '0':
		break
	vis.append(int(string))
	
for i in xrange(1026):
	flag = False
	for e in vis:
		if e == i + 1:
			flag = True
			break
	if flag == False:
		out.write(str(i + 1) + '\n')
		
file.close()
out.close()
	
		

