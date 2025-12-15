# Kế Hoạch Footer (Chân Trang)

## 1. Cấu Trúc Footer
Sử dụng Layout 3 hoặc 4 cột để hiển thị thông tin đầy đủ và chuyên nghiệp.

### Cột 1: Thông Tin Chung (Identity)
*   **Logo/Brand Name**: Spiritual Feed.
*   **Slogan**: Nơi chia sẻ đức tin và tri thức.
*   **Copyright**: © 2025 Spiritual Feed. All rights reserved.

### Cột 2: Quick Links (Liên Kết Nhanh)
*   Trang Chủ (Home).
*   Bài Viết (Blog/News).
*   Tài Liệu (Docs Library).
*   Về Chúng Tôi (About Us - *Future*).

### Cột 3: Liên Hệ (Contact Us)
*   **Email**: contact@spiritualfeed.com (Placeholder).
*   **Phone**: +84 90 123 4567.
*   **Address**: Ho Chi Minh City, Vietnam.

### Cột 4: Social Media (Mạng Xã Hội)
*   Facebook (Icon).
*   Youtube (Icon).
*   Zalo (Icon).

## 2. Implementation Steps
1.  **Sửa file**: `app/templates/base.html`.
2.  **CSS**: Sử dụng Tailwind Grid (`grid-cols-1 md:grid-cols-4 gap-8`).
3.  **Icons**: Sử dụng SVG inline hoặc FontAwesome (nếu có, hiện tại ưu tiên SVG để nhẹ).

## 3. Nội Dung Mẫu (HTML Snippet)
```html
<footer class="bg-gray-800 text-white mt-12">
    <div class="max-w-7xl mx-auto py-12 px-4 sm:px-6 lg:px-8 grid grid-cols-1 md:grid-cols-4 gap-8">
        <!-- Col 1 -->
        <div>
            <h3 class="text-lg font-bold">Spiritual Feed</h3>
            <p class="mt-4 text-gray-300 text-sm">Kết nối cộng đồng, chia sẻ niềm tin.</p>
        </div>
        <!-- Col 2 -->
        <div>
            <h3 class="text-sm font-semibold tracking-wider uppercase text-gray-400">Khám Phá</h3>
            <ul class="mt-4 space-y-4">
                <li><a href="{{ url_for('main.index') }}" class="text-base text-gray-300 hover:text-white">Trang Chủ</a></li>
                <li><a href="{{ url_for('docs.index') }}" class="text-base text-gray-300 hover:text-white">Tài Liệu</a></li>
            </ul>
        </div>
        <!-- Col 3 -->
        <div>
             <h3 class="text-sm font-semibold tracking-wider uppercase text-gray-400">Liên Hệ</h3>
             <ul class="mt-4 space-y-4 text-gray-300 text-sm">
                <li>Email: contact@example.com</li>
                <li>SĐT: 0123 456 789</li>
             </ul>
        </div>
    </div>
</footer>
```
