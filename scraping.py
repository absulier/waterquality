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

#uses a base url for each state but with the individual state abbreviation taken out
#builds a url for each state in the database of states and abrreviations
#and puts them into the database
start = "https://oaspub.epa.gov/enviro/sdw_query_v3.get_list?wsys_name=&fac_search=fac_beginning&fac_county=&fac_city=&pop_serv=500&pop_serv=3300&pop_serv=10000&pop_serv=100000&pop_serv=100001&sys_status=active&pop_serv=&wsys_id=&fac_state="
end = "&last_fac_name=&page=1&query_results=&total_rows_found="
url = []
for i in df['initial']:
    url.append(start + i + end)
df['url']=url


#Goes to a state and pulls information on each water treatment  facility
#just goes to first state in database for now
url=df['url'][0]

#reads url for the state that has list of treatment plants
page=urllib.urlopen(url).read()
soup = BeautifulSoup(page, "html.parser")

#creates a list of info for each treatment plant, info still needs to be parsed
plants=[]
for item in soup.find('table').findAll('tr'):
    plants.append(item.findAll('td'))
#plants list has one item that doesnt contain info, so just delete it
del plants[0]

#parses information and places the info into lists
links,county,city,population,watertype,activity,wid,state= [],[],[],[],[],[],[],[]
for i in plants:
    links.append ( (i[0].find('a')['href']) )
    county.append( (i[1].renderContents()) )
    city.append ( (i[2].renderContents()) )
    population.append( (i[3].renderContents()) )
    watertype.append( (i[4].renderContents()) )
    activity.append( (i[5].renderContents()) )
    wid.append ( (i[6].renderContents().replace('<center>','').replace('</center>','')) )
    state.append('STATE')

#puts those lists into a dataframe
df2 = pd.DataFrame()
df2['wid']=wid
df2['links']=links
df2['county']=county
df2['city']=city
df2['state']=state
df2['population']=population
df2['watertype']=watertype
df2['activity']=activity

df2
