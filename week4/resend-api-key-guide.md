# Hướng dẫn lấy API Key của Resend

## Resend là gì?

[Resend](https://resend.com) là dịch vụ gửi email dành cho developers, cung cấp API đơn giản, dễ tích hợp vào các dự án hiện đại.

---

## Bước 1: Tạo tài khoản Resend

1. Truy cập [https://resend.com](https://resend.com)
2. Nhấn **"Sign Up"** ở góc trên bên phải
3. Đăng ký bằng **GitHub**, **Google**, hoặc **Email**
4. Xác nhận email nếu đăng ký bằng email thường

---

## Bước 2: Vào trang quản lý API Key

Sau khi đăng nhập thành công:

1. Vào **Dashboard** tại [https://resend.com/api-keys](https://resend.com/api-keys)
2. Hoặc: Click vào **"API Keys"** ở thanh sidebar bên trái

---

## Bước 3: Tạo API Key mới

1. Nhấn nút **"Create API Key"**
2. Đặt tên cho key (ví dụ: `my-agent-project`)
3. Chọn quyền cho key:
   - **Full access** — có thể gửi email và quản lý domain
   - **Sending access** — chỉ dùng để gửi email *(khuyến nghị cho production)*
4. Chọn **Domain** muốn gắn key này (hoặc để mặc định `All domains`)
5. Nhấn **"Add"** để tạo

> **Lưu ý quan trọng:** API Key chỉ hiển thị **một lần duy nhất** ngay sau khi tạo. Hãy sao chép và lưu lại ngay!

---

## Bước 4: Sao chép API Key

Sau khi tạo, bạn sẽ thấy key có dạng:

```
re_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

Nhấn **Copy** để sao chép key vào clipboard.

---

## Bước 5: Thêm API Key vào dự án Agent

### Cách 1: Dùng file `.env`

mở file `.env` ở thư mục gốc của dự án:

```env
RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Cách 2: Export biến môi trường (Terminal)

```bash
export RESEND_API_KEY=re_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

### Cách 3: Dùng trong code (ví dụ Node.js)

```javascript
import { Resend } from 'resend';

const resend = new Resend(process.env.RESEND_API_KEY);
```

```python
# Python
import os
import resend

resend.api_key = os.environ["RESEND_API_KEY"]
```

---

## Kiểm tra API Key hoạt động

Chạy lệnh sau để test nhanh:

```bash
curl -X POST 'https://api.resend.com/emails' \
  -H 'Authorization: Bearer re_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx' \
  -H 'Content-Type: application/json' \
  -d '{
    "from": "onboarding@resend.dev",
    "to": ["your@email.com"],
    "subject": "Test email",
    "text": "API Key hoạt động!"
  }'
```

Nếu nhận được response `{ "id": "..." }` là thành công 

---

## Bảo mật API Key

- **Không** commit API Key lên Git — thêm `.env` vào `.gitignore`
- **Không** hard-code key trực tiếp trong source code
- Dùng **secret manager** (AWS Secrets Manager, Vercel Env, v.v.) khi deploy production
- Nếu key bị lộ, xoá ngay tại [https://resend.com/api-keys](https://resend.com/api-keys) và tạo key mới

---

## Tài liệu tham khảo

- [Resend Quickstart](https://resend.com/docs/introduction)
- [Resend API Reference](https://resend.com/docs/api-reference/introduction)
- [Resend SDK - Node.js](https://resend.com/docs/send-with-nodejs)
- [Resend SDK - Python](https://resend.com/docs/send-with-python)
