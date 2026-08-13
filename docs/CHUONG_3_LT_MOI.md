---
sidebar_position: 3
title: Chương 3
---

# GIÁO TRÌNH LÝ THUYẾT & THỰC CHIẾN

## CHƯƠNG 3: COMPONENTS CAO CẤP, TỐI ƯU RE-RENDER & HỆ THỐNG THIẾT KẾ (DESIGN SYSTEM)

**Thời lượng:** 6 tiết Lý thuyết + 3 tiết Thực hành

> **Ánh xạ đề cương:** Chương này phủ đủ nhóm **Hooks** trong đề cương môn học — ôn lại `useState`/`useEffect` (đã học Chương 1–2), bổ sung **`useContext`** và **`useReducer`** (mới, Phần 3.3), rồi tối ưu render với `useMemo`/`useCallback` (Phần 3.5).

---

> [!IMPORTANT]
> **Thực hành chương = Sprint ShopAI cuối file.** Hoàn thành Sprint này để đạt mục tiêu chương. Hoàn thành đủ 11 chương theo `SHOPAI_HOAN_THIEN.md` = sản phẩm ShopAI **hoàn thiện đẳng cấp**.

## 📚 MỤC TIÊU HỌC TẬP

Sau khi hoàn thành chương này, học viên sẽ:

- ✅ Hiểu được triết lý **Atomic Design** để xây dựng Design System (Hệ thống thiết kế) nhất quán.
- ✅ Biết bản chất hệ thống CSS của React Native (`StyleSheet.create`) và tại sao Inline Styles giết chết hiệu năng.
- ✅ **Cầm tay chỉ việc:** Đọc được `StyleSheet` như đọc một "bản vẽ UI" — nhìn 1 khối giao diện là biết ngay cần khai báo key nào (`backgroundColor`, `padding`, `borderRadius`, `fontSize`...), không còn bỡ ngỡ với cú pháp style của React Native.
- ✅ Làm chủ 2 Hook còn lại của đề cương: **`useContext`** (chia sẻ dữ liệu toàn cục, tránh Prop Drilling) và **`useReducer`** (quản lý State phức tạp bằng mô hình Action/Reducer) — đồng thời ôn lại `useState`/`useEffect` đã học.
- ✅ Làm chủ Kỹ thuật tách logic ra khỏi giao diện bằng **Custom Hooks**.
- ✅ Nắm vững nghệ thuật tối ưu hóa Re-render với `React.memo`, `useMemo`, `useCallback` (Đặc biệt: Nhận biết lúc nào DÙNG LÀ SAI).
- ✅ Biết xu hướng Style hiện đại 2025–2026 (**NativeWind**, **Unistyles 3**) đang được nhiều dự án Enterprise dùng, dù ShopAI vẫn trung thành với `StyleSheet` chuẩn để nắm chắc bản chất trước.
- ✅ **Thực chiến:** Xây dựng bộ UI Kit tiêu chuẩn cho ShopAI (Button, Input, Typography) kèm chế độ **Sáng/Tối (Dark Mode) thật** bằng `ThemeContext`.
- ✅ Hiểu và tích hợp **i18n** (Đa ngôn ngữ) để ứng dụng hỗ trợ Tiếng Việt & Tiếng Anh.
- ✅ Ứng dụng **Micro-animations** (Lottie) để tạo hiệu ứng mượt mà, chuyên nghiệp (Luxury UI).

---

## 🎨 PHẦN 3.1: HỆ THỐNG THIẾT KẾ (DESIGN SYSTEM) VÀ ATOMIC DESIGN

### 1. Vấn đề của lập trình viên mới

Khi xây dựng ứng dụng, sinh viên thường có thói quen copy-paste code giao diện. Ví dụ, bạn có 10 màn hình cần dùng nút "Xác nhận". Bạn viết CSS cho nút bấm đó ở màn hình 1, rồi copy sang 9 màn hình còn lại.
Khi khách hàng yêu cầu: _"Hãy đổi toàn bộ nút màu Xanh dương sang màu Cam"_. Bạn sẽ phải đi sửa 10 file khác nhau. Nếu quên 1 file, app sẽ bị lệch màu.

### 2. Triết lý Atomic Design (Thiết kế nguyên tử)

Để giải quyết vấn đề trên, các tập đoàn lớn (Facebook, Uber, Shopee) sử dụng mô hình Atomic Design do Brad Frost tạo ra. Nó chia giao diện thành 5 cấp độ từ nhỏ đến lớn:

1. **Atoms (Nguyên tử):** Các thành phần cơ bản nhất, không thể chia nhỏ hơn (Ví dụ: Thẻ `<Text>`, một cái Nút, một ô Input, một cái Icon).
2. **Molecules (Phân tử):** Sự kết hợp của vài Atoms (Ví dụ: Một ô Input đi kèm với một cái Nút tìm kiếm tạo thành Thanh Tìm Kiếm).
3. **Organisms (Sinh vật):** Kết hợp nhiều Molecules (Ví dụ: Header của ứng dụng bao gồm Thanh Tìm Kiếm, Logo, Nút Giỏ hàng).
4. **Templates:** Khung sườn bố cục chưa có dữ liệu thật.
5. **Pages:** Màn hình hoàn chỉnh được bơm dữ liệu thật từ API.

_Trong dự án ShopAI, chúng ta sẽ áp dụng triệt để cấp độ Atoms bằng cách tạo ra một thư mục `@components/ui` chuyên chứa các nút bấm, chữ viết dùng chung._

---

## 💅 PHẦN 3.2: BẢN CHẤT CỦA `StyleSheet` TRONG REACT NATIVE

### 3.2.0 StyleSheet cho người mới — cầm tay chỉ việc

> Mục này dành cho bạn nào lần đầu thấy `style={styles.button}` mà chưa hiểu nó là cái gì, tới từ đâu. Đọc xong mục này rồi hẵng đọc tiếp phần "bản chất nâng cao" (mục 1-3 phía dưới).

#### A. Nhìn giao diện trước, học code sau — "bản vẽ UI" là gì?

Trước khi viết bất kỳ dòng code nào, hãy tập thói quen của dân thiết kế/lập trình chuyên nghiệp: **nhìn 1 màn hình, chia nó ra thành từng khối nhỏ, rồi hỏi "khối này cần thuộc tính gì?"**. Đây là màn hình ví dụ chúng ta sẽ dựng trong mục này:

```
┌───────────────────────────────────────┐
│              📱  Màn hình               │
│                                         │
│                                         │
│        (A) Chào mừng đến ShopAI!       │
│                                         │
│         ┌─────────────────────┐        │
│         │   (B)   Mua ngay    │        │
│         └─────────────────────┘        │
│              ▲                         │
│              (C) toàn khối canh giữa   │
│                  theo chiều ngang/dọc  │
└───────────────────────────────────────┘
```

Giờ "dịch" từng khối trong bản vẽ trên sang đúng tên key mà `StyleSheet` dùng:

| Ký hiệu | Phần tử nhìn thấy trên hình              | Key StyleSheet tương ứng                     | Ý nghĩa                                                                                   |
| ------- | ---------------------------------------- | -------------------------------------------- | ----------------------------------------------------------------------------------------- |
| (A)     | Dòng chữ tiêu đề                         | `fontSize`, `color`                          | Cỡ chữ và màu chữ của dòng "Chào mừng..."                                                 |
| (B)     | Khối nút màu đỏ, bo tròn góc             | `backgroundColor`, `padding`, `borderRadius` | Màu nền nút, khoảng đệm bên trong nút, độ bo góc                                          |
| (C)     | Toàn bộ nội dung được canh giữa màn hình | `alignItems`, `justifyContent`               | Canh giữa các phần tử con theo chiều ngang (`alignItems`) và chiều dọc (`justifyContent`) |

**Cách đọc bảng này:** mỗi khi bạn nhìn thấy 1 thiết kế (từ Figma, ảnh chụp, hoặc yêu cầu bằng lời của khách hàng), hãy tập "bóc tách" nó thành từng mảnh nhỏ như bảng trên **trước khi** mở code editor ra gõ. Đây chính là kỹ năng "đọc bản vẽ UI" nhắc ở mục tiêu đầu chương.

#### B. React Native KHÔNG có file `.css` — mọi thứ là Object JavaScript

Nếu bạn từng học web, phản xạ đầu tiên sẽ là tìm file `.css` hoặc gõ `className="..."`. Trong React Native, **KHÔNG TỒN TẠI** khái niệm đó:

- Không có file `.css`, `.scss` nào cả.
- Không có `class`/`id` để rồi viết `.button { ... }` ở nơi khác.
- Prop `style` của mọi thẻ (`<View>`, `<Text>`, `<Image>`...) chỉ nhận vào **một Object JavaScript thuần túy** — giống hệt một object bình thường bạn khai báo bằng `{ key: value }`.
- `StyleSheet.create({...})` là cách làm **chuẩn (tiêu chuẩn ngành)** để khai báo nhiều style cùng lúc, gọn gàng, tách khỏi phần JSX — bạn sẽ dùng nó ở gần như 100% component trong suốt khóa học.

```tsx
// Cách 1: viết Object trực tiếp — vẫn chạy được, nhưng không phải chuẩn khuyến nghị
<View style={{ backgroundColor: 'red', padding: 10 }}>

// Cách 2: StyleSheet.create — CHUẨN, dùng xuyên suốt dự án ShopAI
<View style={styles.button}>
```

#### C. File mẫu chạy được: `StyleSheetWalkthrough.tsx`

Copy nguyên file dưới đây vào máy (thay nội dung 1 màn hình bất kỳ, ví dụ `HomeScreen.tsx`) để thấy kết quả thật — đúng với bản vẽ UI ở mục A:

```tsx
// StyleSheetWalkthrough.tsx
// File CHẠY ĐƯỢC — dán nguyên vào 1 màn hình để xem kết quả giống bản vẽ UI ở mục A
import React from "react";
import { View, Text, StyleSheet } from "react-native";

const StyleSheetWalkthrough = () => {
  return (
    <View style={styles.container}>
      <Text style={styles.title}>Chào mừng đến ShopAI!</Text>

      <View style={styles.button}>
        <Text style={styles.buttonText}>Mua ngay</Text>
      </View>
    </View>
  );
};

// StyleSheet.create LUÔN đặt Ở DƯỚI CÙNG file, BÊN NGOÀI Component
const styles = StyleSheet.create({
  container: {
    flex: 1, // Chiếm toàn bộ chiều cao màn hình
    alignItems: "center", // (C) Canh giữa các con theo chiều NGANG
    justifyContent: "center", // (C) Canh giữa các con theo chiều DỌC
    backgroundColor: "#F5F5F5",
  },
  title: {
    fontSize: 20, // (A) Cỡ chữ — SỐ THUẦN, KHÔNG có đơn vị 'px'
    color: "#2C3E50", // (A) Màu chữ — viết là `color`, không phải `font-color`
    marginBottom: 16,
  },
  button: {
    backgroundColor: "red", // (B) Màu nền nút
    paddingVertical: 12, // (B) Khoảng đệm trên/dưới bên trong nút
    paddingHorizontal: 24, // (B) Khoảng đệm trái/phải bên trong nút
    borderRadius: 8, // (B) Bo góc — SỐ THUẦN, KHÔNG có 'px'
  },
  buttonText: {
    color: "#FFFFFF",
    fontSize: 16,
    fontWeight: "600",
  },
});

export default StyleSheetWalkthrough;
```

**Giải thích từng khối:**

| Khối trong file                                         | Ý nghĩa                                                                                                                                                  |
| ------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `import { View, Text, StyleSheet } from 'react-native'` | Bắt buộc phải import `StyleSheet` mới dùng được `StyleSheet.create` — quên dòng này là lỗi phổ biến nhất của người mới (xem mục D bên dưới)              |
| `<View style={styles.container}>`                       | `style` nhận vào **1 object** — ở đây là `styles.container`, tức là "cái key tên `container` nằm trong object `styles`"                                  |
| `const styles = StyleSheet.create({...})`               | Gom tất cả style của file vào 1 object `styles` duy nhất, mỗi key (`container`, `title`, `button`, `buttonText`) tương ứng với 1 khối giao diện          |
| Đặt `styles` **bên ngoài** Component, ở **cuối file**   | Đây là quy ước chuẩn trong toàn bộ React Native: JSX/logic ở trên, `StyleSheet.create` ở dưới cùng — giúp file dễ đọc, tách rõ "cấu trúc" và "hình thức" |
| `flex: 1`                                               | Yêu cầu `View` này chiếm hết khoảng trống có thể chiếm được (ở đây là toàn màn hình)                                                                     |
| `alignItems` / `justifyContent`                         | 2 thuộc tính Flexbox dùng để canh giữa nội dung — học sâu hơn ở Chương 4                                                                                 |
| Comment số `(A)`/`(B)`/`(C)` trong code                 | Cố tình đối chiếu ngược lại với bản vẽ UI ở mục A — giúp bạn nối được "hình" với "code"                                                                  |

#### D. Lỗi thường gặp nhất của người mới

| Lỗi                                | Viết SAI (thói quen từ web)                                  | Viết ĐÚNG (React Native)                     | Vì sao sai                                                                                                                                                                                                                           |
| ---------------------------------- | ------------------------------------------------------------ | -------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| Dùng `className` như web/Tailwind  | `<View className="bg-red-500 p-4">`                          | `<View style={styles.box}>`                  | RN không hiểu prop `className` (trừ khi cài thêm thư viện NativeWind — xem PHẦN 3.2 mục 3 "Xu hướng Style 2025–2026" phía dưới) — component vẫn "chạy" nhưng giao diện **không đổi gì cả**, khiến người mới tưởng mình đang làm đúng |
| Viết tên key kiểu CSS (kebab-case) | `{ 'font-size': 16, 'background-color': 'red' }`             | `{ fontSize: 16, backgroundColor: 'red' }`   | Style RN là Object JavaScript, tên key phải là camelCase như thuộc tính JS bình thường, không phải chuỗi CSS                                                                                                                         |
| Thêm đơn vị `px` vào số            | `{ padding: '10px', borderRadius: '8px' }`                   | `{ padding: 10, borderRadius: 8 }`           | RN mặc định hiểu số là đơn vị density-independent pixel (dp); truyền chuỗi `'10px'` sẽ gây lỗi hoặc bị bỏ qua âm thầm                                                                                                                |
| Quên `import { StyleSheet }`       | Gọi `StyleSheet.create(...)` nhưng import thiếu `StyleSheet` | `import { StyleSheet } from 'react-native';` | Báo lỗi ngay lập tức: `StyleSheet is not defined`                                                                                                                                                                                    |

#### E. Vì sao phải học `StyleSheet.create` thay vì cứ viết Object trực tiếp trong JSX?

```
MỖI LẦN COMPONENT RE-RENDER (state đổi, props đổi...)

Cách 1 — Inline Style: style={{ backgroundColor: 'red', padding: 10 }}
  Render lần 1  →  tạo Object MỚI  (ô nhớ #1001)
  Render lần 2  →  tạo Object MỚI  (ô nhớ #1002)  ← khác ô nhớ lần 1!
  Render lần 3  →  tạo Object MỚI  (ô nhớ #1003)  ← khác cả 2 ô nhớ trước!
  ...cứ thế lặp lại → tốn RAM tạo mới liên tục + tốn CPU dọn rác (Garbage Collector)

Cách 2 — StyleSheet.create: const styles = StyleSheet.create({ button: {...} })
  Chỉ chạy DUY NHẤT 1 LẦN, ngay khi file được nạp (import lần đầu)
  Render lần 1  →  dùng lại object cũ  (ô nhớ #2001)
  Render lần 2  →  dùng lại object cũ  (VẪN ô nhớ #2001)
  Render lần 3  →  dùng lại object cũ  (VẪN ô nhớ #2001)
  ...không bao giờ tạo mới → tiết kiệm RAM/CPU, và (quan trọng hơn) giúp
     React.memo/useMemo so sánh "style cũ vs style mới" chính xác (học kỹ ở Phần 3.5)
```

Đây là lý do đơn giản nhất, dễ hiểu nhất để giải thích cho người mới: **inline style tạo Object mới mỗi lần vẽ lại màn hình, còn `StyleSheet.create` chỉ tạo đúng 1 lần rồi dùng đi dùng lại**. Phần "bản chất nâng cao" ngay bên dưới (mục 1-3) sẽ đào sâu thêm lý do kỹ thuật đằng sau điều này.

> [!NOTE]
> **Xem trước Design System:** Trong file mẫu ở mục C, các màu như `'red'`, `'#2C3E50'`, `'#F5F5F5'` đang được viết "cứng" (hardcode) trực tiếp. Đây là cách làm tạm thời để bạn tập trung học cú pháp `StyleSheet` trước. Ở phần **THỰC CHIẾN SHOPAI (Sprint 3)** cuối chương này, bạn sẽ thay toàn bộ các giá trị hardcode đó bằng hằng số tập trung khai báo trong `theme.ts` (VD: `COLORS.primary` thay cho `'red'`, `COLORS.text` thay cho `'#2C3E50'`) — đây chính là bước đầu tiên hiện thực hoá triết lý **Design System** đã học ở Phần 3.1, giúp đổi màu toàn app chỉ bằng **1 dòng code duy nhất**.

---

React Native không sử dụng CSS thuần (không có class, không có id, không có pseudo-class như `:hover`). Mọi style đều là các Object JavaScript.

### 1. Tại sao KHÔNG NÊN dùng Inline Styles?

Inline Styles là việc khai báo style trực tiếp vào thẻ JSX:

```tsx
// ❌ KHÔNG KHUYẾN KHÍCH TRONG DỰ ÁN LỚN
<View style={{ backgroundColor: "red", padding: 10, borderRadius: 5 }}>
  <Text>Nút bấm</Text>
</View>
```

**Tại sao nó tệ?**
Mỗi khi Component bị Re-render (ví dụ có State thay đổi), JavaScript sẽ phải **tạo ra một Object mới hoàn toàn** trong bộ nhớ RAM (`{ backgroundColor: 'red', ... }`), sau đó chuyển Object này thành chuỗi JSON, nhét qua The Bridge để gửi sang Native Thread yêu cầu vẽ lại. Việc tạo Object mới và gửi qua cầu liên tục làm hao tổn RAM và CPU cực kỳ nghiêm trọng.

### 2. Sức mạnh ngầm của `StyleSheet.create`

Bạn bắt buộc phải dùng `StyleSheet.create()` để định nghĩa style bên ngoài Component:

```tsx
// ✅ CHUẨN ENTERPRISE
import { StyleSheet, View, Text } from "react-native";

const MyButton = () => {
  return (
    <View style={styles.buttonContainer}>
      <Text>Nút bấm</Text>
    </View>
  );
};

// Định nghĩa bên ngoài Component
const styles = StyleSheet.create({
  buttonContainer: {
    backgroundColor: "red",
    padding: 10,
    borderRadius: 5,
  },
});
```

**Under the hood (Bản chất — đã cập nhật, đính chính hiểu lầm phổ biến):**
Nhiều tài liệu cũ lan truyền một huyền thoại rằng `StyleSheet.create` gán cho mỗi style một "ID số nguyên" rồi gửi ID đó qua The Bridge để tiết kiệm băng thông. **Điều này không đúng với cách RN hiện đại hoạt động** — hãy quên huyền thoại "Bridge ID" này đi.

**Lý do thật sự `StyleSheet.create` nhanh hơn Inline Style:**

1. **Object tham chiếu ổn định (Stable Reference):** Vì bạn khai báo `styles` **bên ngoài** Component, object đó chỉ được tạo **một lần** khi file được load, không phải tạo lại mỗi lần Component render. Ngược lại, `style={{ ... }}` viết trực tiếp trong JSX sẽ tạo một Object JS **mới toanh** ở mỗi lần render.
2. **Hỗ trợ so sánh trong `React.memo`:** Vì tham chiếu object ổn định, các cơ chế tối ưu như `React.memo`/`useMemo` (Phần 3.5) mới có thể so sánh "style trước và style sau có giống nhau không" một cách rẻ và chính xác. Nếu style là object mới mỗi lần render, mọi so sánh tham chiếu đều thất bại, `React.memo` gần như vô dụng.
3. **Validate & "đóng băng" ở môi trường DEV:** `StyleSheet.create` chạy `Object.freeze` lên từng style object trong môi trường phát triển, giúp bắt lỗi sớm nếu bạn vô tình gán đè giá trị style — một dạng kiểm tra an toàn, không liên quan gì đến việc "gửi ID qua Bridge".
4. **Với New Architecture (Fabric + JSI):** Ở kiến trúc mới mà ShopAI đang dùng, không còn khái niệm serialize style thành JSON để gửi qua The Bridge nữa — JS và Native giao tiếp qua bộ nhớ chia sẻ (JSI). Câu chuyện "ID số nguyên qua cầu" thuộc về một thời kỳ khác và không phản ánh đúng cơ chế hiện tại.

> **Tóm lại:** `StyleSheet.create` nhanh hơn không phải vì "gửi số ID qua cầu", mà vì nó giữ style **ổn định tham chiếu, tạo đúng 1 lần, nằm ngoài vòng lặp render** — đúng tinh thần tối ưu Re-render mà cả chương này theo đuổi.

### 3. Xu hướng Style 2025–2026: NativeWind & Unistyles (Nhận biết để đi phỏng vấn)

`StyleSheet.create` là **nền tảng bắt buộc phải học trước** — nó dạy bạn hiểu đúng bản chất Object style, Re-render, và cách RN thật sự vẽ giao diện. Nhưng ngoài đời, 2 xu hướng sau đang được nhiều đội Enterprise áp dụng để viết style nhanh hơn:

- **NativeWind:** Mang cú pháp Tailwind CSS (`className="bg-red-500 p-4 rounded-xl"`) vào React Native. Ở dưới, NativeWind vẫn compile ra đúng Object `StyleSheet` — nó chỉ là một lớp "dịch cú pháp" tiện lợi, không phải một cơ chế render mới.
- **Unistyles 3:** Thư viện style hiệu năng cao, cho phép style tự động đổi theo Theme (Sáng/Tối) và Breakpoint (Tablet/Phone) mà **không cần Re-render Component** — nó cập nhật trực tiếp ở Native Thread qua JSI, nhanh hơn cách đổi State + Context truyền thống.

```tsx
// Ví dụ KHÁI NIỆM (conceptual) — cú pháp Unistyles 3, KHÔNG cần cài vào ShopAI
import { StyleSheet } from "react-native-unistyles";

const styles = StyleSheet.create((theme) => ({
  button: {
    backgroundColor: theme.colors.primary, // Tự đổi theo Theme, không cần useTheme()/Re-render
    padding: theme.gap(2),
    borderRadius: 12,
  },
}));
```

> [!NOTE]
> **ShopAI KHÔNG bắt buộc chuyển sang NativeWind/Unistyles** — dự án thực chiến của khóa học tiếp tục dùng `StyleSheet.create` xuyên suốt để bạn nắm chắc nền tảng. Biết 2 cái tên này để tự tin trả lời khi nhà tuyển dụng hỏi "Bạn biết style hiện đại nào ngoài StyleSheet không?".

> [!TIP]
> **Accessibility nhỏ mà quan trọng:** `Pressable`/`ShopButton` nên có prop `accessibilityLabel` để phần mềm đọc màn hình (VoiceOver/TalkBack) đọc đúng tên nút cho người khiếm thị, thay vì im lặng hoặc đọc nhầm nội dung con bên trong. Ở Sprint 3 (Bước 4), ta sẽ thêm prop `accessibilityLabel` (tùy chọn) vào `ShopButton` — mặc định lấy luôn giá trị `title` nếu không truyền riêng.

---

## 🔗 PHẦN 3.3: HOOKS ĐỀ CƯƠNG — `useContext` & `useReducer` (VÀ ÔN TẬP `useState`/`useEffect`)

### 0. Bản đồ Hooks của khóa học

Đến đây bạn đã đi qua:

- **Chương 1–2:** `useState` (lưu dữ liệu đổi theo thời gian, tự động vẽ lại UI khi đổi) và `useEffect` (chạy code phụ khi Component mount/update — gọi API, đăng ký sự kiện, dọn dẹp timer...).
- **Chương 3 (chương này):** Bổ sung 2 Hook còn thiếu trong đề cương — `useContext` (chia sẻ dữ liệu toàn cục, không cần truyền Props qua từng tầng) và `useReducer` (quản lý State phức tạp bằng mô hình Action/Reducer) — cộng thêm `useMemo`/`useCallback` (tối ưu render, học ở Phần 3.5).

| Hook                      | Dùng để làm gì                                                              | Học ở đâu           |
| ------------------------- | --------------------------------------------------------------------------- | ------------------- |
| `useState`                | Lưu 1 giá trị đơn giản, tự re-render khi đổi                                | Chương 1–2          |
| `useEffect`               | Chạy side-effect (gọi API, timer, subscription)                             | Chương 1–2          |
| `useContext`              | Đọc dữ liệu từ 1 Provider cha, không cần truyền Props qua từng tầng         | Chương 3 (mục này)  |
| `useReducer`              | Quản lý State phức tạp bằng Action + Reducer, thay nhiều `useState` rời rạc | Chương 3 (mục này)  |
| `useMemo` / `useCallback` | Ghi nhớ giá trị/hàm để chặn Re-render thừa                                  | Chương 3 (Phần 3.5) |
| Zustand _(xem trước)_     | Global State ngoài React, chỉ re-render đúng nơi cần                        | Chương 6            |

### 1. `useContext` — Chia sẻ dữ liệu toàn cục (chống Prop Drilling bản nhẹ)

Giả sử ShopAI muốn hỗ trợ 2 giao diện: Sáng (Light) và Tối (Dark). Nếu không có Context, bạn phải truyền `theme` xuống qua từng Component con theo từng tầng — gọi là **Prop Drilling** (sẽ phân tích kỹ và so sánh với Zustand ở Chương 6).

**Bước 1 — Tạo Context** (`src/contexts/ThemeContext.tsx`):

```tsx
import React, { createContext, useContext, useState, ReactNode } from "react";

const LIGHT_COLORS = {
  background: "#F5F5F5",
  text: "#2C3E50",
  surface: "#FFFFFF",
};
const DARK_COLORS = {
  background: "#121212",
  text: "#F5F5F5",
  surface: "#1E1E1E",
};

interface ThemeContextValue {
  isDark: boolean;
  colors: typeof LIGHT_COLORS;
  toggleTheme: () => void;
}

// 1. Tạo "cái hộp" Context — giá trị mặc định undefined, chỉ dùng khi thiếu Provider
const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

// 2. Provider — đứng ở gốc cây Component, "phát sóng" dữ liệu xuống mọi Con bên dưới
export const ThemeProvider = ({ children }: { children: ReactNode }) => {
  const [isDark, setIsDark] = useState(false);

  const value: ThemeContextValue = {
    isDark,
    colors: isDark ? DARK_COLORS : LIGHT_COLORS,
    toggleTheme: () => setIsDark((prev) => !prev),
  };

  return (
    <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
  );
};

// 3. Custom Hook tiện dụng — gọn hơn việc gọi useContext(ThemeContext) ở mọi nơi
export const useTheme = () => {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error("useTheme phải được gọi bên trong <ThemeProvider>");
  return ctx;
};
```

**Bước 2 — Bọc App bằng Provider** (`App.tsx`):

> Import dùng alias `@contexts` (đã thêm vào `babel.config.js`/`tsconfig.json` từ Chương 2). Nếu project của bạn chưa có alias này, dùng đường dẫn tương đối `../contexts/ThemeContext` thay thế.

```tsx
import { SafeAreaProvider } from "react-native-safe-area-context";
import { ThemeProvider } from "@contexts/ThemeContext";
import HomeScreen from "@screens/HomeScreen";

function App() {
  // Chưa cài React Navigation (chỉ có từ Chương 5) nên ThemeProvider chỉ bọc trực tiếp
  // HomeScreen — không cần NavigationContainer ở bước này.
  return (
    <SafeAreaProvider>
      <ThemeProvider>
        {/* Mọi Component con của HomeScreen đều "nghe" được Theme, không cần truyền Props */}
        <HomeScreen />
      </ThemeProvider>
    </SafeAreaProvider>
  );
}
```

**Bước 3 — Dùng ở bất kỳ Component con nào, dù nằm sâu bao nhiêu tầng:**

```tsx
import { useTheme } from "@contexts/ThemeContext";

const SettingsScreen = () => {
  const { isDark, colors, toggleTheme } = useTheme(); // Không cần nhận Props theme!
  return (
    <View style={{ backgroundColor: colors.background }}>
      <Text style={{ color: colors.text }}>
        Chế độ hiện tại: {isDark ? "Tối" : "Sáng"}
      </Text>
      <ShopButton title="Đổi giao diện" onPress={toggleTheme} />
    </View>
  );
};
```

> [!WARNING]
> **Cạm bẫy Re-render của Context:** Khi giá trị trong Provider đổi (VD: gọi `toggleTheme`), **TẤT CẢ** Component con đang gọi `useContext` (dù chỉ dùng 1 trường rất nhỏ trong đó) đều bị Re-render — Context KHÔNG có cơ chế lọc theo trường như Zustand (Chương 6). Vì vậy `useContext` hợp với dữ liệu ít thay đổi (Theme, Ngôn ngữ, User đăng nhập), KHÔNG hợp với dữ liệu đổi liên tục (VD: vị trí cuộn, giá trị real-time).

### 2. `useReducer` — Khi State phức tạp hơn 1 biến

`useState` rất hợp với 1 giá trị đơn giản (`count`, `text`...). Nhưng khi 1 màn hình có nhiều giá trị State liên quan chặt với nhau, cùng bị thay đổi bởi nhiều "hành động" khác nhau (Ví dụ Giỏ hàng: thêm, xoá, đổi số lượng), gọi liên tiếp nhiều `setState` rời rạc dễ làm logic rối rắm và khó kiểm thử.

`useReducer` mang tư duy Redux vào 1 Hook: bạn viết 1 hàm thuần `reducer(state, action)` xử lý toàn bộ logic thay đổi State, Component chỉ cần "bắn" (`dispatch`) hành động lên — không tự tay sửa State.

**Ví dụ: Giỏ hàng mini (cart-lite reducer) với action `ADD`/`REMOVE`:**

```tsx
import React, { useReducer } from "react";
import { View, Text } from "react-native";
import ShopButton from "@components/ShopButton";

interface CartItem {
  id: string;
  name: string;
  qty: number;
}
type CartState = CartItem[];
type CartAction =
  | { type: "ADD"; payload: { id: string; name: string } }
  | { type: "REMOVE"; payload: { id: string } };

// Hàm thuần (pure function): nhận State cũ + Action -> trả về State MỚI, không sửa trực tiếp state cũ
function cartReducer(state: CartState, action: CartAction): CartState {
  switch (action.type) {
    case "ADD": {
      const existing = state.find((i) => i.id === action.payload.id);
      if (existing) {
        // Đã có trong giỏ -> tăng số lượng
        return state.map((i) =>
          i.id === action.payload.id ? { ...i, qty: i.qty + 1 } : i,
        );
      }
      // Chưa có -> thêm item mới với qty = 1
      return [...state, { ...action.payload, qty: 1 }];
    }
    case "REMOVE":
      return state.filter((i) => i.id !== action.payload.id);
    default:
      return state;
  }
}

const CartDemo = () => {
  // dispatch: hàm "bắn" Action lên reducer, thay cho việc gọi nhiều setState rời rạc
  const [cart, dispatch] = useReducer(cartReducer, []);

  return (
    <View>
      <Text>Số món trong giỏ: {cart.length}</Text>
      <ShopButton
        title="Thêm iPhone"
        onPress={() =>
          dispatch({ type: "ADD", payload: { id: "ip15", name: "iPhone 15" } })
        }
      />
      <ShopButton
        title="Xoá iPhone"
        onPress={() => dispatch({ type: "REMOVE", payload: { id: "ip15" } })}
      />
    </View>
  );
};
```

### 3. Bảng so sánh: `useState` vs `useReducer` vs Zustand (xem trước Chương 6)

| Tiêu chí          | `useState`                        | `useReducer`                                                     | Zustand _(Chương 6)_                                       |
| ----------------- | --------------------------------- | ---------------------------------------------------------------- | ---------------------------------------------------------- |
| Hợp cho           | 1 giá trị đơn giản                | Nhiều giá trị liên quan, nhiều Action                            | Dữ liệu Global (Auth, Cart) cần dùng ở nhiều màn hình      |
| Phạm vi           | Nội bộ 1 Component                | Nội bộ 1 Component (hoặc kèm Context để chia sẻ)                 | Toàn App, không cần Provider bọc ngoài                     |
| Logic thay đổi    | Viết rải rác ở nơi gọi `setState` | Tập trung 1 chỗ trong hàm `reducer` (dễ test, dễ log lại Action) | Viết trong file Store, gọi trực tiếp không qua Props       |
| Re-render khi đổi | Chỉ Component chứa State          | Chỉ Component chứa State (trừ khi đưa qua Context)               | Chỉ Component thực sự dùng đúng phần dữ liệu đó (Selector) |
| Ví dụ điển hình   | Ô input, toggle 1 nút             | Giỏ hàng mini, Form nhiều bước, State máy (Wizard)               | Token đăng nhập, Giỏ hàng thật của ShopAI                  |

> [!TIP]
> Một pattern rất phổ biến ở dự án thật: **Context + `useReducer`** (thay `useState` bên trong Provider bằng `useReducer` khi Store nội bộ có nhiều Action) — đây chính là "Redux thu nhỏ" dùng thuần React, không cần cài thêm thư viện. Tuy nhiên khi ứng dụng lớn dần (nhiều Store, cần DevTools, Persist xuống bộ nhớ máy, tránh Re-render tràn lan như đã cảnh báo ở mục 1), Chương 6 sẽ giới thiệu **Zustand** để thay thế gọn nhẹ và hiệu năng cao hơn.

---

## 🧠 PHẦN 3.4: CUSTOM HOOKS - NGHỆ THUẬT TÁCH RỜI LOGIC VÀ UI

Khi màn hình của bạn dài đến 500 dòng code, trong đó 300 dòng là logic xử lý sự kiện (API, form validation) và 200 dòng là giao diện JSX. File sẽ trở thành một mớ hỗn độn không thể bảo trì.
**Custom Hook** là một hàm JS bắt đầu bằng chữ `use` (ví dụ `useLogin`), cho phép bạn "bốc" toàn bộ 300 dòng logic ra một file riêng.

### Ví dụ về Custom Hook: Đếm ngược thời gian (Countdown)

**Bình thường (Logic dính chặt với UI - Khó đọc):**

```tsx
const SaleBanner = () => {
  const [timeLeft, setTimeLeft] = useState(60);

  useEffect(() => {
    const timer = setInterval(() => {
      setTimeLeft((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);
    return () => clearInterval(timer);
  }, []);

  return <Text>Giảm giá kết thúc sau: {timeLeft}s</Text>;
};
```

**Clean Architecture (Dùng Custom Hook - Đẳng cấp):**

_Bước 1: Tắt logic ra file riêng `hooks/useCountdown.ts`_

```ts
import { useState, useEffect } from "react";

// Hàm Custom Hook
export const useCountdown = (initialSeconds: number) => {
  const [timeLeft, setTimeLeft] = useState(initialSeconds);

  useEffect(() => {
    if (timeLeft <= 0) return;
    const timer = setInterval(() => {
      setTimeLeft((prev) => prev - 1);
    }, 1000);
    return () => clearInterval(timer);
  }, [timeLeft]);

  // Trả về dữ liệu cần thiết cho UI
  return { timeLeft, isFinished: timeLeft === 0 };
};
```

_Bước 2: Giao diện chỉ tập trung vào việc hiển thị_

```tsx
import { useCountdown } from "@hooks/useCountdown";

const SaleBanner = () => {
  // Component sạch sẽ, chỉ chứa đúng 1 dòng logic!
  const { timeLeft, isFinished } = useCountdown(60);

  if (isFinished) return <Text>Đã hết hạn khuyến mãi!</Text>;
  return <Text>Giảm giá kết thúc sau: {timeLeft}s</Text>;
};
```

---

## ⚡ PHẦN 3.5: NGHỆ THUẬT TỐI ƯU RE-RENDER (`React.memo`, `useMemo`, `useCallback`)

Re-render (Vẽ lại) là bản chất của React. Mỗi khi State của Component Cha thay đổi, toàn bộ các Component Con nằm trong nó đều bị ép vẽ lại từ đầu, dù Props của Con chẳng thay đổi gì.
Tuy nhiên, nếu Component Con quá nặng (chứa 1000 tấm ảnh), việc vẽ lại vô nghĩa này sẽ làm đứng máy. Ta cần các kỹ thuật "Ghi nhớ" (Memoization).

### 1. `React.memo` (Cái khiên bảo vệ Component)

`React.memo` bọc bên ngoài Component Con. Nó báo cho React biết: _"Này, nếu Props tôi nhận vào không bị đổi giá trị, thì cấm không được bắt tôi Re-render, dù cho Component Cha có bị Re-render đi chăng nữa!"_.

```tsx
// Component con bị ép Re-render liên tục nếu không có React.memo
const HeavyProductList = React.memo(({ products }) => {
  console.log("Đang vẽ lại danh sách nặng nề...");
  return <View>...</View>;
});
```

### 2. Sự phản bội của Object/Function và `useCallback`, `useMemo`

Kẻ thù lớn nhất của `React.memo` là biến dạng tham chiếu (Reference Type: Object, Array, Function).

Trong JavaScript, `[1, 2] === [1, 2]` sẽ trả về `false`. Mặc dù ruột giống nhau, nhưng chúng là 2 ô nhớ khác nhau trong RAM.
Nếu Cha truyền một Function `onPress={() => {}}` xuống cho Con. Mỗi lần Cha re-render, nó lại sinh ra một cái Function mới toanh (ô nhớ mới). Con kiểm tra thấy Props bị đổi ô nhớ -> React.memo bị xuyên thủng -> Con vẫn Re-render!

**Giải pháp 1: `useCallback` (Ghi nhớ hàm)**
`useCallback` khóa chặt hàm lại, không cho tạo hàm mới ở mỗi lần render, giúp bảo vệ `React.memo` của Con.

```tsx
const Parent = () => {
  const [count, setCount] = useState(0);

  // Khóa hàm này lại, chỉ tạo lại nếu `id` thay đổi
  const handleAddToCart = useCallback((id) => {
    console.log("Thêm vào giỏ", id);
  }, []);

  return (
    <View>
      <Text>{count}</Text>
      <Button onPress={() => setCount(count + 1)} title="Tăng số" />
      {/* HeavyProductList giờ đây an toàn, không bị re-render khi bấm Tăng số */}
      <HeavyProductList onAdd={handleAddToCart} />
    </View>
  );
};
```

**Giải pháp 2: `useMemo` (Ghi nhớ giá trị tính toán nặng)**
Chặn không cho máy tính chạy lại các vòng lặp tính toán nặng nề nếu dữ liệu đầu vào không đổi.

```tsx
const Parent = ({ users }) => {
  // Giả sử mảng users có 1 triệu phần tử.
  // Không dùng useMemo, mỗi lần re-render máy sẽ phải filter lại 1 triệu phần tử cực lag.
  const activeUsers = useMemo(() => {
    return users.filter((u) => u.isActive);
  }, [users]); // Chỉ chạy lại vòng lặp khi mảng users bị thay đổi

  return <UserList data={activeUsers} />;
};
```

> [!CAUTION]
> **Bẫy lạm dụng (Over-memoization):**
> Nhược điểm của `useMemo` và `useCallback` là chúng tốn RAM để lưu trữ dữ liệu/hàm vào bộ đệm, và tốn CPU để so sánh Dependency Array xem có đổi hay không.
> **LUẬT:** Nếu phép tính chỉ là phép cộng trừ nhân chia đơn giản (tốn 0.1 mili-giây) hoặc một hàm `() => console.log()`, việc bọc `useCallback/useMemo` sẽ làm app **CHẬM ĐI** vì chi phí so sánh còn đắt hơn chi phí tạo mới! Chỉ dùng cho vòng lặp ngàn phần tử hoặc truyền xuống Component Con cực nặng.

---

## 🌐 PHẦN 3.6: i18n — ĐA NGÔN NGỮ (GLOBALIZATION)

### 1. Tại sao cần i18n?

Một ứng dụng chuyên nghiệp (như Shopee, Lazada) không bao giờ hardcode (viết cứng) chuỗi văn bản như `"Đăng nhập"`, `"Giỏ hàng"` trực tiếp vào UI. Thay vào đó, chúng ta sử dụng cơ chế **i18n (Internationalization)** để tự động dịch các chuỗi văn bản này tùy theo ngôn ngữ người dùng đã chọn.

### 2. Thư viện chuẩn mực: `i18next` & `react-i18next`

Trong hệ sinh thái React/React Native, `i18next` là thư viện tiêu chuẩn công nghiệp.

- **`i18next`**: Chịu trách nhiệm lưu trữ các file ngôn ngữ (JSON) và logic dịch thuật.
- **`react-i18next`**: Cung cấp hook `useTranslation()` để sử dụng trực tiếp trong Component.

### 3. Cấu trúc thư mục (Best Practice)

```text
src/
└── locales/
    ├── i18n.ts       # Cấu hình khởi tạo
    ├── vi.json       # { "home": { "welcome": "Chào mừng" } }
    └── en.json       # { "home": { "welcome": "Welcome" } }
```

### 4. Sử dụng trong Component

```tsx
import { useTranslation } from "react-i18next";
import { Text, View, Button } from "react-native";

const WelcomeScreen = () => {
  const { t, i18n } = useTranslation();

  const changeLanguage = (lang: string) => {
    i18n.changeLanguage(lang);
  };

  return (
    <View>
      <Text>{t("home.welcome")}</Text>
      <Button title="Tiếng Việt" onPress={() => changeLanguage("vi")} />
      <Button title="English" onPress={() => changeLanguage("en")} />
    </View>
  );
};
```

_Ghi chú: Việc chuyển đổi ngôn ngữ bằng `i18n.changeLanguage` sẽ tự động trigger re-render cho mọi Component đang dùng hook `useTranslation()`._

---

## ✨ PHẦN 3.7: MICRO-ANIMATIONS (LOTTIE) — THỔI HỒN VÀO UI

### 1. Micro-animations là gì?

Micro-animations là các hiệu ứng chuyển động rất nhỏ, tinh tế (ví dụ: nút tim đập thịch khi nhấn like, pháo hoa nổ khi thanh toán thành công, vòng xoay loading vui nhộn). Nó giúp ứng dụng bớt "cứng nhắc" và mang lại trải nghiệm Luxury UI.

### 2. Lottie — Tiêu chuẩn Animation di động

Viết animation bằng code (Animated, Reanimated) rất tốn thời gian. Airbnb đã tạo ra **Lottie** — một thư viện render trực tiếp file JSON xuất ra từ Adobe After Effects.

- Kích thước cực nhỏ (vài chục KB).
- Không bị vỡ nét (dựa trên vector).
- Hiệu năng rất cao trên thiết bị di động.

### 3. Sử dụng `lottie-react-native`

Thư viện này cung cấp component `<LottieView>`.

```tsx
import React, { useRef, useEffect } from "react";
import LottieView from "lottie-react-native";
import { View } from "react-native";

const SuccessScreen = () => {
  const animation = useRef<LottieView>(null);

  useEffect(() => {
    // Tự động play khi vào màn hình
    animation.current?.play();
  }, []);

  return (
    <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
      <LottieView
        ref={animation}
        source={require("../assets/lottie/success.json")}
        autoPlay={true}
        loop={false}
        style={{ width: 200, height: 200 }}
      />
    </View>
  );
};
```

_Lưu ý: Chỉ dùng Lottie cho các hiệu ứng phức tạp. Với các hiệu ứng đơn giản (fade in, trượt), hãy dùng `react-native-reanimated` để nhẹ máy hơn._

---

## 🚀 THỰC CHIẾN SHOPAI (SPRINT 3: XÂY DỰNG DESIGN SYSTEM & UI KIT)

**User Story:** _"Là một Kỹ sư Front-end, tôi muốn xây dựng bộ UI Kit chuẩn mực gồm Typography, ShopInput, PrimaryButton và một Custom Hook dùng chung, để mọi màn hình sau này chỉ việc lắp ghép Atoms thay vì copy-paste CSS."_

### 📋 Khung thực hành chương (đọc trước khi gõ code)

> Đây là **bài thực hành của Chương 3** (không phải “lab mỗi ngày”). Làm hết Sprint này = đạt mục tiêu chương. Hoàn thành đủ 11 Sprint = sản phẩm ShopAI theo `SHOPAI_HOAN_THIEN.md`.

| Hạng mục                 | Nội dung                                                                                         |
| ------------------------ | ------------------------------------------------------------------------------------------------ |
| **Thời lượng gợi ý**     | 4–5 tiết                                                                                         |
| **Độ khó chương**        | ★★★☆☆                                                                                            |
| **Đầu vào bắt buộc**     | Sprint 2 PASS — có HomeScreen + alias.                                                           |
| **Đầu ra sản phẩm**      | UI Kit (Typography, ShopInput, ShopButton+variant) + theme + Dark Mode + useCountdown trên Home. |
| **Cách làm**             | Làm **tuần tự từng Bước**. Gặp mốc ✓ bên dưới mà FAIL → dừng, sửa, rồi mới sang bước sau.        |
| **Nghiệm thu cuối khóa** | Đối chiếu `SHOPAI_HOAN_THIEN.md` — mỗi Sprint chỉ tích thêm ô, không phá tính năng cũ.           |

### ✓ Kiểm chứng theo mốc (trong lúc làm)

- **Sau Bước 1–4:** Đổi `COLORS.primary` → nút/chữ đổi theo theme.
- **Sau Bước 5–6:** Countdown chạy; Home dùng atoms (không style cứng chữ/nút).
- **Sau Bước 7:** Bật/tắt Dark Mode thấy nền/chữ đổi ngay.

> [!TIP]
> Xong Sprint 3, mở `SHOPAI_HOAN_THIEN.md` và tick các ô thuộc chương này. Mục tiêu cuối khóa: **mọi ô A/B/C/D (+ E đề cương) đều xanh** trong `SHOPAI_HOAN_THIEN.md` — đó mới là ShopAI hoàn thiện đẳng cấp.

### Yêu cầu Nghiệm thu (Acceptance Criteria):

1. Có file `theme.ts` (COLORS + SIZES + FONTS).
2. Có 3 atoms: `Typography`, `ShopInput`, `ShopButton` (đều dùng `StyleSheet` + `memo` khi phù hợp).
3. Có Custom Hook `useCountdown` và demo trên HomeScreen.
4. HomeScreen dùng lại UI Kit (không viết style cứng cho chữ/nút/ô nhập).
5. Có `ThemeContext` (`src/contexts/ThemeContext.tsx`) thật, bọc App bằng `ThemeProvider`, HomeScreen có nút bấm chuyển "Sáng/Tối" đổi màu nền + màu chữ ngay lập tức.
6. Cấu hình thành công **i18next** và có nút chuyển ngôn ngữ Anh/Việt.
7. Hiển thị ít nhất một hiệu ứng **Lottie** (ví dụ: Lottie Loading hoặc Success).
8. _(Tuỳ chọn — áp dụng lý thuyết Phần 3.3)_ Có 1 demo nhỏ dùng `useReducer` (bộ đếm số lượng sản phẩm với action `ADD`/`REMOVE`) trên HomeScreen.

### Hướng dẫn thực thi Step-by-Step:

## 🏗️ Kiến trúc khối Design System ShopAI

Trước khi viết bất kỳ dòng code nào, hãy hình dung **luồng phụ thuộc** giữa các khối bạn sắp tạo — đây chính là cách áp dụng Atomic Design (Phần 3.1) vào thực tế ShopAI:

```
theme.ts (COLORS / SIZES / FONTS)
    ↓
Typography   ShopInput   ShopButton     (atoms — nằm trong src/components/ui, src/components)
    ↓
HomeScreen / ProductCard                (compose nhiều atoms lại thành 1 màn hình)
```

**Đọc sơ đồ này như thế nào?**

1. **`theme.ts`** là tầng thấp nhất — chỉ chứa hằng số thuần túy (chuỗi màu, số pixel), **không** import bất kỳ Component nào. Mọi atom phía trên đều `import { COLORS, SIZES, FONTS } from '@constants/theme'`.
2. **Atoms** (`Typography`, `ShopInput`, `ShopButton`) là các Component nhỏ nhất, tự thân **không có ý nghĩa nghiệp vụ** (không biết gì về "sản phẩm" hay "giỏ hàng") — chúng chỉ biết cách hiển thị chữ/ô nhập/nút bấm **đúng chuẩn theme**. Mỗi atom import `theme.ts`, atom nào cần hiển thị chữ (`ShopInput`, `ShopButton`) thì import thêm `Typography`.
3. **Tầng compose** (`HomeScreen`, và `ProductCard` ở các chương sau) không viết `StyleSheet` cho màu chữ/nút từ đầu nữa — chỉ **lắp ghép** các atoms lại và truyền Props nghiệp vụ (`title="Xác nhận thanh toán"`, `label="Mã giảm giá"`).

**Vì sao kiến trúc 1 chiều (mũi tên chỉ xuống) lại quan trọng?**

- `theme.ts` đổi 1 giá trị (VD: `COLORS.primary`) → mọi atom dùng `COLORS.primary` tự đổi theo → mọi màn hình dùng atom đó tự đổi theo. **Không có chiều ngược lại**: atom không được phép ảnh hưởng lên `theme.ts`, `HomeScreen` không được sửa trực tiếp bên trong `ShopButton`.
- Đây chính là cách giải quyết vấn đề nêu ở Phần 3.1 mục 1 ("đổi 10 file khi khách yêu cầu đổi màu nút") — với kiến trúc này, bạn chỉ sửa **đúng 1 dòng** trong `theme.ts`.

#### Bước 1: Định nghĩa Hệ sinh thái Hằng số (Constants)

Trong thư mục `src/constants/`, tạo file `theme.ts`:

```typescript
// src/constants/theme.ts
export const COLORS = {
  primary: "#FF4D4F",
  secondary: "#1890FF",
  background: "#F5F5F5",
  surface: "#FFFFFF",
  text: "#2C3E50",
  textLight: "#7F8C8D",
  border: "#E8E8E8",
  error: "#FF0000",
  success: "#52C41A",
};

export const SIZES = {
  base: 8,
  font: 14,
  radius: 12,
  padding: 16,
  h1: 24,
  h2: 20,
  h3: 18,
  body1: 16,
  body2: 14,
  small: 12,
};

/** Map variant chữ → fontSize / fontWeight (dùng cho Typography) */
export const FONTS = {
  h1: { fontSize: SIZES.h1, fontWeight: "700" as const },
  h2: { fontSize: SIZES.h2, fontWeight: "700" as const },
  h3: { fontSize: SIZES.h3, fontWeight: "600" as const },
  body1: { fontSize: SIZES.body1, fontWeight: "400" as const },
  body2: { fontSize: SIZES.body2, fontWeight: "400" as const },
  small: { fontSize: SIZES.small, fontWeight: "400" as const },
};
```

> **Custom Fonts (tùy chọn nâng cao):** Nếu muốn dùng font riêng (VD: Inter), bỏ file `.ttf` vào `src/assets/fonts/`, khai báo trong `react-native.config.js`, chạy `npx react-native-asset`, rồi thêm `fontFamily: 'Inter-Regular'` vào `FONTS`. Sprint bắt buộc chỉ cần system font qua `FONTS` ở trên.

#### Bước 2: Atom Typography

Tạo `src/components/ui/Typography.tsx`:

```tsx
import React, { memo } from "react";
import { Text, TextStyle, StyleProp } from "react-native";
import { COLORS, FONTS } from "@constants/theme";

type Variant = keyof typeof FONTS;

interface Props {
  children: React.ReactNode;
  variant?: Variant;
  color?: string;
  style?: StyleProp<TextStyle>;
  numberOfLines?: number;
}

const Typography = ({
  children,
  variant = "body1",
  color = COLORS.text,
  style,
  numberOfLines,
}: Props) => {
  return (
    <Text
      numberOfLines={numberOfLines}
      style={[FONTS[variant], { color }, style]}
    >
      {children}
    </Text>
  );
};

export default memo(Typography);
```

**Giải thích kiến trúc & từng props:**

| Khối / Props                                       | Ý nghĩa                                                                                                                                                                                                                                                                                                                                                                              |
| -------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `import { COLORS, FONTS } from '@constants/theme'` | `Typography` **phụ thuộc trực tiếp** vào tầng `theme.ts` (đúng chiều mũi tên trong sơ đồ kiến trúc) — không hardcode `fontSize`/màu ngay trong component                                                                                                                                                                                                                             |
| `type Variant = keyof typeof FONTS`                | Lấy tự động các key có sẵn trong `FONTS` (`h1`, `h2`, `body1`...) làm kiểu cho prop `variant` — thêm 1 variant mới trong `theme.ts` thì `Typography` tự động "biết" luôn, không cần sửa gì ở đây                                                                                                                                                                                     |
| `children: React.ReactNode`                        | Nội dung chữ nằm giữa `<Typography>...</Typography>`, giống hệt `children` của `<Text>` gốc                                                                                                                                                                                                                                                                                          |
| `variant = 'body1'`                                | Giá trị mặc định — gọi `<Typography>` mà không truyền `variant` vẫn có style hợp lý, không bị vỡ layout                                                                                                                                                                                                                                                                              |
| `color = COLORS.text`                              | Mặc định lấy màu chữ chuẩn từ theme; nơi gọi có thể ghi đè bằng màu khác (VD: `COLORS.error` khi hiển thị lỗi)                                                                                                                                                                                                                                                                       |
| `style={[FONTS[variant], { color }, style]}`       | Style RN chấp nhận **mảng** nhiều object, object sau đè object trước — thứ tự này đảm bảo `style` do nơi gọi truyền vào luôn được ưu tiên cao nhất                                                                                                                                                                                                                                   |
| `export default memo(Typography)`                  | **Vì sao dùng `memo`?** `Typography` sẽ được dùng lặp lại **rất nhiều lần** trên 1 màn hình (mỗi dòng chữ giá, tên sản phẩm...) — nếu Cha (VD: `HomeScreen`) re-render vì 1 lý do không liên quan (gõ ô input khác), `memo` chặn không cho các `Typography` khác vẽ lại nếu Props (`variant`, `color`, `children`...) của chúng không đổi. Xem lại lý thuyết `React.memo` ở Phần 3.5 |

#### Bước 3: Atom ShopInput

Tạo `src/components/ui/ShopInput.tsx`:

```tsx
import React, { memo } from "react";
import {
  View,
  TextInput,
  StyleSheet,
  TextInputProps,
  ViewStyle,
} from "react-native";
import Typography from "./Typography";
import { COLORS, SIZES } from "@constants/theme";

interface Props extends TextInputProps {
  label?: string;
  error?: string;
  containerStyle?: ViewStyle;
}

const ShopInput = ({ label, error, containerStyle, style, ...rest }: Props) => {
  return (
    <View style={[styles.wrap, containerStyle]}>
      {label ? (
        <Typography variant="body2" style={styles.label}>
          {label}
        </Typography>
      ) : null}
      <TextInput
        placeholderTextColor={COLORS.textLight}
        style={[styles.input, error ? styles.inputError : null, style]}
        {...rest}
      />
      {error ? (
        <Typography variant="small" color={COLORS.error} style={styles.error}>
          {error}
        </Typography>
      ) : null}
    </View>
  );
};

const styles = StyleSheet.create({
  wrap: { marginBottom: SIZES.padding },
  label: { marginBottom: 6 },
  input: {
    height: 48,
    borderWidth: 1,
    borderColor: COLORS.border,
    borderRadius: SIZES.radius,
    paddingHorizontal: SIZES.padding,
    backgroundColor: COLORS.surface,
    fontSize: SIZES.body1,
    color: COLORS.text,
  },
  inputError: { borderColor: COLORS.error },
  error: { marginTop: 4 },
});

export default memo(ShopInput);
```

**Giải thích kiến trúc & từng props:**

| Khối / Props                                         | Ý nghĩa                                                                                                                                                                                                                                                                            |
| ---------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `interface Props extends TextInputProps`             | `ShopInput` **kế thừa toàn bộ** props gốc của `TextInput` (`placeholder`, `value`, `onChangeText`, `keyboardType`...) rồi bổ sung thêm 3 props riêng (`label`, `error`, `containerStyle`) — nhờ vậy `ShopInput` dùng được ở mọi nơi `TextInput` dùng được, không mất tính năng nào |
| `label?: string`                                     | Tùy chọn (dấu `?`) — có nhãn phía trên ô nhập (VD: "Mã giảm giá"); không truyền thì ẩn hẳn dòng label (nhờ `label ? <Typography>...</Typography> : null`)                                                                                                                          |
| `error?: string`                                     | Tùy chọn — hiển thị dòng chữ đỏ cảnh báo bên dưới ô nhập **và** đổi viền ô sang màu đỏ (`error ? styles.inputError : null`)                                                                                                                                                        |
| `{...rest}` trong `<TextInput {...rest} />`          | "Trải" toàn bộ props còn lại (không phải `label`/`error`/`containerStyle`/`style`) thẳng xuống `TextInput` gốc — đây là kỹ thuật kế thừa Props phổ biến khi bọc (wrap) một Component có sẵn                                                                                        |
| `<Typography variant="body2">` bên trong `ShopInput` | Đúng chiều kiến trúc: atom `ShopInput` được phép dùng atom `Typography` (cùng tầng "atoms"), không lặp lại code style chữ                                                                                                                                                          |
| `StyleSheet.create({...})` đặt **ngoài** `ShopInput` | Object `styles` chỉ tạo **một lần duy nhất** khi file được nạp (không phải mỗi lần gõ chữ vào ô input lại tạo object mới) — giữ tham chiếu ổn định để `memo` phía dưới hoạt động đúng (xem lại Phần 3.2 mục 2)                                                                     |
| `export default memo(ShopInput)`                     | Ngăn `ShopInput` bị vẽ lại nếu Cha re-render vì lý do khác (VD: đồng hồ đếm ngược `useCountdown` tick mỗi giây ở Bước 5) trong khi Props của ô input này không đổi                                                                                                                 |

#### Bước 4: Atom ShopButton (Primary)

Tạo `src/components/ShopButton.tsx` (hoặc `src/components/ui/ShopButton.tsx` rồi re-export):

```tsx
// src/components/ShopButton.tsx
import React, { memo } from "react";
import {
  TouchableOpacity,
  StyleSheet,
  ActivityIndicator,
  ViewStyle,
  TextStyle,
} from "react-native";
import Typography from "@components/ui/Typography";
import { COLORS, SIZES } from "@constants/theme";

interface ShopButtonProps {
  title: string;
  onPress: () => void;
  isLoading?: boolean;
  disabled?: boolean;
  style?: ViewStyle;
  textStyle?: TextStyle;
  accessibilityLabel?: string; // Tuỳ chọn — xem note Accessibility ở Phần 3.2 mục 3
}

const ShopButton: React.FC<ShopButtonProps> = ({
  title,
  onPress,
  isLoading = false,
  disabled = false,
  style,
  textStyle,
  accessibilityLabel,
}) => {
  return (
    <TouchableOpacity
      style={[styles.button, disabled && styles.disabledButton, style]}
      onPress={onPress}
      disabled={disabled || isLoading}
      activeOpacity={0.8}
      // Không truyền riêng thì mặc định lấy luôn `title` — màn hình đọc (VoiceOver/TalkBack) luôn có tên nút để đọc
      accessibilityLabel={accessibilityLabel ?? title}
      accessibilityRole="button"
    >
      {isLoading ? (
        <ActivityIndicator color={COLORS.surface} />
      ) : (
        <Typography
          variant="body1"
          color={COLORS.surface}
          style={[{ fontWeight: "600" }, textStyle]}
        >
          {title}
        </Typography>
      )}
    </TouchableOpacity>
  );
};

const styles = StyleSheet.create({
  button: {
    backgroundColor: COLORS.primary,
    height: 48,
    borderRadius: SIZES.radius,
    justifyContent: "center",
    alignItems: "center",
    paddingHorizontal: SIZES.padding,
    width: "100%",
    shadowColor: COLORS.primary,
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.3,
    shadowRadius: 5,
    elevation: 4,
  },
  disabledButton: {
    backgroundColor: COLORS.border,
    shadowOpacity: 0,
    elevation: 0,
  },
});

export default memo(ShopButton);
```

**Giải thích kiến trúc & từng props:**

| Khối / Props                                       | Ý nghĩa                                                                                                                                                                                         |
| -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `title: string`                                    | Chuỗi hiển thị trên nút — **bắt buộc** (không có dấu `?`), vì một nút không có chữ là lỗi thiết kế                                                                                              |
| `onPress: () => void`                              | Hàm xử lý khi bấm — **ShopButton không tự quyết định "bấm thì làm gì"**, nó chỉ gọi lại đúng hàm mà nơi dùng nó truyền vào (xem luồng dữ liệu bên dưới)                                         |
| `isLoading?: boolean`                              | Khi `true` → thay chữ bằng `ActivityIndicator` và tự động khóa nút (gộp vào điều kiện `disabled={disabled \|\| isLoading}`) — tránh user bấm 2 lần khi đang gọi API                             |
| `disabled?: boolean`                               | Khóa nút thủ công (VD: hết giờ khuyến mãi) — đổi cả style (`styles.disabledButton`) lẫn hành vi                                                                                                 |
| `style?: ViewStyle` / `textStyle?: TextStyle`      | Cho phép nơi gọi **ghi đè thêm** style riêng (VD: đổi `backgroundColor` theo Theme ở Bước 7) mà không cần sửa code bên trong `ShopButton`                                                       |
| `accessibilityLabel={accessibilityLabel ?? title}` | Toán tử `??` (nullish coalescing) — nếu không truyền riêng, tự lấy `title` làm nhãn đọc màn hình, đảm bảo nút nào cũng có tên cho VoiceOver/TalkBack (xem Phần 3.2 mục cuối)                    |
| `disabled={disabled \|\| isLoading}`               | Nút bị khóa nếu **1 trong 2** điều kiện đúng — logic gộp 2 lý do khóa nút lại một chỗ duy nhất                                                                                                  |
| `StyleSheet.create` ngoài Component + `memo`       | Cùng lý do như `Typography`/`ShopInput`: giữ style ổn định tham chiếu, và chặn Re-render thừa khi nút này được đặt cạnh các Component khác hay đổi State (ô input gõ chữ, đồng hồ đếm ngược...) |

**Luồng dữ liệu: Cha truyền `title`/`onPress` → `ShopButton` hiển thị & gọi lại**

```
1. HomeScreen (Cha) định nghĩa hàm nghiệp vụ: handleCheckout = () => { ...gọi API thanh toán... }
        ↓
2. Cha gắn hàm đó vào Props onPress khi dựng JSX:
   <ShopButton title="Xác nhận thanh toán" onPress={handleCheckout} isLoading={loading} />
        ↓
3. ShopButton (Con) KHÔNG biết "thanh toán" nghĩa là gì — nó chỉ nhận 1 chuỗi (title) để in chữ
   và 1 hàm (onPress) để gắn vào <TouchableOpacity onPress={onPress}>
        ↓
4. User chạm vào nút → TouchableOpacity tự gọi onPress() → chính là gọi lại handleCheckout() của Cha
        ↓
5. handleCheckout chạy, có thể gọi setLoading(true) → HomeScreen re-render
        ↓
6. ShopButton nhận lại isLoading=true qua Props → tự đổi giao diện sang ActivityIndicator
```

**Bài học kiến trúc:** `ShopButton` là một atom **"ngu" một cách có chủ đích** — nó không chứa bất kỳ logic nghiệp vụ nào (không biết gì về thanh toán, giỏ hàng). Toàn bộ "não bộ" nằm ở Component Cha; `ShopButton` chỉ là lớp vỏ hiển thị + chuyển tiếp sự kiện. Nhờ vậy, cùng một `ShopButton` này có thể dùng cho nút "Đăng nhập", "Thêm vào giỏ", "Xác nhận thanh toán"... chỉ khác nhau ở Props truyền vào.

> [!TIP]
> **Mở rộng `ShopButton` với `variant` (khuyến nghị làm ngay trong Sprint 3).** Nút hành động chính ("Xác nhận thanh toán") và nút phụ ("Huỷ", "Để sau") không nên trông giống hệt nhau — người dùng cần phân biệt ngay đâu là hành động quan trọng nhất màn hình, đâu là lối thoát an toàn. Thêm prop `variant?: 'primary' | 'secondary' | 'outline'` để `ShopButton` tự đổi giao diện, Cha không phải tự viết `style` tay mỗi lần dùng:
>
> ```tsx
> interface ShopButtonProps {
>   title: string;
>   onPress: () => void;
>   isLoading?: boolean;
>   disabled?: boolean;
>   variant?: "primary" | "secondary" | "outline"; // ➕ MỚI — không truyền thì mặc định 'primary'
>   style?: ViewStyle;
>   textStyle?: TextStyle;
>   accessibilityLabel?: string;
> }
>
> const ShopButton: React.FC<ShopButtonProps> = ({
>   title,
>   onPress,
>   isLoading = false,
>   disabled = false,
>   variant = "primary", // ➕ MỚI
>   style,
>   textStyle,
>   accessibilityLabel,
> }) => {
>   // ➕ MỚI: tra đúng style nền + màu chữ theo variant
>   const variantStyle = styles[variant];
>   const textColor = variant === "outline" ? COLORS.primary : COLORS.surface;
>
>   return (
>     <TouchableOpacity
>       // Thứ tự mảng style CHỦ ĐÍCH: layout chung -> màu theo variant -> khoá (disabled) -> style riêng của nơi gọi (ưu tiên cao nhất vì đứng cuối)
>       style={[
>         styles.button,
>         variantStyle,
>         disabled && styles.disabledButton,
>         style,
>       ]}
>       onPress={onPress}
>       disabled={disabled || isLoading}
>       activeOpacity={0.8}
>       accessibilityLabel={accessibilityLabel ?? title}
>       accessibilityRole="button"
>     >
>       {isLoading ? (
>         <ActivityIndicator color={textColor} />
>       ) : (
>         <Typography
>           variant="body1"
>           color={textColor}
>           style={[{ fontWeight: "600" }, textStyle]}
>         >
>           {title}
>         </Typography>
>       )}
>     </TouchableOpacity>
>   );
> };
>
> const styles = StyleSheet.create({
>   button: {
>     /* ...giữ nguyên layout chung như Bước 4... */
>   },
>   disabledButton: {
>     /* ...giữ nguyên như Bước 4... */
>   },
>
>   // ➕ MỚI: ba biến thể — chỉ đổi màu nền/viền, KHÔNG lặp lại layout đã có ở `button`
>   primary: { backgroundColor: COLORS.primary }, // Hành động chính: Thanh toán, Đăng nhập, Xác nhận
>   secondary: { backgroundColor: COLORS.secondary, shadowOpacity: 0 }, // Hành động phụ: Giỏ hàng, Quét mã (Ch.7)
>   outline: {
>     backgroundColor: "transparent",
>     borderWidth: 1.5,
>     borderColor: COLORS.primary,
>     shadowOpacity: 0, // Nút viền rỗng không cần đổ bóng, nhìn đỡ "nặng" hơn nút đặc màu
>   },
> });
> ```
>
> | `variant`              | Dùng khi nào                                                                            | Ví dụ trong ShopAI                                       |
> | ---------------------- | --------------------------------------------------------------------------------------- | -------------------------------------------------------- |
> | `'primary'` (mặc định) | Hành động chính, quan trọng nhất màn hình — mỗi màn hình chỉ nên có **một** nút primary | "Xác nhận thanh toán", "Đăng nhập"                       |
> | `'secondary'`          | Hành động phụ, vẫn quan trọng nhưng không phải trọng tâm                                | "Giỏ hàng", "Quét Mã" (Chương 7)                         |
> | `'outline'`            | Hành động ít quan trọng nhất, hoặc lối thoát an toàn không phá huỷ dữ liệu              | "Huỷ bỏ", "Để sau", "Đăng nhập bằng mật khẩu" (Chương 8) |
>
> Vì `disabledButton` và các `variant` đều nằm trong cùng object `styles`, RN cho phép gộp nhiều style qua mảng `[...]` — style nào đứng sau sẽ ghi đè thuộc tính trùng của style đứng trước. Đây là lý do `style` (props riêng của nơi gọi) luôn phải đặt **cuối cùng** trong mảng.

#### Bước 5: Custom Hook `useCountdown` (áp dụng lý thuyết Phần 3.4)

Tạo `src/hooks/useCountdown.ts`:

```ts
import { useState, useEffect } from "react";

export const useCountdown = (initialSeconds: number) => {
  const [timeLeft, setTimeLeft] = useState(initialSeconds);

  useEffect(() => {
    if (timeLeft <= 0) return;
    const timer = setInterval(() => {
      setTimeLeft((prev) => prev - 1);
    }, 1000);
    return () => clearInterval(timer);
  }, [timeLeft]);

  return { timeLeft, isFinished: timeLeft === 0 };
};
```

**Giải thích kiến trúc Custom Hook — luồng Input → State → Return → UI:**

```
INPUT (tham số truyền vào)
  initialSeconds: number   ──►  VD: useCountdown(60)

STATE (sống BÊN TRONG Hook, KHÔNG lộ ra ngoài)
  const [timeLeft, setTimeLeft] = useState(initialSeconds)
  useEffect(...)  →  mỗi giây tự gọi setTimeLeft(prev => prev - 1)

RETURN (Hook "xuất khẩu" ra đúng những gì UI cần, không hơn)
  return { timeLeft, isFinished: timeLeft === 0 }

UI (Component gọi Hook — CHỈ ĐỌC, không tự đổi số)
  const { timeLeft, isFinished } = useCountdown(60);
  → UI chỉ có nhiệm vụ HIỂN THỊ timeLeft/isFinished, không có setTimeLeft nào lộ ra ngoài
```

**Đọc từng bước:**

1. **Input:** Nơi gọi Hook (`SaleBanner`, hay `HomeScreen` ở Sprint này) truyền vào đúng 1 con số `initialSeconds` — đây là dữ liệu **duy nhất** đi từ ngoài vào trong Hook.
2. **State nội bộ:** `timeLeft` và cơ chế `setInterval` bên trong `useEffect` là "hộp đen" — component gọi Hook **không hề biết** và **không cần biết** có `setInterval` chạy ngầm ở đây. Đây chính là giá trị cốt lõi của Custom Hook: giấu hoàn toàn phần logic phức tạp.
3. **Return:** Hook chỉ trả ra đúng 2 giá trị UI cần: `timeLeft` (số giây còn lại) và `isFinished` (đã hết giờ chưa — tính sẵn bằng `timeLeft === 0` để UI không phải tự so sánh). **Không** trả ra `setTimeLeft` — nếu trả ra, UI có thể tự ý sửa đồng hồ đếm ngược, phá vỡ nguyên tắc "logic nằm trong Hook, UI chỉ hiển thị".
4. **UI chỉ hiển thị:** Component gọi Hook (`const { timeLeft, isFinished } = useCountdown(60)`) không viết bất kỳ dòng `setInterval`/`useEffect` nào nữa — chỉ còn 1 dòng gọi Hook + JSX hiển thị. Muốn đổi cách đếm ngược (VD: đếm theo phút, dừng khi app xuống nền), chỉ sửa **1 file** `useCountdown.ts`, không phải sửa từng màn hình đang dùng nó.

> [!NOTE]
> **Tính liên tục:** Sprint 3 **NÂNG CẤP** `HomeScreen` — giữ nguyên cấu trúc `src/` đã dựng ở Chương 2, chỉ thay phần UI demo (TextInput/FlatList thô) bằng UI Kit (`Typography`, `ShopInput`, `ShopButton`) vừa xây. Phần Fetch danh sách bằng `fetch()` sẽ **trở lại** ở Chương 4/Chương 6 cùng `ProductCard` và FlashList — không bắt buộc giữ lại ở bản dưới đây. Nếu muốn, bạn có thể giữ tạm đoạn fetch cũ ở phía dưới cùng màn hình (không xóa hẳn) để đối chiếu trước khi Chương 4 nâng cấp tiếp.

#### Bước 6: Thử nghiệm UI Kit trên HomeScreen

Mở `src/screens/HomeScreen.tsx`:

```tsx
import React, { useState, useCallback } from "react";
import { View, StyleSheet } from "react-native";
import ShopButton from "@components/ShopButton";
import Typography from "@components/ui/Typography";
import ShopInput from "@components/ui/ShopInput";
import { useCountdown } from "@hooks/useCountdown";
import { COLORS, SIZES } from "@constants/theme";

const HomeScreen = () => {
  const [loading, setLoading] = useState(false);
  const [coupon, setCoupon] = useState("");
  const { timeLeft, isFinished } = useCountdown(60);

  const handleCheckout = useCallback(() => {
    setLoading(true);
    setTimeout(() => {
      setLoading(false);
      console.log("Thanh toán thành công!", coupon);
    }, 2000);
  }, [coupon]);

  return (
    <View style={styles.container}>
      <Typography variant="h1" style={styles.title}>
        ShopAI UI Kit
      </Typography>

      <Typography
        variant="body2"
        color={COLORS.textLight}
        style={{ textAlign: "center", marginBottom: 16 }}
      >
        {isFinished
          ? "Đã hết hạn khuyến mãi!"
          : `Flash sale kết thúc sau: ${timeLeft}s`}
      </Typography>

      <View style={styles.card}>
        <Typography variant="h2" color={COLORS.primary} style={styles.price}>
          Tổng tiền: 15.000.000đ
        </Typography>

        <ShopInput
          label="Mã giảm giá"
          placeholder="Nhập mã (VD: SHOPAI10)"
          value={coupon}
          onChangeText={setCoupon}
          autoCapitalize="characters"
        />

        <ShopButton
          title="Xác nhận thanh toán"
          onPress={handleCheckout}
          isLoading={loading}
          disabled={isFinished}
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
    justifyContent: "center",
    padding: SIZES.padding,
  },
  title: { textAlign: "center", marginBottom: 12 },
  card: {
    backgroundColor: COLORS.surface,
    padding: 20,
    borderRadius: SIZES.radius,
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 10,
    elevation: 5,
  },
  price: { marginBottom: 20, textAlign: "center" },
});

export default HomeScreen;
```

#### Bước 6.5 (TÙY CHỌN — áp dụng lý thuyết Phần 3.3): Bộ đếm số lượng bằng `useReducer`

Không bắt buộc — làm thêm để luyện `useReducer` ngay trên `HomeScreen`, không ảnh hưởng đến `ShopButton`/`Typography`/`useCountdown` đã có. Thêm vào `src/screens/HomeScreen.tsx`:

```tsx
import { useReducer } from "react";

// Đặt cạnh các import khác trong HomeScreen
type QtyAction = { type: "ADD" } | { type: "REMOVE" };

function qtyReducer(state: number, action: QtyAction): number {
  switch (action.type) {
    case "ADD":
      return state + 1;
    case "REMOVE":
      return Math.max(1, state - 1); // Không cho xuống dưới 1
    default:
      return state;
  }
}

// Trong Component HomeScreen, đặt cạnh useState(coupon)/useCountdown:
const [quantity, dispatchQty] = useReducer(qtyReducer, 1);
```

Rồi thêm vào JSX (trong `styles.card`, trước `ShopButton` "Xác nhận thanh toán"):

```tsx
<View
  style={{
    flexDirection: "row",
    alignItems: "center",
    justifyContent: "center",
    marginBottom: 16,
  }}
>
  <ShopButton
    title="-"
    onPress={() => dispatchQty({ type: "REMOVE" })}
    style={{ width: 44, height: 44 }}
  />
  <Typography variant="h3" style={{ marginHorizontal: 20 }}>
    {quantity}
  </Typography>
  <ShopButton
    title="+"
    onPress={() => dispatchQty({ type: "ADD" })}
    style={{ width: 44, height: 44 }}
  />
</View>
```

> Đây chính là mô hình cart-lite reducer ở Phần 3.3 mục 2, chỉ rút gọn thành 1 con số thay vì mảng sản phẩm. Muốn luyện `useContext` **thật đầy đủ** (không chỉ demo lý thuyết suông), xem tiếp Bước 7 ngay dưới đây — nơi `ThemeContext` được nối chính thức vào `App.tsx` và `HomeScreen` với nút bật/tắt Sáng/Tối, có tính vào Checklist nghiệm thu Sprint 3.

#### Bước 7: Kích hoạt Dark Mode thật với `ThemeContext` (áp dụng lý thuyết Phần 3.3 mục 1)

Ở Phần 3.3 mục 1, `ThemeContext` mới chỉ là ví dụ minh hoạ lý thuyết. Giờ ta nối nó vào thật, biến ShopAI thành app có Dark Mode hoạt động, mà **không sửa gì bên trong** `Typography`/`ShopInput`/`ShopButton` đã xây ở Bước 2-4 — nguyên tắc là để UI Kit vẫn nhận màu qua Props như bình thường, chỉ có `HomeScreen` là nơi "quyết định" dùng màu nào.

**7.1. Tạo Context** — Sao chép đúng mẫu ở Phần 3.3 mục 1 vào file `src/contexts/ThemeContext.tsx`:

```tsx
// src/contexts/ThemeContext.tsx
import React, { createContext, useContext, useState, ReactNode } from "react";
import { COLORS } from "@constants/theme";

// Bộ màu Sáng lấy thẳng từ theme.ts (giữ đúng bộ nhận diện thương hiệu ShopAI hiện có)
const LIGHT_COLORS = {
  background: COLORS.background,
  surface: COLORS.surface,
  text: COLORS.text,
  textLight: COLORS.textLight,
  primary: COLORS.primary,
};

// Bộ màu Tối — chỉ đổi nền/chữ, GIỮ NGUYÊN `primary` (màu thương hiệu không nên đổi theo Theme)
const DARK_COLORS = {
  background: "#121212",
  surface: "#1E1E1E",
  text: "#F5F5F5",
  textLight: "#9BA1A6",
  primary: COLORS.primary,
};

interface ThemeContextValue {
  isDark: boolean;
  colors: typeof LIGHT_COLORS;
  toggleTheme: () => void;
}

const ThemeContext = createContext<ThemeContextValue | undefined>(undefined);

export const ThemeProvider = ({ children }: { children: ReactNode }) => {
  const [isDark, setIsDark] = useState(false);

  const value: ThemeContextValue = {
    isDark,
    colors: isDark ? DARK_COLORS : LIGHT_COLORS,
    toggleTheme: () => setIsDark((prev) => !prev),
  };

  return (
    <ThemeContext.Provider value={value}>{children}</ThemeContext.Provider>
  );
};

export const useTheme = () => {
  const ctx = useContext(ThemeContext);
  if (!ctx) throw new Error("useTheme phải được gọi bên trong <ThemeProvider>");
  return ctx;
};
```

**7.2. Bọc App bằng `ThemeProvider`** — Mở `App.tsx` (đã có `SafeAreaProvider` từ trước, chưa có Navigation vì Chương 5 mới cài):

```tsx
import { SafeAreaProvider } from "react-native-safe-area-context";
import { ThemeProvider } from "@contexts/ThemeContext";
import HomeScreen from "@screens/HomeScreen";

function App() {
  return (
    <SafeAreaProvider>
      <ThemeProvider>
        <HomeScreen />
      </ThemeProvider>
    </SafeAreaProvider>
  );
}

export default App;
```

**7.3. Dùng `useTheme()` ở `HomeScreen`** — Thêm nút "Sáng/Tối" và đổi màu nền/chữ qua Props có sẵn của `Typography`/`ShopButton` (KHÔNG cần sửa bên trong 2 Component này):

```tsx
import { useTheme } from "@contexts/ThemeContext";
// ...các import cũ (useState, useCallback, ShopButton, Typography, ShopInput, useCountdown, COLORS, SIZES)

const HomeScreen = () => {
  const { colors, isDark, toggleTheme } = useTheme(); // Lấy bộ màu + hàm chuyển Theme
  // ...state loading/coupon/useCountdown giữ nguyên như Bước 6

  return (
    // Đổi nền qua Props `style` — ShopButton/Typography không cần biết gì về Dark Mode
    <View style={[styles.container, { backgroundColor: colors.background }]}>
      <Typography variant="h1" color={colors.text} style={styles.title}>
        ShopAI UI Kit
      </Typography>

      <ShopButton
        title={isDark ? "Chuyển sang Sáng" : "Chuyển sang Tối"}
        onPress={toggleTheme}
        style={{ backgroundColor: colors.primary, marginBottom: 16 }}
      />

      {/* ...phần Typography đếm ngược + card giữ nguyên như Bước 6, chỉ đổi color={colors.text}/colors.textLight thay vì COLORS.text/COLORS.textLight nếu muốn card cũng đổi màu theo Theme */}
    </View>
  );
};
```

> [!TIP]
> Đây chính là lựa chọn **"giữ COLORS tĩnh trong `theme.ts`, để `ThemeContext` override đúng những giá trị hay đổi nhất theo Theme (`background`/`surface`/`text`/`textLight`), còn `primary` — màu thương hiệu — giữ nguyên"** — cách làm nhẹ nhàng, không phải viết lại `Typography`/`ShopButton`/`ShopInput` để tự gọi `useTheme()` bên trong (cách đó cũng đúng, nhưng tốn công hơn nhiều cho Sprint 3). Ở các dự án lớn hơn, khi UI Kit cần tự động đổi màu ở mọi nơi, đội ngũ thường nâng cấp lên hướng Unistyles đã nhắc ở Phần 3.2 mục 3.

#### Bước 8: Lưu code (Git)

```bash
git add .
git commit -m "Sprint 3: Design System — Typography, ShopInput, ShopButton, useCountdown, ThemeContext Dark Mode"
git push origin main
```

**Checklist nghiệm thu nhanh:**

- [ ] Đổi `COLORS.primary` trong `theme.ts` → nút và giá đổi màu theo (không sửa từng màn hình)
- [ ] Gõ vào ô Input thấy state cập nhật
- [ ] Đồng hồ đếm ngược chạy, hết giờ thì nút bị `disabled`
- [ ] Bấm nút "Chuyển sang Tối/Sáng" → nền và chữ đổi màu ngay lập tức, không cần khởi động lại app

---

## 🎯 CHUẨN BỊ CHO CHƯƠNG 4

Bạn đã biết làm Component cơ bản, nhưng làm sao để dựng một giao diện phức tạp (Ảnh bên trái, chữ bên phải, nút bấm canh giữa)? Đó là quyền năng của **Flexbox**.
Trong Chương 4, chúng ta sẽ giải phẫu Flexbox, xử lý hiện tượng "Tai thỏ" (Notch) che mất giao diện, và đi sâu vào bí mật Tối ưu hóa Bộ nhớ khi render danh sách ngàn phần tử (FlatList & FlashList).

> Bộ Hooks đã đủ (`useState`, `useEffect`, `useContext`, `useReducer`, `useMemo`, `useCallback`) — hãy nhớ cạm bẫy Re-render của `useContext` ở Phần 3.3, vì Chương 6 sẽ đối chiếu trực tiếp nó với Zustand khi ta đưa Token đăng nhập và Giỏ hàng thật lên Global State.
>
> **Tính liên tục:** `ThemeProvider` bọc ở `App.tsx` từ Sprint 3 sẽ **giữ nguyên** xuyên suốt các chương sau — Chương 4 thêm `SafeAreaProvider`, Chương 5 thêm `NavigationContainer`, đều lồng **bên trong** `ThemeProvider` này, không thay thế nó.
