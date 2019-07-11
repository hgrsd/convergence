# Convergence
### _A REStful API and Frontend to help you find the ideal place to meet._

Convergence is a RESTful API and Frontend built using Flask and using the Google Maps API that helps groups of friends, colleagues, or acquiantances, find the ideal place to meet.
Users of Convergence can create events and invite their friends to these events. When invitees have responded, Convergence will suggest the most suitable places, based on distance, travel times, and ratings, to meet with all those who are keen to attend.

## **Setting up the Backend**

### 1. Dependencies and environment
- Before installing the Convergence app, please make sure that PostgresQL is installed on your system and the service is running. 
- Install the required dependencies and Python environment by navigating to the Convergence root folder and using the following command:
```sh
pipenv install
```
### 2. Setting up the database

- Set up a new PostgresQL database for your app to use, e.g. by using the createdb command:
``` sh
createdb <db name>  # e.g. createdb convergence
```
- Note: if you want to have a database for testing purposes, you may use the `seed.py` script to -fill your database with test data: 
```sh
seed.py <database name> <random seed>
```

- If you have not used the seed.py script, then you must set up the database schema using the manage.py script in the root folder, as follows:
```Python
manage.py db init
manage.py db migrate
manage.py db upgrade
```

### 3. Setting up the configuration file

- Next, create a `config.py` file in `convergence/instance` to hold your API, Flask, database, and other private configuration variables. Add the following variables to the file.
```Python
SECRET_KEY = 'your secret key here'  # Flask secret key
SQLALCHEMY_TRACK_MODIFICATIONS = False 
DB_URL = "postgresql://localhost/convergence"  # PostgresQL database URL
GM_API_KEY = "APIKEY"  # Your google API key
```

### 4. Running the Flask app

- To run the backend, navigate to the root folder and start the app using `run.py`
- This will run in production mode. For debug mode, set the FLASK_DEBUG env var to True before running `run.py`:
```sh
export FLASK_DEBUG=True
```

## **Building the Web Frontend**

- Install node and npm with your package manager of choice.
- Navigate to the folder with all the frontend content:
```sh
cd convergence/static
```
- Install all dependencies with:
```sh
npm install
```
- When deploying to stage or production build distribution with:
```sh
npm run build-prod
```
- When debugging use:
```sh
npm run build-debug
```
- Or build and remain in watch mode with:
```sh
npm start
```
