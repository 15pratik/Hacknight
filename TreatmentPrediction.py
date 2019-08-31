# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 20:15:51 2019

@author: H295088
"""

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix 
from sklearn.metrics import accuracy_score 
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn import metrics
import numpy as np

dataset = pd.read_csv(r'C:\Users\H295088\Downloads\trainms.csv',parse_dates=['Timestamp'],index_col='s.no')
dataset = dataset.drop(['Timestamp'],axis=1)

dataset= dataset.replace(np.nan, '', regex=True)
#dataset.dropna(inplace=True)

y = dataset.treatment
x = dataset.drop('treatment',axis=1)

#labeling
idx = 0
for col in x.columns:
    label_encoder = LabelEncoder()
    print("{} {}".format(idx, col))
    idx += 1
    x[col]=label_encoder.fit_transform(x[col])
    
#logreg = LogisticRegression()
#
## 3. fit 
#logreg.fit(x, y)

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2)

#x_train.head()
#x_train.shape
#x_test.head()
#x_test.shape

trained_model = RandomForestClassifier().fit(x,y)

y_pred = trained_model.predict(x_test)

confusion_matrix(y_test,y_pred)
accuracy_score(y_test,y_pred)
a=trained_model.feature_importances_
print(a)

#report = metrics.classification_report(y_test, y_pred, output_dict=True)
#
#df = dp.DataFrame(report).transpose()

print(np.amax(a))
print(np.amin(a))
result = np.where(a==np.amin(a))
print(result)
#print(metrics.classification_report(y_test,y_pred))
