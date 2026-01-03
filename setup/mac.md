# Setup môi trường học – macOS

Trước khi bắt đầu coding, mình biết các bạn đang rất háo hức, nhưng có **một việc bắt buộc phải làm trước**:  
**Setup environment (môi trường làm việc)** cho Data Science, LLMs và Agentic AI.

Nếu bỏ qua bước này, bạn rất dễ gặp:
- Lỗi thư viện Python
- Phiên bản không tương thích
- Dependency conflict
- Code chạy được ở máy khác nhưng không chạy được ở máy mình

Vì vậy, chúng ta sẽ setup **một môi trường Data Science “xịn sò”**, dùng xuyên suốt toàn bộ khoá học.

---

## Tổng quan 5 bước setup

1. Cài đặt Anaconda / Miniconda  
2. Cài đặt IDE (Cursor hoặc IDE bạn quen dùng)  
3. Clone source code khoá học bằng Git  
4. Tạo virtual environment cho project  
5. Thiết lập API keys (`.env`)

---

## 1. Cài đặt Anaconda / Miniconda

Nếu bạn từng làm việc với Python hoặc Data Science, có thể bạn đã từng gặp “ác mộng”:
- Cài thư viện hôm nay chạy, hôm sau lỗi
- Version Python không khớp
- Thư viện xung đột nhau

**Đó là lý do chúng ta cần virtual environment.**

### Vì sao dùng Anaconda / Miniconda?

- Tạo môi trường Python riêng cho từng project
- Quản lý thư viện AI phức tạp rất dễ:
  - numpy
  - pandas
  - scikit-learn
  - pytorch
- Phổ biến trong cộng đồng Data Science & AI

> Nếu bạn lo Anaconda nặng → **Miniconda là lựa chọn rất tốt**, nhẹ hơn nhiều và hoàn toàn đủ cho khoá học này.

---

### Cách cài đặt

1. Truy cập:  
   https://www.anaconda.com/docs/getting-started/anaconda/install
2. Chọn **Miniconda**
3. Chọn hệ điều hành **macOS**
4. Tải về và cài đặt theo hướng dẫn (Next / Agree / Continue)

Sau khi cài xong, mở **Terminal** và kiểm tra:

`conda --version`
Nếu thấy version hiện ra → cài đặt thành công.

---

## 2. Cài đặt IDE – Cursor (tuỳ chọn)

Trong khoá học này, mình sẽ sử dụng Cursor để minh hoạ.

Bạn không bắt buộc phải dùng Cursor.
VS Code hoặc IDE khác đều hoàn toàn OK.

Cursor là một trải nghiệm mới, có AI hỗ trợ code. Đôi khi gợi ý chưa chính xác, nhưng đáng để thử trong giai đoạn học.

Cài đặt Cursor

Truy cập:
https://www.cursor.sh

Download bản macOS

Cài đặt và mở Cursor

Khi Cursor hỏi các tuỳ chọn ban đầu → chọn mặc định

**Thiết lập nhanh (rất quan trọng)**

Sau khi mở Cursor, nhấn:

`Cmd + Shift + P`


Gõ:

`Shell Command: Install 'code' command`


Nhấn Enter → OK

Bước này cho phép bạn mở Cursor trực tiếp từ Terminal bằng lệnh code .

---

## 3. Clone source code khoá học bằng Git
Kiểm tra Git

macOS thường đã có Git sẵn.
Mở Terminal và kiểm tra:

`git --version`


Nếu chưa có, macOS sẽ gợi ý bạn cài đặt Command Line Tools → chỉ cần đồng ý.

**Tạo thư mục chứa project**:

`mkdir ~/projects`

`cd ~/projects`

Clone repo khoá học

Vào GitHub repo của khoá học

Copy HTTPS link

Quay lại Terminal:

`git clone https://github.com/tam1511/aicourse.git`


Sau khi xong, toàn bộ code của khoá học đã nằm trong máy bạn.

---

## 4. Tạo virtual environment cho project

Vào thư mục project vừa clone:

`cd aicourse`


Kiểm tra các file:

`environment.yml` → dùng cho conda

`requirements.txt` → dùng nếu bạn không dùng conda

Tạo môi trường conda
`conda env create -f environment.yml`


Đợi vài phút để cài toàn bộ thư viện.

Kích hoạt môi trường:

`conda activate llms`

Mở project bằng Cursor
`code .`

Cursor sẽ mở đúng thư mục project và dùng môi trường llms.

---

## 5. Thiết lập API keys (.env)

Để code chạy mượt mà, chúng ta cần thiết lập API keys.

Tạo file `.env`

Trong thư mục gốc của project:

Chuột phải → New File

Đặt tên: `.env`

File `.env` là secret, chỉ tồn tại trên máy bạn và không được push lên GitHub.

OpenAI API Key

Truy cập:
https://platform.openai.com

Vào Billing và nạp tối thiểu 5 USD

Tạo API key tại:
https://platform.openai.com/api-keys

Thêm vào file .env:

`OPENAI_API_KEY=sk-proj-xxxxxxxx`

Hugging Face API Token (miễn phí)

Truy cập:
https://huggingface.co

Click avatar → Settings → Access Tokens

Tạo token mới

Thêm vào .env:

`HF_TOKEN=your_huggingface_token`


Lưu file lại → hoàn tất.

**Kiểm tra lại từ đầu (khuyến nghị)**

Nếu bạn chưa quen:

`cd ~/projects/aicourse`

`conda activate llms`

`code .`


Sau đó vào:

`week1/day1`


Và chúng ta có thể bắt đầu coding ngay bây giờ!
