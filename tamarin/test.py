import os

sep = '//GENERIC CODE AFTER THIS LINE'

for file in os.listdir("./"):
		if '.spthy' in file:
			protocolmodel = open(file).read().split(sep)[0]
			if 'Action' in protocolmodel:
				print file

