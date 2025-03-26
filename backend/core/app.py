import os
from apiflask import APIFlask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS


load_dotenv()


ENV = os.getenv('ENV') or 'development'
HOST = os.getenv('HOST') or 'localhost'
PORT = int(os.getenv('PORT') or 5000)

app = APIFlask(__name__, title='Parking AI API', version='0.0.1', enable_openapi=ENV == 'development')
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['HOST'] = HOST
app.config['PORT'] = PORT

db = SQLAlchemy(app)
