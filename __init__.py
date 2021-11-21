from flask import Flask
from flask import session
from flask import render_template
from flask import request
from flask import redirect, url_for
from forms import RegisterForm, LoginForm
from database import db
import bcrypt
import os


app = Flask(__name__)   # create the app

# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_note_app.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   # don't need this
app.config['SECRET_KEY'] = 'SE3155'                    # add secret key??????

db.init_app(app)                                        # bind the db object to this flask app

with app.app_context():                                 # set up app and run it under app context
    db.create_all()

'''
Decorators
'''

@app.route('/')

@app.route('/index')
def index():
    if session.get('user'):
        return render_template('index.html', user= session['user'])
    return render_template('index.html')

@app.route('/my_questions')
def get_questions():
    if session.get('user'):
        my_questions = db.session.query(Question).filter_by(user_id=session['user_id']).all()
        return render_template('my_questions.html', questions=my_questions, user=session['user'])

@app.route('/my_questions/<question_id>')
def get_question(question_id):
    if session.get('user'):
        my_question = db.session.query(Question).filter_by(note_id, user_id=session['user_id']).one()
        form = CommentForm()
    return render_template('question.html', question=my_question, user=session['user'], form=form)

@app.route('/my_questions/new', methods=['GET', "POST"])
def new_question():
    if session.get('user'):
        if request.method == "POST":
            title = request.form['title']               # get question title
            text = request.form['questionText']         # get question text
            from datetime import date
            today = date.today()
            today = today.strftime("%m-%d-%Y")
            new_record = Question(title, text, session['user_id'])
            db.session.add(new_record)
            db.sesion.commit()

            return redirect(url_for('get_questions'))
        else:
            return render_template('new.html', user=session['user'])        # get request
    else:
        return redirect(url_for('login'))                                   # user is not in session

@app.route('/questions/edit/<question_id>', methods=["GET", "POST"])
def update_question(question_id):
    if session.get('user'):                            # check if a user is saved in session
        if request.method == 'POST':
            title = request.form['title']              # get title data
            text = request.form['questionText']        # get note data
            question = db.session.query(Question).filter_by(id=question_id).one()
            question.title = title
            question.text = text

            db.session.add(question)
            db.session.commit()

            return redirect(url_for('get_questions'))
        else:
            my_question = db.session.query(Question).filter_by(id=question_id).one()
            return render_template('new.html', question=my_question, user=session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/questions/delete/<question_id>', methods=['POST'])
def delete_question(question_id):
    if session.get('user'):
        my_question = db.session.query(Question).filter_by(id=question_id).one()
        db.session.delete(my_question)
        db.session.commit()
        return redirect(url_for('get_questions'))
    else:
        return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == "POST" and form.validate_one_submit():
        h_password = bcrypt.hashpw(
            request.form['password'].encode('utf-8'), bcrypt.gensalt()    # salt and hash password
        )
        first_name = request.form['firstname']
        last_name = request.form['lastname']

        new_user = User(first_name, last_name, request.form['email'], h_password)

        db.session.add(new_user)     # saving new user to database
        db.session.commit()

        session['user'] = first_name
        session['user_id'] = new_user.id        # access id value from user model of this newly added user

        return redirect(url_for('get_questions'))
    return render_template('register.html', form=form)
