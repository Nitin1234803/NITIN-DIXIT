import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df=pd.read_csv("/Users/nitin/Downloads/House Price Prediction model/house_price_prediction.csv")
df.head()

df.isnull().sum()

df=df.fillna(method='pad')
df.head()

df.isnull().sum()

x=df.drop(['price'],axis=1)
y=df['price']

from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.metrics import r2_score

scaler=StandardScaler()
x_scaled=scaler.fit_transform(x)

from sklearn.model_selection import train_test_split
x_train,x_test,y_train,y_test=train_test_split(x,y,train_size=0.7,test_size=0.3,random_state=21)

lr=LinearRegression()
lr.fit(x_train,y_train)

y_pred=lr.predict(x_test)

r2=r2_score(y_test,y_pred)
print(r2)

lr.predict([[79545.45857,5.682861,7.009188,4.09,23086.80050]])

ridge=Ridge()
ridge.fit(x_train,y_train)
y__pred=ridge.predict(x_test)
r2=r2_score(y_test,y__pred)
print(r2)

lasso=Lasso()
lasso.fit(x_train,y_train)
y___pred=lasso.predict(x_test)
r2=r2_score(y_test,y___pred)
print(r2)

import pickle
pickle.dump(ridge,open('model.pkl','wb'))

