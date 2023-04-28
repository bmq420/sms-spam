import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import nltk
import string
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
nltk.download('stopwords')
nltk.download('punkt')
import re
import pickle

sms = pd.read_csv('E:/Conda/sms-spam/smsspamcollection/SMSSpamCollection', sep='\t', names=['label','message'])
print(sms.head())
sms.drop_duplicates(inplace=True)
sms.reset_index(drop=True, inplace=True)

corpus = []
ps = PorterStemmer()

# for i in range(0,sms.shape[0]):
#     message = re.sub(pattern='[^a-zA-Z]', repl=' ', string=sms.message[i]) #Cleaning special character from the message
#     message = message.lower() #Converting the entire message into lower case
#     words = message.split() # Tokenizing the review by words
#     words = [word for word in words if word not in set(stopwords.words('english'))] #Removing the stop words
#     words = [ps.stem(word) for word in words] #Stemming the words
#     message = ' '.join(words) #Joining the stemmed words
#     corpus.append(message) #Building a corpus of messages

# file_name = "corpus2.pkl"
# pickle.dump(corpus, open(file_name, 'wb'))

encoder = LabelEncoder()
sms['label'] = encoder.fit_transform(sms['label'])
sms = sms.drop_duplicates(keep="first")

def getImportantFeatures(sent):
    sent = sent.lower()
    list = []
    sent = nltk.word_tokenize(sent)
    for i in sent:
        if i.isalnum():
            list.append(i)
    return list

def removingStopWords(sent):
    list = []
    for i in sent:
        if i not in stopwords.words('english') and i not in string.punctuation:
            list.append(i)
    return list

def potterStem(sent):
    list = []
    for i in sent:
        list.append(ps.stem(i))
    return " ".join(list)

sms['implementFeatures'] = sms['message'].apply(getImportantFeatures)

sms['implementFeatures'] = sms['implementFeatures'].apply(removingStopWords)

sms['implementFeatures'] = sms['implementFeatures'].apply(potterStem)

#train_test_split
from sklearn.model_selection import train_test_split
X = sms['implementFeatures']
y = sms['label']
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)

tfidf = TfidfVectorizer()
feature = tfidf.fit_transform(X_train)
 
tuned_parameters = {'kernel':['linear','rbf'],'gamma':[1e-3,1e-4], 'C':[1,10,100,1000]}
model = GridSearchCV(SVC(),tuned_parameters)
model.fit(feature, y_train)

# function to predict the spam 
def predict_spam(sample_message):
    # implement the above model
    return model.predict(sample_message)

def main():
    while True:
        msg = input("Enter your message: ") 
        print(predict_spam(msg))
        if (predict_spam(msg)):
            print("Spam")
        else:
            print("Normal")
        if msg == "exit":
            break

main()


import numpy as np
import pandas as pd
from sklearn.preprocessing import LabelEncoder
import nltk
import string
from sklearn.svm import SVC
from sklearn.model_selection import GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
import re
import pickle

nltk.download('stopwords')
nltk.download('punkt')

sms = pd.read_csv('E:/Conda/sms-spam/smsspamcollection/SMSSpamCollection', sep='\t', names=['label','message'])
sms.drop_duplicates(inplace=True)
sms.reset_index(drop=True, inplace=True)

corpus = []
ps = PorterStemmer()

for i in range(sms.shape[0]):
    message = re.sub(pattern='[^a-zA-Z]', repl=' ', string=sms.message[i]) #Cleaning special character from the message
    message = message.lower() #Converting the entire message into lower case
    words = message.split() # Tokenizing the review by words
    words = [word for word in words if word not in set(stopwords.words('english'))] #Removing the stop words
    words = [ps.stem(word) for word in words] #Stemming the words
    message = ' '.join(words) #Joining the stemmed words
    corpus.append(message) #Building a corpus of messages

encoder = LabelEncoder()
sms['label'] = encoder.fit_transform(sms['label'])

tfidf = TfidfVectorizer()
X = tfidf.fit_transform(corpus)
y = sms['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)

tuned_parameters = {'kernel':['linear','rbf'],'gamma':[1e-3,1e-4], 'C':[1,10,100,1000]}
model = GridSearchCV(SVC(),tuned_parameters)
model.fit(X_train, y_train)

def preprocess_message(msg):
    ps = PorterStemmer()
    msg = re.sub(pattern='[^a-zA-Z]', repl=' ', string=msg) #Cleaning special character from the message
    msg = msg.lower() #Converting the entire message into lower case
    words = msg.split() # Tokenizing the review by words
    words = [word for word in words if word not in set(stopwords.words('english'))] #Removing the stop words
    words = [ps.stem(word) for word in words] #Stemming the words
    msg = ' '.join(words) #Joining the stemmed words
    return msg

# function to predict whether a message is spam or not
def predict_spam(msg):
    msg = preprocess_message(msg)
    feature = tfidf.transform([msg])
    return model.predict(feature)[0]

def main():
    while True:
        msg = input("Enter your message: ") 
        if msg == "exit":
            break
        if predict_spam(msg):
            print("Spam")
        else:
            print("Normal")

main()