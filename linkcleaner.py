import pandas as pd
sdwis=pd.read_csv('sdwis.csv')
sdwis.links[2164]

for index in sdwis.index:
    print index
    sdwis.links[index]=sdwis.links[index].replace('e\r\n1f41\r\npa','epa')

sdwis.links[2164]
