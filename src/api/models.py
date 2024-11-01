from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request, Blueprint, url_for
from flask_admin import Admin, BaseView, expose
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from datetime import datetime

db = SQLAlchemy()

from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, nullable=False)
    email = db.Column(db.String, unique=True, nullable=False)
    password_hash = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    # Relación con encuestas creadas

    # Relación con votos realizados

    # Relación con invitaciones recibidas


    def __repr__(self):
        return f'<User {self.email}>'

    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            "full_name": self.full_name,
           # "created_at": self.created_at.isoformat(),
            "is_active": self.is_active
        }

class Survey(db.Model):
    __tablename__ = 'surveys'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String, nullable=False)
    description = db.Column(db.Text)
    start_date = db.Column(db.DateTime)
    end_date = db.Column(db.DateTime)
    is_public = db.Column(db.Boolean, default=True)

    status = db.Column(db.Enum('draft', 'active', 'closed', name='status'))
    type = db.Column(db.Enum('survey', 'poll', name='type'), nullable=False)
   # created_at = db.Column(db.DateTime, default=datetime.utcnow)
    usuaries = db.relationship('User')
        # Relación con preguntas

    # Relación con votos
   

    # Relación con invitaciones
   

    #def __repr__(self):
        #return f'<Survey {self.title}>'

    def serialize(self):
        return {
            "id": self.id,
            "creator_id": self.creator_id,
            "title": self.title,
            "description": self.description,
           # "start_date": self.start_date.isoformat() if self.start_date else None,
            #"end_date": self.end_date.isoformat() if self.end_date else None,
            "is_public": self.is_public,
            "status": self.status,
            "type": self.type,
           # "created_at": self.created_at.isoformat()
        }

class Question(db.Model):
    __tablename__ = 'questions'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'), nullable=False)
    question_text = db.Column(db.String, nullable=False)
    question_type = db.Column(db.Enum('yes_no', 'multiple_choice', 'open_ended', 'scale', name='question_type'), nullable=False)
    order = db.Column(db.Integer)
    required = db.Column(db.Boolean, default=True)

    question_surveys = db.relationship('Survey')

    # Relación con opciones de respuesta
    #options = db.relationship('Option', backref='question', lazy=True)

    # Relación con votos
    #votes = db.relationship('Vote', backref='question', lazy=True)

    def __repr__(self):
        return f'<Question {self.question_text}>'

    def serialize(self):
        return {
            "id": self.id,
            "survey_id": self.survey_id,
            "question_text": self.question_text,
            "question_type": self.question_type,
            "order": self.order,
            "required": self.required
        }

class Option(db.Model):
    __tablename__ = 'options'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    option_text = db.Column(db.String, nullable=False)
    order = db.Column(db.Integer)

    # Relación con votos
    option_questions = db.relationship('Question')

    def __repr__(self):
        return f'<Option {self.option_text}>'

    def serialize(self):
        return {
            "id": self.id,
            "question_id": self.question_id,
            "option_text": self.option_text,
            "order": self.order
        }

class Vote(db.Model):
    __tablename__ = 'votes'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    question_id = db.Column(db.Integer, db.ForeignKey('questions.id'), nullable=False)
    option_id = db.Column(db.Integer, db.ForeignKey('options.id'))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    votes_usuaries = db.relationship('User')
    votes_questions = db.relationship('Question')
    votes_options = db.relationship('Option')


    def __repr__(self):
        return f'<Vote by User {self.user_id} on Survey {self.survey_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "survey_id": self.survey_id,
            "user_id": self.user_id,
            "question_id": self.question_id,
            "option_id": self.option_id,
            "created_at": self.created_at.isoformat()
        }

class Invitation(db.Model):
    __tablename__ = 'invitations'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    survey_id = db.Column(db.Integer, db.ForeignKey('surveys.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    token = db.Column(db.String, unique=True, nullable=False)
    expires_at = db.Column(db.DateTime)
    used = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    usuaries = db.relationship('User')
    survies = db.relationship('Survey')

    def __repr__(self):
        return f'<Invitation {self.token} for Survey {self.survey_id}>'

    def serialize(self):
        return {
            "id": self.id,
            "survey_id": self.survey_id,
            "user_id": self.user_id,
            "token": self.token,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "used": self.used,
            "created_at": self.created_at.isoformat()
        }

    