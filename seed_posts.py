from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.content import Post
from datetime import datetime, timedelta

app = create_app()

def seed_posts():
    with app.app_context():
        # Get admin user
        user = User.query.filter_by(username='admin').first()
        if not user:
            print("Admin user not found! Create admin first.")
            return

        print(f"Seeding posts for user: {user.username}...")
        
        # Sample data
        titles = [
            "Lời Chứng: Quyền Năng Của Sự Cầu Nguyện",
            "5 Điều Cần Làm Mỗi Sáng Để Có Ngày Phước Hạnh",
            "Giải Nghĩa Kinh Thánh: Thi Thiên 23",
            "Sức Mạnh Của Sự Tha Thứ Trong Gia Đình",
            "Làm Thế Nào Để Vượt Qua Sự Lo Lắng?",
            "Câu Chuyện Giáng Sinh: Ý Nghĩa Thật Sự",
            "Đức Tin Hành Động: Giúp Đỡ Người Nghèo",
            "Nhạc Thánh Ca: Những Bài Hát Bất Hủ",
            "Tĩnh Nguyện Hằng Ngày: Chúa Là Đấng Chăn Chiên",
            "Thông Báo: Chương Trình Thờ Phượng Chủ Nhật"
        ]
        
        for i, title in enumerate(titles):
            post = Post(
                title=title,
                slug=f"post-{i}-{datetime.now().timestamp()}",
                content=f"""
                <p>Đây là nội dung mẫu cho bài viết <strong>{title}</strong>.</p>
                <p>Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.</p>
                <blockquote>"Hãy hết lòng tin cậy Đức Giê-hô-va, chớ nương cậy nơi sự thông sáng của con." - Châm Ngôn 3:5</blockquote>
                <p>Cầu xin Chúa ban phước cho bạn!</p>
                """,
                summary=f"Tóm tắt ngắn gọn cho bài viết {title}. Đọc để tìm hiểu thêm về chủ đề này...",
                author=user,
                status='published',
                created_at=datetime.utcnow() - timedelta(days=i) # Backdate posts
            )
            db.session.add(post)
        
        db.session.commit()
        print("Done! 10 posts created.")

if __name__ == "__main__":
    seed_posts()
