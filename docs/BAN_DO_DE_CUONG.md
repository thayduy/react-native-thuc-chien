---
sidebar_position: 0
title: Bản Đồ Đề Cương
---

# BẢN ĐỒ ĐỀ CƯƠNG CHÍNH THỨC ↔ GIÁO TRÌNH SHOPAI (11 CHƯƠNG)

> [!IMPORTANT]
> **Xem thêm `SHOPAI_HOAN_THIEN.md`** — checklist nghiệm thu **ShopAI hoàn thiện đẳng cấp** cuối khóa (A chạy được / B hành trình mua / C AI+Native / D chất lượng / E đề cương). Mỗi chương có **một Sprint** = bài thực hành chương đó; khung 📋 nằm đầu mỗi Sprint trong `CHUONG_*_LT_MOI.md`.

Tài liệu này giúp giảng viên và học viên biết: **mỗi mục đề cương nằm ở chương nào**, và **ShopAI áp dụng chỗ nào**.

> Giáo trình dạy **11 chương thực chiến ShopAI**, nhưng **phủ đủ 7 chương đề cương chính thức**. Một số chủ đề đề cương được dạy sâu hơn (Zustand, NestJS…) nhưng vẫn bắt buộc có phần đề cương (Context API, Redux Toolkit, Jest, RNTL, RN Debugger, Flipper…).

---

## Bảng ánh xạ nhanh

| Đề cương chính thức | File giáo trình ShopAI | Ghi chú |
|---------------------|------------------------|---------|
| **Ch.1** Giới thiệu RN (1.1.1–1.1.5) | `CHUONG_1_LT_MOI.md` | **Chỉ** công cụ + môi trường + chạy được app. Mục đề cương **1.2** (Props/State…) dạy ở `CHUONG_2` |
| **Ch.2** Core Components + Fetch/Axios (2.1, 2.2) | `CHUONG_2` + `CHUONG_4` (list) + `CHUONG_6` (API sâu) | View/Text/Image… ở Ch.2; FlatList sâu ở Ch.4; Fetch/Axios nhập môn ở Ch.2, đào sâu Interceptor ở Ch.6 |
| **Ch.3** Hooks (useState, useEffect, useContext, useReducer, useMemo, useCallback) | `CHUONG_2` (useState/useEffect) + `CHUONG_3` (useContext/useReducer/useMemo/useCallback) | Xem trước Context ở Ch.3 → hệ thống hóa lại đầy đủ ở Ch.6 (5.1.1) |
| **Ch.4** Navigation (Stack, Tab, Drawer, Params, Deep Link) | `CHUONG_5_LT_MOI.md` | Stack, Tab, Drawer, params, Deep Link — dùng `MainTabNavigator` xuyên suốt từ Ch.6 |
| **Ch.5** State Management (5.1.1 Context, 5.1.2 Redux Toolkit, 5.2.1–5.2.4 RTK chi tiết) | `CHUONG_6_LT_MOI.md` (Phần 6.2 → 6.4) | Context API + Redux Toolkit đầy đủ (đề cương) + **Zustand (lựa chọn Production của ShopAI)** — có bảng so sánh 3 giải pháp |
| **Ch.6** API & hiển thị dữ liệu (6.1 Fetch/Axios sâu, 6.2 Map data + Pagination) | `CHUONG_6_LT_MOI.md` (Phần 6.5 → 6.8) + `CHUONG_9` | React Query, Axios Instance + Interceptor, Pagination (`onEndReached`/`useInfiniteQuery`); NestJS (Ch.9) = nguồn API thật |
| **Ch.7** Kiểm thử & Debug (Jest, RNTL, RN Debugger, Flipper) | `CHUONG_11_LT_MOI.md` (Phần 11.1 → 11.3) | Maestro E2E và CI/CD (GitHub Actions/Fastlane) = nâng cao, mở rộng ngoài đề cương |

---

## Chi tiết từng mục đề cương

### Đề cương Chương 1 — Giới thiệu React Native
| Mục | Nội dung | Nơi học |
|-----|----------|---------|
| 1.1.1 | React Native là gì? | `CHUONG_1_LT_MOI.md` — Phần 1.1 |
| 1.1.2 | RN so với React | `CHUONG_1` |
| 1.1.3 | Expo CLI vs React Native CLI | `CHUONG_1` (+ cài môi trường Phần 1.5) |
| 1.1.4 | Tổng quan kiến trúc RN | `CHUONG_1` (khái quát) → `CHUONG_2` (Bridge/JSI sâu) |
| 1.1.5 | VS Code / Cursor | `CHUONG_1` — Phần 0.4 + 1.1.5 |
| *(nền, ngoài chữ đề cương)* | Terminal, Git, Node/npm | `CHUONG_1` — Phần 0 |
| 1.2.1 | Component & JSX | **`CHUONG_2`** — Phần 2.2 *(dời khỏi Ch.1 để tránh trùng)* |
| 1.2.2 | State & Props | **`CHUONG_2`** — Phần 2.3 |
| 1.2.3 | Xử lý sự kiện | **`CHUONG_2`** — kèm Pressable / TextInput |
| 1.2.4 | Style | **`CHUONG_2`** (nền StyleSheet) → `CHUONG_3` (Design System) |

### Đề cương Chương 2 — Core Components + Fetch/Axios nhập môn
| Mục | Nội dung | Nơi học |
|-----|----------|---------|
| 2.1.1 | View, Text, Image, TextInput, ScrollView | `CHUONG_2_LT_MOI.md` — Phần 2.5 |
| 2.1.2 | Button / Touchable / Pressable | `CHUONG_2` — mục 2.5.6 |
| 2.1.3 | FlatList, SectionList (cơ bản) | `CHUONG_2` — Phần 2.5; đào sâu Virtualization + `FlashList` ở `CHUONG_4` |
| 2.2.1 | Fetch API | `CHUONG_2` — Phần 2.7 (lý thuyết + Sprint) |
| 2.2.2 | Axios (nhập môn) | `CHUONG_2` — Phần 2.7 (nhận diện, Sprint không bắt buộc cài); nâng cấp **Instance + Interceptor** ở `CHUONG_6` (Phần 6.6) |

### Đề cương Chương 3 — Hooks
| Mục | Nội dung | Nơi học |
|-----|----------|---------|
| `useState` | Quản lý State nội bộ Component | `CHUONG_2` — Phần 2.3–2.4 |
| `useEffect` | Side Effect, gọi API, cleanup | `CHUONG_2` |
| `useContext` | Chia sẻ dữ liệu toàn cục, chống Prop Drilling | `CHUONG_3` — Phần 3.3 (xem trước) → `CHUONG_6` — Phần 6.2 (đầy đủ, đề cương 5.1.1) |
| `useReducer` | Quản lý State phức tạp bằng Action/Reducer | `CHUONG_3` — Phần 3.3 |
| `useMemo` / `useCallback` | Tối ưu Re-render, ghi nhớ giá trị/hàm | `CHUONG_3` — Phần 3.5 |
| `React.memo` | Chặn Re-render Component con | `CHUONG_3` — Phần 3.5 |

### Đề cương Chương 4 — Navigation
| Mục | Nội dung | Nơi học |
|-----|----------|---------|
| Stack Navigator | Điều hướng chồng màn hình (Push/Pop) | `CHUONG_5_LT_MOI.md` — Phần 5.1–5.2 |
| Tab Navigator | Điều hướng đáy (Bottom Tab) — `MainTabNavigator` | `CHUONG_5` — Phần 5.1 mục 2 (lý thuyết) + thực hành Sprint `MainTabNavigator` (Bước 5); dùng xuyên suốt từ `CHUONG_6` đến `CHUONG_11` |
| Drawer Navigator | Menu kéo từ cạnh màn hình | `CHUONG_5` — Phần 5.5 |
| Truyền Params giữa màn hình | Route Params, `navigation.navigate(name, params)` | `CHUONG_5` — Phần 5.3 |
| Deep Linking | Mở App trực tiếp từ Link Web | `CHUONG_5` — Phần 5.4 |
| Auth Flow (đăng nhập/**đăng ký**/đăng xuất điều hướng) | State Machine Auth Stack (Login ↔ Register) ↔ Main Stack | `CHUONG_5` — Phần 5.2 + Sprint Bước 2.5; đồng bộ Zustand `CHUONG_6`; API thật `CHUONG_9` |
| *(Bổ sung thương mại)* | Lịch sử đơn / chi tiết hóa đơn / Pay `PENDING`→`PAID` | UI `CHUONG_6` Bước 9.6; Nest `CHUONG_9` Bước 7f + 9f |

### Đề cương Chương 5 — State Management
| Mục | Nội dung | Nơi học |
|-----|----------|---------|
| 5.1.1 | Context API (`createContext`, `Provider`, `useContext`) | `CHUONG_6_LT_MOI.md` — Phần 6.2 (đầy đủ; xem trước ở `CHUONG_3` Phần 3.3) |
| 5.1.2 | Redux Toolkit — vì sao có Redux, RTK vs Redux cổ điển | `CHUONG_6` — Phần 6.4, mục 1–2 |
| 5.2.1 | Cài đặt `@reduxjs/toolkit` + `react-redux` | `CHUONG_6` — Phần 6.4, mục 3 |
| 5.2.2 | `createSlice` (Action + Reducer gộp), `configureStore` | `CHUONG_6` — Phần 6.4, mục 4–5 |
| 5.2.3 | `Provider`, `useSelector`, `useDispatch` | `CHUONG_6` — Phần 6.4, mục 6 |
| 5.2.4 | Ví dụ thực hành `counterSlice`/`cartSlice` + Bài tập bắt buộc `src/store/redux/` | `CHUONG_6` — Phần 6.4 mục 4 (lý thuyết) + Sprint 6, Bước 10 (bắt buộc nộp bài) |
| *(Bổ sung so sánh)* | Bảng so sánh Context vs Redux Toolkit vs Zustand | `CHUONG_6` — Phần 6.4, mục 7 |
| *(Lựa chọn Production ShopAI)* | Zustand — Client State thật của Auth/Cart | `CHUONG_6` — Phần 6.1 & 6.3 |

### Đề cương Chương 6 — API & hiển thị dữ liệu
| Mục | Nội dung | Nơi học |
|-----|----------|---------|
| 6.1 | Fetch/Axios sâu: Axios Instance (`axios.create`), Interceptor gắn Token tự động, xử lý lỗi 401 tập trung | `CHUONG_6_LT_MOI.md` — Phần 6.6 |
| 6.1 *(nền)* | Server State, Caching, `staleTime`/`gcTime` với TanStack Query | `CHUONG_6` — Phần 6.5 |
| 6.2 | Map dữ liệu ra danh sách (`FlatList`/`renderItem`) | `CHUONG_4` (Virtualization) + `CHUONG_6` (kết hợp Query/Zod) |
| 6.2 | Pagination: `FlatList.onEndReached` + `page` state, và `useInfiniteQuery` | `CHUONG_6` — Phần 6.8 |
| *(Bổ sung Type-Safety)* | Zod validate dữ liệu API trước khi hiển thị | `CHUONG_6` — Phần 6.7 |
| *(Nguồn API thật)* | Backend NestJS + **JWT Guards** + **Prisma/SQLite** + Auth register + Orders list/detail/pay | `CHUONG_9` |

### Đề cương Chương 7 — Kiểm thử & Debug
| Mục | Nội dung | Nơi học |
|-----|----------|---------|
| Jest Unit Test | Test hàm thuần túy (`formatCurrency`) | `CHUONG_11_LT_MOI.md` — Phần 11.1 (lý thuyết) + Sprint 11, Bước 5–6 |
| React Native Testing Library (RNTL) | Integration Test Component (`render`, `fireEvent.press`, `ShopButton`) | `CHUONG_11` — Phần 11.2 (lý thuyết) + Sprint 11, Bước 7–8 |
| React Native Debugger / DevTools | Bật React Native DevTools (built-in RN 0.73+), xem Component tree, Profiler | `CHUONG_11` — Phần 11.3, mục 1 + Sprint 11, Bước 9 |
| Flipper | Network Inspector, Layout Inspector, vai trò lịch sử & vì sao "deprecated-ish" | `CHUONG_11` — Phần 11.3, mục 2 |
| *(Nâng cao, ngoài đề cương)* | Maestro E2E Test | `CHUONG_11` — Phần 11.4 + Sprint 11, Phần 1 |
| *(Nâng cao, ngoài đề cương)* | CI/CD với GitHub Actions + phác thảo Fastlane | `CHUONG_11` — Phần 11.5 + Sprint 11, Phần 4 |

---

## Mạch dự án ShopAI (logic giữa các chương)

```
Ch1: Công cụ + môi trường + init ShopAI chạy được (chưa dạy Props/State)
  → Ch2: JSX/Props/State/Hooks + kiến trúc + Core Components + Fetch/Axios nhập môn + cấu trúc src/
  → Ch3: UI Kit (Typography, Input, Button) + useContext/useReducer (xem trước)
  → Ch4: Home Grid + FlashList (List Virtualization)
  → Ch5: Auth (**Login + Register**) + Tab (MainTabNavigator) + Detail + Deep Link
  → Ch6: Context/Redux Toolkit (đề cương) + Zustand (Production) + React Query + Axios Interceptor + Pagination + Zod + Cart + **Lịch sử đơn / HĐ + Pay PENDING→PAID (local)**
  → Ch7: Camera quét mã
  → Ch8: SecureStore + AI chat (tạm client)
  → Ch9: NestJS + JWT (**login + register**) + Orders (**list/detail/pay**) + giấu API Key
  → Ch10: Crashlytics + OTA
  → Ch11: Jest + RNTL + RN DevTools/Flipper (đề cương) + Maestro + CI (nâng cao)
```

---

## Ghi chú quan trọng cho giảng viên

- **Chương 1 ShopAI** tập trung công cụ + môi trường + chạy được app. Mục đề cương 1.2 nằm ở `CHUONG_2`.
- **Không có mục đề cương nào bị bỏ sót.** Mọi chủ đề đề cương (gồm cả 1.2, Context, Redux Toolkit, Jest, RNTL, RN Debugger, Flipper…) đều có phần lý thuyết + code ví dụ trong các file `CHUONG_*`, dù ShopAI chọn công cụ khác (Zustand, Maestro) làm giải pháp Production.
- **Zustand không thay thế việc học Redux Toolkit.** Sprint 6 có bước bắt buộc riêng (`src/store/redux/`) độc lập với Cart Production — học viên phải nộp bài này để đạt chuẩn đề cương.
- **Maestro/CI-CD là phần mở rộng**, không nằm trong 7 chương đề cương chính thức nhưng được giữ lại vì giá trị thực chiến cao cho học viên khi đi làm.
