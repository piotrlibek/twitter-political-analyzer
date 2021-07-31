import re
import os
import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import argparse

token = ""

width = 26
height = 8
usePartyPatterns = False
useOnlyFollowersData = False
dontUseFollowersData = False

politicalPartiesNames = []
politicalPartyColors = []
politicalPartiesValues = {}
ideologyColors = []
ideologyNames = []
politicalParties = {}
ideologies = {}
rightPatterns = {}
leftPatterns = {}
centerPatterns = {}

rightWing = 0
leftWing = 0

bufferX = 0
bufferY = 0

politicalCompassX = 0
politicalCompassY = 0

twitterName = ""
languageFilename = ""


def transform_x(l):
	lower, upper = -0.5, 0.5
	l_norm = lower + (upper - lower) * l
	return np.clip(l_norm, -9.5, 9.5)

def transform_y(l):
	lower, upper = -0.25, 0.25
	l_norm = lower + (upper - lower) * l
	return np.clip(l_norm, -9.5, 9.5)

def make_political_compass(x, y):
	plt.clf()
	figure = plt.figure()
	ax = figure.add_subplot(111)
	ax.xaxis.set_visible(False)
	ax.yaxis.set_visible(False)

	# Normalize coordinates
	x = transform_x(x)
	y = transform_y(y)

	authoritarianRight = plt.Rectangle((0, 0), 10, 10, color='#40A8FC')
	authoritarianLeft = plt.Rectangle((-10, 0), 10, 10, color='#D98C7E')
	liberalRight = plt.Rectangle((0, -10), 10, 10, color='#B79CCF')
	liberalLeft = plt.Rectangle((-10, -10), 10, 10, color='#9ADC99')
	ax.text(-2, 10.5, 'Authoritarian', size=12)
	ax.text(-2, -11.5, 'Libertarian', size=12)
	ax.text(10.5, -0.50, 'Right', size=12)
	ax.text(-12, -0.50, 'Left', size=12)
	ax.text(-10, 10.5, format(x, '.1f') + ', ' + format(y, '.1f'), size=12)

	ax.add_patch(authoritarianRight)
	ax.add_patch(authoritarianLeft)
	ax.add_patch(liberalRight)
	ax.add_patch(liberalLeft)

	# Marker position

	plt.scatter(x, y, s=150, facecolors='red', edgecolors='black', zorder=2)
	plt.title("@" + twitterName, loc="right")

	plt.xlim(-10, 10)
	plt.ylim(-10, 10)
	plt.grid()
	plt.savefig(os.path.join(twitterName, 'political_compass.png'))

def load_data():
	for i in range(0, len(jsonData['politicalParties'])):
		# Append political parties colors to array
		politicalPartyColors.append(jsonData['politicalParties'][i]["color"])

	# Append political ideologies colors and names to array

	for i in range(0, len(jsonData['politicalIdeologies'][0]["rightPatterns"])):
		ideologyColors.append(
			jsonData['politicalIdeologies'][0]["rightPatterns"][i]["color"])
		ideologyNames.append(jsonData['politicalIdeologies']
							 [0]["rightPatterns"][i]["screenName"])

	for i in range(0, len(jsonData['politicalIdeologies'][1]["leftPatterns"])):
		ideologyColors.append(
			jsonData['politicalIdeologies'][1]["leftPatterns"][i]["color"])
		ideologyNames.append(jsonData['politicalIdeologies']
							 [1]["leftPatterns"][i]["screenName"])

	for i in range(0, len(jsonData['politicalIdeologies'][2]["centerPatterns"])):
		ideologyColors.append(
			jsonData['politicalIdeologies'][2]["centerPatterns"][i]["color"])
		ideologyNames.append(jsonData['politicalIdeologies']
							 [2]["centerPatterns"][i]["screenName"])

	for i in range(0, len(jsonData['politicalParties'])):
		# Append political parties to dictionary
		politicalParty = jsonData['politicalParties'][i]["name"]
		pattern = jsonData['politicalParties'][i]["pattern"]
		politicalParties[politicalParty] = pattern
		politicalPartiesValues[politicalParty] = 0

	# Append ideologies and default points to dictionary

	for i in range(0, len(jsonData['politicalIdeologies'][0]["rightPatterns"])):
		ideologyName = jsonData['politicalIdeologies'][0]["rightPatterns"][i]["name"]
		ideologyPattern = jsonData['politicalIdeologies'][0]["rightPatterns"][i]["pattern"]
		rightPatterns[ideologyName] = ideologyPattern
		ideologies[ideologyName] = 0

	for i in range(0, len(jsonData['politicalIdeologies'][1]["leftPatterns"])):
		ideologyName = jsonData['politicalIdeologies'][1]["leftPatterns"][i]["name"]
		ideologyPattern = jsonData['politicalIdeologies'][1]["leftPatterns"][i]["pattern"]
		leftPatterns[ideologyName] = ideologyPattern
		ideologies[ideologyName] = 0

	for i in range(0, len(jsonData['politicalIdeologies'][2]["centerPatterns"])):
		ideologyName = jsonData['politicalIdeologies'][2]["centerPatterns"][i]["name"]
		ideologyPattern = jsonData['politicalIdeologies'][2]["centerPatterns"][i]["pattern"]
		centerPatterns[ideologyName] = ideologyPattern
		ideologies[ideologyName] = 0

	rightValues = "".join(list(rightPatterns.values()))

	# Combine all patterns of ideology into one right-wing pattern
	rightPatterns["rightWing"] = re.sub('\)\(', '|', rightValues)

	leftValues = "".join(list(leftPatterns.values()))
	leftPatterns["leftWing"] = re.sub('\)\(', '|', leftValues)

	for key, value in politicalParties.items():
		# Create the array of political party names
		politicalPartiesNames.append(key)

def check_token():
	if token:
		print("Found a Bearer Token!")
	else:
		print("Bearer Token is not set! check tpan.py and change 'token' variable!")
		exit()

def check_arguments():
	parser = argparse.ArgumentParser()
	parser.add_argument("twitterName", help="Twitter username here")
	parser.add_argument("languageFilename", help="Language filename here")
	parser.add_argument("--width", help="Output image width")
	parser.add_argument("--height", help="Output image height")
	parser.add_argument("--dontUseFollowersData", help="Do not use data about the people who follow the user", action='store_true')
	parser.add_argument("--useOnlyFollowersData", action='store_true')
	parser.add_argument("--bearerToken", help="Bearer Authentication token")
	parser.add_argument("--usePartyPatterns", help="Experimental, improve the ideologies results", action='store_true')
	args = parser.parse_args()

	if args.twitterName and args.languageFilename:
		globals()["twitterName"] = args.twitterName
		globals()["languageFilename"] = args.languageFilename
		if args.width and args.height:
			globals()["width"] = int(args.width)
			globals()["height"] = int(args.height)
			print(f'The output image size is set to {width}x{height}')
		if args.bearerToken:
			globals()["token"] = args.bearerToken
		if args.usePartyPatterns:
			globals()["usePartyPatterns"] = True
		if args.useOnlyFollowersData:
			globals()["useOnlyFollowersData"] = True
		if args.dontUseFollowersData:
			globals()["dontUseFollowersData"] = True
	else:
		exit()

def make_work(users):
	for user in users["users"]:  # For each twitter user
		# Political Parties
		for key, value in politicalParties.items():  # For each political party
			# Check if that political party matches the pattern
			if re.search(politicalParties[key], user["description"], re.IGNORECASE):
				# Add the one point to that political party
				politicalPartiesValues[key] += 1
		# Right-wing
		for key, value in rightPatterns.items():  # For each right-wing ideologies
			# Check if that ideology or political wing matches the pattern
			if re.search(rightPatterns[key], user["description"], re.IGNORECASE):
				if key != "rightWing":  # Check if we check ideology
					if key in rightPatterns.keys():
						index = list(rightPatterns.keys()).index(key)
						globals()["bufferX"] += jsonData['politicalIdeologies'][0]["rightPatterns"][index]["x"]
						globals()["bufferY"] += jsonData['politicalIdeologies'][0]["rightPatterns"][index]["y"]
						partyPatterns = []
						fullPartyPattern = ""
						if usePartyPatterns:
							if jsonData['politicalIdeologies'][0]["rightPatterns"][index]["partyPattern"]:
								for party in jsonData['politicalIdeologies'][0]["rightPatterns"][index]["partyPattern"].split(","):
									partyPatterns.append(politicalParties[party])

								fullPartyPattern = "".join(list(partyPatterns))
								fullPartyPattern = re.sub('\)\(', '|', fullPartyPattern)
								if re.search(fullPartyPattern, user["description"], re.IGNORECASE):
									ideologies[key] += 1
					ideologies[key] += 1
				else:  # We check the political wing
					globals()["rightWing"] += 1
		# Left-wing
		for key, value in leftPatterns.items():  # For each left-wing ideologies
			if re.search(leftPatterns[key], user["description"], re.IGNORECASE):
				if key != "leftWing":
					if key in leftPatterns.keys():
						index = list(leftPatterns.keys()).index(key)
						globals()["bufferX"] += jsonData['politicalIdeologies'][1]["leftPatterns"][index]["x"]
						globals()["bufferY"] += jsonData['politicalIdeologies'][1]["leftPatterns"][index]["y"]
						partyPatterns = []
						fullPartyPattern = ""
						if usePartyPatterns:
							if jsonData['politicalIdeologies'][1]["leftPatterns"][index]["partyPattern"]:
								for party in jsonData['politicalIdeologies'][1]["leftPatterns"][index]["partyPattern"].split(","):
									partyPatterns.append(politicalParties[party])

								fullPartyPattern = "".join(list(partyPatterns))
								fullPartyPattern = re.sub('\)\(', '|', fullPartyPattern)
								if re.search(fullPartyPattern, user["description"], re.IGNORECASE):
									ideologies[key] += 1
					ideologies[key] += 1
				else:
					globals()["leftWing"] += 1
			# if key == "pro-lgbt":  # Check if that user has rainbow flag in twitter name
			#	if re.findall(leftPatterns[key], user["name"], re.IGNORECASE):
			#		ideologies[key] += 1
		# Centrism
		for key, value in centerPatterns.items():
			if re.search(centerPatterns[key], user["description"], re.IGNORECASE):
				ideologies[key] += 1

check_arguments()
check_token()

# Parse JSON and redirect data to variables

languageFile = open(languageFilename)
jsonData = json.load(languageFile)

load_data()

url = "https://api.twitter.com/1.1/friends/list.json?screen_name=" + \
	twitterName + "&count=200"

headers = {"Authorization": "Bearer " + token}

friendsData = requests.get(url, headers=headers).json()

url = "https://api.twitter.com/1.1/followers/list.json?screen_name=" + \
	twitterName + "&count=200"

followersData = requests.get(url, headers=headers).json()

if useOnlyFollowersData:
	make_work(followersData)
elif dontUseFollowersData:
	make_work(friendsData)
else:
	make_work(followersData)
	make_work(friendsData)

# Create a directory

output_directory = twitterName

try:
	os.mkdir(output_directory)
except OSError:
	print("Creation of the directory failed, check if is already exists!")
	exit()
else:
	print("Successfully created the directory")

# Political wing

pieLabels = ['Right-wing',
			 'Left-wing']
colors = ['#2196F3', '#F44336']

fig, ax = plt.subplots(1, 1, figsize=(4, 4))

ax.pie([rightWing, leftWing], labels=pieLabels, colors=colors,
	   labeldistance=9999999, autopct='%1.2f%%', explode=(0.03, 0.03))
ax.set(adjustable='box', aspect='equal')
ax.set_title("@" + twitterName)

handles, labels = ax.axes.get_legend_handles_labels()
ax.legend(handles, labels, prop={'size': 6},
		  bbox_transform=fig.transFigure)

plt.savefig(os.path.join(twitterName, 'political_wing.png'))
plt.clf()

# Ideologies

plt.figure(figsize=(width, height))
plt.bar(ideologyNames, ideologies.values(), color=ideologyColors, width=1)
plt.title("@" + twitterName)
plt.savefig(os.path.join(twitterName, 'ideologies.png'))
plt.clf()

# Political Party

plt.figure(figsize=(width, height))
plt.bar(politicalPartiesNames, politicalPartiesValues.values(),
		color=politicalPartyColors, width=1)
plt.title("@" + twitterName)
plt.savefig(os.path.join(twitterName, 'political_parties.png'))
plt.clf()

make_political_compass(bufferX, bufferY)

print("Done!")
