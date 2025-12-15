from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Email

class UpdateProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    avatar = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'], 'Images only!')])
    submit = SubmitField('Update')
