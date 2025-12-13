# Kế hoạch Chi tiết Giai đoạn 2: User Identity (Xác thực & Định danh)

Giai đoạn này tập trung xây dựng hệ thống quản lý người dùng, bao gồm: Đăng ký, Đăng nhập, Đăng xuất và Quản lý phiên làm việc (Session).

## 1. Cơ sở dữ liệu (User Model)

### Checklists
- [ ] Tạo model `User` trong `app/models/user.py`.
- [ ] Định nghĩa các trường: `id`, `username`, `email` (index, unique), `password_hash`, `role`, `is_active`, `created_at`.
- [ ] Implement phương thức `set_password` và `check_password` (dùng `werkzeug.security`).
- [ ] Chạy migration để tạo bảng `users`.

### 🛡️ Best Practices
*   **Password Storage**: Tuyệt đối KHÔNG lưu password dạng plain text. Bắt buộc dùng `generate_password_hash`.
*   **User Mixin**: Kế thừa `flask_login.UserMixin` để có sẵn các thuộc tính `is_authenticated`, `is_active`, v.v.
*   **Indexing**: Đánh index cho trường `email` và `username` để query nhanh hơn khi login.

## 2. Hệ thống Xác thực (Authentication System)

### Checklists
- [ ] Cài đặt `Flask-Login` và `Flask-WTF` (đã có trong requirements hoặc cần add thêm).
- [ ] Khởi tạo `LoginManager` trong `app/extensions.py`.
- [ ] Cấu hình `user_loader` callback.
- [ ] Tạo `auth` Blueprint trong `app/blueprints/auth/`.

### 🛡️ Best Practices
*   **Blueprint Structure**: Gom toàn bộ logic auth vào thư mục riêng:
    ```
    app/blueprints/auth/
    ├── __init__.py      # Blueprint definition
    ├── routes.py        # Controller logic
    ├── forms.py         # Login/Register WTForms
    └── email.py         # Password reset logic (Future)
    ```
*   **Login View**: Cấu hình `login_manager.login_view = 'auth.login'` để Flask tự redirect khi user chưa đăng nhập truy cập trang kín.

## 3. Forms & Validation (Flask-WTF)

### Checklists
- [ ] Tạo `LoginForm`: email, password, remember_me (boolean).
- [ ] Tạo `RegisterForm`: username, email, password, confirm_password (validator: EqualTo).
- [ ] Custom validation: Check email đã tồn tại chưa ngay trong form validate.

### 🛡️ Best Practices
*   **CSRF Protection**: Luôn hiển thị `{{ form.hidden_tag() }}` hoặc cấu hình `CSRFProtect` global.
*   **Strong Passwords**: Thêm validator yêu cầu độ dài tối thiểu (vd: Length(min=8)).

## 4. Giao diện (Templates & UI)

### Checklists
- [ ] Thiết lập base template (`base.html`) với Flash Messages block.
- [ ] Tạo trang `login.html` và `register.html`.
- [ ] Sử dụng TailwindCSS qua CDN (cho dev nhanh) hoặc cài đặt PostCSS (nếu production cần tối ưu).

### 🛡️ Best Practices
*   **Feedback Loop**: Sử dụng Flask `flash()` message để báo lỗi nhập liệu hoặc thông báo đăng nhập thành công.
*   **Aesthetics**: Thiết kế form đăng nhập hiện đại, căn giữa màn hình, có shadow và border radius mềm mại (Glassmorphism nếu muốn ấn tượng).

---
**Kết quả đầu ra dự kiến của Giai đoạn 2**:
User có thể đăng ký tài khoản, đăng nhập (session được lưu), và đăng xuất. Database có bảng `users` với mật khẩu đã mã hóa.
