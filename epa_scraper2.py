#Set up environment
import urllib
import pandas as pd
from bs4 import BeautifulSoup
from sys import setrecursionlimit as srl
srl(500000)

#Make sure to change which df you are reading each time a new chunk is run
sdwis=pd.read_csv('df9.csv')
#function takes an index from the dataframe of water treatment plants
#uses that index to find the wid and link to page on violations
#creats two dataframes of health violations and reporting violations
def viodata(index):
    #creating the soup and gathering wid
    wid=sdwis.wid[index]
    url ='https:' + sdwis.links[index]
    page=urllib.urlopen(url).read()
    soup = BeautifulSoup(page, "html.parser")

    #goes into the page and finds the tables of health and reporting violations
    allhvio=[]
    allmrvio=[]
    for table in soup.findAll('table', {'class':'result2'}):
        count=0
        for item in table.findAll('th'):
            count+=1
        if count == 6: #checks if table is a health violation
            hvio=[wid]
            for item in table.findAll('td'):
                hvio.append(item.renderContents()) #builds a list of all data for that violation
            allhvio.append(hvio) #builds list of lists of all violations and their data
        if count == 5: #checks if table is a reporting violation
            mrvio=[wid]
            for item in table.findAll('td'):
                mrvio.append(item.renderContents())
            allmrvio.append(mrvio)

    #builds dataframe from teh lists of lists generated,
    dfh=pd.DataFrame(allhvio,columns=['wid','vio_type','date_begin','date_end','water_rule','analytics','vio_id'])
    dfmr=pd.DataFrame(allmrvio,columns=['wid','vio_type','date_begin','date_end','water_rule','vio_id'])

    return dfh,dfmr

allhealth=pd.DataFrame(columns=['wid','vio_type','date_begin','date_end','water_rule','analytics','vio_id'])
allreporting=pd.DataFrame(columns=['wid','vio_type','date_begin','date_end','water_rule','vio_id'])

for i in sdwis.index:
    print i
    health,reporting=viodata(i)
    allhealth=pd.concat([allhealth,health])
    allreporting=pd.concat([allreporting,reporting])

#Make sure to change the dataframe each time you run a new chunk so that you
#dont override
pd.DataFrame.to_csv(allhealth,"health_violations9.csv")
pd.DataFrame.to_csv(allreporting,"reporting_violations9.csv")
