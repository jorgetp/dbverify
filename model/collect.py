import os

def list_to_table_line(items, tag):
	return "\n".join(["<"+tag+">" + item + "</" + tag + ">" for item in items])


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

	# create HTML code

	html = 	"<!DOCTYPE html><html><head><style>\
						table {\
	    				border-collapse: collapse;\
	    				width: 100%;\
						}\
						td, th {\
	    				border: 1px solid #dddddd;\
	    				text-align: left;\
	    				padding: 8px;\
						}\
						tr:nth-child(even) {\
	    				background-color: #dddddd;\
						}\
					</style></head><body>\
					<h2>Verification results: " + str(proto_count) + " protocol(s) analyzed</h2>\
					<table align=\"left\">\n"

	html += "<tr>" + list_to_table_line(lemmas, 'th')+"</tr>\n"

	for results in global_results:

		results_list = []
		for lemma in lemmas:
			try:
				results_list.append( results[lemma] )
			except:
				results_list.append('')
		
		html += "<tr>" + list_to_table_line(results_list, 'td')+"</tr>\n"

	html += "</table></body></html>"
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
