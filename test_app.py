import unittest
import os
from .app import create_app
from models import setup_db, db_drop_and_create_all, Actor, Movie
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy


class CapstoneTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        load_dotenv()
        self.database_path = os.environ.get("DATABASE_URL_TEST")
        self.token_assistant = os.environ.get("TOKEN_ASSISTANT")
        self.token_director = os.environ.get("TOKEN_DIRECTOR")
        self.token_producer = os.environ.get("TOKEN_PRODUCER")
        
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path
        })

        self.client = self.app.test_client
        setup_db(self.app, self.database_path)
        db_drop_and_create_all()
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    
    def tearDown(self):
        """Executed after reach test"""
        pass
    
    # movie test
    def test_get_movies_success_role_assistant(self):
        res = self.client().get(
            '/movies', 
            headers={'Authorization': f"Bearer {self.token_assistant}"})
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_movies_error_role_assistant(self):
        res = self.client().get('/movies')
        data = res.get_json()

        self.assertEqual(data["error"], 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Authorization header is expected.")

    def test_add_movies_success_role_producer(self):
        res = self.client().post('/movies', 
            json={
                'title': 'Who created?',
                'release': 'next week'
            },
            headers={'Authorization': f"Bearer {self.token_producer}"}
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_add_movies_error_role_producer(self):
        res = self.client().post('/movies', 
            json={
                'title': 'Who created?'
            },
            headers={'Authorization': f"Bearer {self.token_producer}"}
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Missing required fields')

    def test_update_movie_success_role_director(self):
        with self.app.app_context():
            movie = Movie.query.first()
        res = self.client().patch(
            f"/movies/{movie.id}", 
            json={
                'title': 'Who created update?',
                'release': 'next week'
            },  
            headers={'Authorization': f"Bearer {self.token_director}"}
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIsNotNone(data["movie"])

    def test_update_movie_error_role_assistant(self):
        res = self.client().patch(
            "/movies/1",             
            headers={'Authorization': f"Bearer {self.token_assistant}"}
            )

        data = res.get_json()

        self.assertEqual(data["error"], 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Permission not found.")

    def test_delete_movies_success_role_deirector(self):
        with self.app.app_context():     
          movie = Movie.query.first()
        res = self.client().delete(
            f"/movies/{movie.id}",
            headers={'Authorization': f"Bearer {self.token_director}"}
            )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_movies_error_role_assistant(self):
        res = self.client().delete(
            "/movies/1",
            headers={'Authorization': f"Bearer {self.token_assistant}"}
            )
        data = res.get_json()

        self.assertEqual(data["error"], 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Permission not found.")

    # actor test
    def test_get_actors_success_role_director(self):
        res = self.client().get(
            '/actors', 
            headers={'Authorization': f"Bearer {self.token_director}"})
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_get_actors_error_role_producer(self):
        res = self.client().get('/actors',)
        data = res.get_json()

        self.assertEqual(data["error"], 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Authorization header is expected.")

    def test_add_actors_success_role_producer(self):
        res = self.client().post('/actors', 
            json={
                'name': 'LTA?',
                'age': 18,
                'gender': 'Male'
            },
            headers={'Authorization': f"Bearer {self.token_producer}"}
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_add_actors_error_role_director(self):
        res = self.client().post('/actors', 
            json={
                'name': 'LTA?'
            },
            headers={'Authorization': f"Bearer {self.token_director}"}
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Missing required fields')

    def test_update_actor_success_role_director(self):
        with self.app.app_context():
            actor = Actor.query.first()
        res = self.client().patch(
            f"/actors/{actor.id}", 
            json={
                'name': 'LTA update',
                'gender': 'Male',
                'age' : '19'
            },  
            headers={'Authorization': f"Bearer {self.token_director}"}
        )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertIsNotNone(data["actor"])

    def test_update_actor_error_role_assistant(self):
        res = self.client().patch(
            "/actors/1",             
            headers={'Authorization': f"Bearer {self.token_assistant}"}
            )

        data = res.get_json()

        self.assertEqual(data["error"], 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Permission not found.")

    def test_delete_actors_success_role_producer(self):
        with self.app.app_context():     
          actor = Actor.query.first()
        res = self.client().delete(
            f"/actors/{actor.id}",
            headers={'Authorization': f"Bearer {self.token_producer}"}
            )
        data = res.get_json()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_delete_actors_error_role_assistant(self):
        res = self.client().delete(
            "/actors/1",
            headers={'Authorization': f"Bearer {self.token_assistant}"}
            )
        data = res.get_json()

        self.assertEqual(data["error"], 403)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Permission not found.")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()