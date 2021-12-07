from bs4 import BeautifulSoup
from urllib import request
def load_players(job, format):
    response=request.urlopen(f"https://www.icc-cricket.com/rankings/mens/player-rankings/{format}")
    data=response.read().decode("utf-8")
    soup=BeautifulSoup(data, 'html.parser')
    top=soup.select(f'div[data-cricket-role={job}]')[0]
    num1=top.select('.rankings-block__banner--name')
    print(num1[0].text)
    table=top.find('table')
    rows=table.select('a')
    players=[num1[0].text]
    for thing in rows:
        players.append(thing.text)
    return players
def load_teams(format):
    teamNames=[]
    response=request.urlopen(f"https://www.icc-cricket.com/rankings/mens/team-rankings/{format}")
    data=response.read().decode("utf-8")
    soup=BeautifulSoup(data, 'html.parser')
    table=soup.find("table")
    rows=table.find_all("tr")
    for row in rows:
        tds=row.find_all('td')
        for td in tds:
            name=td.find_all('span')
            if(len(name)>1):
                for tad in name:
                    if('u-hide-phablet' in tad['class']):
                        teamNames.append(tad.text)
    return teamNames