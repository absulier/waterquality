import pandas as pd
from datetime import datetime

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
date=df[['date_begin','date_end']]

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

date.head()
len(date)

months=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC']
num=[1,2,3,4,5,6,7,8,9,10,11,12]
conve=pd.DataFrame({'months':months,'num':num})

date['y_b']=y_b
date['months']=m_b
date=date.merge(conve, how='left', on='months').drop('months',axis=1)
date=date.rename(columns={'num':'m_b'})
date['d_b']=d_b

date['y_e']=y_e
date['months']=m_e
date=date.merge(conve, how='left', on='months').drop('months',axis=1)
date=date.rename(columns={'num':'m_e'})
date['d_e']=d_e

length=[]
for i in date.index:
    if len(date.y_b[i])==4 and len(date.y_e[i])==4:
        start=datetime(int(date.y_b[i]),int(date.m_b[i]),int(date.d_b[i]))
        end=datetime(int(date.y_e[i]),int(date.m_e[i]),int(date.d_e[i]))
        gap=end-start
        length.append(gap.days)
    else:
        length.append('---')

df['length_days']=length
