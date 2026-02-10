# Hướng Dẫn Setup Dự Án

## Hỗ Trợ

Nếu bạn gặp lỗi không fix được hoặc ý kiến đóng góp, hãy thoải mái liên hệ với mình qua:

- Email: timiofficial.vn@gmail.com
- LinkedIn: https://www.linkedin.com/in/timi11
- Group: https://discord.com/invite/HhnY8DRA

Chúng ta sẽ xử lý cùng nhau. Nếu bạn thấy mình trả lời chậm quá, hãy gửi lên group để tất cả mọi người có thể hỗ trợ.

---

## Bước 1: Đăng Ký Vercel

### 1.1 Truy cập trang web Vercel
1. Mở trình duyệt web và truy cập: https://vercel.com
2. Click vào nút **Sign Up** ở góc trên bên phải

### 1.2 Chọn gói dịch vụ
- Chọn **Hobby** (dành cho các dự án cá nhân)
- Nhập tên của bạn

### 1.3 Chọn phương thức đăng ký
Bạn có thể chọn một trong các phương thức sau:

- **GitHub** (khuyến nghị) - Click "Continue with GitHub" và authorize Vercel
- **GitLab** - Click "Continue with GitLab" và authorize Vercel
- **Bitbucket** - Click "Continue with Bitbucket" và authorize Vercel
- **Email** - Nhập địa chỉ email và làm theo các bước xác minh

### 1.4 Hoàn tất quá trình đăng ký
- Complete the onboarding process
- Bạn có thể bỏ qua việc tạo team

---

## Bước 2: Tạo Dự Án Mới

### 2.1 Di chuyển đến thư mục làm việc

Mở terminal/cmd và gõ lệnh:

```bash
cd ../projects/aicourse/week5
```

Hoặc nếu bạn đang ở đúng vị trí, chỉ cần:

```bash
cd week5
```

### 2.2 Tạo folder riêng cho dự án của bạn

**Lưu ý quan trọng:**

Mình khuyến khích bạn **tạm bỏ qua folder mẫu** và tạo một folder riêng với tên gọi khác, rồi follow mình từng bước.

**Lý do:**
- Trong suốt buổi này, chúng ta sẽ tạo nhiều repo nhỏ cho từng phần
- Việc có folder riêng sẽ giúp bạn dễ quản lý hơn

### 2.3 Kiến thức nền tảng về Git/GitHub

**Yêu cầu bắt buộc:**

Nếu bạn chưa quen với Git hay GitHub, hãy đọc hướng dẫn về Git trước khi tiếp tục.

- Đây là kiến thức nền tảng bắt buộc
- Không quá phức tạp nhưng rất quan trọng
- Nếu bạn không biết, sẽ rất dễ bị lạc trong các bước sau

---

## Bước 3: Tạo FastAPI Server

### 3.1 Giới thiệu về FastAPI

**FastAPI** là một web framework để build API với:
- Hiệu suất cao
- Đơn giản và dễ sử dụng
- Hỗ trợ tốt cho việc làm sản phẩm

### 3.2 Công nghệ sử dụng

Backend của chúng ta sẽ được xây dựng bằng:
- **Python** - Ngôn ngữ lập trình
- **FastAPI** - Web framework

---

## Bước 4: Cài Đặt Node.js

### 4.1 Tại sao cần Node.js?

Node.js là yêu cầu bắt buộc cho Vercel CLI.

### 4.2 Tải và cài đặt

Truy cập trang download chính thức: https://nodejs.org/en/download

#### Chọn phương thức cài đặt:

**Option 1: Direct Download**
- Download trực tiếp installer cho hệ điều hành của bạn

**Option 2: Package Manager**
- **Mac:** Sử dụng Homebrew
- **Windows:** Sử dụng Chocolatey
- **Linux:** Sử dụng package manager của distro

**Option 3: Version Manager (khuyến nghị)**
- `nvm` - Node Version Manager
- `fnm` - Fast Node Manager
- `volta` - JavaScript Tool Manager

### 4.3 Kiểm tra cài đặt

Sau khi cài đặt xong:

1. Mở một terminal/cmd window mới
2. Chạy các lệnh sau để kiểm tra:

```bash
node --version
```

```bash
npm --version
```

Nếu hiển thị số phiên bản, bạn đã cài đặt thành công! 

---

## Các Bước Tiếp Theo

Sau khi hoàn tất các bước setup trên, bạn đã sẵn sàng để:
- Tạo dự án FastAPI
- Deploy lên Vercel
- Xây dựng API cho ứng dụng AI

**Chúc bạn học tập hiệu quả!** 

---

## Tài Nguyên Tham Khảo

- [Vercel Documentation](https://vercel.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Node.js Documentation](https://nodejs.org/docs/latest/api/)
- [Git Documentation](https://git-scm.com/doc)
