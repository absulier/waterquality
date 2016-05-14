#Set up environment
import urllib
import pandas as pd
from bs4 import BeautifulSoup

#creating the soup
url = 'https://oaspub.epa.gov/enviro/sdw_report_v3.first_table?pws_id=DC0000007&state=DC&source=Surface%20water%20purchased&population=12499&sys_num=0'
page=urllib.urlopen(url).read()
soup = BeautifulSoup(page, "html.parser")

#goes into the page and fund the tables of health related violations
allhvio=[]
allmrvio=[]
for table in soup.findAll('table', {'class':'result2'}):
    count=0
    for item in table.findAll('th'):
        count+=1
    if count == 6:
        hvio=[]
        for item in table.findAll('td'):
            hvio.append(item.renderContents())
        allhvio.append(hvio)
    if count == 5:
        mrvio=[]
        for item in table.findAll('td'):
            mrvio.append(item.renderContents())
        allmrvio.append(mrvio)

dfh=pd.DataFrame(allhvio,columns=['vio_type','date_begin','date_end','water_rule','analytics','vio_id'])
dfmr=pd.DataFrame(allmrvio,columns=['vio_type','date_begin','date_end','water_rule','vio_id'])
