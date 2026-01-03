# Setup môi trường học – Windows

Trước khi bắt đầu coding, chúng ta cần làm **một việc rất quan trọng**: **Setup environment (môi trường làm việc)** cho Data Science, LLMs và Agentic AI.

Mình biết các bạn đang rất háo hức để vào code, nhưng nếu bỏ qua bước này, rất dễ gặp:
- Lỗi thư viện
- Phiên bản Python không khớp
- Dependency conflict
- “Chạy được trên máy bạn, không chạy trên máy mình”

Vì vậy, chúng ta sẽ làm việc này **một lần cho thật chuẩn**.

---

## Tổng quan 5 bước setup

1. Cài đặt Anaconda / Miniconda  
2. Cài đặt IDE (Cursor hoặc IDE bạn quen dùng)  
3. Clone source code của khoá học từ GitHub  
4. Tạo virtual environment cho project  
5. Thiết lập API keys (`.env`)

---

## 1. Cài đặt Anaconda / Miniconda

Nếu bạn đã từng làm việc với Python hoặc Data Science, có thể bạn đã từng “ác mộng” với việc cài thư viện:
- Version không khớp
- Thư viện xung đột
- Cài hôm nay chạy, mai lỗi

**Đó chính là lý do chúng ta cần virtual environment.**

### Vì sao chọn Anaconda / Miniconda?

- Tạo **môi trường riêng cho từng project**
- Quản lý tốt các thư viện như:
  - numpy
  - pandas
  - scikit-learn
  - pytorch
- Phổ biến trong Data Science & AI

> Nếu bạn lo Anaconda nặng → **Miniconda là lựa chọn rất tốt** và nhẹ hơn nhiều.

### Cách cài đặt

1. Truy cập:  
   https://www.anaconda.com/docs/getting-started/anaconda/install
2. Chọn **Miniconda** (khuyến nghị)
3. Chọn hệ điều hành **Windows**
4. Tải về và cài đặt (chỉ cần nhấn **Next / OK** theo mặc định)

Sau khi cài xong, mở **Command Prompt** và kiểm tra:

`conda --version`
Nếu thấy version hiện ra là thành công.

## 2. Cài đặt IDE – Cursor (hoặc IDE khác)

Trong khoá học này, mình sẽ sử dụng Cursor.

Bạn không bắt buộc phải dùng Cursor.
VS Code hoặc IDE khác đều được.

Cursor là một trải nghiệm mới, có AI hỗ trợ code rất đáng để thử.

Cài đặt Cursor

Truy cập:
https://www.cursor.sh

Download và cài đặt

Khi mở lần đầu, chọn tất cả các tuỳ chọn mặc định

Thiết lập nhanh (rất quan trọng)

Mở Cursor → nhấn:

`Ctrl + Shift + P`


Gõ:

`Shell Command: Install 'code' command`


Nhấn Enter → OK
Bước này giúp bạn mở Cursor nhanh từ terminal bằng code .

---

## 3. Clone source code khoá học bằng Git
Kiểm tra Git

Mở Command Prompt, gõ:

git --version


Nếu chưa có Git, cài tại:
https://git-scm.com/install/windows

Tạo thư mục `projects`:

`mkdir %USERPROFILE%\projects`

`cd %USERPROFILE%\projects`

Clone repo:

Vào GitHub repo của khoá học

Copy HTTPS link

Quay lại terminal:

`git clone https://github.com/tam1511/aicourse.git`


Sau khi xong, toàn bộ source code đã nằm trong máy bạn.

---

## 4. Tạo virtual environment cho project

Vào thư mục project:

`cd aicourse`


Kiểm tra file:

`environment.yml` → dùng cho conda

`requirements.txt` → dùng cho pip (nếu cần)

Tạo môi trường conda
`conda env create -f environment.yml`


Đợi vài phút để cài thư viện.

Kích hoạt môi trường:

`conda activate llms`


Mở project bằng Cursor:

`code .`

---

## 5. Thiết lập API Keys (.env)
Tạo file `.env`

Trong thư mục gốc của project:

Chuột phải → New File

Đặt tên: `.env`

File `.env` là secret, chỉ nằm trên máy bạn.

OpenAI API Key

Truy cập:
https://platform.openai.com

Vào Billing và nạp tối thiểu 5 USD

Tạo API key tại:
https://platform.openai.com/api-keys

Thêm vào file .env:

`OPENAI_API_KEY=sk-proj-xxxxxxxx`

Hugging Face Token (miễn phí)

Truy cập:
https://huggingface.co

Avatar → Settings → Access Tokens

Create token

Thêm vào .env:

`HF_TOKEN=your_huggingface_token`

### Hoàn tất setup

Để chắc chắn mọi thứ hoạt động:

`cd %USERPROFILE%\projects\aicourse`

`conda activate llms`

`code .`


Vào:

`week1/day1`


Và chúng ta bắt đầu coding ngay bây giờ!
