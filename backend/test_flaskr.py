import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia"
        self.database_path = "postgresql://{}/{}".format('postgres:Medongleopoldine1@localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after each test"""
        print("*******************************************")
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # GET /categories : successful and failure request for getting categories
    def test_get_categories(self):
        res = self.client().get('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['categories'])

    def test_get_categories_405(self):
        res = self.client().post('/categories')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 405)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Method not allowed')

    # GET /questions : successful and failure request for getting questions
    def test_get_questions(self):
        res = self.client().get('/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['categories'])

    def test_get_questions_404(self):
        res = self.client().get('/books?page=1000')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # DELETE /questions/id : successful and failure request for deleting question
    def test_delete_question(self):
        res = self.client().delete('/questions/19')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['deleted_id'])

    def test_delete_question_422(self):
        res = self.client().delete('/questions/0')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Processable')

    # POST /questions : successful and failure request for creating a question
    def test_create_question(self):
        body = {
            'question': "When is the factise monotonie provendirisi conta",
            'answer': "Salvidi",
            'category': 3,
            'difficulty': 5
        }
        res = self.client().post('/questions', json=body)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data, {})

    def test_create_question_400_422(self):
        body = {
            'question': "When is the factise monotonie provendirisi conta",
            'category': 3
        }
        res = self.client().post('/questions', json=body)
        data = json.loads(res.data)
        self.assertIn(res.status_code, [400, 422])
        self.assertEqual(data['success'], False)
        self.assertIn(data['message'], ['Not Processable', 'Bad Request'])

    # POST /questions : successful and failure request for searching questions
    def test_search_question_by_term(self, body=None):
        if body is None:
            body = {
                'searchTerm': "What is",
            }
        res = self.client().post('/questions', json=body)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])

    def test_search_question_by_term_500(self):
        body = {}
        res = self.client().post('/questions', json=body)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Not Processable')

    # GET /categories/{id}/questions : successful and failure request for getting questions in a given category
    def test_get_questions_of_category(self):
        res = self.client().get('categories/2/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['questions'])
        self.assertTrue(data['totalQuestions'])
        self.assertTrue(data['currentCategory'])

    def test_get_questions_of_category_404(self):
        res = self.client().get('categories/0/questions')
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Resource Not Found')

    # POST /quizzes : successful and failure request for playing quizzes
    def test_quizzes(self):
        body = {
            'previous_questions': [1, 5, 8],
            'quiz_category': {"type": "Art", "id": 2}
        }
        res = self.client().post('/quizzes', json=body)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['question'])

    def test_quizzes_500(self):
        body = {
            'previous_questions': [1, 5, 8]
        }
        res = self.client().post('/quizzes', json=body)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 500)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Internal Server Error')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
