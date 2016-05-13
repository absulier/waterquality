#Set up environment
import urllib
import pandas as pd
from bs4 import BeautifulSoup

#reading page with map of states
url = 'https://www3.epa.gov/enviro/facts/sdwis/search.html'
page=urllib.urlopen(url).read()
soup = BeautifulSoup(page, "html.parser")

#Building a database with states and abbreviation
name=[]
initial=[]
for state in soup.findAll('map',{'name':'state_test'}):
    for state2 in state.findAll('area'):
        name.append(state2['alt'])
        initial.append(state2['href'][59:61])
df= pd.DataFrame()
df['name']=name
df['initial']=initial
