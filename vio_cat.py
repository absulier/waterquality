import pandas as pd

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

drop=lambda x : x.replace('<br/>','')

health_violations=health_violations.dropna()
reporting_violations=reporting_violations.dropna()

for column in health_violations.columns:
    health_violations[column]=health_violations[column].apply(drop)

for column in reporting_violations.columns:
    reporting_violations[column]=reporting_violations[column].apply(drop)
