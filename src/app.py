import os
import psycopg2
from dotenv import load_dotenv
from flask import Flask
from src.controllers.users_controller import users_bp
from src.controllers.index import index_bp

app = Flask(__name__)

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

conn = psycopg2.connect(os.getenv('DATABASE_URL'))
app.config['conn'] = conn

app.register_blueprint(users_bp)
app.register_blueprint(index_bp)
