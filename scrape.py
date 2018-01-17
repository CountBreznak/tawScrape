from lxml import html
import requests
import csv

# https://python-guide-pt-br.readthedocs.io/en/latest/scenarios/scrape/

# plan is to:
#		-collect data from the wings of liberty server about the tours
#		-could maybe be used for taw statistics, too
#
#		-save it as a csv file, so it can be exported to excel or something

page = requests.get('http://il2stat.aviaskins.com:8008/en/?tour=21')
tree = html.fromstring(page.content)

#	<div class="bar_red_num">181</div>
#	<div class="bar_blue_num">181</div>
#	<div class="bar_gray_num">181</div>
#	<div class="total_num">1256</div>
#
#	All data seems to be set up in lists. Assuming lists are always set up in the same way, we get the following:
#		NumRed
#			1:	Number of won missions for reds
#			2:	Number of shot down aircraft by(?) reds
#			3: 	Number of destroyed ground Targets by red
#			4:	Score
#			5:	Number of h
#			6:	Number exclusive red Players in Tour
#		same goes for blue
#		note: NumGray just has the number of non-nation exclusive players in tour.


NumRed = tree.xpath('//div[@class="bar_red_num"]/text()')
NumRed = map(int, NumRed)
NumBlue = tree.xpath('//div[@class="bar_blue_num"]/text()')
NumBlue = map(int, NumBlue)
NumGray = tree.xpath('//div[@class="bar_gray_num"]/text()')
NumGray = map(int, NumGray)
NumPlayers = tree.xpath('//div[@class="total_num"]/text()')
NumPlayers = map(int, NumPlayers)

print 'Number of red Players: ', NumRed
print 'Number of blue Players: ', NumBlue
print 'Number of gray Players: ', NumGray
print 'Total Number of Players: ', NumPlayers
print NumRed[0]

nWonMisRed = NumRed[0]
nKillsRed = NumRed[1]
nGKRed = NumRed[2]
scoreRed = NumRed[3]
nHoursRed = NumRed[4]
nExclPlRed = NumRed[5]

nWonMisBlue = NumBlue[0]
nKillsBlue = NumBlue[1]
nGKBlue = NumBlue[2]
scoreBlue = NumBlue[3]
nHoursBlue = NumBlue[4]
nExclPlBlue = NumBlue[5]

nPlGray = NumGray[0]

nPlTotal = NumPlayers[0]

# not complete

# .csv file could look like this:
# tour-nr; Total Players, Player red; Player Blue; Player Gray; Missons Red; Missions Blue; Kills Red; Kills Blue; GKills Red; GKills Blue; ScoreRed; ScoreBlue; Hours Red; HoursBlue;

with open('csv.csv', 'wb') as csvfile:
	fieldnames = ['TourNo', 'NumUnique', 'NumPlayersRed', 'NumPlayersBlue', 'NumPlayersGray', ]
	writer = csv.DictWriter(csvfile, fieldnames = fieldnames, delimiter = '; ')
	writer.writeheader()
	writer.writerow({'Tour': nPlGray, 'Num': NumPlayers})