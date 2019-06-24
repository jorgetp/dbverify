import os, re, platform

def to_timeformat(time):
	hours = int(time / 3600)
	time -= hours * 3600
	mins = int(time / 60)
	time  -= mins * 60
	secs = time

	tt = str(mins) + 'm' + '{0:.3f}'.format(secs) + 's'
	if hours > 0:
		tt = hours + 'h' + tt
	return tt

def to_secs(time):
	t = 0.0
	if 'h' in time:
		t += int(time.split('h')[0]) * 3600
		time = time.split('h')[1]
	if 'm' in time:
		t += int(time.split('m')[0]) * 60
		time = time.split('m')[1]
	t += float(time.split('s')[0])
	return t

def protocol_name(results):
	return results.get('Protocol')

def list_to_table_entry(items):
	html_code = "<tr>\n"
	
	html_code += "\t<td>"+items[0]+"</td>\n"

	for item in items[1:]:
		style = ""
		if "falsified" in item:
			style = " style=\"color:red\""
		elif "verified" in item:
			style = " style=\"color:green\""
		
		html_code += "\t<td"+style+">" + item + "</td>\n"
	
	html_code += "</tr>\n"
	return html_code

def create_html_code():

	print 'Creating html code...'
	
	global_results = []
	lemmas = ['Protocol']

	time_sum = {'user': 0.0, 'sys': 0.0, 'real': 0.0}
	time_min = {'user': 1000000000.0, 'sys': 1000000000.0, 'real': 1000000000.0}
	time_max = {'user': 0.0, 'sys': 0.0, 'real': 0.0}

	loc_sum = 0

	proto_count = 0

	for file in os.listdir("./"):

		if '.proof' in file:

			results = {}
			proto_name = file.replace('.proof', '')			
			print 'Gathering results for: ', proto_name
			results['Protocol'] = proto_name
			proto_count += 1
			
			content = open('./' + file).read()

			res = re.findall(r'^ (.*) \((all-traces|exists-trace)\): (.*\(\d* steps\))$', \
						content, re.MULTILINE)
		
			for (lemma, dummy, result) in res:
				lemma = lemma.strip()
				if lemma not in lemmas:
					lemmas.append(lemma)
				results[ lemma ] = result.strip()

			# timings
			time_display = {}
			TIMING_FORMAT = ''
			res = re.findall(r'^(real|user|sys)\s([\d*h]?\d*m\d*[\.,]\d*s)$', \
						content, re.MULTILINE)

			for (key, time) in res:
				time_display[key] = time
				t = to_secs ( time )					
				time_sum[key] += t
				if t < time_min[key]: time_min[key] = t
				if t > time_max[key]: time_max[key] = t

			#results['Time (real, user, sys)'] = \
			#			timing_display['real'] + ", " + \
			#			timing_display['user'] + ", " + \
			#			timing_display['sys']
			results['Time'] = time_display['real']

			# lines of code
			loc = len(open(proto_name + '.spthy').readlines())
			results['LoC'] = str(loc)
			loc_sum  += loc

			global_results.append(results)

	global_results.sort(key=protocol_name)

	# move 'WARNING' column to the end		
	if 'WARNING' in lemmas:
		index = lemmas.index('WARNING')
		lemmas = lemmas[:index] + lemmas[index+1:] + ['WARNING']
	
	# just in case, move column 'Protocol' to the front
	index = lemmas.index('Protocol')
	lemmas = ['Protocol'] + lemmas[:index] + lemmas[index+1:]

	# add 'LoC' and 'Time' columns
	lemmas = lemmas + ['LoC', 'Time']
	
	# create HTML code
	head 	= "<head>\n"
	head +=	"<meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">\n"
	head += "<link rel=\"stylesheet\" href=\"https://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.css\">\n"
	head += "<script src=\"https://code.jquery.com/jquery-1.11.3.min.js\"></script>\n"
	head += "<script src=\"https://code.jquery.com/mobile/1.4.5/jquery.mobile-1.4.5.min.js\"></script>\n"
	head += "<style>\n"
	head += "	td, th {\n"
	head += "  	border: 1px solid #dddddd;\n"
	head += "  	text-align: left\n"
	head += "	}\n"
	head += "	tr:nth-child(even) {\n"
	head += "  	background-color: #dddddd;\n"
	head += "	}\n"
	head += "</style>\n</head>\n"

	html 	= "<!DOCTYPE html>\n<html>\n"+ head +"<body>\n"
	html += "<h2>Verification results</h2>\n\n"
	#html += "<p>System info: \'<b>" + str(platform.uname()) + "\'</b></p>\n\n"
	#html += "<p>Protocol models in: \'<b>" + os.path.abspath('.') + "\'</b></p>\n\n"
	html += "<p>Number of protocols analyzed: <b>" + str(proto_count) + "</b></p>\n\n"
	html += "<p>Average number of lines of code: <b>" + str( loc_sum / proto_count ) + "</b></p>\n\n"
	#html += "<p>Average timings: \
	#				real <b>" + to_timeformat	( timing_sum['real'] / proto_count) + "</b>, \
	#				user <b>" + to_timeformat	( timing_sum['user'] / proto_count) + "</b>, \
	#				sys <b>" + to_timeformat	( timing_sum['sys'] / proto_count) +"</b></p>\n\n"
	html += "<p>Verification time: \
					min <b>" + to_timeformat	( time_min['real'] ) + "</b>, \
					ave <b>" + to_timeformat	( time_sum['real'] / proto_count) + "</b>, \
					max <b>" + to_timeformat	( time_max['real'] ) +"</b></p>\n\n"
	
	html += "<table data-role=\"table\" data-mode=\"columntoggle\" class=\"ui-responsive compact\" >\n"

	# table head
	html += "<thead>\n<tr>\n\t<th>Protocol</th>\n"
	for col in lemmas[1:]:
		html += "\t<th data-priority=\"1\">"+ col + "</th>\n"
	html += "</tr>\n</thead>\n"

	# table body
	html += "<tbody>\n"
	for results in global_results:

		results_list = []
		for lemma in lemmas:
			try:
				results_list.append( results[lemma] )
			except:
				results_list.append('')
		
		html += list_to_table_entry(results_list)

	html += "</tbody>\n</table>\n<p></p>\n</body>\n</html>"
	print 'Done.'
	return html

def write_html_to_output(html, output):
	print 'Writing html code to output...'
	outfile = open('./'+output, 'w')
	outfile.write(html)
	outfile.close()
	print 'Done.'

def main():
	html = create_html_code()
	write_html_to_output(html, 'results.html')

main()
