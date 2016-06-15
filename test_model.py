import pandas as pd
import numpy as np
from sklearn.lda import LDA
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import confusion_matrix
from sklearn.cross_validation import train_test_split
import warnings
warnings.filterwarnings("ignore")

#read in data (drop unecessary columns, drop 2016 because tryin w/ test for 2015)
df=pd.read_csv('vio_org.csv').drop(['wid','state','county','2016'],axis=1)

#turn 2015 into a binary for testing
_2015=[]
for i in df['2015']:
    if i >0:
        _2015.append(1)
    else:
        _2015.append(0)
df['2015']=_2015

#builds a score for watertype
df2 = df.groupby(by=["watertype"], as_index=False)
df2 = df2.agg({'2015': np.mean,
            })
df.watertype=df.merge(df2,on='watertype',how='left')['2015_y']

#strange 'GA' data point needs to be changed, and strings need to be turned to ints
def to_int(x):
    if isinstance(x,str):
        if 'GA' in x:
            return 0
        else:
            return int(x)
    else:
        return int(x)
df.population=df.population.apply(to_int)

train,test=train_test_split(df,train_size=.9)
y_train=train['2015']
x_train=train.drop('2015',axis=1)
y_test=test['2015']
x_test=test.drop('2015',axis=1)

#LDA
lda_classifier = LDA(n_components=2)
lda_x_axis = lda_classifier.fit(x_train, y_train).transform(x_train)
lda_classifier.score(x_test, y_test, sample_weight=None)


#Look at Decision Tree Accuracy
dt = DecisionTreeClassifier(class_weight='balanced')
dt.fit(x_train,y_train)
dt.score(x_test,y_test)

#Look at Random Forest Accuracy
rf = RandomForestClassifier(class_weight='balanced')
rf.fit(x_train,y_train)
rf.score(x_test,y_test)

y_pred=rf.predict(x_test)

#(true negative) (false positive)
#(false negative) (true positive)
print confusion_matrix(y_test,y_pred)
