from app import create_app
from app.extensions import db
from app.models.bible import BibleBook, BibleChapter, BibleVerse

app = create_app()

def seed_bible():
    with app.app_context():
        print("Seeding Bible data...")
        
        # Check if already exists
        if BibleBook.query.filter_by(name='Sáng Thế Ký').first():
            print("Already seeded.")
            return

        # 1. Create Book
        genesis = BibleBook(name='Sáng Thế Ký', abbreviation='Gen', testament='OT')
        db.session.add(genesis)
        db.session.commit() # Commit to get ID
        
        # 2. Create Chapter 1
        chap1 = BibleChapter(book_id=genesis.id, number=1)
        db.session.add(chap1)
        db.session.commit()

        # 3. Create Verses (Sample Genesis 1:1-5, Vietnamese)
        verses_data = [
            "Ban đầu Đức Chúa Trời dựng nên trời đất.",
            "Vả, đất là vô hình và trống không, sự mờ tối ở trên mặt vực; Thần Đức Chúa Trời vận hành trên mặt nước.",
            "Đức Chúa Trời phán rằng: Hãy có sự sáng; thì có sự sáng.",
            "Đức Chúa Trời thấy sự sáng là tốt lành, bèn phân sáng ra cùng tối.",
            "Đức Chúa Trời đặt tên sự sáng là ngày, sự tối là đêm. Vậy, có buổi chiều và buổi mai; ấy là ngày thứ nhất."
        ]
        
        for i, text in enumerate(verses_data, 1):
            verse = BibleVerse(chapter_id=chap1.id, number=i, content=text)
            db.session.add(verse)
            
        db.session.commit()
        print("Seeded Genesis 1:1-5 successfully.")

if __name__ == "__main__":
    seed_bible()
