import pandas as pd
import os
import json
import requests
import collections as co
from bs4 import BeautifulSoup

teams=['ARI','ATL','BAL','BOS','CHC','CHW','CIN','CLE','COL','DET','HOU','KCR','LAA','LAD','MIA','MIL','MIN','NYM','NYY','OAK','PHI','PIT','SDP','SEA','SFG','STL','TBR','TEX','TOR','WSN']
years=['2019','2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2006','2005','2004','2003','2002','2001','2000']

finaldf = pd.DataFrame(columns=['Team','Year','OPS','ERA'])

for team in teams:
    print(team)
    masterdf = pd.DataFrame(columns=['Team','Year','OPS','ERA'])
    for year in years:
        print(year)
        url = 'https://www.baseball-reference.com/teams/%s/%s.shtml' %(team,year)
        r = requests.get(url)

        soup = BeautifulSoup(r.text, 'lxml')
        try:
            hit_table = soup.find('table', {'class': 'sortable stats_table', 'id': 'team_batting'})
            pitch_table = soup.find('table', {'class': 'sortable stats_table', 'id': 'team_pitching'})

            hit_table_foot = hit_table.find('tfoot')
            pitch_table_foot = pitch_table.find('tfoot')

            opslist = []
            for td in hit_table_foot.findAll('td', {'data-stat': 'onbase_plus_slugging'}):
                opslist.append(td.text)
            the_ops = opslist[0]

            eralist = []
            for td in pitch_table_foot.findAll('td', {'data-stat': 'earned_run_avg'}):
                eralist.append(td.text)
            the_era = eralist[0]

            tempdf = pd.DataFrame({'Team': team, 'Year': year, 'OPS': the_ops, 'ERA': the_era}, index=[0])
            masterdf = pd.concat([masterdf,tempdf])
        except:
            print('Problem with ' + team + ' in ' + year)
    finaldf = pd.concat([finaldf,masterdf])

finaldf = finaldf[['Team','Year','OPS','ERA']]
print(finaldf.shape)