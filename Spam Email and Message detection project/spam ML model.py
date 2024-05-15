import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

df = pd.read_csv("/Users/nitin/Downloads/spam detection model/spam.csv", encoding='latin-1')
df.head()

df.drop(['Unnamed: 2'], axis=1, inplace=True)
df.drop(['Unnamed: 3'], axis=1, inplace=True)
df.drop(['Unnamed: 4'], axis=1, inplace=True)
df.head()

df.rename(columns={'v1': 'target', 'v2': 'message'}, inplace=True)

data = df.where((pd.notnull(df)), '')

data.info()
data.shape

x = data['message']
y = data['target']

from sklearn.preprocessing import LabelEncoder

encoder = LabelEncoder()
df['target'] = encoder.fit_transform(df['target'])
df.head()

# missing values
df.isnull().sum()

# duplicate values
df.duplicated().sum()

# remove duplicates
df = df.drop_duplicates(keep='first')

import nltk

nltk.download('punkt')

df['num_characters'] = df['message'].apply(len)
df.head()

df['num_words'] = df['message'].apply(lambda x: len(nltk.word_tokenize(x)))

df.head()

df['num_sentences'] = df['message'].apply(lambda x: len(nltk.sent_tokenize(x)))
df.head()

df.loc[df['target'] == 'spam', 'target'] = 1
df.loc[df['target'] == 'ham', 'target'] = 0

# DATA PRE-PROCESSING
# 1.lower case
# 2.tokenization
# 4.removing special characters
# 4.removing stop words and punctuation
# 5.stemming

import re
import nltk

nltk.download('stopwords')
from nltk.corpus import stopwords


def transform_message(message):
    message = message.lower()
    message = nltk.word_tokenize(message)

    y = []
    for i in message:
        if i.isalnum():
            y.append(i)

    message = y[:]
    y.clear()

    for i in message:
        if i not in stopwords.words('english'):
            y.append(i)

    message = y[:]
    y.clear()

    for i in message:
        y.append(i)

    return " ".join(y)


transform_message('I loved the YT lectures on Machine Learning. How about you')

df['transformed_message'] = df['message'].apply(transform_message)
df.head()

# MODEL BUILDING
from sklearn.feature_extraction.text import CountVectorizer

cv = CountVectorizer()

x = cv.fit_transform(df['transformed_message']).toarray()

x.shape

y = df['target'].values
y = y.astype('int')

# train test split
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.8, test_size=0.2, random_state=21)

from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
# Different regression metrics
from sklearn.metrics import accuracy_score, confusion_matrix, precision_score

gnb = GaussianNB()
mnb = MultinomialNB()
bnb = BernoulliNB()

gnb.fit(x_train, y_train)
y_pred = gnb.predict(x_test)
print(precision_score(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
print(accuracy_score(y_test, y_pred))

mnb.fit(x_train, y_train)
y_pred = mnb.predict(x_test)
print(precision_score(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
print(accuracy_score(y_test, y_pred))

bnb.fit(x_train, y_train)
y_pred = bnb.predict(x_test)
print(precision_score(y_test, y_pred))
print(confusion_matrix(y_test, y_pred))
print(accuracy_score(y_test, y_pred))

import pickle

pickle.dump(cv, open('model1.pkl', 'wb'))
pickle.dump(bnb, open('model2.pkl', 'wb'))

