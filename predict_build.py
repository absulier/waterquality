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

#dropping redundant demographic income information
df=df.drop(['10Kdown','10K15K','15K20K','20K25K','25K30K','30K35K','35K40K','40K45K',
        '45K50K','50K60K','60K75K','75K100K','100K125K','125K150K','150K200K','200Kup'],axis=1)

#dropping redudant demographic race information
df=df.drop(['white','black','native','asian','islander','twoplus','hispanic'],axis=1)

per_lowincome=[]
for i in df.index:
    per_lowincome.append(df.per_10Kdown[i]+df.per_10K15K[i]+df.per_15K20K[i]+df.per_20K25K[i])
df['per_lowincome']=per_lowincome

per_highincome=[]
for i in df.index:
    per_highincome.append(df.per_100K125K[i]+df.per_125K150K[i]+df.per_150K200K[i]+df.per_200Kup[i])
df['per_highincome']=per_highincome

#drop seperate categories of income data, now reduced to just low income/highincome
df=df.drop(['per_10Kdown','per_10K15K','per_15K20K','per_20K25K','per_25K30K','per_30K35K','per_35K40K','per_40K45K',
        'per_45K50K','per_50K60K','per_60K75K','per_75K100K','per_100K125K','per_125K150K','per_150K200K','per_200Kup',
        'total_inc'],
        axis=1)

# #blocked out because appears to be less effective then having race data
# #figures out a 'percentage' of individuals who are not part of the
# #racial majority of the county. does this because overall, more diverse counties
# #were shown to have higher problems with water violations across races
# #Note: due to the way the census counts hispanics, hispanic indivuals are double counted
# #so the 'percentage not in the majority' isn't techniqually correct and may be over 100%
# per_diverse=[]
# for i in df.index:
#     perc=[df.per_white[i],df.per_black[i],df.per_native[i],df.per_asian[i],
#     df.per_islander[i],df.per_twoplus[i],df.per_hispanic[i]]
#     perc.sort()
#     perc=perc[0:6]
#     diverse=sum(perc)
#     per_diverse.append(diverse)
#
# df['per_diverse']=per_diverse
#
# df=df.drop(['per_white','per_black','per_native','per_asian','per_islander',
#             'per_twoplus','per_hispanic'],axis=1)
#
df=df.rename(columns={'total_dem':'county_pop'})

#print predict csv
pd.DataFrame.to_csv(df,'../predict2016.csv',index=False)
