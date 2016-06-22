import warnings
warnings.filterwarnings("ignore")
import pandas as pd
import numpy as np
from sklearn.metrics import roc_curve as skrc
from sklearn.metrics import auc
from sklearn.lda import LDA
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, ExtraTreesClassifier, BaggingClassifier, AdaBoostClassifier, GradientBoostingClassifier
from sklearn.metrics import confusion_matrix
from sklearn.cross_validation import train_test_split
import matplotlib.pyplot as plt
%matplotlib inline

df=pd.read_csv('../fulltest_w_census.csv').drop(['state','county','2016h','2016r'],axis=1)
df.drop('wid',axis=1,inplace=True)

y=df['2015h']
X=df.drop(['2015h'],axis=1)

#build new train and test sets
train,test=train_test_split(df,train_size=.9)
y_train=train['2015h']
x_train=train.drop('2015h',axis=1)
y_test=test['2015h']
x_test=test.drop('2015h',axis=1)

#LDA Accuracy
lda_classifier = LDA(n_components=2)
lda_x_axis = lda_classifier.fit(x_train, y_train).transform(x_train)
lda_classifier.score(x_test, y_test, sample_weight=None)
#Get AUC for test
proba=pd.DataFrame(lda_classifier.predict_proba(x_test))[1]
false_positive_rate, true_positive_rate, thresholds = skrc(y_test,proba)
auc(false_positive_rate, true_positive_rate)

#Decision Tree Accuracy
dt = DecisionTreeClassifier(class_weight='balanced')
dt.fit(x_train,y_train)
dt.score(x_test,y_test)
proba=pd.DataFrame(dt.predict_proba(x_test))[1]
false_positive_rate, true_positive_rate, thresholds = skrc(y_test,proba)
auc(false_positive_rate, true_positive_rate)

#Random Forest Accuracy (okay baseline)
rf = RandomForestClassifier(class_weight='balanced')
rf.fit(x_train,y_train)
rf.score(x_test,y_test)
proba=pd.DataFrame(rf.predict_proba(x_test))[1]
false_positive_rate, true_positive_rate, thresholds = skrc(y_test,proba)
auc(false_positive_rate, true_positive_rate)

#Extra Trees Accuracy (not as good as random forest)
et = ExtraTreesClassifier(class_weight='balanced')
et.fit(x_train,y_train)
et.score(x_test,y_test)
proba=pd.DataFrame(et.predict_proba(x_test))[1]
false_positive_rate, true_positive_rate, thresholds = skrc(y_test,proba)
auc(false_positive_rate, true_positive_rate)

#Bagging Accuracy (Competitive for best depending on features)
bc = BaggingClassifier(dt)
bc.fit(x_train,y_train)
bc.score(x_test,y_test)
proba=pd.DataFrame(bc.predict_proba(x_test))[1]
false_positive_rate, true_positive_rate, thresholds = skrc(y_test,proba)
auc(false_positive_rate, true_positive_rate)

#Boosting Accuracy (worst)
#also takes too long to build model, avoid
ab = AdaBoostClassifier(dt)
ab.fit(x_train,y_train)
ab.score(x_test,y_test)
proba=pd.DataFrame(ab.predict_proba(x_test))[1]
false_positive_rate, true_positive_rate, thresholds = skrc(y_test,proba)
auc(false_positive_rate, true_positive_rate)

#Gradient Boosting Accuracy (Competitive for best depending on features)
gb = GradientBoostingClassifier()
gb.fit(x_train,y_train)
gb.score(x_test,y_test)
proba=pd.DataFrame(gb.predict_proba(x_test))[1]
false_positive_rate, true_positive_rate, thresholds = skrc(y_test,proba)
auc(false_positive_rate, true_positive_rate)

#find best features for Gradient Boost
#Feature selection based on AUC
X,X_test,y,y_test=train_test_split(X,y,train_size=.9)
model=GradientBoostingClassifier()
features=[]
scores=[]
for i in X:
    features.append(i)
    model.fit_transform(X[[i]],y)
    proba=model.predict_proba(X_test[[i]])
    proba=pd.DataFrame(proba)[1]
    false_positive_rate, true_positive_rate, thresholds = skrc(y_test,proba)
    scores.append(auc(false_positive_rate, true_positive_rate))
df_f=pd.DataFrame({'features':features, 'scores':scores})
df_f=df_f.sort_values(by='scores',ascending=False)
best=df_f.features


#Find best AUC
#build new train and test sets
train,test=train_test_split(df,train_size=.9)
y_train=train['2015h']
x_train=train.drop('2015h',axis=1)
y_test=test['2015h']
x_test=test.drop('2015h',axis=1)
model=GradientBoostingClassifier()
ran=[]
score_auc=[]
for i in range(5,len(best)):
    model.fit(x_train[best[0:i]],y_train)
    proba=pd.DataFrame(model.predict_proba(x_test[best[0:i]]))[1]
    false_positive_rate, true_positive_rate, thresholds = skrc(y_test,proba)
    ran.append(i)
    score_auc.append(auc(false_positive_rate, true_positive_rate))
    print i, auc(false_positive_rate, true_positive_rate)

print max(score_auc)
for i in range(len(ran)):
    if score_auc[i]==max(score_auc):
        print score_auc[i],ran[i]

#Construct final model
y=df['2015h']
X=df.drop(['2015h'],axis=1)
#build new train and test sets
train,test=train_test_split(df,train_size=.9)
y_train=train['2015h']
x_train=train.drop('2015h',axis=1)
y_test=test['2015h']
x_test=test.drop('2015h',axis=1)
x_train=x_train[best[0:62]]
x_test=x_test[best[0:62]]

#fit model
gb = GradientBoostingClassifier()
gb.fit(x_train,y_train)
gb.score(x_test,y_test)
proba=pd.DataFrame(gb.predict_proba(x_test))[1]
false_positive_rate, true_positive_rate, thresholds = skrc(y_test,proba)
auc(false_positive_rate, true_positive_rate)

#Construct ROC
roc_auc=auc(false_positive_rate, true_positive_rate)
fig_size = plt.rcParams["figure.figsize"]
fig_size[0] = 15
fig_size[1] = 10
plt.rcParams["figure.figsize"] = fig_size
plt.title('ROC',size=30)
plt.plot(false_positive_rate, true_positive_rate, 'r', label='AUC: %f' % roc_auc,linewidth=10)
plt.legend(loc='lower right',fontsize=20)
plt.xlabel('False Positve Rate',size=20)
plt.ylabel('True Positive Rate',size=20)
plt.show
plt.savefig('ROC.jpg')

#Construct confusion matrix (seems that best cut off is at .09)
y_pred=gb.predict(x_test)
y_pred_prob=gb.predict_proba(x_test)
proba=pd.DataFrame(y_pred_prob)[1]
proba.mean()
y_pred2=[]
for i in proba:
    if i>.105:
        y_pred2.append(1)
    else:
        y_pred2.append(0)

#(true negative) (false positive)
#(false negative) (true positive)
print confusion_matrix(y_test,y_pred2)
