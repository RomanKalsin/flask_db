import os
from dotenv import load_dotenv
from flask import (
    Flask,
    render_template,
    Blueprint,
    current_app
)

from src.model.users_repository import UserRepository

users_bp = Blueprint("users", __name__, url_prefix="/users")

def get_repo():
    conn = current_app.config["conn"]
    return UserRepository(conn)

@users_bp.route('/')
def get_users():
    content = get_repo().get_content()
    return render_template('users/index.html', users=content)


@users_bp.route('/<id>')
def users_show(id):
    content = get_repo().find(id)
    return render_template('users/show.html', user=content)
