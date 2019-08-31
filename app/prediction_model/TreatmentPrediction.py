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
import pickle

def fit(data_list):
    """
    This will fit the encoder for all the unique values and introduce unknown value
    :param data_list: A list of string
    :return: self
    """
    label_encoder = LabelEncoder()
    label_encoder = label_encoder.fit(list(data_list) + ['Unknown'])
    return label_encoder

def transform(label_encoder, data_list):
    """
    This will transform the data_list to id list where the new values get assigned to Unknown class
    :param data_list:
    :return:
    """
    new_data_list = list(data_list)
    for unique_item in np.unique(data_list):
        if str(unique_item) not in label_encoder.classes_:
            new_data_list = ['Unknown' if x==unique_item else x for x in new_data_list]

    return label_encoder.transform(new_data_list)

dataset = pd.read_csv(r'./app/prediction_model/trainData.csv',parse_dates=['Timestamp'],index_col='s.no')
dataset = dataset.drop(['Timestamp'],axis=1)

dataset= dataset.replace(np.nan, '', regex=True)
#dataset.dropna(inplace=True)

y = dataset.treatment
x = dataset.drop('treatment',axis=1)

print(x.shape)

#labeling
idx = 0
for col in x.columns:
    print("{} {}".format(idx, col))
    idx += 1
    label_encoder = fit(x[col])
    x[col]=transform(label_encoder, x[col])
    outfile = './app/prediction_model/columns/' + col
    with open(outfile, 'wb') as pickle_file:
        pickle.dump(label_encoder, pickle_file)

#logreg = LogisticRegression()
#
## 3. fit 
#logreg.fit(x, y)

x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.00001)

#x_train.head()
#x_train.shape
#x_test.head()
#x_test.shape

trained_model = RandomForestClassifier(n_estimators=100).fit(x,y)

outfile = './app/prediction_model/prediction.model'
with open(outfile, 'wb') as pickle_file:
	pickle.dump(trained_model, pickle_file)

y_pred = trained_model.predict(x_test)
print(y_pred)
print(y_pred.shape)
confusion_matrix(y_test,y_pred)
accuracy_score(y_test,y_pred)
a=trained_model.feature_importances_
print(a)

#report = metrics.classification_report(y_test, y_pred, output_dict=True)
#df = dp.DataFrame(report).transpose()

# print(np.amax(a))
# print(np.amin(a))
result = np.where(a==np.amin(a))
# print(result)
# print(metrics.classification_report(y_test,y_pred))
