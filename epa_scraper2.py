#Set up environment
import urllib
import pandas as pd
from bs4 import BeautifulSoup

#creating the soup
url = 'https://oaspub.epa.gov/enviro/sdw_report_v3.first_table?pws_id=DC0000007&state=DC&source=Surface%20water%20purchased&population=12499&sys_num=0'
page=urllib.urlopen(url).read()
soup = BeautifulSoup(page, "html.parser")

#goes into the page and fund the tables of health related violations 
for table in soup.findAll('table', {'class':'result2'}):
    count=0
    for item in table.findAll('th'):
        count+=1
    if count == 6:
        print table
        print "======"


    #for item in table.findAll('td'):
    #    print item
