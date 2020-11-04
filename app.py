from flask import *
from flask_pymongo import PyMongo

from flask_bootstrap import Bootstrap

import random

app = Flask('jumbled_words')

#app.config['MONGO_URI'] = 'mongodb://localhost:27017/jumbled-words-db'


app.config['MONGO_URI'] = 'mongodb+srv://richardlin:richardlin@cluster0-4kl8t.azure.mongodb.net/words?retryWrites=true&w=majority'
Bootstrap(app)

mongo = PyMongo(app)

@app.route('/', methods = ['GET', 'POST'])

def jumbled_words():

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
    '''percentage =0
    if total_words == 0:
        redirect('/')
    '''
    if request.method == 'GET':
        for doc in found_docs:
            jumbled_word_letters = list(doc['word'])
            random.shuffle(jumbled_word_letters)
            jumbled_word=''.join(jumbled_word_letters)
            doc['word'] = jumbled_word
        return render_template('find-the-words.html',docs = found_docs, count = total_words)
    elif request.method == 'POST':
        score = 0
        user_answers=[]
        #data = request.form.to_dict(flat = False)
        #if len(data)==0:
        #    return redirect('/')
        #for doc in data['name']:
        #    user_answers.append(doc.strip().upper())
        #print(user_answers)

        #found_docs = [x for x in mongo.db.words.find({})]
        #total_answers=len(user_answers)
        '''for index in range(total_words):
            if user_answers[index] == found_docs[index]['word']:
                score += 1
        '''
        for item in request.form:
            user_answers.append(request.form[item].strip().upper())
        for index in range(0,total_words):
            if user_answers[index] == found_docs[index]['word']:
                score += 1

        try:
            percentage = score / total_words * 100
        except ZeroDivisionError:
            print('error')
        message =''
        grade = ''
        if 90.0 <=percentage<=100:
            message ='Excellent'
            grade = 'A'
        elif 80.0 <=percentage<90:
            message ='Good'
            grade ="B"
        elif 70 <= percentage <80:
            message = 'Average'
            grade = 'C'
        elif 60 <= percentage < 70:
            message = 'Below Average'
            grade = 'D'
        elif 0<= percentage<60:
            grade = 'F'
            message = 'Failure'

        return render_template('results.html', score = str(score), total= total_words, message= message, grade = grade)

if __name__ == '__main__':
    app.run(host='https://sensationnel-monsieur-51684.herokuapp.com/',debug=True)