# Hướng dẫn Deploy AI Interview Prep SaaS

> Hướng dẫn chi tiết deploy Full-stack AI SaaS lên Production với Railway (Backend) và Vercel (Frontend)
> Link repo dự án: [https://github.com/tam1511/interviewprep.git]

---

## Mục lục

- [Giới thiệu](#giới-thiệu)
- [Kiến trúc Deployment](#kiến-trúc-deployment)
- [Chuẩn bị Deploy](#chuẩn-bị-deploy)
- [Deploy Backend - Railway](#deploy-backend---railway)
- [Deploy Frontend - Vercel](#deploy-frontend---vercel)
- [Kiểm tra và Testing](#kiểm-tra-và-testing)
- [Custom Domain](#custom-domain)
- [Troubleshooting](#troubleshooting)
- [Monitoring và Maintenance](#monitoring-và-maintenance)

---

## Giới thiệu

Sau khi xây dựng xong ứng dụng AI Interview Prep trên localhost, bước tiếp theo là đưa nó lên internet để mọi người có thể sử dụng. Chúng ta sẽ sử dụng:

- **Railway** cho Backend (FastAPI) - Chạy Python tốt, không giới hạn timeout
- **Vercel** cho Frontend (Next.js) - Deploy nhanh, tối ưu cho React

### Tại sao tách riêng Backend và Frontend?

**Railway**: 
- Chuyên xử lý Python/FastAPI
- Không có giới hạn timeout cho long-running requests
- Streaming support tốt
- Pricing linh hoạt

**Vercel**: 
- Tối ưu cho Next.js
- Deploy cực nhanh với CDN global
- Serverless functions
- Free tier hào phóng

---

## Kiến trúc Deployment

```
┌──────────────────────────────────────────────────────┐
│                    User Browser                       │
└─────────────────────┬────────────────────────────────┘
                      │
                      ▼
┌──────────────────────────────────────────────────────┐
│              Vercel (Next.js Frontend)                │
│  • Serve static files                                 │
│  • API Routes (proxy)                                 │
│  • Clerk Authentication                               │
└─────────────────────┬────────────────────────────────┘
                      │
                      │ HTTPS Request
                      ▼
┌──────────────────────────────────────────────────────┐
│              Railway (FastAPI Backend)                │
│  • AI Processing (OpenAI)                             │
│  • Streaming responses                                │
│  • JWT Verification (Clerk)                           │
└──────────────────────────────────────────────────────┘
```

---

## Chuẩn bị Deploy

### Bước 1: Tạo các file cấu hình cần thiết

#### Backend - `railway.json`

Tạo file `backend/railway.json`:

```json
{
  "$schema": "https://railway.app/railway.schema.json",
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "uvicorn app.main:app --host 0.0.0.0 --port $PORT",
    "restartPolicyType": "ON_FAILURE",
    "restartPolicyMaxRetries": 10
  }
}
```

**Giải thích:**
- `builder: NIXPACKS` - Railway tự động detect Python và install dependencies
- `startCommand` - Command để chạy FastAPI server
- `--host 0.0.0.0` - Cho phép truy cập từ bên ngoài
- `--port $PORT` - Railway tự động inject biến PORT
- `restartPolicy` - Tự động restart nếu crash

#### Frontend - `middleware.ts`

Tạo file `frontend/middleware.ts` (cùng cấp với thư mục `app/`):

```typescript
import { clerkMiddleware, createRouteMatcher } from '@clerk/nextjs/server';

// Define which routes require authentication
const isProtectedRoute = createRouteMatcher([
  '/product(.*)',
]);

export default clerkMiddleware(async (auth, req) => {
  // Protect routes that match the matcher
  if (isProtectedRoute(req)) {
    await auth.protect();
  }
});

export const config = {
  matcher: [
    // Skip Next.js internals and all static files, unless found in search params
    '/((?!_next|[^?]*\\.(?:html?|css|js(?!on)|jpe?g|webp|png|gif|svg|ttf|woff2?|ico|csv|docx?|xlsx?|zip|webmanifest)).*)',
    // Always run for API routes
    '/(api|trpc)(.*)',
  ],
};
```

**Chức năng:**
- Khởi tạo Clerk cho toàn bộ app
- Protect route `/product` - yêu cầu đăng nhập
- Cho phép dùng `auth()` trong API routes

#### Frontend - API Proxy Route

Tạo file `frontend/app/api/interview/route.ts`:

```typescript
import { auth } from "@clerk/nextjs/server";

export async function POST(req: Request) {
  const session = await auth();
  const token = await session.getToken();

  if (!token) {
    return new Response("Unauthorized", { status: 401 });
  }

  const body = await req.text();

  const API_URL =
    process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

  const res = await fetch(`${API_URL}/api/interview`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: `Bearer ${token}`,
      Accept: "text/event-stream",
    },
    body,
  });

  // If backend failed, forward error clearly
  if (!res.ok || !res.body) {
    const errorText = await res.text();
    return new Response(errorText || "Upstream error", {
      status: res.status,
    });
  }

  // Pipe SSE stream directly
  const reader = res.body.getReader();

  const stream = new ReadableStream({
    async start(controller) {
      try {
        while (true) {
          const { done, value } = await reader.read();
          if (done) break;
          controller.enqueue(value);
        }
      } catch (err) {
        controller.error(err);
      } finally {
        controller.close();
        reader.releaseLock();
      }
    },
  });

  return new Response(stream, {
    headers: {
      "Content-Type": "text/event-stream; charset=utf-8",
      "Cache-Control": "no-cache, no-transform",
      Connection: "keep-alive",
    },
  });
}
```

**Chức năng:**
- Proxy requests từ frontend sang backend
- Forward JWT token từ Clerk
- Stream SSE responses trực tiếp
- Error handling rõ ràng

### Bước 2: Tạo `.gitignore`

Đảm bảo `.gitignore` có các dòng sau:

```gitignore
# Environment variables
.env
.env.local
.env*.local

# Python
__pycache__/
*.py[cod]
*$py.class
venv/
env/

# Next.js
.next/
out/
node_modules/

# OS
.DS_Store
Thumbs.db
```

### Bước 3: Push code lên GitHub

```bash
# Khởi tạo git (nếu chưa có)
git init

# Thêm tất cả files
git add .

# Commit
git commit -m "Initial commit - ready for deployment"

# Tạo repository trên GitHub
# Truy cập: https://github.com/new
# Tên repository: interviewprep

# Kết nối với GitHub repo
git remote add origin https://github.com/YOUR_USERNAME/interviewprep.git

# Push lên GitHub
git push -u origin main
```

**Lưu ý:** Thay `YOUR_USERNAME` bằng username GitHub của bạn.

---

## Deploy Backend - Railway

### Bước 1: Tạo tài khoản Railway

1. Truy cập: https://railway.app
2. Click **"Sign up"**
3. Chọn **"Continue with GitHub"**
4. Authorize Railway truy cập GitHub

### Bước 2: Tạo Project mới

1. Click **"New Project"**
2. Chọn **"Deploy from GitHub repo"**
3. Chọn repository **"interviewprep"** vừa push

### Bước 3: Cấu hình Root Directory

**QUAN TRỌNG**: Repository có cả backend và frontend

1. Sau khi chọn repo, Railway sẽ hỏi Root Directory
2. Chọn **`backend`** (không phải root `/`)
3. Click **"Deploy"**

Railway sẽ bắt đầu build... nhưng sẽ **FAIL** vì thiếu environment variables!

### Bước 4: Thêm Environment Variables

1. Click vào service vừa tạo
2. Vào tab **"Variables"**
3. Click **"New Variable"**

Thêm 2 biến sau:

#### Variable 1: CLERK_JWKS_URL
```
CLERK_JWKS_URL=https://your-app.clerk.accounts.dev/.well-known/jwks.json
```

**Cách lấy:**
- Vào Clerk Dashboard: https://dashboard.clerk.com
- Chọn application "InterviewPrep"
- Vào **API Keys**
- Copy **JWKS Endpoint** URL

#### Variable 2: OPENAI_API_KEY
```
OPENAI_API_KEY=sk-proj-xxxxxxxxxxxxx
```

**Cách lấy:**
- Vào OpenAI Platform: https://platform.openai.com
- Vào **API Keys**
- Create new key hoặc copy existing key

4. Click **"Add"** cho mỗi biến
5. Railway sẽ **tự động redeploy**

### Bước 5: Lấy Railway URL

Sau khi deploy thành công:

1. Click vào service
2. Vào tab **"Settings"**
3. Scroll xuống **"Networking"**
4. Copy **Domain** (dạng: `your-app.railway.app`)

**Ví dụ:**
```
https://interviewprep-backend-production-abc123.railway.app
```

### Bước 6: Kiểm tra Backend

Test backend bằng cách truy cập:

```
https://your-app.railway.app/docs
```

Bạn sẽ thấy **FastAPI Swagger UI** 🎉

---

## Deploy Frontend - Vercel

### Bước 1: Tạo tài khoản Vercel

1. Truy cập: https://vercel.com
2. Click **"Sign Up"**
3. Chọn **"Continue with GitHub"**
4. Authorize Vercel

### Bước 2: Import Project

1. Click **"Add New..."** → **"Project"**
2. Click **"Import Git Repository"**
3. Chọn repository **"interviewprep"**

### Bước 3: Cấu hình Root Directory

 **QUAN TRỌNG**: Chọn đúng folder frontend

1. Trong phần **"Configure Project"**
2. Click **"Edit"** ở Root Directory
3. Chọn **`frontend`** (không phải root `/`)

### Bước 4: Thêm Environment Variables

Trong phần **"Environment Variables"**, thêm các biến sau:

#### Variable 1: NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY
```
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_test_xxxxx
```

**Cách lấy:**
- Vào Clerk Dashboard
- Chọn app "InterviewPrep"
- Copy **Publishable Key**

#### Variable 2: CLERK_SECRET_KEY
```
CLERK_SECRET_KEY=sk_test_xxxxx
```

**Cách lấy:**
- Cùng trang với Publishable Key
- Copy **Secret Key**

#### Variable 3: NEXT_PUBLIC_API_URL
```
NEXT_PUBLIC_API_URL=https://your-app.railway.app
```

**Giá trị:** Railway URL vừa copy ở bước trước (không có `/api` ở cuối)

### Bước 5: Deploy

1. Kiểm tra lại các biến môi trường
2. Click **"Deploy"**
3. Đợi 1-2 phút để Vercel build

### Bước 6: Lấy Vercel URL

Sau khi deploy thành công:

1. Vercel sẽ show URL (dạng: `your-app.vercel.app`)
2. **Copy URL này** - chúng ta cần nó cho bước tiếp theo!

**Ví dụ:**
```
https://interviewprep-frontend.vercel.app
```

---

## Kết nối Frontend ↔ Backend

### Bước: Cập nhật Railway với Frontend URL

Backend cần biết Frontend URL để configure CORS (nếu cần):

1. Quay lại **Railway Dashboard**
2. Click vào backend service
3. Vào tab **"Variables"**
4. Click **"New Variable"**
5. Thêm biến:

```
FRONTEND_URL=https://your-app.vercel.app
```

6. Railway sẽ **tự động redeploy** backend

---

## Kiểm tra và Testing

### Test 1: Truy cập Homepage

```
https://your-app.vercel.app
```

Bạn sẽ thấy:
- Landing page với gradient đẹp
- Button "Đăng nhập"
- Features section

### Test 2: Đăng nhập

1. Click **"Đăng nhập"**
2. Chọn **Sign up with Google** (hoặc Email)
3. Hoàn tất sign up
4. Redirect về app

### Test 3: Subscribe Premium (nếu đã setup Clerk Billing)

1. Sau khi đăng nhập, vào **"/product"**
2. Bạn sẽ thấy **Pricing Table**
3. Chọn plan **Premium Subscription**
4. Hoàn tất payment flow (test mode)

### Test 4: Tạo Interview Prep

1. Điền form với thông tin:
   - Họ tên
   - Target role (chọn từ dropdown)
   - Experience level
   - Technical skills (multi-select)
   - Projects summary

2. Click **"🚀 Tạo kế hoạch phỏng vấn"**

3. Kiểm tra:
   - Loading state hiển thị
   - Text được stream real-time
   - Markdown render đúng format
   - Các section hiển thị rõ ràng

### Test 5: Kiểm tra Logs

#### Railway Logs:
1. Vào Railway Dashboard
2. Click vào service
3. Vào tab **"Deployments"**
4. Click vào deployment hiện tại
5. Xem **Build Logs** và **Deploy Logs**

#### Vercel Logs:
1. Vào Vercel Dashboard
2. Click vào project
3. Vào tab **"Logs"**
4. Xem real-time logs

---

## Custom Domain (Optional)

### Thêm Domain cho Vercel

1. Mua domain từ Namecheap, GoDaddy, hoặc Cloudflare
2. Vào Vercel project → **Settings** → **Domains**
3. Thêm domain (ví dụ: `aiinterviewprep.com`)
4. Cấu hình DNS records theo hướng dẫn của Vercel:

```
Type: A
Name: @
Value: 76.76.21.21

Type: CNAME
Name: www
Value: cname.vercel-dns.com
```

5. Đợi DNS propagate (15 phút - 48 giờ)

### Thêm Domain cho Railway

1. Vào Railway project → **Settings** → **Networking**
2. Click **"Add Custom Domain"**
3. Nhập domain (ví dụ: `api.aiinterviewprep.com`)
4. Cấu hình DNS:

```
Type: CNAME
Name: api
Value: your-app.railway.app
```

---

## Troubleshooting

### 1. Railway Build Failed

**Lỗi:** `No Python version specified`

**Giải pháp:**
Tạo file `backend/runtime.txt`:
```
python-3.11
```

Commit và push lại.

---

### 2. Vercel Build Failed - Module not found

**Lỗi:** `Cannot find module 'react-select'`

**Giải pháp:**
```bash
cd frontend
npm install
git add package-lock.json
git commit -m "Update package-lock.json"
git push
```

Vercel sẽ redeploy tự động.

---

### 3. Frontend không kết nối được Backend

**Lỗi:** `Failed to fetch` hoặc CORS error

**Kiểm tra:**
1. `NEXT_PUBLIC_API_URL` có đúng Railway URL không?
2. Railway URL có `https://` không?
3. Backend có đang chạy không? (check Railway Logs)

**Giải pháp:**
- Vào Vercel → Settings → Environment Variables
- Edit `NEXT_PUBLIC_API_URL`
- Redeploy

---

### 4. Unauthorized khi call API

**Lỗi:** `401 Unauthorized`

**Kiểm tra:**
1. `CLERK_JWKS_URL` trong Railway có đúng không?
2. User đã đăng nhập chưa?
3. Token có được gửi trong header không?

**Debug:**
```typescript
// Trong InterviewPrepForm.tsx, log token
const jwt = await getToken();
console.log('JWT:', jwt?.substring(0, 20) + '...');
```

---

### 5. Streaming không hoạt động

**Lỗi:** Response bị block hoặc không real-time

**Giải pháp:**
- Kiểm tra `app/api/interview/route.ts` có đúng code proxy không
- Đảm bảo headers có:
  ```typescript
  "Content-Type": "text/event-stream; charset=utf-8",
  "Cache-Control": "no-cache, no-transform",
  ```

---

### 6. Railway Service Sleeping

**Hiện tượng:** Request đầu tiên chậm (cold start)

**Giải pháp:**
- Upgrade lên Railway Pro ($5/month) để tắt sleeping
- Hoặc dùng cron job ping service mỗi 5 phút:
  ```bash
  */5 * * * * curl https://your-app.railway.app/docs
  ```

---

### 7. OpenAI API Error

**Lỗi:** `Incorrect API key provided` hoặc `Rate limit exceeded`

**Kiểm tra:**
1. `OPENAI_API_KEY` có đúng không?
2. API key có credit không?
3. Project có set limits không?

**Giải pháp:**
- Vào OpenAI Platform → Billing
- Add credit card và add credits
- Hoặc đợi monthly limit reset

---

## Monitoring và Maintenance

### 1. Theo dõi Railway

**Metrics quan trọng:**
- CPU usage
- Memory usage
- Request count
- Response time

**Cách xem:**
- Railway Dashboard → Service → **Metrics** tab

**Alert:** Setup alerts trong Railway settings nếu CPU/Memory cao

---

### 2. Theo dõi Vercel

**Analytics:**
- Vào project → **Analytics**
- Xem:
  - Page views
  - Unique visitors
  - Top pages
  - Performance metrics

**Speed Insights:**
- Kiểm tra Core Web Vitals
- Optimize nếu cần

---

### 3. Logs Management

**Railway Logs:**
```bash
# Xem logs real-time
railway logs
```

**Vercel Logs:**
- Real-time logs trong Dashboard
- Hoặc dùng Vercel CLI:
  ```bash
  vercel logs
  ```

---

### 4. Cost Monitoring

**Railway Free Tier:**
- $5 credit/month
- Usage-based pricing sau đó

**Vercel Free Tier:**
- Unlimited deployments
- 100GB bandwidth/month
- Serverless functions: 100GB-hours

**Mẹo tiết kiệm:**
- Optimize API calls (cache khi có thể)
- Minimize cold starts
- Monitor OpenAI usage

---

### 5. Backup và Version Control

**GitHub:**
- Mọi code đều có trên GitHub
- Git history = backup
- Easy rollback nếu cần

**Environment Variables:**
- Export từ Railway/Vercel
- Lưu vào password manager (1Password, Bitwarden)
- **KHÔNG commit** vào Git

---

### 6. Updates và Maintenance

**Cập nhật dependencies:**
```bash
# Frontend
cd frontend
npm outdated
npm update

# Backend
cd backend
pip list --outdated
pip install --upgrade <package>
```

**Deploy updates:**
```bash
git add .
git commit -m "Update dependencies"
git push
```

Railway và Vercel sẽ auto-deploy.

---

## Best Practices

### 1. Environment Variables

**DO:**
- Lưu trong Railway/Vercel
- Không có hardcode values
- Dùng prefix `NEXT_PUBLIC_` cho client-side vars

**DON'T:**
- Commit `.env` files vào Git
- Share keys publicly
- Log sensitive values

---

### 2. Error Handling

**DO:**
```typescript
try {
  const response = await fetch(...);
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}`);
  }
} catch (error) {
  console.error('Error:', error);
  // Show user-friendly message
}
```

**DON'T:**
- Silent failures
- Expose internal errors to users

---

### 3. Security

**DO:**
- Always validate JWT tokens
- Use HTTPS only
- Sanitize user inputs
- Rate limit API calls

 **DON'T:**
- Allow unauthenticated access to protected routes
- Trust client-side data
- Expose sensitive info in logs

---

### 4. Performance

 **DO:**
- Use streaming for long responses
- Implement loading states
- Cache when possible
- Optimize images

**DON'T:**
- Block UI during API calls
- Load large data at once
- Skip error boundaries

---

## 📝 Deployment Checklist

Trước khi deploy, kiểm tra:

- [ ] Code đã test kỹ trên localhost
- [ ] `.gitignore` đã có `.env*`
- [ ] `railway.json` đã tạo đúng
- [ ] `middleware.ts` đã có Clerk config
- [ ] API proxy route `/api/interview/route.ts` đã đúng
- [ ] Code đã commit và push lên GitHub
- [ ] Railway đã setup với Root Directory = `backend`
- [ ] Railway env vars: `CLERK_JWKS_URL`, `OPENAI_API_KEY`
- [ ] Vercel đã setup với Root Directory = `frontend`
- [ ] Vercel env vars: Clerk keys + `NEXT_PUBLIC_API_URL`
- [ ] Railway service đang chạy (check `/docs`)
- [ ] Vercel app accessible
- [ ] Authentication hoạt động
- [ ] API calls successful
- [ ] Streaming responses work

---

## Chúc mừng!

Bạn đã deploy thành công một **Full-stack AI SaaS Application** lên production! 

### Những gì bạn đã làm:

Xây dựng Backend API với FastAPI  
Xây dựng Frontend với Next.js  
Tích hợp Authentication với Clerk  
Tích hợp AI với OpenAI API  
Deploy Backend lên Railway  
Deploy Frontend lên Vercel  
Configure environment variables  
Setup streaming responses  

### Next Steps:

1. **Customize branding** - Thay đổi logo, colors, fonts
2. **Add email notifications** - Send interview preps qua email
3. **Database integration** - Save user history với PostgreSQL
4. **Analytics** - Track user behavior với Google Analytics
5. **i18n** - Add support for English
6. **Custom domain** - Mua và setup domain riêng

---

## Resources

- [Railway Documentation](https://docs.railway.app)
- [Vercel Documentation](https://vercel.com/docs)
- [Clerk Documentation](https://clerk.com/docs)
- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Next.js Deployment](https://nextjs.org/docs/deployment)

---

## Need Help?

Nếu gặp vấn đề:

1. Kiểm tra [Troubleshooting](#troubleshooting) section
2. Xem logs trong Railway/Vercel
3. Test từng component riêng lẻ
4. Ask on Discord/Community

---

**Happy Deploying! 🚀**
