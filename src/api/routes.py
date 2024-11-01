"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
from flask import Flask, request, jsonify, url_for, Blueprint
from api.models import db, User
from api.utils import generate_sitemap, APIException
from flask_cors import CORS

api = Blueprint('api', __name__)

# Allow CORS requests to this API
CORS(api)


@api.route('/hello', methods=['POST', 'GET'])
def handle_hello():

    response_body = {
        "message": "Hello! I'm a message that came from the backend, check the network tab on the google inspector and you will see the GET request"
    }

    return jsonify(response_body), 200

@api.route('/users', methods=['POST'])
def create_user():
    data = request.json
    user = User(email=data['email'], password_hash=data['password'], full_name=data.get('full_name'))
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'User created', 'user_id': user.id}), 201

@api.route('/surveys', methods=['POST'])
def create_survey():
    data = request.json
    survey = Survey(creator_id=data['creator_id'], title=data['title'], description=data.get('description'),
                    start_date=data.get('start_date'), end_date=data.get('end_date'),
                    is_public=data.get('is_public', True), status='draft', type=data['type'])
    db.session.add(survey)
    db.session.commit()
    return jsonify({'message': 'Survey created', 'survey_id': survey.id}), 201

@api.route('/questions', methods=['POST'])
def add_question():
    data = request.json
    question = Question(survey_id=data['survey_id'], question_text=data['question_text'],
                        question_type=data['question_type'], order=data.get('order'), required=data.get('required', True))
    db.session.add(question)
    db.session.commit()
    return jsonify({'message': 'Question added', 'question_id': question.id}), 201

@api.route('/options', methods=['POST'])
def add_option():
    data = request.json
    option = Option(question_id=data['question_id'], option_text=data['option_text'], order=data.get('order'))
    db.session.add(option)
    db.session.commit()
    return jsonify({'message': 'Option added', 'option_id': option.id}), 201

@api.route('/votes', methods=['POST'])
def submit_vote():
    data = request.json
    vote = Vote(survey_id=data['survey_id'], user_id=data['user_id'], question_id=data['question_id'], option_id=data.get('option_id'))
    db.session.add(vote)
    db.session.commit()
    return jsonify({'message': 'Vote submitted', 'vote_id': vote.id}), 201

@api.route('/invitations', methods=['POST'])
def create_invitation():
    data = request.json
    invitation = Invitation(survey_id=data['survey_id'], user_id=data['user_id'], token=data['token'],
                            expires_at=data.get('expires_at'), used=False)
    db.session.add(invitation)
    db.session.commit()
    return jsonify({'message': 'Invitation created', 'invitation_id': invitation.id}), 201

if __name__ == '__main__':
    db.create_all()
    api.run(debug=True)