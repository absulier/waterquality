import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np

#read in data (drop unecessary columns, drop 2016 because tryin w/ test for 2015)
#also wont need the reporting violations for 2015
df=pd.read_csv('../vio_org.csv').drop(['2016h','2016r','2015r'],axis=1).dropna()

#Agrregates into wid
df = df.groupby(by=["wid"], as_index=False)
df = df.agg({'state':lambda x: x.iloc[0],
                'county':lambda x: x.iloc[0],
                'population':lambda x: x.iloc[0],
                'watertype':lambda x: x.iloc[0],
                'length':np.mean,
                'analytics':np.mean,
                'lead':np.sum,
                'e_coli':np.sum,
                'coliform':np.sum,
                '2006r':np.sum,
                '2007r':np.sum,
                '2008r':np.sum,
                '2009r':np.sum,
                '2010r':np.sum,
                '2011r':np.sum,
                '2012r':np.sum,
                '2013r':np.sum,
                '2014r':np.sum,
                'unknown/oldr':np.sum,
                '2006h':np.sum,
                '2007h':np.sum,
                '2008h':np.sum,
                '2009h':np.sum,
                '2010h':np.sum,
                '2011h':np.sum,
                '2012h':np.sum,
                '2013h':np.sum,
                '2014h':np.sum,
                '2015h':np.sum,
                'unknown/oldh':np.sum })

df=df[['wid','state','county','population','watertype','length','analytics',
    'lead','e_coli','coliform',
    '2006r','2007r','2008r','2009r','2010r','2011r','2012r','2013r','2014r',
    'unknown/oldr',
    '2006h','2007h','2008h','2009h','2010h','2011h','2012h','2013h','2014h',
    '2015h','unknown/oldh']]

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
