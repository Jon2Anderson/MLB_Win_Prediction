import pandas as pd
import os
import json
import requests
import collections as co
from bs4 import BeautifulSoup

teams=['ARI','ATL','ANA','MON','TBD','BAL','BOS','CHC','CHW','CIN','CLE','COL','DET','HOU','FLA','KCR','LAA','LAD','MIA','MIL','MIN','NYM','NYY','OAK','PHI','PIT','SDP','SEA','SFG','STL','TBR','TEX','TOR','WSN']
teamnamechangedict = json.load(open('/home/Jon2Anderson/school/team_namechange_dict.json'))
teamabbrevdict = json.load(open('/home/Jon2Anderson/school/teamabbrevs.json'))
years=['2019','2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2006','2005','2004','2003','2002','2001','2000']
masterdf = pd.DataFrame(columns=['Team','Year','Attend'])
for year in years:
    print(year)
    url = 'https://www.baseball-reference.com/leagues/MLB/%s-misc.shtml' %year
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    table = soup.find('table', {'class': 'sortable stats_table', 'id': 'teams_miscellaneous'})

    table_head = table.find('thead')
    table_body = table.find('tbody')

    header=[]
    for th in table_head.findAll('th'):
        key=th.get_text()
        header.append(key)


    teamlist=[]
    for a in table_body.findAll('a'):
        teamlist.append(a.text)

    teamlist2 = []
    for team in teamlist:
        if team in teams:
            teamlist2.append(team)


    trlist=[]
    for tr in table_body.findAll('tr'):
        trlist.append(tr)

    listofdicts=[]
    for row in trlist:
        the_row=[]
        for td in row.findAll('td'):
            the_row.append(td.text)
        od = co.OrderedDict(zip(header, the_row))
        listofdicts.append(od)

    df = pd.DataFrame(listofdicts)
    df['Team'] = teamlist2
    df['Year'] = year
    df = df[['Team','Year','Tm']]
    df.columns=['Team','Year','Attend']
    masterdf = pd.concat([masterdf,df])

masterdf['Team'] = masterdf['Team'].replace(teamabbrevdict)
print(masterdf.shape)
masterdf.to_csv('Last20Years_Attendance.csv')
