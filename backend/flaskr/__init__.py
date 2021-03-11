import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

'''
Constant: Number of elements showed in the page.
This is intended for pagination.
'''
QUESTIONS_PER_PAGE = 10

'''
Pagination Function:

It determines how many questions will be shown per page, controlled by the
'QUESTIONS_PER_PAGE' variable (default = 10). It follows the guidelines from
API course's example: "Bookshelf App".
'''


def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    page_questions = questions[start:end]

    return page_questions


'''
Main App:

Configuration and definition for the main App, API endpoints and Error
Handlers.

Task needed to be convered:

    1.  Set up CORS. Allow '*' for origins.
    2.  Use the after_request decorator to set Access-Control-Allow
    3.  Create an endpoint to handle GET requests for all available categories.
    4.  Create an endpoint to handle GET requests for questions, including
        pagination (every 10 questions).
    5.  Create an endpoint to DELETE question using a question ID.
    6.  Create an endpoint to POST a new question, which will require the
        question and answer text, category, and difficulty score.
    7.  Create a POST endpoint to get questions based on a search term.
        It should return any questions for whom the search term is a substring
        of the question.
    8.  Create a GET endpoint to get questions based on category.
    9.  Create a POST endpoint to get questions to play the quiz.
    10. Create error handlers for all expected errors including 404 and 422.
'''


def create_app(test_config=None):

    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    # 1.- Set up CORS allowing all the origins
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # 2.- Access control
    @app.after_request
    def after_request(response):
        response.headers.add(
            'Access-Control-Allow-Headers',
            'Content-Type,Authorization,true')
        response.headers.add(
            'Access-Control-Allow-Methods',
            'GET,PUT,POST,DELETE,OPTIONS')
        return response

    '''
    A.- ENDPOINTS:

    '''
    # 3.- GET ALL AVAILABLE CATEGORIES
    @app.route('/categories')
    def get_categories():
        '''
        Description: Query all the categories existing in the DB and add it to
        a dictionary that will be presented in JSON format if success.
        Otherwise, throw an 404 error.
        '''
        # Collect (query) all categories in DB and dictionary initialization.
        categories = Category.query.all()
        category_dictionary = {}

        # Make Key:Value using 'Id': 'Type'
        # (1:Science, 2:Art, 3:Geography, 4:History, 5:Entertainment, 6:Sports)
        for c in categories:
            category_dictionary[c.id] = c.type

        # When dictionary is empty >>>> Throws 404 error #
        # if 'category_dictionary' in not empty
        if (len(category_dictionary) != 0):
            # Show the data from the dictionary in JSON format.
            return jsonify({
                'success': True,
                'categories': category_dictionary,
                }), 200
        # Dictionary is empty
        else:
            abort(404)

    # 4.- GET ALL QUESTIONS
    @app.route('/questions')
    def get_questions():
        '''
        Description: Query all the questions existing in the DB, add it to
        a dictionary and use pagination to present results in JSON format
        if success. Otherwise, throw an 404 error.
        '''
        # Collect (query) all questions in DB and dictionary initialization.
        questions = Question.query.all()
        page_questions = paginate_questions(request, questions)

        # Collect (query) all categories in DB and dictionary initialization.
        categories = Category.query.all()
        category_dictionary = {}
        for category in categories:
            category_dictionary[category.id] = category.type

        try:
            if page_questions:
                return jsonify({
                    'success': True,
                    'questions': page_questions,
                    'total_questions': len(questions),
                    'categories': category_dictionary
                    }), 200
            # DB is empty
            else:
                abort(404)

        # Another error > Unprocessable
        except BaseException:
            abort(422)

    # 5.- DELETE QUESTION
    @app.route('/questions/<int:question_id>', methods=['DELETE'])
    def delete_question(question_id):
        '''
        Description: If the user selects the trash can in the app, get the
        question's ID and delete it from the DB, delivering a success message
        indicating which question ID was deleted.
        '''
        try:
            # Select the question by ID
            question = Question.query.get_or_404(question_id)
            if question:
                question.delete()
                return jsonify({
                    'success': True,
                    'id': question_id,
                    'message': "Question deleted successfully!"
                    }), 200
            else:
                abort(404)
        except BaseException:
            abort(422)

    # 6.- ADD NEW QUESTION
    @app.route('/questions', methods=['POST'])
    def create_question():
        '''
        Description: Create a new question from the UI, indicating 'question',
        'category', 'answer' and 'difficulty'. All the data needs to be
        in filled in order to create a new question.
        '''
        # Get the data from the UI
        user_data = request.get_json()
        user_question = user_data.get("question")
        user_answer = user_data.get("answer")
        user_category = user_data.get("category")
        user_difficulty = user_data.get("difficulty")

        # All the information needs to be provided
        if (user_answer and user_category and (
                user_difficulty and user_question)):

            try:
                new_question = Question(
                    question=user_question,
                    answer=user_answer,
                    category=user_category,
                    difficulty=user_difficulty,
                    )
                new_question.insert()

                # Return success in JSON format
                return jsonify({
                    'success': True,
                    'message': "Question successfully added to the database!",
                    'question': new_question.format(),
                    }), 200

            except BaseException:
                abort(400)
        # Some info is missing
        else:
            abort(400)

    # 7.- SEARCH FOR A TERM
    @app.route("/questions/search", methods=["POST"])
    def search_question():
        '''
        Description: Search in the DB for the searchterm typed by the user and
        returns all the questions that have the word in it.
        If there's no question including the searchterm provided, a 404 error
        will be send.
        '''
        # Get the data from the UI
        search_data = request.get_json()
        search_term = search_data.get("searchTerm")
        search_results = Question.query.filter(
            Question.question.ilike(f'%{search_term}%')).all()
        results = paginate_questions(
            request,
            search_results)

        try:
            if len(results):
                return jsonify({
                    'success': True,
                    'questions': results,
                    'total_questions': len(results),
                    'current_category': None,
                    }), 200
            # There's no result for searchTerm
            else:
                abort(404)
        # Unprocessable error
        except BaseException:
            abort(422)

    # 8.- FILTER QUESTIONS BY CATEGORY
    @app.route("/categories/<int:category_id>/questions", methods=["GET"])
    def get_questions_by_category(category_id):
        '''
        Description: Get the list of questions filtered by category.
        Pagination is abailable. If the category doesn't exists, an error 404
        will be showed.
        '''
        # Filter the questions according to the corresponding category
        filtered = Question.query.filter_by(category=category_id).all()
        questions = paginate_questions(request, filtered)

        try:
            if len(filtered):
                return jsonify({
                    "success": True,
                    "questions": questions,
                    "total_questions": len(filtered),
                    "current_category": category_id,
                    }), 200
            else:
                abort(404)
        # Unprocessable error
        except BaseException:
            abort(422)

    # 9.- PLAY THE GAME - RANDOM QUIZ
    @app.route("/quizzes", methods=["POST"])
    def get_quizzes():
        '''
        Description: Get a random question to ask the user depending on the
        category (or all categories) and return a succes in JSON format.
        '''
        data = request.get_json()
        previous_questions = data.get("previous_questions")
        quiz_category = data.get("quiz_category")
        quiz_category_id = int(quiz_category["id"])

        # Excl. all the previous questions
        questions = Question.query.filter(
            Question.id.notin_(previous_questions))

        # Take the first question from the remaining questions array
        # of the corresponding category
        if quiz_category_id:
            new_question = (
                questions.filter_by(
                    category=quiz_category_id).first().format())

        try:
            return jsonify({
                "success": True,
                "question": new_question,
                }), 200
        except BaseException:
            abort(422)
    '''
    B.- ERROR HANDLERS:

    '''
    # 10.- ERROR HANDLERS DEFINITION

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": "bad request"
        }), 400

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

    return app
