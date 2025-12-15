import os
import secrets
from flask import render_template, current_app, flash, redirect, url_for, request
from flask_login import login_required, current_user
from app.extensions import db
from app.blueprints.user import bp
from app.blueprints.user.forms import UpdateProfileForm

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.root_path, 'static/uploads/avatars', picture_fn)
    
    # Create avatar folder if not exists
    os.makedirs(os.path.dirname(picture_path), exist_ok=True)
    
    form_picture.save(picture_path)
    return picture_fn

@bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('user/dashboard.html', title='Dashboard')

@bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    form = UpdateProfileForm()
    if form.validate_on_submit():
        if form.avatar.data:
            picture_file = save_picture(form.avatar.data)
            current_user.avatar = picture_file
        current_user.username = form.username.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('user.profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        
    image_file = url_for('static', filename='uploads/avatars/' + current_user.avatar) if current_user.avatar else url_for('static', filename='img/default.jpg') # Assuming default.jpg exists or handled
    return render_template('user/profile.html', title='Profile', image_file=image_file, form=form)
