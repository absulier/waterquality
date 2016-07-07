import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)
import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve as skrc
from sklearn.metrics import auc
from sklearn.lda import LDA
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, BaggingClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.metrics import confusion_matrix
from sklearn.cross_validation import cross_val_score
from sklearn.cross_validation import train_test_split
import matplotlib.pyplot as plt
%matplotlib inline

df=pd.read_csv('../traintest2015.csv').drop(['state','county','wid',
                '9r','8r','7r','6r','9h','8h','7h','6h',
                'unknown/oldh','unknown/oldr'],axis=1)

train,test=train_test_split(df,train_size=.9)
y_train=train['2015h']
x_train=train.drop('2015h',axis=1)
y_test=test['2015h']
x_test=test.drop('2015h',axis=1)

#Gradient Boosting Accuracy (Competitive for best depending on features)
#exponential loss performs slightly better
gb = GradientBoostingClassifier(loss='exponential')
gb.fit(x_train,y_train)
gb.score(x_test,y_test)
proba=pd.DataFrame(gb.predict_proba(x_test))[1]
false_positive_rate, true_positive_rate, thresholds = skrc(y_test,proba)
auc(false_positive_rate, true_positive_rate)

#GB significantly outperforms other models, get average AUC score
aucs=[]
for i in range(12):
    train,test=train_test_split(df,train_size=.9)
    y_train=train['2015h']
    x_train=train.drop('2015h',axis=1)
    y_test=test['2015h']
    x_test=test.drop('2015h',axis=1)
    gb.fit(x_train,y_train)
    gb.score(x_test,y_test)
    proba=pd.DataFrame(gb.predict_proba(x_test))[1]
    false_positive_rate, true_positive_rate, thresholds = skrc(y_test,proba)
    aucs.append(auc(false_positive_rate, true_positive_rate))
    print i
np.mean(aucs)

#check that accuracy is better than base
float(len(df[df['2015h']==0]))/float(len(df))
np.mean(cross_val_score(gb,test.drop('2015h',axis=1),test['2015h'],cv=12))

#train final model on all data
gb.fit(test.drop('2015h',axis=1),test['2015h'])

#load in new data
to_predict=pd.read_csv('../predict2016.csv').drop(['state','county','wid',
                '9r','8r','7r','6r','9h','8h','7h','6h',
                'unknown/oldh','unknown/oldr'],axis=1)

#see how many violations happened in 2015
sum(df['2015h'])

#make predictions
probs=gb.predict_proba(to_predict)
proba=pd.DataFrame(probs)[1]
proba.mean()

#play with the predication threshold to see falsenegative/positive trade off
y_pred=[]
for i in proba:
    if i>.1:
        y_pred.append(1)
    else:
        y_pred.append(0)

sum(y_pred)

predictions=pd.read_csv('../predict2016.csv')[['wid','state','county']]
predictions['prediction']=y_pred
predictions['probability']=proba
pd.DataFrame.to_csv(predictions,'predictions.csv',index=False)
predictions 
