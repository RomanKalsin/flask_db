import os
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    Blueprint
)

from src.model.users_repository import UserRepository

index_bp = Blueprint("index", __name__)

@index_bp.route('/')
def index():
    return render_template('index.html', content='Welcome to Flask!')