import pandas as pd
import numpy as np
from datetime import datetime
import math
import warnings
warnings.filterwarnings("ignore")

df=pd.read_csv('../violations.csv', low_memory=False)

#Clean up begin date
begin_date=[]
for i in df.date_begin:
    if isinstance(i,str):
        begin_date.append(i)
    else:
        begin_date.append('---')
df.date_begin=begin_date

#clean up end date
end_date=[]
for i in df.date_end:
    if isinstance(i,str):
        end_date.append(i)
    else:
        end_date.append('---')
df.date_end=end_date

#gets list of just the years from the date the violation began
year=[]
for i in df.date_begin:
    if isinstance(i,str):
        year.append(i[-4:])
    else:
        year.append('--')

#If violation happened in 2006 or after, that year is saved to new list
#otherwised marked old
years=['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016']
years_recent=[]
for i in year:
    if i in years:
        years_recent.append(i)
    else:
        years_recent.append('old')

#builds new data frame of these years for past decade. Turns into dummy variables
#renames columns for clarity and merges with original dataframe
df2=pd.DataFrame({'year':years_recent})
df2=pd.get_dummies(df2)
df2.columns=['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','unknown/old']
df=df.merge(df2, left_index=True, right_index=True)

#drops incomplete information
df=df.dropna()

#reads through info on violations and check if they are related to lead, e coli,
#or coliforms, creates list of dummy variables for them.
lead=[]
for i in df.index:
    if 'lead' in df.vio_type[i].lower() or 'lead' in df.water_rule[i].lower():
        lead.append(1)
    else:
        lead.append(0)
ecoli=[]
for i in df.index:
    if 'e. coli' in df.vio_type[i].lower() or 'e. coli' in df.water_rule[i].lower():
        ecoli.append(1)
    else:
        ecoli.append(0)
coliform=[]
for i in df.index:
    if 'coliform' in df.vio_type[i].lower() or 'coliform' in df.water_rule[i].lower():
        coliform.append(1)
    else:
        coliform.append(0)

#reads in dummy variable lists to df
df['lead']=lead
df['e_coli']=ecoli
df['coliform']=coliform

#working with dates
#builds a database to hold data information
date=df[['date_begin','date_end']]

#parses out the string into year, month, and day
y_b=[]
m_b=[]
d_b=[]
for i in date.date_begin:
    if len(i)==11:
        y_b.append(i[-4:])
        m_b.append(i[0:3])
        d_b.append(i[4:6])
    else:
        y_b.append('---')
        m_b.append('---')
        d_b.append('---')

#does the same parse, but for the end date
y_e=[]
m_e=[]
d_e=[]
for i in date.date_end:
    if len(i)==11:
        y_e.append(i[-4:])
        m_e.append(i[0:3])
        d_e.append(i[4:6])
    else:
        y_e.append('---')
        m_e.append('---')
        d_e.append('---')

#builds a new data frame so to convert months to numbers
months=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
num=[1,2,3,4,5,6,7,8,9,10,11,12]
conve=pd.DataFrame({'months':months,'num':num})

#puts the year and month into data frame, then merges numbers for month,
#then drops the non numeric month, then adds days
date['y_b']=y_b
date['months']=m_b
date=date.merge(conve, how='left', on='months').drop('months',axis=1)
date=date.rename(columns={'num':'m_b'})
date['d_b']=d_b

#repeats for end dates
date['y_e']=y_e
date['months']=m_e
date=date.merge(conve, how='left', on='months').drop('months',axis=1)
date=date.rename(columns={'num':'m_e'})
date['d_e']=d_e

#finds the lengths of violations, puts that into dataframe,
#then deletes date and other variables that were used to construct features
length=[]
for i in date.index:
    if len(date.y_b[i])==4 and len(date.y_e[i])==4:
        start=datetime(int(date.y_b[i]),int(date.m_b[i]),int(date.d_b[i]))
        end=datetime(int(date.y_e[i]),int(date.m_e[i]),int(date.d_e[i]))
        gap=end-start
        length.append(gap.days)
    else:
        length.append('---')
df['length']=length
df=df.drop(['date_begin','date_end','vio_id','city','vio_type','water_rule'],axis=1)
df=df.merge(pd.get_dummies(df.vio_class),how='left',left_index=True,right_index=True).drop('vio_class',axis=1)

#gets rid of '---' and turns into NaN so we can reorganize
def to_nan(x):
    if x == '---':
        return np.nan
    else:
        return x
for i in df.columns:
    df[i]=df[i].apply(to_nan)

#turns all analytics values to floats
to_float = lambda x : float(x)
df.analytics=df.analytics.apply(to_float)

#seperating out health and reporting violations
dfhealth=df[['health','2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','unknown/old']]
#health
dfh=dfhealth[dfhealth['health']==1].drop('health',axis=1)
dfh.columns=['2006h','2007h','2008h','2009h','2010h','2011h','2012h','2013h','2014h','2015h','2016h','unknown/oldh']
df=df.merge(dfh, how='left', left_index=True, right_index=True)

#reporting
dfr=dfhealth[dfhealth['health']==0].drop('health',axis=1)
dfr.columns=['2006r','2007r','2008r','2009r','2010r','2011r','2012r','2013r','2014r','2015r','2016r','unknown/oldr']
df=df.merge(dfr, how='left', left_index=True, right_index=True)

#get rid of original years column
df=df.drop(['2006','2007','2008','2009','2010','2011','2012','2013','2014','2015','2016','unknown/old'],axis=1)

#Drop null values
def nan_0(x):
    if isinstance(x,float):
        if math.isnan(x):
            return 0
        else:
            return x
    else:
        return x

for i in df.columns:
    df[i]=df[i].apply(nan_0)

#reorder columns
df=df[['wid','state','county','population','watertype','length','analytics',
    'lead','e_coli','coliform',
    '2006r','2007r','2008r','2009r','2010r','2011r','2012r','2013r','2014r',
    '2015r','2016r','unknown/oldr',
    '2006h','2007h','2008h','2009h','2010h','2011h','2012h','2013h','2014h',
    '2015h','2016h','unknown/oldh']]

pd.DataFrame.to_csv(df,'../vio_org.csv',index=False)
