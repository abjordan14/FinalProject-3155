from .database import db
import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_whooshalchemy import whoosh_index
from app import app
db = SQLAlchemy()

class Question(db.Model):
    __searchable__ = ['name']
    name = db.Column(db.String(64))
    id = db.Column('id', db.Integer, primary_key=True)
    title = db.Column('title', db.String(200))
    text = db.Column('text', db.String(100))
    img_url = db.Column('img_url', db.String(200))
    date = db.Column('date', db.String(50))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    comments = db.relationship('Comment', backref='question', cascade='all, delete-orphan', lazy=True)
    like = db.relationship('Liked', backref='question', cascade='all, delete-orphan', lazy=True)

whoosh_index(app, User)

    def __init__(self, title, text, date, img_url, user_id):
        self.title = title
        self.text = text
        self.date = date
        self.img_url = img_url
        self.user_id = user_id



class User(db.Model):
    id = db.Column('id', db.Integer, primary_key=True)
    first_name = db.Column('first_name', db.String(100))
    last_name = db.Column('last_name', db.String(100))
    email = db.Column('email', db.String(100))
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    questions = db.relationship('Question', backref='user', lazy=True)
    comments = db.relationship('Comment', backref='user', lazy=True)
    like = db.relationship('Liked', backref='user', lazy='dynamic')


    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.registered_on = datetime.date.today()


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False)
    content = db.Column(db.VARCHAR, nullable=False)
    date = db.Column('date', db.String(50))
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, content, question_id, date, user_id):
        self.date_posted = datetime.date.today()
        self.content = content
        self.question_id = question_id
        self.date = date
        self.user_id = user_id

class Liked(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, question_id, user_id):
        self.question_id = question_id
        self.user_id = user_id
  
