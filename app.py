from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import pickle 
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem.porter import PorterStemmer
nltk.download('stopwords')
import re
from sklearn.feature_extraction.text import CountVectorizer

# Prediction
#Import Pickle file
file_name = "spam_sms_prediction.pkl"
classifier = pickle.load(open(file_name, 'rb'))

file_name = "corpus.pkl"
corpus = pickle.load(open(file_name, 'rb'))

# file_name2 = "Spam_sms_prediction_svm.pkl"

#Creating the Bag of Words model
cv = CountVectorizer(max_features=2500)
X = cv.fit_transform(corpus).toarray()

def predict_spam(sample_message):
    sample_message = re.sub(pattern='[^a-zA-Z]',repl=' ', string = sample_message)
    sample_message = sample_message.lower()
    sample_message_words = sample_message.split()
    sample_message_words = [word for word in sample_message_words if not word in set(stopwords.words('english'))]
    ps = PorterStemmer()
    final_message = [ps.stem(word) for word in sample_message_words]
    final_message = ' '.join(final_message)
    temp = cv.transform([final_message]).toarray()
    return classifier.predict(temp)

# Flask app
app = Flask(__name__)
cors = CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:bmqisme123@localhost:3306/security'
db = SQLAlchemy(app)

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255))
    label = db.Column(db.String(50))
    available = db.Column(db.Integer)

@app.route('/api/v1', methods=['POST'])
def add_message():
    data = request.json
    if data['message'] == "":
        return jsonify({'message': 'message is empty'}), 400
    messages = Message.query.all()
    for message in messages:
        if message.message == data['message']:
            return jsonify({'message': 'message already exists'}), 400
    
    if predict_spam(data['message']) == 1:
        checkResult = "HAM"
    else:
        checkResult = "NORMAL"
    message = Message(message=data['message'], available=data['available'], label=checkResult)
    db.session.add(message)
    db.session.commit()
    return jsonify({'id': message.id, 'message': message.message, 'label': message.label, 'available': message.available}), 200

@app.route('/api/v1/<int:id>', methods=['GET'])
def get_message(id):
    message = Message.query.get(id)
    return jsonify({'id': message.id, 'message': message.message, 'label': message.label, 'available': message.available}), 200

@app.route('/api/v1', methods=['GET'])
def get_messages():
    messages = Message.query.all()
    result = []
    for message in messages:
        if message.available == 1:
            result.append({'id': message.id, 'message': message.message, 'label': message.label, 'available': message.available})
    return jsonify(result), 200  

@app.route('/api/v1/result', methods=['GET'])
def get_result():
    max_id = db.session.query(db.func.max(Message.id)).scalar()
    message = Message.query.get(max_id)
    print(message.message + " " + message.label)
    return str(message.label), 200

@app.route('/api/v1/<int:id>', methods=['POST'])
def set_available(id):
    message = Message.query.get(id)
    message.available = 0
    db.session.commit()
    return jsonify({'id': message.id, 'message': message.message, 'label': message.label, 'available': message.available}), 200

@app.route('/api/v1', methods=['POST'])
def set_all_available():
    messages = Message.query.all()
    for message in messages:
        message.available = 0
    db.session.commit()
    return jsonify({'message': 'All messages are not available'}), 200

if __name__ == '__main__':
    app.run(debug=True)