##Most of this code comes from the mitchware script named scamalytics_ahk.py.  Made a few adjustments for clarity and error resolution.
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



s=requests.session()

##Pulls the IPs to investigate from the clipboard
print("IPs are pulled from the most recent item in the clipboard.")
ips=re.findall('\d{1,3}(?:\.\d{1,3}){3}', pyperclip.paste())

print(ips)
## Fields to extract
ip_data={}
for ip in ips:
	ip_data[ip]={
		'city':'',
		'region':'',
		'country code':'',
		'organization name':'',
		'isp name':'',
		'score':'',
		'connection type':'',
		'anonymizing vpn':'',
		'tor exit node':'',
		'public proxy':'',
		'web proxy':'',
		'server':''
	}
	
	response=s.get(f"https://scamalytics.com/ip/{ip}")
	soup=BeautifulSoup(response.text, features='lxml')
	threat_info=json.loads(soup.find('pre').text.strip())
	ip_data[ip]['score']=threat_info['score']+'/100'
	#print(threat_info)
	
	table=soup.find('table')
	rows=table.find_all('tr')
	for row in rows:
		field=''
		value=''
		try:
			field=row.find('th').text.lower()
		except Exception:
			field='n/a'
		try:
			value=row.find('td').text.lower()
		except Exception:
			value='n/a'
		
		#print(field,value)
		if field in ip_data[ip]:
			ip_data[ip][field]=value

data_string=''
for ip, data in ip_data.items():
## Create if thens which convert Yes/no values to Server, VPN, etc
#	if data['server']=='No':
#		serv='Not Server'
#	else:
#		serv="Server"
	## Exported fields
	data_string+=f"{ip}, {data['city'].title()}, {data['region'].title()}, {data['country code'].upper()}, {data['isp name'].title()}, {data['organization name'].title()}, {data['connection type'].title()}, {data['score']}, {data['server'].title()}, {data['anonymizing vpn'].title()}, {data['tor exit node'].title()}, {data['public proxy'].title()}, {data['web proxy'].title()}\n"
## Prints results to console
print("Results")
print("Note: Results are also exported to clipboard")
print("---------------------------------------------------------")
print("IP, City, Region, Country, ISP, Organization, Connection Type, Score, Server? (Yes/No), Anonymizing VPN?, TOR?, Public Proxy?, Web Proxy?")
print(data_string)

## Exports results to clipboard
pyperclip.copy(data_string)