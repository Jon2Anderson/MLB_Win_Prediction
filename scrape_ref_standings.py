import pandas as pd
import os
import requests
import collections as co
from bs4 import BeautifulSoup

os.chdir('g:\\gradschool\\bigdata\\project')
years=['2019','2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2006','2005','2004','2003','2002','2001','2000']
masterstandingsdf = pd.DataFrame(columns=['Team','Year','W','L'])
for year in years:
    print(year)
    url = 'https://www.baseball-reference.com/leagues/MLB/%s-standings.shtml' %year
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    tables = soup.findAll('table', {'class': 'suppress_all sortable stats_table'})
    
    standingsdf = pd.DataFrame(columns=['Team','Year','W','L'])
    i=0
    for table in tables:
        table_head = tables[i].find('thead')
        table_body = tables[i].find('tbody')
        
        header=[]
        for th in table_head.findAll('th'):
            key=th.get_text()
            header.append(key)
            
        teamlist=[]
        for a in table_body.findAll('a'):
            teamlist.append(a.text)
            
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
        df['Team'] = teamlist
        df['Year'] = year
        df = df[['Team', 'Year', 'Tm','W']]
        df.columns = ['Team','Year','W','L']
        standingsdf = pd.concat([standingsdf, df])
        i = i + 1
    
    masterstandingsdf = pd.concat([masterstandingsdf, standingsdf])

masterstandingsdf['W'] = pd.to_numeric(masterstandingsdf['W'])
masterstandingsdf['L'] = pd.to_numeric(masterstandingsdf['L'])
masterstandingsdf['Pct'] = masterstandingsdf['W'] / (masterstandingsdf['L'] + masterstandingsdf['W'])
masterstandingsdf.to_csv('Last20Years_MLBStandings.csv')
