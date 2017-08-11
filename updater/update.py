import json
import re
import requests
import sys

with open('../site/users.json', 'r') as data_file:
	data = json.load(data_file)

def wrong_arg():
	print("[-] Missing or wrong argument")
	print("[-] Example: \n\tupdate.py update -> to update the json\n\tupdate.py add username realname -> to add a user to the json")
	sys.exit()

def update_users(user):
	print("[+] Starting update profil")
	r = requests.get('https://www.root-me.org/'+ user['username'] + '?inc=score')

	regex = r'<h1 itemprop="givenName">.*<span .*?>(.*)</span>'
	matches = re.search(regex, r.text)
	if matches:
		user['username_r'] = "{group}".format(group = matches.group(1))

	regex = r'<span.*?>\n(.*)<span.*?>/(.*)</span>'
	matches = re.search(regex, r.text)
	if matches:
		user['rank'] = "{group}".format(group = matches.group(1))
		total_rank = "{group}".format(group = matches.group(2))

	regex = r'<span.*?>\n(.*)&nbsp;Points'
	matches = re.search(regex, r.text)
	if matches:
		user['points'] = "{group}".format(group = matches.group(1))

	regex = r'<span.*?>\n([a-z]*)&nbsp;'
	matches = re.search(regex, r.text)
	if matches:
		user['status'] = "{group}".format(group = matches.group(1))

	regex = r'<span.*?>\n([0-9]*)/([0-9]*)'
	matches = re.search(regex, r.text)
	if matches:
		user['challenges'] = "{group}".format(group = matches.group(1))
		total_challenge = "{group}".format(group = matches.group(2))

	regex = r'<h1 itemprop="givenName"><img class=\'.*? logo_auteur .*?\' src="(.*?)"'
	matches = re.search(regex, r.text)
	if matches:
		avatar = "{group}".format(group = matches.group(1))
		user['avatar'] = "https://www.root-me.org/" + avatar

	print("[+] Infos user:")
	print("\t Url name", user['username'], "\n\t Username", user['username_r'], "\n\t Realn", user['realn'], "\n\t Avatar", user['avatar'], "\n\t Rank", user['rank'], "\n\t Points", user['points'], "\n\t Challenges succed",user['challenges'], "\n\t Status", user['status'])

	# Get all data from challenge
	regex = r'<span.*?>\n([0-9]*)&nbsp;Points&nbsp;([0-9]*)/([0-9]*)'
	matches = re.finditer(regex, r.text)
	for iter_chall, match in enumerate(matches):
		user['details'][iter_chall]["points"] 	= "{group}".format(group = match.group(1))
		user['details'][iter_chall]["flag"] 	= "{group}".format(group = match.group(2))
		user['details'][iter_chall]["total"] 	= "{group}".format(group = match.group(3))

	for detail in user['details']:
		print('\t',detail['name'], detail['points'], detail['flag'], detail['total'])

	with open('../site/users.json', 'w') as data_file:
		json.dump(data, data_file)

	print("[+] End update profil")

def update():
	print("[+] Starting Update generic information")

	# get generic data 
	r = requests.get('https://www.root-me.org/fr/Communaute/Classement/')
	regex = r'<a href=".*?>([0-9]+)</a>'
	matches = re.search(regex, r.text)
	if matches:
		data['total_points'] = "{group}".format(group = matches.group(1))

	r = requests.get('https://www.root-me.org/Capitaine-John?inc=score')
	regex = r'<span.*?>\n([0-9]*)/([0-9]*)'
	matches = re.search(regex, r.text)
	if matches:
		data['total_challenge'] = "{group}".format(group = matches.group(2))

	print("\t Total oints", data['total_points'], "\n\t Total challenge", data['total_challenge'])
	print("[+] End of update generic information")

	for user in data['users']:
		update_users(user)

def add_user(username, realn):
	print("[+] Starting to add user", username)

	data['users'].append({"username": username, "username_r": "", "realn": realn, "avatar": "https://www.root-me.org/local/cache-vignettes/L48xH48/auton0-5220c.png", "rank": 0, "points": 0, "challenges": 0, "status": "newbie", "details": [{"color": "#dbff6b", "total": "0", "points": "0", "flag": "0", "name": "App-Script"}, {"color": "#6166ff", "total": "0", "points": "0", "flag": "0", "name": "App-System"}, {"color": "#ff4141", "total": "0", "points": "0", "flag": "0", "name": "Cracking"}, {"color": "#b06cfb", "total": "0", "points": "0", "flag": "0", "name": "Cryptanalysis"}, {"color": "#35de59", "total": "0", "points": "0", "flag": "0", "name": "Forensic"}, {"color": "#6db8e4", "total": "0", "points": "0", "flag": "0", "name": "Progamming"}, {"color": "#ff5887", "total": "0", "points": "0", "flag": "0", "name": "Realist"}, {"color": "#e1e0ff", "total": "0", "points": "0", "flag": "0", "name": "Network"}, {"color": "#a441ff", "total": "0", "points": "0", "flag": "0", "name": "Steganography"}, {"color": "#ff84f0", "total": "0", "points": "0", "flag": "0", "name": "Web-Client"}, {"color": "#35a2ff", "total": "0", "points": "0", "flag": "0", "name": "Web-Server"}]})
	with open('../site/users.json', 'w') as data_file:
		json.dump(data, data_file)

	print("[+] End of add")
	# then update lasted
	update_users(data['users'][-1])

# ## STARTING POINT####
if len(sys.argv) < 2:
	wrong_arg()
else:
	if sys.argv[1] == "update":
		update()
	elif sys.argv[1] == "add" and len(sys.argv) == 4:
		add_user(sys.argv[2],sys.argv[3])
	else:
		wrong_arg()
