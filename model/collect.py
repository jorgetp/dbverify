import os

def protocol_name(results):
	return results.get('Protocol')

def list_to_table_entry(items):
	html_code = "<tr>\n"
	
	html_code += "\t<td>"+items[0]+"</td>\n"

	for item in items[1:]:
		style = ""
		if "falsified" in item:
			style = " style=\"color:red;\""
		elif "verified" in item:
			style = " style=\"color:green;\""
		
		html_code += "\t<td"+style+">" + item + "</td>\n"
	
	html_code += "</tr>\n"
	return html_code

def list_to_table_head(items):
	html_code = "<thead>\n<tr>\n"
	i = 1
	for item in items:
		if item == "Protocol":
			html_code += "\t<th>"+ item + "</th>\n"
		else:
			html_code += "\t<th data-priority=\""+ str(i) +"\">"+ item + "</th>\n"
			i += 1
	html_code += "</tr>\n</thead>\n"
	return html_code

def create_html_code():

	print 'Creating html code...'
	
	global_results = []
	lemmas = []

	proto_count = 0

	for file in os.listdir("./"):
		
		if '.proof' in file:
			
			print '\tProcessing:', file

			proto_count += 1
			
			results = {}
			
			lines = open('./' + file).readlines()
			lines = lines[lines.index('summary of summaries:\n')+1:]
			
			for line in lines:
				if ':' in line:
					l = line.split(':')
					
					lemma = l[0].strip()

					if '(exists-trace)' in lemma:
						lemma = lemma[:-15]

					if '(all-traces)' in lemma:
						lemma = lemma[:-13]

					result = l[1].strip()

					if lemma == 'analyzed':
						lemma = 'Protocol'
						result = result[:-6]

					if lemma not in lemmas:
						lemmas.append(lemma)

					results[ lemma ] = result

			global_results.append(results)

	# move 'warning' column to the end		
	if 'WARNING' in lemmas:
		index = lemmas.index('WARNING')
		lemmas = lemmas[:index] + lemmas[index+1:] + ['WARNING']

	global_results.sort(key=protocol_name)

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
	html += "<h2>Verification results: " + str(proto_count) + " protocol(s) analyzed</h2>\n\n"
	html += "<table data-role=\"table\" data-mode=\"columntoggle\" class=\"ui-responsive\">\n"
	html += list_to_table_head(lemmas)
	
	html += "<tbody>\n"
	for results in global_results:

		results_list = []
		for lemma in lemmas:
			try:
				results_list.append( results[lemma] )
			except:
				results_list.append('')
		
		html += list_to_table_entry(results_list)

	html += "</tbody>\n</table>\n</body>\n</html>"
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
