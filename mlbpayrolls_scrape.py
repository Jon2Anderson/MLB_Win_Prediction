import pandas as pd
import os
import requests
import collections as co
from bs4 import BeautifulSoup


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
