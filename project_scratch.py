# -*- coding: utf-8 -*-
"""
Big Data Analytics Final Project
Scratch Pad
"""
import pandas as pd, os, json, requests, collections as co
from bs4 import BeautifulSoup
os.chdir('g:\\gradschool\\bigdata\\project')
teamnamechangedict = json.load(open('G:\\GradSchool\\BigData\\project\\data\\team_namechange_dict.json'))
teamabbrevdict = json.load(open('G:\\GradSchool\\BigData\\project\\data\\teamabbrevs.json'))

## Import Data
standings = pd.read_csv("G:\\GradSchool\\BigData\\project\\data\\Last20Years_MLBStandings.csv")
attendance = pd.read_csv("G:\\GradSchool\\BigData\\project\\data\\Last20Years_Attendance.csv")
attendance['Attend'] = attendance['Attend'].str.replace(",","")
payrolls = pd.read_csv("G:\\GradSchool\\BigData\\project\\data\\Last20Years_Payrolls.csv")
teamstats = pd.read_csv("G:\\GradSchool\\BigData\\project\\data\\Last20Years_stats.csv")

mlb = pd.merge(standings, attendance, on=["Team","Year"])
mlb = pd.merge(mlb,payrolls, on=["Team","Year"])
mlb = pd.merge(mlb,teamstats, on=["Team","Year"])
mlb = mlb.loc[:,~mlb.columns.str.contains('^Unnamed')]

'''
## Functions used to collect data ##
def getTeamStats():
    teams=['ARI','ATL','BAL','BOS','CHC','CHW','CIN','CLE','COL','DET','HOU','KCR','LAA','LAD','MIA','MIL','MIN','NYM','NYY','OAK','PHI','PIT','SDP','SEA','SFG','STL','TBR','TEX','TOR','WSN']
    years=['2019','2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2006','2005','2004','2003','2002','2001','2000']
    
    finaldf = pd.DataFrame(columns=['Team','Year','OPS','ERA'])
    
    for team in teams:
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
    return(finaldf)

def getStandings():
    years=['2019','2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2006','2005','2004','2003','2002','2001','2000']
    masterstandingsdf = pd.DataFrame(columns=['Team','Year','W','L'])
    for year in years:
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
    return(masterstandingsdf)

def getAttendance():
    teams=['ARI','ATL','ANA','MON','TBD','BAL','BOS','CHC','CHW','CIN','CLE','COL','DET','HOU','FLA','KCR','LAA','LAD','MIA','MIL','MIN','NYM','NYY','OAK','PHI','PIT','SDP','SEA','SFG','STL','TBR','TEX','TOR','WSN']

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
    return(masterdf)

def getPayrolls():
    years=['2018','2017','2016','2015','2014','2013','2012','2011','2010','2009','2008','2007','2006','2005','2004','2003','2002','2001','2000']

    finaldf = pd.DataFrame(columns=['Team','Year','Payroll'])
    for year in years:
        print(year)
    
        # Input URL we want to scrape
        url = 'http://www.thebaseballcube.com/extra/payrolls/byYear.asp?Y=%s' %year
        
        # Get HTML contents of the URL
        r = requests.get(url)
        
        # Convert the text of that call to BeautifulSoup format 
        soup = BeautifulSoup(r.text, 'lxml')
        
        # Isolate the table we want, in this case it's a table
        # with class "sortable"
        table = soup.find('table', {'class': 'sortable'})
        
        # Loop through the table make list of all the contents of each row
        trlist=[]
        for tr in table.findAll('tr'):
            trlist.append(tr)
        
        # Make our header for the dataframe
        header=['Team','League','Payroll','Attend','Rk','Top5']
        
        # Loop through each row and grab the text of every <td> tag, saving
        # the text of those <td>'s in a list. Then we can make a dataframe
        # out of that
        listofdicts=[]
        for row in trlist:
            the_row=[]
            for td in row.findAll('td'):
                the_row.append(td.text)
            od = co.OrderedDict(zip(header, the_row))
            listofdicts.append(od)
        
        df = pd.DataFrame(listofdicts)
        df = df.drop(df.index[0])
        df['Year']=year
        df = df[['Team','Year','Payroll']]
        finaldf = pd.concat([finaldf,df])
        
    finaldf['Payroll'] = finaldf['Payroll'].str.replace('$','')
    finaldf['Payroll'] = finaldf['Payroll'].str.replace(',','')
    finaldf['Payroll'] = pd.to_numeric(finaldf['Payroll'])
    return(finaldf)
    
 '''