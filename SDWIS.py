from bs4 import BeautifulSoup
import urllib
r1 = urllib.urlopen('https://www3.epa.gov/enviro/facts/sdwis/search.html')
soup1 = BeautifulSoup(r1, 'lxml')
a1 = soup1.find_all('a')

states=[]

for item in a1:
    i=str(item)
    if 'state_abbr' in i:
        states.append(i[68:70])

del states[0]

def getsdwis (state):
    print state
    first = 'https://oaspub.epa.gov/enviro/sdw_query_v3.get_list?wsys_name=&fac_search=fac_beginning&fac_county=&fac_city=&pop_serv=500&pop_serv=3300&pop_serv=10000&pop_serv=100000&pop_serv=100001&sys_status=active&pop_serv=&wsys_id=&fac_state='
    state = state
    second = '&last_fac_name=&page=1&query_results=&total_rows_found='

    source = first + state + second

    r2 = urllib.urlopen(source)
    soup2 = BeautifulSoup(r2, 'lxml')
    a2 = soup2.find_all('a')

    links=[]
    switch='off'

    for item in a2:
        i=str(item)
        if switch == 'on' and i != '<a href="//oaspub.epa.gov/enviro/EF_METADATA_HTML.sdwis_page?p_column_name=PWS_NAME" scope="col">Water System Name</a>':
            links.append(i)
        elif switch == 'off' and i== '<a href="//oaspub.epa.gov/enviro/EF_METADATA_HTML.sdwis_page?p_column_name=PWSID" scope="col">Water System ID</a>':
            switch = 'on'
        elif switch == 'on' and i == '<a href="//oaspub.epa.gov/enviro/EF_METADATA_HTML.sdwis_page?p_column_name=PWS_NAME" scope="col">Water System Name</a>':
            switch = 'off for good'

    linksclean=[]
    for string in links:
        link='http:'
        switch='off'
        for i in string:
            if switch == 'on' and i != '"':
                link+=i
            elif switch == 'off' and i== '"':
                switch = 'on'
            elif switch == 'on' and i == '"':
                switch = 'off for good'
        linksclean.append(link)
    return linksclean

sdwisus=[]
for item in states:
    sdwisus+=getsdwis(item)

import pandas as pd
df = pd.DataFrame()
print "Aggregating DataFrame"
df['sdwsis']=sdwisus
print "Exporting DataFrame"
pd.DataFrame.to_csv(df,"SDWISUS_US.csv")
