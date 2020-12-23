import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from app import create_app
from models import setup_db, Movie, Actor

casting_assistant_token = str('Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJUTkNzZ2U1MTFDcnYwdFNQT09IWSJ9.eyJpc3MiOiJodHRwczovL2ZhaGFkeHQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZTBjYmRmZWEzZmM3MDA3ODc2ZDA5NSIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjA4NzA0NTY4LCJleHAiOjE2MDg3OTA5NjgsImF6cCI6InlrZk5Ja1U3SFljZGxERGlZN1V0eE9weXhXSGhpVlZxIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyJdfQ.FjMIIayYDtdTwJDjXV1ju_8ZjO7Ax7nb4FZPUrrWdeVQ05svJ1WJY-cwFblJsJszdDq7kMLZLUVtEcBCJogQF3-JBIEmQ6GzuhQnr8gTzHuYWC1gpMF__23jlQbz6mT49CE4WTn4nZVYWe9l_oXd1UwzjA_VCfg_oBGthKUD233WTv8-2q0ft1OsRCONFobcHB6r1tw0-sAideHz52ZOHuOBmJAoZzyje5yKm-6tJz9ERGEfNPQaVisGKmJW46oOJxC7hlbKi-MVXCAHANre2zMef92XwqbVSUykqvRL0tBZNUrTtrtKm4IRZCHwu2_ayWTbZus0JCvEcz0sTCGiDA')
casting_director_token = str('Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJUTkNzZ2U1MTFDcnYwdFNQT09IWSJ9.eyJpc3MiOiJodHRwczovL2ZhaGFkeHQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZTBjYzNlNTRlYTIwMDA2OWM3NzZkMCIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjA4NzA0NjI1LCJleHAiOjE2MDg3OTEwMjUsImF6cCI6InlrZk5Ja1U3SFljZGxERGlZN1V0eE9weXhXSGhpVlZxIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyJdfQ.anThh94NTir24yboCpwL0Gy675fF13LMTqWe96E1hkudYpp3oHz7ILx-WTUNB8_j5NKu6ZmR4HnI9l4AmYYz_eHRKP7mC3B8EkHXgawnezY3AJV2hADbhzWTcoVrbD00K34yZiC_HjSOJbO9JArgKoMMyDsHlKop-VVp9TzjeOOa3i9MPa2bl3DTtSmRgmy6AK7d0w2WRYxWCyjPb6GH6vQr9TUCf1zY7sF5yXDQMLh7_StBUhOhkihSFKd2fE0SsLXMBVm8gZJb1jt0VWrVnHYyTQkdVQyPdz6oKUwoETznjUa3BnyRMBw0iarI0gBdykv3FvpxRGiPV9Dg8SUpdg')
executive_producer_token = str('Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6ImJUTkNzZ2U1MTFDcnYwdFNQT09IWSJ9.eyJpc3MiOiJodHRwczovL2ZhaGFkeHQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDVmZTBjYzZiNTY5NmFlMDA3MTJlMTFmYSIsImF1ZCI6ImNhcHN0b25lIiwiaWF0IjoxNjA4NzA0NjY3LCJleHAiOjE2MDg3OTEwNjcsImF6cCI6InlrZk5Ja1U3SFljZGxERGlZN1V0eE9weXhXSGhpVlZxIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIiwicGF0Y2g6YWN0b3JzIiwicGF0Y2g6bW92aWVzIiwicG9zdDphY3RvcnMiLCJwb3N0Om1vdmllcyJdfQ.uJ5Auucc6Axro4CXsskRRspsfio9qI6fmtcPb72TE8aJSej8AJDxjXHRCf5bSmm98kiRpnTqgvTyS2tLf9C9L3mbZzKkim73pku97fHtpIm06WWgMkMiNQZy7gnJn4fVkNDg2pKF28vk0xZbVYSebN1Fnx7gHnsdCx2A3r7_UvSQI3HEhl_I1HAZncTmsI63v8MgDDKHpwPdgH6aqJXKYCV6yYF-UFcU6D7q4Sfiw8_wOpSLj3ChzmzjLwdQ8vk64-Oo6I_sT7VV5-cv74QCT19RjABoJP_hEJ2i5cTgbY9Pi2BROA56c5Gc341QXVdQyZxrI2ch2c8V_0ICwS8Y1Q')


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
