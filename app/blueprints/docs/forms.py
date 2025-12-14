from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf.file import FileAllowed, FileRequired

class UploadDocumentForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    file = FileField('Document File', validators=[
        FileRequired(),
        FileAllowed(['pdf', 'doc', 'docx', 'ppt', 'pptx', 'xls', 'xlsx', 'txt'], 'Documents only!')
    ])
    submit = SubmitField('Upload')
