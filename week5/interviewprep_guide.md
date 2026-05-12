# AI Interview Prep SaaS

> Nền tảng chuẩn bị phỏng vấn AI/ML chuyên nghiệp được xây dựng bằng Next.js và FastAPI

> Link repo dự án: [https://github.com/tam1511/interviewprep.git]

## 📋 Mục lục

- [Giới thiệu](#giới-thiệu)
- [Tính năng](#tính-năng)
- [Công nghệ sử dụng](#công-nghệ-sử-dụng)
- [Cấu trúc dự án](#cấu-trúc-dự-án)
- [Yêu cầu hệ thống](#yêu-cầu-hệ-thống)
- [Cài đặt](#cài-đặt)
- [Cấu hình](#cấu-hình)
- [Chạy dự án](#chạy-dự-án)
- [Hướng dẫn sử dụng](#hướng-dẫn-sử-dụng)
- [Tính năng Premium](#tính-năng-premium)

---

## Giới thiệu

**AI Interview Prep** là một nền tảng SaaS giúp ứng viên chuẩn bị phỏng vấn chuyên nghiệp cho các vị trí trong lĩnh vực AI/ML như:
- Machine Learning Engineer
- AI Researcher
- Data Scientist
- MLOps Engineer
- Computer Vision Engineer
- NLP Engineer
- AI Product Manager

Ứng dụng sử dụng AI để tạo câu hỏi phỏng vấn phù hợp, gợi ý trả lời theo framework STAR, và đưa ra lộ trình học tập cá nhân hóa.

---

## Tính năng

### Tính năng chính

- **Tạo câu hỏi phỏng vấn tùy chỉnh**: 8-10 câu hỏi technical + behavioral phù hợp với role và level
- **Gợi ý trả lời theo STAR**: Framework chuyên nghiệp cho phỏng vấn
- **Đánh giá năng lực**: Phân tích điểm mạnh/yếu dựa trên kinh nghiệm
- **Lộ trình học tập**: Timeline 3-6 tháng với mục tiêu rõ ràng
- **Real-time streaming**: Kết quả được hiển thị theo thời gian thực
- **Bảo mật**: Xác thực người dùng với Clerk
- **Subscription**: Tích hợp thanh toán với Clerk Pricing

### Tính năng kỹ thuật

- Form có cấu trúc với dropdown và multi-select
- Streaming AI responses với Server-Sent Events
- Responsive UI với Tailwind CSS
- Markdown rendering cho output đẹp mắt
- Dark mode support

---

## Công nghệ sử dụng

### Frontend
- **Next.js 15** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Clerk** - Authentication & Subscription
- **React Select** - Advanced dropdowns
- **React Markdown** - Markdown rendering
- **Microsoft Fetch Event Source** - SSE streaming

### Backend
- **FastAPI** - Modern Python web framework
- **OpenAI API** (GPT-4o-mini) - AI generation
- **Pydantic** - Data validation
- **FastAPI Clerk Auth** - JWT authentication
- **Uvicorn** - ASGI server

---

## 📁 Cấu trúc dự án

```
interviewprep/
├── frontend/                 # Next.js application
│   ├── app/
│   │   ├── page.tsx         # Landing page
│   │   ├── layout.tsx       # Root layout
│   │   ├── globals.css      # Global styles
│   │   └── product/
│   │       ├── page.tsx     # Product page (protected)
│   │       └── InterviewPrepForm.tsx
│   ├── components/
│   │   └── ClientSelect.tsx # Dynamic Select component
│   ├── package.json
│   └── .env.local          # Environment variables
│
└── backend/                  # FastAPI application
    ├── app/
    │   ├── main.py          # Entry point
    │   ├── api/
    │   │   └── interview.py # API routes
    │   ├── schemas/
    │   │   └── interview.py # Pydantic models
    │   ├── prompts/
    │   │   └── interview.py # System prompts
    │   └── services/
    │       └── service.py   # Business logic
    ├── requirements.txt
    └── .env                 # Environment variables
```

---

## Yêu cầu hệ thống

- **Node.js** 18.x trở lên
- **Python** 3.9 trở lên
- **npm** hoặc **yarn**
- **pip**
- Tài khoản **Clerk** (miễn phí)
- API key **OpenAI**

---

## Cài đặt

### Bước 1: Clone hoặc tạo dự án

```bash
# Tạo thư mục dự án
mkdir interviewprep
cd interviewprep
mkdir frontend backend
```

### Bước 2: Setup Frontend

```bash
cd frontend

# Tạo Next.js app
npx create-next-app@latest .

# Chọn các options sau:
# ✅ TypeScript
# ✅ ESLint
# ✅ Tailwind CSS
# ✅ App Router
# ❌ src/ directory
# ✅ import alias (@/*)

# Cài đặt dependencies
npm install @clerk/nextjs
npm install react-select
npm install react-datepicker
npm install react-markdown remark-gfm remark-breaks
npm install @microsoft/fetch-event-source

# Dev dependencies
npm install --save-dev @types/react-select @types/react-datepicker
```

### Bước 3: Setup Backend

```bash
cd ../backend

# Tạo virtual environment (khuyến nghị)
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Tạo file requirements.txt với nội dung sau:
cat > requirements.txt << EOF
fastapi
uvicorn
pydantic
python-dotenv
openai
fastapi-clerk-auth
EOF

# Cài đặt dependencies
pip install -r requirements.txt
```

---

## Cấu hình

### Bước 1: Tạo Clerk Application

1. Truy cập [clerk.com](https://clerk.com) và đăng ký/đăng nhập
2. Tạo application mới với tên **"InterviewPrep"**
3. Chọn **Email** và/hoặc **Google** làm phương thức đăng nhập
4. Copy các API keys

### Bước 2: Cấu hình Clerk Subscription (Billing)

1. Trong Clerk Dashboard, vào **Billing** → **Subscriptions**
2. Click **Enable Subscriptions**
3. Tạo pricing plan với:
   - **Plan Name**: `premium_subscription` (phải khớp với code)
   - **Price**: Tùy ý (ví dụ: $9.99/month)
   - **Features**: Interview Prep Pro access

### Bước 3: Lấy OpenAI API Key

1. Truy cập [platform.openai.com](https://platform.openai.com)
2. Vào **API Keys** → **Create new secret key**
3. Copy key và lưu lại

### Bước 4: Environment Variables

#### Frontend `.env.local`

Tạo file `frontend/.env.local`:

```env
# Clerk Keys (từ Clerk Dashboard)
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_xxxxx
CLERK_SECRET_KEY=sk_test_xxxxx

# API Proxy
NEXT_PUBLIC_API_URL=http://localhost:8000
```

Thêm vào `frontend/next.config.ts`:

```typescript
import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  async rewrites() {
    return [
      {
        source: '/api/:path*',
        destination: 'http://localhost:8000/api/:path*',
      },
    ];
  },
};

export default nextConfig;
```

#### Backend `.env`

Tạo file `backend/.env`:

```env
# OpenAI
OPENAI_API_KEY=sk-xxxxx

# Clerk
CLERK_JWKS_URL=https://your-app.clerk.accounts.dev/.well-known/jwks.json
```

**Lấy CLERK_JWKS_URL:**
- Vào Clerk Dashboard → **API Keys**
- Copy URL dạng: `https://[your-app].clerk.accounts.dev/.well-known/jwks.json`

---

## Tạo các file code

### Backend Files

#### 1. `backend/app/schemas/interview.py`

```python
from pydantic import BaseModel
from typing import List, Optional

class InterviewPrep(BaseModel):
    full_name: str
    target_role: str
    experience_level: str
    target_company: Optional[str] = None
    technical_skills: List[str]
    years_of_experience: int = 0
    current_role: Optional[str] = None
    projects_summary: str
    interview_date: Optional[str] = None
```

#### 2. `backend/app/prompts/interview.py`

```python
SYSTEM_PROMPT = """
Bạn là một Senior Technical Interviewer chuyên về AI / Machine Learning với hơn 15 năm kinh nghiệm.

**CRITICAL: YOU MUST FOLLOW THIS EXACT FORMAT WITH BLANK LINES**

Example of CORRECT output (notice the blank lines):

## Interview Context

- Role đang phỏng vấn: Data Scientist
- Level: Mid

---

## Interview Questions

1. Bạn có thể giải thích về overfitting không?

2. Khi nào bạn sử dụng Random Forest vs Neural Network?

3. Hãy mô tả một dự án khó khăn mà bạn đã làm.

---

## Follow-up Questions

1. Về câu hỏi 1: Bạn đã xử lý overfitting như thế nào trong dự án thực tế?

2. Về câu hỏi 2: Trade-off nào bạn cân nhắc khi chọn thuật toán?

---

## Technical Depth Evaluation

- **Conceptual understanding**: Đánh giá ở đây
- **Practical experience**: Đánh giá ở đây
- **Ability to reason**: Đánh giá ở đây

Tổng kết: Mid-level

---

## Communication & Thinking Skills

**Điểm mạnh:**
- Trình bày rõ ràng
- Tư duy logic tốt

**Điểm yếu:**
- Cần cải thiện khả năng đi sâu vào chi tiết

---

## Improvement Suggestions & Learning Roadmap

**3 tháng đầu:**
- Học sâu về Deep Learning
- Practice coding trên LeetCode

**3-6 tháng:**
- Xây dựng end-to-end ML project
- Học MLOps basics

---

NOW CREATE THE INTERVIEW FOLLOWING THIS EXACT FORMAT. You MUST:
1. Add blank line after every heading (## or ###)
2. Add blank line between numbered items
3. Add blank line before and after ---
4. Add blank line between paragraphs

Include these sections:
1. Interview Context (role, level)
2. Interview Questions (8-10 câu technical + behavioral, tăng dần độ khó)
3. Follow-up Questions (1-2 câu cho mỗi technical question)
4. Technical Depth Evaluation (conceptual, practical, reasoning → Junior/Mid/Senior)
5. Communication & Thinking Skills (điểm mạnh, điểm yếu)
6. Improvement Suggestions & Learning Roadmap (3-6 tháng)

Write in Vietnamese, professional but clear.
"""

def build_system_prompt(ctx):
    return SYSTEM_PROMPT
```

#### 3. `backend/app/services/service.py`

```python
from openai import OpenAI
from app.schemas.interview import InterviewPrep
from app.prompts.interview import build_system_prompt
import json

client = OpenAI()

def stream_interview_prep(prep: InterviewPrep):
    system_prompt = build_system_prompt(prep)

    user_prompt = f"""
Candidate profile:

Full name: {prep.full_name}
Target role: {prep.target_role}
Experience level: {prep.experience_level}
Years of experience: {prep.years_of_experience}
Technical skills: {", ".join(prep.technical_skills)}

Projects summary:
{prep.projects_summary}

REMEMBER: Use double newlines (\\n\\n) between sections, before/after headings, and between list items!
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    stream = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=messages,
        stream=True,
    )

    for chunk in stream:
        delta = chunk.choices[0].delta
        if delta and delta.content:
            yield delta.content
```

#### 4. `backend/app/api/interview.py`

```python
from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from fastapi_clerk_auth import ClerkConfig, ClerkHTTPBearer, HTTPAuthorizationCredentials
import os
import json
from app.schemas.interview import InterviewPrep
from app.services.service import stream_interview_prep

router = APIRouter()

clerk_config = ClerkConfig(jwks_url=os.getenv("CLERK_JWKS_URL"))
clerk_guard = ClerkHTTPBearer(clerk_config)

@router.post("/interview")
def interview_preparation(
    prep: InterviewPrep,
    creds: HTTPAuthorizationCredentials = Depends(clerk_guard),
):
    stream = stream_interview_prep(prep)

    def event_stream():
        for text in stream:
            payload = json.dumps({"chunk": text})
            yield f"data: {payload}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
    )
```

#### 5. `backend/app/main.py`

```python
from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()

from app.api.interview import router as interview_router

app = FastAPI()
app.include_router(interview_router, prefix="/api")
```

### Frontend Files

Tạo các file như đã cung cấp trong tài liệu:
- `app/page.tsx` - Landing page
- `app/layout.tsx` - Root layout
- `app/product/page.tsx` - Product page
- `app/product/InterviewPrepForm.tsx` - Main form
- `components/ClientSelect.tsx` - Select component
- `app/globals.css` - Global styles

---

## Chạy dự án

### Terminal 1: Backend

```bash
cd backend

# Activate virtual environment nếu chưa
source venv/bin/activate  # macOS/Linux
# hoặc
venv\Scripts\activate  # Windows

# Chạy server
uvicorn app.main:app --reload --port 8000
```

Backend sẽ chạy tại: http://localhost:8000

### Terminal 2: Frontend

```bash
cd frontend

# Chạy development server
npm run dev
```

Frontend sẽ chạy tại: http://localhost:3000

---

## Hướng dẫn sử dụng

### 1. Truy cập ứng dụng
Mở trình duyệt và truy cập: http://localhost:3000

### 2. Đăng ký/Đăng nhập
- Click **"Đăng nhập"** 
- Đăng ký tài khoản mới hoặc đăng nhập bằng email/Google
- Clerk sẽ xử lý authentication

### 3. Subscribe Premium (nếu bật)
- Sau khi đăng nhập, bạn sẽ thấy **Pricing Table**
- Chọn gói **Premium Subscription**
- Hoàn tất thanh toán (test mode)

### 4. Điền thông tin phỏng vấn
- **Họ tên**: Nhập tên của bạn
- **Vị trí mục tiêu**: Chọn role (ML Engineer, Data Scientist, etc.)
- **Level kinh nghiệm**: Entry/Mid/Senior/Lead
- **Kỹ năng kỹ thuật**: Multi-select (Python, TensorFlow, PyTorch, etc.)
- **Tóm tắt dự án**: Mô tả ngắn gọn các dự án đã làm

### 5. Tạo kế hoạch phỏng vấn
- Click **"Tạo kế hoạch phỏng vấn"**
- AI sẽ stream kết quả real-time
- Xem câu hỏi, gợi ý trả lời, và lộ trình học tập

---

## Tính năng Premium

Khi enable subscription trong Clerk:

- Truy cập không giới hạn
- Tạo nhiều interview prep plans
- Lộ trình học tập cá nhân hóa
- Follow-up questions chi tiết
- Technical depth evaluation

---

## Troubleshooting

### Lỗi: "CORS Error"
**Giải pháp**: Kiểm tra `next.config.ts` đã có `rewrites` chưa

### Lỗi: "Unauthorized" khi call API
**Giải pháp**: 
- Kiểm tra `CLERK_JWKS_URL` trong backend `.env`
- Đảm bảo user đã đăng nhập

### Lỗi: OpenAI API timeout
**Giải pháp**:
- Kiểm tra `OPENAI_API_KEY` hợp lệ
- Kiểm tra credit OpenAI còn đủ

### React-Select không hiển thị
**Giải pháp**: Đã dùng dynamic import với `ssr: false` trong `ClientSelect.tsx`

---

## Tài liệu tham khảo

- [Next.js Documentation](https://nextjs.org/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Clerk Documentation](https://clerk.com/docs)
- [OpenAI API Reference](https://platform.openai.com/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)

---

## Học thêm

Dự án này là một phần của series xây dựng SaaS với AI. Bạn có thể mở rộng thêm:

- Dashboard theo dõi tiến độ
- Lưu trữ interview history
- Mock interview với AI voice
- Mobile app với React Native
- A/B testing các prompts khác nhau

---

## License

MIT License - Feel free to use for personal and commercial projects!

---

## Tác giả

Dự án được xây dựng như một phần của khóa học 

**Happy Coding! 🚀**
