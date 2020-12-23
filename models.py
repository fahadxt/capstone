import os
from sqlalchemy import Column, String, Integer, Date, DateTime
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

database_name = "capstone"
database_path = "postgresql://{}:{}@{}/{}".format(
    'postgres', 'root', 'localhost:5432', database_name)

db = SQLAlchemy()
migrate = Migrate()


def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get('DATABASE_URL', database_path) 
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    migrate.init_app(app, db)


class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    release_date = Column(Date)
    created_at = Column(DateTime, server_default=db.func.now())
    updated_at = Column(DateTime, server_default=db.func.now(),
                        server_onupdate=db.func.now())

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            # 'created_at': self.created_at,
        }


class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    age = Column(Integer)
    gender = Column(String)
    created_at = Column(DateTime, server_default=db.func.now())
    updated_at = Column(DateTime, server_default=db.func.now(),
                        server_onupdate=db.func.now())

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def insert(self):
      db.session.add(self)
      db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
        }

def drop_and_migrate_test():
  db.drop_all
  db.create_all