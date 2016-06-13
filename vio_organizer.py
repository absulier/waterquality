import pandas as pd

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
