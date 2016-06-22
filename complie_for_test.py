import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np

#read in data (drop unecessary columns, drop 2016 because tryin w/ test for 2015)
#also wont need the reporting violations for 2015
df=pd.read_csv('vio_org.csv').drop(['wid','2016h','2016r','2015r'],axis=1).dropna()

#turn 2015 into a binary for testing
_2015=[]
for i in df['2015h']:
    if i >0:
        _2015.append(1)
    else:
        _2015.append(0)
df['2015h']=_2015

#builds a score for watertype
df2 = df.groupby(by=["watertype"], as_index=False)
df2 = df2.agg({'2015h': np.mean,})
df.watertype=df.merge(df2,on='watertype',how='left')['2015h_y']

#strange 'GA' data point needs to be changed, and strings need to be turned to ints
def to_int(x):
    if isinstance(x,str):
        if 'GA' in x:
            return 0
        else:
            return int(x)
    else:
        return int(x)
df.population=df.population.apply(to_int)
#lower case county
df.county=df.county.apply(lambda x : x.lower())

#reads in census data
cen=pd.read_csv('../census.csv')
#reads in state initial key
state=pd.read_csv('states.csv')
#merges in the key onto the census data so it can be joinged with violations
cen.state=cen.merge(state,how='left',on='state').initial
#lower case county
cen.county=cen.county.apply(lambda x : x.lower())

df=df.merge(cen,how='left',on=['state','county'])

def nan_to_0 (x):
    if pd.isnull(x):
        return 0
    else:
        return x

for x in df.columns:
    df[x]=df[x].apply(nan_to_0)

pd.DataFrame.to_csv(df, '../fulltest_w_census.csv',index=False)
