import pandas as pd
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
nltk.download('stopwords')
import re
import pickle

sms = pd.read_csv('E:/sms-spam-python/smsspamcollection/SMSSpamCollection', sep='\t', names=['label','message'])
sms.drop_duplicates(inplace=True)
sms.reset_index(drop=True, inplace=True)

corpus = []
ps = PorterStemmer()

for i in range(0,sms.shape[0]):
    message = re.sub(pattern='[^a-zA-Z]', repl=' ', string=sms.message[i]) #Cleaning special character from the message
    message = message.lower() #Converting the entire message into lower case
    words = message.split() # Tokenizing the review by words
    words = [word for word in words if word not in set(stopwords.words('english'))] #Removing the stop words
    words = [ps.stem(word) for word in words] #Stemming the words
    message = ' '.join(words) #Joining the stemmed words
    corpus.append(message) #Building a corpus of messages

#Save corpus for use in deployment
file_name = "corpus2.pkl"
pickle.dump(corpus, open(file_name, 'wb'))

# Convert the preprocessed text data into a feature matrix using CountVectorizer
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=2500)
X = cv.fit_transform(corpus).toarray()

# Convert the labels into binary values
y = pd.get_dummies(sms['label'])
y = y.iloc[:, 1].values

# Split the dataset into training and test sets
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20, random_state=0)

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import tensorflow as tf
tf.get_logger().setLevel('ERROR')

# Define the model architecture
classifier = tf.keras.models.Sequential([
    tf.keras.layers.Dense(128, input_shape=(X_train.shape[1],), activation='relu'),
    tf.keras.layers.Dropout(0.5),
    tf.keras.layers.Dense(1, activation='sigmoid')
])


# Compile the model
classifier.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

# Train the model
classifier.fit(X_train, y_train, batch_size=32, epochs=10, validation_data=(X_test, y_test)) 

#Save Model
file_name = "backpropagation.pkl"
pickle.dump(classifier, open(file_name, 'wb'))