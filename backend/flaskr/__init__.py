import json
import os
from json.decoder import JSONDecodeError

from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)

    """
    @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
    """
    resources = {r'/api/*': {'origin': '*'}}
    CORS(app, resources=resources)

    """
    @TODO: Use the after_request decorator to set Access-Control-Allow
    """
    @app.after_request
    def after_request(response):
        print(response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization, true'))
        print(response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE'))
        return response

    """
    @TODO:
    Create an endpoint to handle GET requests
    for all available categories.
    """
    @app.route('/categories', methods=['GET'])
    def get_categories():
        categories = Category.query.all()
        categories = {x.id: x.type for x in categories}

        return jsonify({
            'categories': categories
        })

    """
    @TODO:
    Create an endpoint to handle GET requests for questions,
    including pagination (every 10 questions).
    This endpoint should return a list of questions,
    number of total questions, current category, categories.
    
    TEST: At this point, when you start the application
    you should see questions and categories generated,
    ten questions per page and pagination at the bottom of the screen for three pages.
    Clicking on the page numbers should update the questions.
    """
    @app.route('/questions')
    def get_questions():
        page = request.args.get('page', 1, type=int)
        start = (page - 1) * QUESTIONS_PER_PAGE
        end = start + QUESTIONS_PER_PAGE
        questions = Question.query.all()
        questions = [x.format() for x in questions]

        if questions is None or len(questions) == 0:
            abort(404)

        return jsonify({
            'questions': questions[start:end],
            'totalQuestions': len(questions),
            'currentCategory': None,
            'categories': {x.id: x.type for x in Category.query.all()}
        })

    """
    @TODO:
    Create an endpoint to DELETE question using a question ID.

    TEST: When you click the trash icon next to a question, the question will be removed.
    This removal will persist in the database and when you refresh the page.
    """
    @app.route('/questions/<int:id_q>', methods=['DELETE'])
    def delete_question(id_q):
        question = Question.query.get(id_q)

        if question is None:
            abort(422)
        question.delete()

        return jsonify({
            'status_code': 200,
            'deleted_id': id_q
        })

    """
    @TODO:
    Create an endpoint to POST a new question,
    which will require the question and answer text,
    category, and difficulty score.

    TEST: When you submit a question on the "Add" tab,
    the form will clear and the question will appear at the end of the last page
    of the questions list in the "List" tab.
    """
    @app.route('/questions', methods=['POST'])
    def create_question():
        try:
            data = json.loads(request.data)
            if data['question'] is None or data['answer'] is None or data['category'] is None or data['difficulty'] is None:
                abort(400)

            question = Question(question=data['question'], answer=data['answer'], category=data['category'], difficulty=data['difficulty'])
            question.insert()

            return jsonify({})
        except JSONDecodeError as json_error:
            print(json_error.__str__())
            return abort(500)
        except:
            # Redirect to search in case is not a question creation
            return search_question_by_term()

    """
    @TODO:
    Create a POST endpoint to get questions based on a search term.
    It should return any questions for whom the search term
    is a substring of the question.

    TEST: Search by any phrase. The questions list will update to include
    only question that include that string within their question.
    Try using the word "title" to start.
    """
    @app.route('/questions', methods=['POST'])
    def search_question_by_term():
        data = json.loads(request.data)
        try:
            term = '%{0}%'.format(data['searchTerm'])
            questions = Question.query.filter(Question.question.ilike(term))
            questions = [x.format() for x in questions]

            return jsonify({
                'questions': questions,
                'totalQuestions': len(questions),
                'currentCategory': None
            })
        except:
            # Exit in cas it is not question creation or question search by term
            abort(422)

    """
    @TODO:
    Create a GET endpoint to get questions based on category.

    TEST: In the "List" tab / main screen, clicking on one of the
    categories in the left column will cause only questions of that
    category to be shown.
    """
    @app.route('/categories/<int:id_q>/questions', methods=['GET'])
    def get_category(id_q):
        # Find if the category exists
        cur_category = Category.query.get(id_q)
        if cur_category is None:
            abort(404)
        questions = Question.query.filter_by(category=str(id_q))
        questions = [x.format() for x in questions]

        return jsonify({
            'questions': questions,
            'totalQuestions': len(questions),
            'currentCategory': cur_category.type
        })

    """
    @TODO:
    Create a POST endpoint to get questions to play the quiz.
    This endpoint should take category and previous question parameters
    and return a random questions within the given category,
    if provided, and that is not one of the previous questions.

    TEST: In the "Play" tab, after a user selects "All" or a category,
    one question at a time is displayed, the user is allowed to answer
    and shown whether they were correct or not.
    """
    @app.route('/quizzes', methods=['POST'])
    def quizze():
        data = json.loads(request.data)

        try:
            prev = data['previous_questions']
            cur_category = data['quiz_category']
            category = Category.query.get(cur_category['id'])
            if category is None:
                pos_questions = Question.query.all()
            else:
                pos_questions = Question.query.filter_by(category=str(category.id))
            pos_questions = [x for x in pos_questions]
            for ques in pos_questions:
                if ques.id in prev:
                    pos_questions.remove(ques)

            question = random.choice(pos_questions)

            return jsonify({
                'question': question.format()
            })

        except Exception as e:
            print(e.__str__())
            abort(500)

    """
    @TODO:
    Create error handlers for all expected errors
    including 404 and 422.
    """
    @app.errorhandler(400)
    def handle_400(error):
        return jsonify({
            'success': False,
            'error': 400,
            'message': 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def handle_404(error):
        return jsonify({
            'success': False,
            'error': 404,
            'message': 'Resource Not Found'
        }), 404

    @app.errorhandler(405)
    def handle_405(error):
        return jsonify({
            'success': False,
            'error': 405,
            'message': 'Method not allowed'
        }), 405

    @app.errorhandler(422)
    def handle_422(error):
        return jsonify({
            'success': False,
            'error': 422,
            'message': 'Not Processable'
        }), 422

    @app.errorhandler(500)
    def handle_500(error):
        return jsonify({
            'success': False,
            'error': 500,
            'message': 'Internal Server Error'
        }), 500

    return app

