# Kế hoạch Chi tiết Giai đoạn 3: Core Features (Tính năng chính)

Giai đoạn này tập trung vào nội dung và tiện ích cho người dùng: Dashboard cá nhân, Hệ thống Blog và Quản lý File Upload.

## 1. Dashboard & User Profile

### Checklists
- [ ] Tạo blueprint `user` (hoặc `main` nếu muốn đơn giản).
- [ ] Route `/dashboard` (yêu cầu login).
- [ ] Trang Profile: Upload Avatar, Đổi mật khẩu, Cập nhật thông tin cá nhân.

### 🛡️ Best Practices
- **Role Based Access**: Dashboard của Admin sẽ khác User thường (sẽ xử lý kỹ hơn ở Giai đoạn phân quyền).
- **Security**: Endpoint đổi mật khẩu phải bắt buộc xác nhận mật khẩu cũ (Old Password Validation).

## 2. Hệ thống Blog (Content Management)

### Checklists
- [ ] Tạo Model `Post`: `title`, `slug`, `content` (Markdown/HTML), `author_id`, `created_at`, `status` (draft/published).
- [ ] Tạo Model `Tag` hoặc `Category` (Many-to-Many với Post).
- [ ] Blueprint `blog`:
    - `GET /blog`: Danh sách bài viết (Pagination).
    - `GET /blog/<slug>`: Chi tiết bài viết.
    - `GET /blog/create`, `POST /blog/create`: Tạo bài viết mới (chỉ Admin/Author).
- [ ] Tích hợp trình soạn thảo (Markdown Editor hoặc SimpleMDE/EasyMDE).

### 🛡️ Best Practices
- **SEO Friendly URLs**: Sử dụng `slug` (ví dụ: `bai-viet-so-1`) thay vì ID trên URL. Dùng thư viện `python-slugify` để tự tạo slug từ title.
- **Pagination**: Luôn phân trang cho danh sách bài viết để tối ưu hiệu năng DB.
- **Sanitization**: Nếu cho phép nhập HTML, bắt buộc dùng `bleach` để lọc thẻ script độc hại (XSS).

## 3. Xử lý File Upload (Avatar & Post Images)

### Checklists
- [ ] Cấu hình `MAX_CONTENT_LENGTH` để giới hạn dung lượng file (vd: 16MB).
- [ ] Tạo helper function `save_file(file, folder)`:
    - Đổi tên file an toàn (secure_filename + UUID).
    - Lưu file vào thư mục `app/static/uploads` (cho Dev).
    - (Future) Chuẩn bị interface để switch sang S3 dễ dàng.
- [ ] Validate file extensions (chỉ cho phép `.jpg`, `.png`, `.webp`).

### 🛡️ Best Practices
- **Serve Static Files**: Trong môi trường Docker/Prod, Flask không nên serve static files trực tiếp. Cấu hình Nginx hoặc WhiteNoise (tuy nhiên với mô hình hiện tại Gunicorn, ta có thể dùng `Shared Volume` và Nginx container ở Giai đoạn Deployment sau).
- **Optimization**: Resize ảnh lớn trước khi lưu (dùng thư viện `Pillow`) để tiết kiệm dung lượng.

---
**Kết quả đầu ra dự kiến của Giai đoạn 3**:
- Người dùng có trang Dashboard riêng.
- Admin có thể viết blog, upload ảnh, và công khai bài viết ra trang chủ.
