from flask import Blueprint

bp = Blueprint('bible', __name__, url_prefix='/bible')

from app.blueprints.bible import routes
