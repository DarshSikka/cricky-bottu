from urllib import request
from bs4 import BeautifulSoup
def load_matches():
    response=request.urlopen(f"https://www.espncricinfo.com/")
    data=response.read().decode("utf-8")
    soup=BeautifulSoup(data, 'html.parser')
    matches=""
    for a in range(5):
        matchinfo=soup.select('.match-info')[a]
        teamsFull=matchinfo.select('.teams')[0]
        teams=teamsFull.select('.team')
        team1_name=teams[0].select('.name-detail')[0].text
        team2_name=teams[1].select('.name-detail')[0].text
        scoreboard=team1_name+ " vs "+team2_name
        matches+=f'\n {a}. {scoreboard}'
    return matches