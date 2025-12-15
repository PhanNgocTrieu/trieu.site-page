# 🚀 Hướng Dẫn Deploy Spiritual Feed lên Render.com

## Bước 1: Chuẩn bị tài khoản

1. Truy cập [render.com](https://render.com)
2. Đăng ký/Đăng nhập bằng GitHub account
3. Cho phép Render truy cập vào repository `trieu.site-page`

---

## Bước 2: Tạo Web Service

### 2.1. Tạo service mới
1. Từ Dashboard, click **"New +"** → **"Web Service"**
2. Chọn repository: `PhanNgocTrieu/trieu.site-page`
3. Click **"Connect"**

### 2.2. Cấu hình Web Service

**Thông tin cơ bản:**
- **Name**: `spiritual-feed` (hoặc tên bất kỳ)
- **Region**: `Singapore` (gần Việt Nam nhất)
- **Branch**: `master`
- **Runtime**: `Docker`

**Build & Deploy:**
- **Dockerfile Path**: `./Dockerfile` (Render tự detect)
- **Docker Command**: Để trống (sẽ dùng CMD trong Dockerfile)

**Instance Type:**
- Chọn **"Free"** (0$/month)

---

## Bước 3: Cấu hình Environment Variables

Trong phần **Environment**, thêm các biến sau:

```bash
# App Config
FLASK_APP=wsgi.py
FLASK_CONFIG=production
APP_ENV=prod
SECRET_KEY=<tạo-secret-key-mạnh-ở-đây>

# Database (Neon - đang dùng)
DATABASE_URL=postgresql://neondb_owner:npg_eh3tK2PmidNA@ep-small-term-ahos6cxn-pooler.c-3.us-east-1.aws.neon.tech/neondb?sslmode=require
DB_HOST=ep-small-term-ahos6cxn-pooler.c-3.us-east-1.aws.neon.tech
DB_USER=neondb_owner
DB_NAME=neondb
POSTGRES_PASSWORD=npg_eh3tK2PmidNA

# Optional (nếu dùng AI)
OPENAI_API_KEY=<your-openai-key-if-any>
```

> **Lưu ý**: Tạo SECRET_KEY mạnh bằng lệnh:
> ```bash
> python -c "import secrets; print(secrets.token_hex(32))"
> ```

---

## Bước 4: Deploy

1. Click **"Create Web Service"**
2. Render sẽ tự động:
   - Pull code từ GitHub
   - Build Docker image
   - Chạy `entrypoint.sh`
   - Start Gunicorn

**Thời gian deploy**: ~3-5 phút lần đầu

---

## Bước 5: Kiểm tra Logs

Sau khi deploy, vào tab **"Logs"** để xem:

```
=== Spiritual Feed Startup ===
Database connection successful!
Running database migrations...
Ensuring default admin user exists...
✓ Created default admin user: admin/admin12345
=== Starting Gunicorn Server ===
```

Nếu thấy logs như trên → **Deploy thành công!** ✅

---

## Bước 6: Truy cập ứng dụng

URL của bạn sẽ có dạng:
```
https://spiritual-feed.onrender.com
```

**Đăng nhập admin:**
- Username: `admin`
- Password: `admin12345`

> ⚠️ **Quan trọng**: Đổi password admin ngay sau khi deploy!

---

## Bước 7: Cấu hình Custom Domain (Tùy chọn)

1. Vào **Settings** → **Custom Domain**
2. Thêm domain của bạn (ví dụ: `spiritualfeed.com`)
3. Cập nhật DNS records theo hướng dẫn của Render
4. SSL certificate sẽ tự động được cấp

---

## 🔧 Troubleshooting

### Lỗi: "Application failed to start"
**Nguyên nhân**: Database connection failed

**Giải pháp**:
1. Kiểm tra `DATABASE_URL` có đúng không
2. Kiểm tra Neon database có online không
3. Xem logs chi tiết trong tab "Logs"

### Lỗi: "Build failed"
**Nguyên nhân**: Docker build error

**Giải pháp**:
1. Kiểm tra `Dockerfile` syntax
2. Đảm bảo `requirements.txt` đầy đủ
3. Xem build logs để debug

### Service "sleeps" sau 15 phút
**Nguyên nhân**: Free tier limitation

**Giải pháp**:
- Chấp nhận (khởi động lại ~30s khi có request)
- Hoặc upgrade lên Paid plan ($7/month)

---

## 📊 Monitoring & Maintenance

### Auto-deploy từ GitHub
Render tự động deploy khi bạn push code mới lên `master`:
```bash
git add .
git commit -m "Update feature"
git push
# Render sẽ tự động deploy sau ~2-3 phút
```

### Xem Metrics
- **Dashboard** → Service → **Metrics**
- CPU, Memory, Request count
- Response time

### Backup Database
Neon tự động backup, nhưng nên export định kỳ:
```bash
# Từ Neon Dashboard → Export
```

---

## 🎯 Checklist Deploy

- [ ] Tạo Render account
- [ ] Connect GitHub repository
- [ ] Tạo Web Service với Docker runtime
- [ ] Cấu hình Environment Variables
- [ ] Deploy và kiểm tra logs
- [ ] Truy cập URL và test
- [ ] Đổi password admin
- [ ] (Optional) Setup custom domain

---

## 💡 Tips

1. **Free tier limitations**:
   - Service ngủ sau 15 phút không hoạt động
   - 750 giờ/tháng (đủ cho 1 service chạy 24/7)
   - Bandwidth: 100GB/tháng

2. **Performance**:
   - Free tier: 512MB RAM, 0.1 CPU
   - Đủ cho ~50-100 concurrent users

3. **Scaling**:
   - Nếu cần performance tốt hơn → Upgrade lên Starter ($7/month)
   - Hoặc chuyển sang Railway/Fly.io

---

## 📞 Hỗ trợ

- Render Docs: https://render.com/docs
- Community: https://community.render.com
- Status: https://status.render.com

---

**Chúc anh deploy thành công!** 🎉

Nếu gặp vấn đề gì, cứ hỏi em nhé!
