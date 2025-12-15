# Kế Hoạch Triển Khai Nâng Cấp Hệ Thống Website (Implementation Plan)

tài liệu này chi tiết hóa kế hoạch nâng cấp website `trieu.site-page` theo các mục tiêu: News Feed, Kinh Thánh App, Docs Management và tích hợp AI.

---

## 1. Tổng quan & Mục tiêu

*   **Mục tiêu cốt lõi**: Xây dựng Nền tảng Chia sẻ Thông tin & Tôn giáo hiện đại (Spiritual Feed).
*   **Điểm nhấn mới**:
    *   **AI-Powered Content**: Sử dụng OpenAI để tự động format bài viết.
    *   **Docs Repository**: Kho tệp tin/tài liệu cho cộng đồng.
    *   **Bible App**: Đọc và tra cứu Kinh Thánh.

---

## 2. Kế hoạch Chi tiết từng Giai đoạn (Phases)

### Giai đoạn 1: News Feed & UI Foundation
**Status**: [x] Completed
- Homepage News Feed (Grid Layout).
- Rebranding ("Spiritual Feed").
- Docs Library.

### Giai đoạn 2: User Experience & Authentication
**Status**: [x] Completed
- Login by Email/Username.
- User Profile Enhancement (Avatar Upload).

### Giai đoạn 3: AI Integration
**Status**: [x] Completed (Core Integration)
- `AIService` & API `/api/ai/format-post`.
- "AI Magic Format" button.
- OpenAI Integration (Mock mode verified).

### Giai đoạn 4: Bible App Integration
**Mục tiêu**: Ứng dụng Kinh Thánh.

*   **4.1. Core Bible Data**:
    *   Tạo Models (`BibleBook`, `BibleChapter`, `BibleVerse`).
    *   Script seed data (Demo Sáng Thế Ký đoạn 1).
*   **4.2. Bible Reader UI**:
    *   Giao diện Mục lục (Danh sách Sách Cựu Ước/Tân Ước).
    *   Giao diện Đọc (Chương/Câu), điều hướng Trước/Sau.
*   **4.3. Search**:
    *   Tính năng tìm kiếm câu Kinh Thánh.

**Status**: [x] Completed (Skeleton)
- Đã xây dựng hoàn chỉnh khung sườn và giao diện.
- Đã import dữ liệu mẫu (Sáng Thế Ký 1).
- Chức năng Tìm kiếm hoạt động tốt.
- *Lưu ý*: Cần import toàn bộ dữ liệu Kinh Thánh (JSON/SQL) để app hoàn chỉnh.

---

## 3. Công nghệ & Hạ tầng (Tech Stack Update)
*   **Backend**: Flask + SQLAlchemy.
*   **AI**: OpenAI API.
*   **Frontend**: Tailwind CSS.

## 4. Lộ trình triển khai (Roadmap)
1.  **Phase 1**: News Feed + Docs (Xong).
2.  **Phase 2**: User Profile (Xong).
3.  **Phase 3**: AI Integration (Xong).
4.  **Phase 4**: Bible App (Xong khung sườn).
