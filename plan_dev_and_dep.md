# Kế Hoạch Quản Lý Môi Trường Development & Deployment (Dev vs Dep Plan)

## 1. Hiện Trạng & Vấn Đề
*   **Vấn đề**: Khi khởi chạy container lần đầu (fresh start), code `create_app` cố gắng tạo Admin user TRƯỚC KHI migration kịp chạy xong, dẫn đến lỗi `UndefinedTable`.
*   **Nguyên nhân**: Race condition giữa Application Code (chạy ngay) và Migration Command (chạy async hoặc chậm hơn).

## 2. Giải Pháp: Tách Biệt Môi Trường

### 2.1. Sử dụng Entrypoint Script
Thay vì chạy trực tiếp `flask db upgrade && gunicorn` trong `docker-compose`, ta sẽ dùng một file script `entrypoint.sh` thông minh hơn.

**Logic của entrypoint.sh:**
1.  Chờ Database sẵn sàng (Wait for DB).
2.  Chạy Migration: `flask db upgrade`.
3.  *(Optional)* Chạy Seed Data (nếu là Dev hoặc lần đầu deploy): `python seed_data.py`.
4.  Khởi động App: `gunicorn ...`.

### 2.2. Phân Biệt Config (Environment Variables)
Sử dụng biến `FLASK_ENV` hoặc `APP_ENV` trong `.env`:

*   **Development (`APP_ENV=dev`)**:
    *   Bật Debug Mode.
    *   Auto-reload code.
    *   Tự động Seed dữ liệu mẫu (Fake posts, users).
*   **Production (`APP_ENV=prod`)**:
    *   Tắt Debug.
    *   Logging ra `stdout` (JSON format nếu cần).
    *   Không tự động tạo data rác, chỉ tạo Admin mặc định nếu chưa có.

## 3. Plan Implement (Cụ thể)

### Bước 1: Tạo file `entrypoint.sh`
```bash
#!/bin/bash
# Chờ DB port mở
# Chạy migration
echo "Running Migrations..."
flask db upgrade

# Nếu ENV=dev, check và seed data
if [ "$APP_ENV" = "dev" ]; then
    echo "Seeding Development Data..."
    python seed_data_dev.py
fi

# Tạo Admin mặc định (Production safe)
echo "Ensuring Default Admin..."
python -c "from app import create_app; from app.blueprints.admin_utils import create_default_admin; create_default_admin()"

# Start Server
exec gunicorn -w 4 -b 0.0.0.0:5000 wsgi:app
```

### Bước 2: Tách logic tạo Admin
Chuyển logic `create_default_admin` ra khỏi `__init__.py` (vì nó chạy mỗi khi import app) sang một script riêng hoặc command `flask init-db`.
-> **Khuyến nghị**: Dùng Custom Flask Command `flask init-db`.

## 4. Kết luận
Việc tách script khởi tạo giúp pipeline ổn định, tránh lỗi race condition và đảm bảo môi trường Prod sạch sẽ.
