from flask import Blueprint

bp = Blueprint('docs', __name__)

from app.blueprints.docs import routes
