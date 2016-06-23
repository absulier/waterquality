import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
import math

#Reads in violations
df=pd.read_csv('../vio_org.csv')
df=df[df['2016h']!=1][df['2016r']!=1]
df=df.drop(['2016r','2016h'],axis=1)

#Reads in all wids and creates an 'ghost' violation for each facility
#This way, facilities with no violations will still show up in final dataframe,
#but as having no violations
allwid=pd.read_csv('EPA/sdwis_clean.csv').drop(['Unnamed: 0','links','city'],axis=1)
extracol=['length','analytics','lead','e_coli','coliform',
    '2006r','2007r','2008r','2009r','2010r','2011r','2012r','2013r','2014r','unknown/oldr',
    '2006h','2007h','2008h','2009h','2010h','2011h','2012h','2013h','2014h','unknown/oldh']
for i in extracol:
    allwid[i]=np.zeros(len(allwid))

#puts the dfs together
df=pd.concat([df,allwid])

#cleans up the wid column
dropper= lambda x : x.replace('<c ="" enter="">','' ).replace('</c>' ,'')
df.wid=df.wid.apply(dropper)

#turns zeros to nan so that they dont effect means
def tonan(x):
    if x==0:
        return np.nan
    else:
        return x
df.length=df.length.apply(tonan)
df.analytics=df.analytics.apply(tonan)

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
                '2015r':np.sum,
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

#reorganize columns
df=df[['wid','state','county','population','watertype','length','analytics',
    'lead','e_coli','coliform',
    '2006r','2007r','2008r','2009r','2010r','2011r','2012r','2013r','2014r','2015r','unknown/oldr',
    '2006h','2007h','2008h','2009h','2010h','2011h','2012h','2013h','2014h','2015h','unknown/oldh']]

#adding 2006 to old counts, since model will only be trained on past 9 years
oldsumh,oldsumr=[],[]
for i in df.index:
    oldsumh.append(df['2006h'][i]+df['unknown/oldh'][i])
    oldsumr.append(df['2006r'][i]+df['unknown/oldr'][i])
df['unknown/oldh']=oldsumh
df['unknown/oldr']=oldsumr
df=df.drop(['2006h','2006r'],axis=1)

#rename columns
df.columns=[['wid','state','county','population','watertype','length','analytics',
    'lead','e_coli','coliform',
    '9r','8r','7r','6r','5r','4r','3r','2r','1r','unknown/oldr',
    '9h','8h','7h','6h','5h','4h','3h','2h','1h','unknown/oldh']]

#merge in census
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
#merge onto df
df=df.merge(cen,how='left',on=['state','county'])
#fix georgia point
def to_int(x):
    if isinstance(x,str):
        if 'GA' in x:
            return 0
        else:
            return int(x)
    else:
        return int(x)
df.population=df.population.apply(to_int)

#get score for watertype
waterscore = pd.read_csv('watertype_score.csv')
df.watertype=df.merge(waterscore,on='watertype',how='left')['2015h']

#Turns nan back to zero
def tozero(x):
    if pd.isnull(x):
        return 0
    else:
        return x
for i in df.columns:
    df[i]=df[i].apply(tozero)

#print predict csv
pd.DataFrame.to_csv(df,'../predict2016.csv',index=False)
