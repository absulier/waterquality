import pandas as pd
sdwis=pd.read_csv('sdwis.csv')
sdwis=sdwis.drop(['Unnamed: 0'], axis=1)

#Worked for most part, but had to manually enter link for TX183007

for i in sdwis.index:
    sdwis.wid[i]=sdwis.wid[i].replace('1f41','').replace('\r\n','')
    sdwis.links[i]=sdwis.links[i].replace('1f41','').replace('\r\n','')
    sdwis.county[i]=sdwis.county[i].replace('1f41','').replace('\r\n','')
    sdwis.city[i]=sdwis.city[i].replace('1f41','').replace('\r\n','')
    sdwis.state[i]=sdwis.state[i].replace('1f41','').replace('\r\n','')
    sdwis.population[i]=sdwis.population[i].replace('1f41','').replace('\r\n','')
    sdwis.watertype[i]=sdwis.watertype[i].replace('1f41','').replace('\r\n','')

pd.DataFrame.to_csv(sdwis,"sdwis_clean.csv")
