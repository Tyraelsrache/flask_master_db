import os
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
import random
import sys

from models import *


# create and configure the app
app = Flask(__name__)
setup_db(app)

CORS(app)
migrate = Migrate(app, db)

@app.after_request
def after_request(response):
    response.headers.add(
        'Access-Control-Allow-Headers',
        'Content-Type,Authorization,true')
    response.headers.add(
        'Access-Control-Allow-Methods',
        'GET,PUT,POST,DELETE,OPTIONS')
    return response


@app.route('/')
def landing_page():

    return 'Hello to my API'




# TODO: GET Actor

@app.route('/actor', methods=['GET'])
def get_actor():
    return 'get actor'

# TODO: GET Movie

@app.route('/movie', methods=['GET'])
def get_movie():
    return 'get movie'


# TODO: Post Actor

@app.route('/actor', methods=['POST'])
def post_actor():
    return 'post actor'

# TODO: Post Movie

@app.route('/movie', methods=['POST'])
def post_movie():
    return 'post movie'

# TODO: Patch Actor

@app.route('/actor/<id>', methods=['PATCH'])
def patch_actor(id):
    return 'patch actor'

# TODO: Patch Movie
@app.route('/movie/<id>', methods=['PATCH'])
def patch_movie(id):
    return 'patch movie'

# TODO: Delete Actor

@app.route('/actor/<id>', methods=['DELETE'])
def delete_actor(id):
    return 'delete actor'

# TODO: Delete Movie
@app.route('/movie/<id>', methods=['DELETE'])
def delete_movie(id):
    return 'delete movie'








@app.route('/questions')
def get_q():
    selection = Question.query.order_by(Question.id).all()
    current_q = paginate(request, selection)
    categories = Category.query.order_by(Category.type).all()

    if len(current_q) == 0:
        abort(404)

    return jsonify({
        'success': True,
        'questions': current_q,
        'total_questions': len(selection),
        'categories': {category.id: category.type
                        for category in categories},
        'current_category': None
    })

@app.route("/questions/<question_id>", methods=['DELETE'])
def delete_q(question_id):
    try:
        question = Question.query.get(question_id)
        question.delete()
        return jsonify({
            'success': True,
            'deleted': question_id
        })
    except BaseException:
        abort(422)

@app.route("/questions", methods=['POST'])
def add_question():
    body = request.get_json()
    question = body.get('question')
    answer = body.get('answer')
    difficulty = body.get('difficulty')
    category = body.get('category')

    try:
        question = Question(
            question=question,
            answer=answer,
            difficulty=difficulty,
            category=category)
        question.insert()

        return jsonify({
            'success': True,
            'created': question.id,
        })

    except BaseException:
        abort(422)

@app.route('/questions/search', methods=['POST'])
def search_questions():
    body = request.get_json()
    search_term = body.get('searchTerm', None)
    if (search_term is None):
        abort(422)

    else:
        questions = Question.query.filter(
            Question.question.contains(search_term)).all()
        return jsonify({
            'success': True,
            'questions': [question.format() for question in questions],
            'total_questions': len(questions),
            'current_category': "2"
        })

@app.route('/categories/<int:category_id>/questions', methods=['GET'])
def get_question_by_id(category_id):

    try:
        questions = Question.query.filter(
            Question.category == str(category_id)).all()

        return jsonify({
            'success': True,
            'questions': [question.format() for question in questions],
            'total_questions': len(questions),
            'current_category': category_id
        })
    except BaseException:
        abort(404)

@app.route('/quizzes', methods=['POST'])
def play_quiz():

    try:
        body = request.get_json()
        category = body.get('quiz_category')
        previous_questions = body.get('previous_questions')
        print(category, file=sys.stderr)
        if (category['id'] == '0'):
            questions = Question.query.filter(
                Question.id.notin_((previous_questions))).all()
        else:
            questions = Question.query.filter_by(
                category=category['id']).filter(
                Question.id.notin_(
                    (previous_questions))).all()

        next_question = questions[random.randrange(
            0, len(questions))].format()

        return jsonify({
            'success': True,
            'question': next_question
        })
    except BaseException:
        abort(404)

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404

@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422

