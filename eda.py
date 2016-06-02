import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
%matplotlib inline

df=pd.read_csv('vio_full.csv',low_memory=False).drop('Unnamed: 0',axis=1)

df.columns

df2 = df[df.vio_class=='health'].groupby(by=["wid"], as_index=False)
df2 = df2.agg({'vio_class': np.count_nonzero,
                'per_black':lambda x: x.iloc[0],
                'per_white':lambda x: x.iloc[0],
                'per_native':lambda x: x.iloc[0],
                'per_asian':lambda x: x.iloc[0],
                'per_islander':lambda x: x.iloc[0],
                'per_twoplus':lambda x: x.iloc[0],
                'per_hispanic':lambda x: x.iloc[0],
                'per_10Kdown':lambda x: x.iloc[0],
                'per_200Kup':lambda x: x.iloc[0]
                }).dropna()

df2
y=df2.vio_class
y.mean()
y.median()

x=df2.per_200Kup
fit = np.polyfit(x, y, deg=1)
plt.plot(x, fit[0] * x + fit[1], color='red')
#plt.scatter(x, y)
plt.show()
