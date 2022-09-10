import requests
from bs4 import BeautifulSoup
years={}
for year in range(2001,2022):
    weeks={}
    for week in [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]:
        url = f'https://www.nfl.com/injuries/league/{year}/REG{week}'
        r = requests.get(url)
        soup = BeautifulSoup(r.text,'html.parser')
        players={}
        counter=0
        if soup.find_all("table", {"class" : "d3-o-table d3-o-table--detailed d3-o-reports--detailed"})!=[]:
            for nom in soup.find_all("table", {"class" : "d3-o-table d3-o-table--detailed d3-o-reports--detailed"}):
                for lick in nom.tbody.find_all('tr'):
                    for yeah in lick.find_all('td'):
                        counter+=1
                        if counter==1:
                            player=(" ".join(yeah.text.split()))
                        if counter==2:
                            position=(" ".join(yeah.text.split()))
                        if counter==3:
                            injury=(" ".join(yeah.text.split()))
                        if counter==4:
                            practicestatus=(" ".join(yeah.text.split()))
                        if counter==5:
                            gamestatus=(" ".join(yeah.text.split()))
                            print(year,week,player.split(',')[0],position.split(',')[0],injury.split(',')[0],practicestatus.split(',')[0],gamestatus.split(',')[0],sep=',')
                            counter=0
