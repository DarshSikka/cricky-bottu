from urllib import request
from bs4 import BeautifulSoup
def load_score(i=0):
    response=request.urlopen(f"https://www.espncricinfo.com/")
    data=response.read().decode("utf-8")
    soup=BeautifulSoup(data, 'html.parser')
    matchinfo=soup.select('.match-info')[i]
    print(matchinfo.text)
    teamsFull=matchinfo.select('.teams')[0]
    teams=teamsFull.select('.team')
    team1_name, team1_score=teams[0].select('.name-detail')[0], teams[0].select('.score-detail')[0]
    team2_name=teams[1].select('.name-detail')[0]
    score=soup.select('.match-info-link-HSB')[1]
    print(score)
    link='https://espncricinfo.com/'+score['href']
    print(link)
    response2=request.urlopen(link)
    data2=response2.read().decode("utf-8")
    soup2=BeautifulSoup(data2, 'html.parser')
    table=soup2.select('table')[0]
    batting, bowling=table.select("tbody")[0], table.select("tbody")[1]
    batter1, batter2=batting.select("tr")
    bowler1, bowler2=bowling.select('tr')
    batter1_name, batter1_runs, batter1_balls=batter1.select("td")[0].select('.player-name')[0].text, batter1.select("td")[1].text, batter1.select("td")[2].text
    batter2_name, batter2_runs, batter2_balls=batter2.select("td")[0].select('.player-name')[0].text, batter2.select("td")[1].text, batter2.select("td")[2].text
    print(batter1_name, batter1_runs, batter1_balls)
    print(batter2_name, batter2_runs, batter2_balls)
    bowler1_name, bowler1_wickets, bowler1_runs=bowler1.select("td")[0].select('.player-name')[0].text, bowler1.select("td")[4].text, bowler1.select("td")[3].text
    bowler2_name, bowler2_wickets, bowler2_runs=bowler2.select("td")[0].select('.player-name')[0].text, bowler2.select("td")[4].text, bowler2.select("td")[3].text
    try:
        team2_score=teams[1].select('.score-detail')[0]
        print(team2_score)
    except:
        team2_score={
            'text':'did not bat'}
    try:
        team1_second_innings=teams[0].select('.score-detail')[1]
    except:
        team1_second_innings={'text':'did not bat'}
    try: 
        team2_second_innings=teams[1].select('.score-detail')[1]
    except:
        team2_second_innings={'text':'did not bat'}
    return {
        'team1': {
            'name': team1_name.text,
            'score': team1_score.text+ " & " + team1_second_innings['text']
        },
        'team2': {
            'name': team2_name.text,
            'score': team2_score['text']+" & "+team2_second_innings['text']
        },
        'batting-info':f'''
        Batter 1, {batter1_name}```{batter1_runs} of {batter1_balls}```
        Batter 2, {batter2_name}```{batter2_runs} of {batter2_balls}```
        ''',
        'bowling-info':f'''
        Bowler 1, {bowler1_name}
        ```{bowler1_wickets} wickets for {bowler1_runs} runs ``` Bowler 2, {bowler2_name}, ```{bowler2_wickets} wickets for {bowler2_runs} runs```
        '''
    }