---
sidebar_position: 4
title: Chương 4
---

# GIÁO TRÌNH LÝ THUYẾT & THỰC CHIẾN

## CHƯƠNG 4: UI/UX ENGINEERING, FLEXBOX MASTERY & LIST VIRTUALIZATION

**Thời lượng:** 6 tiết Lý thuyết + 4 tiết Thực hành

---

> [!IMPORTANT]
> **Thực hành chương = Sprint ShopAI cuối file.** Hoàn thành Sprint này để đạt mục tiêu chương. Hoàn thành đủ 11 chương theo `SHOPAI_HOAN_THIEN.md` = sản phẩm ShopAI **hoàn thiện đẳng cấp**.

## 📚 MỤC TIÊU HỌC TẬP

Sau khi hoàn thành chương này, học viên sẽ:

- ✅ **Làm chủ Flexbox:** Không còn phải đoán mò (`guess-driven development`) khi căn chỉnh giao diện. Hiểu rõ trục chính (Main axis) và trục phụ (Cross axis).
- ✅ Xử lý triệt để vấn đề giao diện bị che khuất bởi "Tai thỏ" (Notch), Dynamic Island (iOS) và Thanh điều hướng (Android) với `SafeAreaView`.
- ✅ **Giải phẫu List Virtualization:** Hiểu tận gốc cơ chế "Tái chế View" (Recycling) của `FlatList`. Tại sao dùng `ScrollView` cho danh sách ngàn dòng lại làm cháy RAM điện thoại.
- ✅ Biết cách sử dụng `FlashList` (Thư viện siêu tốc của Shopify) thay thế FlatList trong các dự án hiệu năng cao.
- ✅ Hiểu nguyên lý hoạt động của `Reanimated 3` (Chạy Animation trên luồng UI Thread thay vì JS Thread).
- ✅ Thiết kế và xây dựng tính năng **Advanced Search & Filter** (Tìm kiếm và lọc nâng cao) sử dụng kỹ thuật Debounce và Bottom Sheet/Modal.
- ✅ **Thực chiến:** Xây dựng màn hình Trang chủ (HomeScreen) của ShopAI với Danh sách Sản phẩm chia 2 cột, mượt mà ở tốc độ 60FPS.

---

## 📐 PHẦN 4.1: FLEXBOX MASTERY - LÀM CHỦ KHÔNG GIAN BỐ CỤC

React Native sử dụng Yoga Engine (viết bằng C++) để dịch các quy tắc Flexbox thành tọa độ X, Y trên màn hình điện thoại. Khác với Web (CSS mặc định xếp ngang từ trái sang phải), **Flexbox trong React Native xếp dọc từ trên xuống dưới theo mặc định.**

### 4.1.0 Flexbox nhìn thấy được (minh họa UI)

Phần này là bản đồ "cầm tay chỉ việc" — mỗi khái niệm Flexbox đều đi kèm hình minh họa khung điện thoại để bạn **thấy** trước khi code, tránh học vẹt lý thuyết suông.

#### A. `flexDirection`: dọc (`column`) hay ngang (`row`)?

Mặc định của React Native là `column` (khác với Web là `row`). Đây là khung xương của MỌI layout:

```text
flexDirection: 'column'  (MẶC ĐỊNH của RN)   flexDirection: 'row'
┌─────────────────────┐                      ┌─────────────────────┐
│ ┌─────────────────┐ │                      │ ┌───┐┌───┐┌───┐      │
│ │      Box 1      │ │                      │ │Box││Box││Box│      │
│ └─────────────────┘ │                      │ │ 1 ││ 2 ││ 3 │      │
│ ┌─────────────────┐ │                      │ └───┘└───┘└───┘      │
│ │      Box 2      │ │                      │                      │
│ └─────────────────┘ │                      │                      │
│ ┌─────────────────┐ │                      │                      │
│ │      Box 3      │ │                      │                      │
│ └─────────────────┘ │                      │                      │
└─────────────────────┘                      └─────────────────────┘
   Main Axis: ↓ (dọc)                           Main Axis: → (ngang)
   Cross Axis: ↔ (ngang)                         Cross Axis: ↕ (dọc)
```

**Ghi nhớ cốt lõi:** `flexDirection` quyết định Trục Chính (Main Axis). `justifyContent` LUÔN căn theo Trục Chính. `alignItems` LUÔN căn theo Trục Phụ (vuông góc với Trục Chính). Đây là nguồn gốc của 90% lỗi "căn hoài không đúng" ở người mới.

#### B. `justifyContent`: căn dọc theo Trục Chính

Giả sử `flexDirection: 'row'` (Trục Chính = ngang), 3 Box nhỏ hơn chiều rộng màn hình:

```text
justifyContent: 'flex-start'  (MẶC ĐỊNH)
┌─────────────────────────────────┐
│ [Box1][Box2][Box3]               │
└─────────────────────────────────┘

justifyContent: 'center'
┌─────────────────────────────────┐
│        [Box1][Box2][Box3]        │
└─────────────────────────────────┘

justifyContent: 'space-between'
┌─────────────────────────────────┐
│ [Box1]      [Box2]      [Box3]  │
└─────────────────────────────────┘
  ↑ sát mép trái            ↑ sát mép phải, khoảng cách CHỈ ở giữa

justifyContent: 'space-around'
┌─────────────────────────────────┐
│   [Box1]    [Box2]    [Box3]    │
└─────────────────────────────────┘
  ↑ có khoảng cách nhỏ ở 2 mép ngoài (bằng 1 nửa khoảng giữa)

justifyContent: 'flex-end'
┌─────────────────────────────────┐
│               [Box1][Box2][Box3] │
└─────────────────────────────────┘
```

#### C. `alignItems`: căn dọc theo Trục Phụ

Vẫn `flexDirection: 'row'` (Trục Chính = ngang → Trục Phụ = dọc), Box cha cao hơn Box con nhiều:

```text
alignItems: 'flex-start'         alignItems: 'center'            alignItems: 'stretch' (MẶC ĐỊNH)
┌───────────────────┐            ┌───────────────────┐           ┌───────────────────┐
│[Box1][Box2][Box3] │            │                   │           │[Box1][Box2][Box3] │
│                   │            │[Box1][Box2][Box3] │           │[    ][    ][    ] │
│                   │            │                   │           │[    ][    ][    ] │
└───────────────────┘            └───────────────────┘           └───────────────────┘
 Box con dính mép trên            Box con nằm chính giữa dọc      Box con TỰ GIÃN cao
                                                                  bằng chiều cao Box cha
                                                                  (chỉ khi Box con KHÔNG
                                                                   set height cố định)

alignItems: 'flex-end'
┌───────────────────┐
│                   │
│                   │
│[Box1][Box2][Box3] │
└───────────────────┘
 Box con dính mép dưới
```

> [!IMPORTANT]
> `stretch` là giá trị MẶC ĐỊNH của `alignItems` — đây là lý do vì sao nhiều bạn không set `width` cho `<View>` con mà nó vẫn tự giãn full chiều ngang (khi `flexDirection: 'column'`). Nếu bạn không muốn bị giãn, phải set `alignItems: 'flex-start'` (hoặc `center`/`flex-end`) cho Box cha, hoặc set cứng `width` cho Box con.

#### D. Wireframe Product Card — nơi bạn sẽ dùng `flexDirection: 'row'` thật sự (Sprint ShopAI)

Đây chính là bố cục `ProductCard` dạng danh sách ngang (list-item), khác với dạng Grid ở Sprint 4 phía dưới — dùng khi hiển thị "Sản phẩm đã xem" hoặc "Giỏ hàng":

```text
flexDirection: 'row', alignItems: 'center'  (Card cha)
┌──────────────────────────────────────────────────┐
│ ┌──────────┐  ┌──────────────────────────────┐   │
│ │          │  │ Tai nghe Bluetooth Pro         │   │ ← Trục Chính: → (row)
│ │  ẢNH SP  │  │ ⭐⭐⭐⭐☆ (120 đánh giá)         │   │
│ │ (Image)  │  │ 1.500.000 đ        [Mua ngay]  │   │ ← Trục Phụ: ↕ (center)
│ │          │  │                                │   │
│ └──────────┘  └──────────────────────────────┘   │
│  flex: 0 (kích        flex: 1 (chiếm hết          │
│  thước cố định)        phần còn lại)              │
└──────────────────────────────────────────────────┘
```

Cấu trúc JSX tương ứng (khối `View` cha bọc `flexDirection: 'row'`, khối bên phải dùng `flex: 1` để tự giãn lấp đầy không gian còn lại — đây chính là mẫu bố cục "ảnh trái, chữ phải" xuất hiện lặp lại xuyên suốt các màn hình danh sách của ShopAI):

```tsx
<View style={{ flexDirection: "row", alignItems: "center", padding: 12 }}>
  {/* Cột trái: ảnh, kích thước cố định, KHÔNG dùng flex */}
  <Image
    source={{ uri: product.image }}
    style={{ width: 80, height: 80, borderRadius: 8 }}
  />

  {/* Cột phải: chữ, dùng flex: 1 để tự giãn lấp đầy phần còn lại của hàng */}
  <View style={{ flex: 1, marginLeft: 12 }}>
    <Text numberOfLines={2}>{product.name}</Text>
    <Text style={{ color: "red", fontWeight: "bold" }}>{product.price}</Text>
  </View>
</View>
```

#### E. File demo chạy được ngay: `FlexboxDemo.tsx`

Tạo file này ở `src/screens/FlexboxDemo.tsx` (hoặc bất kỳ đâu, tạm thời gắn vào `App.tsx` để chạy thử) — 4 khối minh họa Row/Column/JustifyContent/AlignItems trên cùng 1 `ScrollView`, có nút bấm chuyển đổi (toggle) `justifyContent` để tự tay quan sát sự khác biệt trên máy thật:

```tsx
// src/screens/FlexboxDemo.tsx
import React, { useState } from "react";
import {
  View,
  Text,
  ScrollView,
  StyleSheet,
  TouchableOpacity,
  FlexAlignType,
} from "react-native";

// Ô màu nhỏ dùng chung cho mọi demo, có nhãn số thứ tự để dễ quan sát thứ tự sắp xếp
const Box = ({
  label,
  color = "#4F46E5",
}: {
  label: string | number;
  color?: string;
}) => (
  <View style={[styles.box, { backgroundColor: color }]}>
    <Text style={styles.boxText}>{label}</Text>
  </View>
);

const JUSTIFY_OPTIONS = [
  "flex-start",
  "center",
  "flex-end",
  "space-between",
  "space-around",
] as const;

const ALIGN_OPTIONS: FlexAlignType[] = [
  "flex-start",
  "center",
  "flex-end",
  "stretch",
];

export default function FlexboxDemo() {
  // Toggle để tự tay đổi justifyContent/alignItems và xem layout thay đổi ngay lập tức
  const [justify, setJustify] =
    useState<(typeof JUSTIFY_OPTIONS)[number]>("flex-start");
  const [align, setAlign] = useState<FlexAlignType>("stretch");

  return (
    <ScrollView contentContainerStyle={styles.scrollContent}>
      {/* ===== DEMO 1: flexDirection column (mặc định) ===== */}
      <Text style={styles.sectionTitle}>
        1. flexDirection: 'column' (mặc định)
      </Text>
      <View style={[styles.demoFrame, { flexDirection: "column" }]}>
        <Box label={1} />
        <Box label={2} />
        <Box label={3} />
      </View>

      {/* ===== DEMO 2: flexDirection row ===== */}
      <Text style={styles.sectionTitle}>2. flexDirection: 'row'</Text>
      <View style={[styles.demoFrame, { flexDirection: "row" }]}>
        <Box label={1} />
        <Box label={2} />
        <Box label={3} />
      </View>

      {/* ===== DEMO 3: justifyContent (có nút bấm đổi giá trị) ===== */}
      <Text style={styles.sectionTitle}>
        3. justifyContent (Trục Chính) — đang là: {justify}
      </Text>
      <View style={styles.toggleRow}>
        {JUSTIFY_OPTIONS.map((option) => (
          <TouchableOpacity
            key={option}
            style={styles.toggleBtn}
            onPress={() => setJustify(option)}
          >
            <Text style={styles.toggleText}>{option}</Text>
          </TouchableOpacity>
        ))}
      </View>
      <View
        style={[
          styles.demoFrame,
          { flexDirection: "row", justifyContent: justify },
        ]}
      >
        <Box label={1} />
        <Box label={2} />
        <Box label={3} />
      </View>

      {/* ===== DEMO 4: alignItems (có nút bấm đổi giá trị) ===== */}
      <Text style={styles.sectionTitle}>
        4. alignItems (Trục Phụ) — đang là: {align}
      </Text>
      <View style={styles.toggleRow}>
        {ALIGN_OPTIONS.map((option) => (
          <TouchableOpacity
            key={option}
            style={styles.toggleBtn}
            onPress={() => setAlign(option)}
          >
            <Text style={styles.toggleText}>{option}</Text>
          </TouchableOpacity>
        ))}
      </View>
      <View
        style={[
          styles.demoFrame,
          styles.tallFrame,
          { flexDirection: "row", alignItems: align },
        ]}
      >
        <Box label={1} />
        <Box label={2} />
        <Box label={3} />
      </View>

      {/* ===== DEMO 5 (bonus): flex: 1 chia tỉ lệ không gian ===== */}
      <Text style={styles.sectionTitle}>
        5. flex: 1 vs flex: 2 (chia tỉ lệ)
      </Text>
      <View style={[styles.demoFrame, { flexDirection: "row", height: 80 }]}>
        <View style={[styles.flexBox, { flex: 1, backgroundColor: "#F59E0B" }]}>
          <Text style={styles.boxText}>flex: 1</Text>
        </View>
        <View style={[styles.flexBox, { flex: 2, backgroundColor: "#EF4444" }]}>
          <Text style={styles.boxText}>flex: 2</Text>
        </View>
      </View>
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  scrollContent: {
    padding: 16,
    paddingBottom: 40,
  },
  sectionTitle: {
    fontSize: 15,
    fontWeight: "700",
    marginTop: 20,
    marginBottom: 8,
    color: "#111827",
  },
  // Khung điện thoại giả lập — có viền để nhìn rõ ranh giới cha/con
  demoFrame: {
    minHeight: 90,
    borderWidth: 1,
    borderColor: "#D1D5DB",
    borderRadius: 8,
    backgroundColor: "#F9FAFB",
    padding: 8,
  },
  tallFrame: {
    minHeight: 140, // Cao hơn để thấy rõ alignItems theo Trục Phụ
  },
  box: {
    width: 56,
    height: 56,
    marginRight: 6,
    marginBottom: 6,
    borderRadius: 6,
    justifyContent: "center",
    alignItems: "center",
  },
  boxText: {
    color: "#fff",
    fontWeight: "bold",
  },
  flexBox: {
    justifyContent: "center",
    alignItems: "center",
    marginRight: 4,
    borderRadius: 6,
  },
  toggleRow: {
    flexDirection: "row",
    flexWrap: "wrap",
    marginBottom: 8,
  },
  toggleBtn: {
    paddingHorizontal: 10,
    paddingVertical: 6,
    backgroundColor: "#E5E7EB",
    borderRadius: 6,
    marginRight: 6,
    marginBottom: 6,
  },
  toggleText: {
    fontSize: 12,
    color: "#374151",
  },
});
```

> [!TIP]
> Hãy thật sự copy file này vào project và bấm các nút toggle trên máy/giả lập thật. Việc TỰ TAY thấy `space-between` khác `space-around` như thế nào chỉ mất 2 phút nhưng nhớ lâu hơn 10 lần so với đọc định nghĩa suông.

#### F. Bảng tra cứu nhanh — prop nào cho ra hình gì trên màn hình

| Prop             | Giá trị hay dùng        | Nhìn trên màn hình sẽ thấy gì                                                                                      |
| ---------------- | ----------------------- | ------------------------------------------------------------------------------------------------------------------ |
| `flexDirection`  | `column` (mặc định)     | Các phần tử con xếp CHỒNG lên nhau từ trên xuống dưới                                                              |
| `flexDirection`  | `row`                   | Các phần tử con xếp CẠNH nhau từ trái sang phải                                                                    |
| `justifyContent` | `flex-start` (mặc định) | Các phần tử dồn hết về ĐẦU Trục Chính, phần còn lại của màn hình bỏ trống ở cuối                                   |
| `justifyContent` | `center`                | Cả cụm phần tử nằm giữa màn hình theo Trục Chính, khoảng trống chia đều 2 đầu                                      |
| `justifyContent` | `flex-end`              | Các phần tử dồn hết về CUỐI Trục Chính                                                                             |
| `justifyContent` | `space-between`         | Phần tử đầu dính mép đầu, phần tử cuối dính mép cuối, khoảng trống CHỈ nằm ở giữa các phần tử                      |
| `justifyContent` | `space-around`          | Mỗi phần tử có khoảng trống đều 2 bên (mép ngoài cùng có khoảng trống nhỏ bằng nửa khoảng giữa)                    |
| `justifyContent` | `space-evenly`          | Mọi khoảng trống (kể cả 2 mép ngoài) đều bằng nhau tuyệt đối                                                       |
| `alignItems`     | `stretch` (mặc định)    | Phần tử con tự GIÃN full theo Trục Phụ (VD: full chiều ngang khi `column`) — trừ khi con đã set kích thước cố định |
| `alignItems`     | `flex-start`            | Phần tử con dồn về mép ĐẦU Trục Phụ (VD: dính bên trái khi `column`)                                               |
| `alignItems`     | `center`                | Phần tử con nằm giữa theo Trục Phụ (VD: căn giữa ngang khi `column`)                                               |
| `alignItems`     | `flex-end`              | Phần tử con dồn về mép CUỐI Trục Phụ                                                                               |
| `alignSelf`      | (đặt ở phần tử CON)     | Ghi đè riêng `alignItems` của cha, chỉ áp dụng cho MỘT phần tử con này                                             |
| `flex: 1`        | số nguyên dương         | Phần tử CHIẾM HẾT không gian còn trống theo tỉ lệ (so với các anh em cùng có `flex`)                               |
| `flexWrap`       | `wrap`                  | Khi các phần tử tràn quá 1 hàng/cột, chúng tự XUỐNG DÒNG thay vì bị tràn ra ngoài màn hình                         |
| `flexShrink`     | `0`                     | Ngăn phần tử bị ép co lại nhỏ hơn kích thước gốc khi không đủ chỗ                                                  |
| `gap`            | số pixel                | Tạo khoảng cách đều giữa các phần tử con (thay thế margin thủ công từng phần tử)                                   |

#### G. Lỗi kinh điển hay gặp (Common Mistakes)

> [!WARNING]
> **Lỗi 1 — Quên `flex: 1` ở phần tử CHA:** Rất nhiều bạn set `flex: 1` cho `<ScrollView>` hoặc `<View>` con nhưng lại quên rằng phần tử CHA của nó (thường là component gốc `App` hoặc `<SafeAreaView>`) cũng phải có `flex: 1`. Nếu cha không có `flex: 1` (chiều cao mặc định = 0 hoặc theo nội dung), thì `flex: 1` ở con hoàn toàn VÔ NGHĨA — màn hình sẽ trắng trơn hoặc co lại đúng bằng nội dung, không giãn hết màn hình. Quy tắc: `flex: 1` phải được truyền liên tục từ gốc cây xuống, đứt đoạn ở đâu là hỏng ở đó.

> [!WARNING]
> **Lỗi 2 — Trộn lẫn `margin` thủ công với `justifyContent: 'space-between'`:** Khi bạn đã dùng `space-between` để tự động chia đều khoảng cách, nhưng lại CÒN thêm `marginRight` thủ công vào từng phần tử con, khoảng cách sẽ bị CỘNG DỒN lệch lạc — phần tử cuối có thể bị đẩy tràn ra khỏi màn hình vì margin dư thừa cộng thêm khoảng trống mà `space-between` đã tự tính. Quy tắc: chỉ chọn MỘT trong hai cách — hoặc dùng `justifyContent`/`gap` để tự động chia khoảng cách, hoặc tự set `margin` thủ công cho từng phần tử, không dùng lẫn lộn cả hai trên cùng một hàng.

> [!WARNING]
> **Lỗi 3 — Nhầm Trục Chính và Trục Phụ khi đổi `flexDirection`:** Khi đổi từ `column` sang `row`, `justifyContent` và `alignItems` sẽ ĐỔI VAI TRÒ cho nhau (căn ngang ↔ căn dọc). Đây là lý do code căn giữa hoạt động đúng ở màn hình A (`column`) nhưng bị "lệch trục" khi copy sang màn hình B đang dùng `row`.

### 1. Trục Chính (Main Axis) và Trục Phụ (Cross Axis)

Đây là chìa khóa để hiểu toàn bộ Flexbox:

- **`flexDirection` (Hướng đi):** Quyết định Trục Chính. Mặc định là `column` (dọc). Nếu bạn đổi thành `row`, Trục Chính sẽ thành chiều ngang.
- **`justifyContent`:** Căn chỉnh các phần tử DỌC THEO Trục Chính.
- **`alignItems`:** Căn chỉnh các phần tử DỌC THEO Trục Phụ (Trục vuông góc với Trục Chính).

**Tình huống thực tế:** Làm thế nào để căn giữa một Nút bấm chính xác vào tâm màn hình?

```tsx
<View
  style={{
    flex: 1, // Chiếm toàn bộ không gian màn hình
    justifyContent: "center", // Căn giữa theo trục dọc (Main Axis = column)
    alignItems: "center", // Căn giữa theo trục ngang (Cross Axis)
  }}
>
  <Text>Tôi nằm chính giữa!</Text>
</View>
```

### 2. Sức mạnh của `flex: 1`

Thay vì định nghĩa chiều cao cứng (`height: 300`), dùng `flex` giúp giao diện tự co giãn khớp với mọi kích thước màn hình (Từ iPhone SE bé xíu đến iPad to đùng).

- Nếu View A có `flex: 1` và View B có `flex: 2`, tổng không gian là 3 phần. View A chiếm 1/3 màn hình, View B chiếm 2/3 màn hình.

### 3. Absolute vs Relative Positioning (Định vị tuyệt đối)

Trong thiết kế Mobile, khi bạn muốn làm một nút "Dấu Cộng" lơ lửng ở góc dưới cùng bên phải màn hình (FAB - Floating Action Button), bạn phải dùng `position: 'absolute'`.

Nó sẽ tách phần tử đó ra khỏi dòng chảy bình thường (thoát khỏi Flexbox), và ghim chặt tọa độ vào mép của phần tử Cha (phần tử Cha phải có vị trí `relative`).

```tsx
// Ví dụ Nút Giỏ hàng nổi ở góc phải dưới
<View style={{ position: "absolute", bottom: 20, right: 20 }}>
  <Icon name="cart" />
</View>
```

---

## 🛡️ PHẦN 4.2: BẪY "TAI THỎ" VÀ SAFE AREA

Điện thoại ngày nay không còn là hình chữ nhật hoàn hảo. iPhone có Tai thỏ (Notch), Dynamic Island, và vạch quẹt Home ở đáy. Android có nốt ruồi camera.
Nếu bạn dùng `<View flex={1}>`, nội dung ở trên cùng sẽ bị phần khuyết của camera đâm thủng, nội dung ở dưới cùng sẽ bị thanh ngang Home đè lên. Không thể bấm được.

**Cách giải quyết kinh điển:** Thay thế `<View>` ngoài cùng bằng `<SafeAreaView>` của thư viện `react-native-safe-area-context`.
Nó sẽ gọi xuống hệ điều hành để tính toán chính xác số Pixel của tai thỏ, và tự động đẩy nội dung thụt lùi vào trong "Vùng An Toàn".

```tsx
import { SafeAreaView } from "react-native-safe-area-context";

export default function App() {
  return (
    // Bọc ngoài cùng bằng SafeAreaView thay vì View
    <SafeAreaView style={{ flex: 1, backgroundColor: "white" }}>
      <Text>Chữ này sẽ không bao giờ bị camera che mất</Text>
    </SafeAreaView>
  );
}
```

---

## 🚄 PHẦN 4.3: GIẢI PHẪU LIST VIRTUALIZATION VÀ FLATLIST

Đây là phần kiến thức quan trọng nhất để phân biệt một lập trình viên Mobile sơ cấp và một kỹ sư cấp cao.

### 1. Thảm họa ScrollView

Nếu bạn có một danh sách 10.000 người dùng lấy từ API. Bạn viết một vòng lặp `map` và nhét 10.000 thẻ `<View>` vào trong `<ScrollView>`.
**Điều gì xảy ra?**
Mặc dù màn hình điện thoại chỉ hiển thị được 10 người dùng cùng lúc, nhưng `<ScrollView>` vẫn bắt điện thoại phải nạp (Render) đồ họa cho cả 9.990 người dùng còn lại ở bên dưới màn hình.
Bộ nhớ RAM bị nhồi nhét, GPU quá tải. App của bạn giật tung tóe và lập tức báo lỗi **Out of Memory (OOM) - Văng App!**

### 2. Sự cứu rỗi của FlatList (Recycling / Virtualization)

`<FlatList>` là Component chuyên dụng để render danh sách vô hạn.
**Nguyên lý hoạt động (View Recycling):**

- FlatList tính toán chỉ cần vẽ đủ số phần tử lấp đầy màn hình (VD: 10 phần tử).
- Nó vẽ thêm 5 phần tử dự phòng (Buffer) ở trên và dưới. Tổng cộng chỉ vẽ 15 phần tử lên RAM.
- Khi bạn dùng ngón tay vuốt lên (cuộn xuống): Phần tử số 1 trôi lên khỏi màn hình -> FlatList lập tức **HỦY** đồ họa của phần tử số 1, lấy vùng nhớ đó đắp dữ liệu của phần tử số 16 vào và đẩy xuống đáy màn hình.
- Nhờ việc tái chế bộ nhớ (Recycling) liên tục, dù danh sách dài 1 triệu dòng, app của bạn vẫn chỉ tiêu tốn RAM đúng bằng 15 phần tử.

**Các Props sinh tử của FlatList:**

```tsx
<FlatList
  data={products}
  renderItem={({ item }) => <ProductCard data={item} />} // Hàm vẽ giao diện từng dòng
  keyExtractor={(item) => item.id} // Bắt buộc: Cung cấp ID duy nhất để RN biết cần hủy dòng nào
  initialNumToRender={10} // Số lượng vẽ lần đầu tiên (Nên bằng đúng số dòng che phủ màn hình)
  maxToRenderPerBatch={5} // Số dòng vẽ thêm mỗi khung hình khi cuộn nhanh (Càng cao càng mượt nhưng nặng CPU)
  windowSize={11} // Số trang nháp được giữ lại trong RAM (Mặc định 21 là quá lớn, nên giảm xuống 11 để tiết kiệm RAM)
  removeClippedSubviews={true} // Xóa triệt để các View không nằm trên màn hình (Android)
  onEndReached={loadMoreData} // Phân trang: Kích hoạt hàm load thêm data khi cuộn gần tới đáy
  onEndReachedThreshold={0.5} // Cách đáy nửa màn hình thì kích hoạt onEndReached
/>
```

### 3. FlashList (Shopify) - Vị vua mới của Hiệu năng

Mặc dù FlatList đã tốt, nhưng trên các máy Android giá rẻ (Samsung J7, Xiaomi Redmi), cuộn danh sách phức tạp bằng FlatList vẫn có thể xuất hiện các mảng màu trắng (Blank Space) do JS thread chưa kịp phối hợp render kịp tốc độ cuộn — di sản của thời kỳ Bridge, dù đã giảm nhiều với kiến trúc mới.

Shopify đã tạo ra thư viện `@shopify/flash-list`. Nó viết lại thuật toán Recycling bằng C++, tối ưu đáng kể so với FlatList và giảm mạnh hiện tượng Blank Space. Cú pháp sử dụng giống hệt FlatList 100%.

> [!NOTE]
> **Về prop `estimatedItemSize`:** FlashList **v1** (bản phổ biến hiện nay trên nhiều máy sinh viên) **bắt buộc** phải khai báo `estimatedItemSize`, nếu thiếu sẽ có warning và giảm hiệu năng. FlashList **v2** (nếu `npm install` cài được bản mới) có thể **không cần** prop này nữa — hãy xem changelog chính thức của `@shopify/flash-list` tại thời điểm bạn học. Ví dụ trong khóa học vẫn giữ `estimatedItemSize` để đảm bảo tương thích với v1 — phổ biến trên nhiều máy sinh viên.

_Đây là lựa chọn được khuyến nghị cho mọi app e-commerce hiện đại (Shopee, Lazada) cần danh sách dài, mượt._

---

## 🎬 PHẦN 4.4: ĐỈNH CAO UI VỚI REANIMATED 3 (KHÁI NIỆM)

Khi bạn muốn làm hiệu ứng: Người dùng vuốt màn hình xuống -> Thanh Header thu nhỏ lại và mờ dần.
Nếu dùng Animated API mặc định của React Native theo cách "ngây thơ" (tính toán trên JS Thread rồi đợi phối hợp với UI Thread mỗi khung hình): đây vốn là điểm nghẽn kinh điển thời kỳ Bridge — JS Thread và UI Thread phải qua lại nhiều lượt, dễ gây giật khựng (Stuttering) khi JS Thread đang bận việc khác (gọi API, tính toán nặng).

**Reanimated 3** ra đời để giải quyết đúng điểm nghẽn đó. Bằng sức mạnh của JSI (Kiến trúc mới), nó đưa ra khái niệm **Shared Value (Giá trị chia sẻ)** và **Worklets**.

- Toàn bộ logic toán học tính toán tọa độ Animation được ném thẳng sang chạy ngầm trên **Native UI Thread**.
- JavaScript Thread hoàn toàn thảnh thơi, không dính líu gì đến quá trình chạy animation.
  Kết quả: Animation mượt mà ở tốc độ khung hình cao kể cả khi JS Thread đang bị khóa chết bởi một vòng lặp nặng nề.

> [!NOTE]
> Dù ShopAI đã dùng **New Architecture** (JSI, không còn nghẽn theo kiểu Bridge cũ giữa JS ↔ Native), nguyên tắc "animation nên chạy trên UI thread bằng worklet, không phụ thuộc JS Thread" **vẫn luôn là lựa chọn ưu tiên** — vì JS Thread vẫn có thể bị bận (render, gọi API, tính toán) bất kể kiến trúc nào. Đây là lý do Reanimated vẫn là tiêu chuẩn cho animation mượt, không chỉ để "vá lỗi Bridge" của ngày xưa.

### 1. Bốn viên gạch nền của Reanimated 3

| API                                                        | Vai trò                                                                                                                                       | Chạy ở đâu                                            |
| ---------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| `useSharedValue(initial)`                                  | Tạo một "biến" đặc biệt sống song song giữa JS và UI Thread. Đọc/ghi qua `.value`, KHÔNG kích hoạt re-render React như `useState`.            | Cả hai, nhưng phép TÍNH TOÁN trên nó chạy ở UI Thread |
| `useAnimatedStyle(() => ({...}))`                          | "Worklet" — hàm nhỏ được Reanimated tự biên dịch để chạy trực tiếp trên UI Thread, trả về object style phụ thuộc vào 1 hay nhiều Shared Value | UI Thread (Worklet)                                   |
| `withTiming(toValue, config)`                              | Chuyển giá trị hiện tại sang `toValue` một cách mượt mà theo thời gian (VD: 400ms), có thể tùy chỉnh `easing`                                 | UI Thread                                             |
| `interpolate(value, inputRange, outputRange, extrapolate)` | "Nội suy" — ánh xạ 1 giá trị đang chạy (VD: vị trí cuộn) từ một khoảng số sang một khoảng số KHÁC (VD: từ pixel cuộn sang độ mờ opacity)      | UI Thread                                             |

`useSharedValue` + `withTiming` đã xuất hiện ở `ProductCard` (Sprint 4, Bước 3) để làm hiệu ứng mờ dần MỘT LẦN lúc mount. Phần tiếp theo giới thiệu `interpolate` — mảnh ghép còn thiếu để làm animation **bám theo hành động cuộn tay của người dùng** (scroll-driven), thay vì chỉ chạy một lần cố định.

### 2. Ví dụ đầy đủ: Collapsing Header — Header co lại khi cuộn xuống

**Ý tưởng:** Khi người dùng cuộn danh sách sản phẩm xuống, Header "Khám phá" ở trên cùng phải tự **co nhỏ chiều cao lại** và **chữ cũng nhỏ + mờ dần theo** — hiệu ứng kinh điển thấy ở hầu hết App thương mại điện tử (Shopee, Lazada, Tiki).

**Minh họa ASCII — 2 trạng thái trước/sau khi cuộn:**

```text
CUỘN Ở ĐẦU DANH SÁCH (scrollY = 0)          CUỘN XUỐNG (scrollY ≥ SCROLL_RANGE)
┌─────────────────────────────┐             ┌─────────────────────────────┐
│                             │             │ Khám phá         (nhỏ, mờ)  │ ← height co còn 64px
│                             │ ← height    ├─────────────────────────────┤
│        Khám phá             │   180px     │ [Ảnh SP1]      [Ảnh SP2]    │
│        (chữ to, rõ)          │             │ [Ảnh SP3]      [Ảnh SP4]    │
├─────────────────────────────┤             │ [Ảnh SP5]      [Ảnh SP6]    │
│ [Ảnh SP1]      [Ảnh SP2]    │             │ [Ảnh SP7]      [Ảnh SP8]    │
│ [Ảnh SP3]      [Ảnh SP4]    │             │ ...                         │
└─────────────────────────────┘             └─────────────────────────────┘
      scrollY = 0                                 scrollY = SCROLL_RANGE (64px đã cuộn)
```

**File hoàn chỉnh:** `src/screens/CollapsingHeaderDemo.tsx` (demo độc lập — an toàn khi chạy thử mà không đụng vào `HomeScreen` chính thức của Sprint 4):

```tsx
// src/screens/CollapsingHeaderDemo.tsx
import React from "react";
import { StyleSheet, View } from "react-native";
import Animated, {
  useSharedValue,
  useAnimatedScrollHandler,
  useAnimatedStyle,
  interpolate,
  Extrapolation,
} from "react-native-reanimated";
import { FlashList } from "@shopify/flash-list";
import ProductCard from "@components/ProductCard";
import { MOCK_PRODUCTS, Product } from "@data/mockProducts";
import { COLORS, SIZES } from "@constants/theme";

// FlashList không có sẵn bản "Animated" như FlatList (react-native đã export sẵn Animated.FlatList).
// Phải tự bọc bằng createAnimatedComponent để useAnimatedScrollHandler gắn được vào sự kiện cuộn của nó.
const AnimatedFlashList =
  Animated.createAnimatedComponent<
    React.ComponentProps<typeof FlashList<Product>>
  >(FlashList);

const HEADER_MAX_HEIGHT = 180; // Chiều cao Header lúc đầu (chưa cuộn)
const HEADER_MIN_HEIGHT = 64; // Chiều cao Header nhỏ nhất khi đã cuộn đủ xa
const SCROLL_RANGE = HEADER_MAX_HEIGHT - HEADER_MIN_HEIGHT; // Cuộn 116px là co xong hoàn toàn

export default function CollapsingHeaderDemo() {
  // Shared Value giữ vị trí cuộn hiện tại (tính bằng pixel) — sống trên UI Thread,
  // được cập nhật liên tục MỖI KHUNG HÌNH khi ngón tay đang kéo, không qua JS Thread.
  const scrollY = useSharedValue(0);

  // useAnimatedScrollHandler: phiên bản "Worklet" của onScroll thông thường.
  // Chạy thẳng trên UI Thread ngay khi FlashList bắn sự kiện cuộn — không có độ trễ
  // 1 khung hình như khi xử lý onScroll ở phía JS Thread.
  const scrollHandler = useAnimatedScrollHandler({
    onScroll: (event) => {
      scrollY.value = event.contentOffset.y;
    },
  });

  // useAnimatedStyle: trả về 1 object style được TÍNH LẠI mỗi khi scrollY đổi giá trị.
  const headerAnimatedStyle = useAnimatedStyle(() => {
    // interpolate(giá trị đang chạy, [khoảng đầu vào], [khoảng đầu ra], cách xử lý khi vượt khoảng)
    // Ở đây: scrollY chạy từ 0 -> SCROLL_RANGE thì height chạy NGƯỢC từ 180 -> 64
    const height = interpolate(
      scrollY.value,
      [0, SCROLL_RANGE],
      [HEADER_MAX_HEIGHT, HEADER_MIN_HEIGHT],
      Extrapolation.CLAMP, // CLAMP: cuộn quá xa cũng KHÔNG co nhỏ hơn 64 hay phình to hơn 180
    );
    return { height };
  });

  const titleAnimatedStyle = useAnimatedStyle(() => {
    const fontSize = interpolate(
      scrollY.value,
      [0, SCROLL_RANGE],
      [28, 18],
      Extrapolation.CLAMP,
    );
    // Chữ chỉ mờ tới 50% (không biến mất hẳn) và mờ nhanh hơn (dùng 80% quãng cuộn thay vì 100%)
    const opacity = interpolate(
      scrollY.value,
      [0, SCROLL_RANGE * 0.8],
      [1, 0.5],
      Extrapolation.CLAMP,
    );
    return { fontSize, opacity };
  });

  return (
    <View style={styles.container}>
      {/* Header co giãn — chiều cao và cỡ chữ đều "bám" theo scrollY qua interpolate ở trên */}
      <Animated.View style={[styles.header, headerAnimatedStyle]}>
        <Animated.Text style={[styles.headerTitle, titleAnimatedStyle]}>
          Khám phá
        </Animated.Text>
      </Animated.View>

      <AnimatedFlashList
        data={MOCK_PRODUCTS}
        keyExtractor={(item) => item.id}
        renderItem={({ item }) => <ProductCard product={item} />}
        numColumns={2}
        estimatedItemSize={260}
        onScroll={scrollHandler} // Gắn Worklet xử lý cuộn trực tiếp vào danh sách
        scrollEventThrottle={16} // ~60 lần/giây — chuẩn khai báo đi kèm khi bắt sự kiện onScroll
        contentContainerStyle={{ padding: SIZES.padding / 2 }}
      />
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: COLORS.background },
  header: {
    justifyContent: "flex-end",
    paddingHorizontal: SIZES.padding,
    paddingBottom: 16,
    backgroundColor: COLORS.surface,
    borderBottomWidth: 1,
    borderBottomColor: "#E5E7EB",
  },
  headerTitle: {
    fontWeight: "bold",
    color: COLORS.text,
  },
});
```

**Giải thích từng khối — vì sao mỗi dòng lại nằm ở đó:**

| Khối code                                                                       | Giải thích                                                                                                                                                                                                                                    |
| ------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `const scrollY = useSharedValue(0)`                                             | Biến "sống" trên UI Thread, giữ đúng 1 con số: vị trí cuộn hiện tại. Đọc/ghi qua `.value`, KHÔNG bao giờ gây re-render React (khác hẳn `useState`).                                                                                           |
| `Animated.createAnimatedComponent(FlashList)`                                   | `FlashList` là Component của thư viện ngoài (Shopify), không phải Component "thuần Reanimated" như `Animated.View`/`Animated.FlatList` có sẵn — phải tự nâng cấp nó lên bằng hàm này để nó hiểu được `onScroll={scrollHandler}` dạng Worklet. |
| `useAnimatedScrollHandler({ onScroll: ... })`                                   | Thay thế cho `onScroll` thường của React Native. Hàm bên trong là 1 Worklet — chạy thẳng trên UI Thread, gán giá trị cuộn mới vào `scrollY.value` mỗi khung hình, không cần "hỏi" JS Thread.                                                  |
| `useAnimatedStyle(() => { ... return {...} })`                                  | Nơi TÍNH TOÁN style cuối cùng. Reanimated tự động biết hàm này phụ thuộc vào `scrollY` (vì có đọc `scrollY.value` bên trong) và tự re-run nó mỗi khi `scrollY` đổi — hoàn toàn trên UI Thread.                                                |
| `interpolate(scrollY.value, [0, SCROLL_RANGE], [180, 64], Extrapolation.CLAMP)` | Phép "quy đổi tỉ lệ": scrollY chạy từ 0 đến 116 thì height chạy từ 180 xuống 64 theo đúng tỉ lệ tuyến tính. `Extrapolation.CLAMP` chặn giá trị output không bao giờ vượt ra ngoài `[64, 180]` dù `scrollY` có vượt 116 hay âm.                |
| `scrollEventThrottle={16}`                                                      | Yêu cầu hệ thống bắn sự kiện `onScroll` khoảng mỗi 16ms (~60 lần/giây) — khớp với tốc độ khung hình mượt mà Reanimated hướng tới.                                                                                                             |

> [!TIP]
> Muốn làm hiệu ứng "mờ dần opacity toàn bộ ảnh sản phẩm khi cuộn" (thay vì co Header) — chỉ cần đổi `outputRange` của `interpolate` từ `[180, 64]` (chiều cao) thành `[1, 0]` (độ mờ `opacity`) và áp style đó lên `<Animated.View style={fadeStyle}>` bọc ngoài `FlashList`. Cơ chế `scrollY` + `useAnimatedScrollHandler` + `interpolate` giữ nguyên y hệt — đây chính là bản chất "scroll-driven opacity" mà nhiều học viên hay hỏi.

### 3. Layout Animations — cách viết TẮT hơn cho Fade/Slide lúc Mount/Unmount

Ngoài việc tự tay viết `useSharedValue` + `useEffect` + `withTiming` như `ProductCard` đang làm (Sprint 4, Bước 3), Reanimated 3 còn cung cấp sẵn các **preset Layout Animation** thông qua 2 prop đặc biệt `entering`/`exiting` — chỉ cần gắn vào `Animated.View`, không cần viết `useEffect` thủ công:

```tsx
import Animated, { FadeIn, FadeOut, SlideInRight } from 'react-native-reanimated';

// Cách viết TẮT — tương đương với useSharedValue + useEffect + withTiming mà ProductCard đang làm thủ công
<Animated.View entering={FadeIn.duration(400)} exiting={FadeOut.duration(200)}>
  <ProductCard product={item} />
</Animated.View>

// Preset khác: trượt vào từ bên phải — hay dùng cho Toast/Banner thông báo
<Animated.View entering={SlideInRight.duration(300)}>
  <Text>Đã thêm vào giỏ hàng!</Text>
</Animated.View>
```

| Prop       | Kích hoạt khi nào                                        | Preset hay dùng                                 |
| ---------- | -------------------------------------------------------- | ----------------------------------------------- |
| `entering` | Component vừa được MOUNT (xuất hiện lần đầu trên cây UI) | `FadeIn`, `SlideInRight`, `SlideInUp`, `ZoomIn` |
| `exiting`  | Component sắp bị UNMOUNT (biến mất khỏi cây UI)          | `FadeOut`, `SlideOutLeft`, `ZoomOut`            |

> [!NOTE]
> **Vì sao `ProductCard` ở Sprint 4 vẫn giữ cách viết thủ công (`useSharedValue`/`useEffect`/`withTiming`) thay vì dùng `entering={FadeIn}` cho gọn?** Mục đích SƯ PHẠM: học viên cần thấy rõ 3 viên gạch nền (Shared Value, Worklet, UI Thread) hoạt động ra sao TRƯỚC KHI dùng các preset "đóng hộp sẵn". Trong dự án thực tế, hoàn toàn có thể rút gọn `ProductCard` bằng `entering={FadeIn.duration(400)}` — đây là bài tập tùy chọn, không bắt buộc trong Yêu cầu Nghiệm thu Sprint 4 (xem mục 7 bên dưới).

---

## 🖼️ PHẦN 4.5: ẢNH HIỆN ĐẠI (`expo-image`) & PULL-TO-REFRESH

### 1. Vì sao `<Image>` mặc định của React Native "yếu"?

Thẻ `<Image>` gốc của React Native có bộ nhớ đệm (Cache) khá đơn giản: mỗi lần danh sách bị re-mount (VD: rời màn hình rồi quay lại), ảnh có thể phải tải lại từ mạng thay vì lấy từ đĩa, gây giật lag và tốn băng thông 4G — đúng vấn đề ta vừa học ở FlashList/List Virtualization, ảnh là phần nặng nhất trong mỗi `ProductCard`.

Hai giải pháp phổ biến để thay thế:

- **`expo-image`** (khuyến nghị 2025–2026): Cache ảnh 2 tầng (RAM + Disk) cực mạnh, hỗ trợ blurhash placeholder (hiện khung mờ trong lúc chờ tải), transition mượt, và được xây trên **Expo Modules API** — dùng được cả trong dự án Bare RN CLI (không cần chuyển hẳn sang Expo) nếu đã có hạ tầng Expo Modules.
- **`react-native-fast-image`**: Lựa chọn lâu đời hơn, vẫn ổn định nhưng ít được cập nhật bằng `expo-image` gần đây.

> [!NOTE]
> **Về thứ tự học trong khóa:** Ở Chương 4 này, `ProductCard` **có thể dùng `<Image>` chuẩn của React Native** — hoàn toàn đủ dùng cho Sprint 4. Phải đến **Chương 8**, khi ShopAI cài đặt hạ tầng **Expo Modules API** trên nền Bare RN CLI (để dùng `expo-secure-store`), ta mới có sẵn "chân đế" để nâng cấp `<Image>` lên `expo-image` mà không tốn công cài riêng. Cài `expo-image` sớm ở Chương 4 (khi project vẫn thuần Bare RN CLI) sẽ đòi hỏi cấu hình Expo Modules ngay từ bây giờ — không cần thiết, để dành cho Chương 8 cho gọn.

```bash
# Chỉ chạy lệnh này ở Chương 8 trở đi (khi đã có hạ tầng Expo Modules) — KHÔNG chạy ở Chương 4
npx expo install expo-image
```

```tsx
// Cú pháp expo-image — gần giống <Image>, thêm placeholder + transition mượt
import { Image } from "expo-image";

<Image
  source={{ uri: product.image }}
  style={styles.image}
  placeholder={{ blurhash: "L6PZfSi_.AyE_3t7t7R**0o#DgR4" }} // Khung mờ hiện tạm trong lúc chờ tải ảnh thật
  transition={300} // Hiệu ứng mờ dần khi ảnh tải xong, tránh "nhảy khung" đột ngột
  cachePolicy="memory-disk" // Cache cả RAM lẫn Đĩa — ảnh cũ hiện lại tức thời khi quay lại màn hình
/>;
```

### 2. Pull-to-Refresh — Kéo để làm mới danh sách

Đây là thao tác kinh điển: người dùng kéo tay xuống ở đầu danh sách để báo "làm mới dữ liệu giùm tôi". Cả `FlatList` lẫn `FlashList` đều hỗ trợ sẵn 2 Props `refreshing` (Boolean đang làm mới hay không) và `onRefresh` (hàm gọi khi người dùng kéo):

```tsx
import React, { useState, useCallback } from "react";
import { FlashList } from "@shopify/flash-list";

const [refreshing, setRefreshing] = useState(false);

const handleRefresh = useCallback(() => {
  setRefreshing(true);
  // Giả lập gọi lại API mất 1.5 giây — Chương 6 sẽ thay bằng `refetch()` thật của React Query
  setTimeout(() => setRefreshing(false), 1500);
}, []);

<FlashList
  data={products}
  renderItem={({ item }) => <ProductCard product={item} />}
  refreshing={refreshing} // FlashList tự vẽ vòng xoay loading ở đầu danh sách khi true
  onRefresh={handleRefresh} // Được gọi tự động khi người dùng kéo tay xuống
/>;
```

> [!TIP]
> Pull-to-refresh chỉ là UI — nó không tự biết "làm mới" nghĩa là gì, bạn phải tự viết logic gọi lại API/dữ liệu bên trong `onRefresh`. Ở Sprint 4 (chưa có API thật), ta sẽ giả lập bằng `setTimeout`; đến Chương 6 khi có TanStack Query, `onRefresh` sẽ gọi thẳng hàm `refetch()` có sẵn của `useQuery` — không cần tự quản lý `refreshing` bằng `useState` nữa (React Query có sẵn `isRefetching`).

---

## 🔍 PHẦN 4.6: ADVANCED SEARCH & FILTER (TÌM KIẾM VÀ LỌC NÂNG CAO)

### 1. UX của chức năng Tìm Kiếm & Lọc hiện đại

Trong các sàn TMĐT (Shopee, Lazada), tìm kiếm không chỉ là gõ text rồi nhấn Enter. Nó bao gồm:

- **Gợi ý tìm kiếm (Auto-suggest / Debounce Search):** Hiển thị ngay kết quả hoặc từ khóa liên quan trong lúc người dùng đang gõ.
- **Lịch sử tìm kiếm:** Lưu lại các từ khóa đã tìm gần đây.
- **Bộ lọc động (Dynamic Filters):** Lọc theo danh mục, khoảng giá, đánh giá sao, nhãn hàng.

### 2. Kỹ thuật Debounce Search (Chống Spam API)

Nếu người dùng gõ "Iphone 15", mỗi ký tự "I", "p", "h"... sẽ gọi 1 API. Để tránh sập server, ta dùng kỹ thuật `Debounce`: Chỉ gọi API khi người dùng ngừng gõ sau một khoảng thời gian (ví dụ 500ms).

```tsx
import { useState, useEffect } from 'react';

// Custom Hook Debounce
export const useDebounce = <T>(value: T, delay: number): T => {
  const [debouncedValue, setDebouncedValue] = useState<T>(value);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedValue(value);
    }, delay);

    return () => clearTimeout(handler);
  }, [value, delay]);

  return debouncedValue;
};
```

### 3. Xây dựng Bottom Sheet Filter

Thay vì mở một trang mới để lọc, các app hiện đại thường mở một thanh trượt từ dưới lên (Bottom Sheet) chứa các tùy chọn. Ta có thể dùng `Modal` (Chương 2) kết hợp với `Animated` hoặc thư viện `@gorhom/bottom-sheet` để làm giao diện này.

---

## 🚀 THỰC CHIẾN SHOPAI (SPRINT 4: HOMESCREEN VỚI FLASHLIST, SAFE AREA CHUẨN & REANIMATED)

**User Story:** _"Là một Khách hàng, tôi muốn xem danh sách các sản phẩm mới nhất được trình bày dưới dạng Grid 2 cột trên trang chủ, cuộn nhanh không bị giật lag, giao diện không bị Tai thỏ che mất."_

### 📋 Khung thực hành chương (đọc trước khi gõ code)

> Đây là **bài thực hành của Chương 4** (không phải “lab mỗi ngày”). Làm hết Sprint này = đạt mục tiêu chương. Hoàn thành đủ 11 Sprint = sản phẩm ShopAI theo `SHOPAI_HOAN_THIEN.md`.

| Hạng mục                 | Nội dung                                                                                  |
| ------------------------ | ----------------------------------------------------------------------------------------- |
| **Thời lượng gợi ý**     | 4–6 tiết                                                                                  |
| **Độ khó chương**        | ★★★☆☆                                                                                     |
| **Đầu vào bắt buộc**     | Sprint 3 PASS — có ShopButton/Typography/theme.                                           |
| **Đầu ra sản phẩm**      | Home dạng lưới 2 cột FlashList; fade-in ProductCard; SafeArea chuẩn; pull-to-refresh.     |
| **Cách làm**             | Làm **tuần tự từng Bước**. Gặp mốc ✓ bên dưới mà FAIL → dừng, sửa, rồi mới sang bước sau. |
| **Nghiệm thu cuối khóa** | Đối chiếu `SHOPAI_HOAN_THIEN.md` — mỗi Sprint chỉ tích thêm ô, không phá tính năng cũ.    |

### ✓ Kiểm chứng theo mốc (trong lúc làm)

- **Sau Bước 1:** pod install + Reanimated plugin cuối babel — app build lại OK.
- **Sau Bước 3–4:** Lưới 2 cột cuộn mượt; thẻ có fade-in.
- **Sau Bước 4.5:** Kéo xuống đầu list → spinner rồi list “làm mới”.

> [!TIP]
> Xong Sprint 4, mở `SHOPAI_HOAN_THIEN.md` và tick các ô thuộc chương này. Mục tiêu cuối khóa: **mọi ô A/B/C/D (+ E đề cương) đều xanh** trong `SHOPAI_HOAN_THIEN.md` — đó mới là ShopAI hoàn thiện đẳng cấp.

### Yêu cầu Nghiệm thu:

1. **Safe Area:** Toàn bộ màn hình dùng `SafeAreaView` của thư viện `react-native-safe-area-context` (KHÔNG dùng bản `SafeAreaView` cũ đi kèm `react-native`). `App.tsx` phải được bọc ngoài bằng `SafeAreaProvider`.
2. **FlashList:** Danh sách sản phẩm dùng `FlashList` (`@shopify/flash-list`) thay cho `FlatList`, có khai báo `estimatedItemSize` (bắt buộc với v1; xem changelog nếu máy bạn cài được v2).
3. **Reanimated cơ bản:** `ProductCard` có hiệu ứng mờ dần hiện ra (Fade-in) chạy bằng `react-native-reanimated`, xử lý hoàn toàn trên UI Thread.
4. Toàn bộ import trong `ProductCard` dùng Path Alias (`@components`, `@constants`, `@data`) — không còn đường dẫn tương đối `../`.
5. Giao diện chia Grid 2 cột chuẩn Flexbox, tái sử dụng Component `ShopButton` đã tạo ở Sprint 3.
6. **Pull-to-refresh:** Kéo tay xuống đầu danh sách trên `FlashList` phải hiện vòng xoay loading rồi tự tắt sau khi "làm mới" xong (mô phỏng bằng `setTimeout` với `MOCK_PRODUCTS`, đúng lý thuyết Phần 4.5 mục 2).
7. **(Tùy chọn nâng cao)** Có Component minh họa Collapsing Header / scroll-driven opacity dùng `useAnimatedScrollHandler` + `interpolate`, đúng lý thuyết Phần 4.4 mục 2 — có thể để riêng ở `CollapsingHeaderDemo.tsx` hoặc áp thẳng lên Header của `HomeScreen`.
8. Có giao diện **Thanh Tìm Kiếm (Search Bar)** ở Header và **Bộ Lọc Nâng Cao (Filter Bottom Sheet/Modal)** để lọc sản phẩm theo mức giá hoặc danh mục.

### Hướng dẫn thực thi Step-by-Step:

#### Bước 1: Cài đặt thư viện FlashList và Reanimated

Mở Terminal, cài 2 thư viện chủ lực của Sprint này (kèm luôn `react-native-safe-area-context` nếu máy bạn chưa có):

```bash
npm install @shopify/flash-list react-native-reanimated react-native-safe-area-context
```

Vì các thư viện này có chứa mã Native (C++/Swift/Kotlin), trên iOS bạn cần link lại Pod:

```bash
cd ios
pod install
cd ..
```

> [!IMPORTANT]
> **Vị trí Plugin Babel của Reanimated là SỐNG CÒN.** Reanimated cần "chèn" mã của nó vào giai đoạn biên dịch cuối cùng để biến các hàm Worklet thành mã chạy được trên UI Thread. Do đó, plugin `'react-native-reanimated/plugin'` **BẮT BUỘC phải là phần tử CUỐI CÙNG** trong mảng `plugins` của `babel.config.js` — đứng sau cả `module-resolver` (Path Alias) đã cấu hình ở Chương 2. Nếu đặt sai vị trí, animation sẽ chạy sai hoặc app báo lỗi rất khó hiểu.

Mở `babel.config.js` ở gốc dự án, cập nhật lại như sau:

```javascript
module.exports = {
  presets: ["module:@react-native/babel-preset"],
  plugins: [
    [
      "module-resolver",
      {
        root: ["./src"],
        extensions: [".ios.js", ".android.js", ".js", ".ts", ".tsx", ".json"],
        alias: {
          "@assets": "./src/assets",
          "@components": "./src/components",
          "@screens": "./src/screens",
          "@navigation": "./src/navigation",
          "@store": "./src/store",
          "@services": "./src/services",
          "@hooks": "./src/hooks",
          "@data": "./src/data",
          "@utils": "./src/utils",
          "@constants": "./src/constants",
          "@types": "./src/types",
        },
      },
    ],
    "react-native-reanimated/plugin", // ⚠️ LUÔN LUÔN đứng cuối cùng trong danh sách plugins
  ],
};
```

Sau khi sửa file cấu hình Babel, luôn nhớ xóa cache Metro rồi chạy lại:

```bash
npm start -- --reset-cache
```

#### Bước 2: Chuẩn bị dữ liệu mẫu (Mock Data)

Tạo file `src/data/mockProducts.ts`:

```ts
// src/data/mockProducts.ts
export interface Product {
  id: string;
  name: string;
  price: number;
  image: string;
}

// Tạo mảng 50 sản phẩm mẫu
export const MOCK_PRODUCTS: Product[] = Array.from({ length: 50 }).map(
  (_, index) => ({
    id: `prod_${index}`,
    name: `Tai nghe Bluetooth Pro ${index}`,
    price: 1500000 + index * 10000,
    image: `https://picsum.photos/id/${10 + index}/400/400`,
  }),
);
```

#### Bước 3: Viết Component Thẻ Sản Phẩm (Product Card) với Reanimated Fade-in

Tạo file `src/components/ProductCard.tsx`. Chú ý toàn bộ import đều đi qua Path Alias, không còn `../` nào cả:

```tsx
import React, { memo, useEffect } from "react";
import { View, Text, Image, StyleSheet, Dimensions } from "react-native";
import Animated, {
  useSharedValue,
  useAnimatedStyle,
  withTiming,
} from "react-native-reanimated";
import { COLORS, SIZES } from "@constants/theme";
import ShopButton from "@components/ShopButton";
import { Product } from "@data/mockProducts";

// Lấy chiều rộng màn hình để tính kích thước cột (Grid 2 cột, có khe hở đều 2 bên)
const { width } = Dimensions.get("window");
const GAP = SIZES.padding;
const CARD_WIDTH = (width - GAP * 3) / 2;

interface Props {
  product: Product;
}

const ProductCard = ({ product }: Props) => {
  // Reanimated: Shared Value sống trên UI Thread, không phải state React thông thường
  const opacity = useSharedValue(0);

  useEffect(() => {
    // withTiming đẩy toàn bộ phép tính animation sang chạy Native (Worklet),
    // JS Thread không cần bận tâm gì tới quá trình mờ dần hiện ra này.
    opacity.value = withTiming(1, { duration: 400 });
  }, [opacity]);

  const fadeInStyle = useAnimatedStyle(() => ({
    opacity: opacity.value,
  }));

  return (
    <Animated.View style={[styles.card, fadeInStyle]}>
      <Image
        source={{ uri: product.image }}
        style={styles.image}
        resizeMode="cover"
      />
      <View style={styles.infoContainer}>
        <Text style={styles.name} numberOfLines={2}>
          {product.name}
        </Text>
        <Text style={styles.price}>
          {new Intl.NumberFormat("vi-VN", {
            style: "currency",
            currency: "VND",
          }).format(product.price)}
        </Text>

        {/* Tái sử dụng Nút bấm từ Sprint 3 */}
        <ShopButton
          title="Mua ngay"
          onPress={() => {}}
          style={styles.button}
          textStyle={{ fontSize: 12 }}
        />
      </View>
    </Animated.View>
  );
};

const styles = StyleSheet.create({
  card: {
    width: CARD_WIDTH,
    marginHorizontal: GAP / 2, // Khe hở đều giữa 2 cột và ở 2 mép màn hình
    marginBottom: GAP,
    backgroundColor: COLORS.surface,
    borderRadius: SIZES.radius,
    overflow: "hidden",
    // Đổ bóng
    shadowColor: "#000",
    shadowOffset: { width: 0, height: 2 },
    shadowOpacity: 0.1,
    shadowRadius: 4,
    elevation: 3,
  },
  image: {
    width: "100%",
    height: CARD_WIDTH, // Ảnh hình vuông
  },
  infoContainer: {
    padding: 10,
  },
  name: {
    fontSize: SIZES.body2,
    color: COLORS.text,
    fontWeight: "500",
    height: 40, // Cố định chiều cao 2 dòng
  },
  price: {
    fontSize: SIZES.body1,
    color: COLORS.primary,
    fontWeight: "bold",
    marginVertical: 8,
  },
  button: {
    height: 36,
  },
});

export default memo(ProductCard);
```

> **Vì sao Fade-in lại thuộc về Reanimated?** Nhìn kỹ 3 dòng `useSharedValue`, `useAnimatedStyle`, `withTiming`: không có `setState`, không có `re-render` nào của React bị kích hoạt. Toàn bộ chuỗi tăng dần `opacity` từ 0 lên 1 chạy thẳng trên UI Thread native, tách biệt hoàn toàn khỏi JS Thread — đúng như lý thuyết Phần 4.4 đã giải thích.

#### Bước 4: Ráp giao diện vào HomeScreen với FlashList + Safe Area chuẩn

Mở lại `src/screens/HomeScreen.tsx` và nâng cấp nó lên:

```tsx
import React from "react";
import { View, Text, StyleSheet } from "react-native";
// ĐÚNG: SafeAreaView phải lấy từ 'react-native-safe-area-context', KHÔNG lấy từ 'react-native'
import { SafeAreaView } from "react-native-safe-area-context";
import { FlashList } from "@shopify/flash-list";
import ProductCard from "@components/ProductCard";
import { MOCK_PRODUCTS } from "@data/mockProducts";
import { COLORS, SIZES } from "@constants/theme";

const HomeScreen = () => {
  return (
    // SafeAreaView của safe-area-context tự tính đúng khoảng Tai thỏ/Dynamic Island
    <SafeAreaView style={styles.safeArea} edges={["top", "left", "right"]}>
      <View style={styles.container}>
        {/* Header AppBar */}
        <View style={styles.header}>
          <Text style={styles.headerTitle}>Khám phá</Text>
        </View>

        {/* FlashList: thuật toán Recycling viết bằng C++ của Shopify, nhanh hơn FlatList ~10 lần */}
        <FlashList
          data={MOCK_PRODUCTS}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => <ProductCard product={item} />}
          // --- CẤU HÌNH GRID 2 CỘT ---
          numColumns={2} // Chia 2 cột (khe hở đã xử lý bằng margin trong ProductCard)
          // --- PROP QUAN TRỌNG CỦA FLASHLIST v1 ---
          // Nếu dùng FlashList v1: bắt buộc estimatedItemSize.
          // Nếu npm cài được v2: prop này có thể không cần, xem changelog @shopify/flash-list.
          // Khóa học vẫn ghi estimatedItemSize để tương thích v1 phổ biến trên nhiều máy sinh viên.
          estimatedItemSize={260} // Chiều cao ước lượng 1 thẻ, giúp FlashList tính trước bộ khung Recycle
          contentContainerStyle={{ padding: SIZES.padding / 2 }}
          showsVerticalScrollIndicator={false}
        />
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: {
    flex: 1,
    backgroundColor: COLORS.background, // Màu nền vùng tai thỏ
  },
  container: {
    flex: 1,
    backgroundColor: COLORS.background,
  },
  header: {
    paddingHorizontal: SIZES.padding,
    paddingVertical: 15,
    backgroundColor: COLORS.surface,
  },
  headerTitle: {
    fontSize: SIZES.h1,
    fontWeight: "bold",
    color: COLORS.text,
  },
});

export default HomeScreen;
```

> [!NOTE]
> `estimatedItemSize` chỉ là con số **ước lượng khởi điểm** để FlashList tính toán bộ khung dựng hình đầu tiên — không cần chính xác tuyệt đối, sai khoảng vài chục pixel vẫn chạy tốt. FlashList sẽ tự đo lại kích thước thật của từng dòng khi nó render xong và tự điều chỉnh.

#### Bước 4.5: Thêm Pull-to-Refresh (áp dụng lý thuyết Phần 4.5 mục 2)

Chưa có API thật (Chương 6 mới có), nên ta mô phỏng "làm mới dữ liệu" bằng cách xáo lại `MOCK_PRODUCTS` sau một khoảng trễ giả lập. Mở lại `src/screens/HomeScreen.tsx`, thêm state `refreshing` và hàm `handleRefresh`:

```tsx
import React, { useState, useCallback } from "react";
// ...các import cũ giữ nguyên (SafeAreaView, FlashList, ProductCard, MOCK_PRODUCTS, COLORS, SIZES)

const HomeScreen = () => {
  // Danh sách hiển thị giờ nằm trong State thay vì đọc thẳng MOCK_PRODUCTS,
  // để hàm "làm mới" có chỗ ghi dữ liệu mới vào sau khi giả lập gọi lại API
  const [products, setProducts] = useState(MOCK_PRODUCTS);
  const [refreshing, setRefreshing] = useState(false);

  const handleRefresh = useCallback(() => {
    setRefreshing(true);
    // Giả lập gọi lại API mất 1.5 giây — Chương 6 sẽ thay bằng refetch() thật của React Query
    setTimeout(() => {
      // Xáo ngẫu nhiên mảng để người dùng THẤY RÕ danh sách vừa "làm mới", không chỉ là loading suông
      setProducts([...MOCK_PRODUCTS].sort(() => Math.random() - 0.5));
      setRefreshing(false);
    }, 1500);
  }, []);

  return (
    <SafeAreaView style={styles.safeArea} edges={["top", "left", "right"]}>
      <View style={styles.container}>
        <View style={styles.header}>
          <Text style={styles.headerTitle}>Khám phá</Text>
        </View>

        <FlashList
          data={products}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => <ProductCard product={item} />}
          numColumns={2}
          estimatedItemSize={260}
          refreshing={refreshing} // FlashList tự vẽ vòng xoay loading khi true
          onRefresh={handleRefresh} // Gọi tự động khi người dùng kéo tay xuống đầu danh sách
          contentContainerStyle={{ padding: SIZES.padding / 2 }}
          showsVerticalScrollIndicator={false}
        />
      </View>
    </SafeAreaView>
  );
};
```

> [!NOTE]
> `refreshing`/`onRefresh` hoạt động giống hệt trên cả `FlatList` lẫn `FlashList` — cùng 1 API, không có gì phải học lại nếu sau này đổi thư viện danh sách.

#### Bước 4.6 (Tùy chọn nâng cao): Áp dụng Collapsing Header lên HomeScreen thật

Đây là bài tập **không bắt buộc** để luyện tay với `interpolate` (Phần 4.4 mục 2) ngay trên màn hình thật thay vì chỉ xem file demo riêng lẻ. Có 2 cách, chọn 1:

**Cách A (an toàn, khuyến nghị cho lớp học):** Giữ nguyên `HomeScreen.tsx` như Bước 4, chỉ tạo thêm `src/screens/CollapsingHeaderDemo.tsx` (đúng như file hoàn chỉnh ở Phần 4.4 mục 2), rồi tạm thời gắn nó vào `App.tsx` thay cho `HomeScreen` để xem hiệu ứng chạy thật trên máy — xem xong đổi lại `HomeScreen` như cũ. Không đụng gì đến `ProductCard`/`HomeScreen` chính thức của Sprint 4.

**Cách B (nâng cao, thay thế trực tiếp):** Copy đúng 3 khối `useSharedValue` + `useAnimatedScrollHandler` + `useAnimatedStyle` (interpolate height/fontSize) từ `CollapsingHeaderDemo.tsx` vào thẳng `HomeScreen.tsx`, thay khối `<View style={styles.header}>` tĩnh bằng `<Animated.View style={[styles.header, headerAnimatedStyle]}>`, và đổi `<FlashList>` thường thành `AnimatedFlashList` (nhớ khai báo `onScroll={scrollHandler}` + `scrollEventThrottle={16}`).

> [!WARNING]
> Dù chọn Cách A hay B, **`ProductCard` với hiệu ứng Fade-in thủ công (`useSharedValue`/`withTiming`) ở Bước 3 phải được GIỮ NGUYÊN** — đây là 2 hiệu ứng độc lập nhau (một cái chạy 1 lần lúc mount, một cái chạy liên tục theo cuộn tay), không cái nào thay thế cái nào.

#### Bước 5: Bọc App.tsx bằng SafeAreaProvider

Đây là điều kiện bắt buộc để mọi `SafeAreaView` con phía trong tính đúng số Pixel an toàn. Mở `App.tsx`:

```tsx
import React from "react";
import { SafeAreaProvider } from "react-native-safe-area-context";
import { ThemeProvider } from "@contexts/ThemeContext";
import HomeScreen from "@screens/HomeScreen";

function App(): React.JSX.Element {
  return (
    // Toàn bộ cây App phải nằm trong SafeAreaProvider — chỉ cần khai báo 1 lần duy nhất ở gốc
    <SafeAreaProvider>
      {/* ThemeProvider giữ nguyên từ Sprint 3 (Chương 3) — nếu xoá mất, nút Dark Mode ở
          HomeScreen sẽ báo lỗi "useTheme phải được gọi bên trong ThemeProvider" */}
      <ThemeProvider>
        <HomeScreen />
      </ThemeProvider>
    </SafeAreaProvider>
  );
}

export default App;
```

#### Bước 6: Lưu code (Git)

App của chúng ta đã có một giao diện Grid bán hàng lộng lẫy, mượt mà 60FPS, đúng chuẩn Safe Area và có animation Reanimated!

```bash
git add .
git commit -m "Sprint 4: FlashList Grid + Safe Area Context + Reanimated fade-in + Pull-to-refresh"
```

> [!NOTE]
> **Tính liên tục:**
>
> - `MOCK_PRODUCTS` (`src/data/mockProducts.ts`) chỉ là dữ liệu **tạm thời** để dựng UI — Chương 6 sẽ thay bằng dữ liệu thật lấy qua React Query, giữ nguyên giao diện `ProductCard`/`FlashList` đã xây ở đây.
> - `ProductCard` đang **tái sử dụng** `ShopButton` (Chương 3) cho nút "Mua ngay" — đúng tinh thần Design System, không viết lại nút bấm riêng.
> - `SafeAreaProvider` bọc ở `App.tsx` từ Chương 4 sẽ **giữ nguyên vĩnh viễn** ở gốc cây App trong toàn bộ các chương sau (Chương 5 thêm Navigation cũng lồng bên trong `SafeAreaProvider` này, không thay thế nó). `ThemeProvider` (Chương 3) tiếp tục lồng bên trong `SafeAreaProvider` như đã thấy ở Bước 5.
> - Pattern `refreshing`/`onRefresh` giả lập bằng `setTimeout` ở Bước 4.5 sẽ được **thay thế nguyên khối** bằng `isRefetching`/`refetch` thật của TanStack Query ở Chương 6 — giao diện FlashList không đổi, chỉ đổi nguồn dữ liệu.
> - `<Image>` chuẩn dùng trong `ProductCard` vẫn ổn cho đến khi nâng cấp lên `expo-image` ở Chương 8 (xem Phần 4.5 mục 1) — không cần đổi gì thêm ở đây.

---

### ✅ Checklist nghiệm thu Sprint 4 (tick trước khi sang Chương 5)

- [ ] `SafeAreaProvider` + `SafeAreaView` từ `react-native-safe-area-context`
- [ ] Home dùng **FlashList** lưới 2 cột + `estimatedItemSize` (nếu v1)
- [ ] `ProductCard` có fade-in Reanimated; dùng Path Alias
- [ ] Pull-to-refresh hoạt động trên Home
- [ ] Tái sử dụng `ShopButton` từ Chương 3
- [ ] `git commit` Sprint 4

## 🎯 CHUẨN BỊ CHO CHƯƠNG 5

App đã có màn hình Home mượt mà, nhưng làm sao bấm vào 1 sản phẩm để nhảy sang màn hình "Chi tiết sản phẩm"? Làm sao có thanh Tab dưới đáy để chuyển qua "Giỏ hàng"? Làm sao bấm nút "Thoát" để văng thẳng ra màn hình Đăng nhập, không thể bấm Back lách luật?
Chúng ta cần một "Người lái xe" dẫn đường. Chương 5 sẽ hướng dẫn bạn cài đặt **React Navigation V7 (Mới nhất)** với **Bottom Tab Navigator**, quản lý luồng Auth (Bảo mật) bằng State Machine, truyền `productId` giữa các màn hình qua Route Params, và cấu hình Deep Linking.
