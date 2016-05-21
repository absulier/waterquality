#File is too big to run all at once, splits file into small files so I can run
#in chunks

import pandas as pd
from sklearn.cross_validation import train_test_split as tts

df=pd.read_csv('sdwis_clean.csv')
df=df.drop(['Unnamed: 0'], axis=1)

df,df1=tts(df,train_size=.9)
df,df2=tts(df, train_size=.89)
df,df3=tts(df, train_size=.88)
df,df4=tts(df, train_size=.86)
df,df5=tts(df, train_size=.83)
df,df6=tts(df, train_size=.8)
df,df7=tts(df, train_size=.75)
df,df8=tts(df, train_size=.66)
df10,df9=tts(df,train_size=.5)


pd.DataFrame.to_csv(df1,"df1.csv")
pd.DataFrame.to_csv(df2,"df2.csv")
pd.DataFrame.to_csv(df3,"df3.csv")
pd.DataFrame.to_csv(df4,"df4.csv")
pd.DataFrame.to_csv(df5,"df5.csv")
pd.DataFrame.to_csv(df6,"df6.csv")
pd.DataFrame.to_csv(df7,"df7.csv")
pd.DataFrame.to_csv(df8,"df8.csv")
pd.DataFrame.to_csv(df9,"df9.csv")
pd.DataFrame.to_csv(df10,"df10.csv")

len(df1)
