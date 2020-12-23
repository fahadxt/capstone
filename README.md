# Capstone ❤️ 

## Getting Started 

### Installing Dependencies

#### Python 3.7

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

#### Virtual Enviornment

We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

#### PIP Dependencies

Once you have your virtual environment setup and running, install dependencies by running:

```bash
pip install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

##### Key Dependencies

- [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

- [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

- [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 



### Running the server

ensure you are working using your created virtual environment, and to run the server, execute:

```bash
export FLASK_APP=app.py;
export FLASK_ENV=development
flask run --reload
```

Setting the `FLASK_ENV` variable to `development` will detect file changes and restart the server automatically.

### API ✨

#### `GET` `/movies` 
#### Endpoint for get all available movies
**-** **Response result** (example):
```
{
    "movies": [
        {
            "id": 1,
            "release_date": "Thu, 03 Sep 2020 00:00:00 GMT",
            "title": "Tenet"
        }
    ],
    "success": true
}
```

------

#### `GET` `/actors` 
#### Endpoint for get all available actors in the database
**-** **Request arguments**: Accept only integer "Page Number"

**-** **Response result** (example): `/actors`
```
{
    "actors": [
        {
            "age": 36,
            "gender": "male",
            "id": 1,
            "name": "John David Washington"
        },
    ],
    "success": true
}
```

------

#### `DELETE` `/movies/<int:id>` 
#### Endpoint for delete a movie by id.
**-** **Request arguments** : Accept only integer "Movie ID"

**-** **Response result** (example): `'/movies/1'`
```
{
    "deleted": "1",
    "success": true
}
```

------

#### `DELETE` `/actors/<int:id>` 
#### Endpoint for delete a actors by id.
**-** **Request arguments** : Accept only integer "Actor ID"

**-** **Response result** (example): `'/actors/1'`
```
{
    "deleted": "1",
    "success": true
}
```

------

#### `POST` `/movies` 
####  Endpoint for create a new movie
**-** **Request body**
```
{
    "title": "string",
    "release_date": "date"
}
```
**-** **Response result** (example) :
```
{
    "success": True,
    "created": 2,
    "movies": [
        {
            "id": 1,
            "release_date": "Thu, 03 Sep 2020 00:00:00 GMT",
            "title": "Tenet"
        },
        {
            "id": 2,
            "release_date": "Thu, 14 May 2020 00:00:00 GMT",
            "title": "Mad Max: Fury Road"
        },
    ],  
}
```

------

#### `POST` `/actors` 
####  Endpoint for create a new actor
**-** **Request body**
```
{
    "age": Integer,
    "gender": "String",
    "name": "String"
}
```
**-** **Response result** (example) :
```
{
    "success": True,
    "created": 2,
    "actors": [
        {
            "age": 36,
            "gender": "male",
            "id": 1,
            "name": "John David Washington"
        },
        {
            "age": 43,
            "gender": "male",
            "id": 2,
            "name": "Tom Hardy"
        }
    ],  
}
```
    
------

#### `PATCH` `/movies/<int:id>` 
####  Endpoint for update a movie
**-** **Request arguments** : Accept only integer "Movie ID"
**-** **Request body**
```
{
    "title": "String",
    "release_date": "Date",
}
```
**-** **Response result** (example) :
```
{
    "movies": [
        {
            "id": 2,
            "release_date": "Thu, 14 May 2020 00:00:00 GMT",
            "title": "Mad Max: Fury Road 2"
        }
    ],
    "success": true
}
```
    
------

#### `PATCH` `/actors/<int:id>` 
####  Endpoint for update a actor
**-** **Request arguments** : Accept only integer "Actor ID"
**-** **Request body**
```
{
    "age": Integer,
    "gender": "String",
    "name": "String"
}
```
**-** **Response result** (example) :
```
{
    "actor": [
        {
            "age": 43,
            "gender": "male",
            "id": 2,
            "name": "Tom Hardy 2"
        }
    ],
    "success": true
}
```
    
------
    



    

### Testing
To run the tests, run
```bash
python test_app.py
```
