from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, Length

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(min=1, max=140)])
    content = TextAreaField('Content', validators=[DataRequired()])
    summary = TextAreaField('Summary', validators=[Length(max=300)])
    cover_image = FileField('Cover Image', validators=[FileAllowed(['jpg', 'png', 'jpeg', 'webp'])])
    submit = SubmitField('Submit')
