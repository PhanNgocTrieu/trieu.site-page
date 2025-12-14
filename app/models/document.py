from datetime import datetime
from app.extensions import db

class Document(db.Model):
    __tablename__ = 'documents'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_type = db.Column(db.String(50)) # pdf, docx, pptx
    file_size = db.Column(db.Integer) # in bytes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # User relationship
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    uploader = db.relationship('User', backref='documents')

    def __repr__(self):
        return f'<Document {self.title}>'
