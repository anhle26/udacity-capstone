import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

from models import db_drop_and_create_all, setup_db, Movie, Actor
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)

  if test_config is None:
    setup_db(app)
    db_drop_and_create_all()
  else:
    database_path = test_config.get('SQLALCHEMY_DATABASE_URI')
    setup_db(app, database_path=database_path)
    db_drop_and_create_all()

  CORS(app)

  @app.route('/')
  def get_greeting():
      excited = os.environ['EXCITED']
      greeting = "Hello" 
      if excited == 'true': 
          greeting = greeting + "!!!!! You are doing great in this Udacity project."
      return greeting

  '''
  Get list movies
  '''
  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def get_list_movies(payload):
    try:
      list_movies = Movie.query.all()
      
      if len(list_movies) == 0: 
        abort(404, description=str('Movie not found!'))

      movies = [movie.format() for movie in list_movies]
      return jsonify({
        "success": True,
        "movies": movies
      }), 200
    
    except Exception as e:
      abort(404, description=str(e))

  '''
  Delete movie by Id
  '''
  @app.route('/movies/<int:id>', methods=['DELETE'])
  @requires_auth('delete:movies')
  def delete_movies(payload, id): 
    movie_id = id
    movie = Movie.query.filter_by(id=movie_id).one_or_none()
    if movie is None:
      abort(404, description="Movie not found!")

    try:
      movie.delete()
      return jsonify({
        'success': True,
        'delete': movie_id
      }), 200

    except Exception as e:
      abort(404, description = (str(e)))

  '''
  Create movie
  '''
  @app.route('/movies', methods=['POST'])
  @requires_auth('post:movies')
  def create_movies(payload):
    body = request.get_json()

    if 'title' not in body or 'release' not in body:
      abort(404, description = 'Missing required fields')

    title = body['title']
    release = body['release']

    try:
      movie = Movie(title=title, release=release)
      movie.insert()

      return jsonify({
        'success': True,
        'movie': movie.format()
      }), 200
    
    except Exception as e:
      abort(404, description = (str(e)))

  ''' 
  '''
  @app.route('/movies/<int:id>', methods=['PATCH'])
  @requires_auth('patch:movies')
  def update_movies(payload, id):
    body = request.get_json()
    movie_id = id
    movie = Movie.query.filter_by(id=movie_id).one_or_none()
    if movie is None:
      abort(404, description="Movie not found!")

    if 'title' not in body and 'release' not in body:
      abort(404, description = 'Missing required fields')
    
    if 'title' in body:
      movie.title = body['title']
    if 'release' in body:
      movie.release = body['release']

    try:
      movie.update()

      return jsonify({
        'success': True,
        'movie': movie.format()
      }), 200

    except Exception as e:
      abort(404, description = (str(e)))

  '''
  Get list actors
  '''
  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def get_list_actors(payload):
    try:
      list_actors = Actor.query.all()
      
      if len(list_actors) == 0: 
        abort(404, description=str('Actor not found!'))

      actors = [actor.format() for actor in list_actors]
      return jsonify({
        "success": True,
        "actors": actors
      }), 200
    
    except Exception as e:
      abort(404, description=str(e))

  '''
  Delete actor by Id
  '''
  @app.route('/actors/<int:id>', methods=['DELETE'])
  @requires_auth('delete:actors')
  def delete_actors(payload, id): 
    actor_id = id
    actor = Actor.query.filter_by(id=actor_id).one_or_none()
    if actor is None:
      abort(404, description="Actor not found!")

    try:
      actor.delete()
      return jsonify({
        'success': True,
        'delete': actor_id
      }), 200

    except Exception as e:
      abort(404, description = (str(e)))

  '''
  Create actor
  '''
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def create_actors(payload):
    body = request.get_json()

    if 'name' not in body or 'age' not in body or 'gender' not in body:
      abort(404, description = 'Missing required fields')

    name = body['name']
    age = body['age']
    gender = body['gender']

    try:
      actor = Actor(name=name, age=age, gender=gender)
      actor.insert()

      return jsonify({
        'success': True,
        'actor': actor.format()
      }), 200
    
    except Exception as e:
      abort(404, description = (str(e)))

  ''' 
  '''
  @app.route('/actors/<int:id>', methods=['PATCH'])
  @requires_auth('patch:actors')
  def update_actors(payload, id):
    body = request.get_json()
    actor_id = id
    actor = Actor.query.filter_by(id=actor_id).one_or_none()
    if actor is None:
      abort(404, description="Actor not found!")

    if 'name' not in body or 'age' not in body or 'gender' not in body:
      abort(404, description = 'Missing required fields')
    
    if 'name' in body:
      actor.name = body['name']
    if 'age' in body:
      actor.age = body['age']
    if 'gender' in body:
      actor.gender = body['gender']

    try:
      actor.update()

      return jsonify({
        'success': True,
        'actor': actor.format()
      }), 200

    except Exception as e:
      abort(404, description = (str(e)))


  @app.errorhandler(404)
  def not_found_error(error):
    return jsonify({
      "success": False,
      "error": 404,
      "message":  error.description if error.description else "Resource not found"
    }), 404

  @app.errorhandler(422)
  def unprocessable_error(error):
    return jsonify({
      "success": False,
      "error": 422,
      "message": error.description if error.description else "Unprocessable entity"
    }), 422

  return app

app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)