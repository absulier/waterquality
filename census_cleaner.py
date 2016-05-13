import pandas as pd

df = pd.read_csv("censusdem.csv")

county,total,white,black,native,asian,islander,twoplus=[],[],[],[],[],[],[],[]
df= df.drop(['Unnamed: 1'], axis=1)
df.columns=['county','total','white','black','native','asian','islander','twoplus']
df
