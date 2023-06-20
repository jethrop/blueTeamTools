##Import all required packages
import sys
import subprocess

try:
	import re, requests, json, pyperclip, lxml
	from bs4 import BeautifulSoup
except Exception as e:
	## Auto install is not yet working
	##toInstall = ["re", "requests", "json", "pyperclip", "bs4", "lxml"]
	#for x in toInstall:
		# implement pip as a subprocess:
	#	subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
	#	x])
	print("You are missing required packages. If it fails again use pip install to remedy this")
	print(e)
        
#Define variables
output = ''

##Get contents of clipboard
clipboard = pyperclip.paste()

#Creates a list object containing all of the domains
pattern = '(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]'
domains = re.findall(pattern, clipboard)

#Function to sort list by the second level domain.  Adjust the list location [] to adjust what level of domain you want to sort by.  sub.second.root -3.-2.-1
###Use loop to sort by every level
def tld(Input):
    return Input.split('.')[-2]

#Store sorted list in a new list object
sDomains = sorted(domains, key=tld)

#Test prints
#print(clipboard)
#print(domains)
#print(sDomains)

#Convert list to a newline delimited string
for i in range(0, len(sDomains)):
     output += sDomains[i] + '\n'
sOutput = str(output)

#Info for end user
print("This tool takes a list of domains stored in the clipboard, sorts by the second level domain name, then outputs the results to the console and clipboard.")

#Output to console
print(sOutput)

#Output to clipboard
pyperclip.copy(str(sOutput))