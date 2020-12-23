import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

casting_assistant_token = str('Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJUTkNzZ2U1MTFDcnYwdFNQT09IWSJ9.eyJpc3MiOiJodHRwczovL2ZhaGFkeHQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZTBjYmRmZWEzZmM3MDA3ODc2ZDA5NSIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjA4Njc1MDYzLCJleHAiOjE2MDg3NjE0NjMsImF6cCI6InlrZk5Ja1U3SFljZGxERGlZN1V0eE9weXhXSGhpVlZxIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.r9QU7rs9tYs0p5Wn1TmBPTV6xvjuV7Shyk8jWeSNkZT0jXMjBAqkAup-OjQSY_XPBMN9mVNQOAvWCUtrHF9onJA_HaRR5EyQVrXleVth-UUtepi-a5Z7nkFaWwb-n6Zd3qYlUX-tsCoA58fT8Cz243XhV9LInZUwdXO9pfZh-JmO_VFr6ORoYv8yoF59QjCjRJp5-q65L_N7V1xux81l4xAHya1BuINliqYqR1Vpu3kUA5Niu77yOe43XfXFif2zmRKhdjHSryb4DmZ78qykcTlZI_uZIxMm_EiHIlBALzCZIDiTPPn4O-wsPByhrGXqnvc29DSWheFYKh9sqlPYHg')
casting_director_token = str('Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJUTkNzZ2U1MTFDcnYwdFNQT09IWSJ9.eyJpc3MiOiJodHRwczovL2ZhaGFkeHQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZTBjYzNlNTRlYTIwMDA2OWM3NzZkMCIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjA4Njc1MTY5LCJleHAiOjE2MDg3NjE1NjksImF6cCI6InlrZk5Ja1U3SFljZGxERGlZN1V0eE9weXhXSGhpVlZxIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.TlTjtH4r5z1k7ftVLdu2ukpNX7I4eXh5mFwj4gB1daLxwXtf2YAXOH0Y8zYof0vX5p80nGHthbaTa2U0JVwPIU3E__Mz2tlabhdpFySBexgG6PIjYLvar6y_OiPlFe1NMHwkWzetGGtskAKCo-NHRXJ7q_ChjYUpotoH4cN8QS1P0Exe05jErvvpuWZQHx4HfPcwMSbQEUmMaIZLmisN2Ohl86fqqegdbYXxy0VvXBtsJ-PfkDf4qx4FAPP_PR8wDP4OhuCi2GcWx4FntkmpfIh734oDRu63N9Z8O1fCpXlziPM0E1ZQcToA5ZF9cA3BV0JVobBDuYZlQhVbAYGYvw')
executive_producer_token = str('Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJUTkNzZ2U1MTFDcnYwdFNQT09IWSJ9.eyJpc3MiOiJodHRwczovL2ZhaGFkeHQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZTBjYzZiNTY5NmFlMDA3MTJlMTFmYSIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjA4Njc1MzAyLCJleHAiOjE2MDg3NjE3MDIsImF6cCI6InlrZk5Ja1U3SFljZGxERGlZN1V0eE9weXhXSGhpVlZxIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.wb44p5tDwGoY-56QsYKYTLTCHZLL4B8XQ59g5ut36-W8v2yqM3OuQREuQJS07g-s7x-7w_YrlWwhyBmHf7xd-01LD2bPzsUlgDmvZ3Ac9g0xOrJRaB-EY2rr-3z6uYvlpKETvGu0PijdMMtFDRR4NYt8fxJjNI8NfgRfpOv0ZISHZJiwdsV6u9j2V3FprxysuPHG7rBopJWDDXWLT2EFWXDH3bgZE2iNXNHQvBRB-4sMwOFDD04zWRLsvNAjzzzS8jyAKhzGk1aXyJN1mT-ood9IDGn_CigFZOmMpG8k9qKdO8mp9KVcvHl_0bN3-5AuDr9N3-9Kx7L59Pq37IO3GA')


class CapstoneTestCase(unittest.TestCase):
    """This class represents the capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "capstone"
        self.database_path = "postgresql://{}:{}@{}/{}".format(
            'postgres', 'root', 'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.casting_assistant = {
            'Content-Type': 'application/json', 'Authorization': casting_assistant_token}
        self.casting_director = {
            'Content-Type': 'application/json', 'Authorization': casting_director_token}
        self.executive_producer = {
            'Content-Type': 'application/json', 'Authorization': executive_producer_token}
        self.db = SQLAlchemy()

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_movies_index_without_token(self):
        response = self.client().get('/movies', headers=None)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)

    def test_movies_index_with_token(self):
        response = self.client().get('/movies', headers=self.casting_assistant)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_movie_store_without_token(self):
        response = self.client().post('/movies', headers=None, json={
            "title": "test_movie_store_without_token1",
            "release_date": "01-01-2020"
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)

    def test_movie_store_with_token(self):
        response = self.client().post('/movies', headers=self.executive_producer, json={
            "title": "test_movie_store_with_token2",
            "release_date": "01-01-2020"
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_movie_update_without_token(self):
        movie = Movie(title='test_movie_update_without_token3',
                      release_date='01-01-2020')
        movie.insert()
        response = self.client().patch('/movies/' + str(movie.id), headers=None, json={
            "title": "test_movie_update_without_token3",
            "release_date": "01-01-2020"
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        movie.delete()

    def test_movie_update_with_token(self):
        movie = Movie(title='test_movie_update_with_token4',
                      release_date='01-01-2020')
        movie.insert()

        response = self.client().patch('/movies/' + str(movie.id), headers=self.executive_producer, json={
            "title": "test_movie_update_with_token4",
            "release_date": "01-01-2020"
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        movie.delete()

    def test_movie_update_unprocessable(self):
        response = self.client().patch('/movies/0', headers=self.executive_producer, json={
            "age": "0",
            "gender": "male",
            "name": "test_movie_update_unprocessable"
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_movie_destroy_without_token(self):
        movie = Movie(title='test_movie_destroy_without_token5',
                      release_date='01-01-2020')
        movie.insert()

        response = self.client().patch('/movies/' + str(movie.id), headers=None)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        movie.delete()

    def test_movie_destroy_with_token(self):
        movie = Movie(title='test_movie_destroy_with_token6',
                      release_date='01-01-2020')
        movie.insert()

        response = self.client().delete('/movies/' + str(movie.id),
                                        headers=self.executive_producer)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_movie_destroy_unprocessable(self):
        response = self.client().delete('/movies/0', headers=self.executive_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_actors_index_without_token(self):
        response = self.client().get('/actors', headers=None)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)

    def test_actors_index_with_token(self):
        response = self.client().get('/actors', headers=self.casting_assistant)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_actor_store_without_token(self):
        response = self.client().post('/actors', headers=None, json={
            "age": "1",
            "gender": "male",
            "name": "test_actor_store_without_token"
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)

    def test_actor_store_with_token(self):
        response = self.client().post('/actors', headers=self.executive_producer, json={
            "age": "2",
            "gender": "male",
            "name": "test_actor_store_with_token"
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_actor_update_without_token(self):
        actor = Actor(age='3', gender='male',
                      name='test_actor_update_without_token')
        actor.insert()

        response = self.client().patch('/actors/' + str(actor.id), headers=None, json={
            "age": "33",
            "gender": "male",
            "name": "test_actor_update_without_token33"
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)

        actor.delete()

    def test_actor_update_with_token(self):
        actor = Actor(age='4', gender='male',
                      name='test_actor_update_with_token')
        actor.insert()

        response = self.client().patch('/actors/' + str(actor.id), headers=self.executive_producer, json={
            "age": "44",
            "gender": "male",
            "name": "test_actor_update_with_token44"
        })
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

        actor.delete()

    def test_actor_update_unprocessable(self):
        response = self.client().patch('/actors/0', headers=self.executive_producer, json={
            "age": "0",
            "gender": "male",
            "name": "test_actor_update_unprocessable"
        })
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')

    def test_actor_destroy_without_token(self):
        actor = Actor(age='5', gender='male',
                      name='test_actor_destroy_without_token')
        actor.insert()

        response = self.client().patch('/actors/' + str(actor.id), headers=None)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)
        actor.delete()

    def test_actor_destroy_with_token(self):
        actor = Actor(age='6', gender='male',
                      name='test_actor_destroy_with_token')
        actor.insert()

        response = self.client().delete('/actors/' + str(actor.id),
                                        headers=self.executive_producer)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_actor_destroy_unprocessable(self):
        response = self.client().delete('/actors/0', headers=self.executive_producer)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'unprocessable')


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
