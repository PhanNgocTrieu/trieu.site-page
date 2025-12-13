# Kế hoạch Chi tiết Giai đoạn 1: Foundation (Nền tảng)

Tài liệu này quy định các bước thực hiện và tiêu chuẩn (Best Practices) để xây dựng lớp nền tảng cho dự án Flask SaaS. Mục tiêu là sự **ổn định**, **dễ mở rộng** và **an toàn** ngay từ dòng code đầu tiên.

## 1. Thiết lập Môi trường & Quản lý Dependencies

### Checklists
- [ ] Khởi tạo Git repository và file `.gitignore` tiêu chuẩn cho Python.
- [ ] Thiết lập môi trường ảo (`venv`).
- [ ] Cài đặt gói thư viện cốt lõi: `Flask`, `python-dotenv`.

### 🛡️ Best Practices
*   **Virtual Environment**: Bắt buộc sử dụng `venv` nằm trong thư mục `.venv` tại root dự án để cô lập gói thư viện.
*   **Dependencies**: Không dùng `pip freeze > requirements.txt` một cách bừa bãi.
    *   Hãy tạo file `requirements.in` (nếu dùng `pip-tools`) để liệt kê các thư viện chính (ví dụ: `Flask`, `SQLAlchemy`).
    *   Hoặc quản lý thủ công `requirements.txt` nhưng chia rõ các section `# Core`, `# Database`, `# Dev Tools`.
    *   **Strict Versioning**: Nên ghim version cụ thể (vd: `Flask==3.0.0`) để tránh lỗi khi deploy production khác version với dev.

## 2. Cấu trúc Dự án (Application Factory Pattern)

### Checklists
- [ ] Tạo cấu trúc thư mục phân tầng (`app/`, `tests/`, `migrations/`).
- [ ] Implement hàm `create_app()` trong `app/__init__.py`.
- [ ] Tạo file `extensions.py` để khởi tạo các plugin (SQLAlchemy, LoginManager...).
- [ ] Tạo `wsgi.py` (hoặc `run.py`) làm entry point.

### 🛡️ Best Practices
*   **Circular Imports**: Đây là lỗi kinh điển của Flask.
    *   **Giải pháp**: Dùng module `extensions.py`. Khởi tạo extension ở đó (vd: `db = SQLAlchemy()`). Sau đó trong `create_app`, mới gọi `db.init_app(app)`.
    *   Tuyệt đối không import `app` instance trực tiếp vào models hay views.
*   **Blueprints**: Đăng ký Blueprint ngay trong `create_app`. Gom nhóm logic theo chức năng (`auth`, `blog`) chứ không gom theo kỹ thuật (`views`, `models`).

## 3. Quản lý Cấu hình (Configuration)

### Checklists
- [ ] Tạo file `.env` (và `.env.example`) để chứa bí mật.
- [ ] Tạo class `Config`, `DevelopmentConfig`, `ProductionConfig`.
- [ ] Load config tự động dựa trên biến môi trường `FLASK_ENV` hoặc `FLASK_CONFIG`.

### 🛡️ Best Practices
*   **12-Factor App**: Config phải tách biệt khỏi Code.
*   **Environment Variables**: KHÔNG BAO GIỜ hardcode password DB hay Secret Key trong file `.py`.
*   **Config Class**: Dùng Class inheritance để kế thừa cấu hình chung.
    ```python
    class Config:
        SECRET_KEY = os.environ.get('SECRET_KEY')
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    class ProductionConfig(Config):
        DEBUG = False
        # Cấu hình SSL, Cookie Secure...
    ```
*   **.gitignore**: Đảm bảo file `.env` được ignore tuyệt đối.

## 4. Hệ thống Logging & Monitoring cơ bản

### Checklists
- [ ] Cấu hình Logging sử dụng thư viện chuẩn `logging` của Python.
- [ ] Thiết lập `RotatingFileHandler` để ghi log ra file (tránh file log phình to vô hạn).
- [ ] Format log đầy đủ: `[Time] [Level] [Module]: Message`.

### 🛡️ Best Practices
*   **No Print Statements**: Tuyệt đối không dùng `print()` để debug trong code production. Luôn dùng `current_app.logger.info()` hoặc `logging.warning()`.
*   **Log Levels**: Phân biệt rõ `DEBUG` (cho dev), `INFO` (hoạt động bình thường), `WARNING` (có gì đó lạ nhưng chưa lỗi), `ERROR` (lỗi chức năng), `CRITICAL` (sập hệ thống).
*   **Structured Logging** (Optional): Nếu dự định dùng hệ thống gom log (ELK stack), nên log dạng JSON. Với giai đoạn 1, text format là đủ.

## 5. Cơ sở dữ liệu (Neon PostgreSQL + SQLAlchemy)

### Checklists
- [ ] Cài đặt `flask-sqlalchemy`, `flask-migrate`, `psycopg2-binary`.
- [ ] Tạo kết nối tới Neon PostgreSQL qua `SQLALCHEMY_DATABASE_URI`.
- [ ] Thiết lập `Alembic` để quản lý version DB (`flask db init`).

### 🛡️ Best Practices
*   **Connection Pooling**: PostgreSQL tốn tài nguyên cho mỗi connection. SQLAlchemy có sẵn pool, nhưng cần cấu hình `SQLALCHEMY_ENGINE_OPTIONS` hợp lý (vd: `pool_size=10`, `max_overflow=20`) để không làm sập DB server.
*   **Naming Convention**: Alembic cần nhất quán. Nên cấu hình `MetaData` của SQLAlchemy để tự động đặt tên cho Index và Foreign Key (tránh lỗi khi migrate).
    ```python
    convention = {
        "ix": 'ix_%(column_0_label)s',
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "ck": "ck_%(table_name)s_%(constraint_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s"
    }
    metadata = MetaData(naming_convention=convention)
    ```
*   **SSL Mode**: Khi kết nối cloud DB như Neon, bắt buộc tham số `?sslmode=require` trong Connection String.

---
**Kết quả đầu ra dự kiến của Giai đoạn 1**: Một source code khung có thể chạy lệnh `flask run`, kết nối thành công tới DB Neon, và ghi log ra file khi có request. Chưa có giao diện người dùng, nhưng "bộ khung xương" đã vững chắc.
