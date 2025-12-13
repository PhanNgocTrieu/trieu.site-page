# Kế hoạch Xây dựng Flask SaaS Boilerplate (Production-Ready)

## Mục tiêu
Xây dựng một khung dự án (boilerplate) Flask chuẩn mực, sẵn sàng cho môi trường production, phục vụ các nhu cầu: Website cá nhân/tổ chức, Blog, và Hệ thống E-learning (LMS).

## 1. Kiến trúc & Công nghệ (Architecture & Tech Stack)

### Core Framework
*   **Web Framework**: Flask (Python) - Theo yêu cầu.
*   **Application Structure**: **Application Factory Pattern** kết hợp với **Blueprints** để chia nhỏ module (Auth, Blog, Courses, API, User).
*   **Configuration**: Quản lý config qua biến môi trường (`python-dotenv`), chia tách `DevelopmentConfig`, `ProductionConfig`, `TestingConfig`.

### Database & Storage
*   **Database**: PostgreSQL (kết nối Neon Tech).
*   **ORM**: SQLAlchemy (dùng `Flask-SQLAlchemy`).
*   **Migrations**: Alembic (dùng `Flask-Migrate`).
*   **File Storage**: AWS S3 hoặc MinIO (dùng `boto3`). Interface trừu tượng để dễ dàng thay đổi provider.
*   **Redis**: Dùng làm Message Broker cho Celery và Caching.

### Authentication & Authorization
*   **Auth**: `Flask-Login` (Session based) cho Web UI, `Flask-JWT-Extended` cho API (nếu cần tách biệt Mobile App sau này).
*   **Permissions**: Custom Decorators hoặc `Flask-Principal` để quản lý Role (Admin, Instructor, Student).
*   **Security form**: `Flask-WTF` (CSRF protection).

### Background Jobs
*   **Task Queue**: Celery.
*   **Broker**: Redis.
*   **Use Cases**: Gửi email (Welcome, Reset password), Xử lý video upload, Tạo report.

### Logging & Monitoring
*   **Logging**: Python `logging` module, xoay vòng log file (`RotatingFileHandler`), tích hợp gửi lỗi quan trọng qua Email/Slack.
*   **Monitoring**: Prometheus metrics (dùng `prometheus-flask-exporter`) hoặc Sentry để tracking errors.

### Frontend (User Interface)
*   **Templating**: Jinja2.
*   **CSS Framework**: TailwindCSS (Khuyên dùng để đạt "Rich Aesthetics" và hiện đại) hoặc Bootstrap 5.
*   **JS**: Vanilla JS hoặc Alpine.js cho các tương tác nhẹ (tránh phức tạp hóa với React/Vue nếu không cần SPA hoàn toàn).

---

## 2. Cấu trúc Dự án Đề xuất
```text
flask_saas_boilerplate/
├── app/
│   ├── __init__.py          # Application Factory
│   ├── extensions.py        # Khởi tạo db, login_manager, migrate, celery
│   ├── models/              # Định nghĩa Database Models
│   │   ├── user.py
│   │   ├── content.py       # Blog, Pages
│   │   └── course.py        # LMS models
│   ├── blueprints/          # Các module chức năng
│   │   ├── auth/            # Login, Register, Reset Pass
│   │   ├── main/            # Homepage, Static pages
│   │   ├── blog/            # Blog listing, details
│   │   ├── courses/         # Course listing, learning view
│   │   ├── user/            # Profile, Settings
│   │   └── admin/           # Admin Dashboard
│   ├── templates/           # Jinja2 HTML files
│   ├── static/              # CSS, JS, Images
│   ├── services/            # Business Logic (Storage, Email)
│   └── tasks/               # Celery Tasks
├── tests/                   # Unit & Integration Tests
├── migrations/              # Database Migrations versions
├── .env.example             # Mẫu biến môi trường
├── config.py                # Class cấu hình
├── docker-compose.yml       # Dev environment (Redis, App, DB)
├── Dockerfile               # Production build
├── requirements.txt         # Dependencies
└── wsgi.py                  # Entry point
```

---

## 3. Thiết kế Database (Sơ bộ)

### Users & Auth
*   **User**: `id`, `email`, `password_hash`, `full_name`, `avatar_url`, `is_active`, `role` (enum: admin, user, instructor), `created_at`.
*   **Role/Permission**: Có thể đơn giản là cột `role` trong bảng User hoặc bảng riêng nếu phân quyền phức tạp.

### Content (Blog/Pages)
*   **Post**: `id`, `title`, `slug` (unique), `content` (Markdown/HTML), `author_id`, `status` (draft/published), `published_at`.
*   **Tag/Category**: Phân loại bài viết.

### LMS (Learning Management System)
*   **Course**: `id`, `title`, `description`, `price`, `instructor_id`, `thumbnail_url`.
*   **Module/Section**: Chương học.
*   **Lesson**: `id`, `module_id`, `title`, `video_type` (Youtube/Upload), `video_url`, `duration`, `content` (text document).
*   **Enrollment**: `user_id`, `course_id`, `enrolled_at`, `progress`.

---

## 4. Các bước xây dựng (Step-by-Step Plan)

### Giai đoạn 1: Foundation (Nền tảng)
1.  Thiết lập môi trường ảo (venv), cài đặt Flask.
2.  Cấu trúc thư mục theo App Factory pattern.
3.  Cấu hình `Config` class và biến môi trường.
4.  Thiết lập Logging cơ bản.
5.  Thiết lập Database (SQLAlchemy) và Migrations (Alembic). Kết nối thử với Neon PostgreSQL.

### Giai đoạn 2: User Identity (Định danh)
1.  Tạo Model `User`.
2.  Xây dựng trang Login, Register, Logout, Forgot Password.
3.  Tích hợp `Flask-Login` để quản lý session.
4.  Bảo vệ các route yêu cầu đăng nhập (`@login_required`).

### Giai đoạn 3: Core Features (Blog & Dashboard)
1.  Tạo Dashboard cơ bản cho User sau khi login.
2.  Xây dựng module Blog: CRUD bài viết (chỉ Admin/Editor).
3.  Hiển thị bài viết ra public view.
4.  Tích hợp File Upload (S3/Local) để upload ảnh bài viết/avatar.

### Giai đoạn 4: LMS Features (Khoá học)
1.  Xây dựng Model Course, Lesson.
2.  Giao diện tạo khoá học (cho Instructor/Admin).
3.  Giao diện học (Learning interface) cho học viên.
4.  Logic xử lý ghi danh (Enrollment).

### Giai đoạn 5: Advanced & Background Jobs
1.  Cài đặt Redis.
2.  Tích hợp Celery.
3.  Viết task gửi email welcome không đồng bộ (Async).
4.  (Tuỳ chọn) Task xử lý video sau khi upload (encode, generate thumbnail).

### Giai đoạn 6: Security & Deployment
1.  Review bảo mật: CSRF, XSS (autoescape của Jinja2 lo phần lớn), SQL Injection (ORM lo).
2.  Cấu hình HTTPS (SSL) và biến môi trường production.
3.  Viết `Dockerfile`.
4.  Cấu hình CI/CD (GitHub Actions) để chạy test và deploy tự động.

## Best Practices cần lưu ý
*   **12-Factor App**: Tuân thủ nguyên tắc 12-factor cho ứng dụng SaaS.
*   **Code Style**: Tuân thủ PEP8, dùng `black` và `flake8` để format code.
*   **Testing**: Viết unit test ngay từ đầu (`pytest`).
*   **Dependency Management**: Luôn "pin" version trong `requirements.txt` để tránh breaking changes.
*   **Error Handling**: Custom trang 404, 500 đẹp mắt và thân thiện.
