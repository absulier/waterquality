#Set up environment
import urllib
import pandas as pd
from bs4 import BeautifulSoup

#reading page with map of states
url = 'https://www.census.gov/popest/data/counties/asrh/2014/PEPSR6H.html'
page=urllib.urlopen(url).read()
soup = BeautifulSoup(page, "html.parser")

#Building a database with states and links
states,links=[],[]
for state in soup.findAll('td',{'class':'rowName2'}):
    for link in state:
        links.append(state.find('a')['href'])
        states.append(state.find('a').renderContents() )

df= pd.DataFrame()
df['state']=states
df['url']=links

df.head()
