from app.extensions import db

class BibleBook(db.Model):
    __tablename__ = 'bible_books'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    abbreviation = db.Column(db.String(10))
    testament = db.Column(db.String(10)) # 'OT' or 'NT'
    chapters = db.relationship('BibleChapter', backref='book', lazy='dynamic')

    def __repr__(self):
        return f'<BibleBook {self.name}>'

class BibleChapter(db.Model):
    __tablename__ = 'bible_chapters'
    id = db.Column(db.Integer, primary_key=True)
    book_id = db.Column(db.Integer, db.ForeignKey('bible_books.id'), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    verses = db.relationship('BibleVerse', backref='chapter', lazy='dynamic')

    def __repr__(self):
        return f'<BibleChapter {self.book.name} {self.number}>'

class BibleVerse(db.Model):
    __tablename__ = 'bible_verses'
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey('bible_chapters.id'), nullable=False)
    number = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f'<BibleVerse {self.chapter.book.name} {self.chapter.number}:{self.number}>'
