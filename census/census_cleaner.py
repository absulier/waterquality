#set up environemnt
import pandas as pd

#read in the race dataset, rename columns
df = pd.read_csv("censusdem.csv")
df= df.drop(['Unnamed: 1'], axis=1)
df.columns=['county','total_dem','white','black','native','asian','islander','twoplus']

#reds in hispanic dataset (census counts hispanic differenly than other races, so downloaded seperately)
#merges in hispanic number
hisp=pd.read_csv('hispanic.csv')
hisp.columns=['county','hispanic']
len(df)
len(hisp)
df= df.merge(hisp, how='outer',on='county')
df=df.dropna()

#split the counties into county and state
county,state=[],[] #empty lists to put county and state into
for index in df.index: #loops through each row in the df
    ct, st = df['county'][index].split(", ") #splits the county and state names at the comma, stores county in ct and state in st
    county.append(ct)
    state.append(st)
df['county']=county
df['state']=state
for index in df.index: #deletes 'County' and extra space from county name where it appears
    df['county'][index]=df['county'][index].replace(' County', '')

#turn strings into integers
numclean =lambda x: int(x.replace(',',''))

#finds percentage of each dem out of total population
def percentage(column):
    pl=[]
    for index in df.index:
        pl.append(100*float(column[index])/float(df.total_dem[index]))
    return pl

#apply the string to integer function
df.total_dem=df.total_dem.apply(numclean)
df.white=df.white.apply(numclean)
df.black=df.black.apply(numclean)
df.native=df.native.apply(numclean)
df.asian=df.asian.apply(numclean)
df.islander=df.islander.apply(numclean)
df.twoplus=df.twoplus.apply(numclean)
df.hispanic=df.hispanic.apply(numclean)

#apply the percentage function
df['per_white']=percentage(df.white)
df['per_black']=percentage(df.black)
df['per_native']=percentage(df.native)
df['per_asian']=percentage(df.asian)
df['per_islander']=percentage(df.islander)
df['per_twoplus']=percentage(df.twoplus)
df['per_hispanic']=percentage(df.hispanic)

#read in new dataset, put in df, renames columns, drop extra rows
df2 = pd.read_csv("censusinc.csv")
df2= df2.drop(['Unnamed: 1'], axis=1)
df2.columns =['county','total_inc','10Kdown','10K15K','15K20K','20K25K','25K30K','30K35K','35K40K','40K45K','45K50K','50K60K','60K75K','75K100K','100K125K','125K150K','150K200K','200Kup']
df2 = df2.dropna()

#splits counties from states(same as above)
county,state=[],[]
for index in df2.index:
    ct, st = df2.county[index].split(", ")
    county.append(ct)
    state.append(st)
df2['county']=county
df2['state']=state
for index in df.index:
    df2['county'][index]=df2['county'][index].replace(' County', '')

#turns items into strings so we can use numclean on them
stringer =lambda x: str(x)

#turns the values into integers
cleanup=['total_inc','10Kdown','10K15K','15K20K','20K25K','25K30K','30K35K','35K40K','40K45K','45K50K','50K60K','60K75K','75K100K','100K125K','125K150K','150K200K','200Kup']
for item in cleanup:
    df2[item]=df2[item].apply(stringer)
    df2[item]=df2[item].apply(numclean)

#merges the dataframes together and prints them out!
census = df.merge(df2, how='outer',on=['state','county'])
census.columns

inc=census[['total_inc','10Kdown','10K15K','15K20K','20K25K','25K30K','30K35K','35K40K','40K45K','45K50K','50K60K','60K75K','75K100K','100K125K','125K150K','150K200K','200Kup']]


def fun_per_inc(column):
    for index in inc.index:
        inc[column][index]=100*inc[column][index]/inc.total_inc[index]


per_inc=inc.drop('total_inc',axis=1)
per_inc.columns=['per_10Kdown','per_10K15K','per_15K20K','per_20K25K','per_25K30K','per_30K35K','per_35K40K','per_40K45K','per_45K50K','per_50K60K','per_60K75K','per_75K100K','per_100K125K','per_125K150K','per_150K200K','per_200Kup']
inc
per_inc

pd.DataFrame.to_csv(census,"census.csv")
