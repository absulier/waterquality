import pandas as pd
import re

df1=pd.read_csv('health_violations1.csv')
df2=pd.read_csv('health_violations2.csv')
df3=pd.read_csv('health_violations3.csv')
df4=pd.read_csv('health_violations4.csv')
df5=pd.read_csv('health_violations5.csv')
df6=pd.read_csv('health_violations6.csv')
df7=pd.read_csv('health_violations7.csv')
df8=pd.read_csv('health_violations8.csv')
df9=pd.read_csv('health_violations9.csv')
df10=pd.read_csv('health_violations10.csv')
health_violations=pd.concat([df1,df2,df3,df4,df5,df6,df7,df8,df9,df10])
health_violations=health_violations.drop("Unnamed: 0",axis=1)

df1=pd.read_csv('reporting_violations1.csv')
df2=pd.read_csv('reporting_violations2.csv')
df3=pd.read_csv('reporting_violations3.csv')
df4=pd.read_csv('reporting_violations4.csv')
df5=pd.read_csv('reporting_violations5.csv')
df6=pd.read_csv('reporting_violations6.csv')
df7=pd.read_csv('reporting_violations7.csv')
df8=pd.read_csv('reporting_violations8.csv')
df9=pd.read_csv('reporting_violations9.csv')
df10=pd.read_csv('reporting_violations10.csv')
reporting_violations=pd.concat([df1,df2,df3,df4,df5,df6,df7,df8,df9,df10])
reporting_violations=reporting_violations.drop("Unnamed: 0",axis=1)

drop=lambda x : re.sub('<.*?>', '', x.replace('<br/>','').replace('1f41','').replace('\r\n',''))

health_violations=health_violations.dropna()
reporting_violations=reporting_violations.dropna()

for column in health_violations.columns:
    health_violations[column]=health_violations[column].apply(drop)

for column in reporting_violations.columns:
    reporting_violations[column]=reporting_violations[column].apply(drop)

health_violations=health_violations.reset_index(drop=True)
reporting_violations=reporting_violations.reset_index(drop=True)

#Adding empty analytics column to reporting so that it can be added to health
analytics=[]
for i in range(len(reporting_violations)):
    analytics.append('---')
reporting_violations['analytics']=analytics

vio_class=[]
for i in range(len(reporting_violations)):
    vio_class.append('reporting')
reporting_violations['vio_class']=vio_class

vio_class=[]
for i in range(len(health_violations)):
    vio_class.append('health')
health_violations['vio_class']=vio_class

violations=pd.concat([health_violations,reporting_violations]).reset_index(drop=True)

sdwis=pd.read_csv('sdwis_clean.csv').drop(['Unnamed: 0','links'],axis=1)

drop=lambda x : re.sub('<.*?>', '', str(x).replace('<br/>','').replace('1f41','').replace('\r\n',''))

for column in sdwis.columns:
    sdwis[column]=sdwis[column].apply(drop)

violations.head()
sdwis.head()
len(violations)
len(sdwis)
len(violations.drop_duplicates())
violations=violations.merge(sdwis,how='outer',on='wid').drop_duplicates().reset_index(drop=True)

pd.DataFrame.to_csv(violations,"../../violations.csv",index=False)
