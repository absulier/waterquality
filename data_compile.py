import pandas as pd

vio=pd.read_csv('../violations.csv',low_memory=False)
census=pd.read_csv('../census.csv',low_memory=False)
ab=pd.read_csv('states.csv')

census.head()
census.head()
ab.set_index(ab.state).drop('state',axis=1)
census=census.merge(ab,how='outer',on='state')
census.state=census.initial
census=census.drop('initial',axis=1)
census=census.head(3221)

lower=lambda x: x.lower()

census.county=census.county.apply(lower)
census.head()
vio.county=vio.county.apply(lower)
vio=vio.merge(census,how='left',on=['state','county']).reset_index(drop=True)

pd.DataFrame.to_csv(vio,"../vio_full.csv")
