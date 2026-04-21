from flask import (
    render_template,
    Blueprint,
    current_app,
    request,
    redirect,
    url_for,
    flash,
    get_flashed_messages,
    g
)

from src.model.users_repository import UserRepository
from src.model.validators import validate_user

users_bp = Blueprint("users", __name__, url_prefix="/users")

def get_repo():
    if 'conn' not in g:
        g.conn = psycopg2.connect(current_app.config['DATABASE_URL'])
    return UserRepository(g.conn)
#    conn = current_app.config["conn"]
#    return UserRepository(conn)

@users_bp.teardown_request
def close_conn(error):
    conn = g.pop('conn', None)
    if conn is not None:
        conn.close()

@users_bp.route('/')
def get_users():
    query = request.args.get('query', '')
    if query:
        content = get_repo().get_by_term(query)
    else:
        content = get_repo().get_content()
    messages = get_flashed_messages(with_categories=True)
    return render_template('users/index.html', users=content, search=query, messages=messages)

@users_bp.route('/<int:id>')
def users_show(id):
    content = get_repo().find(id)
    if content is None:
        return "Oops!", 404
    return render_template('users/show.html', user=content)

@users_bp.route('/new')
def users_new():
    errors = {}
    user = {
        'name': '',
        'email': ''
    }
    return render_template('users/new.html', user=user, errors=errors)

@users_bp.route('/', methods=['POST'])
def users_post():
    user_data = request.form.to_dict()
    errors = validate_user(user_data)
    if errors:
        return render_template('users/new.html', user=user_data, errors=errors)
    get_repo().save(user_data)
    flash("Пользователь создан", "success")
    return redirect(url_for("users.get_users"), 302)

@users_bp.route('<int:id>/edit')
def users_edit(id):
    content = get_repo().find(id)
    errors = {}
    return render_template('users/edit.html', user=content, errors=errors)

@users_bp.route('/<int:id>/patch', methods=['POST'])
def users_patch(id):
    user_data = request.form.to_dict()
    user_data['id'] = id
    errors = validate_user(user_data)
    if errors:
        return render_template('users/edit.html', user=user_data, errors=errors)
    get_repo().save(user_data)
    flash("Пользователь отредактирован", "success")
    return redirect(url_for('users.get_users'), 302)

@users_bp.route('/<int:id>/delete', methods=['POST'])
def users_delete(id):
    get_repo().delete(id)
    flash("Пользователь удален", "success")
    return redirect(url_for('users.get_users'), 302)

@users_bp.errorhandler(404)
def not_found(error):
    return "Oops!", 404
