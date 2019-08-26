from flask import *
from flask_pymongo import PyMongo

from flask_bootstrap import Bootstrap

import random

app = Flask('jumbled_words')

app.config['MONGO_URI'] = 'mongodb://localhost:27017/jumbled-words-db'

Bootstrap(app)

mongo = PyMongo(app)

@app.route('/', methods = ['GET', 'POST'])

def jumbled_words():
    #mongo.db.words.drop({})
    return render_template('jumble_a_word.html')

@app.route('/drop')

def drop():
    mongo.db.words.drop()
    return render_template('jumble_a_word.html')

@app.route('/jumble', methods=['GET', 'POST'])
def jumble():
    if request.method == 'GET':
        found_docs = [x for x in mongo.db.words.find({})]
        return render_template('jumble-a-word.html')
    elif request.method == 'POST':
        doc = {}
        for item in request.form:
            doc[item] = request.form[item].strip().upper()
        print(doc)
        mongo.db.words.insert_one(doc)
        return redirect('/')

@app.route('/figureout', methods =['GET', 'POST'])
def figureout():
    found_docs =list(mongo.db.words.find())
    total_words = len(found_docs)
    user_answers = []
    score = 0
    if request.method == 'GET':
        for doc in found_docs:
            jumbled_word_letters = list(doc['word'])
            random.shuffle(jumbled_word_letters)
            jumbled_word=''.join(jumbled_word_letters)
            doc['word'] = jumbled_word
        return render_template('find-the-words.html',docs = found_docs)
    elif request.method == 'POST':
        data = request.form.to_dict(flat = False)
        print(data)
        for doc in data['name']:
            user_answers.append(doc.strip().upper())
        found_docs = [x for x in mongo.db.words.find({})]
        total_answers=len(user_answers)
        for index in range(total_answers):
            if user_answers[index] == found_docs[index]['word']:
                score += 1
        return render_template('results.html', score = str(score))


app.run(debug=True)