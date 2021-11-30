import bcrypt
import os
from flask import Flask
from flask import session
from flask import render_template
from flask import request
from flask import redirect, url_for
from werkzeug.utils import secure_filename
from .models import Question as Question
from .models import User as User
from .models import Comment as Comment
from .models import Img as Img
from .forms import RegisterForm, LoginForm, CommentForm
from .database import db



app = Flask(__name__)   # create the app

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flask_class_app.db'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False   # don't need this
app.config['SECRET_KEY'] = 'SE3155'                    # add secret key??????

db.init_app(app)                                        # bind the db object to this flask app

with app.app_context():                                 # set up app and run it under app context
    db.create_all()

'''
Decorators
'''

@app.route('/')

@app.route('/landing')
def landing():
    return render_template('landing.html')

@app.route('/profile')
def profile():
    if session.get('user'):
        my_questions = db.session.query(Question).all()
        return render_template('profile.html', questions=my_questions, user= session['user'])
    return redirect(url_for('login'))

@app.route('/my_questions')
def get_questions():
    if session.get('user'):
        my_questions = db.session.query(Question).filter_by(user_id=session['user_id']).all()
        return render_template('my_questions.html', questions=my_questions, user=session['user'])
    else:
        return redirect(url_for('login'))

@app.route('/my_questions/<question_id>')
def get_question(question_id):
    if session.get('user'):
        my_question = db.session.query(Question).filter_by(id=question_id, user_id=session['user_id']).one()
        form = CommentForm()
    return render_template('question.html', question=my_question, user=session['user'], form=form)

@app.route('/my_questions/new', methods=['GET', "POST"])
def new_question():
    if session.get('user'):
        if request.method == 'POST':
            title = request.form['title']               # get question title
            text = request.form['questionText']         # get question text
            from datetime import date
            today = date.today()
            today = today.strftime("%m-%d-%Y")
            new_record = Question(title, text, today, session['user_id'])
            db.session.add(new_record)
            db.session.commit()

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
        return redirect(url_for('get_questions'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    form = RegisterForm()

    if request.method == "POST" and form.validate_on_submit():
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

@app.route('/login', methods=['POST', 'GET'])
def login():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        the_user = db.session.query(User).filter_by(email=request.form['email']).one()
        if bcrypt.checkpw(request.form['password'].encode('utf-8'), the_user.password):
            session['user'] = the_user.first_name
            session['user_id'] = the_user.id

            return redirect(url_for('get_questions'))
        login_form.password.errors = ['incorrect username or password']
        return render_template('login.html', form=login_form)
    else:
        return render_template('login.html', form=login_form)

@app.route('/logout')
def logout():
    if session.get('user'):
        session.clear()
    return redirect(url_for('index'))

@app.route('/questions/<question_id>/comment', methods=['POST'])
def new_comment(question_id):
    if session.get('user'):
        comment_form = CommentForm()
        if comment_form.validate_on_submit():
            comment_text = request.form['comment']
            new_record = Comment(comment_text, int(question_id), session['user_id'])
            db.session.add(new_record)
            db.session.commit()
            return redirect(url_for('get_question', question_id=question_id))
    else:
        return redirect(url_for('login'))



@app.route('/questions/<question_id>/upload', methods=["GET", "POST"])
def upload(question_id):
    pic = request.files['pic']
    if not pic:
        return "No pic uploaded", 400

    filename = secure_filename(file.filename)
    mimetype = pic.mimetype
    img = Img(img=pic.read(), mimetype=mimetype, name=filename)
    db.session.add(img)
    db.sesion.commit()
    return redirect(url_for('get_question'))

'''@app.route('/questions/<question_id>/image')
def get_image(question_id):
    img = Img.query.filter_by(id=question_id).first()
    if not img:
        return redirect(url_for('get_question'))
    return redirect(url_for() '''

app.run(host=os.getenv('IP', '127.0.0.1'), port=int(os.getenv('PORT', 5000)), debug=True)