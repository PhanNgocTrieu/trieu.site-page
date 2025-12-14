from flask import render_template
from flask_login import login_required, current_user
from app.blueprints.user import bp

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('user/dashboard.html', title='Dashboard')

@bp.route('/profile')
@login_required
def profile():
    return render_template('user/profile.html', title='Profile', user=current_user)
