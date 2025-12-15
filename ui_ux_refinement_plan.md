# Kế Hoạch Cải Thiện UI/UX (UI/UX Refinement Plan)

Tài liệu này đề xuất các cải tiến về giao diện và trải nghiệm người dùng để hệ thống hoàn thiện hơn, giải quyết vấn đề trạng thái không đồng bộ và nâng cao tính chuyên nghiệp.

---

## 1. Vấn đề Hiện Tại (Current Issues)

### 1.1. Navigation Active State
*   **Mô tả**: Khi người dùng click vào "Blog", trang chuyển hướng nhưng thanh menu vẫn highlight "Home".
*   **Nguyên nhân**: Code `base.html` đang set cứng class `border-indigo-500` (active) cho Home và `border-transparent` cho các link khác mà không kiểm tra URL hiện tại.
*   **Giải pháp**: Sử dụng Jinja2 logic để kiểm tra `request.endpoint` và apply class active động.

### 1.2. Responsive Navigation (Mobile)
*   **Mô tả**: Chưa có logic JS để toggle menu trên mobile (Hamburger button hiện tại có thể chưa hoạt động hoặc chưa tối ưu).
*   **Giải pháp**: Thêm Alpine.js hoặc Vanilla JS để toggle class `hidden` cho mobile menu block.

### 1.3. User Experience (Flash & Empty States)
*   **Flash Messages**: Thông báo (Login success, Error) hiện tại chỉ là text box xanh/đỏ, không tự tắt sau vài giây, làm rối giao diện.
*   **Empty States**: Trang Bible Search hoặc Blog nếu không có dữ liệu chỉ hiện text đơn điệu. Cần minh họa đẹp hơn.

---

## 2. Các Thay Đổi Cụ Thể (Proposed Changes)

### 2.1. Cập Nhật Navbar (Gấp)
Logic mới cho từng link trong `base.html`:
```html
<!-- Logic kiểm tra Active -->
{% set active_class = "border-indigo-500 text-gray-900" %}
{% set inactive_class = "border-transparent text-gray-500 hover:border-gray-300 hover:text-gray-700" %}

<a href="{{ url_for('main.index') }}" 
   class="{{ active_class if request.endpoint == 'main.index' else inactive_class }} inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
   Home
</a>
<a href="{{ url_for('blog.index') }}" 
   class="{{ active_class if 'blog.' in request.endpoint else inactive_class }} inline-flex items-center px-1 pt-1 border-b-2 text-sm font-medium">
   Blog
</a>
<!-- Tương tự cho Docs và Bible -->
```

### 2.2. Loading States
*   Thêm Global Loader (NProgress) hoặc Spinner khi chuyển trang để user biết hệ thống đang xử lý.
*   Thêm Spinner cho nút "AI Magic Format" khi đang chờ API context.

### 2.3. Trang Lỗi (Error Pages)
*   Custom 404 (Not Found) và 500 (Server Error) với hình ảnh thân thiện thay vì text mặc định của trình duyệt/Flask.

### 2.4. Refactor Bible Reader
*   Thêm Dropdown chọn Sách/Chương nhanh (Jump to) thay vì phải quay lại trang chủ Bible.

---

## 3. Lộ Trình Thực Hiện (Roadmap)

1.  **Bước 1: Fix Navigation State** (Ưu tiên cao nhất - theo yêu cầu user).
2.  **Bước 2: Flash Message Auto-dismiss** (Tăng trải nghiệm ngay lập tức).
3.  **Bước 3: Error Pages Design**.
4.  **Bước 4: Mobile Menu Logic**.
