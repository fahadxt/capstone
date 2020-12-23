import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Movie, Actor
from flask_migrate import Migrate

from auth.auth import AuthError, requires_auth

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    db = setup_db(app)
    CORS(app)

    # CORS Headers
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers',
                             'Content-Type,Authorization,true')

        response.headers.add('Access-Control-Allow-Methods',
                             'GET,PUT,POST,DELETE,OPTIONS')

        return response


    # endpoint for index 
    @app.route('/')
    def index():
        return jsonify({
            'success': True,
            'msg': 'index',
        })


    # endpoint for all available movies
    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def movies_index(payload):
        movies = Movie.query.order_by(Movie.id).all()
        movies = [movie.format() for movie in movies]

        return jsonify({
          'success': True,
          'movies': movies,
        })


    # endpoint for new movie (store)
    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def movie_store(payload):
      body = request.get_json()
      title = body.get('title', None)
      release_date = body.get('release_date', None)

      try:
        data = Movie(title= title, release_date= release_date)
        data.insert()

        movies = Movie.query.order_by(Movie.id).all()
        movies = [movie.format() for movie in movies]

        return jsonify({
          'success': True,
          'created': data.id,
          'movies': movies,
        })
        

      except:
            abort(422)

    # endpoint for update a movie, and require the 'patch:movies' permission
    @app.route('/movies/<int:id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def movie_update(payload, id):
        body = request.get_json()
        movie = Movie.query.filter(Movie.id == id).one_or_none()

        try:
            title = body.get('title')
            release_date = body.get('release_date')

            if title:
                movie.title = title

            if release_date:
                movie.release_date = release_date

            movie.update()

        except BaseException:
            abort(422)

        return jsonify({
            'success': True,
            'movies': [movie.format()]
        })

    # endpoint for DELETE a movie by id (destroy) 
    @app.route("/movies/<int:id>", methods=['DELETE'])
    @requires_auth('delete:movies')
    def movie_destroy(payload, id):
      try:
        data = Movie.query.get(id)
        data.delete()

        return jsonify({
            'success': True,
            'deleted': id
        })
      except:
        abort(422)



    # endpoint for all available actors
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def actors_index(payload):
        actors = Actor.query.order_by(Actor.id).all()
        actors = [actor.format() for actor in actors]

        return jsonify({
          'success': True,
          'actors': actors,
        })

    # endpoint for new actor (store)
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def actor_store(payload):
      body = request.get_json()
      name = body.get('name', None)
      age = body.get('age', None)
      gender = body.get('gender', None)

      try:
        data = Actor(
          name= name, 
          age= age,
          gender= gender
        )
        data.insert()

        actors = Actor.query.order_by(Actor.id).all()
        actors = [actor.format() for actor in actors]

        return jsonify({
          'success': True,
          'created': data.id,
          'actors': actors,
        })
        

      except:
            abort(422)

    # endpoint for update a actors, and require the 'patch:actors' permission
    @app.route('/actors/<int:id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def actor_update(payload, id):
        body = request.get_json()
        actor = Actor.query.filter(Actor.id == id).one_or_none()

        try:
            name = body.get('name')
            age = body.get('age')
            gender = body.get('gender')

            if name:
                actor.name = name

            if age:
                actor.age = age

            if gender:
                actor.gender = gender

            actor.update()

        except BaseException:
            abort(422)

        return jsonify({
            'success': True,
            'actor': [actor.format()]
        })

    # endpoint for DELETE a actor by id (destroy) 
    @app.route("/actors/<int:id>", methods=['DELETE'])
    @requires_auth('delete:actors')
    def actor_destroy(payload, id):
      try:
        data = Actor.query.get(id)
        data.delete()

        return jsonify({
            'success': True,
            'deleted': id
        })


      except:
        abort(422)



    # Error Handling
    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    @app.errorhandler(400)
    def bad_request(error):
        return jsonify({
            "success": False,
            "error": 400,
            "message": 'Bad Request'
        }), 400

    @app.errorhandler(404)
    def not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    # error handler for AuthError
    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
