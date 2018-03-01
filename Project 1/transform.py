from bs4 import BeautifulSoup

import requests
import csv

r = requests.get("https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions")
html_content = r.text
tuples = []
soup = BeautifulSoup(html_content, "html.parser")

'''takes input as the entire cell and returns team name and number'''
def parse_team_name(arg1):
    name = ''
    for c in arg1:
        if c != "!":
            name += c
        else:
            name = name[:len(name)-1]
            break
    return name


'''returns false if the match has not taken place'''
def checkResult( arg2 ):
    if arg2[0] == 'X':
        return False
    else:
        return True


table = soup.find_all('table')[1]
for rows in table.find_all('tr'):
    cells = rows.find_all('td')
    if len(cells) > 0:
        game = cells[0].get_text()
        game = game[4:]
        year = cells[1].get_text()
        year = year[8:12]
        winning_team = parse_team_name(cells[2].get_text())
        score = cells[3].get_text()
        if "(OT)" in score:
            score = score[0:2] + "-" + score[2:4] + " OT"
        else:
            score = score[0:2] + "-" + score[2:4]
        losing_team = parse_team_name(cells[4].get_text())
        venue = parse_team_name(cells[5].get_text())
        item = {'game': game, 'year': year, 'winning_team':winning_team, 'score': score, 'losing_team': losing_team, 'venue': venue}
        tuples.append(item)

f = open('transformed.csv','a+')
with f:
    f.write('Game,Year,Winning team,Score,Losing team,Venue\n')
    for row in tuples:
        result = checkResult(row['winning_team'])
        if result:
            val = row['game'] + "," + row['year'] + "," + row['winning_team'] + "," + row['score'] + "," + row['losing_team'] + "," + row['venue']
            f.write(val + "\n")
f.close()
