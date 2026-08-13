---
sidebar_position: 99
title: ShopAI Hoàn Thiện
---

# SHOPAI HOÀN THIỆN — CHUẨN SẢN PHẨM ĐẲNG CẤP (CUỐI KHÓA)

Tài liệu này là **kim chỉ nam nghiệm thu**.  
Hoàn thành đủ 11 Sprint trong `CHUONG_*_LT_MOI.md` **và** tick hết các ô bên dưới = ShopAI đạt mức **sản phẩm học thuật–thực chiến hoàn thiện** (portfolio Junior+).

> Mỗi chương chỉ tích thêm tính năng — **cấm** phá tính năng đã PASS ở chương trước.  
> Sprint cuối mỗi chương = **bài thực hành của chương đó** (có khung 📋 + checklist trong từng file).

---

## 0. Định nghĩa “đẳng cấp / hoàn thiện” trong khóa này

ShopAI cuối khóa phải thỏa **đồng thời** 4 lớp:

| Lớp | Ý nghĩa |
|-----|---------|
| **A. Chạy được** | Mobile + Backend cùng lúc, máy ảo/máy thật |
| **B. Đủ hành trình mua hàng** | Register/Login → duyệt SP → giỏ → checkout → đơn `PENDING` → Pay `PAID` → xem hóa đơn |
| **C. Đủ “app thương mại + AI”** | Camera/scan, bảo mật token, App Lock, chat AI không lộ Key |
| **D. Đủ chất lượng nghề** | Test tự động + CI + giám sát crash + đường build Release |

Thiếu một lớp → **chưa** gọi là hoàn thiện đẳng cấp.

---

## 1. Luồng người dùng bắt buộc (phải demo được trước hội đồng)

```
Mở app
  → (có token SecureStore?) MainTabs : AuthStack (Login ↔ Register)
  → Đăng ký mới HOẶC Đăng nhập NestJS JWT thật (demo@shopai.com)
  → Tab Trang chủ: SP từ Nest + InfiniteQuery + Zod + pull-to-refresh
  → Bấm SP → Chi tiết (productId) → Mua ngay
  → Tab Giỏ (icon + badge) → sửa SL / xóa → Thanh toán (Modal)
  → Checkout useMutation + Bearer → Nest ghi Prisma status PENDING → thấy orderId → giỏ trống
  → Tab Đơn hàng: thấy đơn vừa tạo → Chi tiết hóa đơn
  → Bấm “Thanh toán giả lập” → status PAID (POST /api/orders/:id/pay)
  → Restart Nest → đơn vẫn còn trong DB (PAID)
  → Quét mã (máy thật) → haptic → mã về Home / mở Detail
  → LocationBadge ước tính phí ship
  → Vào nền > timeout → App Lock / biometric lại
  → AI Chat (history + retry + gợi ý) qua Nest proxy — không có Gemini Key trong app
  → Đăng xuất → về Login (không Back lén vào Main)
```

---

## 2. Bản đồ tính năng ↔ Chương (tích lũy)

| Tính năng “đẳng cấp” | Chương khóa | Bắt buộc? |
|----------------------|-------------|-----------|
| Repo chạy được, GitHub | 1 | Có |
| Kiến trúc `src/` + Core UI + Fetch nền | 2 | Có |
| Design System + Dark Mode + Button variants | 3 | Có |
| FlashList grid + Reanimated + SafeArea + refresh | 4 | Có |
| Auth Flow **Login + Register** + Tab icon/badge + Detail + Deep Link | 5 | Có |
| Zustand persist cart + **Orders local PENDING/PAID** + InfiniteQuery + Checkout + Zod + Axios + RTK đề cương | 6 | Có |
| Vision Camera scan + haptic + GPS ship | 7 | Có (máy thật) |
| SecureStore + Biometric + App Lock + AI UX | 8 | Có |
| Nest + JWT (**login + register**) + Prisma + AI proxy + Orders (**list/detail/pay**) chống gian lận giá | 9 | Có |
| Crashlytics + EAS Update + ≥1 đường Release build | 10 | Có (đường thoát nếu thiếu Apple) |
| Jest + RNTL + Maestro + Nest Supertest + CI | 11 | Có |

---

## 3. Kiến trúc cuối khóa (cây Provider — phải giữ nguyên)

```
SafeAreaProvider
  └─ QueryClientProvider
      └─ Redux Provider          ← chỉ phục vụ bài tập đề cương / demo RTK
          └─ ThemeProvider       ← Dark/Light (Ch.3)
              └─ NavigationContainer (+ linking shopai://)
                  ├─ AuthStack (Login ↔ Register → Nest JWT)
                  └─ RootStackNavigator
                       ├─ MainTabs (MainTabNavigator)
                       │     ├─ HomeStack: Home, Detail, Scanner, AIChat
                       │     ├─ Cart (+ badge)
                       │     └─ Orders (lịch sử đơn)
                       ├─ Checkout (Modal)
                       └─ OrderDetail (chi tiết hóa đơn + Pay)
```

Token: **SecureStore** (Ch.8). Cart: **Zustand persist**. Products/Orders/AI/Auth: **Nest + Prisma**.

---

## 4. Checklist nghiệm thu cuối khóa

### A. Chạy được
- [ ] iOS Simulator **hoặc** Android Emulator chạy ShopAI
- [ ] Backend `shopai-backend` chạy LAN (`0.0.0.0:3000`), Mobile gọi được qua `API_BASE_URL` / `env.ts`
- [ ] Máy thật: Camera Sprint 7 PASS (hoặc có biên bản hoãn có lý do + vẫn PASS phần còn lại)

### B. Hành trình sản phẩm (bắt buộc demo)
- [ ] Login / Logout / **Register** — conditional navigator an toàn (AuthStack Login ↔ Register)
- [ ] Login gọi `POST /api/auth/login` thật; Register gọi `POST /api/auth/register` thật — không còn `mock_token`
- [ ] Token SecureStore — tắt app mở lại vẫn vào Main (trừ khi App Lock yêu cầu biometric)
- [ ] App Lock: vào nền quá lâu → phải xác thực lại
- [ ] Home: Nest + `useInfiniteQuery` + Zod + phân biệt lỗi mạng / Zod
- [ ] Pull-to-refresh Home
- [ ] Detail theo `productId` (Deep Link cũng mở được)
- [ ] Giỏ: thêm/xóa/tổng tiền; persist sau kill app
- [ ] Tab Giỏ: icon + badge số lượng
- [ ] Checkout: `useMutation` → `POST /api/orders` + Bearer → đơn **`PENDING`** + `orderId`; chỉ xóa giỏ khi thành công
- [ ] Tab **Đơn hàng**: danh sách từ Nest; **Chi tiết hóa đơn**; **Pay** → **`PAID`**
- [ ] Restart Nest: đơn vẫn còn (Prisma)
- [ ] Orders không Token → `401`
- [ ] Dark Mode hoạt động
- [ ] Deep Link native + JS (ít nhất 1 URL demo)

### C. AI & Native (đẳng cấp thương mại học thuật)
- [ ] Scanner: quyền chuẩn, không spam scan, haptic khi trúng
- [ ] LocationBadge / ước tính ship trên Home
- [ ] AI Chat: history + typing + Thử lại + gợi ý; gọi Nest `/api/ai/chat`
- [ ] **Không** còn Gemini API Key trong bundle Mobile (`geminiConfig` đã xóa)

### D. Chất lượng nghề (bắt buộc để gọi là “hoàn thiện”)
- [ ] Jest: `formatCurrency` + `useCartStore` (logic tiền) PASS
- [ ] RNTL: `ShopButton` PASS
- [ ] Maestro: `login_home` PASS; `cart_checkout` PASS (Nest đang chạy)
- [ ] Nest: Unit `AuthService` (mock Prisma) PASS
- [ ] Nest: Supertest login + register + orders `401`/`201` + pay PASS (khuyến nghị)
- [ ] CI GitHub Actions: lint + test Mobile xanh (khuyến nghị thêm `backend-test`)
- [ ] Crashlytics: nhận test crash (dev) + non-fatal checkout/fetch
- [ ] `eas.json` đủ profile; **≥1** minh chứng build Release (local AAB/IPA **hoặc** `eas build` preview)

### E. Đề cương (nộp kèm đồ án)
- [ ] `src/store/redux/` RTK demo chạy được
- [ ] Giải thích miệng: Context vs RTK vs Zustand; vì sao ShopAI chọn Zustand
- [ ] Giải thích Drawer vs Tab; Deep Link vs navigate thường

---

## 5. Rubric chấm nhanh (gợi ý giảng viên)

| Mức | Điều kiện |
|-----|-----------|
| **Đạt** | A + B đủ; C thiếu Camera có lý do; D thiếu 1–2 ô phụ |
| **Khá** | A+B+C đủ; D đủ Jest/RNTL/CI cơ bản |
| **Giỏi / Đẳng cấp khóa** | **A+B+C+D+E đủ** + demo mạch mục 1 trôi chảy < 10 phút |
| **Xuất sắc** | Giỏi + OTA demo hoặc EAS Build + Maestro checkout xanh + biên bản bảo mật (Key không trong APK) |

---

## 6. Xu hướng công nghệ đã nằm trong sản phẩm (2025–2026)

| Xu hướng | Chương |
|----------|--------|
| New Architecture (JSI/Fabric) | 1–2 |
| FlashList | 4 |
| Zustand + TanStack Query + Zod | 6 |
| SecureStore + Biometrics + App Lock | 8 |
| NestJS + JWT + Prisma + Order lifecycle PENDING/PAID | 9 |
| EAS Update / EAS Build | 10 |
| Maestro + Jest + RNTL + Supertest + CI | 11 |

---

*Cập nhật cùng giáo trình ShopAI — dùng để chấm đồ án / thi thực hành cuối kỳ. Mỗi Sprint trong `CHUONG_*` phải đóng góp đúng một phần checklist này.*
