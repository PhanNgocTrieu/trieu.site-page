# Kế Hoạch Giai Đoạn 5: UI/UX Polish & Feature Enhancements

Giai đoạn này tập trung vào việc giải quyết các phản hồi của người dùng về giao diện và trải nghiệm viết bài, cũng như thêm chế độ Dark Mode.

---

## 1. Mục Tiêu

1.  **Cải thiện giao diện bài viết (Blog UI)**: Làm cho trang đọc bài viết đẹp hơn, dễ đọc hơn (Typography, Spacing).
2.  **Chức năng Sửa bài (Edit Post)**: Cho phép tác giả cập nhật nội dung bài viết.
3.  **Rich Text Editor**: Tích hợp trình soạn thảo văn bản (WYSIWYG) để người dùng không phải nhìn thấy HTML tags thô, và AI có thể trả về HTML mà editor hiển thị được.
4.  **Dark Mode**: Chế độ giao diện tối.

---

## 2. Giải Pháp Chi Tiết

### 2.1. Rich Text Editor (Fix vấn đề HTML Tags)
*   **Vấn đề**: Hiện tại `content` là một `TextAreaField` đơn giản. Khi AI trả về HTML (<code>&lt;h2&gt;...&lt;/h2&gt;</code>), người dùng nhìn thấy code thay vì văn bản định dạng.
*   **Giải pháp**: Tích hợp **Quill.js** hoặc **EasyMDE**. Ưu tiên **Quill.js** vì nó nhẹ và hỗ trợ HTML tốt.
*   **Thay đổi**:
    *   `forms.py`: Giữ nguyên `TextAreaField` nhưng ẩn đi.
    *   `create_post.html` & `edit_post.html`: Thêm Quill container và JS để sync nội dung giữa Quill và hidden textarea.

### 2.2. Chức năng Sửa Bài (Edit Post)
*   **Route**: `/blog/<id>/update`.
*   **Permission**: Chỉ `author` hoặc `admin` mới được sửa.
*   **UI**: Nút "Edit" trên trang chi tiết bài viết (nếu có quyền).

### 2.3. Cải thiện Blog Detail UI
*   **Typography**: Sử dụng class `prose prose-lg prose-indigo` của Tailwind Typography plugin để tự động format headings, paragraphs, lists, images đẹp mắt.
*   **Layout**:
    *   Cover Image rộng (Full width hoặc Container width).
    *   Author info & Date rõ ràng hơn.

### 2.4. Dark Mode
*   **Tailwind Config**: Bật `darkMode: 'class'`.
*   **Toggle Button**: Thêm nút Mặt trăng/Mặt trời trên Navbar.
*   **Logic**: Sử dụng Alpine.js để lưu preference vào `localStorage` và toggle class `dark` trên thẻ `<html>`.
*   **Styling**: Thêm các class `dark:bg-gray-900 dark:text-gray-100` vào `base.html` và các component chính.

---

## 3. Lộ Trình Thực Hiện

1.  **Bước 1: Edit Functionality** (Backend logic trước).
2.  **Bước 2: Rich Text Editor + Blog UI** (Frontend polish).
3.  **Bước 3: Dark Mode** (Global style change).
