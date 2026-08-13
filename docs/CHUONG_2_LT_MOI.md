---
sidebar_position: 2
title: Chương 2
---

# GIÁO TRÌNH LÝ THUYẾT & THỰC CHIẾN
## CHƯƠNG 2: KHÁI NIỆM REACT + CORE COMPONENTS + API NHẬP MÔN
**Thời lượng:** 6 tiết Lý thuyết + 2 tiết Thực hành  
**Ánh xạ đề cương:**
- Đề cương **1.2** (Component, JSX, Props, State, Event, Style)
- Đề cương **2.1–2.2** (Core Components + Fetch/Axios nhập môn)
- Kiến trúc RN (nối tiếp Ch.1 mục 1.1.4)

---

> [!IMPORTANT]
> **Thực hành chương = Sprint ShopAI cuối file.** Hoàn thành Sprint này để đạt mục tiêu chương. Hoàn thành đủ 11 chương theo `SHOPAI_HOAN_THIEN.md` = sản phẩm ShopAI **hoàn thiện đẳng cấp**.

## 📚 MỤC TIÊU HỌC TẬP

Sau khi hoàn thành chương này, học viên sẽ:
- ✅ Hiểu kiến trúc Bridge → JSI/Fabric
- ✅ Nắm **Component, JSX, Props, State, Event, StyleSheet** (có mô hình UI + file chạy được)
- ✅ Thành thạo **Core Components phổ biến**: View, Text, Image, TextInput, ScrollView, Pressable, FlatList, SectionList, ActivityIndicator, Modal, Switch, Alert, SafeAreaView
- ✅ Biết khi nào dùng ScrollView vs FlatList vs SectionList
- ✅ Thành thạo `useState` / `useEffect` (tránh Memory Leak, Closure Trap)
- ✅ Gọi API cơ bản bằng **Fetch** và **Axios** (nhập môn — sâu hơn ở Ch.6)
- ✅ Dựng cấu trúc thư mục + Path Aliases cho ShopAI
- ✅ **Thực chiến:** HomeScreen demo đủ core components + fetch thử dữ liệu mẫu

---

## 🗺️ LỘ TRÌNH CHƯƠNG NÀY

```
2.1 Kiến trúc under the hood
2.2 Component & JSX (+ mô hình UI)
2.3 Props & State (+ DemoPropsState)
2.4 Style & StyleSheet (cầm tay chỉ việc + bản vẽ UI)
2.5 useState / useEffect
2.6 Core Components ĐẦY ĐỦ   ← đề cương 2.1
2.7 Fetch & Axios nhập môn   ← đề cương 2.2
2.8 Clean Architecture + Path Alias
Sprint 2: Cấu trúc src/ + HomeScreen + fetch
```

---

## 🏗️ PHẦN 2.1: KIẾN TRÚC REACT NATIVE (UNDER THE HOOD)

Để trở thành một kỹ sư cấp cao (Senior Engineer), bạn không thể chỉ biết gõ code React. Bạn phải hiểu hệ thống bên dưới biên dịch và thực thi code của bạn như thế nào. 

Nhiều người lầm tưởng React Native (RN) là tạo ra một trang Web HTML/CSS rồi nhúng vào một trình duyệt thu nhỏ (WebView). **Đây là một quan niệm hoàn toàn sai lầm.**

Khi bạn viết `<View>`, RN không biến nó thành `<div>`. RN giao tiếp với hệ điều hành để yêu cầu tạo ra một `UIView` (trên iOS) hoặc `android.view.ViewGroup` (trên Android). Code của bạn thực sự tạo ra giao diện Native (Bản địa).

### 1. Kiến trúc Cũ: Kỷ nguyên của Cầu nối (The Bridge)
Trong các phiên bản RN trước 0.68, hệ thống được chia làm 3 luồng (Threads) hoạt động hoàn toàn độc lập, không biết gì về nhau:

1. **JS Thread (Luồng JavaScript):** Nơi toàn bộ code React của bạn (logic, state, API) được chạy. Nó sử dụng một Engine tên là **Hermes** (hoặc JavaScriptCore).
2. **Native Thread (Luồng UI):** Luồng chính của hệ điều hành. Nơi trực tiếp vẽ đồ họa, hiển thị nút bấm, hình ảnh lên màn hình điện thoại. Nó được viết bằng Objective-C/Swift (iOS) hoặc Java/Kotlin (Android).
3. **Shadow Thread:** Luồng trung gian. Vì JS và Native đo lường kích thước khác nhau, Shadow Thread sử dụng một công cụ tên là **Yoga Engine** để dịch các lệnh Flexbox (width: 100%, justifyContent: center) thành tọa độ điểm ảnh tuyệt đối (X, Y, Width, Height) trước khi đưa cho Native Thread vẽ.

**🔴 Nút thắt cổ chai (The Bottleneck):**
JS Thread và Native Thread khác ngôn ngữ, không chia sẻ bộ nhớ. Để chúng nói chuyện được với nhau, Facebook tạo ra một cây cầu gọi là **The Bridge**.
Mỗi khi JS muốn Native vẽ một cái hộp màu đỏ, nó phải chuyển đổi yêu cầu đó thành chuỗi văn bản dạng JSON (Serialization):
`{"command": "createView", "color": "red", "width": 100}`
Tin nhắn JSON này bị nhét qua cây cầu. Đầu kia, Native Thread phải dịch ngược chuỗi JSON này ra mã máy (Deserialization) rồi mới vẽ.

> **Hậu quả:** Quá trình đóng/mở gói JSON này cực kỳ tốn thời gian (Asynchronous). Nếu bạn có một màn hình danh sách 1000 sản phẩm, hàng chục ngàn tin nhắn JSON sẽ bị nhồi nhét qua cây cầu này trong tích tắc. Cây cầu bị kẹt xe! Kết quả là màn hình bị giật (Drop FPS), nút bấm bị trễ sau khi chạm.

### 2. Kiến trúc Mới: Kỷ nguyên Không Cầu Nối (JSI & Fabric)
Để giải quyết tận gốc vấn đề trên, từ bản 0.68+, Facebook đập bỏ The Bridge và thay bằng Kiến trúc Mới (New Architecture):

1. **JSI (JavaScript Interface):** Đây là một lớp C++ siêu nhẹ. Nó cho phép JS Thread **chia sẻ bộ nhớ (Shared Memory)** trực tiếp với Native Thread. Lần đầu tiên trong lịch sử, code JS có thể gọi THẲNG (Invoke) các hàm C++/Java/Objective-C của hệ điều hành mà không cần phải chuyển thành chuỗi JSON nữa. Tốc độ giao tiếp từ Bất đồng bộ (Chờ đợi) đã trở thành Đồng bộ (Lập tức).
2. **Fabric (Renderer mới):** Tận dụng JSI, Fabric cho phép luồng UI vẽ giao diện và phản hồi sự kiện chạm vuốt trực tiếp cho JS Thread với độ trễ gần bằng 0.
3. **TurboModules:** Trước đây, khi app bật lên, RN phải tải mọi module (Camera, Bluetooth, GPS...) vào RAM dù chưa dùng đến. Giờ đây, TurboModules chỉ nạp Module Camera vào RAM ngay tại chính xác mili-giây mà bạn bấm nút "Mở Camera" (Lazy Loading).

*Trong dự án ShopAI, chúng ta đang sử dụng RN 0.74+, Kiến trúc mới này đã được bật mặc định!*

---

## ⚛️ PHẦN 2.2: COMPONENT & JSX — CẦM TAY CHỈ VIỆC

> Mục tiêu: sau phần này bạn hiểu cấu trúc một file React Native, **nhìn một màn hình** và **viết được** cây JSX tương ứng.

### A. Giải phẫu một file React Native (Dành cho người mới tinh)

Trước khi viết giao diện, bạn cần hiểu cấu trúc của một file mã nguồn React Native. Người mới học thường sao chép (copy-paste) mã mà không hiểu tại sao lại cần những dòng lệnh đầu tiên và cuối cùng của file.

Một file Component trong React Native luôn gồm **3 phần chính**:

**1. Phần `import` (Nhập khẩu đồ nghề):**
Ở đầu mỗi file, bạn luôn thấy các dòng bắt đầu bằng chữ `import`.
```tsx
import React from 'react';
import { View, Text } from 'react-native';
```
- **Ý nghĩa:** Máy tính không tự biết `View` hay `Text` là gì. `import` giống như việc bạn vào kho dụng cụ (thư viện `react-native`) và lấy ra cái búa (`View`), cái kìm (`Text`) để chuẩn bị xây nhà.
- **Quy tắc vàng:** Dùng cái gì phải `import` cái đó. Nếu bạn gõ thẻ `<Image />` ở dưới mà quên `import { Image } from 'react-native'` ở trên, app sẽ báo lỗi đỏ rực màn hình (ReferenceError).

**2. Phần Thân (Trái tim của Component):**
Đây là nơi bạn viết logic và giao diện. Nó luôn là một hàm (function).
```tsx
function HomeScreen() {
  return (
    <View>
      <Text>Xin chào ShopAI</Text>
    </View>
  );
}
```
- **Ý nghĩa:** Một Component bản chất chỉ là **một hàm trả về Giao diện (JSX)**. Mọi thứ bạn muốn hiển thị trên màn hình đều phải được bọc trong lệnh `return (...)`.

**3. Phần `export` (Xuất khẩu thành phẩm):**
Thường nằm ở dòng cuối cùng của file.
```tsx
export default HomeScreen;
```
- **Ý nghĩa:** Sau khi xây xong màn hình `HomeScreen`, bạn phải "đóng gói và xuất khẩu" (`export`) nó. Nhờ dòng chữ này, file cấu hình chính như `App.tsx` mới có thể "nhập khẩu" (`import HomeScreen from './...HomeScreen'`) và hiển thị nó lên điện thoại.
- **Nếu quên:** Màn hình của bạn bị nhốt kín trong file đó, không file nào khác gọi được nó, hệ thống sẽ báo lỗi `Element type is invalid`.

*Tóm lại công thức:* **Nhập đồ nghề (import) → Chế tạo (function) → Xuất xưởng (export default).**

---

### B. Mô hình giao diện trước — rồi mới gõ code

Hãy tưởng tượng màn hình Welcome đơn giản của ShopAI:

```
┌─────────────────────────────┐
│         (màn hình)          │  ← View (hộp ngoài, flex:1)
│                             │
│         ShopAI              │  ← Text (thương hiệu)
│   Môi trường đã sẵn sàng    │  ← Text (dòng phụ)
│                             │
└─────────────────────────────┘
```

**Luật vàng khi nhìn mô hình → viết JSX:**
1. Mỗi **hộp chữ nhật** = thường là một `<View>`.
2. Mỗi **dòng chữ** = bắt buộc một `<Text>` (không được viết chữ trần trong `View`).
3. Hộp ngoài bao hộp trong = **JSX lồng nhau** (indent thụt vào = nằm bên trong).

Cây UI của mô hình trên:

```
View (màn hình)
├── Text ("ShopAI")
└── Text ("Môi trường đã sẵn sàng")
```

### B. JSX là gì? (giải thích dễ hiểu)

JSX là cách viết **trông giống HTML** nhưng nằm trong file JavaScript/TypeScript. Máy không chạy JSX trực tiếp — Babel dịch thành `React.createElement(...)`. Bạn chỉ cần nhớ: **viết JSX cho dễ đọc**.

| Web (HTML/React) | React Native |
|------------------|--------------|
| `<div>` | `<View>` |
| `<span>` / chữ | `<Text>` |
| `<img>` | `<Image>` |
| `className="..."` + file CSS | `style={...}` + object JS / `StyleSheet` |

### C. File đầy đủ — `JsxWelcomeDemo.tsx` (copy chạy được)

Tạo `src/screens/demos/JsxWelcomeDemo.tsx`:

```tsx
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

/**
 * JsxWelcomeDemo — bài đầu: nhìn mô hình → viết JSX
 * Tạm gắn vào App: return <JsxWelcomeDemo />
 */
function JsxWelcomeDemo() {
  return (
    <View style={styles.screen}>
      <Text style={styles.brand}>ShopAI</Text>
      <Text style={styles.subtitle}>Môi trường đã sẵn sàng</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1,
    backgroundColor: '#F5F5F5',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  brand: { fontSize: 36, fontWeight: '800', color: '#FF4D4F' },
  subtitle: { marginTop: 8, fontSize: 16, color: '#7F8C8D' },
});

export default JsxWelcomeDemo;
```

### D. Giải thích từng khối

| Khối | Ý nghĩa (đọc chậm) |
|------|---------------------|
| `import React from 'react'` | Nạp React (cần cho JSX trong nhiều cấu hình TS/Babel) |
| `import { View, Text, StyleSheet } from 'react-native'` | Lấy đúng “viên gạch” UI của RN — **thiếu dòng này là đỏ ngay** |
| `function JsxWelcomeDemo()` | Functional Component = hàm trả về JSX |
| `return ( ... )` | Trả về **một** gốc UI (ở đây một `View` bao ngoài) |
| `<View style={styles.screen}>` | Hộp màn hình; `style` trỏ object đã tạo bằng `StyleSheet` |
| `<Text>...</Text>` | Chữ hiển thị |
| `StyleSheet.create({...})` | Bản vẽ giao diện — học tường tận ở **Phần 2.4** bên dưới |
| `export default` | Cho `App.tsx` `import` được |

### E. Component: Class vs Functional (chỉ cần nhớ kết luận)

| | Class (cũ) | Functional (ShopAI dùng) |
|--|------------|---------------------------|
| Viết như | `class X extends React.Component` | `function X() { return ... }` |
| State | `this.state` rối | `useState` rõ ràng |
| Khóa học | Không bắt viết mới | **Bắt buộc** |

### F. Lỗi hay gặp với JSX

| Sai | Đúng |
|-----|------|
| `<View>Hello</View>` | `<View><Text>Hello</Text></View>` |
| Hai gốc cạnh nhau không bọc | Bọc bằng một `View` (hoặc `<>...</>`) |
| Quên `import { Text } ...` | Luôn import đủ |
| `className="box"` | `style={styles.box}` |

---

## 🎭 PHẦN 2.3: PROPS VÀ STATE — CẦM TAY CHỈ VIỆC

> Đây là bài quan trọng nhất của React. Đọc theo thứ tự: **Props → State → file gộp cả hai → sơ đồ luồng dữ liệu**.

### A. Phân biệt trong một câu + bảng

| | **Props** | **State** |
|--|-----------|-----------|
| Là gì? | Dữ liệu **Cha truyền xuống Con** | Dữ liệu **nội bộ** Component tự giữ |
| Ai đổi? | Chỉ Cha đổi khi truyền lại | Chính Component đó gọi `set...` |
| Con sửa được không? | **Không** (read-only) | Có, qua hàm cập nhật |
| Ví dụ ShopAI | `title="iPhone 15"` trên thẻ SP | Số lượng trong giỏ, chữ đang gõ ô tìm |

### B. Mô hình giao diện — thẻ sản phẩm (Props)

```
┌────────────────────────────────┐
│  iPhone 15 Pro                 │  ← Text nhận props.title
│  30.000.000 VNĐ                │  ← Text nhận props.price
│  (màu đỏ nếu đang giảm giá)    │  ← phụ thuộc props.isDiscount
└────────────────────────────────┘
```

Cha (danh sách) **truyền** `title` / `price` / `isDiscount` xuống Con (`ProductCard`). Con chỉ **hiển thị**, không được gán `title = "..."`.

### C. File Props — đủ import

```tsx
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

type ProductCardProps = {
  title: string;
  price: string;
  isDiscount: boolean;
};

/** Component CON — chỉ nhận Props, không tự đổi title/price */
function ProductCard({ title, price, isDiscount }: ProductCardProps) {
  return (
    <View style={styles.card}>
      <Text style={styles.title}>{title}</Text>
      <Text style={[styles.price, isDiscount && styles.priceSale]}>
        {price} VNĐ
      </Text>
    </View>
  );
}

/** Component CHA — truyền Props xuống */
export default function PropsDemo() {
  return (
    <View style={styles.screen}>
      <Text style={styles.heading}>Danh sách sản phẩm</Text>
      <ProductCard title="iPhone 15 Pro" price="30.000.000" isDiscount={false} />
      <ProductCard title="Ốp lưng trong suốt" price="150.000" isDiscount={true} />
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, padding: 16, backgroundColor: '#F5F5F5' },
  heading: { fontSize: 18, fontWeight: '700', marginBottom: 12, color: '#2C3E50' },
  card: {
    backgroundColor: '#fff',
    padding: 14,
    borderRadius: 12,
    marginBottom: 10,
  },
  title: { fontSize: 18, fontWeight: '700', color: '#2C3E50' },
  price: { marginTop: 6, fontSize: 16, color: '#2C3E50' },
  priceSale: { color: '#FF4D4F', fontWeight: '700' },
});
```

**Giải thích từng khối (Props):**

| Khối | Ý nghĩa |
|------|---------|
| `type ProductCardProps = {...}` | Khai báo “hợp đồng” dữ liệu Cha phải truyền |
| `function ProductCard({ title, price, isDiscount })` | Destructuring: lấy từng prop ra biến |
| `{title}` trong JSX | In giá trị prop ra màn hình |
| `style={[styles.price, isDiscount && styles.priceSale]}` | Mảng style: style sau ghi đè/bổ sung khi điều kiện đúng |
| `<ProductCard title="..." />` | Cha **truyền** prop — đây là chiều dữ liệu Cha → Con |

### D. State — mô hình nút tăng số lượng

```
┌────────────────────────────────┐
│  Số lượng:  2                  │  ← Text đọc state quantity
│  [  −  ]      [  +  ]          │  ← Pressable gọi setQuantity
└────────────────────────────────┘
```

Khi bấm `+`, gọi `setQuantity(...)` → React **vẽ lại** → chữ “Số lượng” đổi. Nếu gán `quantity = quantity + 1` trực tiếp → **màn hình không đổi** (sai luật).

### E. File State đơn giản — đủ import

```tsx
import React, { useState } from 'react';
import { View, Text, Pressable, StyleSheet } from 'react-native';

export default function StateDemo() {
  const [quantity, setQuantity] = useState(1);

  return (
    <View style={styles.screen}>
      <Text style={styles.label}>Số lượng: {quantity}</Text>
      <View style={styles.row}>
        <Pressable
          style={styles.btn}
          onPress={() => setQuantity(prev => Math.max(1, prev - 1))}
        >
          <Text style={styles.btnText}>−</Text>
        </Pressable>
        <Pressable
          style={styles.btn}
          onPress={() => setQuantity(prev => prev + 1)}
        >
          <Text style={styles.btnText}>+</Text>
        </Pressable>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  label: { fontSize: 20, marginBottom: 16, color: '#2C3E50' },
  row: { flexDirection: 'row', gap: 16 },
  btn: {
    width: 48,
    height: 48,
    borderRadius: 12,
    backgroundColor: '#FF4D4F',
    alignItems: 'center',
    justifyContent: 'center',
  },
  btnText: { color: '#fff', fontSize: 22, fontWeight: '700' },
});
```

| Khối | Ý nghĩa |
|------|---------|
| `useState(1)` | Tạo State, giá trị ban đầu = 1 |
| `quantity` | Đọc giá trị hiện tại để đưa vào `<Text>` |
| `setQuantity(prev => prev + 1)` | Cập nhật dựa trên giá trị cũ (an toàn) — chi tiết Batching ở Phần 2.5 |
| `onPress={() => ...}` | **Sự kiện**: truyền hàm, không viết `onPress={setQuantity(1)}` (sai: gọi ngay lúc render) |

### F. File gộp Props + State — `DemoPropsState.tsx` (bắt buộc hiểu)

**Mô hình:**

```
┌────────────────────────────────────────┐
│  [ProductCard]                         │
│   Tên + giá (từ PROPS)                 │
│   Số lượng: 2   [−] [+]  (STATE ở CHA) │
│                                        │
│  Tạm tính: 60.000.000                  │  ← CHA tính từ state × giá
└────────────────────────────────────────┘
```

**Luồng dữ liệu (đọc theo số):**

```
1. Cha giữ State: quantity = 2
2. Cha truyền Props xuống ProductCard: name, price, quantity, onInc, onDec
3. User bấm + trên ProductCard
4. ProductCard GỌI onInc() (callback từ Cha) — Con không tự setQuantity
5. Cha chạy setQuantity → quantity = 3
6. React re-render Cha + Con với quantity mới
7. Dòng "Tạm tính" ở Cha cũng đổi theo
```

```tsx
import React, { useState } from 'react';
import { View, Text, Pressable, StyleSheet } from 'react-native';

type CardProps = {
  name: string;
  price: number;
  quantity: number;
  onInc: () => void;
  onDec: () => void;
};

function ProductCard({ name, price, quantity, onInc, onDec }: CardProps) {
  return (
    <View style={styles.card}>
      <Text style={styles.name}>{name}</Text>
      <Text style={styles.price}>{price.toLocaleString('vi-VN')} VNĐ</Text>
      <View style={styles.row}>
        <Pressable style={styles.btn} onPress={onDec}>
          <Text style={styles.btnText}>−</Text>
        </Pressable>
        <Text style={styles.qty}>{quantity}</Text>
        <Pressable style={styles.btn} onPress={onInc}>
          <Text style={styles.btnText}>+</Text>
        </Pressable>
      </View>
    </View>
  );
}

export default function DemoPropsState() {
  const price = 30000000;
  const [quantity, setQuantity] = useState(1);

  return (
    <View style={styles.screen}>
      <ProductCard
        name="iPhone 15 Pro"
        price={price}
        quantity={quantity}
        onInc={() => setQuantity(q => q + 1)}
        onDec={() => setQuantity(q => Math.max(1, q - 1))}
      />
      <Text style={styles.total}>
        Tạm tính: {(price * quantity).toLocaleString('vi-VN')} VNĐ
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, padding: 16, justifyContent: 'center', backgroundColor: '#F5F5F5' },
  card: { backgroundColor: '#fff', borderRadius: 12, padding: 16 },
  name: { fontSize: 20, fontWeight: '800', color: '#2C3E50' },
  price: { marginTop: 6, color: '#7F8C8D' },
  row: { flexDirection: 'row', alignItems: 'center', marginTop: 16, gap: 12 },
  btn: {
    width: 40,
    height: 40,
    borderRadius: 10,
    backgroundColor: '#FF4D4F',
    alignItems: 'center',
    justifyContent: 'center',
  },
  btnText: { color: '#fff', fontSize: 20, fontWeight: '700' },
  qty: { fontSize: 18, fontWeight: '700', minWidth: 24, textAlign: 'center' },
  total: { marginTop: 20, fontSize: 18, fontWeight: '700', color: '#FF4D4F' },
});
```

> **Vì sao `quantity` sống ở Cha?** Vì cả `ProductCard` lẫn dòng “Tạm tính” đều cần cùng một số. State đặt chỗ **cần dùng chung** (Lifting State Up).

---

## 🎨 PHẦN 2.4: STYLE & `StyleSheet` — CẦM TAY CHỈ VIỆC

> Nhiều người đọc `StyleSheet.create` mà không hiểu vì **không nối được từng dòng style với hình trên màn hình**. Phần này làm đúng việc đó.

### A. RN không có file CSS — vậy style viết ở đâu?

| Web | React Native |
|-----|--------------|
| `styles.css` + `className="btn"` | **Không có** file `.css` cho UI native |
| Thuộc tính `font-size`, `background-color` | Object JS: `fontSize`, `backgroundColor` (**camelCase**) |
| Đơn vị `px`, `rem` | Số thuần: `fontSize: 16` (RN hiểu là density-independent) |

Bạn gắn style bằng prop `style={...}` trên `View` / `Text` / …

### B. Bản vẽ UI trước — ánh xạ sang StyleSheet

Mô hình nút đỏ ShopAI:

```
┌─────────────────────────────┐
│                             │  screen: flex 1, nền xám, căn giữa
│      ┌───────────────┐      │
│      │  Thêm vào giỏ │      │  button: nền đỏ, padding, bo góc
│      └───────────────┘      │  buttonText: chữ trắng, đậm
│                             │
└─────────────────────────────┘
```

| Nhìn thấy trên máy | Key trong StyleSheet | Ví dụ giá trị |
|--------------------|----------------------|---------------|
| Nền cả màn xám | `backgroundColor` | `'#F5F5F5'` |
| Nội dung nằm giữa màn | `justifyContent` + `alignItems` | `'center'` |
| Nút có khoảng thở trong | `paddingVertical` / `paddingHorizontal` | `14` / `28` |
| Góc nút bo tròn | `borderRadius` | `12` |
| Nút màu đỏ ShopAI | `backgroundColor` | `'#FF4D4F'` |
| Chữ nút trắng, to | `color`, `fontSize`, `fontWeight` | `'#fff'`, `16`, `'700'` |

### C. Ba cách viết style (chỉ nhớ cách 2 & 3 cho ShopAI)

**1) Inline (nhanh nhưng dễ làm chậm app nếu lạm dụng):**
```tsx
<View style={{ backgroundColor: '#fff', padding: 16 }} />
```
Mỗi lần Component render, object `{...}` **tạo mới** → khó tối ưu sau này.

**2) `StyleSheet.create` (chuẩn khóa học):**
```tsx
const styles = StyleSheet.create({
  card: { backgroundColor: '#fff', padding: 16 },
});
// dùng: style={styles.card}
```
Object tạo **một lần** khi file được nạp, nằm **ngoài** hàm Component.

**3) Mảng style (rất hay dùng):**
```tsx
<Text style={[styles.price, isSale && styles.priceSale]} />
```
Style sau được gộp / ghi đè lên style trước. `false`/`null` trong mảng bị bỏ qua.

### D. File đầy đủ — `StyleSheetWalkthrough.tsx`

```tsx
import React from 'react';
import { View, Text, Pressable, StyleSheet } from 'react-native';

/**
 * Đọc file này cùng bản vẽ ASCII ở mục B.
 * Mỗi key trong `styles` tương ứng một phần nhìn thấy trên máy.
 */
export default function StyleSheetWalkthrough() {
  return (
    <View style={styles.screen}>
      <Text style={styles.title}>ShopAI</Text>
      <Text style={styles.caption}>StyleSheet = bản vẽ giao diện bằng Object JS</Text>

      <Pressable style={styles.button}>
        <Text style={styles.buttonText}>Thêm vào giỏ</Text>
      </Pressable>

      {/* Hai lớp style: nền + trạng thái nhấn (demo tĩnh) */}
      <Pressable style={[styles.button, styles.buttonOutline]}>
        <Text style={[styles.buttonText, styles.buttonOutlineText]}>Xem chi tiết</Text>
      </Pressable>
    </View>
  );
}

// ĐẶT NGOÀI Component — tạo 1 lần, không tạo lại mỗi lần vẽ màn hình
const styles = StyleSheet.create({
  screen: {
    flex: 1, // chiếm hết chiều cao cha (thường = cả màn)
    backgroundColor: '#F5F5F5',
    justifyContent: 'center', // xếp con theo trục dọc, đẩy vào giữa
    alignItems: 'center', // căn giữa theo ngang
    padding: 24, // khoảng cách mép trong của screen
  },
  title: {
    fontSize: 32,
    fontWeight: '800',
    color: '#FF4D4F',
  },
  caption: {
    marginTop: 8, // cách title 8 đơn vị
    marginBottom: 24,
    fontSize: 14,
    color: '#7F8C8D',
    textAlign: 'center',
  },
  button: {
    backgroundColor: '#FF4D4F',
    paddingVertical: 14,
    paddingHorizontal: 28,
    borderRadius: 12,
    marginBottom: 12,
  },
  buttonText: {
    color: '#FFFFFF',
    fontSize: 16,
    fontWeight: '700',
  },
  buttonOutline: {
    backgroundColor: 'transparent',
    borderWidth: 2,
    borderColor: '#FF4D4F',
  },
  buttonOutlineText: {
    color: '#FF4D4F',
  },
});
```

### E. Giải thích từng khối StyleSheet (đọc như chú thích bản vẽ)

| Khối | Trên màn hình bạn thấy gì? |
|------|----------------------------|
| `flex: 1` trên `screen` | Hộp ngoài giãn full chiều cao → mới căn giữa được |
| `justifyContent: 'center'` | Các con (title, nút…) dịch vào giữa theo **chiều dọc** (trục chính mặc định của RN là cột) |
| `alignItems: 'center'` | Các con căn giữa theo **chiều ngang** |
| `padding: 24` | Nội dung không dính sát mép điện thoại |
| `marginTop` / `marginBottom` | Đẩy phần tử **ra xa** anh em xung quanh |
| `paddingVertical` trên nút | Chữ trong nút không bị sát trên/dưới |
| `borderRadius: 12` | Góc nút bo tròn |
| `borderWidth` + `borderColor` | Viền nút outline |
| `StyleSheet.create` ngoài hàm | Bản vẽ ổn định; Chương 3 giải thích thêm vì sao tốt cho hiệu năng |

### F. Sơ đồ: Inline vs StyleSheet (để hết bối rối)

```
INLINE mỗi lần render:
  render #1 → tạo object A  → gắn vào View
  render #2 → tạo object B  → gắn vào View  (tham chiếu mới liên tục)

StyleSheet.create (ngoài Component):
  file load  → tạo object styles.button MỘT LẦN
  render #1 → dùng lại styles.button
  render #2 → dùng lại styles.button
```

### G. Lỗi khiến người mới “không hiểu gì”

| Sai (thói quen Web) | Đúng trong RN |
|---------------------|---------------|
| `className="title"` | `style={styles.title}` |
| `font-size: 16px` | `fontSize: 16` |
| `background-color` | `backgroundColor` |
| File `App.css` | Không dùng cho UI Native |
| Quên `flex: 1` ở màn ngoài | Nội dung không căn giữa / không full màn |
| `style={styles.button, styles.x}` (sai cú pháp) | `style={[styles.button, styles.x]}` |

### H. Sự kiện (`onPress`) gắn với style nút — 30 giây

```tsx
<Pressable
  onPress={() => console.log('bấm')}
  style={({ pressed }) => [styles.button, pressed && { opacity: 0.85 }]}
>
  <Text style={styles.buttonText}>Thêm vào giỏ</Text>
</Pressable>
```

- `onPress` = **việc xảy ra khi chạm** (logic).
- `style` = **trông thế nào** (bản vẽ).
- `pressed` = Pressable cho biết đang giữ tay → bạn đổi nhẹ opacity (phản hồi xúc giác).

> Flexbox sâu (`row` / `space-between` / lưới 2 cột) học ở **Chương 4** với minh họa UI. Design token `COLORS` / `SIZES` học ở **Chương 3**.

---

## 🪝 PHẦN 2.5: LÀM CHỦ REACT HOOKS (`useState` & `useEffect`)

Hooks là các hàm đặc biệt được Facebook thêm vào từ React 16.8, cho phép Functional Component có thể lưu trữ State và can thiệp vào vòng đời (Lifecycle).

### 1. `useState` Toàn tập

**Cú pháp chuẩn:**
```tsx
// const [tên_biến, hàm_cập_nhật] = useState(giá_trị_khởi_tạo);
const [count, setCount] = useState(0);
```

**Khái niệm Batching (Gộp tác vụ):**
Một lỗi 99% sinh viên mắc phải khi dùng State là hiểu sai về Batching. Xem ví dụ sau:

```tsx
import React, { useState } from 'react';
import { View, Text, Button } from 'react-native';

export default function Counter() {
  const [count, setCount] = useState(0);

  const handlePress = () => {
    // Giả sử count đang là 0. Chạy 3 lệnh setCount liên tiếp!
    setCount(count + 1); // setCount(0 + 1)
    setCount(count + 1); // setCount(0 + 1)
    setCount(count + 1); // setCount(0 + 1)
    
    // Câu hỏi: Sau khi bấm nút, count sẽ là 3 hay 1?
    // Trả lời: Count sẽ bằng 1!
  };

  return (
    <View style={{ marginTop: 50, alignItems: 'center' }}>
      <Text>Số lần bấm: {count}</Text>
      <Button title="Cộng 3 lần" onPress={handlePress} />
    </View>
  );
}
```
**Giải thích:** React không cập nhật state ngay lập tức. Để tối ưu hiệu năng, React đưa các lệnh `setCount` vào một hàng đợi (Queue) và gộp chúng lại (Batching). Tại thời điểm hàm `handlePress` chạy, biến `count` vẫn đang mang giá trị cũ là `0`. Nên cả 3 hàm đều thực thi `setCount(1)`.

**Cách khắc phục (Functional Update):**
Nếu State mới phụ thuộc vào State cũ, bắt buộc phải truyền một Callback Function vào hàm set.
```tsx
  const handlePress = () => {
    setCount((prev) => prev + 1); // prev là 0, trả về 1
    setCount((prev) => prev + 1); // prev là 1, trả về 2
    setCount((prev) => prev + 1); // prev là 2, trả về 3 (Kết quả cuối cùng)
  };
```

### 2. `useEffect` - Quản lý Vòng đời & Side Effects
Một Component có 3 giai đoạn sống (Lifecycle):
- **Mount:** Vừa sinh ra, được gắn lên màn hình.
- **Update:** Bị vẽ lại do State/Props đổi.
- **Unmount:** Bị phá hủy, gỡ khỏi màn hình.

`useEffect` được dùng để bắt các sự kiện này, và thực thi các tác vụ phụ (Side effects) như: Gọi API từ Server, Bật đồng hồ bấm giờ (Timer), Lắng nghe sự kiện bàn phím.

**Cú pháp:**
```tsx
useEffect(() => {
  // 1. Code Side-effect (Chạy khi Mount hoặc Update)
  
  return () => {
    // 2. Cleanup Function (Chạy trước khi Unmount hoặc trước lần Update tiếp theo)
  };
}, [dependencyArray]); // 3. Mảng phụ thuộc
```

**Sức mạnh của Mảng Phụ Thuộc (Dependency Array):**
Chính cái mảng `[]` ở cuối quyết định `useEffect` chạy khi nào:
1.  **Không có mảng `useEffect(() => {...})`:** Chạy lại ở MỌI LẦN re-render. Cực kỳ nguy hiểm, thường gây treo máy (Infinite Loop) nếu bên trong có hàm `setState`.
2.  **Mảng rỗng `useEffect(() => {...}, [])`:** Chạy ĐÚNG 1 LẦN DUY NHẤT khi Component vừa Mount. Lý tưởng nhất để gọi API tải dữ liệu ban đầu.
3.  **Có biến trong mảng `useEffect(() => {...}, [id, name])`:** Sẽ chạy lại MỖI KHI biến `id` hoặc `name` thay đổi giá trị.

### 3. Hiểm họa: Memory Leak (Rò rỉ bộ nhớ)
Xảy ra khi bạn bật một tiến trình ngầm (Ví dụ: `setInterval`, lắng nghe GPS, Websocket) lúc Component Sinh ra (Mount), nhưng quên Tắt nó đi lúc Component Chết (Unmount).
Tiến trình ngầm đó vẫn chạy mãi trong RAM điện thoại dù người dùng đã thoát khỏi màn hình đó, làm app ngày càng chậm và cuối cùng là Crash (Văng app).

**Cách khắc phục (Bắt buộc dùng Cleanup Function):**
```tsx
import React, { useState, useEffect } from 'react';
import { Text, View } from 'react-native';

export default function TimerScreen() {
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    console.log("Component Timer vừa Mount!");
    
    // Bật bộ đếm thời gian
    const timerId = setInterval(() => {
      setSeconds(prev => prev + 1);
      console.log("Đồng hồ đang chạy ngầm...");
    }, 1000);

    // BẮT BUỘC: Hàm dọn dẹp (Cleanup) trả về để hủy hẹn giờ
    return () => {
      console.log("Component Timer sắp Unmount! Dọn dẹp RAM!");
      clearInterval(timerId); // Hủy tiến trình ngầm
    };
  }, []); // Mảng rỗng -> Chỉ chạy lúc Mount

  return <Text>Giây: {seconds}</Text>;
}
```

### 4. Hiểm họa: Closure Trap
Đây là lỗi cực kỳ khó phát hiện. Xảy ra khi một hàm bất đồng bộ bên trong `useEffect` (như `setInterval`) bị kẹt lại với giá trị State cũ của lần render đầu tiên (gọi là Stale Closure).

**Ví dụ Lỗi Closure Trap:**
```tsx
export default function TrapScreen() {
  const [count, setCount] = useState(0);

  useEffect(() => {
    const timerId = setInterval(() => {
      // ❌ CLOSURE TRAP: count ở đây mãi mãi bị kẹt ở giá trị 0 (giá trị lúc component mount)
      setCount(count + 1); 
      // Kết quả trên màn hình: Số 1 hiện lên và ĐỨNG IM vĩnh viễn!
    }, 1000);

    return () => clearInterval(timerId);
  }, []); // Mảng rỗng khiến useEffect không bao giờ cập nhật biến count bên trong nó
  
  // ✅ Cách sửa: Dùng Functional Update: setCount(prev => prev + 1)
  // Hoặc đưa biến count vào mảng phụ thuộc: [count] (nhưng cách này sẽ làm Interval bị hủy và tạo lại liên tục).
  // Ưu tiên dùng Functional Update!
  return <Text>{count}</Text>;
}
```

---

## 📱 PHẦN 2.6: CORE COMPONENTS (Đề cương 2.1) — HƯỚNG DẪN TƯỜNG TẬN

Trong React Native bạn **không** dùng HTML (`div`, `span`, `img`). Mỗi Core Component được RN dịch thành **UI Native thật** trên iOS/Android.

### Cách đọc mỗi mục (bắt buộc theo thứ tự này)

Mỗi component dưới đây đều có đủ 6 phần:
1. **Là gì / nằm đâu trong cây UI**
2. **Ví dụ file đầy đủ** (có `import`, chạy được)
3. **Giải thích từng khối code**
4. **Bảng props quan trọng**
5. **Lỗi hay gặp**
6. **ShopAI dùng chỗ nào**

> [!IMPORTANT]
> Đừng chỉ nhìn JSX lẻ. Người mới thường copy `<Text>...</Text>` thiếu `import` → báo đỏ `Text is not defined`. **Luôn nhìn cả file mẫu.**

### Sơ đồ kiến trúc khối trên một màn hình ShopAI

```
SafeAreaView / View (màn hình)
├── View (header)
│   ├── Text (tiêu đề)
│   └── Pressable → Text (nút)
├── Image (banner)
├── TextInput (ô tìm)
└── FlatList
    └── View (mỗi dòng)
        ├── Image
        └── Text
```

Mỗi ô trong sơ đồ = **một component**. Hiểu cây này trước khi gõ code.

---

### 2.6.1. `<View>` — Hộp chứa (tương đương `div`)

#### 1) Là gì?
`View` là **hộp bố cục**. Nó không hiện chữ. Nhiệm vụ: bao quanh các component khác và quyết định vị trí (Flexbox).

#### 2) Ví dụ file đầy đủ (copy vào `ViewDemo.tsx` rồi import tạm vào App để chạy)

```tsx
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';

/**
 * DemoView — minh họa View lồng View
 * File: src/screens/demos/ViewDemo.tsx (học viên có thể tạo thư mục demos để thử)
 */
function ViewDemo() {
  return (
    // View ngoài cùng: chiếm full màn hình
    <View style={styles.screen}>
      {/* View con: một "thẻ" trắng nằm giữa */}
      <View style={styles.card}>
        <Text style={styles.title}>ShopAI</Text>
        <Text style={styles.caption}>View chỉ là hộp chứa — chữ phải nằm trong Text</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: {
    flex: 1, // chiếm hết không gian cha (ở đây = cả màn hình)
    backgroundColor: '#F5F5F5',
    justifyContent: 'center', // xếp con theo trục dọc, căn giữa
    alignItems: 'center', // căn giữa theo trục ngang
    padding: 16,
  },
  card: {
    width: '100%',
    backgroundColor: '#FFFFFF',
    borderRadius: 12,
    padding: 16,
  },
  title: { fontSize: 22, fontWeight: '700', color: '#FF4D4F' },
  caption: { marginTop: 8, color: '#7F8C8D' },
});

export default ViewDemo;
```

#### 3) Giải thích từng khối
| Khối | Ý nghĩa |
|------|---------|
| `import { View, Text, StyleSheet } from 'react-native'` | Lấy component có sẵn của RN. **Thiếu dòng này là lỗi ngay.** |
| `function ViewDemo()` | Functional Component — một hàm trả về JSX |
| `<View style={styles.screen}>` | Hộp ngoài; `style` trỏ tới object trong `StyleSheet` |
| `flex: 1` | “Chiếm hết chỗ còn trống của cha” |
| `justifyContent` / `alignItems` | Căn chỉnh **con** bên trong View (học sâu Flexbox ở Chương 4) |
| `<Text>...</Text>` | Chữ **không** được viết trần trong View |
| `export default` | Cho phép `App.tsx` import màn này |

#### 4) Props quan trọng
| Prop | Ý nghĩa | Ví dụ |
|------|---------|-------|
| `style` | Style object / mảng style | `style={styles.card}` |
| `pointerEvents` | Cho phép/chặn chạm xuyên qua | `'none'` khi loading overlay |
| `onLayout` | Biết kích thước thật sau khi vẽ | đo chiều cao header |

#### 5) Lỗi hay gặp
```tsx
// ❌ SAI — crash: chữ không được nằm trực tiếp trong View
<View>Xin chào ShopAI</View>

// ✅ ĐÚNG
<View><Text>Xin chào ShopAI</Text></View>
```

#### 6) ShopAI dùng chỗ nào?
Mọi màn (`HomeScreen`, `CartScreen`, `CheckoutScreen`) đều bắt đầu bằng một `View`/`SafeAreaView` làm khung.

---

### 2.6.2. `<Text>` — Văn bản (ví dụ bạn đang thiếu kiểu này)

#### 1) Là gì?
`Text` là **component duy nhất** được phép hiển thị chuỗi chữ trên màn hình RN. Trên iOS nó map sang `UILabel`/`UITextView`, trên Android sang `TextView`.

#### 2) Ví dụ file đầy đủ

```tsx
import React from 'react';
import { View, Text, StyleSheet, Alert } from 'react-native';

/**
 * TextDemo — đủ import, đủ style, có Text lồng Text + onPress
 */
function TextDemo() {
  const productName = 'Tai nghe Bluetooth Pro';
  const price = 1500000;

  return (
    <View style={styles.container}>
      {/* 1) Text thường */}
      <Text style={styles.heading}>Chi tiết sản phẩm</Text>

      {/* 2) Nội suy biến JS vào JSX bằng { } */}
      <Text style={styles.name}>{productName}</Text>

      {/* 3) Text lồng Text: phần "Giá:" màu đen, phần số tiền màu đỏ kế thừa fontSize từ cha nếu không ghi đè */}
      <Text style={styles.priceLine}>
        Giá:{' '}
        <Text style={styles.priceValue}>
          {price.toLocaleString('vi-VN')} đ
        </Text>
      </Text>

      {/* 4) Cắt chữ dài thành tối đa 2 dòng + dấu ... */}
      <Text style={styles.desc} numberOfLines={2} ellipsizeMode="tail">
        Mô tả dài: chống ồn chủ động, pin 30 giờ, tương thích iOS/Android,
        bảo hành chính hãng 12 tháng tại ShopAI trên toàn quốc.
      </Text>

      {/* 5) Text bấm được — giống link */}
      <Text
        style={styles.link}
        onPress={() => Alert.alert('ShopAI', 'Bạn vừa bấm vào chính sách đổi trả')}
      >
        Xem chính sách đổi trả
      </Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, backgroundColor: '#fff', justifyContent: 'center' },
  heading: { fontSize: 14, color: '#95A5A6', marginBottom: 8 },
  name: { fontSize: 22, fontWeight: '700', color: '#2C3E50' },
  priceLine: { marginTop: 12, fontSize: 16, color: '#2C3E50' },
  priceValue: { color: '#FF4D4F', fontWeight: '700' },
  desc: { marginTop: 12, fontSize: 14, color: '#7F8C8D', lineHeight: 20 },
  link: { marginTop: 16, color: '#1890FF', textDecorationLine: 'underline' },
});

export default TextDemo;
```

#### 3) Giải thích từng khối (đọc chậm)
1. **`import { View, Text, StyleSheet, Alert } from 'react-native'`**  
   - `Text`, `View`, `StyleSheet`: UI.  
   - `Alert`: hộp thoại hệ thống (để demo `onPress`).  
2. **`const productName = ...`** — biến JS bình thường.  
3. **`{productName}`** trong JSX — dấu `{}` = “chèn biểu thức JavaScript vào đây”.  
4. **Text lồng Text** — Text con có thể **kế thừa** một phần style từ Text cha (đặc biệt của Text, `View` không làm được vậy với chữ).  
5. **`numberOfLines={2}`** — tối đa 2 dòng; dư thì cắt.  
6. **`ellipsizeMode="tail"`** — cắt ở cuối, hiện `...`.  
7. **`onPress` trên Text** — biến đoạn chữ thành vùng bấm (không cần `Pressable` nếu chỉ là link nhỏ).

#### 4) Props quan trọng
| Prop | Kiểu | Ý nghĩa |
|------|------|---------|
| `style` | object / mảng | fontSize, color, fontWeight, textAlign… |
| `numberOfLines` | number | Giới hạn số dòng |
| `ellipsizeMode` | `'head' \| 'middle' \| 'tail' \| 'clip'` | Cách cắt chữ |
| `onPress` | `() => void` | Bấm vào chữ |
| `selectable` | boolean | Cho phép bôi đen copy |

#### 5) Lỗi hay gặp
| Sai | Đúng |
|-----|------|
| `<View>Hello</View>` | `<View><Text>Hello</Text></View>` |
| Quên import Text | `import { Text } from 'react-native'` |
| Style `className="title"` (thói quen web) | `style={styles.title}` |

#### 6) ShopAI dùng chỗ nào?
Tiêu đề “Khám phá”, tên SP trên `ProductCard`, giá tiền, empty state giỏ hàng — **100% là `Text`** (sau này bọc thành `Typography` ở Chương 3 cho đồng bộ font).

---

### 2.6.3. `<Image>` — Hình ảnh

#### 1) Là gì?
Hiển thị ảnh local (trong project) hoặc ảnh mạng (URL). Map sang `UIImageView` / `ImageView`.

#### 2) Ví dụ file đầy đủ

```tsx
import React from 'react';
import { View, Image, Text, StyleSheet } from 'react-native';

function ImageDemo() {
  return (
    <View style={styles.container}>
      <Text style={styles.label}>1) Ảnh từ mạng (URI)</Text>
      {/* BẮT BUỘC có width + height (hoặc flex) — nếu không, ảnh mạng thường không hiện */}
      <Image
        source={{ uri: 'https://picsum.photos/id/1/400/300' }}
        style={styles.remote}
        resizeMode="cover"
        onError={() => console.log('Tải ảnh lỗi — kiểm tra mạng / URL')}
      />

      <Text style={styles.label}>2) Ảnh local (require)</Text>
      {/*
        Đặt file vào src/assets/logo.png rồi bỏ comment dòng dưới.
        require phải là đường dẫn tĩnh (không ghép chuỗi động).
      */}
      {/* <Image source={require('../../assets/logo.png')} style={styles.local} /> */}
      <Text style={styles.hint}>Bỏ comment dòng require sau khi đã có file logo.png</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, padding: 16, backgroundColor: '#fff' },
  label: { marginTop: 16, marginBottom: 8, fontWeight: '600' },
  remote: { width: '100%', height: 200, borderRadius: 12, backgroundColor: '#EEE' },
  local: { width: 80, height: 80 },
  hint: { color: '#95A5A6', fontSize: 12 },
});

export default ImageDemo;
```

#### 3) Giải thích
| Code | Ý nghĩa |
|------|---------|
| `source={{ uri: 'https://...' }}` | Ảnh mạng — object có key `uri` |
| `source={require('./a.png')}` | Ảnh đóng gói cùng app — Metro bundle lúc build |
| `resizeMode="cover"` | Phủ kín khung, có thể cắt mép |
| `style` có `width`/`height` | **Bắt buộc với ảnh URI** |

#### 4) `resizeMode`
| Giá trị | Hành vi |
|---------|---------|
| `cover` | Phủ kín, có thể crop |
| `contain` | Hiện trọn ảnh, có thể dư viền |
| `stretch` | Kéo đúng khung (dễ méo) |
| `center` | Giữ kích thước gốc, căn giữa |

#### 5) Lỗi hay gặp
- Ảnh mạng không hiện → quên `width`/`height`.  
- `require('./' + name + '.png')` → **không được** (path phải tĩnh).  
- HTTP (không HTTPS) trên Android mới → bị chặn cleartext.

#### 6) ShopAI
Banner Home, ảnh SP trên `ProductCard` / `ProductDetail` dùng `source={{ uri: product.image }}`.

---

### 2.6.4. `<TextInput>` — Ô nhập liệu (Controlled Component)

#### 1) Là gì?
Ô người dùng gõ chữ. **Luôn** gắn với State: `value` + `onChangeText` (kiểm soát 2 chiều — Controlled).

#### 2) Ví dụ file đầy đủ

```tsx
import React, { useState } from 'react';
import { View, Text, TextInput, StyleSheet, KeyboardAvoidingView, Platform } from 'react-native';

function TextInputDemo() {
  // State giữ nội dung ô nhập
  const [keyword, setKeyword] = useState('');

  return (
    // KeyboardAvoidingView: đẩy UI lên khi bàn phím mở (iOS thường cần)
    <KeyboardAvoidingView
      style={styles.flex}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <View style={styles.box}>
        <Text style={styles.label}>Tìm sản phẩm ShopAI</Text>

        <TextInput
          value={keyword}                 // 1) hiển thị đúng state hiện tại
          onChangeText={setKeyword}       // 2) mỗi lần gõ → cập nhật state → re-render
          placeholder="Ví dụ: tai nghe"
          placeholderTextColor="#95A5A6"
          style={styles.input}
          autoCapitalize="none"           // không tự viết hoa
          autoCorrect={false}
          returnKeyType="search"          // nút trên bàn phím hiện chữ Search
          onSubmitEditing={() => {
            // 3) user bấm Search trên bàn phím
            console.log('Tìm:', keyword);
          }}
        />

        <Text style={styles.preview}>Bạn đang gõ: {keyword || '(trống)'}</Text>
      </View>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1, backgroundColor: '#fff' },
  box: { flex: 1, padding: 16, justifyContent: 'center' },
  label: { marginBottom: 8, fontWeight: '600', color: '#2C3E50' },
  input: {
    height: 48,
    borderWidth: 1,
    borderColor: '#E8E8E8',
    borderRadius: 12,
    paddingHorizontal: 16,
    backgroundColor: '#FAFAFA',
    fontSize: 16,
    color: '#2C3E50',
  },
  preview: { marginTop: 12, color: '#7F8C8D' },
});

export default TextInputDemo;
```

#### 3) Luồng dữ liệu (quan trọng — vẽ trong đầu)
```
User gõ phím
  → onChangeText nhận chuỗi mới
  → setKeyword(chuỗi)
  → Component re-render
  → TextInput nhận value={keyword} mới
  → Màn hình hiện đúng chữ vừa gõ
```
Nếu **quên** `value={keyword}`: ô nhập “lệch” state, rất khó debug.

#### 4) Props quan trọng
| Prop | Dùng khi |
|------|----------|
| `secureTextEntry` | Ô mật khẩu |
| `keyboardType="email-address"` | Email |
| `keyboardType="numeric"` | Chỉ số |
| `multiline` | Ô ghi chú nhiều dòng |
| `editable={false}` | Khóa không cho gõ |

#### 5) ShopAI
Login (email/password), ô tìm Home, ô chat AI — đều là `TextInput` (sau này bọc `ShopInput`).

---

### 2.6.5. `<ScrollView>` — Cuộn nội dung ngắn (form, trang tĩnh)

#### 1) Là gì?
`ScrollView` = một `View` **cuộn được**. Toàn bộ con bên trong được vẽ một lần rồi cuộn. Hợp form đăng nhập, trang chính sách, màn chi tiết ngắn — **không** hợp feed 200 sản phẩm.

#### 2) Mô hình UI

```
┌─────────────────────────┐
│ ▼ nội dung dài hơn màn  │  ← ScrollView (vùng nhìn thấy)
│  [ô email]              │
│  [ô mật khẩu]           │
│  [nút Đăng nhập]        │
│  đoạn chữ chính sách…   │
│  …(kéo tiếp xuống)…     │
└─────────────────────────┘
```

#### 3) File đầy đủ — `ScrollDemo.tsx`

```tsx
import React, { useState } from 'react';
import {
  ScrollView,
  View,
  Text,
  TextInput,
  Pressable,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
} from 'react-native';

export default function ScrollDemo() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');

  return (
    <KeyboardAvoidingView
      style={styles.flex}
      behavior={Platform.OS === 'ios' ? 'padding' : undefined}
    >
      <ScrollView
        style={styles.flex}
        contentContainerStyle={styles.content}
        keyboardShouldPersistTaps="handled"
        showsVerticalScrollIndicator={false}
      >
        <Text style={styles.title}>Đăng nhập ShopAI</Text>

        <TextInput
          style={styles.input}
          placeholder="Email"
          value={email}
          onChangeText={setEmail}
          keyboardType="email-address"
          autoCapitalize="none"
        />
        <TextInput
          style={styles.input}
          placeholder="Mật khẩu"
          value={password}
          onChangeText={setPassword}
          secureTextEntry
        />

        <Pressable style={styles.btn}>
          <Text style={styles.btnText}>Đăng nhập</Text>
        </Pressable>

        <Text style={styles.policy}>
          Kéo xuống để đọc tóm tắt điều khoản. ScrollView phù hợp form + vài đoạn chữ.
          Không dùng ScrollView để map() hàng trăm sản phẩm — hãy dùng FlatList.
        </Text>
      </ScrollView>
    </KeyboardAvoidingView>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1, backgroundColor: '#F5F5F5' },
  content: { padding: 16, paddingBottom: 40 },
  title: { fontSize: 22, fontWeight: '800', marginBottom: 16, color: '#2C3E50' },
  input: {
    height: 48,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#E5E5E5',
    backgroundColor: '#fff',
    paddingHorizontal: 14,
    marginBottom: 12,
  },
  btn: {
    height: 48,
    borderRadius: 12,
    backgroundColor: '#FF4D4F',
    alignItems: 'center',
    justifyContent: 'center',
    marginTop: 8,
  },
  btnText: { color: '#fff', fontWeight: '700' },
  policy: { marginTop: 24, lineHeight: 22, color: '#7F8C8D' },
});
```

#### 4) Props quan trọng
| Prop | Ý nghĩa |
|------|---------|
| `contentContainerStyle` | Style của **nội dung bên trong** (padding list) — khác `style` (khung cuộn) |
| `keyboardShouldPersistTaps="handled"` | Bấm nút khi bàn phím đang mở vẫn nhận sự kiện |
| `horizontal` | Cuộn ngang (banner nhỏ) |
| `showsVerticalScrollIndicator` | Ẩn/hiện thanh cuộn |

#### 5) Lỗi hay gặp
| Sai | Đúng |
|-----|------|
| `{products.map(...)}` 200 item trong ScrollView | `FlatList` |
| Nhầm `style` vs `contentContainerStyle` | `style` = khung; `contentContainerStyle` = padding nội dung |
| Quên `flex: 1` trên ScrollView | Không chiếm hết màn → cuộn kỳ lạ |

#### 6) ShopAI
Login form, Checkout tóm tắt, trang điều khoản — `ScrollView`. Trang Home sản phẩm — **FlatList/FlashList**.

---

### 2.6.6. `Button` / `TouchableOpacity` / `Pressable`

#### 1) Là gì?
Ba cách tạo vùng chạm. ShopAI **ưu tiên `Pressable`** (linh hoạt nhất: style theo `pressed`, hỗ trợ hitSlop…).

| Component | Khi nào dùng |
|-----------|--------------|
| `Button` | Demo nhanh — **khó style** (màu nền hạn chế trên Android) |
| `TouchableOpacity` | Còn phổ biến trong code cũ — mờ khi nhấn |
| `Pressable` | **Chuẩn mới** — ShopAI / ShopButton |

#### 2) Mô hình UI nút

```
┌──────────────────────────┐
│     Thêm vào giỏ         │  ← Pressable + Text bên trong
└──────────────────────────┘
     ↑ onPress = logic
     ↑ style = màu / bo góc / opacity khi pressed
```

#### 3) File đầy đủ — `PressableDemo.tsx`

```tsx
import React, { useState } from 'react';
import { View, Text, Pressable, StyleSheet, Alert } from 'react-native';

export default function PressableDemo() {
  const [count, setCount] = useState(0);

  const handleAdd = () => {
    setCount(prev => prev + 1);
    Alert.alert('ShopAI', 'Đã thêm vào giỏ');
  };

  return (
    <View style={styles.box}>
      <Text style={styles.label}>Số lượng đã thêm: {count}</Text>

      <Pressable
        onPress={handleAdd}
        onLongPress={() => Alert.alert('ShopAI', 'Giữ lâu — mở mua nhanh')}
        hitSlop={8}
        style={({ pressed }) => [styles.btn, pressed && styles.btnPressed]}
      >
        <Text style={styles.btnText}>Thêm vào giỏ</Text>
      </Pressable>

      <Pressable
        disabled={count === 0}
        onPress={() => setCount(0)}
        style={({ pressed }) => [
          styles.btnOutline,
          count === 0 && styles.btnDisabled,
          pressed && styles.btnPressed,
        ]}
      >
        <Text style={styles.btnOutlineText}>Xóa hết</Text>
      </Pressable>
    </View>
  );
}

const styles = StyleSheet.create({
  box: { flex: 1, justifyContent: 'center', padding: 24, gap: 12 },
  label: { textAlign: 'center', marginBottom: 8, fontSize: 18 },
  btn: {
    backgroundColor: '#FF4D4F',
    height: 48,
    borderRadius: 12,
    alignItems: 'center',
    justifyContent: 'center',
  },
  btnOutline: {
    height: 48,
    borderRadius: 12,
    borderWidth: 2,
    borderColor: '#FF4D4F',
    alignItems: 'center',
    justifyContent: 'center',
  },
  btnPressed: { opacity: 0.85 },
  btnDisabled: { opacity: 0.4 },
  btnText: { color: '#fff', fontWeight: '700', fontSize: 16 },
  btnOutlineText: { color: '#FF4D4F', fontWeight: '700', fontSize: 16 },
});
```

#### 4) Giải thích từng khối
| Khối | Ý nghĩa |
|------|---------|
| `onPress={handleAdd}` | Truyền **tham chiếu** hàm — không `onPress={handleAdd()}` |
| `style={({ pressed }) => ...}` | Pressable báo đang giữ tay → đổi opacity |
| `hitSlop={8}` | Mở rộng vùng chạm thêm 8px (nút nhỏ dễ bấm hơn) |
| `disabled` | Không nhận chạm + thường giảm opacity |
| `onLongPress` | Giữ lâu (mua nhanh, menu) |
| `Alert.alert` | Hộp thoại hệ thống (xem thêm mục 2.6.12) |

#### 5) Lỗi hay gặp
```tsx
// ❌ Gọi hàm ngay lúc render → bấm một cái chạy cả trăm lần / vòng lặp
<Pressable onPress={handleAdd()} />

// ✅
<Pressable onPress={handleAdd} />
```

#### 6) ShopAI
Mọi nút (`ShopButton`) bọc `Pressable`. `Button` gốc gần như không dùng trong Production.

---

### 2.6.7. `<FlatList>` — Danh sách dài (ảo hóa)

#### 1) Là gì?
`FlatList` chỉ **vẽ các dòng đang nằm trong vùng nhìn thấy** (+ buffer). Kéo xuống thì tái sử dụng cell. Đây là lý do list 500 sản phẩm vẫn mượt hơn `ScrollView` + `map`.

#### 2) Mô hình UI

```
┌─────────────────────────┐
│ Tai nghe Pro    1.5tr   │  ← chỉ các dòng này được mount
│ Ốp lưng           120k  │
│ Sạc 65W           450k  │
│ … (kéo) …               │
└─────────────────────────┘
     data[] ──renderItem──► từng dòng
```

#### 3) File đầy đủ — có Empty + Header

```tsx
import React from 'react';
import { View, Text, FlatList, StyleSheet } from 'react-native';

type Product = { id: string; name: string; price: number };

const DATA: Product[] = [
  { id: '1', name: 'Tai nghe Pro', price: 1500000 },
  { id: '2', name: 'Ốp lưng trong', price: 120000 },
  { id: '3', name: 'Sạc nhanh 65W', price: 450000 },
];

export default function FlatListDemo() {
  return (
    <View style={styles.flex}>
      <FlatList
        data={DATA}
        keyExtractor={(item) => item.id}
        renderItem={({ item, index }) => (
          <View style={styles.row}>
            <Text style={styles.index}>#{index + 1}</Text>
            <View style={styles.info}>
              <Text style={styles.name}>{item.name}</Text>
              <Text style={styles.price}>
                {item.price.toLocaleString('vi-VN')} đ
              </Text>
            </View>
          </View>
        )}
        ItemSeparatorComponent={() => <View style={styles.sep} />}
        ListHeaderComponent={
          <Text style={styles.header}>Danh sách mẫu ShopAI</Text>
        }
        ListEmptyComponent={
          <Text style={styles.empty}>Chưa có sản phẩm</Text>
        }
        contentContainerStyle={styles.listContent}
        initialNumToRender={8}
        windowSize={5}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  flex: { flex: 1, backgroundColor: '#F5F5F5' },
  listContent: { padding: 16, flexGrow: 1 },
  header: {
    marginBottom: 12,
    fontSize: 20,
    fontWeight: '700',
    color: '#2C3E50',
  },
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#fff',
    padding: 14,
    borderRadius: 10,
  },
  index: { width: 36, color: '#95A5A6', fontWeight: '700' },
  info: { flex: 1 },
  name: { fontSize: 16, fontWeight: '600', color: '#2C3E50' },
  price: { marginTop: 4, color: '#FF4D4F', fontWeight: '700' },
  sep: { height: 10 },
  empty: { textAlign: 'center', marginTop: 40, color: '#95A5A6' },
});
```

#### 4) Ba props bắt buộc + props hay dùng
| Prop | Vai trò |
|------|---------|
| `data` | Mảng nguồn |
| `keyExtractor` | Trả về `id` **string duy nhất** — tái sử dụng cell đúng |
| `renderItem` | `({ item, index }) => JSX` — UI một dòng |
| `ListHeaderComponent` / `ListFooterComponent` | Đầu/cuối list |
| `ListEmptyComponent` | Khi `data=[]` |
| `ItemSeparatorComponent` | Khe giữa các dòng |
| `onEndReached` | Gần cuối list → tải trang tiếp (Ch.6) |
| `refreshing` + `onRefresh` | Kéo để làm mới (Ch.4/6) |

#### 5) Lỗi hay gặp
| Sai | Hậu quả |
|-----|---------|
| `keyExtractor` trùng / dùng `index` khi list đổi thứ tự | Nhấp nháy sai item, state ô nhập loạn |
| Component nặng trong `renderItem` không `memo` | Giật khi cuộn (Ch.3) |
| Đặt FlatList trong ScrollView dọc | Cuộn xung đột, mất ảo hóa |

#### 6) ShopAI
Home sản phẩm, Cart dòng hàng, kết quả tìm kiếm. Ch.4 nâng `FlashList` + grid 2 cột.

---

### 2.6.8. `<SectionList>` — List có nhóm (danh mục)

#### 1) Là gì?
Giống FlatList nhưng data theo **section**: mỗi nhóm có `title` + `data[]`. Dùng màn “Danh mục”: Điện thoại / Phụ kiện / …

#### 2) Mô hình UI

```
┌─────────────────────────┐
│ Điện thoại              │  ← section header
│   iPhone 15             │
│   Galaxy S24            │
│ Phụ kiện                │  ← section header
│   Ốp lưng               │
└─────────────────────────┘
```

#### 3) File đầy đủ

```tsx
import React from 'react';
import { SectionList, Text, View, StyleSheet } from 'react-native';

const SECTIONS = [
  {
    title: 'Điện thoại',
    data: [
      { id: '1', name: 'iPhone 15' },
      { id: '2', name: 'Galaxy S24' },
    ],
  },
  {
    title: 'Phụ kiện',
    data: [
      { id: '3', name: 'Ốp lưng' },
      { id: '4', name: 'Sạc nhanh' },
    ],
  },
];

export default function SectionListDemo() {
  return (
    <SectionList
      sections={SECTIONS}
      keyExtractor={(item) => item.id}
      renderSectionHeader={({ section }) => (
        <View style={styles.sectionHeader}>
          <Text style={styles.sectionTitle}>{section.title}</Text>
        </View>
      )}
      renderItem={({ item }) => (
        <View style={styles.item}>
          <Text>{item.name}</Text>
        </View>
      )}
      stickySectionHeadersEnabled
      contentContainerStyle={{ paddingBottom: 24 }}
    />
  );
}

const styles = StyleSheet.create({
  sectionHeader: { backgroundColor: '#EEE', padding: 8 },
  sectionTitle: { fontWeight: '700', color: '#2C3E50' },
  item: {
    padding: 14,
    backgroundColor: '#fff',
    borderBottomWidth: 1,
    borderBottomColor: '#F0F0F0',
  },
});
```

#### 4) Khác FlatList chỗ nào?
| | FlatList | SectionList |
|--|----------|-------------|
| Prop data | `data={[]}` | `sections={[{ title, data }]}` |
| Header nhóm | Tự dựng trong data | `renderSectionHeader` |
| Dùng khi | List phẳng | Có nhóm / danh mục |

#### 5) ShopAI
Màn danh mục theo ngành hàng; bộ lọc nhóm (tuỳ chọn Sprint).

---

### 2.6.9. `<ActivityIndicator>` — Vòng loading

#### 1) Là gì?
Spinner hệ thống báo “đang tải”. Dùng khi `loading === true` (fetch API, submit form).

#### 2) Mô hình UI

```
┌─────────────────────────┐
│                         │
│          ⟳             │  ← ActivityIndicator
│     Đang tải...         │
│                         │
└─────────────────────────┘
```

#### 3) File đầy đủ

```tsx
import React, { useEffect, useState } from 'react';
import { View, Text, ActivityIndicator, StyleSheet } from 'react-native';

export default function LoadingDemo() {
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const t = setTimeout(() => setLoading(false), 2000);
    return () => clearTimeout(t);
  }, []);

  if (loading) {
    return (
      <View style={styles.center}>
        <ActivityIndicator size="large" color="#FF4D4F" />
        <Text style={styles.caption}>Đang tải sản phẩm...</Text>
      </View>
    );
  }

  return (
    <View style={styles.center}>
      <Text style={styles.done}>Tải xong!</Text>
    </View>
  );
}

const styles = StyleSheet.create({
  center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  caption: { marginTop: 12, color: '#7F8C8D' },
  done: { fontSize: 18, fontWeight: '700', color: '#2C3E50' },
});
```

#### 4) Props
| Prop | Giá trị thường dùng |
|------|---------------------|
| `size` | `'small'` \| `'large'` |
| `color` | Màu thương hiệu `#FF4D4F` |
| `animating` | `false` để dừng quay |

#### 5) ShopAI
Dùng cho nút bấm (Checkout), tải trang đơn giản, hoặc AI chat khi chờ phản hồi.

---

### 2.6.9b. Skeleton Loading (UI/UX Đẳng cấp) — Thay thế ActivityIndicator

#### 1) Là gì?
Trong các ứng dụng thương mại điện tử chuyên nghiệp (Shopee, Lazada), thay vì dùng vòng xoay `ActivityIndicator` nhàm chán giữa màn hình trống, hệ thống hiển thị một "khung xương" (Skeleton) mô phỏng cấu trúc UI đang tải. Điều này giúp giảm "nhận thức về thời gian chờ" (Perceived Wait Time) của người dùng.

#### 2) Mô hình UI

```
┌─────────────────────────┐
│ [ Hình vuông xám nhạt ] │  ← Skeleton Banner
│ [ Dòng chữ xám nhạt ]   │  ← Skeleton Title
│ [ Dòng chữ ngắn hơn ]   │  ← Skeleton Subtitle
└─────────────────────────┘
```

#### 3) File đầy đủ (Tự build cơ bản với Animated)

*Ghi chú: Thực tế ShopAI dùng `moti/skeleton` hoặc `react-native-reanimated` để có hiệu ứng sóng lấp lánh (shimmer).*

```tsx
import React, { useEffect, useRef } from 'react';
import { View, Animated, StyleSheet } from 'react-native';

export default function SkeletonDemo() {
  const fadeAnim = useRef(new Animated.Value(0.3)).current;

  useEffect(() => {
    Animated.loop(
      Animated.sequence([
        Animated.timing(fadeAnim, { toValue: 1, duration: 800, useNativeDriver: true }),
        Animated.timing(fadeAnim, { toValue: 0.3, duration: 800, useNativeDriver: true })
      ])
    ).start();
  }, [fadeAnim]);

  return (
    <View style={styles.card}>
      <Animated.View style={[styles.skeletonImage, { opacity: fadeAnim }]} />
      <Animated.View style={[styles.skeletonText, { opacity: fadeAnim }]} />
      <Animated.View style={[styles.skeletonTextSmall, { opacity: fadeAnim }]} />
    </View>
  );
}

const styles = StyleSheet.create({
  card: { padding: 16, backgroundColor: '#fff', borderRadius: 12, marginBottom: 12 },
  skeletonImage: { width: '100%', height: 120, backgroundColor: '#E0E0E0', borderRadius: 8 },
  skeletonText: { width: '80%', height: 16, backgroundColor: '#E0E0E0', borderRadius: 4, marginTop: 12 },
  skeletonTextSmall: { width: '50%', height: 16, backgroundColor: '#E0E0E0', borderRadius: 4, marginTop: 8 },
});
```

#### 4) ShopAI
Dùng Skeleton cho danh sách sản phẩm ở Home và trang Chi tiết (Detail) lúc gọi API (TanStack Query `isPending`). Đây là yếu tố sống còn của một "Luxury UI".

---

### 2.6.10. `<Modal>` — Lớp phủ / hộp thoại tùy biến

#### 1) Là gì?
Vẽ một lớp UI **đè lên** màn hiện tại (xác nhận xóa giỏ, bộ lọc, ảnh phóng to). Khác `Alert`: Modal do **bạn** thiết kế 100% giao diện.

#### 2) Mô hình UI

```
┌─────────────────────────┐
│  (màn Home mờ phía sau) │
│   ┌─────────────────┐   │
│   │ Xóa giỏ hàng?   │   │  ← Modal
│   │ [Hủy] [Xóa]     │   │
│   └─────────────────┘   │
└─────────────────────────┘
```

#### 3) File đầy đủ

```tsx
import React, { useState } from 'react';
import { View, Text, Modal, Pressable, StyleSheet } from 'react-native';

export default function ModalDemo() {
  const [visible, setVisible] = useState(false);

  return (
    <View style={styles.screen}>
      <Pressable style={styles.btn} onPress={() => setVisible(true)}>
        <Text style={styles.btnText}>Xóa giỏ hàng</Text>
      </Pressable>

      <Modal
        visible={visible}
        transparent
        animationType="fade"
        onRequestClose={() => setVisible(false)}
      >
        <View style={styles.backdrop}>
          <View style={styles.card}>
            <Text style={styles.title}>Xóa toàn bộ giỏ?</Text>
            <Text style={styles.body}>Thao tác không hoàn tác.</Text>
            <View style={styles.row}>
              <Pressable style={styles.secondary} onPress={() => setVisible(false)}>
                <Text>Hủy</Text>
              </Pressable>
              <Pressable
                style={styles.danger}
                onPress={() => {
                  setVisible(false);
                  // clearCart() ở Ch.6
                }}
              >
                <Text style={styles.btnText}>Xóa</Text>
              </Pressable>
            </View>
          </View>
        </View>
      </Modal>
    </View>
  );
}

const styles = StyleSheet.create({
  screen: { flex: 1, justifyContent: 'center', padding: 24 },
  btn: {
    backgroundColor: '#FF4D4F',
    padding: 14,
    borderRadius: 12,
    alignItems: 'center',
  },
  btnText: { color: '#fff', fontWeight: '700' },
  backdrop: {
    flex: 1,
    backgroundColor: 'rgba(0,0,0,0.45)',
    justifyContent: 'center',
    padding: 24,
  },
  card: { backgroundColor: '#fff', borderRadius: 16, padding: 20 },
  title: { fontSize: 18, fontWeight: '800', color: '#2C3E50' },
  body: { marginTop: 8, color: '#7F8C8D' },
  row: { flexDirection: 'row', justifyContent: 'flex-end', gap: 12, marginTop: 20 },
  secondary: { padding: 12 },
  danger: {
    backgroundColor: '#FF4D4F',
    paddingHorizontal: 16,
    paddingVertical: 12,
    borderRadius: 10,
  },
});
```

#### 4) Props quan trọng
| Prop | Ý nghĩa |
|------|---------|
| `visible` | Bật/tắt Modal (thường gắn State) |
| `transparent` | Nền Modal trong suốt → tự vẽ backdrop |
| `animationType` | `'none'` \| `'slide'` \| `'fade'` |
| `onRequestClose` | **Bắt buộc trên Android** khi bấm nút Back |

#### 5) ShopAI
Xác nhận xóa giỏ, chọn biến thể SP, popup hết hàng.

---

### 2.6.11. `<Switch>` — Công tắc Bật/Tắt

#### 1) Là gì?
Nút gạt 2 trạng thái (boolean). Dùng Dark Mode, “Nhận thông báo”, “Lưu địa chỉ”.

#### 2) File đầy đủ

```tsx
import React, { useState } from 'react';
import { View, Text, Switch, StyleSheet } from 'react-native';

export default function SwitchDemo() {
  const [enabled, setEnabled] = useState(true);

  return (
    <View style={styles.row}>
      <Text style={styles.label}>Nhận thông báo đơn hàng</Text>
      <Switch
        value={enabled}
        onValueChange={setEnabled}
        trackColor={{ false: '#E5E5E5', true: '#FFB4B4' }}
        thumbColor={enabled ? '#FF4D4F' : '#f4f3f4'}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  row: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    padding: 16,
    backgroundColor: '#fff',
  },
  label: { fontSize: 16, color: '#2C3E50', flex: 1, paddingRight: 12 },
});
```

#### 3) Lưu ý
Giống TextInput: **controlled** — luôn có `value` + `onValueChange`. ShopAI: toggle Dark Mode (Ch.3 Theme), bật sinh trắc học (Ch.8).

---

### 2.6.12. `Alert` — Hộp thoại hệ thống nhanh

#### 1) Là gì?
API (không phải component JSX) hiện hộp thoại native. Nhanh cho thông báo / xác nhận đơn giản. UI **không** tùy biến sâu → cần đẹp thì dùng `Modal`.

```tsx
import { Alert } from 'react-native';

Alert.alert('ShopAI', 'Đã thêm vào giỏ', [
  { text: 'Ở lại', style: 'cancel' },
  { text: 'Xem giỏ', onPress: () => {} },
]);
```

| Dùng Alert khi | Dùng Modal khi |
|----------------|----------------|
| Thông báo 1–2 nút, không cần brand UI | Cần layout riêng, ảnh, form nhỏ |

---

### 2.6.13. `SafeAreaView` — Tránh tai thỏ / thanh Home

#### 1) Là gì?
Đảm bảo nội dung không bị che bởi notch, Dynamic Island, thanh cử chỉ. **Chuẩn ShopAI:** lấy từ `react-native-safe-area-context` (không dùng bản deprecated trong `react-native` nếu có thể).

#### 2) Mô hình

```
┌─────────────────────────┐
│ ▓▓▓ tai thỏ / status ▓▓▓│  ← vùng KHÔNG vẽ nội dung quan trọng
│  ShopAI                 │  ← SafeAreaView bắt đầu dưới vùng này
│  ...                    │
│ ▓▓▓ thanh Home ▓▓▓▓▓▓▓▓│
└─────────────────────────┘
```

#### 3) Pattern bắt buộc trong App

```tsx
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';

export default function App() {
  return (
    <SafeAreaProvider>
      <SafeAreaView style={{ flex: 1 }} edges={['top', 'bottom']}>
        {/* màn hình */}
      </SafeAreaView>
    </SafeAreaProvider>
  );
}
```

| Khối | Ý nghĩa |
|------|---------|
| `SafeAreaProvider` | Bọc **gốc** app — cung cấp số đo vùng an toàn |
| `SafeAreaView` | Áp padding theo cạnh an toàn |
| `edges` | Chỉ pad các cạnh cần (vd header tự xử lý top → `edges={['bottom']}`) |

> Đào sâu notch / padding từng cạnh: **Chương 4**.

---

### 2.6.14. Bảng chọn nhanh — toàn bộ Core Components Chương 2

| Nhu cầu | Component | Độ sâu trong Ch.2 | File demo |
|---------|-----------|-------------------|-----------|
| Hộp bố cục | `View` | Đầy đủ | `ViewDemo` |
| Chữ | `Text` | Đầy đủ | `TextDemo` |
| Ảnh | `Image` | Đầy đủ | `ImageDemo` |
| Gõ liệu | `TextInput` | Đầy đủ (+ KeyboardAvoiding) | `TextInputDemo` |
| Form / trang ngắn | `ScrollView` | Đầy đủ | `ScrollDemo` |
| Nút | `Pressable` | Đầy đủ | `PressableDemo` |
| List dài | `FlatList` | Đầy đủ | `FlatListDemo` |
| List nhóm | `SectionList` | Đầy đủ | `SectionListDemo` |
| Loading | `ActivityIndicator` | Đầy đủ | `LoadingDemo` |
| Lớp phủ tùy UI | `Modal` | Đầy đủ | `ModalDemo` |
| Công tắc | `Switch` | Đầy đủ | `SwitchDemo` |
| Dialog nhanh | `Alert` | Đầy đủ | (API) |
| An toàn notch | `SafeAreaView` | Nhập môn | (pattern App) |

**Chưa dạy sâu ở Ch.2 (có chủ đích — chương sau):**
| Component / chủ đề | Chương |
|--------------------|--------|
| Flexbox lưới 2 cột, `RefreshControl` | Ch.4 |
| `StatusBar` chi tiết / Dark Mode | Ch.3–4 |
| FlashList, Reanimated | Ch.4 |
| Navigation screens | Ch.5 |

**Bài tập trước Sprint 2:** Tạo `src/screens/demos/`, chạy lần lượt `TextDemo` → `TextInputDemo` → `FlatListDemo` → `ModalDemo`. Trong `App.tsx` tạm `return <ModalDemo />`.

---

## 🌐 PHẦN 2.7: FETCH API & AXIOS NHẬP MÔN (Đề cương 2.2)

> Mục tiêu Chương 2: **biết gọi API và đưa JSON ra màn hình**. Caching, React Query, phân trang chuẩn → Chương 6. Backend NestJS → Chương 9.

### 2.7.1. Fetch API (có sẵn, không cần cài)

```tsx
async function loadProducts() {
  try {
    const res = await fetch('https://jsonplaceholder.typicode.com/posts?_limit=5');
    if (!res.ok) throw new Error(`HTTP ${res.status}`);
    const data = await res.json(); // bắt buộc await — body là stream
    return data;
  } catch (e) {
    console.error('Lỗi mạng:', e);
    throw e;
  }
}
```

**Trong component:**
```tsx
const [items, setItems] = useState([]);
const [loading, setLoading] = useState(true);

useEffect(() => {
  let alive = true;
  (async () => {
    try {
      const data = await loadProducts();
      if (alive) setItems(data);
    } finally {
      if (alive) setLoading(false);
    }
  })();
  return () => { alive = false; }; // tránh setState sau unmount
}, []);
```

### 2.7.2. Axios (thư viện — tiện interceptor, timeout)

```bash
npm install axios
```

```tsx
import axios from 'axios';

const api = axios.create({
  baseURL: 'https://jsonplaceholder.typicode.com',
  timeout: 10000,
});

// GET
const { data } = await api.get('/posts', { params: { _limit: 5 } });

// POST
await api.post('/posts', { title: 'ShopAI', body: 'hello', userId: 1 });
```

| | Fetch | Axios |
|---|-------|-------|
| Có sẵn? | Có | Cài thêm |
| JSON | Tự `res.json()` | Tự parse → `response.data` |
| Timeout | Tự viết / AbortController | Có sẵn |
| Interceptor (gắn Token) | Tự viết | Có sẵn — rất hữu ích Ch.6–9 |

**ShopAI:** Sprint 2 dùng **Fetch** cho đơn giản; từ Chương 6 ưu tiên Axios + React Query.

---

## 🏛️ PHẦN 2.8: KIẾN TRÚC THƯ MỤC ENTERPRISE (CLEAN ARCHITECTURE)

Tại sao lại cần kiến trúc thư mục?
Khi làm bài tập sinh viên, bạn chỉ có 2-3 file, vứt đâu cũng được. Nhưng một app như ShopAI sẽ có 50 màn hình, 200 components, 30 API. Nếu không có "Quy hoạch phân khu", dự án của bạn sẽ trở thành một mớ rác (Spaghetti Code).

**Triết lý Clean Architecture (Sự phân tách trách nhiệm):**
- **Tầng UI (Giao diện):** Chỉ chứa các hàm vẽ giao diện. Tuyệt đối không chứa logic tính toán phức tạp hay hàm gọi mạng (API).
- **Tầng Domain (Nghiệp vụ):** Nơi chứa các quy tắc kinh doanh (Ví dụ: Công thức tính giảm giá).
- **Tầng Data (Dữ liệu):** Nơi chuyên làm việc với Server/Database (Gọi API).

**Làm rõ mức độ áp dụng trong khóa học:**
- Sprint 2 tạo **bộ khung thư mục theo hướng Clean Architecture** (tách UI / data / utils).
- Các tầng Domain (use-case phức tạp) và Data (repository thật) sẽ được **đổ đầy dần** từ Chương 6–9, không bắt buộc viết hết ngay ngày đầu.

**Sơ đồ thư mục áp dụng cho dự án ShopAI:**
```text
ShopAI/
├── src/                      # BẮT BUỘC MỌI CODE LOGIC PHẢI NẰM TRONG ĐÂY
│   ├── assets/               # Hình ảnh tĩnh (.png, .jpg), Fonts chữ, Lottie animations
│   ├── components/           # Component dùng chung toàn app (Nút bấm, Card, Input)
│   │   └── ui/               # Atoms Design System (Typography, Button, Input) — Chương 3
│   ├── screens/              # Các màn hình lớn (Home, Cart, Checkout, Profile)
│   ├── navigation/           # File cấu hình luồng chuyển trang (Stack, Tab)
│   ├── store/                # Quản lý State toàn cục (Zustand — Chương 6)
│   ├── services/             # Giao tiếp với API (Axios/Fetch + React Query — Chương 6, 9)
│   ├── hooks/                # Custom Hooks tách logic khỏi UI (Chương 3+)
│   ├── data/                 # Mock data / fixtures dùng khi chưa có Backend
│   ├── utils/                # Hàm tiện ích dùng chung (formatCurrency, validateEmail)
│   ├── constants/            # Hằng số (Bảng màu COLORS, Kích thước SIZES, API_URL)
│   └── types/                # (Dành cho TypeScript) Nơi định nghĩa các Interface, Type
├── App.tsx                   # Trái tim của App, nơi khởi chạy các Provider bọc bên ngoài
├── babel.config.js           # Cấu hình trình biên dịch mã nguồn
└── package.json              # Chứa thông tin các thư viện bên thứ 3
```

### Tại sao cần cấu hình Path Aliases (Bí danh đường dẫn)?
Trong một màn hình nằm rất sâu ở `src/screens/Checkout/Payment/CreditCardScreen.tsx`, nếu muốn gọi một Nút bấm từ thư mục `components`, bạn phải `import` theo cách duyệt cây thư mục rất đau khổ:
`import ShopButton from '../../../../components/ShopButton';`
Trông cực kỳ rối mắt, và nếu bạn di chuyển file đi chỗ khác, đường dẫn sẽ gãy.

**Giải pháp Path Aliases:** Tạo ra các lối tắt bắt đầu bằng chữ `@`. Dù bạn đang ở ngóc ngách nào của dự án, bạn chỉ cần gõ:
`import ShopButton from '@components/ShopButton';`

Để làm được điều này, chúng ta phải cấu hình 2 file hệ thống: `babel.config.js` (để Máy tính hiểu lúc chạy) và `tsconfig.json` (để Cursor/VS Code hiểu lúc bạn gõ code).

---

## 🚀 THỰC CHIẾN SHOPAI (SPRINT 2: CẤU TRÚC + CORE COMPONENTS + FETCH)

**User Story:** *"Là học viên, tôi muốn dựng khung thư mục Enterprise, cấu hình Path Alias, và viết HomeScreen dùng đủ Core Components (View, Text, Image, TextInput, FlatList, Pressable) đồng thời Fetch thử dữ liệu từ mạng — đúng đề cương Chương 2."*


### 📋 Khung thực hành chương (đọc trước khi gõ code)

> Đây là **bài thực hành của Chương 2** (không phải “lab mỗi ngày”). Làm hết Sprint này = đạt mục tiêu chương. Hoàn thành đủ 11 Sprint = sản phẩm ShopAI theo `SHOPAI_HOAN_THIEN.md`.

| Hạng mục | Nội dung |
|----------|----------|
| **Thời lượng gợi ý** | 4–6 tiết |
| **Độ khó chương** | ★★☆☆☆ |
| **Đầu vào bắt buộc** | Sprint 1 PASS — app chạy được. |
| **Đầu ra sản phẩm** | Cấu trúc `src/` + Path Alias; HomeScreen đủ Core Components + Fetch list. |
| **Cách làm** | Làm **tuần tự từng Bước**. Gặp mốc ✓ bên dưới mà FAIL → dừng, sửa, rồi mới sang bước sau. |
| **Nghiệm thu cuối khóa** | Đối chiếu `SHOPAI_HOAN_THIEN.md` — mỗi Sprint chỉ tích thêm ô, không phá tính năng cũ. |

### ✓ Kiểm chứng theo mốc (trong lúc làm)

- **Sau Bước 1–4:** Import `@screens/...` không báo đỏ (đã reset Metro cache nếu cần).
- **Sau Bước 6:** HomeScreen hiện list từ Fetch; ô tìm / nút làm mới hoạt động.
- **Sau Bước 7–10:** App trỏ HomeScreen qua alias; đã commit.

> [!TIP]
> Xong Sprint 2, mở `SHOPAI_HOAN_THIEN.md` và tick các ô thuộc chương này. Mục tiêu cuối khóa: **mọi ô A/B/C/D (+ E đề cương) đều xanh** trong `SHOPAI_HOAN_THIEN.md` — đó mới là ShopAI hoàn thiện đẳng cấp.

### Liên hệ Lý thuyết → Thực hành

| Đề cương / Lý thuyết | Trong Sprint |
|----------------------|--------------|
| 2.1 View, Text, Image, TextInput | Header + ô tìm + ảnh sản phẩm |
| 2.1 Pressable | Nút "Làm mới" |
| 2.1 FlatList | Danh sách bài viết/sản phẩm mẫu |
| 2.2 Fetch API | `useEffect` + `fetch` JSONPlaceholder |
| Clean Architecture | Thư mục `src/` + `@screens` alias |

### Yêu cầu Nghiệm thu:
1. Đủ cấu trúc `src/` + Path Alias hoạt động (`@screens`, `@services`…).
2. `HomeScreen` có TextInput, Image, FlatList, Pressable.
3. Dữ liệu list lấy bằng **Fetch** (không hardcode toàn bộ).
4. `App.tsx` import `HomeScreen` qua `@screens/HomeScreen`.

---

#### Bước 1: Tạo cấu trúc thư mục (Cầm tay chỉ việc)

Trong Cursor/VS Code, ở cột bên trái (Explorer), bạn hãy tìm đến thư mục `src`. Nếu chưa có, hãy tạo nó. Sau đó, chúng ta sẽ tạo hàng loạt các thư mục con bên trong `src` để sắp xếp code gọn gàng (Clean Architecture).

**Cách 1 (Tạo bằng chuột - Dành cho người mới):**
1. Chuột phải vào thư mục gốc của dự án `ShopAI` -> Chọn **New Folder** -> Đặt tên là `src`.
2. Chuột phải vào thư mục `src` vừa tạo -> Chọn **New Folder** -> Tạo lần lượt các thư mục: `assets`, `components`, `screens`, `navigation`, `store`, `services`, `hooks`, `data`, `utils`, `constants`, `types`, `contexts`.
3. Bên trong thư mục `components`, tạo tiếp một thư mục tên là `ui`.

**Cách 2 (Tạo nhanh bằng Terminal):**
Mở Terminal trong Cursor (Ctrl + ` hoặc View > Terminal), dán lệnh sau và nhấn Enter:
```bash
mkdir -p src/{assets,components/ui,screens,navigation,store,services,hooks,data,utils,constants,types,contexts}
```

> Thư mục `contexts/` được tạo sẵn ở đây dù Chương 2 chưa dùng đến — Chương 3 sẽ dùng nó để chứa file `ThemeContext.tsx`.

#### Bước 2: Cài đặt thư viện Path Alias

Để không phải viết đường dẫn dài loằng ngoằng như `../../../../components/Button`, chúng ta cần cài một plugin.
Trong Terminal, gõ lệnh sau để tải thư viện về:
```bash
npm install --save-dev babel-plugin-module-resolver
```
*(Chờ dòng chữ hiển thị cài đặt thành công).*

#### Bước 3: Cấu hình file `babel.config.js`

1. Nhìn sang cột bên trái (Explorer), tìm file `babel.config.js` ở thư mục gốc (nằm ngay dưới cùng, ngang hàng với `package.json`).
2. Mở file đó ra, **xóa hết** nội dung cũ và **dán** nội dung mới này vào:

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
        },
      },
    ],
  ],
};
```
*(Lưu ý: Bấm Ctrl+S / Cmd+S để lưu file lại).*

#### Bước 4: Cấu hình file `tsconfig.json`

Để Editor (Cursor) không báo gạch chân đỏ khi bạn gõ chữ `@screens`, bạn phải bảo cho Editor biết.
1. Mở file `tsconfig.json` (nằm ở thư mục gốc).
2. Tìm đến phần `"compilerOptions": {` và thêm đoạn cấu hình `baseUrl` cùng `paths` vào ngay bên dưới nó. (Cẩn thận dấu phẩy).

Đoạn thêm vào sẽ trông như thế này:
```json
{
  "extends": "@react-native/typescript-config/tsconfig.json",
  "compilerOptions": {
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
      "@contexts/*": ["src/contexts/*"]
    }
  }
}
```

#### Bước 5: Tạo file gọi API (Tầng Services)

Chúng ta sẽ tách việc tải dữ liệu từ internet ra một file riêng để code gọn gàng.
1. Trong thư mục `src`, mở thư mục `services`.
2. Tạo một file mới (Chuột phải > **New File**) và đặt tên là `productApi.ts`.
3. Dán đoạn code sau vào và lưu lại:

```ts
// Khai báo kiểu dữ liệu trả về (TypeScript)
export type PostItem = {
  id: number;
  title: string;
  body: string;
};

// Hàm tải dữ liệu từ mạng Internet
export async function fetchSamplePosts(): Promise<PostItem[]> {
  const res = await fetch(
    'https://jsonplaceholder.typicode.com/posts?_limit=10',
  );
  if (!res.ok) {
    throw new Error(`HTTP ${res.status}`);
  }
  return res.json();
}
```

#### Bước 6: Viết màn hình HomeScreen

Đây là bước quan trọng nhất. Chúng ta sẽ áp dụng toàn bộ Core Components đã học (Text, Image, TextInput, FlatList...).
1. Trong thư mục `src`, mở thư mục `screens`.
2. Tạo một file mới tên là `HomeScreen.tsx`.
3. Dán toàn bộ mã nguồn bên dưới vào và Lưu lại. Hãy đọc các dòng comment (//) để hiểu luồng chạy.

```tsx
// 1. IMPORT ĐỒ NGHỀ TỪ BÊN NGOÀI
import React, { useCallback, useEffect, useRef, useState } from 'react';
import {
  View,
  Text,
  Image,
  TextInput,
  FlatList,
  Pressable,
  ActivityIndicator,
  StyleSheet,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
// Import hàm tải dữ liệu nhờ Path Alias @services
import { fetchSamplePosts, PostItem } from '@services/productApi';

// 2. TẠO COMPONENT HOMESCREEN
const HomeScreen = () => {
  // STATE: Quản lý biến nội bộ của màn hình
  const [keyword, setKeyword] = useState(''); // Chữ đang gõ
  const [posts, setPosts] = useState<PostItem[]>([]); // Danh sách bài viết
  const [loading, setLoading] = useState(true); // Vòng xoay chờ tải
  const [error, setError] = useState<string | null>(null); // Báo lỗi
  
  // Cờ "còn sống" tránh Memory Leak (Phần 2.5)
  const aliveRef = useRef(true);

  // HÀM: Chịu trách nhiệm gọi API
  const load = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchSamplePosts(); // Gọi sang file productApi.ts
      if (aliveRef.current) setPosts(data); // Cập nhật danh sách
    } catch (e) {
      if (aliveRef.current) setError('Không tải được dữ liệu.');
    } finally {
      if (aliveRef.current) setLoading(false); // Tắt vòng xoay
    }
  }, []);

  // USE EFFECT: Gọi hàm load() ngay lần đầu màn hình xuất hiện (Mount)
  useEffect(() => {
    aliveRef.current = true;
    load();
    return () => {
      aliveRef.current = false; // Cleanup khi thoát màn hình
    };
  }, [load]);

  // LOGIC: Lọc bài viết theo từ khóa (Không phân biệt hoa thường)
  const filtered = posts.filter(p =>
    p.title.toLowerCase().includes(keyword.toLowerCase()),
  );

  // 3. GIAO DIỆN (JSX)
  return (
    <SafeAreaView style={styles.safe}>
      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.brand}>ShopAI</Text>
        <Text style={styles.caption}>Sprint 2 — Core Components + Fetch</Text>
      </View>

      {/* Ảnh Banner tĩnh */}
      <Image
        source={{ uri: 'https://picsum.photos/800/200' }}
        style={styles.banner}
        resizeMode="cover"
      />

      {/* Ô tìm kiếm */}
      <TextInput
        value={keyword}
        onChangeText={setKeyword}
        placeholder="Tìm theo tiêu đề..."
        placeholderTextColor="#95A5A6"
        style={styles.input}
        autoCapitalize="none"
      />

      {/* Nút bấm tải lại danh sách */}
      <Pressable
        onPress={load}
        style={({ pressed }) => [styles.btn, pressed && { opacity: 0.85 }]}
      >
        <Text style={styles.btnText}>Làm mới danh sách</Text>
      </Pressable>

      {/* Vòng xoay Loading (Chỉ hiện khi loading = true) */}
      {loading && <ActivityIndicator style={{ marginTop: 24 }} color="#FF4D4F" />}
      
      {/* Báo lỗi đỏ (Chỉ hiện khi error có dữ liệu) */}
      {error && <Text style={styles.error}>{error}</Text>}

      {/* Danh sách FlatList mượt mà */}
      {!loading && !error && (
        <FlatList
          data={filtered}
          keyExtractor={item => String(item.id)}
          contentContainerStyle={{ paddingBottom: 24 }}
          ListEmptyComponent={
            <Text style={styles.empty}>Không có kết quả cho từ khóa này</Text>
          }
          renderItem={({ item }) => (
            <View style={styles.card}>
              <Text style={styles.cardTitle} numberOfLines={2}>
                {item.title}
              </Text>
              <Text style={styles.cardBody} numberOfLines={2}>
                {item.body}
              </Text>
            </View>
          )}
        />
      )}
    </SafeAreaView>
  );
};

// 4. BẢN VẼ GIAO DIỆN (STYLESHEET)
const styles = StyleSheet.create({
  safe: { flex: 1, backgroundColor: '#F5F5F5' },
  header: { padding: 16, backgroundColor: '#fff' },
  brand: { fontSize: 28, fontWeight: '800', color: '#FF4D4F' },
  caption: { color: '#7F8C8D', marginTop: 4 },
  banner: { width: '100%', height: 120, marginTop: 8 },
  input: {
    margin: 16,
    height: 48,
    borderRadius: 12,
    borderWidth: 1,
    borderColor: '#E8E8E8',
    paddingHorizontal: 16,
    backgroundColor: '#fff',
  },
  btn: {
    marginHorizontal: 16,
    marginBottom: 8,
    backgroundColor: '#FF4D4F',
    paddingVertical: 12,
    borderRadius: 12,
    alignItems: 'center',
  },
  btnText: { color: '#fff', fontWeight: '600' },
  card: {
    marginHorizontal: 16,
    marginTop: 10,
    padding: 14,
    backgroundColor: '#fff',
    borderRadius: 12,
  },
  cardTitle: { fontWeight: '700', color: '#2C3E50', marginBottom: 6 },
  cardBody: { color: '#7F8C8D' },
  error: { color: '#FF0000', textAlign: 'center', marginTop: 16 },
  empty: { textAlign: 'center', color: '#95A5A6', marginTop: 24 },
});

// 5. XUẤT KHẨU COMPONENT (BẮT BUỘC)
export default HomeScreen;
```

#### Bước 7: Cập nhật `App.tsx` để hiển thị `HomeScreen`

Bây giờ chúng ta cần nói cho hệ thống biết hãy hiển thị `HomeScreen` thay vì màn hình chào mặc định ở Sprint 1.
1. Mở file `App.tsx` (ở thư mục gốc).
2. Xóa toàn bộ code cũ đi và thay bằng:

```tsx
import React from 'react';
import { SafeAreaProvider } from 'react-native-safe-area-context';
// Nhờ cấu hình Alias ở Bước 3,4, ta import cực kỳ ngắn gọn
import HomeScreen from '@screens/HomeScreen';

function App(): React.JSX.Element {
  return (
    // SafeAreaProvider bọc ngoài cùng để tính toán phần "Tai thỏ" (Notch) trên iPhone
    <SafeAreaProvider>
      <HomeScreen />
    </SafeAreaProvider>
  );
}

export default App;
```

#### Bước 8: Dọn dẹp bộ nhớ đệm (Reset Cache) và Chạy App

Vì chúng ta vừa cấu hình thư viện `babel` mới (Path Alias), React Native cần phải xóa bộ nhớ đệm cũ đi để cập nhật.
1. Mở Terminal, **tắt tiến trình cũ** (bấm Ctrl + C vài lần).
2. Chạy lệnh sau để bật lại máy chủ đóng gói (Metro bundler) và bắt buộc xóa cache:
```bash
npm start -- --reset-cache
```
3. Mở một Tab Terminal thứ 2 (Bấm dấu `+` trong cửa sổ Terminal của Cursor), gõ lệnh khởi chạy:
```bash
npm run ios 
# hoặc npm run android
```

**✅ Tự kiểm tra kết quả:**
- Chờ ứng dụng lên, bạn sẽ thấy ảnh Banner và danh sách các thẻ trắng (bài viết tiếng Latinh).
- Gõ vào ô tìm kiếm chữ "sunt" -> Dữ liệu bên dưới phải lọc lại ngay lập tức.
- Bấm nút "Làm mới danh sách" -> Thấy vòng tròn đỏ xoay xoay rồi tải lại.
- Tắt WiFi máy tính, bấm Làm mới -> Báo dòng chữ đỏ "Không tải được dữ liệu...".

#### Bước 9: Lưu trữ lên Git (Bắt buộc)

Sau khi kiểm chứng mọi thứ hoạt động hoàn hảo, đừng quên lưu lại thành quả.
Mở Terminal gõ lần lượt:
```bash
git add .
git commit -m "Sprint 2: Tạo cấu trúc thư mục, Path Alias, gọi Fetch API hiển thị HomeScreen"
git push origin main
```

---

## 📝 TỔNG KẾT CHƯƠNG 2 (theo đề cương)

| Mục đề cương | Đã học |
|--------------|--------|
| **1.2.1** Component & JSX | Có — Phần 2.2 |
| **1.2.2** Props & State | Có — Phần 2.3 |
| **1.2.3** Xử lý sự kiện | Có — Pressable `onPress`, TextInput `onChangeText` |
| **1.2.4** Style | Có — **Phần 2.4** StyleSheet cầm tay + dùng lại ở Core Components |
| 2.1.1 View, Text, Image, TextInput, ScrollView | Có (đầy đủ + mô hình UI) |
| 2.1.2 Button / Touchable / Pressable | Có (ưu tiên Pressable) |
| 2.1.3 FlatList, SectionList | Có |
| *(bổ sung thực chiến)* | ActivityIndicator, Modal, Switch, Alert, SafeAreaView |
| 2.2.1 Fetch | Có + Sprint |
| 2.2.2 Axios | Có (lý thuyết; cài khi cần) |
| *(Hooks nền)* | `useState` / `useEffect` — Phần 2.5 |

**Checklist:**
- [ ] Phân biệt **Props** (từ cha, read-only) và **State** (nội bộ, đổi → re-render)
- [ ] Viết được Functional Component + JSX
- [ ] Phân biệt ScrollView vs FlatList vs SectionList
- [ ] Viết TextInput controlled (`value` + `onChangeText`)
- [ ] Fetch JSON và đổ vào FlatList
- [ ] Path alias `@screens` / `@services` chạy được
- [ ] Hiểu Bridge/JSI ở mức “vì sao list dài cần ảo hóa”

---


### ✅ Checklist nghiệm thu Sprint 2 (tick trước khi sang Chương 3)
- [ ] Thư mục `src/` đủ nhánh (screens, components, services, …)
- [ ] Path Alias `@screens` / `@services` import được (Metro không đỏ)
- [ ] HomeScreen có TextInput + FlatList/Image/Pressable
- [ ] List dữ liệu đến từ **Fetch** (không hardcode toàn bộ list)
- [ ] `App.tsx` render `HomeScreen` qua alias + `SafeAreaProvider`
- [ ] `git commit` Sprint 2

## 🎯 CHUẨN BỊ CHO CHƯƠNG 3

Chương 3 (Design System) sẽ:
- Chuẩn hóa Pressable/TextInput thành **ShopButton / ShopInput / Typography**
- Dạy `useMemo` / `useCallback` / `React.memo` (đề cương Hooks một phần)
- Custom Hooks tách logic

**Chương 4 (Flexbox + List sâu)** sẽ nâng FlatList → FlashList + phân trang UI.  
**Chương 6** sẽ nâng Fetch → Axios + React Query + pagination chuẩn đề cương.

**Chúc bạn học tốt!** 🚀
