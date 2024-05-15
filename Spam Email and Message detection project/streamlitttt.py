import streamlit as st
import pickle
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer

ps=PorterStemmer()

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

CV=pickle.load(open("model1.pkl",'rb'))
BNB=pickle.load((open('model2.pkl','rb')))

st.title('Email/SMS Spam Classifier')

input_sms=st.text_input("enter the message")

transform_sms=transform_message(input_sms)

vector_input=CV.transform([transform_sms])

result=BNB.predict(vector_input)[0]

if result==1:
    st.header("spam")

else:
    st.header("not spam")




