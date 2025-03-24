import os
from apiflask import APIFlask
from dotenv import load_dotenv

load_dotenv()

app = APIFlask(__name__)

HOST = os.getenv('HOST') or 'localhost'
PORT = int(os.getenv('PORT') or 5000)

app.config['HOST'] = HOST
app.config['PORT'] = PORT
