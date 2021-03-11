import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    # # Original - Jorge Villarroel
    # def setUp(self):
    #     """Define test variables and initialize app."""
    #     self.app = create_app()
    #     self.client = self.app.test_client
    #     self.database_name = "trivia_test"
    #     self.database_path = "postgres://{}/{}".format(
    #         'localhost:5432', self.database_name)
    #     setup_db(self.app, self.database_path)

    #     # binds the app to the current context
    #     with self.app.app_context():
    #         self.db = SQLAlchemy()
    #         self.db.init_app(self.app)
    #         # create all tables
    #         self.db.create_all()

    # Suggested by Udacity's project reviewer
    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.DB_HOST = os.getenv('DB_HOST', '127.0.0.1:5432')
        self.DB_USER = os.getenv('DB_USER', 'postgres')
        self.DB_PASSWORD = os.getenv('DB_PASSWORD', 'postgres')
        self.DB_NAME = os.getenv('DB_NAME', 'trivia_test')
        self.DB_PATH = 'postgresql+psycopg2://{}:{}@{}/{}'.format(
            self.DB_USER,
            self.DB_PASSWORD,
            self.DB_HOST,
            self.DB_NAME)
        
        setup_db(self.app, self.DB_PATH)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass
    
    def test_get_categories(self):
        '''Get existing categories'''
        res = self.client().get('/categories')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(len(data['categories']))

    def test_get_questions(self):
        '''Get existing questions'''
        res = self.client().get('/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])        

    def test_delete_question(self):
        '''Delete a question. For testing purposes a new question will be created and the same will be deleted.'''

        # Create a new sample question to be deleted.
        test_question = {
            'question': 'Just a sample question to be deleted.',
            'answer': 'Just a sample answer',
            'difficulty': 1,
            'category': '1'
        }

        new_question = Question(
            question = test_question['question'],
            answer = test_question['answer'],
            category = test_question['category'],
            difficulty = test_question['difficulty'],
        )

        new_question.insert()

        question_id = new_question.id

        # Delete the question created
        res = self.client().delete('/questions/{}'.format(question_id))
        data = json.loads(res.data)
        
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_create_new_question(self):
        '''Create new question'''
        
        new_question = {
            'question': 'How many "Copa America" cups has Chile won?',
            'answer': '2',
            'difficulty': 2,
            'category': '6'
        }

        res = self.client().post('/questions', json=new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
    
    def test_get_searchTerm(self):
        '''Search for a term in the questions available'''
        searchTerm = 'What'
        res = self.client().get('/questions', json={'searchTerm': searchTerm})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    def test_get_questions_by_category(self):
        '''Get questions by category. For testing purposes it will be category 5 = Entertainment'''
        res = self.client().get(
            '/categories/5/questions')
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])

    def test_play_quiz(self):
        """Test when playing game"""
        response = self.client().post(
            '/quizzes',
            json={
                'previous_questions': [8, 9],
                'quiz_category': {'type': 'Geography', 'id': '2'}})
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()