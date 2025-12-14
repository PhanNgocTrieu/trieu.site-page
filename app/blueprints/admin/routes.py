from flask import render_template
from flask_login import login_required
from app.blueprints.admin import bp
from app.decorators import admin_required
from app.models.user import User
from app.models.content import Post

@bp.route('/')
@login_required
@admin_required
def index():
    user_count = User.query.count()
    post_count = Post.query.count()
    return render_template('admin/index.html', title='Admin Dashboard', 
                           user_count=user_count, post_count=post_count)

@bp.route('/users')
@login_required
@admin_required
def users():
    users = User.query.all()
    return render_template('admin/users.html', title='User Management', users=users)
