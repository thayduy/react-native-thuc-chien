---
sidebar_position: 6
title: Chương 6
---

# GIÁO TRÌNH LÝ THUYẾT & THỰC CHIẾN
## CHƯƠNG 6: DỮ LIỆU ĐÁM MÂY - STATE MANAGEMENT (CONTEXT, REDUX TOOLKIT, ZUSTAND) & SERVER STATE (REACT QUERY)
**Thời lượng:** 6 tiết Lý thuyết + 4 tiết Thực hành

---

> [!IMPORTANT]
> **Thực hành chương = Sprint ShopAI cuối file.** Hoàn thành Sprint này để đạt mục tiêu chương. Hoàn thành đủ 11 chương theo `SHOPAI_HOAN_THIEN.md` = sản phẩm ShopAI **hoàn thiện đẳng cấp**.

## 📚 MỤC TIÊU HỌC TẬP

Sau khi hoàn thành chương này, học viên sẽ:
- ✅ Nắm vững **Context API** của React thuần (`createContext`, `Provider`, `useContext`) và biết rõ khi nào dùng, khi nào KHÔNG nên dùng.
- ✅ Làm chủ **Redux Toolkit** (`@reduxjs/toolkit` + `react-redux`) đúng chuẩn đề cương: `createSlice`, `configureStore`, `Provider`, `useSelector`, `useDispatch` — kể cả tại sao Redux cổ điển (classic Redux) bị xem là cồng kềnh.
- ✅ Hiểu rõ sự sụp đổ của đế chế Redux cổ điển trên nền tảng Mobile và tại sao ShopAI (dự án thực chiến) chọn **Zustand** làm giải pháp chính, trong khi vẫn hiểu và biết dùng Redux Toolkit theo đúng yêu cầu đề cương.
- ✅ Phân định ranh giới tuyệt đối giữa **Client State** (Trạng thái UI, Giỏ hàng) và **Server State** (Dữ liệu từ API Database).
- ✅ Giải phẫu kiến trúc của **TanStack Query (React Query)**: Khái niệm Caching, StaleTime, và Background Fetching.
- ✅ Dùng **`useMutation`** để GHI dữ liệu lên Server (đặt hàng, thêm Wishlist...) đúng chuẩn: trạng thái `isPending`/`isError`, `invalidateQueries` để làm mới Cache liên quan, và `onSuccess`/`onError` để xử lý hậu-quả (dọn giỏ hàng, thông báo lỗi).
- ✅ Dùng **Axios chuyên nghiệp**: tạo `axios.create()` instance riêng và gắn **Interceptor** tự động đính kèm Token xác thực vào mọi Request.
- ✅ Hiển thị danh sách dữ liệu lớn với **Pagination** (phân trang) — không load 1000 sản phẩm cùng lúc làm treo máy.
- ✅ Biết cách chuẩn hóa và xác thực Dữ liệu bằng **Zod** (Type-Safety từ Font-end đến Back-end).
- ✅ Làm Giỏ hàng **sống sót qua mỗi lần tắt/mở lại App** bằng `zustand/middleware` **persist** + `AsyncStorage`, và biết **MMKV** (`react-native-mmkv`) là lựa chọn Production nhanh hơn khi cần.
- ✅ Hoàn thiện vòng đời mua sắm bằng **`CheckoutScreen`** (đặt hàng, tự xóa giỏ), **Lịch sử đơn / Chi tiết hóa đơn** (`OrdersScreen` + `OrderDetailScreen`), trạng thái thanh toán giả lập **`PENDING` → `PAID`**, và kiến trúc **`RootStackNavigator`** (Modal Stack bọc ngoài `MainTabNavigator`).
- ✅ **Thực chiến:** Đưa Token xác thực và Giỏ hàng lên "Đám mây" Zustand (có Persist), Fetch danh sách sản phẩm từ API Mock thông qua React Query có phân trang + Pull-to-refresh, hoàn thành luồng Thanh toán + quản lý hóa đơn (local), và hoàn thành bài tập bắt buộc đề cương với Redux Toolkit.

> [!IMPORTANT]
> **Đây là chương "chốt hạ" luồng mua sắm cốt lõi của ShopAI:** Duyệt sản phẩm → Thêm giỏ (persist) → Thanh toán → **Đơn `PENDING` vào Lịch sử** → (tuỳ chọn) **Thanh toán giả lập → `PAID`** → xem Chi tiết hóa đơn. Từ Chương 7 trở đi (Camera, Bảo mật, AI…) nâng cấp Native/AI; **Chương 9** nối Nest thật cho Register / Orders / Pay — không phá UI đã dựng ở đây.

> [!NOTE]
> **Ánh xạ đề cương chính thức (Chương 5 "State Management" + Chương 6 "API & hiển thị dữ liệu"):** Context API (5.1.1), Redux Toolkit đầy đủ (5.1.2, 5.2.1–5.2.4), Fetch/Axios sâu (6.1), Map/render dữ liệu + Pagination (6.2) — **TẤT CẢ được dạy đủ trong chương này**. ShopAI (dự án thực chiến xuyên suốt khóa) chọn **Zustand** làm giải pháp Production chính thức vì nhẹ và ít boilerplate hơn, nhưng học viên vẫn phải hoàn thành bài tập Redux Toolkit riêng để đúng chuẩn đề cương (xem Sprint 6 — Bước bắt buộc).

---

## ☁️ PHẦN 6.1: CĂN BỆNH PROP DRILLING VÀ SỰ SỤP ĐỔ CỦA REDUX

### 1. Nỗi đau Prop Drilling
Ở Chương 5, để đổi trạng thái Đăng nhập từ `LoginScreen`, ta phải truyền hàm `onLogin` từ thẻ `<App>` xuống `<AuthStack>`, rồi truyền tiếp vào `<LoginScreen>`.
Hãy tưởng tượng màn hình Nút Thanh Toán nằm sâu 10 lớp: `<App>` -> `<MainStack>` -> `<Tab>` -> `<Home>` -> `<ProductList>` -> `<ProductCard>` -> `<CheckoutButton>`.
Việc truyền một cái `State` xuyên qua 10 lớp Component trung gian (những kẻ chẳng dùng gì đến dữ liệu đó) được gọi là **Prop Drilling** (Khoan giếng Props). Code trở nên vô cùng rối rắm và không thể tái sử dụng.

### 2. Sự cứu rỗi của Global State (Trạng thái Toàn cục)
Global State giống như việc bạn tạo ra một "Đám mây" (Store) lơ lửng trên cùng. Bất kỳ Component nào (dù sâu bao nhiêu) cần lấy hoặc sửa dữ liệu, chỉ việc vươn tay thẳng lên Đám mây để thao tác.

### 3. Tại sao Redux thoái trào trên Mobile?
5 năm trước, **Redux** là vị vua. Nhưng để đổi một biến `count` từ 0 lên 1 bằng Redux, bạn phải viết 3 file: `Action`, `Reducer`, `Dispatch` (Khái niệm Boilerplate - code thừa thãi quá nhiều). Hơn nữa, Redux thiết kế theo kiểu **Centralized Store** (Một cục Store khổng lồ nhét mọi thứ vào), làm tăng thời gian khởi động App (Cold start) trên điện thoại rất đáng kể.

**Có 3 hướng đi phổ biến để giải quyết Prop Drilling** mà chương này sẽ dạy đủ cả ba: **Context API** (có sẵn trong React, không cần cài thêm gì), **Redux Toolkit** (chuẩn công nghiệp, đúng đề cương chính thức) và **Zustand** (giải pháp ShopAI chọn cho Production vì nhẹ và ít boilerplate).

---

## 🧩 PHẦN 6.2: CONTEXT API — GIẢI PHÁP CÓ SẴN CỦA REACT (ĐỀ CƯƠNG 5.1.1)

### 0. 🖐️ CẦM TAY CHỈ VIỆC — Nhìn "Prop Drilling vs Store" bằng hình vẽ

Trước khi học Context/Zustand/Redux, hãy nhìn sự khác biệt giữa 2 cách đưa dữ liệu xuống Component con — đây là hình ảnh sẽ đi theo bạn suốt cả chương này.

```
❌ CÁCH 1 — PROP DRILLING (phải "khoan giếng" truyền tay qua từng tầng):

   App
    │   props: { token, onLogout }
    ▼
  MainTabNavigator        ⚠️ Tầng này KHÔNG hề dùng token/onLogout,
    │   props: { token, onLogout }   chỉ nhận rồi truyền tiếp xuống — code thừa!
    ▼
  HomeStackNavigator       ⚠️ Tầng này CŨNG KHÔNG dùng, lại tiếp tục truyền
    │   props: { token, onLogout }
    ▼
  HomeScreen  ✅ Chỉ có tầng CUỐI CÙNG này mới thực sự cần dùng token/onLogout


✅ CÁCH 2 — STORE / CONTEXT Ở CHÍNH GIỮA (mọi tầng tự "vươn tay" lên lấy):

                    ┌─────────────────────────────┐
                    │   ☁️  STORE / CONTEXT         │
                    │   { token, cartItems, ... }  │
                    └───────────────┬─────────────┘
                     ▲              ▲              ▲
                     │              │              │
                    App        HomeScreen     ProfileScreen
              (không cần    (useAuthStore()   (useAuthStore()
               biết gì cả)   lấy trực tiếp,    lấy trực tiếp,
                             không qua Props)  không qua Props)
```

> [!TIP]
> Nhìn hình trên là hiểu ngay lý do tồn tại của cả **Context API**, **Zustand** lẫn **Redux Toolkit**: cả ba đều là các cách hiện thực hoá "đám mây ở giữa" đó — chỉ khác nhau ở cách viết code và cách tối ưu Re-render (sẽ so sánh chi tiết ở bảng cuối Phần 6.4).

> [!NOTE]
> Bạn đã "xem trước" `useContext` ở Chương 3 (Phần 3.3) với ví dụ `ThemeContext`. Phần này hệ thống hóa lại đầy đủ **Context API** theo đúng mục 5.1.1 đề cương, đặt cạnh Redux Toolkit và Zustand để bạn thấy rõ vì sao dự án ShopAI không chọn Context cho state nặng như Giỏ hàng.

**Context API** là vũ khí đầu tiên và có sẵn trong chính thư viện React (không cần `npm install` gì thêm) để giải quyết Prop Drilling. Nó cho phép một Component Cha "phát sóng" dữ liệu, và bất kỳ Component Con nào (dù sâu bao nhiêu tầng) đều có thể "bắt sóng" mà không cần nhận qua Props.

### 1. Ba bước dùng Context API

1. **`createContext()`**: Tạo ra "kênh phát sóng".
2. **`<Context.Provider value={...}>`**: Bọc quanh Component Cha để bắt đầu phát dữ liệu xuống toàn bộ cây con.
3. **`useContext(Context)`**: Component Con bất kỳ gọi hook này để "bắt sóng" giá trị, không cần Props.

**Ví dụ mini: `ThemeContext` (chế độ Sáng/Tối)** — Tạo file `src/context/ThemeContext.tsx`:

```tsx
import React, { createContext, useContext, useState } from 'react';

interface ThemeContextType {
  isDarkMode: boolean;
  toggleTheme: () => void;
}

// Bước 1: Tạo kênh phát sóng (giá trị mặc định chỉ dùng khi thiếu Provider)
const ThemeContext = createContext<ThemeContextType | undefined>(undefined);

// Bước 2: Provider — Component Cha bọc quanh App để phát sóng xuống toàn bộ cây con
export const ThemeProvider = ({ children }: { children: React.ReactNode }) => {
  const [isDarkMode, setIsDarkMode] = useState(false);
  const toggleTheme = () => setIsDarkMode((prev) => !prev);

  return (
    <ThemeContext.Provider value={{ isDarkMode, toggleTheme }}>
      {children}
    </ThemeContext.Provider>
  );
};

// Bước 3: Custom Hook để bất kỳ Component con nào cũng "bắt sóng" được, không cần Props
export const useTheme = () => {
  const context = useContext(ThemeContext);
  if (!context) {
    throw new Error('useTheme phải được gọi bên trong <ThemeProvider>');
  }
  return context;
};
```

Bọc `App.tsx` bằng `<ThemeProvider>`, sau đó ở BẤT KỲ Component con nào (dù sâu 10 tầng) chỉ cần:

```tsx
const SettingsScreen = () => {
  const { isDarkMode, toggleTheme } = useTheme(); // Không cần Props!
  return (
    <ShopButton
      title={isDarkMode ? 'Đang Tối — Chuyển Sáng' : 'Đang Sáng — Chuyển Tối'}
      onPress={toggleTheme}
    />
  );
};
```

### 2. Giới hạn chí mạng của Context API — Vì sao KHÔNG dùng cho Giỏ hàng?

Context API có một nhược điểm nghiêm trọng: **mỗi khi giá trị trong `Provider` thay đổi, TOÀN BỘ cây Component con bên trong Provider đó sẽ bị Re-render lại**, kể cả những Component không hề dùng giá trị vừa đổi. Nếu bạn nhét `CartContext` (giỏ hàng, thay đổi liên tục khi bấm "Mua ngay") vào Context API bao quanh toàn bộ App, mỗi lần thêm 1 sản phẩm vào giỏ, hàng trăm Component khác (Header, Footer, ProductList...) đều bị vẽ lại một cách vô nghĩa → Giật lag trên máy yếu.

> [!IMPORTANT]
> **Nguyên tắc chọn công cụ:**
> - **Context API**: Hợp với dữ liệu ÍT thay đổi, phát sóng rộng (Theme Sáng/Tối, Ngôn ngữ, thông tin User cơ bản ít cập nhật).
> - **Global state NẶNG, thay đổi liên tục** (Giỏ hàng, danh sách sản phẩm, Auth Token cập nhật nhiều lần) → PHẢI dùng **Zustand** hoặc **Redux Toolkit** (mục tiếp theo), vì cả hai đều tối ưu để chỉ render đúng Component nào thực sự "đăng ký" lắng nghe phần dữ liệu đó, không kéo theo cả cây Component.

---

## 🧠 PHẦN 6.3: CLIENT STATE (ZUSTAND) VÀ KIẾN TRÚC LƯU TRỮ

**Client State** là những dữ liệu do người dùng tạo ra trên điện thoại và chưa (hoặc không cần) gửi lên Server ngay lập tức. (Ví dụ: Chế độ ban đêm Dark Mode, Ngôn ngữ Tiếng Việt, Token Đăng nhập, Hàng đang chọn trong Giỏ).

**Cú pháp khai báo Zustand chuẩn Enterprise:**
```tsx
import { create } from 'zustand';

// 1. Định nghĩa khuôn mẫu (Type) bằng TypeScript
interface AuthState {
  token: string | null;
  login: (newToken: string) => void;
  logout: () => void;
}

// 2. Khởi tạo Đám mây (Store)
export const useAuthStore = create<AuthState>((set) => ({
  token: null, // Giá trị ban đầu
  
  // Các hàm thay đổi State
  login: (newToken) => set({ token: newToken }),
  logout: () => set({ token: null }),
}));
```
Khi dùng ở Component bất kỳ, chỉ cần gọi `useAuthStore()` là lấy được dữ liệu. Tốc độ thực thi chớp nhoáng vì nó không dùng Context API của React (Context API sẽ bắt toàn bộ cây component render lại, còn Zustand thì báo thẳng cho component nào cần nó).

### 🖐️ CẦM TAY CHỈ VIỆC — Mini Cart Store đầy đủ trong 1 file, đọc từng khối trước khi vào Sprint

Trước khi gặp bản `useCartStore` đầy đủ (có `persist`) ở Sprint 6 phía dưới, hãy nhìn phiên bản TỐI GIẢN dưới đây để nắm chắc **4 khối bắt buộc** của mọi Zustand Store: khai báo Type, khởi tạo Store, đọc State bằng `get()`, và sửa State bằng `set()`.

```ts
// useCartStore.ts — Phiên bản tối giản (CHƯA có persist, sẽ thêm ở Phần 6.9)
import { create } from 'zustand';

// Khối 1: Khuôn mẫu 1 dòng hàng trong giỏ
interface CartItem {
  id: string;
  name: string;
  price: number;
  quantity: number;
}

// Khối 2: Khuôn mẫu toàn bộ Store — vừa có dữ liệu (items), vừa có hành động (addItem...)
interface CartState {
  items: CartItem[];
  addItem: (item: Omit<CartItem, 'quantity'>) => void;
  removeItem: (id: string) => void;
  totalPrice: () => number;
}

// Khối 3: Khởi tạo Store thật bằng create<CartState>((set, get) => ({...}))
export const useCartStore = create<CartState>((set, get) => ({
  items: [], // Giá trị ban đầu — giỏ hàng rỗng

  // Khối 4: set(...) — CÁCH DUY NHẤT hợp lệ để thay đổi State, luôn trả về Object State mới
  addItem: (item) =>
    set((state) => ({ items: [...state.items, { ...item, quantity: 1 }] })),

  removeItem: (id) =>
    set((state) => ({ items: state.items.filter((i) => i.id !== id) })),

  // Khối 5: get() — CÁCH ĐỌC State hiện tại từ BÊN TRONG Store (không phải trong Component)
  totalPrice: () => get().items.reduce((sum, i) => sum + i.price * i.quantity, 0),
}));
```

**Bảng giải thích từng khối cho người mới:**

| Khối | Cú pháp | Giải thích cho người mới |
|---|---|---|
| Import | `import { create } from 'zustand'` | `create` là hàm DUY NHẤT bạn cần từ Zustand để khởi tạo 1 "đám mây" (Store) mới |
| `interface CartItem` | Khuôn TypeScript cho 1 dòng hàng | Bắt buộc phải có `id`, `name`, `price`, `quantity` — thiếu trường nào, TypeScript báo lỗi ngay lúc code |
| `interface CartState` | Khuôn cho CẢ Store | Trộn lẫn cả dữ liệu (`items`) và hành động (`addItem`, `removeItem`, `totalPrice`) trong CÙNG một khuôn — khác Context API phải tách `value` riêng |
| `create<CartState>((set, get) => ({...}))` | Khởi tạo Store | `set` và `get` là 2 tham số Zustand tự động cấp cho bạn — không cần import thêm gì khác |
| `set((state) => ({ items: [...] }))` | Ghi/sửa State | **`set`** = "Tôi muốn ĐỔI dữ liệu". Luôn nhận vào `state` cũ, trả ra Object chứa phần cần đổi (Zustand tự gộp phần còn lại) |
| `get().items.reduce(...)` | Đọc State | **`get`** = "Tôi muốn ĐỌC dữ liệu hiện tại", dùng khi cần tính toán ngay bên trong Store (không dùng Hook `useCartStore()` được ở đây vì đang ở ngoài Component) |
| *(sẽ thêm ở Phần 6.9)* | `persist(...)` bọc ngoài `create(...)` | Chỉ cần bọc thêm 1 lớp — Zustand tự lưu `items` xuống ổ cứng và tự đọc lại khi mở App, KHÔNG cần sửa gì bên trong `addItem`/`removeItem`/`totalPrice` |

> [!TIP]
> Ghi nhớ ngắn gọn: **`set` để GHI, `get` để ĐỌC** — ngay trong Store, không qua Hook. Ở Component thì luôn dùng `useCartStore((state) => state.xxx)` như các ví dụ Sprint 6 phía dưới.

---

## 🏛️ PHẦN 6.4: REDUX TOOLKIT — CHUẨN CÔNG NGHIỆP CỦA ĐỀ CƯƠNG

Dù ShopAI chọn Zustand làm giải pháp Production, **Redux Toolkit (RTK)** vẫn là kiến thức **bắt buộc theo đề cương chính thức** và vẫn là công cụ phổ biến nhất trong tuyển dụng thực tế — rất nhiều công ty lớn (đặc biệt dự án cũ, dự án Enterprise nhiều năm tuổi) vẫn dùng Redux. Phần này dạy đủ: vì sao có Redux, RTK khác Redux cổ điển ra sao, và cách viết một Store RTK hoàn chỉnh.

### 1. Vì sao có Redux? Redux cổ điển (Classic Redux) cồng kềnh ra sao?

Redux ra đời để giải quyết đúng vấn đề Prop Drilling như Context/Zustand, nhưng theo triết lý **một chiều (Unidirectional Data Flow)** rất nghiêm ngặt: UI bắn ra một **Action** (mô tả "việc gì đã xảy ra") → **Reducer** (hàm thuần túy) nhận Action đó và tính ra State mới → UI tự động cập nhật theo State mới.

Với Redux cổ điển (trước RTK), để làm một tính năng "Tăng số đếm" đơn giản, bạn phải viết tối thiểu 3-4 file: `actionTypes.js`, `actions.js`, `reducer.js`, rồi tự tay dùng `combineReducers` và cấu hình `createStore` với Middleware thủ công. Rất nhiều **Boilerplate** (code khuôn mẫu lặp lại) chỉ để làm một việc nhỏ.

### 2. Redux Toolkit (RTK) giải quyết vấn đề đó thế nào?

**Redux Toolkit** là bộ công cụ CHÍNH THỨC do đội ngũ Redux phát hành để thay thế hoàn toàn cách viết Redux cổ điển. RTK gộp Action + Reducer vào một khối duy nhất gọi là **Slice**, tự động sinh Action Creators, và cho phép viết code "như đang mutate trực tiếp" (thực chất bên dưới dùng thư viện Immer để đảm bảo Immutability an toàn).

### 3. Cài đặt

```bash
npm install @reduxjs/toolkit react-redux
```

### 4. `createSlice` — Gộp Action và Reducer vào một nơi

Ví dụ một `counterSlice` kinh điển để nắm cú pháp trước khi áp dụng vào `cartSlice` thật ở Sprint 6:

```ts
// src/store/redux/counterSlice.ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';

interface CounterState {
  value: number;
}

const initialState: CounterState = { value: 0 };

const counterSlice = createSlice({
  name: 'counter',
  initialState,
  reducers: {
    // Viết như đang "mutate" trực tiếp state.value — RTK dùng Immer lo phần Immutability
    increment: (state) => {
      state.value += 1;
    },
    decrement: (state) => {
      state.value -= 1;
    },
    incrementByAmount: (state, action: PayloadAction<number>) => {
      state.value += action.payload;
    },
  },
});

// RTK TỰ ĐỘNG sinh ra các Action Creators — không cần viết tay actionTypes/actions nữa!
export const { increment, decrement, incrementByAmount } = counterSlice.actions;
export default counterSlice.reducer;
```

### 5. `configureStore` — Ráp các Slice thành một Store

```ts
// src/store/redux/store.ts
import { configureStore } from '@reduxjs/toolkit';
import counterReducer from './counterSlice';

export const store = configureStore({
  reducer: {
    counter: counterReducer, // Mỗi Slice là một "ngăn" riêng trong Store lớn
    // cartRedux: cartReducer,  <- sẽ thêm ở Sprint 6 khi làm bài tập bắt buộc
  },
});

// Tự suy ra Type cho useSelector/useDispatch — chuẩn TypeScript
export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;
```

### 6. `Provider`, `useSelector`, `useDispatch` — Kết nối vào React

Bọc App bằng `<Provider>` của `react-redux` (tương tự `QueryClientProvider` đã học ở phần Server State):

```tsx
import { Provider } from 'react-redux';
import { store } from '@store/redux/store';

function App() {
  return (
    <Provider store={store}>
      {/* Toàn bộ App bên trong giờ có thể dùng useSelector/useDispatch */}
    </Provider>
  );
}
```

Trong bất kỳ Component nào, đọc State bằng `useSelector`, bắn Action bằng `useDispatch`:

```tsx
import { useSelector, useDispatch } from 'react-redux';
import { increment, decrement } from '@store/redux/counterSlice';
import type { RootState } from '@store/redux/store';

const CounterDemo = () => {
  const count = useSelector((state: RootState) => state.counter.value); // Đọc State
  const dispatch = useDispatch(); // Lấy hàm bắn Action

  return (
    <View>
      <Text>Số đếm: {count}</Text>
      <ShopButton title="Tăng" onPress={() => dispatch(increment())} />
      <ShopButton title="Giảm" onPress={() => dispatch(decrement())} />
    </View>
  );
};
```

### 7. Bảng so sánh: Context API vs Redux Toolkit vs Zustand

| Tiêu chí | Context API | Redux Toolkit | Zustand |
|---|---|---|---|
| Cần cài thêm thư viện? | ❌ Không (có sẵn React) | ✅ `@reduxjs/toolkit` + `react-redux` | ✅ `zustand` |
| Boilerplate (code khuôn mẫu) | Thấp | Trung bình (Slice, Store, Provider) | Rất thấp (như 1 Custom Hook) |
| Hiệu năng Re-render | Kém (render cả cây con) | Tốt (chỉ render Component dùng `useSelector` liên quan) | Rất tốt (chỉ render đúng Component đăng ký) |
| DevTools debug Time-travel | ❌ Không có | ✅ Redux DevTools rất mạnh | ⚠️ Có nhưng đơn giản hơn |
| Độ phổ biến tuyển dụng | Trung bình | Rất cao (chuẩn đề cương, nhiều dự án cũ) | Đang tăng nhanh (dự án mới) |
| Hợp dùng cho | Theme, Locale, state ít đổi | Dự án lớn, nhiều Dev, cần chuẩn hóa nghiêm ngặt | Dự án vừa/nhỏ, muốn gọn nhẹ, tốc độ code nhanh |
| **Lựa chọn của ShopAI** | Không dùng cho state nặng | ⚠️ Học đủ, làm bài tập bắt buộc (đề cương) | ✅ **Chọn cho Production** (Cart, Auth thật) |

> [!IMPORTANT]
> **ShopAI chọn Zustand làm giải pháp chính thức cho Production** vì ít boilerplate hơn và tốc độ phát triển nhanh hơn cho quy mô dự án của khóa học. Tuy nhiên, **học viên BẮT BUỘC phải hoàn thành bài tập Redux Toolkit** ở Sprint 6 phía dưới để đúng chuẩn đề cương chính thức — kiến thức Redux vẫn rất cần khi đi làm ở các công ty dùng dự án Redux có sẵn.

---

## 📡 PHẦN 6.5: SERVER STATE (TANSTACK QUERY) - CÁCH MẠNG FETCHING

### 1. Tại sao dùng Fetch / Axios chay lại là sai lầm?
Cách truyền thống sinh viên hay làm: Gọi `useEffect` -> Bật loading -> Dùng `axios.get()` -> Tắt loading -> Đổ data vào `useState`.
**Nhược điểm chí mạng:**
- Bạn vào màn hình Home -> App gọi API mất 2 giây. Bạn bấm sang giỏ hàng, rồi bấm quay lại màn hình Home -> App LẠI GỌI API MẤT 2 GIÂY NỮA. (Tốn băng thông 4G, người dùng chửi vì app chậm).
- Thiếu cơ chế tự động thử lại khi mất mạng.
- Thiếu cơ chế tự động làm mới khi có người khác thay đổi dữ liệu trên server.

### 2. Sự ưu việt của React Query (TanStack Query)
React Query không phải là thư viện để gọi mạng (nó vẫn dùng fetch/axios bên dưới). Nó là **Thư viện Quản lý Trạng thái Máy chủ (Server State Management) và Bộ đệm (Caching).**

**Nguyên lý hoạt động (The Cache Lifecycle):**
1. Lần đầu vào màn hình: Trạng thái là `Loading` -> Gọi API mất 2s -> Có data -> Lưu vào **Cache (Bộ đệm RAM)**.
2. Bạn thoát màn hình ra ngoài. React Query giữ dữ liệu đó trong RAM. Dữ liệu bắt đầu bị "Thiu" (Stale).
3. 5 giây sau bạn quay lại màn hình đó. React Query lập tức lấy dữ liệu trong Cache ra đập vào mặt người dùng (Trải nghiệm tức thời 0s). NGAY SAU ĐÓ, dưới nền (Background), nó âm thầm gọi lại API Server xem có gì mới không. Nếu có dữ liệu mới, nó tự động vẽ đè lên giao diện cũ mà người dùng không hề thấy giật lag.

**Các khái niệm sống còn:**
- `staleTime`: Khoảng thời gian dữ liệu được coi là "còn tươi" (Fresh). Nếu để `staleTime: 60000` (1 phút), trong 1 phút đó dù người dùng có quay lại màn hình 100 lần, app KHÔNG BẬT API LÊN GỌI NỮA, mà lấy thẳng trong RAM ra.
- `gcTime` (Garbage Collection): Khi người dùng thoát màn hình, dữ liệu trong RAM sẽ bị dọn dẹp sau bao lâu để chống tràn RAM. (Mặc định 5 phút).

### 3. 🖐️ CẦM TAY CHỈ VIỆC — 3 trạng thái giao diện BẮT BUỘC phải xử lý

Người mới học `useQuery` thường chỉ code phần "có data" rồi quên mất 2 trạng thái còn lại, khiến app bị "màn hình trắng" vài giây đầu hoặc crash khi mất mạng. Hãy luôn hình dung đủ 3 khối giao diện sau trước khi viết code:

```
┌───────────────────────┐   ┌───────────────────────┐   ┌───────────────────────┐
│ 📱  isLoading = true   │   │ 📱  isError = true     │   │ 📱  data tồn tại       │
│ ─────────────────────  │   │ ─────────────────────  │   │ ─────────────────────  │
│                        │   │                        │   │  [Ảnh SP1] [Ảnh SP2]  │
│                        │   │      ❌                │   │  [Ảnh SP3] [Ảnh SP4]  │
│        ⏳              │   │  Lỗi mạng hoặc dữ      │   │  [Ảnh SP5] [Ảnh SP6]  │
│   (ActivityIndicator)  │   │  liệu không hợp lệ!    │   │                        │
│                        │   │   [ Thử lại ]          │   │  (kéo xuống để         │
│                        │   │                        │   │   Pull-to-refresh)     │
└───────────────────────┘   └───────────────────────┘   └───────────────────────┘
   Query chạy LẦN ĐẦU,          queryFn ném lỗi/reject       fetch thành công,
   chưa hề có Cache nào          (mất mạng, Zod chặn dữ      hiển thị danh sách
   để hiển thị tạm                liệu bẩn...)                thật bằng FlashList
```

**Bảng: Cờ (flag) nào điều khiển khối giao diện nào?**

| Cờ trả về từ `useQuery` | Khi nào bằng `true`/có giá trị | UI tương ứng nên hiển thị | Vị trí trong code Sprint 6 |
|---|---|---|---|
| `isLoading` | Lần gọi ĐẦU TIÊN, chưa có Cache để hiển thị tạm | `<ActivityIndicator>` chiếm toàn màn hình, ẩn hết danh sách | `{isLoading && <ActivityIndicator ... />}` |
| `isError` | `queryFn` ném lỗi (`reject`/`throw`) — VD: mất mạng, hoặc Zod chặn dữ liệu bẩn | Thông báo lỗi rõ ràng, khuyến khích có nút "Thử lại" gọi `refetch()` | `{isError && <Text>Lỗi mạng...</Text>}` |
| `data` (khác `undefined`) | Request thành công, dù là lần đầu hay lấy từ Cache | Danh sách/nội dung thật (`FlashList`, `ScrollView`...) | `{products && <FlashList data={products} .../>}` |
| `isRefetching` | Đang gọi lại API NGẦM nhưng **đã có** `data` cũ để hiển thị | KHÔNG che màn hình bằng Spinner to — chỉ hiện icon xoay nhỏ ở đầu danh sách (Pull-to-refresh) | `<FlashList refreshing={isRefetching} onRefresh={refetch} .../>` |

> [!CAUTION]
> **Bẫy thường gặp:** Nhầm lẫn `isLoading` với `isFetching`. `isLoading` CHỈ `true` ở lần tải ĐẦU TIÊN (chưa có Cache). Còn `isFetching` sẽ `true` ở MỌI lần gọi lại API (kể cả background refetch âm thầm) — nếu bạn dùng `isFetching` để hiện Spinner to, người dùng sẽ thấy màn hình bị "giật" che mất danh sách cũ mỗi khi Query tự làm mới ngầm, trải nghiệm rất tệ. Luôn dùng đúng cặp `isLoading` (lần đầu) + `isRefetching` (kéo tay làm mới) như bảng trên.

### 4. `useMutation` — GHI dữ liệu lên Server (POST/PUT/DELETE)

`useQuery` (và `useInfiniteQuery` ở Phần 6.8) chỉ dùng để **ĐỌC** dữ liệu (GET) — tự động chạy ngay khi Component mount. Nhưng khi cần **GHI** dữ liệu (đặt hàng, thêm Wishlist, đổi mật khẩu...), ta cần một hành động do người dùng **chủ động bấm nút mới chạy**, chứ không tự chạy khi vào màn hình. Đó chính xác là việc của `useMutation`.

**Khác biệt cốt lõi so với `useQuery`:**

| Tiêu chí | `useQuery` (Đọc) | `useMutation` (Ghi) |
|---|---|---|
| Khi nào chạy? | Tự động chạy ngay khi Component mount (và khi `queryKey` đổi) | CHỈ chạy khi bạn tự gọi hàm `mutate(...)` (VD: bấm nút "Đặt hàng") |
| Có Cache theo `queryKey` không? | Có — đây là lý do tồn tại của `useQuery` | Không — mỗi lần `mutate()` là một lần gọi mới, không cache kết quả |
| Cờ trạng thái loading | `isLoading` (lần đầu) / `isFetching` (mọi lần) | `isPending` (đang gửi request) |
| Cờ trạng thái lỗi | `isError` + `error` | `isError` + `error` (giống hệt tên, khác Hook) |
| Xử lý hậu-quả (dọn dẹp State khác, điều hướng...) | Ít dùng | `onSuccess` / `onError` / `onSettled` — nơi lý tưởng để `invalidateQueries`, `clearCart`, điều hướng... |

**Ví dụ mini: Thêm sản phẩm vào Wishlist (yêu thích) bằng `useMutation`:**

```tsx
import { useMutation, useQueryClient } from '@tanstack/react-query';
import axiosClient from '@api/axiosClient';

// Hàm gọi API GHI dữ liệu — luôn trả về 1 Promise, giống queryFn nhưng nhận thêm biến (payload)
const addToWishlist = async (productId: string) => {
  const res = await axiosClient.post('/wishlist', { productId });
  return res.data;
};

const WishlistButton = ({ productId }: { productId: string }) => {
  const queryClient = useQueryClient();

  const { mutate, isPending, isError } = useMutation({
    mutationFn: addToWishlist, // Hàm thực thi khi mutate() được gọi

    // onSuccess: chạy SAU KHI Server xác nhận thành công
    onSuccess: () => {
      // Báo cho React Query biết Cache 'wishlist' đã "Thiu" (Stale) — lần vào lại
      // màn hình Wishlist sẽ tự động fetch lại dữ liệu mới nhất, KHÔNG cần setState thủ công
      queryClient.invalidateQueries({ queryKey: ['wishlist'] });
    },

    // onError: chạy khi Server trả lỗi hoặc mất mạng — nơi hiện Toast/Alert báo người dùng
    onError: (error) => {
      console.error('❌ Thêm Wishlist thất bại:', error);
    },
  });

  return (
    <ShopButton
      title={isPending ? 'Đang thêm...' : 'Thêm vào yêu thích ❤️'}
      onPress={() => mutate(productId)} // Chỉ khi bấm nút, request mới thật sự chạy
      disabled={isPending}
    />
  );
};
```

**Bảng giải thích các trường trả về từ `useMutation`:**

| Trường | Giải thích cho người mới |
|---|---|
| `mutationFn` | Hàm bất đồng bộ (Promise) thực hiện việc GHI dữ liệu — nhận đúng 1 tham số là dữ liệu truyền vào `mutate(...)` |
| `mutate(payload)` | Hàm bạn gọi trong `onPress` để **kích hoạt** request — KHÔNG tự chạy như `useQuery` |
| `isPending` | `true` trong lúc request đang bay đi chờ Server phản hồi — dùng để disable nút, tránh bấm 2 lần |
| `isError` / `error` | `true`/có giá trị khi Server trả lỗi hoặc mất mạng — hiện thông báo lỗi rõ ràng |
| `onSuccess(data)` | Chạy khi request thành công — nơi lý tưởng để `invalidateQueries` (làm mới Cache liên quan) hoặc điều hướng |
| `onError(error)` | Chạy khi request thất bại — nơi lý tưởng để hiện Toast/Alert lỗi |
| `queryClient.invalidateQueries({ queryKey: [...] })` | "Đánh dấu Thiu" một hoặc nhiều Cache theo `queryKey` — Query nào đang được màn hình khác hiển thị sẽ tự động fetch lại ngầm ngay lập tức |

> [!TIP]
> Nguyên tắc ghi nhớ: **`useQuery` để ĐỌC (tự động), `useMutation` để GHI (chủ động bấm nút)**. Sau khi GHI thành công, luôn dùng `invalidateQueries` trong `onSuccess` để đồng bộ lại mọi Cache liên quan — đây là cách "chuẩn Enterprise" thay vì tự tay gọi `refetch()` từng nơi. Ta sẽ áp dụng đúng mẫu này để `CheckoutScreen` gọi API đặt hàng ở Sprint 6 (Bước 9.5).

---

## 🌐 PHẦN 6.6: AXIOS CHUYÊN NGHIỆP — INSTANCE VÀ INTERCEPTOR

Ở các chương trước, ta mới dùng `fetch`/`axios` một cách "chay" — gọi trực tiếp URL đầy đủ mỗi lần, tự tay gắn Header thủ công. Trong dự án Enterprise thật, không ai làm vậy. Ta cần một **Axios Instance** dùng chung cho cả App, và một **Interceptor** (Bộ chặn) tự động can thiệp vào MỌI Request/Response.

### 1. Tại sao cần `axios.create()` thay vì gọi `axios.get()` trực tiếp?

Gọi `axios.get('https://api.shopai.com/products')` lặp lại URL gốc ở khắp mọi file là một thảm họa bảo trì — nếu đổi domain Server, bạn phải sửa hàng chục file. Giải pháp: tạo **một Instance duy nhất** chứa sẵn `baseURL`, `timeout`, Header mặc định.

Tạo file `src/api/axiosClient.ts`:

```ts
import axios from 'axios';

const axiosClient = axios.create({
  baseURL: 'https://api.shopai.com', // Domain gốc — chỉ sửa 1 nơi duy nhất
  timeout: 10000, // Quá 10 giây không phản hồi -> tự động báo lỗi Timeout
  headers: {
    'Content-Type': 'application/json',
  },
});

export default axiosClient;
```

### 2. Interceptor — Tự động gắn Token vào MỌI Request

**Interceptor** (Bộ chặn) là một hàm được Axios tự động gọi TRƯỚC khi Request rời khỏi máy (Request Interceptor) hoặc NGAY KHI Response về đến máy (Response Interceptor). Đây là nơi hoàn hảo để tự động đính `Authorization: Bearer <token>` vào mọi lời gọi API, thay vì phải tự tay gắn Header ở từng màn hình.

```ts
// src/api/axiosClient.ts (tiếp)
import axios from 'axios';
import { useAuthStore } from '@store/useAuthStore';

const axiosClient = axios.create({
  baseURL: 'https://api.shopai.com',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
});

// REQUEST INTERCEPTOR: Chạy TRƯỚC mỗi Request — tự động lấy Token từ Zustand và gắn vào Header
axiosClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token; // Lấy State ngay lập tức, không cần Hook/Component
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// RESPONSE INTERCEPTOR: Chạy KHI Response về — bắt lỗi 401 (Token hết hạn) tập trung một chỗ
axiosClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.warn('⚠️ Token hết hạn hoặc không hợp lệ — tự động đăng xuất!');
      useAuthStore.getState().logout(); // Bắn logout ngay, không cần chờ UI xử lý
    }
    return Promise.reject(error);
  }
);

export default axiosClient;
```

> [!TIP]
> `useAuthStore.getState()` là cách gọi Zustand Store **bên ngoài** một Component React (ở đây là bên trong Interceptor) — không dùng được Hook `useAuthStore()` thông thường ở những nơi không phải Component/Custom Hook. Đây là một trong những lý do Zustand rất linh hoạt so với Context API (Context KHÔNG thể đọc được giá trị bên ngoài cây Component).

Từ giờ, mọi lời gọi API trong ShopAI chỉ cần:

```ts
import axiosClient from '@api/axiosClient';

// Không cần viết lại baseURL, không cần tự gắn Token — Interceptor đã lo hết!
const getProducts = () => axiosClient.get('/products');
```

---

## 🛡️ PHẦN 6.7: ZOD - TẤM KHIÊN TYPE-SAFETY

Khi gọi API, Server Backend (có thể do ông A viết code lỗi) trả về một Object bị mất trường `price`. App Mobile của bạn gọi `item.price.toString()` -> BÙM! Văng App (Crash). Đừng bao giờ tin tưởng tuyệt đối Backend.

**Zod** là một thư viện Schema Validation. Ngay khi dữ liệu từ API chạy về điện thoại, nó phải đi qua trạm kiểm soát của Zod.
Nếu Zod phát hiện kiểu dữ liệu sai (Thiếu trường, String bị biến thành Null), Zod sẽ báo lỗi lập tức trước khi luồng dữ liệu đó đi vào giao diện React của bạn. Giúp App không bao giờ bị văng. (Chúng ta sẽ **thực chiến ngay tính năng này ở Sprint 6** phía dưới — không cần chờ đến dự án Production nữa!).

---

## 📄 PHẦN 6.8: PAGINATION — PHÂN TRANG DỮ LIỆU LỚN

Server thật của ShopAI (NestJS ở Chương 9) có thể có 10.000 sản phẩm. Gọi API tải hết 10.000 sản phẩm một lượt rồi `map` ra `FlatList` sẽ làm App treo cứng, tốn băng thông 4G khủng khiếp. **Pagination** (phân trang) là kỹ thuật chỉ tải một phần nhỏ dữ liệu mỗi lần, tải thêm khi người dùng cuộn tới gần cuối danh sách.

### 1. Cách 1: `FlatList.onEndReached` + State quản lý `page` thủ công

Đây là cách kinh điển, không cần thư viện gì thêm ngoài React State:

```tsx
const HomeScreenPaginated = () => {
  const [products, setProducts] = useState<Product[]>([]);
  const [page, setPage] = useState(1);
  const [isFetchingMore, setIsFetchingMore] = useState(false);

  const loadPage = async (pageNumber: number) => {
    setIsFetchingMore(true);
    const res = await axiosClient.get(`/products?page=${pageNumber}&limit=10`);
    setProducts((prev) => [...prev, ...res.data.items]); // Nối thêm vào danh sách cũ, không thay thế
    setIsFetchingMore(false);
  };

  useEffect(() => {
    loadPage(1);
  }, []);

  const handleLoadMore = () => {
    if (isFetchingMore) return; // Chống gọi API trùng lặp khi cuộn quá nhanh
    const nextPage = page + 1;
    setPage(nextPage);
    loadPage(nextPage);
  };

  return (
    <FlatList
      data={products}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => <ProductCard product={item} />}
      onEndReached={handleLoadMore} // Tự động gọi khi cuộn gần tới cuối danh sách
      onEndReachedThreshold={0.5} // Kích hoạt khi còn cách đáy 50% chiều cao màn hình
      ListFooterComponent={isFetchingMore ? <ActivityIndicator /> : null}
    />
  );
};
```

### 2. Cách 2: `useInfiniteQuery` của React Query — "Vô hạn" và có Cache sẵn

Kết hợp Pagination với sức mạnh Cache đã học ở Phần 6.5, TanStack Query có hẳn một Hook chuyên dụng tên `useInfiniteQuery`, tự động quản lý `page`, tự động gộp dữ liệu các trang, và vẫn giữ nguyên toàn bộ lợi ích Cache/StaleTime:

```tsx
import { useInfiniteQuery } from '@tanstack/react-query';

const fetchProductsPage = async ({ pageParam = 1 }): Promise<{ items: Product[]; nextPage: number | null }> => {
  const res = await axiosClient.get(`/products?page=${pageParam}&limit=10`);
  return res.data; // Server trả về { items: [...], nextPage: 2 } hoặc nextPage: null nếu hết trang
};

const HomeScreenInfinite = () => {
  const {
    data,
    fetchNextPage,   // Gọi hàm này để tải thêm trang kế tiếp
    hasNextPage,     // Còn trang để tải hay không
    isFetchingNextPage,
  } = useInfiniteQuery({
    queryKey: ['productsInfinite'],
    queryFn: fetchProductsPage,
    initialPageParam: 1,
    getNextPageParam: (lastPage) => lastPage.nextPage, // Lấy số trang kế tiếp từ Response
  });

  // data.pages là một mảng CÁC TRANG — cần "làm phẳng" (flatten) lại thành 1 mảng sản phẩm
  const allProducts = data?.pages.flatMap((page) => page.items) ?? [];

  return (
    <FlatList
      data={allProducts}
      keyExtractor={(item) => item.id}
      renderItem={({ item }) => <ProductCard product={item} />}
      onEndReached={() => {
        if (hasNextPage) fetchNextPage(); // Chỉ tải thêm khi Server còn dữ liệu
      }}
      onEndReachedThreshold={0.5}
      ListFooterComponent={isFetchingNextPage ? <ActivityIndicator /> : null}
    />
  );
};
```

> [!TIP]
> Với dự án ShopAI thật (có Backend NestJS ở Chương 9), **`useInfiniteQuery` là lựa chọn được khuyến nghị** vì tận dụng lại toàn bộ hạ tầng Cache đã học, thay vì tự quản lý `page` bằng `useState` như Cách 1 (Cách 1 vẫn quan trọng để hiểu bản chất `onEndReached` hoạt động ra sao).

---

## 💾 PHẦN 6.9: PERSIST GIỎ HÀNG — ZUSTAND `persist` MIDDLEWARE & MMKV

### 1. Vấn đề: Giỏ hàng "mất trí nhớ" mỗi khi tắt App
`useCartStore` ở Phần 6.3 sống hoàn toàn trong RAM. Người dùng thêm 5 sản phẩm vào giỏ, tắt hẳn App (Swipe kill) rồi mở lại → Giỏ hàng **trống trơn**, vì Zustand mặc định không tự lưu State xuống ổ cứng. Đây là lỗi trải nghiệm nghiêm trọng ở app thương mại điện tử thật.

**Giải pháp:** Zustand có sẵn `persist` — một Middleware "bọc" quanh Store, tự động lưu State xuống bộ nhớ máy sau mỗi lần `set()`, và tự động đọc lại khi App khởi động.

> [!CAUTION]
> **Chỉ Persist Giỏ hàng, TUYỆT ĐỐI KHÔNG Persist Token đăng nhập theo cách này!** `AsyncStorage` (cách đơn giản nhất bên dưới) lưu dữ liệu dưới dạng Clear-text (chữ thường, không mã hóa) — hợp với Giỏ hàng (dữ liệu không nhạy cảm), nhưng **cực kỳ nguy hiểm** cho Access Token (Chương 8 sẽ giải thích rõ tại sao và chuyển Token sang `SecureStore` mã hóa phần cứng). Từ giờ đến Chương 8, `useAuthStore` **giữ nguyên không persist** — mỗi lần tắt App vẫn phải đăng nhập lại, đúng chủ đích sư phạm để Chương 8 có vấn đề thật để giải quyết.

### 2. Cách đơn giản: `persist` + `@react-native-async-storage/async-storage`
Đây là lựa chọn được khuyến nghị cho Sprint 6 vì **đơn giản hơn MMKV** — không phải vì nó "không có code Native".

> [!CAUTION]
> **Đính chính quan trọng:** `AsyncStorage` **VẪN có code Native** (khác hẳn Zustand/Context API — những thứ thuần JavaScript, không cần build lại App bao giờ). Nó chỉ *đơn giản hơn* `react-native-mmkv` vì bên dưới gọi thẳng API lưu trữ Key-Value có sẵn của hệ điều hành (`UserDefaults` trên iOS, `SharedPreferences` trên Android) thay vì tự viết tầng C++ tùy biến như MMKV — **KHÔNG phải là "không cần cài Native gì cả"**. Vì vậy, sau khi `npm install`, macOS **BẮT BUỘC phải chạy `pod install`** rồi build lại App, giống mọi thư viện Native khác đã học từ Chương 4/5 — bỏ qua bước này App sẽ báo lỗi kiểu `TurboModuleRegistry.getEnforcing(...): 'RNCAsyncStorage' could not be found` khi gọi tới `AsyncStorage`.

```bash
npm install @react-native-async-storage/async-storage

# Bắt buộc trên macOS — AsyncStorage có code Native, phải link Pod như mọi thư viện Native khác
cd ios && pod install && cd ..
```

Sau khi `pod install` xong, đây là thay đổi Native nên **Hot Reload không áp dụng** — build lại App hoàn toàn:
```bash
npm run ios
npm run android
```

```ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';

// Bọc thêm persist(...) quanh hàm khởi tạo Store cũ — logic bên trong KHÔNG đổi gì cả
export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      // ...y nguyên toàn bộ items/addItem/removeItem/totalQuantity/totalPrice/clearCart
    }),
    {
      name: 'shopai-cart-storage', // Tên "chìa khóa" lưu trong AsyncStorage
      storage: createJSONStorage(() => AsyncStorage),
      partialize: (state) => ({ items: state.items }), // Chỉ lưu `items` — không lưu các hàm addItem/removeItem
    }
  )
);
```

Chỉ cần thêm đúng 1 lớp `persist(...)` bọc ngoài — mọi Component đang gọi `useCartStore()` ở nơi khác **không cần sửa gì**, vì API dùng (`addItem`, `removeItem`, `totalPrice()`...) giữ nguyên y hệt.

### 3. Lựa chọn Production nhanh hơn: MMKV (`react-native-mmkv`)
`AsyncStorage` hoạt động bất đồng bộ (Async) và dùng cơ chế lưu trữ Key-Value khá cũ của nền tảng gốc, tốc độ đọc/ghi chậm hơn đáng kể so với chuẩn hiện đại. **MMKV** (do đội ngũ WeChat phát triển, được `react-native-mmkv` đóng gói lại cho React Native) đọc/ghi **đồng bộ (Sync)** và nhanh hơn AsyncStorage tới hàng chục lần nhờ dùng bộ nhớ ánh xạ (memory-mapped file) viết bằng C++.

```ts
// Cần cài đặt Native (pod install lại) — react-native-mmkv có code C++, khác AsyncStorage
// npm install react-native-mmkv
import { MMKV } from 'react-native-mmkv';

const cartMMKV = new MMKV();

// Chỉ cần đổi đúng 1 chỗ trong config persist — logic Store không đổi gì thêm:
storage: createJSONStorage(() => ({
  getItem: (name) => cartMMKV.getString(name) ?? null,
  setItem: (name, value) => cartMMKV.set(name, value),
  removeItem: (name) => cartMMKV.delete(name),
})),
```

> [!TIP]
> **Nguyên tắc chọn công cụ:** Sprint 6 dùng `AsyncStorage` vì **dễ cấu hình hơn MMKV** (vẫn phải `pod install` như mục 2 ở trên). Khi triển khai Production, đổi sang MMKV chỉ tốn đúng đoạn `storage` — toàn bộ `cartSlice`/`useCartStore` không cần viết lại. Tách `storage` ra khỏi logic Store ngay từ đầu là quyết định kiến trúc đúng.

---

## 🛒 PHẦN 6.10: TÍNH NĂNG THƯƠNG MẠI NÂNG CAO (WISHLIST, REVIEW & VOUCHER)

Trong một ứng dụng thương mại điện tử cấp độ Enterprise, ngoài luồng mua hàng cơ bản (Giỏ hàng -> Thanh toán), chúng ta cần các tính năng giữ chân người dùng (Retention) và kích cầu (Promotion). 

### 1. Wishlist (Danh sách yêu thích) với Zustand
Wishlist hoạt động tương tự như Giỏ hàng nhưng không có số lượng (`quantity`). Nó lưu danh sách các `productId` mà người dùng đã bấm "thả tim".
- **Tại sao dùng Zustand?** Wishlist cần được truy cập ở `ProductCard` (để hiện tim đỏ/trắng), ở màn hình `ProductDetail`, và ở tab `WishlistScreen`. Do đó, nó là một Global Client State hoàn hảo.
- **Persist:** Giống như Giỏ hàng, Wishlist cần được `persist` bằng `AsyncStorage` hoặc `MMKV` để không bị mất khi thoát app. Khi kết nối Backend (Chương 9), Wishlist sẽ được đồng bộ lên Server mỗi lần app mở lên.

### 2. Review & Rating (Đánh giá sản phẩm)
Đánh giá sản phẩm là dạng **Server State** nặng.
- Dữ liệu Review thay đổi liên tục bởi nhiều người dùng khác nhau.
- **Giải pháp:** Sử dụng `useQuery` (React Query) để fetch danh sách Review. Dùng `useInfiniteQuery` nếu số lượng Review lớn (phân trang).
- Khi người dùng viết Review mới, dùng `useMutation` để gửi dữ liệu (`rating`, `comment`, `images`) lên Server. Nhớ gọi `queryClient.invalidateQueries({ queryKey: ['reviews', productId] })` để làm mới danh sách sau khi đánh giá thành công.

### 3. Voucher & Khuyến mãi trong Giỏ hàng
Voucher là một State kết hợp: 
- Mã code/id của Voucher được lưu trong **Client State** (Zustand Cart Store).
- Số tiền giảm giá thực tế (Discount Amount) phải được tính toán từ **Server** thông qua một API `/api/cart/calculate` (dùng React Query `useMutation` để gửi mảng `items` và `voucherCode` lên server, lấy về tổng tiền cuối cùng).

> [!WARNING]
> **Quy tắc bảo mật tối thượng:** Tuyệt đối không tự tính toán số tiền giảm giá (Discount) hay tổng tiền cuối cùng (Final Total) bằng công thức trên Frontend (Client). Kẻ gian có thể dịch ngược app và sửa code để giảm giá 100%. Frontend chỉ hiển thị con số do Backend (Server) trả về.

---

## 🚀 THỰC CHIẾN SHOPAI (SPRINT 6: MẠNG LƯỚI DATA VỚI ZUSTAND, QUERY & ZOD)

**User Story:** *"Là người dùng, tôi muốn bấm Đăng nhập ở bất kỳ đâu và dữ liệu Token được đồng bộ toàn app. Danh sách sản phẩm phải được load nhanh, lưu cache để không tốn lưu lượng 4G khi tôi ra vào màn hình nhiều lần. Khi tôi bấm 'Mua ngay' ở bất kỳ sản phẩm nào, nó phải bay thẳng vào Giỏ hàng của tôi, và tôi muốn chắc chắn Server không bao giờ gửi về dữ liệu rác làm App tôi bị Crash."*


### 📋 Khung thực hành chương (đọc trước khi gõ code)

> Đây là **bài thực hành của Chương 6** (không phải “lab mỗi ngày”). Làm hết Sprint này = đạt mục tiêu chương. Hoàn thành đủ 11 Sprint = sản phẩm ShopAI theo `SHOPAI_HOAN_THIEN.md`.

| Hạng mục | Nội dung |
|----------|----------|
| **Thời lượng gợi ý** | 6–8 tiết (một chương — xếp nhiều buổi trong tuần nếu cần) |
| **Độ khó chương** | ★★★★★ |
| **Đầu vào bắt buộc** | Sprint 5 PASS — Tab/Auth/Detail ổn. |
| **Đầu ra sản phẩm** | Zustand Auth+Cart+Orders(persist); Home InfiniteQuery+Zod; Checkout useMutation; Lịch sử đơn + Chi tiết HĐ + Pay PENDING→PAID (local); axiosClient; RTK bài tập đề cương. |
| **Cách làm** | Làm **tuần tự từng Bước**. Gặp mốc ✓ bên dưới mà FAIL → dừng, sửa, rồi mới sang bước sau. |
| **Nghiệm thu cuối khóa** | Đối chiếu `SHOPAI_HOAN_THIEN.md` — mỗi Sprint chỉ tích thêm ô, không phá tính năng cũ. |

### ✓ Kiểm chứng theo mốc (trong lúc làm)

- **Sau Bước 1–5:** Alias `@api` + axiosClient; Auth/Cart store; App không Prop Drilling token.
- **Sau Bước 7–8:** Mua ngay vào giỏ; Home phân trang + Zod; 2 loại lỗi rõ.
- **Sau Bước 9–9.6:** Cart đủ UI; Checkout Modal + mutation; Lịch sử đơn + Chi tiết HĐ + Pay `PENDING`→`PAID`; tắt app giỏ/đơn vẫn còn.
- **Sau Bước 10:** Nộp được module Redux `src/store/redux/`.

> [!TIP]
> Xong Sprint 6, mở `SHOPAI_HOAN_THIEN.md` và tick các ô thuộc chương này. Mục tiêu cuối khóa: **mọi ô A/B/C/D (+ E đề cương) đều xanh** trong `SHOPAI_HOAN_THIEN.md` — đó mới là ShopAI hoàn thiện đẳng cấp.

### Yêu cầu Nghiệm thu:
1. Đưa `userToken` từ state cục bộ ở `App.tsx` (Chương 5) lên Zustand Store.
2. Cài đặt TanStack Query và kết nối nó vào luồng của App.
3. Chỉnh sửa HomeScreen để Load dữ liệu giả lập từ mạng Internet (thay vì Import cứng) bằng **`useInfiniteQuery` có Pagination thật** (không phải chỉ lý thuyết) — cuộn tới cuối danh sách tự động `fetchNextPage()`, có `ListFooterComponent` báo đang tải thêm, đồng thời có Pull-to-refresh gọi `refetch()` (thay cho `setTimeout` giả lập ở Chương 4).
4. Tạo `useCartStore` (Zustand) quản lý **Client State** của Giỏ hàng: `items`, `addItem`, `removeItem`, `totalQuantity`, `totalPrice` — có **`persist`** bằng `AsyncStorage` (xem Phần 6.9), sống sót qua mỗi lần tắt/mở lại App.
5. Nút "Mua ngay" ở `ProductCard` phải bắn sản phẩm thẳng lên Đám mây Giỏ hàng, không cần Route Params lằng nhằng.
6. Nâng cấp `CartScreen` (bản nháp trống từ Chương 5) để hiển thị danh sách hàng thật lấy từ Store, kèm trạng thái Giỏ hàng trống (Empty State).
7. Toàn bộ dữ liệu sản phẩm từ API phải đi qua trạm kiểm soát **Zod** trước khi được phép hiển thị lên giao diện.
8. **`CheckoutScreen`** hoạt động qua `RootStackNavigator` (Modal) — bấm "Thanh toán" ở `CartScreen` → Xác nhận đơn hàng bằng **`useMutation`** (có `isPending`/`isError`/`onSuccess`) → ghi đơn **`PENDING`** vào `useOrderStore` → xóa Giỏ → có thể mở Lịch sử đơn.
9. **Lịch sử đơn / hóa đơn:** Tab **Đơn hàng** (`OrdersScreen`) + `OrderDetailScreen` (chi tiết hóa đơn); nút **Thanh toán giả lập** đổi `PENDING` → `PAID`. *(Ch.9: `GET /api/orders`, `GET /api/orders/:id`, `POST /api/orders/:id/pay`.)*
10. **[Bắt buộc đề cương]** Hoàn thành module học tập `src/store/redux/` với Redux Toolkit (`cartSlice` hoặc `counterSlice` + `store.ts`), có `Provider` bọc App và ít nhất 1 màn hình demo dùng `useSelector`/`useDispatch` — song song với Zustand, KHÔNG thay thế Cart Production.
11. Giữ **`RegisterScreen`** (Ch.5) trong AuthStack; `LoginScreen`/`RegisterScreen` dùng Zustand `login()` (mock token tới Ch.9).

### Hướng dẫn thực thi Step-by-Step:

#### Bước 1: Cài đặt thư viện hạng nặng
```bash
npm install zustand @tanstack/react-query zod axios @reduxjs/toolkit react-redux @react-native-async-storage/async-storage
```
> `@react-native-async-storage/async-storage` dùng để Persist Giỏ hàng ở Bước 3 (xem lý thuyết Phần 6.9). **Lưu ý:** thư viện này VẪN có code Native (khác Zustand/Context API thuần JS) — xem cảnh báo `pod install` đầy đủ ở Phần 6.9 mục 2.

#### Bước 1.5: Mở rộng Path Alias cho tầng API — Tạo `axiosClient`

Trước khi đụng tới `axiosClient` (sẽ dùng lại ở Bước 8, và bắt buộc dùng thật ở Bước 9.5 `CheckoutScreen`), phải **mở rộng Path Alias đã cấu hình từ Chương 2** để thêm `@api` — bỏ qua bước này, mọi `import axiosClient from '@api/axiosClient'` phía dưới sẽ báo lỗi đỏ `Unable to resolve module '@api/axiosClient'`.

**1. Tạo thư mục `src/api`:**
```bash
mkdir -p src/api
```

**2. Mở `babel.config.js`, thêm đúng 1 dòng `'@api': './src/api'` vào khối `alias` đã có từ Chương 2 — GIỮ NGUYÊN toàn bộ các dòng alias cũ:**
```javascript
module.exports = {
  presets: ['module:@react-native/babel-preset'],
  plugins: [
    [
      'module-resolver',
      {
        root: ['./src'],
        extensions: ['.ios.js', '.android.js', '.js', '.ts', '.tsx', '.json'],
        alias: {
          '@assets': './src/assets',
          '@components': './src/components',
          '@screens': './src/screens',
          '@navigation': './src/navigation',
          '@store': './src/store',
          '@services': './src/services',
          '@hooks': './src/hooks',
          '@data': './src/data',
          '@utils': './src/utils',
          '@constants': './src/constants',
          '@types': './src/types',
          '@contexts': './src/contexts',
          '@api': './src/api', // ➕ MỚI (Chương 6) — dùng cho axiosClient
        },
      },
    ],
    'react-native-reanimated/plugin', // Đã cài ở Chương 4 — LUÔN LUÔN đứng cuối cùng, không xê dịch
  ],
};
```

**3. Mở `tsconfig.json`, thêm đúng 1 dòng `"@api/*": ["src/api/*"]` vào `paths` đã có từ Chương 2:**
```json
"baseUrl": ".",
"paths": {
  "@assets/*": ["src/assets/*"],
  "@components/*": ["src/components/*"],
  "@screens/*": ["src/screens/*"],
  "@navigation/*": ["src/navigation/*"],
  "@store/*": ["src/store/*"],
  "@services/*": ["src/services/*"],
  "@hooks/*": ["src/hooks/*"],
  "@data/*": ["src/data/*"],
  "@utils/*": ["src/utils/*"],
  "@constants/*": ["src/constants/*"],
  "@types/*": ["src/types/*"],
  "@contexts/*": ["src/contexts/*"],
  "@api/*": ["src/api/*"]
}
```

> [!WARNING]
> `babel.config.js` là file cấu hình biên dịch — **Fast Refresh/Hot Reload KHÔNG áp dụng được** cho thay đổi này. Tắt hẳn Metro (`Ctrl+C`), chạy lại `npm start -- --reset-cache` rồi build lại App, đúng nguyên tắc đã học mỗi khi sửa `babel.config.js` từ Chương 2/4.

**4. Tạo file `src/api/axiosClient.ts`** (nội dung đầy đủ, đúng như lý thuyết Phần 6.6 — có sẵn cả 2 Interceptor Request/Response):
```ts
import axios from 'axios';
import { useAuthStore } from '@store/useAuthStore';

const axiosClient = axios.create({
  baseURL: 'https://api.shopai.com', // Domain gốc — chỉ sửa 1 nơi duy nhất
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' },
});

// REQUEST INTERCEPTOR: tự động lấy Token từ Zustand và gắn vào Header mọi Request
axiosClient.interceptors.request.use((config) => {
  const token = useAuthStore.getState().token;
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// RESPONSE INTERCEPTOR: bắt lỗi 401 (Token hết hạn) tập trung một chỗ
axiosClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      console.warn('⚠️ Token hết hạn hoặc không hợp lệ — tự động đăng xuất!');
      useAuthStore.getState().logout();
    }
    return Promise.reject(error);
  }
);

export default axiosClient;
```

> [!NOTE]
> File này import `useAuthStore` từ `@store/useAuthStore` — file đó sẽ được tạo ngay ở **Bước 2** kế tiếp. Đây chỉ là tham chiếu "tới trước" bình thường giữa các file trong cùng dự án (giống hệt cách `HomeScreen` ở Bước 8 tham chiếu `ProductCard` của Bước 7) — không phải lỗi, miễn là bạn tạo đủ cả 2 file trước khi chạy thử App.

#### Bước 2: Tạo Đám mây Zustand (Auth Store)
Tạo thư mục và file: `src/store/useAuthStore.ts`:
```ts
import { create } from 'zustand';

interface AuthState {
  token: string | null;
  login: (newToken: string) => void;
  logout: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  token: null, // Khởi tạo chưa đăng nhập
  login: (newToken) => {
    // Ở chương sau (Chương 8) ta sẽ lưu token này vào Ổ cứng Keystore tại đây
    set({ token: newToken });
  },
  logout: () => set({ token: null }),
}));
```

#### Bước 3: Tạo Đám mây Zustand cho Giỏ hàng (Cart Store) — có Persist (Phần 6.9)
Đây là một Đám mây (Store) hoàn toàn tách biệt với Auth — đúng triết lý **Decentralized Stores** đã học ở Phần 6.1. Tạo file `src/store/useCartStore.ts`. Chú ý lớp `persist(...)` bọc ngoài — đây chính là điểm khác biệt so với `useAuthStore` (không persist, xem cảnh báo ở Phần 6.9 mục 1):

```ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Product } from '../types/product.schema';

// Một dòng trong Giỏ hàng = Sản phẩm gốc + số lượng đang chọn
export interface CartItem extends Product {
  quantity: number;
}

interface CartState {
  items: CartItem[];
  addItem: (product: Product) => void;
  removeItem: (productId: string) => void;
  totalQuantity: () => number;
  totalPrice: () => number;
  clearCart: () => void;
}

export const useCartStore = create<CartState>()(
  persist(
    (set, get) => ({
      items: [],

      // Nếu sản phẩm đã có trong giỏ -> Chỉ tăng quantity. Chưa có -> Thêm dòng mới.
      addItem: (product) => {
        set((state) => {
          const existing = state.items.find((item) => item.id === product.id);
          if (existing) {
            return {
              items: state.items.map((item) =>
                item.id === product.id ? { ...item, quantity: item.quantity + 1 } : item
              ),
            };
          }
          return { items: [...state.items, { ...product, quantity: 1 }] };
        });
      },

      removeItem: (productId) => {
        set((state) => ({
          items: state.items.filter((item) => item.id !== productId),
        }));
      },

      // Dùng get() để tính toán "on-demand" thay vì lưu sẵn một State thừa dễ lệch dữ liệu
      totalQuantity: () => get().items.reduce((sum, item) => sum + item.quantity, 0),
      totalPrice: () => get().items.reduce((sum, item) => sum + item.price * item.quantity, 0),

      clearCart: () => set({ items: [] }),
    }),
    {
      name: 'shopai-cart-storage', // "Chìa khóa" lưu trong AsyncStorage — đổi tên này sẽ mất dữ liệu cũ
      storage: createJSONStorage(() => AsyncStorage),
      // Chỉ lưu mảng `items` xuống ổ cứng — không lưu các hàm addItem/removeItem/...
      // (Zustand persist mặc định cũng tự bỏ qua hàm khi JSON.stringify, nhưng khai báo rõ ràng hơn)
      partialize: (state) => ({ items: state.items }) as CartState,
    }
  )
);
```

> [!TIP]
> Muốn nâng cấp lên MMKV (nhanh hơn, đồng bộ) chỉ cần đổi đúng đối tượng truyền vào `storage:` theo mẫu ở Phần 6.9 mục 3 — không đụng gì đến `items`/`addItem`/`removeItem`/... bên trên.

#### Bước 4: Dựng Tấm khiên Zod cho dữ liệu Sản phẩm
Tạo file `src/types/product.schema.ts`. Đây là nơi định nghĩa "khuôn mẫu chuẩn" mà mọi dữ liệu sản phẩm từ Server BẮT BUỘC phải khớp:

```ts
import { z } from 'zod';

// Khuôn mẫu 1 sản phẩm hợp lệ
export const ProductSchema = z.object({
  id: z.string(),
  name: z.string().min(1, 'Tên sản phẩm không được để trống'),
  price: z.number().positive('Giá sản phẩm phải lớn hơn 0'),
  image: z.string().url('Đường dẫn ảnh phải là URL hợp lệ'),
});

// Khuôn mẫu cho cả một Danh sách (Mảng) sản phẩm trả về từ API
export const ProductListSchema = z.array(ProductSchema);

// Tự động suy ra Type TypeScript từ Schema Zod — Không cần viết interface 2 lần!
export type Product = z.infer<typeof ProductSchema>;
```

> [!TIP]
> Từ giờ, mọi nơi trong App cần khai báo Type `Product` (ProductCard, CartStore, HomeScreen...) đều import từ `src/types/product.schema.ts` này, thay cho `src/data/mockProducts.ts` cũ. Một nguồn Type duy nhất — tránh loạn kiểu dữ liệu.

#### Bước 5: Đập bỏ Prop Drilling ở App.tsx, cấu hình QueryClient (GIỮ Bottom Tab từ Chương 5)
Mở file `App.tsx`. **Không được phá** kiến trúc `MainTabNavigator` đã dựng ở Sprint 5. Chỉ thay Prop Drilling bằng Zustand và bọc thêm `QueryClientProvider`.

```tsx
import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { ThemeProvider } from '@contexts/ThemeContext';
import LoginScreen from '@screens/LoginScreen';
import RegisterScreen from '@screens/RegisterScreen';
import MainTabNavigator from '@navigation/MainTabNavigator';
import { useAuthStore } from '@store/useAuthStore';

const AuthStack = createNativeStackNavigator();

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // Dữ liệu còn "Tươi" trong 5 phút
      retry: 2,
    },
  },
});

function App(): React.JSX.Element {
  const token = useAuthStore(state => state.token);

  return (
    <SafeAreaProvider>
      <QueryClientProvider client={queryClient}>
        {/* ThemeProvider giữ nguyên từ Sprint 3 (Chương 3) — không đụng vào */}
        <ThemeProvider>
          <NavigationContainer>
            {token == null ? (
              // GIỮ AuthStack Login + Register từ Chương 5 — chỉ bỏ Prop onLogin (đổi sang Zustand)
              <AuthStack.Navigator screenOptions={{ headerShown: false }}>
                <AuthStack.Screen name="Login" component={LoginScreen} />
                <AuthStack.Screen name="Register" component={RegisterScreen} />
              </AuthStack.Navigator>
            ) : (
              // GIỮ Bottom Tab: Trang chủ (HomeStack) + Giỏ hàng (CartScreen)
              // Bước 9.5 phía dưới sẽ đổi thành <RootStackNavigator /> để có thêm Checkout
              <MainTabNavigator />
            )}
          </NavigationContainer>
        </ThemeProvider>
      </QueryClientProvider>
    </SafeAreaProvider>
  );
}

export default App;
```

> [!IMPORTANT]
> `MainTabNavigator` giờ **không cần** nhận `onLogout` qua Props nữa — `HomeScreen` sẽ gọi thẳng `useAuthStore().logout`. Hãy mở `src/navigation/MainTabNavigator.tsx` và `HomeStackNavigator.tsx`, **xóa prop `onLogout`**, render `<HomeStackNavigator />` đơn giản.

Cụ thể, mở `src/navigation/HomeStackNavigator.tsx` (đã tạo ở Chương 5, Bước 4) và đổi lại `Stack.Screen` của `Home`: **BẮT BUỘC dùng `component=`** (không còn dùng cú pháp Render Prop `{() => <HomeScreen onLogout={onLogout} />}` của Chương 5 nữa), để React Navigation tự động tiêm (`inject`) `navigation`/`route` chuẩn vào `HomeScreen` như mọi màn hình khác:

```tsx
import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import HomeScreen from '@screens/HomeScreen';
import ProductDetailScreen from '@screens/ProductDetailScreen';

export type HomeStackParamList = {
  Home: undefined;
  ProductDetail: { productId: string };
};

const Stack = createNativeStackNavigator<HomeStackParamList>();

// KHÔNG còn nhận Props onLogout — HomeScreen tự lấy useAuthStore().logout
const HomeStackNavigator = () => {
  return (
    <Stack.Navigator>
      {/* Dùng component= để Navigation tự tiêm navigation/route — xóa hẳn Render Prop onLogout của Chương 5 */}
      <Stack.Screen name="Home" component={HomeScreen} options={{ headerShown: false }} />
      <Stack.Screen
        name="ProductDetail"
        component={ProductDetailScreen}
        options={{ title: 'Chi tiết sản phẩm' }}
      />
    </Stack.Navigator>
  );
};

export default HomeStackNavigator;
```

Tương tự, mở `src/navigation/MainTabNavigator.tsx`, xóa Props `onLogout` và Render Prop, render thẳng `<HomeStackNavigator />`:

```tsx
import React from 'react';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import HomeStackNavigator from '@navigation/HomeStackNavigator';
import CartScreen from '@screens/CartScreen';

// Khai báo Type cho tầng Tab — cần export ra để HomeScreen dùng CompositeScreenProps
// (điều hướng "xuyên tầng" từ Home Stack sang Tab Cart cần biết cả 2 ParamList)
export type MainTabParamList = {
  HomeTab: undefined;
  Cart: undefined;
};

const Tab = createBottomTabNavigator<MainTabParamList>();

const MainTabNavigator = () => {
  return (
    <Tab.Navigator screenOptions={{ headerShown: false }}>
      <Tab.Screen name="HomeTab" component={HomeStackNavigator} options={{ title: 'Trang chủ' }} />
      <Tab.Screen name="Cart" component={CartScreen} options={{ title: 'Giỏ hàng' }} />
    </Tab.Navigator>
  );
};

export default MainTabNavigator;
```

#### Bước 6: Sửa LoginScreen + RegisterScreen gọi Zustand
Mở `src/screens/LoginScreen.tsx`. Xóa tham số Props `onLogin` / `onGoRegister` (của Chương 5), thay bằng `useAuthStore().login` + `useNavigation` để sang Register. Toàn bộ phần `email`/`password`/`errors`/`validate` và UI Kit được **GIỮ NGUYÊN**:

```tsx
import React, { useState } from 'react';
import { View, Text, StyleSheet, Pressable } from 'react-native';
import { useNavigation } from '@react-navigation/native';
import ShopButton from '@components/ShopButton';
import ShopInput from '@components/ui/ShopInput';
import { COLORS, SIZES } from '@constants/theme';
import { useAuthStore } from '@store/useAuthStore';

const LoginScreen = () => {
  const navigation = useNavigation<any>();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errors, setErrors] = useState<{ email?: string; password?: string }>({});
  const [loading, setLoading] = useState(false);

  const login = useAuthStore(state => state.login);

  const validate = () => {
    const next: { email?: string; password?: string } = {};
    if (!email.includes('@')) next.email = 'Email không hợp lệ (phải chứa @)';
    if (password.length < 6) next.password = 'Mật khẩu phải có ít nhất 6 ký tự';
    setErrors(next);
    return Object.keys(next).length === 0;
  };

  const handleLogin = () => {
    if (!validate()) return;
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      login('mock_token_123');
    }, 1200);
  };

  return (
    <View style={styles.container}>
      <Text style={styles.title}>ShopAI</Text>
      <Text style={styles.subtitle}>Vui lòng đăng nhập để tiếp tục</Text>

      <ShopInput
        label="Email"
        placeholder="you@example.com"
        value={email}
        onChangeText={setEmail}
        error={errors.email}
        autoCapitalize="none"
        keyboardType="email-address"
      />
      <ShopInput
        label="Mật khẩu"
        placeholder="Ít nhất 6 ký tự"
        value={password}
        onChangeText={setPassword}
        error={errors.password}
        secureTextEntry
      />

      <ShopButton
        title="Đăng nhập ngay"
        onPress={handleLogin}
        isLoading={loading}
        style={styles.loginBtn}
      />

      <Pressable onPress={() => navigation.navigate('Register')} style={styles.registerLink}>
        <Text style={styles.registerLinkText}>
          Chưa có tài khoản? <Text style={styles.registerLinkBold}>Đăng ký</Text>
        </Text>
      </Pressable>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
    justifyContent: 'center',
    padding: SIZES.padding,
  },
  title: {
    fontSize: 40,
    fontWeight: '900',
    color: COLORS.primary,
    textAlign: 'center',
    marginBottom: 10,
  },
  subtitle: {
    fontSize: SIZES.body1,
    color: COLORS.textLight,
    textAlign: 'center',
    marginBottom: 32,
  },
  loginBtn: { marginTop: 8 },
  registerLink: { marginTop: 20, alignItems: 'center' },
  registerLinkText: { fontSize: SIZES.body2, color: COLORS.textLight },
  registerLinkBold: { color: COLORS.primary, fontWeight: '700' },
});

export default LoginScreen;
```

Cập nhật tương tự `RegisterScreen.tsx`: bỏ Props `onRegistered`/`onGoLogin`, dùng `useAuthStore().login` + `navigation.navigate('Login')`. Logic `validate` / form **giữ nguyên** như Chương 5 Bước 2.5.

#### Bước 7: Nối dây "Mua ngay" ở ProductCard vào Giỏ hàng
Mở `src/components/ProductCard.tsx`. Đổi nguồn Type sang Zod Schema, và gọi thẳng `addItem` từ Đám mây Giỏ hàng — không cần Props, không cần Navigation:

```tsx
import React, { memo } from 'react';
import { View, Text, Image, StyleSheet, Dimensions } from 'react-native';
import { COLORS, SIZES } from '@constants/theme';
import ShopButton from './ShopButton';
import { Product } from '../types/product.schema'; // Đổi nguồn Type sang Zod Schema
import { useCartStore } from '@store/useCartStore';

const { width } = Dimensions.get('window');
const CARD_WIDTH = width / 2 - (SIZES.padding * 1.5);

interface Props {
  product: Product;
}

const ProductCard = ({ product }: Props) => {
  const addItem = useCartStore((state) => state.addItem); // Lấy hàm bắn lên Đám mây Giỏ hàng

  return (
    <View style={styles.card}>
      <Image source={{ uri: product.image }} style={styles.image} resizeMode="cover" />
      <View style={styles.infoContainer}>
        <Text style={styles.name} numberOfLines={2}>{product.name}</Text>
        <Text style={styles.price}>
          {new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(product.price)}
        </Text>

        <ShopButton
          title="Mua ngay"
          onPress={() => addItem(product)} // Bắn thẳng sản phẩm lên Giỏ hàng!
          style={styles.button}
          textStyle={{ fontSize: 12 }}
        />
      </View>
    </View>
  );
};

// ... styles và export giữ nguyên như Chương 4
export default memo(ProductCard);
```

#### Bước 8: Gọi API xịn xò với `useInfiniteQuery` (Pagination thật) + Zod tại HomeScreen
Mở `src/screens/HomeScreen.tsx`. Xóa Props `onLogout`. Dùng `useInfiniteQuery` (Phần 6.8) — KHÔNG dùng `useQuery` chay — để tải sản phẩm theo từng trang nhỏ, cho từng trang dữ liệu thô đi qua trạm kiểm soát Zod trước khi trả về cho UI, đồng thời phân biệt rõ 2 loại lỗi (Zod vs Mạng). Đồng thời thêm nút mở Giỏ hàng có đếm số lượng, khôi phục `Pressable` điều hướng sang `ProductDetail` (đã có ở Chương 5, đừng để mất khi thêm React Query), và định kiểu `navigation` đúng bằng `HomeStackParamList` (không dùng `any`):

```tsx
import React from 'react';
import { View, Text, StyleSheet, Pressable, ActivityIndicator } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context'; // BẮT BUỘC lấy từ safe-area-context, KHÔNG lấy từ 'react-native'
import { useInfiniteQuery } from '@tanstack/react-query'; // Import vũ khí hạng nặng — có Pagination sẵn (Phần 6.8)
// Danh sách vẫn nên dùng FlashList như Chương 4/5 (hiệu năng tốt hơn FlatList khi danh sách dài);
// nếu dự án của bạn chưa cài @shopify/flash-list, có thể tạm giữ FlatList tương đương.
import { FlashList } from '@shopify/flash-list';
import type { NativeStackScreenProps } from '@react-navigation/native-stack';
import type { CompositeScreenProps } from '@react-navigation/native';
import type { BottomTabScreenProps } from '@react-navigation/bottom-tabs';
import ProductCard from '@components/ProductCard';
import ShopButton from '@components/ShopButton';
import { COLORS, SIZES } from '@constants/theme';
import { useAuthStore } from '@store/useAuthStore';
import { useCartStore } from '@store/useCartStore';
import { Product, ProductListSchema } from '../types/product.schema';
import type { HomeStackParamList } from '@navigation/HomeStackNavigator';
import type { MainTabParamList } from '@navigation/MainTabNavigator';

// Vì Bước 5 đã đổi Stack.Screen("Home") sang dùng component=, HomeScreen giờ nhận
// thẳng navigation/route qua Props chuẩn của React Navigation. Dùng CompositeScreenProps
// (thay vì "any") vì HomeScreen cần navigate() cả trong Home Stack (ProductDetail) VÀ
// nhảy sang Tab cha (Cart) — TypeScript sẽ bắt lỗi ngay nếu gọi sai tên/sai tham số ở 1 trong 2 tầng
type Props = CompositeScreenProps<
  NativeStackScreenProps<HomeStackParamList, 'Home'>,
  BottomTabScreenProps<MainTabParamList>
>;

const PAGE_SIZE = 10;
const TOTAL_MOCK_PRODUCTS = 47; // Giả lập Server có 47 sản phẩm — đủ nhiều trang để thấy rõ Pagination

// Khuôn 1 "trang" dữ liệu trả về từ Server — đúng format REST phân trang thật (Chương 9 sẽ dùng lại y hệt)
interface ProductPage {
  items: Product[];
  nextPage: number | null;
}

// 2 lớp lỗi riêng biệt để UI phân biệt rạch ròi "lỗi mạng" và "lỗi dữ liệu bẩn (Zod)"
class ZodValidationError extends Error {}
class NetworkError extends Error {}

// Hàm giả lập gọi API PHÂN TRANG — mỗi lần chỉ trả về đúng PAGE_SIZE sản phẩm, không tải hết 1 lượt
const fetchProductsPage = async ({ pageParam }: { pageParam: number }): Promise<ProductPage> => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      // Giả lập ngẫu nhiên ~10% khả năng mất mạng — để thấy rõ nhánh lỗi Mạng khác nhánh lỗi Zod
      if (Math.random() < 0.1) {
        reject(new NetworkError('Mất kết nối mạng, vui lòng thử lại!'));
        return;
      }

      const start = (pageParam - 1) * PAGE_SIZE;
      const rawItems = Array.from({ length: PAGE_SIZE })
        .map((_, i) => {
          const index = start + i;
          if (index >= TOTAL_MOCK_PRODUCTS) return null; // Hết dữ liệu giả lập
          return {
            id: `api_prod_${index}`,
            name: `Sản phẩm từ Cloud ${index}`,
            price: 500000 + index * 5000,
            image: `https://picsum.photos/id/${100 + index}/400/400`,
          };
        })
        .filter((item) => item !== null);

      // TRẠM KIỂM SOÁT ZOD: Kiểm tra riêng TỪNG TRANG trước khi cho phép đi tiếp
      const result = ProductListSchema.safeParse(rawItems);
      if (!result.success) {
        console.error('❌ Zod chặn dữ liệu bẩn từ API:', result.error.format());
        reject(new ZodValidationError('Dữ liệu sản phẩm không hợp lệ (Zod validation failed)!'));
        return;
      }

      const hasMore = start + PAGE_SIZE < TOTAL_MOCK_PRODUCTS;
      resolve({ items: result.data, nextPage: hasMore ? pageParam + 1 : null });
    }, 1200);
  });
};

const HomeScreen = ({ navigation }: Props) => {
  const logout = useAuthStore(state => state.logout); // Gọi Hàm thoát từ Đám mây
  const totalQuantity = useCartStore(state => state.totalQuantity()); // Số lượng hàng trong giỏ

  // BÙM! useInfiniteQuery = toàn bộ sức mạnh Cache/StaleTime (Phần 6.5) CỘNG THÊM Pagination tự động (Phần 6.8)
  const {
    data,
    isLoading,
    isError,
    error,
    refetch,
    isRefetching,
    fetchNextPage,     // Gọi hàm này để tải thêm trang kế tiếp
    hasNextPage,       // Server còn trang để tải hay không
    isFetchingNextPage, // Đang tải trang kế tiếp (khác isLoading — đã có data cũ hiển thị)
  } = useInfiniteQuery({
    queryKey: ['productsInfinite'], // Mã định danh Cache — đổi tên so với 'productsList' vì cấu trúc data đã khác (nhiều trang)
    queryFn: fetchProductsPage,
    initialPageParam: 1,
    getNextPageParam: (lastPage) => lastPage.nextPage,
  });

  // data.pages là mảng CÁC TRANG — "làm phẳng" (flatten) lại thành 1 mảng sản phẩm duy nhất cho FlashList
  const allProducts = data?.pages.flatMap((page) => page.items) ?? [];

  // Phân biệt rõ 2 thông báo lỗi khác nhau bằng instanceof — đúng yêu cầu UX (không gộp chung 1 câu mơ hồ)
  const errorMessage =
    error instanceof ZodValidationError
      ? '⚠️ Dữ liệu sản phẩm không hợp lệ (lỗi kiểm tra Zod) — báo kỹ thuật viên!'
      : '📡 Lỗi mạng — vui lòng kiểm tra kết nối và kéo xuống thử lại!';

  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.container}>
        <View style={styles.header}>
          <Text style={styles.headerTitle}>Khám phá</Text>
          <View style={{ flexDirection: 'row', gap: 10 }}>
            <ShopButton
              title={`Giỏ hàng (${totalQuantity})`}
              onPress={() => navigation.navigate('Cart')}
              style={{ width: 120, height: 32, backgroundColor: COLORS.secondary }}
              textStyle={{ fontSize: 12 }}
            />
            <ShopButton title="Thoát" onPress={logout} style={{ width: 80, height: 32 }} />
          </View>
        </View>

        {/* Xử lý UI 3 trạng thái cực thanh lịch */}
        {isLoading && <ActivityIndicator size="large" color={COLORS.primary} style={{ marginTop: 50 }} />}

        {/* Lỗi Zod và lỗi Mạng dùng CHUNG 1 cờ isError nhưng hiện 2 THÔNG ĐIỆP khác nhau (errorMessage ở trên) */}
        {isError && <Text style={{ textAlign: 'center', marginTop: 50, color: 'red' }}>{errorMessage}</Text>}

        {allProducts.length > 0 && (
          <FlashList
            data={allProducts}
            keyExtractor={(item) => item.id}
            renderItem={({ item }) => (
              // Bọc Pressable để bấm vào Card mở ProductDetail — chỉ gửi productId (Route Params),
              // KHÔNG gửi nguyên Object sản phẩm (đúng nguyên tắc Chương 5, Phần 5.3).
              // Nút "Mua ngay" nằm bên TRONG ProductCard (Bước 7) vẫn hoạt động độc lập —
              // nó tự bắt Touch trước, không bị Pressable ngoài này "cướp" sự kiện.
              <Pressable onPress={() => navigation.navigate('ProductDetail', { productId: item.id })}>
                <ProductCard product={item} />
              </Pressable>
            )}
            numColumns={2}
            estimatedItemSize={260} // Tuỳ chọn ở FlashList v2 — vẫn nên khai báo để layout ổn định hơn ở v1
            contentContainerStyle={{ padding: SIZES.padding }}
            refreshing={isRefetching} // Không cần tự quản lý useState nữa — React Query có sẵn cờ này
            onRefresh={refetch}       // Kéo tay xuống -> gọi lại trang 1, tự động cập nhật Cache
            // PHÂN TRANG THẬT: cuộn gần tới cuối danh sách -> tự động tải thêm trang kế tiếp
            onEndReached={() => {
              if (hasNextPage && !isFetchingNextPage) fetchNextPage();
            }}
            onEndReachedThreshold={0.5} // Kích hoạt khi còn cách đáy 50% chiều cao màn hình
            ListFooterComponent={
              isFetchingNextPage ? (
                <ActivityIndicator size="small" color={COLORS.primary} style={{ marginVertical: 16 }} />
              ) : null
            }
          />
        )}
      </View>
    </SafeAreaView>
  );
};
// ...styles giữ nguyên
export default HomeScreen;
```

> [!IMPORTANT]
> Đây là điểm khác biệt quan trọng nhất so với bản nháp lý thuyết ở Phần 6.8: `queryKey` đã đổi từ `['productsList']` sang `['productsInfinite']` vì cấu trúc `data` trả về của `useInfiniteQuery` là `{ pages: ProductPage[], pageParams: number[] }`, khác hẳn `useQuery` (trả thẳng `Product[]`). Bước 8.5 ngay sau đây phải cập nhật theo đúng `queryKey` và cấu trúc `data.pages` mới này.

#### Bước 8.5: Vá lỗi liên tục — Cập nhật lại `ProductDetailScreen`
> [!CAUTION]
> **Lỗi liên tục (Continuity Bug) nếu bỏ qua bước này:** `ProductDetailScreen` viết ở Chương 5 tra cứu sản phẩm bằng `MOCK_PRODUCTS.find(...)`. Nhưng ở Bước 4 của chương này, ta đã tuyên bố `src/data/mockProducts.ts` bị thay thế hoàn toàn bởi dữ liệu thật lấy qua React Query + Zod (`src/types/product.schema.ts`). Nếu không sửa `ProductDetailScreen`, app sẽ crash hoặc hiển thị "Không tìm thấy sản phẩm" ngay khi bấm vào Card ở Bước 8.

Cách sửa đơn giản nhất: `ProductDetailScreen` vẫn chỉ nhận `productId` qua Route Params (không đổi), nhưng thay vì tự gọi lại API, nó **mượn thẳng Cache mà `HomeScreen` đã tải sẵn** bằng `useQueryClient().getQueryData(['productsInfinite'])` — tận dụng đúng lợi ích Cache đã học ở Phần 6.5, không tốn thêm 1 Request nào. Vì Bước 8 giờ dùng `useInfiniteQuery`, Cache trả về có cấu trúc `{ pages: ProductPage[] }` (nhiều trang) thay vì thẳng `Product[]` — phải `flatMap` lại trước khi `find`. Mở lại `src/screens/ProductDetailScreen.tsx`:

```tsx
import React from 'react';
import { View, Text, StyleSheet, Image, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { RouteProp, useRoute } from '@react-navigation/native';
import { useQueryClient } from '@tanstack/react-query';
import ShopButton from '@components/ShopButton';
import { useCartStore } from '@store/useCartStore';
import { Product } from '../types/product.schema';
import { COLORS, SIZES } from '@constants/theme';
import type { HomeStackParamList } from '@navigation/HomeStackNavigator';

type ProductDetailRouteProp = RouteProp<HomeStackParamList, 'ProductDetail'>;

// Khớp đúng khuôn 1 "trang" dữ liệu mà HomeScreen (Bước 8) đã dùng cho useInfiniteQuery
interface ProductPage {
  items: Product[];
  nextPage: number | null;
}

const ProductDetailScreen = () => {
  const route = useRoute<ProductDetailRouteProp>();
  const { productId } = route.params; // Chỉ nhận đúng 1 chuỗi ID, KHÔNG nhận Object
  const queryClient = useQueryClient();
  const addItem = useCartStore((state) => state.addItem);

  // Móc thẳng vào Cache mà HomeScreen đã lưu với queryKey ['productsInfinite'] —
  // KHÔNG gọi lại API, tận dụng đúng cơ chế Cache của TanStack Query.
  // Cache của useInfiniteQuery có dạng { pages: ProductPage[], pageParams: number[] } —
  // phải flatMap tất cả các trang đã tải thành 1 mảng phẳng trước khi tìm theo id.
  const cachedData = queryClient.getQueryData<{ pages: ProductPage[] }>(['productsInfinite']);
  const cachedProducts = cachedData?.pages.flatMap((page) => page.items) ?? [];
  const product = cachedProducts.find((p) => p.id === productId);

  // Trường hợp Cache trống (VD: mở thẳng bằng Deep Link trước khi HomeScreen kịp Fetch)
  if (!product) {
    return (
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.center}>
          <Text style={styles.notFound}>Đang tải từ cloud... (Mã sản phẩm: {productId})</Text>
          <Text style={styles.hint}>
            Hãy quay lại Trang chủ để danh sách được tải vào Cache trước khi mở lại link này.
          </Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView contentContainerStyle={styles.container}>
        <Image source={{ uri: product.image }} style={styles.image} resizeMode="cover" />
        <Text style={styles.name}>{product.name}</Text>
        <Text style={styles.price}>
          {new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(product.price)}
        </Text>
        <Text style={styles.idNote}>Mã sản phẩm: {product.id}</Text>
        <ShopButton title="Thêm vào giỏ hàng" onPress={() => addItem(product)} style={styles.buyBtn} />
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: COLORS.background },
  container: { padding: SIZES.padding },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: SIZES.padding },
  image: { width: '100%', height: 320, borderRadius: SIZES.radius, marginBottom: SIZES.padding },
  name: { fontSize: SIZES.h2, fontWeight: 'bold', color: COLORS.text, marginBottom: 8 },
  price: { fontSize: SIZES.h1, fontWeight: 'bold', color: COLORS.primary, marginBottom: 8 },
  idNote: { fontSize: SIZES.body2, color: COLORS.textLight, marginBottom: 24 },
  buyBtn: { marginTop: 8 },
  notFound: { fontSize: SIZES.body1, color: COLORS.error, textAlign: 'center', marginBottom: 8 },
  hint: { fontSize: SIZES.body2, color: COLORS.textLight, textAlign: 'center' },
});

export default ProductDetailScreen;
```

> [!TIP]
> Cách khác (không dùng ở đây nhưng vẫn hợp lệ): tạo một `useProductsInfiniteQuery()` Custom Hook dùng chung `queryKey: ['productsInfinite']` ở cả `HomeScreen` và `ProductDetailScreen`, gọi `useInfiniteQuery` ở cả hai nơi — React Query sẽ tự nhận ra 2 lời gọi trùng `queryKey` và chỉ giữ đúng 1 bản Cache, không gọi API 2 lần.

#### Bước 9: Nâng cấp CartScreen từ bản nháp trống của Chương 5
Mở (hoặc tạo) file `src/screens/CartScreen.tsx`. Viết đầy đủ giao diện Danh sách + Trạng thái trống (Empty State):

```tsx
import React from 'react';
import { View, Text, StyleSheet, FlatList } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context'; // BẮT BUỘC lấy từ safe-area-context, KHÔNG lấy từ 'react-native'
import { useCartStore } from '@store/useCartStore';
import ShopButton from '@components/ShopButton';
import { COLORS, SIZES } from '@constants/theme';

const formatCurrency = (value: number) =>
  new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(value);

const CartScreen = ({ navigation }: any) => {
  const items = useCartStore(state => state.items);
  const removeItem = useCartStore(state => state.removeItem);
  const totalPrice = useCartStore(state => state.totalPrice());

  // TRẠNG THÁI TRỐNG (Empty State) — Đừng bao giờ để người dùng nhìn màn hình trắng vô hồn
  if (items.length === 0) {
    return (
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.emptyContainer}>
          <Text style={styles.emptyIcon}>🛒</Text>
          <Text style={styles.emptyText}>Giỏ hàng của bạn đang trống trơn!</Text>
          <ShopButton
            title="Quay về mua sắm"
            onPress={() => navigation.goBack()}
            style={{ marginTop: 20 }}
          />
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.header}>
        <Text style={styles.headerTitle}>Giỏ hàng của bạn</Text>
      </View>

      <FlatList
        data={items}
        keyExtractor={(item) => item.id}
        contentContainerStyle={{ padding: SIZES.padding }}
        renderItem={({ item }) => (
          <View style={styles.cartItem}>
            <View style={{ flex: 1 }}>
              <Text style={styles.itemName} numberOfLines={1}>{item.name}</Text>
              <Text style={styles.itemPrice}>{formatCurrency(item.price)} x {item.quantity}</Text>
            </View>
            <ShopButton
              title="Xóa"
              onPress={() => removeItem(item.id)}
              style={{ width: 70, height: 32, backgroundColor: COLORS.error }}
              textStyle={{ fontSize: 12 }}
            />
          </View>
        )}
      />

      <View style={styles.footer}>
        <Text style={styles.totalLabel}>
          Tổng cộng: <Text style={styles.totalValue}>{formatCurrency(totalPrice)}</Text>
        </Text>
        <ShopButton title="Thanh toán" onPress={() => {}} />
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: COLORS.background },
  emptyContainer: { flex: 1, justifyContent: 'center', alignItems: 'center', padding: SIZES.padding },
  emptyIcon: { fontSize: 60, marginBottom: 10 },
  emptyText: { fontSize: SIZES.body1, color: COLORS.textLight, textAlign: 'center' },
  header: { paddingHorizontal: SIZES.padding, paddingVertical: 15, backgroundColor: COLORS.surface },
  headerTitle: { fontSize: SIZES.h1, fontWeight: 'bold', color: COLORS.text },
  cartItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: COLORS.surface,
    borderRadius: SIZES.radius,
    padding: 12,
    marginBottom: 10,
  },
  itemName: { fontSize: SIZES.body2, color: COLORS.text, fontWeight: '500' },
  itemPrice: { fontSize: SIZES.body2, color: COLORS.primary, marginTop: 4 },
  footer: {
    padding: SIZES.padding,
    backgroundColor: COLORS.surface,
    borderTopWidth: 1,
    borderTopColor: '#eee',
  },
  totalLabel: { fontSize: SIZES.body1, color: COLORS.text, marginBottom: 10 },
  totalValue: { fontWeight: 'bold', color: COLORS.primary },
});

export default CartScreen;
```

> [!NOTE]
> Nút "Thanh toán" ở trên tạm để `onPress={() => {}}` — Bước 9.5 ngay sau đây sẽ nối nó vào `CheckoutScreen` thật.

#### Bước 9.5: Hoàn thiện Vòng lặp Mua sắm — `CheckoutScreen` & `RootStackNavigator`

Đến đây ShopAI đã có đủ Browse → Cart, còn thiếu mảnh cuối cùng: **Thanh toán**. Ta sẽ tạo `CheckoutScreen` và đặt nó vào một tầng Navigator MỚI — `RootStackNavigator` — bọc **bên ngoài** `MainTabNavigator` hiện có. Đây chính là mô hình "Navigator lồng Navigator" đã học ở Chương 5 (Phần 5.5): `MainTabNavigator` (Home Stack + Cart) **không hề bị sửa một dòng nào**, chỉ được nhét làm 1 màn hình con của `RootStackNavigator`, cùng cấp với `CheckoutScreen` hiện ra dạng Modal (trượt từ dưới lên, che luôn cả thanh Tab bar — đúng trải nghiệm Thanh toán của mọi app thương mại điện tử thật).

**9.5.1. Tạo `src/screens/CheckoutScreen.tsx`** — dùng `useMutation` (Phần 6.5 mục 4) thay vì `useState` + `setTimeout` thủ công, đúng chuẩn "GHI dữ liệu lên Server":

```tsx
import React from 'react';
import { View, Text, StyleSheet, ActivityIndicator } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import axiosClient from '@api/axiosClient';
import ShopButton from '@components/ShopButton';
import { useCartStore, CartItem } from '@store/useCartStore';
import { COLORS, SIZES } from '@constants/theme';

const formatCurrency = (value: number) =>
  new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(value);

interface CreateOrderPayload {
  items: CartItem[];
  totalPrice: number;
}

interface CreateOrderResponse {
  orderId: string;
}

// Hàm GHI dữ liệu lên Server qua axiosClient (Interceptor tự gắn Token — Phần 6.6).
// URL vẫn là Mock cho tới khi có Backend NestJS thật ở Chương 9, nhưng CẤU TRÚC gọi API
// đã đúng chuẩn Production ngay từ bây giờ — Chương 9 chỉ cần đổi baseURL, KHÔNG sửa gì ở đây.
const createOrder = async (payload: CreateOrderPayload): Promise<CreateOrderResponse> => {
  const res = await axiosClient.post<CreateOrderResponse>('/orders', payload);
  return res.data;
};

const CheckoutScreen = () => {
  const navigation = useNavigation();
  const queryClient = useQueryClient();
  const items = useCartStore((state) => state.items);
  const totalQuantity = useCartStore((state) => state.totalQuantity());
  const totalPrice = useCartStore((state) => state.totalPrice());
  const clearCart = useCartStore((state) => state.clearCart);

  // useMutation: hành động GHI dữ liệu (POST /orders) — CHỈ chạy khi ta gọi mutate(), không tự động như useQuery
  const { mutate, isPending, isError, isSuccess } = useMutation({
    mutationFn: createOrder,

    // onSuccess: chạy SAU KHI Server xác nhận đặt hàng thành công
    onSuccess: () => {
      clearCart(); // Đặt hàng thành công -> xóa sạch Giỏ hàng (persist ở Bước 3 cũng tự xóa theo)
      // Đơn hàng mới có thể ảnh hưởng tồn kho -> đánh dấu Cache sản phẩm là "Thiu" (Stale),
      // lần vào lại Home sau đó React Query sẽ tự fetch lại ngầm (Background refetch, Phần 6.5)
      queryClient.invalidateQueries({ queryKey: ['productsInfinite'] });
      setTimeout(() => navigation.goBack(), 1200); // Đóng Modal, quay lại Home sau 1.2s
    },

    // onError: chạy khi Server trả lỗi hoặc mất mạng — KHÔNG xóa giỏ hàng trong trường hợp này
    onError: (err) => {
      console.error('❌ Đặt hàng thất bại:', err);
    },
  });

  const handleConfirm = () => {
    mutate({ items, totalPrice }); // Chỉ khi bấm nút, request thật sự mới bay đi
  };

  if (isSuccess) {
    return (
      <SafeAreaView style={styles.safeArea}>
        <View style={styles.center}>
          <Text style={styles.successIcon}>✅</Text>
          <Text style={styles.successText}>Đặt hàng thành công!</Text>
        </View>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.container}>
        <Text style={styles.title}>Xác nhận đơn hàng</Text>

        <View style={styles.summaryRow}>
          <Text style={styles.label}>Số lượng sản phẩm</Text>
          <Text style={styles.value}>{totalQuantity}</Text>
        </View>
        <View style={styles.summaryRow}>
          <Text style={styles.label}>Tổng cộng</Text>
          <Text style={styles.totalValue}>{formatCurrency(totalPrice)}</Text>
        </View>

        {/* isError: hiện khi mutation thất bại (mất mạng, Server lỗi...) — KHÔNG rời màn hình, cho thử lại */}
        {isError && (
          <Text style={styles.errorText}>Đặt hàng thất bại — vui lòng kiểm tra mạng và bấm thử lại!</Text>
        )}

        {isPending ? (
          <ActivityIndicator size="large" color={COLORS.primary} style={{ marginTop: 24 }} />
        ) : (
          <ShopButton
            title="Xác nhận đặt hàng"
            onPress={handleConfirm}
            disabled={totalQuantity === 0}
            style={styles.confirmBtn}
          />
        )}
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: COLORS.background },
  container: { flex: 1, padding: SIZES.padding },
  title: { fontSize: SIZES.h1, fontWeight: 'bold', color: COLORS.text, marginBottom: 24 },
  summaryRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: COLORS.border,
  },
  label: { fontSize: SIZES.body1, color: COLORS.textLight },
  value: { fontSize: SIZES.body1, color: COLORS.text, fontWeight: '600' },
  totalValue: { fontSize: SIZES.h2, color: COLORS.primary, fontWeight: 'bold' },
  confirmBtn: { marginTop: 32 },
  errorText: { color: COLORS.error, textAlign: 'center', marginTop: 16 },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  successIcon: { fontSize: 60, marginBottom: 12 },
  successText: { fontSize: SIZES.h2, fontWeight: 'bold', color: COLORS.success },
});

export default CheckoutScreen;
```

> [!NOTE]
> **`isSuccess` là cờ có sẵn của `useMutation`** — tự động `true` ngay sau khi `mutationFn` resolve thành công (khác `useQuery`, `useMutation` không tự cache nên không cần lo tình trạng "cũ" của cờ này). Không cần thêm bất kỳ biến `useState` cục bộ nào để tự theo dõi trạng thái thành công như bản dùng `setTimeout` thủ công trước đây.
>
> **Về `baseURL` Mock và Lịch sử đơn:** `axiosClient` trỏ domain giả nên `isError` dễ xảy ra. **Bước 9.6** sẽ đổi `mutationFn` sang giả lập thành công cục bộ (trả `PENDING` + ghi `useOrderStore`) để nghiệm thu Lịch sử đơn / hóa đơn **trước khi có Nest**. Chương 9 Bước 9c đổi lại `axiosClient.post('/orders', …)` thật — **không** xóa UI Orders đã dựng.

**9.5.2. Tạo `src/navigation/RootStackNavigator.tsx`** — Tầng Navigator MỚI, bọc ngoài cùng `MainTabNavigator` hiện có:
```tsx
import React from 'react';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import MainTabNavigator from '@navigation/MainTabNavigator';
import CheckoutScreen from '@screens/CheckoutScreen';

export type RootStackParamList = {
  MainTabs: undefined;
  Checkout: undefined;
};

const Stack = createNativeStackNavigator<RootStackParamList>();

const RootStackNavigator = () => {
  return (
    <Stack.Navigator screenOptions={{ headerShown: false }}>
      {/* MainTabNavigator (Chương 5) được nhét nguyên vẹn làm 1 màn hình — KHÔNG sửa gì bên trong nó */}
      <Stack.Screen name="MainTabs" component={MainTabNavigator} />
      <Stack.Screen
        name="Checkout"
        component={CheckoutScreen}
        options={{
          presentation: 'modal', // Trượt từ dưới lên, che cả Tab bar — đúng trải nghiệm Checkout thật
          headerShown: true,
          title: 'Thanh toán',
        }}
      />
    </Stack.Navigator>
  );
};

export default RootStackNavigator;
```

> [!IMPORTANT]
> **Tính liên tục:** `HomeStackNavigator` (Chương 5) **giữ nguyên**. `MainTabNavigator` chỉ **thêm** Tab Đơn hàng ở Bước 9.6 — không đụng Home/Cart. `RootStackNavigator` bọc ngoài để có Checkout + OrderDetail.

**9.5.3. Cập nhật `App.tsx`** — đổi nhánh đã đăng nhập từ `<MainTabNavigator />` sang `<RootStackNavigator />` (chỉ đổi đúng 1 dòng + 1 import, theo đúng lời hẹn ở Bước 5):
```tsx
import RootStackNavigator from '@navigation/RootStackNavigator'; // Thay cho import MainTabNavigator trực tiếp

// ...bên trong NavigationContainer, nhánh đã đăng nhập:
{token == null ? (
  <AuthStack.Navigator screenOptions={{ headerShown: false }}>
    <AuthStack.Screen name="Login" component={LoginScreen} />
    <AuthStack.Screen name="Register" component={RegisterScreen} />
  </AuthStack.Navigator>
) : (
  <RootStackNavigator /> // Đổi từ <MainTabNavigator /> — giờ có thêm Checkout Modal
)}
```

**9.5.4. Nối nút "Thanh toán" ở `CartScreen` sang `Checkout`:**
Mở lại `src/screens/CartScreen.tsx` (Bước 9), chỉ sửa đúng dòng `onPress` của nút "Thanh toán":
```tsx
<ShopButton
  title="Thanh toán"
  onPress={() => navigation.navigate('Checkout')}
/>
```

> [!NOTE]
> `CartScreen` đang nằm sâu trong `Tab.Screen("Cart")` bên trong `MainTabNavigator`, còn `Checkout` lại nằm ở tầng `RootStackNavigator` bên ngoài — khác tầng Navigator hoàn toàn! Điều này **vẫn hoạt động bình thường** nhờ cơ chế "nổi bọt" (bubbling) mặc định của React Navigation: khi gọi `navigate('Checkout')` mà tầng Tab hiện tại không có màn hình tên này, React Navigation tự động tìm lên tầng Navigator cha (`RootStackNavigator`) — đúng nơi có `Checkout` — mà không cần gọi `navigation.getParent()` thủ công. `CartScreen` hiện đang khai báo `navigation: any` (Bước 9) nên TypeScript không cản gì ở đây; nếu muốn chuẩn Type-safe hoàn toàn, có thể định nghĩa lại Props của `CartScreen` bằng `CompositeScreenProps` như đã làm với `HomeScreen` ở Bước 8, ghép `BottomTabScreenProps<MainTabParamList, 'Cart'>` với `NativeStackScreenProps<RootStackParamList>`.

Chạy thử: Đăng nhập → Thêm vài sản phẩm vào giỏ → Sang Tab Giỏ hàng → Bấm "Thanh toán" → Modal `CheckoutScreen` trượt lên. *(Sau Bước 9.6, đặt hàng thành công sẽ ghi đơn `PENDING` vào Lịch sử.)*

#### Bước 9.6: Lịch sử đơn + Chi tiết hóa đơn + thanh toán giả lập `PENDING` → `PAID`

> [!IMPORTANT]
> **Vì sao gắn ở Chương 6?** Checkout/`useMutation` vừa dựng xong — đây là chỗ tự nhiên để đóng vòng **đặt hàng → xem hóa đơn → đổi trạng thái thanh toán**. Chương 9 chỉ thay nguồn local bằng Nest (`GET`/`POST …/pay`), **không** viết lại UI.

**9.6.1. Tạo `src/store/useOrderStore.ts`** (Client State — danh sách hóa đơn, persist như Cart):

```ts
import { create } from 'zustand';
import { persist, createJSONStorage } from 'zustand/middleware';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { CartItem } from './useCartStore';

export type PaymentStatus = 'PENDING' | 'PAID';

export interface OrderRecord {
  id: string;
  items: CartItem[];
  total: number;
  status: PaymentStatus;
  createdAt: string; // ISO
}

interface OrderState {
  orders: OrderRecord[];
  addOrder: (order: OrderRecord) => void;
  markPaid: (orderId: string) => void;
  getById: (orderId: string) => OrderRecord | undefined;
}

export const useOrderStore = create<OrderState>()(
  persist(
    (set, get) => ({
      orders: [],
      addOrder: (order) => set((s) => ({ orders: [order, ...s.orders] })),
      markPaid: (orderId) =>
        set((s) => ({
          orders: s.orders.map((o) =>
            o.id === orderId ? { ...o, status: 'PAID' as const } : o,
          ),
        })),
      getById: (orderId) => get().orders.find((o) => o.id === orderId),
    }),
    {
      name: 'shopai-orders',
      storage: createJSONStorage(() => AsyncStorage),
    },
  ),
);
```

**9.6.2. Cập nhật `CheckoutScreen` — giả lập đặt hàng thành công + ghi đơn `PENDING`**

Thay `mutationFn` / `onSuccess` (giữ UI còn lại). Mục tiêu Ch.6: luôn thấy được nhánh thành công để có hóa đơn trong Tab Đơn hàng:

```tsx
import { useOrderStore } from '@store/useOrderStore';

interface CreateOrderResponse {
  orderId: string;
  status: 'PENDING';
}

const createOrderLocal = async (payload: CreateOrderPayload): Promise<CreateOrderResponse> => {
  // Ch.6: giả lập Server. Ch.9 Bước 9c: đổi thành axiosClient.post('/orders', { items, total })
  await new Promise((r) => setTimeout(r, 1200));
  return { orderId: `ORD-${Date.now()}`, status: 'PENDING' };
};

// trong component:
const addOrder = useOrderStore((s) => s.addOrder);

const { mutate, isPending, isError, isSuccess, data } = useMutation({
  mutationFn: createOrderLocal,
  onSuccess: (res) => {
    addOrder({
      id: res.orderId,
      items: [...items],
      total: totalPrice,
      status: 'PENDING',
      createdAt: new Date().toISOString(),
    });
    clearCart();
    queryClient.invalidateQueries({ queryKey: ['productsInfinite'] });
    setTimeout(() => navigation.goBack(), 1500);
  },
  onError: (err) => console.error('❌ Đặt hàng thất bại:', err),
});
```

Ở nhánh `isSuccess`, hiển thị thêm mã đơn + trạng thái:

```tsx
<Text style={styles.successText}>Đặt hàng thành công!</Text>
<Text>Mã đơn: {data?.orderId}</Text>
<Text>Trạng thái: PENDING (chờ thanh toán)</Text>
```

**9.6.3. `OrdersScreen` + `OrderDetailScreen`**

Tạo `src/screens/OrdersScreen.tsx`:

```tsx
import React from 'react';
import { View, Text, FlatList, Pressable, StyleSheet } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { useNavigation } from '@react-navigation/native';
import { useOrderStore } from '@store/useOrderStore';
import { COLORS, SIZES } from '@constants/theme';

const formatCurrency = (v: number) =>
  new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(v);

const OrdersScreen = () => {
  const navigation = useNavigation<any>();
  const orders = useOrderStore((s) => s.orders);

  return (
    <SafeAreaView style={styles.safe} edges={['top']}>
      <Text style={styles.title}>Đơn hàng của tôi</Text>
      {orders.length === 0 ? (
        <View style={styles.empty}>
          <Text style={styles.emptyText}>Chưa có đơn nào. Hãy đặt hàng từ Giỏ.</Text>
        </View>
      ) : (
        <FlatList
          data={orders}
          keyExtractor={(item) => item.id}
          contentContainerStyle={{ padding: SIZES.padding }}
          renderItem={({ item }) => (
            <Pressable
              style={styles.card}
              onPress={() => navigation.navigate('OrderDetail', { orderId: item.id })}
            >
              <Text style={styles.orderId}>{item.id}</Text>
              <Text style={styles.meta}>
                {formatCurrency(item.total)} · {item.status}
              </Text>
              <Text style={styles.date}>{new Date(item.createdAt).toLocaleString('vi-VN')}</Text>
            </Pressable>
          )}
        />
      )}
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: COLORS.background },
  title: {
    fontSize: SIZES.h2,
    fontWeight: '800',
    color: COLORS.primary,
    padding: SIZES.padding,
  },
  empty: { flex: 1, alignItems: 'center', justifyContent: 'center', padding: 24 },
  emptyText: { color: COLORS.textLight, textAlign: 'center' },
  card: {
    backgroundColor: COLORS.white,
    padding: 16,
    borderRadius: 12,
    marginBottom: 12,
  },
  orderId: { fontWeight: '700', fontSize: SIZES.body1, color: COLORS.text },
  meta: { marginTop: 4, color: COLORS.primary, fontWeight: '600' },
  date: { marginTop: 4, color: COLORS.textLight, fontSize: SIZES.body2 },
});

export default OrdersScreen;
```

Tạo `src/screens/OrderDetailScreen.tsx` (chi tiết hóa đơn + nút Pay giả lập):

```tsx
import React from 'react';
import { View, Text, StyleSheet, ScrollView } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { NativeStackScreenProps } from '@react-navigation/native-stack';
import ShopButton from '@components/ShopButton';
import { useOrderStore } from '@store/useOrderStore';
import { COLORS, SIZES } from '@constants/theme';
import { RootStackParamList } from '@navigation/RootStackNavigator';

type Props = NativeStackScreenProps<RootStackParamList, 'OrderDetail'>;

const formatCurrency = (v: number) =>
  new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(v);

const OrderDetailScreen = ({ route }: Props) => {
  const { orderId } = route.params;
  const order = useOrderStore((s) => s.getById(orderId));
  const markPaid = useOrderStore((s) => s.markPaid);

  if (!order) {
    return (
      <SafeAreaView style={styles.safe}>
        <Text style={styles.missing}>Không tìm thấy đơn {orderId}</Text>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.safe} edges={['bottom']}>
      <ScrollView contentContainerStyle={styles.container}>
        <Text style={styles.heading}>Hóa đơn</Text>
        <Text style={styles.row}>Mã: {order.id}</Text>
        <Text style={styles.row}>Trạng thái: {order.status}</Text>
        <Text style={styles.row}>Ngày: {new Date(order.createdAt).toLocaleString('vi-VN')}</Text>

        <Text style={[styles.heading, { marginTop: 20 }]}>Chi tiết</Text>
        {order.items.map((it) => (
          <View key={it.id} style={styles.itemRow}>
            <Text style={{ flex: 1 }}>{it.name} × {it.quantity}</Text>
            <Text>{formatCurrency(it.price * it.quantity)}</Text>
          </View>
        ))}

        <Text style={styles.total}>Tổng: {formatCurrency(order.total)}</Text>

        {order.status === 'PENDING' ? (
          <ShopButton
            title="Thanh toán giả lập (→ PAID)"
            onPress={() => markPaid(order.id)}
            style={{ marginTop: 24 }}
          />
        ) : (
          <Text style={styles.paidNote}>Đã thanh toán ✓</Text>
        )}
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: COLORS.background },
  container: { padding: SIZES.padding },
  heading: { fontSize: SIZES.h3, fontWeight: '800', color: COLORS.primary, marginBottom: 8 },
  row: { marginBottom: 4, color: COLORS.text },
  itemRow: {
    flexDirection: 'row',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#EEE',
  },
  total: { marginTop: 16, fontSize: SIZES.h3, fontWeight: '800', color: COLORS.text },
  paidNote: { marginTop: 24, color: 'green', fontWeight: '700', textAlign: 'center' },
  missing: { padding: 24, color: COLORS.textLight },
});

export default OrderDetailScreen;
```

**9.6.4. Đăng ký Tab Đơn hàng + màn `OrderDetail` trên RootStack**

Trong `MainTabNavigator.tsx`, **thêm** Tab (không xóa Home/Cart):

```tsx
import OrdersScreen from '@screens/OrdersScreen';
// ...
<Tab.Screen
  name="Orders"
  component={OrdersScreen}
  options={{
    title: 'Đơn hàng',
    tabBarIcon: ({ color, size }) => (
      <Icon name="receipt-text-outline" color={color} size={size} />
    ),
  }}
/>
```

Cập nhật `RootStackNavigator.tsx` — **thêm** (không thay Checkout):

```tsx
import OrderDetailScreen from '@screens/OrderDetailScreen';

export type RootStackParamList = {
  MainTabs: undefined;
  Checkout: undefined;
  OrderDetail: { orderId: string };
};

// thêm Screen:
<Stack.Screen
  name="OrderDetail"
  component={OrderDetailScreen}
  options={{ headerShown: true, title: 'Chi tiết hóa đơn' }}
/>
```

**Nghiệm thu nhanh Bước 9.6:** Checkout thành công → Tab Đơn hàng thấy đơn `PENDING` → mở chi tiết → bấm "Thanh toán giả lập" → `PAID` → tắt app mở lại, đơn vẫn còn (persist).

#### Bước 10: [BÀI TẬP BẮT BUỘC ĐỀ CƯƠNG] Module học tập Redux Toolkit — song song với Zustand

> [!IMPORTANT]
> Bước này là **bắt buộc theo đề cương chính thức** (5.1.2, 5.2.1–5.2.4), độc lập với Cart Production của ShopAI (vẫn dùng Zustand). Mục tiêu: chứng minh học viên tự tay viết được một Store Redux Toolkit hoàn chỉnh, KHÔNG được xóa/thay Zustand Cart đang chạy tốt.

Tạo thư mục học tập `src/store/redux/` — tách biệt hoàn toàn với `src/store/useCartStore.ts` / `useAuthStore.ts` (Zustand) của Production:

**10.1. Tạo `src/store/redux/cartSlice.ts`** (bản học tập, mô phỏng lại logic Cart bằng RTK để so sánh trực tiếp với Zustand):
```ts
import { createSlice, PayloadAction } from '@reduxjs/toolkit';
import { Product } from '../../types/product.schema';

export interface CartItemRedux extends Product {
  quantity: number;
}

interface CartReduxState {
  items: CartItemRedux[];
}

const initialState: CartReduxState = { items: [] };

const cartSlice = createSlice({
  name: 'cartRedux',
  initialState,
  reducers: {
    addItem: (state, action: PayloadAction<Product>) => {
      const existing = state.items.find((item) => item.id === action.payload.id);
      if (existing) {
        existing.quantity += 1; // Immer cho phép "mutate" trực tiếp an toàn
      } else {
        state.items.push({ ...action.payload, quantity: 1 });
      }
    },
    removeItem: (state, action: PayloadAction<string>) => {
      state.items = state.items.filter((item) => item.id !== action.payload);
    },
    clearCart: (state) => {
      state.items = [];
    },
  },
});

export const { addItem, removeItem, clearCart } = cartSlice.actions;
export default cartSlice.reducer;
```

**10.2. Tạo `src/store/redux/store.ts`:**
```ts
import { configureStore } from '@reduxjs/toolkit';
import cartReducer from './cartSlice';

export const reduxStore = configureStore({
  reducer: { cartRedux: cartReducer },
});

export type ReduxRootState = ReturnType<typeof reduxStore.getState>;
export type ReduxAppDispatch = typeof reduxStore.dispatch;
```

**10.3. Bọc thêm `<Provider>` trong `App.tsx`** (lồng cùng `QueryClientProvider` hiện có — không đụng vào `RootStackNavigator`/`ThemeProvider`/Zustand):
```tsx
import { Provider } from 'react-redux';
import { reduxStore } from '@store/redux/store';

// ... bên trong <QueryClientProvider>, bọc thêm — ThemeProvider vẫn ở trong cùng như Bước 5/9.5:
<Provider store={reduxStore}>
  <ThemeProvider>
    <NavigationContainer>
      {/* ...giữ nguyên toàn bộ luồng Auth + RootStackNavigator (MainTabNavigator + Checkout) hiện có... */}
    </NavigationContainer>
  </ThemeProvider>
</Provider>
```

**10.4. Tạo màn hình demo `src/screens/ReduxCartDemoScreen.tsx`** (chỉ để học/nghiệm thu RTK, KHÔNG phải Cart chính thức của App):
```tsx
import React from 'react';
import { View, Text, FlatList } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context'; // Giữ đúng nguồn import — không lấy từ 'react-native'
import { useSelector, useDispatch } from 'react-redux';
import { addItem, removeItem } from '@store/redux/cartSlice';
import type { ReduxRootState } from '@store/redux/store';
import ShopButton from '@components/ShopButton';

const ReduxCartDemoScreen = () => {
  const items = useSelector((state: ReduxRootState) => state.cartRedux.items);
  const dispatch = useDispatch();

  return (
    <SafeAreaView style={{ flex: 1, padding: 16 }}>
      <Text style={{ fontSize: 18, fontWeight: 'bold', marginBottom: 12 }}>
        [Demo Bắt Buộc Đề Cương] Redux Toolkit Cart
      </Text>
      <FlatList
        data={items}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => (
          <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginBottom: 8 }}>
            <Text>{item.name} x {item.quantity}</Text>
            <ShopButton title="Xóa" onPress={() => dispatch(removeItem(item.id))} style={{ width: 70, height: 32 }} />
          </View>
        )}
      />
    </SafeAreaView>
  );
};

export default ReduxCartDemoScreen;
```

Đăng ký `ReduxCartDemoScreen` như một Tab/Screen **tùy chọn** trong `MainTabNavigator` (ví dụ Tab ẩn tên "RTK Demo") chỉ để giảng viên nghiệm thu — Cart thật của người dùng ShopAI vẫn luôn là `useCartStore` (Zustand) ở `CartScreen`.

> [!NOTE]
> Nếu lớp học eo hẹp thời gian, giảng viên có thể thay Bước 10 bằng bài tập về nhà: **học viên tự viết một `counterSlice` RTK độc lập** (theo đúng ví dụ ở Phần 6.4) và nộp lại — không nhất thiết phải tích hợp vào ShopAI, miễn là đúng cú pháp `createSlice` + `configureStore` + `useSelector`/`useDispatch` theo đề cương.

#### Bước 11: Tận hưởng Thành quả & Lưu code
Bạn chạy lại app, bấm đăng nhập. Bạn sẽ thấy vòng xoay Loading hiện ra, rồi load trang sản phẩm ĐẦU TIÊN (10 sản phẩm, đã qua kiểm duyệt Zod). **Cuộn xuống gần cuối danh sách** — `ListFooterComponent` hiện Spinner nhỏ và trang kế tiếp tự động nối vào (Bước 8, `useInfiniteQuery`), cứ thế tới khi hết 47 sản phẩm giả lập thì việc tải thêm tự dừng hẳn. Thỉnh thoảng bạn sẽ thấy thông báo lỗi mạng (do giả lập ngẫu nhiên ~10%) khác hẳn thông báo lỗi Zod — đúng yêu cầu phân biệt 2 loại lỗi. Kéo tay xuống đầu danh sách để thử Pull-to-refresh thật (Bước 8). Bấm "Mua ngay" ở vài sản phẩm, rồi chuyển sang **Tab Giỏ hàng** ở thanh đáy — bạn sẽ thấy đúng những sản phẩm mình vừa chọn, với số lượng và tổng tiền chính xác. **Tắt hẳn App rồi mở lại** — Giỏ hàng vẫn còn nguyên nhờ `persist` (Bước 3). Bấm "Thanh toán" → Modal `CheckoutScreen` hiện ra → Bấm "Xác nhận đặt hàng" → `useMutation` chạy (`isPending` hiện Spinner) → thành công thì Giỏ hàng tự xóa và quay về Home, thất bại (do `baseURL` còn Mock) thì hiện thông báo lỗi rõ ràng và cho phép bấm lại (Bước 9.5).

Bạn vừa nâng tầm cấu trúc luồng dữ liệu của App lên chuẩn Kỹ sư phần mềm toàn cầu: Client State (Cart, có Persist) tách biệt hoàn toàn khỏi Server State (Products phân trang thật bằng `useInfiniteQuery`, có Cache + Pull-to-refresh; Đặt hàng ghi dữ liệu bằng `useMutation` có `invalidateQueries`), và dữ liệu mạng luôn được Zod gác cổng. Không còn một chút rác Prop Drilling nào nữa. `MainTabNavigator`/`HomeStackNavigator` từ Chương 5 vẫn nguyên vẹn 100%, chỉ được bọc thêm bởi `RootStackNavigator` để có Checkout. Đồng thời, bạn đã hoàn thành đủ **cả 3 giải pháp State Management theo đề cương**: Context API (lý thuyết + demo Theme), Redux Toolkit (module `src/store/redux/` bắt buộc), và Zustand (giải pháp Production thật của ShopAI).

**Đến đây, vòng lặp mua sắm cốt lõi của ShopAI đã HOÀN CHỈNH:** Đăng nhập/Đăng ký → Duyệt SP → Giỏ → Checkout → Lịch sử đơn (`PENDING`) → Thanh toán giả lập (`PAID`) → Chi tiết hóa đơn. Các chương sau nâng cấp Native/AI/Backend — Ch.9 nối Nest thật cho Register/Orders/Pay.

```bash
git add .
git commit -m "Sprint 6: Zustand Cart+Orders persist, InfiniteQuery, Checkout, Order history PENDING/PAID, RTK de cuong"
```

### ✅ Checklist Nghiệm thu Sprint 6
- [ ] Token đăng nhập và Giỏ hàng chạy trên Zustand, đồng bộ toàn App qua `RootStackNavigator`/`MainTabNavigator`.
- [ ] AuthStack còn **Login + Register**; cả hai dùng Zustand `login()`.
- [ ] `HomeScreen` load sản phẩm qua TanStack Query, dữ liệu đi qua Zod trước khi hiển thị, kéo tay xuống để Pull-to-refresh (`refetch`).
- [ ] **`HomeScreen` PHẢI phân trang THẬT bằng `useInfiniteQuery`** (không chỉ hiểu lý thuyết suông ở Phần 6.8): cuộn tới cuối danh sách tự động `fetchNextPage()`, dừng đúng lúc khi `hasNextPage` là `false`, có `ListFooterComponent` hiện `ActivityIndicator` nhỏ khi `isFetchingNextPage`.
- [ ] `HomeScreen` phân biệt rõ 2 thông báo lỗi khác nhau khi `isError`: lỗi dữ liệu không hợp lệ (Zod) và lỗi mất mạng — không gộp chung một câu mơ hồ.
- [ ] Giỏ hàng có `persist` (AsyncStorage) — tắt hẳn App rồi mở lại, các sản phẩm đã thêm vẫn còn nguyên.
- [ ] `CheckoutScreen` mở dưới dạng Modal từ `CartScreen`, **đặt hàng bằng `useMutation`** — `onSuccess` ghi đơn `PENDING` vào `useOrderStore` + xóa Giỏ.
- [ ] Tab **Đơn hàng** liệt kê đơn; `OrderDetailScreen` hiện chi tiết hóa đơn; nút **Thanh toán giả lập** đổi `PENDING` → `PAID`; tắt app đơn vẫn còn.
- [ ] `axiosClient` (Interceptor tự gắn Token, tự xử lý lỗi 401) đã được tạo ở `src/api/axiosClient.ts`.
- [ ] Giải thích được sự khác nhau giữa `useQuery` (đọc, tự động) và `useMutation` (ghi, chủ động gọi `mutate()`), và vì sao `invalidateQueries` lại quan trọng sau mỗi lần Ghi thành công.
- [ ] **[Bắt buộc đề cương]** Module `src/store/redux/` (Redux Toolkit) hoàn chỉnh với `createSlice`, `configureStore`, `Provider`, `useSelector`/`useDispatch` — hoạt động song song, không phá vỡ Zustand Cart Production.
- [ ] Hiểu rõ bảng so sánh Context vs Redux Toolkit vs Zustand và giải thích được vì sao ShopAI chọn Zustand.
- [ ] Hiểu vì sao Token KHÔNG được persist bằng AsyncStorage (chờ `SecureStore` ở Chương 8), trong khi Giỏ hàng thì được.
---

## 🎯 CHUẨN BỊ CHO CHƯƠNG 7
Vòng lặp mua sắm cốt lõi (Browse → Cart → Checkout → Orders/Pay) của ShopAI đã hoàn chỉnh. Đến lúc App của bạn vươn mình ra khỏi cái kén JavaScript. Ở Chương 7, chúng ta sẽ cho JS phá rào cản, gọi thẳng xuống Hệ điều hành để Xin quyền truy cập (Permission), kích hoạt **Camera phần cứng** để quét mã vạch Barcode và định vị bản đồ. Bạn sẽ hiểu cái gì gọi là **Native Modules**.

> Token đăng nhập vẫn đang nằm trong Zustand thuần (không persist) — Chương 8 sẽ khắc phục điểm này bằng `SecureStore` mã hóa phần cứng, hoàn thiện nốt mảnh ghép bảo mật cuối cùng.
