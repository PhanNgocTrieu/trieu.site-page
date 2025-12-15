from flask import render_template, abort, request
from app.blueprints.bible import bp
from app.models.bible import BibleBook, BibleChapter, BibleVerse

@bp.route('/')
def index():
    books = BibleBook.query.all()
    # Group by Testament
    ot_books = [b for b in books if b.testament == 'OT']
    nt_books = [b for b in books if b.testament == 'NT']
    return render_template('bible/index.html', ot_books=ot_books, nt_books=nt_books)

@bp.route('/<int:book_id>/<int:chapter_num>')
def chapter(book_id, chapter_num):
    book = BibleBook.query.get_or_404(book_id)
    chapter = BibleChapter.query.filter_by(book_id=book.id, number=chapter_num).first_or_404()
    # Get prev/next links
    prev_chapter = BibleChapter.query.filter_by(book_id=book.id, number=chapter_num - 1).first()
    next_chapter = BibleChapter.query.filter_by(book_id=book.id, number=chapter_num + 1).first()
    
    return render_template('bible/chapter.html', book=book, chapter=chapter, 
                           prev_chapter=prev_chapter, next_chapter=next_chapter)

@bp.route('/search')
def search():
    query = request.args.get('q', '')
    results = []
    if query:
        # Simple case-insensitive search
        results = BibleVerse.query.filter(BibleVerse.content.ilike(f'%{query}%')).limit(50).all()
    
    return render_template('bible/search_results.html', query=query, results=results)
