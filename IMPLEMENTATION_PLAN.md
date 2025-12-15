# Kế Hoạch Triển Khai Nâng Cấp Hệ Thống Website (Implementation Plan)

tài liệu này chi tiết hóa kế hoạch nâng cấp website `trieu.site-page` theo các mục tiêu: News Feed, Kinh Thánh App, Docs Management và tích hợp AI.

---

## 1. Tổng quan & Mục tiêu

*   **Mục tiêu cốt lõi**: Xây dựng Nền tảng Chia sẻ Thông tin & Tôn giáo hiện đại (Spiritual Feed).
*   **Điểm nhấn mới**:
    *   **AI-Powered Content**: Sử dụng OpenAI để tự động format bài viết, tạo bố cục đẹp mắt thay vì văn bản thô sơ.
    *   **Docs Repository**: Kho tệp tin/tài liệu cho cộng đồng.
    *   **Bible App**: Đọc và tra cứu Kinh Thánh.

---

## 2. Kế hoạch Chi tiết từng Giai đoạn (Phases)

### Giai đoạn 1: News Feed & UI Foundation (Giao diện & Tin tức)
**Mục tiêu**: Biến trang chủ thành News Feed sống động.

*   **1.1. Homepage News Feed**
    *   Hiển thị danh sách bài viết dạng **Masonry Grid** hoặc **Magazine Layout** (Tạp chí) thay vì list đơn điệu.
    *   Phân loại: Tin nổi bật (Featured), Tin mới nhất, Theo chủ đề.
    *   Sidebar: Trending posts, Câu gốc mỗi ngày.

*   **1.2. Responsive Navigation**
    *   Hamburger Menu cho Mobile.
    *   Mega Menu cho Desktop (nếu nhiều mục).

*   **1.3. Docs/Resource Library (Quản lý Tài liệu)**
    *   **Mô tả**: Khu vực riêng để upload và chia sẻ tài liệu (PDF, PPT, Docx).
    *   **Tính năng**:
        *   Admin/User upload tài liệu.
        *   Phân loại tài liệu (Học tập, Bài giảng, Nhạc thánh).
        *   Preview tài liệu trực tiếp trên web (nếu hỗ trợ).
    *   **Tech**: Model `Document`, tích hợp thư viện xem PDF.

**Status**: [x] Completed
- Homepage chuyển đổi thành News Feed (Grid Layout).
- Rebranding thành công ("Spiritual Feed").
- Docs Library đã hoạt động (Upload/Download).

---

### Giai đoạn 2: User Experience & Authentication
**Mục tiêu**: Tăng trải nghiệm cá nhân hóa.

*   **2.1. Login by Email**: Chuyển đổi sang đăng nhập bằng Email/Username.
*   **2.2. User Profile**: Avatar upload, Bio, Danh sách bài đã đăng, Tài liệu đã đóng góp.
*   **2.3. Rich Text Editor**:
    *   (Đã tích hợp trong Phase 3 cùng AI).

**Status**: [x] Completed
- Login linh hoạt (Email/Username).
- Profile Page đã hỗ trợ Upload Avatar và Update thông tin.

---

### Giai đoạn 3: AI Integration & Content Enhancement (Tích hợp AI)
**Mục tiêu**: Tự động hóa việc trình bày nội dung bài viết.

*   **3.1. AI Layout Generator (OpenAI Integration)**
    *   **Vấn đề**: User thường viết bài không đẹp (ít xuống dòng, thiếu ảnh minh họa, heading lộn xộn).
    *   **Giải pháp**: Tích hợp OpenAI API.
    *   **Luồng hoạt động**:
        1. User viết nội dung thô (text, ý tưởng).
        2. Bấm nút "✨ AI Magic Format".
        3. App gửi nội dung sang OpenAI kèm prompt về thiết kế.
        4. AI trả về bài viết đã được trình bày lại (HTML).

*   **3.2. Auto-Tagging & Summary**: (Optional) AI tự động tạo Tóm tắt và gắn Tag cho bài viết.

**Status**: [x] Completed (Core Integration)
- Đã xây dựng `AIService` và API Endpoint `/api/ai/format-post`.
- Đã thêm nút "AI Magic Format" vào trang viết bài.
- Đang chạy chế độ **Mock Mode** (Giả lập) do chưa có API Key.
- Cần cấu hình `OPENAI_API_KEY` trong `.env` để chạy thật.

---

### Giai đoạn 4: Bible App Integration
**Mục tiêu**: Ứng dụng Kinh Thánh.

*   **4.1. Core Bible Data**: Import CSDL Kinh Thánh (Sách, Chương, Câu).
*   **4.2. Bible Reader UI**: Giao diện đọc tập trung, Dark/Light mode, Điều chỉnh cỡ chữ.
*   **4.3. Search & Highlight**: Tìm kiếm câu kinh thánh, tô màu câu gốc.

**Status**: [ ] Not Started

---

## 3. Công nghệ & Hạ tầng (Tech Stack Update)

*   **Backend**: Flask + SQLAlchemy.
*   **AI**: OpenAI API (Cần API Key).
*   **Frontend**: Tailwind CSS (Typography plugin), Alpine.js.

## 4. Lộ trình triển khai (Roadmap)
1.  **Phase 1**: News Feed Homepage + Docs Library (Đã xong).
2.  **Phase 2**: User Profile (Đã xong).
3.  **Phase 3**: Tích hợp OpenAI (Đã xong Core).
4.  **Phase 4**: Bible App.
