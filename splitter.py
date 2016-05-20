import pandas as pd
from sklearn.cross_validation import train_test_split as tts



df,df1=tts(df,train_size=.9)
df,df2=tts(df, train_size=.89)
df,df3=tts(df, train_size=.88)
df,df4=tts(df, train_size=.86)
df,df5=tts(df, train_size=.83)
df,df6=tts(df, train_size=.8)
df,df7=tts(df, train_size=.75)
df,df8=tts(df, train_size=.66)
df10,df9=tts(df,train_size=.5)
