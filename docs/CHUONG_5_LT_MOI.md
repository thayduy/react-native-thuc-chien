---
sidebar_position: 5
title: Chương 5
---

# GIÁO TRÌNH LÝ THUYẾT & THỰC CHIẾN

## CHƯƠNG 5: ĐIỀU HƯỚNG BẢO MẬT VÀ LUỒNG ỨNG DỤNG (REACT NAVIGATION V7)

**Thời lượng:** 6 tiết Lý thuyết + 4 tiết Thực hành

---

> [!IMPORTANT]
> **Thực hành chương = Sprint ShopAI cuối file.** Hoàn thành Sprint này để đạt mục tiêu chương. Hoàn thành đủ 11 chương theo `SHOPAI_HOAN_THIEN.md` = sản phẩm ShopAI **hoàn thiện đẳng cấp**.

## 📚 MỤC TIÊU HỌC TẬP

Sau khi hoàn thành chương này, học viên sẽ:

- ✅ Hiểu rõ cơ chế cấp phát bộ nhớ RAM của hệ điều hành khi điều hướng (Stack vs Tab vs Drawer).
- ✅ Thiết kế kiến trúc chuyển trang an toàn, chống rò rỉ dữ liệu bằng **Auth Flow State Machine**.
- ✅ Nắm vững nghệ thuật truyền dữ liệu qua lại giữa các màn hình mà không làm chậm app.
- ✅ Biết cách cấu hình **Deep Linking** để người dùng bấm vào Link Web trên Safari/Chrome và mở thẳng vào app.
- ✅ Làm chủ **Drawer Navigator** và tư duy **Custom Navigation** — lồng nhiều Navigator (Stack/Tab/Drawer) đúng nhu cầu UX của từng ứng dụng.
- ✅ Phân biệt được **Expo Router (File-based Routing)** với **React Navigation (Code-based Routing)** — biết vì sao ShopAI (dự án Bare RN CLI) chọn React Navigation, và khi nào nên chọn Expo Router cho dự án khác.
- ✅ **Thực chiến:** Cài đặt React Navigation V7, dựng luồng Đăng nhập + **Đăng ký** (AuthStack) và luồng Chính (Main) cho ShopAI.

---

## 🧭 PHẦN 5.1: KIẾN TRÚC ĐIỀU HƯỚNG (NAVIGATION ARCHITECTURE)

Trong phát triển Web, bạn bấm vào một đường link, trình duyệt sẽ xóa trang cũ đi và tải trang mới về.
Tuy nhiên, trong ứng dụng Mobile, việc điều hướng không giống như vậy. Màn hình cũ không biến mất, nó chỉ bị **đè lên**.

Thư viện tiêu chuẩn của toàn ngành công nghiệp hiện nay là **React Navigation** (Phiên bản mới nhất là V7). Nó cung cấp 3 mô hình kiến trúc cốt lõi:

### 0. 🖐️ CẦM TAY CHỈ VIỆC — Nhìn Navigation bằng hình vẽ trước khi đọc lý thuyết

Rất nhiều học viên mới đọc "Stack đè lên, Tab đóng băng ngầm" thấy trừu tượng. Trước khi đọc kỹ Phần 5.1, hãy nhìn 2 hình vẽ dưới đây để hình dung đúng những gì xảy ra **trên màn hình điện thoại thật**.

#### a) Wireframe: Stack Push — Home bị "đè" bởi Detail

```
   TRƯỚC KHI BẤM (Chỉ có Home)     SAU KHI BẤM "Xem chi tiết" (Push)

   ┌─────────────────────┐         ┌─────────────────────┐
   │ 📱  Trang chủ        │         │ 📱  Chi tiết SP  ⬅   │  ← Màn hình MỚI, NẰM TRÊN CÙNG
   │ ───────────────────  │         │ ───────────────────  │
   │  [Ảnh SP1] [Ảnh SP2] │   Push  │                      │
   │  [Ảnh SP3] [Ảnh SP4] │  ────▶  │      🖼️  Ảnh lớn      │
   │                      │         │                      │
   │                      │         │   iPhone 15 Pro Max  │
   │                      │         │   Giá: 25.000.000đ   │
   │                      │         │   [ Thêm vào giỏ ]   │
   └─────────────────────┘         └─────────────────────┘
                                     Trang chủ KHÔNG mất đi — nó vẫn
                                     nằm "phía sau", còn nguyên trong RAM
```

> [!TIP]
> Hãy tưởng tượng 2 chiếc điện thoại này là **2 tấm ảnh xếp chồng lên nhau** trong 1 chồng bài (deck) — Home nằm dưới, Detail nằm trên. Bấm nút Back (⬅) chỉ là **rút** tấm trên cùng ra, Home lộ ra nguyên vẹn (không load lại từ đầu).

#### b) Wireframe: Bottom Tabs — 3 Tab luôn nằm dưới đáy màn hình

```
   ┌─────────────────────┐   ┌─────────────────────┐   ┌─────────────────────┐
   │ 📱  Trang chủ        │   │ 📱  Giỏ hàng         │   │ 📱  Hồ sơ            │
   │ ───────────────────  │   │ ───────────────────  │   │ ───────────────────  │
   │  [Ảnh SP1] [Ảnh SP2] │   │  Áo thun x2          │   │   👤  Nguyễn Văn A   │
   │  [Ảnh SP3] [Ảnh SP4] │   │  Quần jean x1        │   │   Đơn hàng của tôi   │
   │                      │   │  ─────────────       │   │   Cài đặt            │
   │                      │   │  Tổng: 850.000đ      │   │   Đăng xuất          │
   │┌───┐   ┌───┐   ┌───┐ │   │┌───┐   ┌───┐   ┌───┐ │   │┌───┐   ┌───┐   ┌───┐ │
   ││🏠 │   │🛒 │   │👤 │ │   ││🏠 │   │🛒 │   │👤 │ │   ││🏠 │   │🛒 │   │👤 │ │
   │└───┘   └───┘   └───┘ │   │└───┘   └───┘   └───┘ │   │└───┘   └───┘   └───┘ │
   │ ▲ đang chọn          │   │        ▲ đang chọn   │   │               ▲ đang │
   └─────────────────────┘   └─────────────────────┘   └─────────────────────┘
       Bấm Tab "🛒"  ──────────────▶   Bấm Tab "👤"  ──────────────▶
```

> [!TIP]
> Khác với Stack, bấm đổi Tab **KHÔNG** đẩy màn hình mới đè lên — nó chỉ **chuyển đổi hiển thị** giữa các cây Component đã được "đóng băng ngầm" sẵn trong bộ nhớ (xem lại giải thích ở mục 2 ngay dưới đây).

#### c) File ví dụ tối giản: `RootNavDemo.tsx` (1 Stack lồng trong 1 Tab)

Đây là bộ khung NHỎ NHẤT có thể chạy được, dựng đúng mô hình "Stack lồng trong Tab" mà ShopAI sẽ dùng ở Sprint 5 phía dưới (Bước 4-5):

```tsx
// RootNavDemo.tsx — Ví dụ tối giản: HomeStack (Home -> Detail) nằm bên trong Bottom Tab
import React from "react";
import { View, Text, Button } from "react-native";
import { NavigationContainer } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";

// Khai báo kiểu Params cho Stack Home — TypeScript sẽ báo lỗi nếu quên gửi "id"
type HomeStackParamList = {
  Home: undefined;
  Detail: { id: string };
};

const Stack = createNativeStackNavigator<HomeStackParamList>();
const Tab = createBottomTabNavigator();

function HomeScreen({ navigation }: any) {
  return (
    <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
      <Text>Trang chủ</Text>
      <Button
        title="Xem chi tiết SP 001"
        onPress={() => navigation.navigate("Detail", { id: "001" })}
      />
    </View>
  );
}

function DetailScreen({ route }: any) {
  // Nếu quên truyền params ở navigate() phía trên, dòng dưới sẽ crash vì route.params là undefined
  const { id } = route.params;
  return (
    <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
      <Text>Chi tiết sản phẩm: {id}</Text>
    </View>
  );
}

// Stack riêng cho nhánh "Trang chủ" — sẽ được nhồi vào làm 1 Tab bên dưới
function HomeStack() {
  return (
    <Stack.Navigator>
      <Stack.Screen name="Home" component={HomeScreen} />
      <Stack.Screen name="Detail" component={DetailScreen} />
    </Stack.Navigator>
  );
}

function CartScreen() {
  return (
    <View style={{ flex: 1, justifyContent: "center", alignItems: "center" }}>
      <Text>Giỏ hàng</Text>
    </View>
  );
}

export default function RootNavDemo() {
  return (
    // NavigationContainer PHẢI là component NGOÀI CÙNG, chỉ khai báo DUY NHẤT 1 lần ở gốc App
    <NavigationContainer>
      <Tab.Navigator>
        {/* Tab này KHÔNG chứa trực tiếp HomeScreen, mà chứa cả 1 HomeStack bên trong */}
        <Tab.Screen
          name="HomeTab"
          component={HomeStack}
          options={{ title: "Trang chủ" }}
        />
        <Tab.Screen
          name="Cart"
          component={CartScreen}
          options={{ title: "Giỏ hàng" }}
        />
      </Tab.Navigator>
    </NavigationContainer>
  );
}
```

**Giải thích từng dòng import — dành cho người mới lần đầu thấy các dòng này:**

| Dòng import                                                                   | Lấy từ đâu                | Dùng để làm gì                                                                                             |
| ----------------------------------------------------------------------------- | ------------------------- | ---------------------------------------------------------------------------------------------------------- |
| `import { View, Text, Button } from 'react-native'`                           | Thư viện gốc React Native | 3 component UI cơ bản nhất: khung chứa, chữ, nút bấm                                                       |
| `import { NavigationContainer } from '@react-navigation/native'`              | Core của React Navigation | "Vỏ bọc" bắt buộc phải có ở NGOÀI CÙNG, quản lý toàn bộ trạng thái điều hướng (lịch sử back, deep link...) |
| `import { createNativeStackNavigator } from '@react-navigation/native-stack'` | Package Stack             | Hàm khởi tạo ra 1 cặp `Stack.Navigator` + `Stack.Screen` để làm hiệu ứng Push/Pop                          |
| `import { createBottomTabNavigator } from '@react-navigation/bottom-tabs'`    | Package Bottom Tabs       | Hàm khởi tạo ra 1 cặp `Tab.Navigator` + `Tab.Screen` để làm thanh Tab dưới đáy                             |

#### d) Diagram: Màn hình nào Mount khi nào?

```
BẤM VÀO SẢN PHẨM Ở HOME (Stack Push):

  Home (đã Mount từ trước)
    │  navigation.navigate('Detail', { id: '001' })
    ▼
  Detail  ──▶  MOUNT MỚI (chạy lại toàn bộ component từ đầu, gọi lại useEffect...)
  Home    ──▶  giữ nguyên, KHÔNG unmount, chỉ bị che khuất phía sau


CHUYỂN TỪ TAB "Trang chủ" SANG TAB "Giỏ hàng":

  HomeTab (đã Mount từ trước)
    │  bấm Tab "🛒 Giỏ hàng"
    ▼
  Cart Tab ──▶  Nếu đây là LẦN ĐẦU bấm vào Tab này -> MOUNT MỚI (1 lần duy nhất)
              Nếu đã từng bấm vào rồi -> KHÔNG Mount lại, chỉ hiện ra ngay lập tức
              (Component vẫn "sống" trong RAM, useEffect KHÔNG chạy lại)
  HomeTab  ──▶  KHÔNG unmount, chỉ ẩn đi — mọi State bên trong (scroll position,
              dữ liệu đã load...) vẫn còn nguyên khi quay lại
```

> [!IMPORTANT]
> Đây là khác biệt cốt lõi cần nhớ: **Stack Push luôn tạo màn hình MỚI mỗi lần bấm** (kể cả bấm lại đúng 1 sản phẩm 2 lần = 2 lần Mount, xem cảnh báo Bẫy bộ nhớ bên dưới), còn **chuyển Tab chỉ Mount đúng 1 LẦN DUY NHẤT** cho mỗi Tab trong suốt vòng đời App (trừ khi bạn cấu hình `unmountOnBlur`).

#### e) Bảng lỗi thường gặp khi mới học Navigation

| Lỗi thường gặp                                                                                                                                 | Triệu chứng khi chạy App                                                               | Nguyên nhân                                                                                                                            | Cách sửa                                                                                                                                                                                                                         |
| ---------------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Lồng Navigator sai chỗ** (VD: nhét `Stack.Navigator` làm `children` trực tiếp của `Tab.Screen` thay vì bọc trong 1 function Component riêng) | App crash hoặc báo lỗi `Got an invalid value for 'component' prop`                     | `Tab.Screen`/`Stack.Screen` cần nhận 1 Component (hàm trả JSX), không nhận thẳng JSX của Navigator khác                                | Luôn tạo 1 hàm Component riêng (VD: `HomeStack`) rồi truyền `component={HomeStack}`, giống ví dụ `RootNavDemo.tsx` ở trên                                                                                                        |
| **Quên bọc `<NavigationContainer>`**                                                                                                           | Lỗi đỏ: `Couldn't find a navigation object` hoặc màn hình trắng tinh khi App khởi động | Mọi `Navigator` (Stack/Tab/Drawer) đều cần sống bên trong đúng 1 `NavigationContainer` gốc để chia sẻ chung trạng thái điều hướng      | Kiểm tra `App.tsx` — `NavigationContainer` phải là thẻ NGOÀI CÙNG bọc toàn bộ cây Navigator, và chỉ khai báo **1 lần duy nhất** trong cả App                                                                                     |
| **`params` bị `undefined`** khi màn hình Detail đọc `route.params.id`                                                                          | Crash: `Cannot read property 'id' of undefined`                                        | Màn hình được mở mà KHÔNG qua `navigate('Detail', {...})` có tham số (VD: mở trực tiếp bằng Deep Link, hoặc quên truyền tham số thứ 2) | Khai báo kiểu `ProductDetail: { productId: string }` (bắt buộc, không phải `undefined`) trong `ParamList` để TypeScript tự báo lỗi lúc code; đồng thời luôn kiểm tra `route.params?.id` phòng trường hợp Deep Link thiếu tham số |
| **Bấm liên tục nhiều lần bằng `navigation.push()`**                                                                                            | App bị lag dần, cuối cùng crash vì hết RAM                                             | Mỗi lần `push()` luôn tạo màn hình MỚI dù đang đứng ở đúng màn hình đó (xem "Bẫy bộ nhớ" ở mục 1 bên dưới)                             | Dùng `navigation.navigate()` thay vì `push()` trong đa số trường hợp — nó tự kiểm tra màn hình đã tồn tại trong Stack chưa                                                                                                       |

---

### 1. Stack Navigation (Ngăn xếp)

**Cơ chế hoạt động:** Giống như việc xếp những chiếc đĩa lên nhau.

- Bấm vào "Chi tiết sản phẩm" -> Một màn hình mới được khởi tạo và **đẩy (Push)** đè lên màn hình "Trang chủ". Lúc này, Trang chủ không bị hủy (Unmount), nó chỉ đang ẩn mình bên dưới và tiêu thụ RAM.
- Bấm nút Back -> Màn hình Chi tiết bị **rút ra (Pop)** và tiêu hủy hoàn toàn khỏi bộ nhớ. Trang chủ lộ ra trở lại.

> [!WARNING]
> **Bẫy bộ nhớ:** Nếu bạn cho phép người dùng click liên tục: _Sản phẩm A -> Sản phẩm B -> Sản phẩm C -> Sản phẩm A_. Nó sẽ tạo ra 4 cái đĩa đè lên nhau. Nếu lặp lại 100 lần, app sẽ sập vì hết RAM (Stack Overflow). Luôn cẩn thận khi dùng lệnh `navigation.push()`. Hãy dùng `navigation.navigate()` (Nó sẽ kiểm tra xem màn hình A đã có trong Stack chưa, nếu có thì sẽ đẩy nó lên đầu chứ không tạo thêm bản sao mới).

### 2. Tab Navigation (Thanh điều hướng đáy)

Dùng cho các tính năng chính của App (Trang chủ, Giỏ hàng, Hồ sơ) nằm ở dưới đáy màn hình.
**Đặc điểm:** Lần đầu bấm vào Tab "Giỏ hàng", nó sẽ Mount. Khi bấm về "Trang chủ", Tab "Giỏ hàng" không bị hủy (Pop) đi như Stack. Nó được **đóng băng ngầm** trong bộ nhớ. Điều này giúp khi bạn bấm lại vào "Giỏ hàng", tốc độ mở là ngay lập tức (0 mili-giây).

### 3. Drawer Navigation (Menu trượt ngang)

Menu trượt từ cạnh trái màn hình ra. Rất phổ biến trên Android (chuẩn Material Design), nhưng ít được ưa chuộng trên iOS. Cơ chế lưu trữ RAM tương tự Tab Navigation.

---

## 🔒 PHẦN 5.2: BẢO MẬT LUỒNG ĐĂNG NHẬP (AUTH FLOW)

Nhiều sinh viên lập trình luồng đăng nhập như sau: Mở app -> Hiện màn hình Trang chủ -> Dùng lệnh `useEffect` kiểm tra Token -> Nếu chưa đăng nhập thì `navigation.navigate('LoginScreen')`.
**ĐÂY LÀ LỖI BẢO MẬT CỰC KỲ NGHIÊM TRỌNG!**
Vì Trang chủ đã kịp Mount, kẻ gian có thể chặn (Intercept) thời gian trễ nửa giây đó để ăn cắp dữ liệu, hoặc bấm nút Back trên Android để quay lại Trang chủ lách luật đăng nhập.

**Mô hình Máy Trạng Thái (State Machine) Tiêu chuẩn Enterprise:**
Bản chất của điều hướng an toàn là không bao giờ để Màn hình Auth và Màn hình Main nằm chung trong một Ngăn xếp (Stack).
Chúng ta sử dụng cấu trúc `Conditional Rendering` dựa trên Token:

> [!NOTE]
> Đoạn code dưới đây chỉ là **ví dụ khái niệm** để minh họa State Machine 2 nhánh Auth/Main — tên `MainAppNavigator` ở đây là đặt tạm cho dễ hiểu. Dự án thực chiến **ShopAI dùng `MainTabNavigator`** (Bottom Tab, dựng ở Sprint 5 Bước 5 phía dưới), không phải một `Stack.Navigator` phẳng chỉ có Home/Cart như ví dụ này.

```tsx
// Kiến trúc chuẩn: Người chưa đăng nhập không bao giờ có thể "Hack" để thấy màn hình Home
return (
  <NavigationContainer>
    {userToken == null ? (
      // Nếu chưa có Token -> Cấp cho cái cây có Login
      <AuthStack.Navigator>
        <AuthStack.Screen name="Login" component={LoginScreen} />
      </AuthStack.Navigator>
    ) : (
      // Nếu có Token -> Rút cây cũ, cấp cho cái cây có Home (ShopAI thật sẽ là MainTabNavigator)
      <MainAppNavigator.Navigator>
        <MainAppNavigator.Screen name="Home" component={HomeScreen} />
        <MainAppNavigator.Screen name="Cart" component={CartScreen} />
      </MainAppNavigator.Navigator>
    )}
  </NavigationContainer>
);
```

> [!TIP]
> **Kỹ thuật thay thế: `navigation.reset()`.** Kiến trúc trên (2 cây riêng biệt, đổi `userToken` để React tự unmount/mount lại toàn bộ) là cách AN TOÀN NHẤT và cũng là cách ShopAI dùng. Nhưng nếu dự án của bạn dùng CHUNG một `Stack.Navigator` cho cả Auth lẫn Main (không tách cây), bạn vẫn có thể chặn đứng việc bấm Back quay lại sau khi đăng xuất bằng `navigation.reset()`:
>
> ```tsx
> // Dùng khi Login/Home nằm CHUNG một Stack.Navigator (KHÔNG phải kiến trúc ShopAI đang dùng ở trên)
> const handleLogout = () => {
>   clearToken(); // Xoá Token khỏi SecureStore/State trước
>   navigation.reset({
>     index: 0, // Vị trí màn hình "đang đứng" sau khi reset — 0 = phần tử đầu tiên trong mảng routes
>     routes: [{ name: "Login" }], // Xoá sạch mọi màn hình cũ trong Stack, chỉ còn lại đúng 1 màn hình 'Login'
>   });
> };
> ```
>
> Khác với `navigation.navigate('Login')` (chỉ đẩy thêm Login lên trên, Home vẫn còn ở dưới, bấm Back vẫn quay lại được), `reset()` **xoá sạch toàn bộ lịch sử Back** trước đó. **ShopAI không cần gọi `reset()`** vì kiến trúc 2 cây riêng biệt ở trên đã tự động unmount hoàn toàn Stack cũ khi `userToken` đổi giá trị — nhưng đây là kỹ thuật bắt buộc phải biết khi làm việc với các dự án dùng kiến trúc Single-Stack (thường gặp ở dự án cũ, hoặc khi Auth Guard được cài xen giữa các màn hình thay vì tách hẳn 2 nhánh).

---

## 📦 PHẦN 5.3: NGHỆ THUẬT TRUYỀN DỮ LIỆU (ROUTE PARAMS VS GLOBAL STATE)

Khi chuyển từ `HomeScreen` sang `DetailScreen`, làm sao truyền được dữ liệu sản phẩm?

**Cách 1: Route Params (Truyền qua hàm Navigate)**

```tsx
// Chuyển trang và gửi dữ liệu
navigation.navigate("DetailScreen", {
  productId: "123",
  productName: "iPhone",
});

// Tại DetailScreen, lấy dữ liệu ra:
const { productId, productName } = route.params;
```

> [!CAUTION]
> **Anti-Pattern (Lỗi thiết kế):** Rất nhiều lập trình viên gửi NGUYÊN MỘT OBJECT KHỔNG LỒ (VD: Gửi toàn bộ 1000 trường dữ liệu của User) qua Route Params.
> React Navigation khuyên: **Tuyệt đối không gửi Object phức tạp.** Nó sẽ làm việc chuyển trang bị giật lag khựng khung hình (do phải stringify/parse). Hãy chỉ gửi cái **ID**, rồi sang màn hình kia dùng ID đó gọi API hoặc móc từ Global State ra!

**Cách 2: Global State (Zustand/Redux)**
Nếu dữ liệu cần được truy cập ở 10 màn hình khác nhau (VD: Tổng tiền trong Giỏ hàng), đừng dùng Route Params để truyền vòng vèo qua 10 lớp. Hãy nhét nó lên Đám mây (Global State) để màn hình nào cần thì đưa tay lên lấy. (Sẽ học sâu ở Chương 6).

---

## 🔗 PHẦN 5.4: DEEP LINKING (LIÊN KẾT SÂU)

Bạn đang xem một cái áo trên trình duyệt Chrome. Bạn bấm "Mở trong Shopee". Bùm! Màn hình giật một cái và App Shopee tự động mở ra ngay đúng cái áo đó. Đó là Deep Linking.

**Cơ chế hoạt động:**

- Ta khai báo với hệ điều hành iOS/Android một URL Scheme riêng (VD: `shopai://`).
- Khi hệ thống bắt được link `shopai://product/123`, nó sẽ gọi app ShopAI dậy.
- React Navigation sẽ bắt lấy chữ `/product/123`, tra vào bảng cấu hình (Configuration), và tự động thực thi lệnh `navigation.navigate('DetailScreen', { id: '123' })`.

> [!IMPORTANT]
> Đây là điểm học viên mới hay nhầm nhất: khai báo `linking` ở phía JavaScript (prop `linking` của `NavigationContainer`, xem Sprint 5 Bước 7) **CHƯA ĐỦ** để Deep Link hoạt động. Đó mới chỉ là "luật chơi bên trong App" — hệ điều hành (iOS/Android) còn phải được báo TRƯỚC rằng "ứng dụng ShopAI sẽ nhận và xử lý mọi link bắt đầu bằng `shopai://`". Việc "báo trước" đó nằm ở tầng **Native**, khai báo trong `Info.plist` (iOS) và `AndroidManifest.xml` (Android) — đây chính là phần cấu hình bên dưới.

### 1. Cấu hình Native BẮT BUỘC — iOS: khai báo `CFBundleURLSchemes` trong `Info.plist`

Mở file `ios/ShopAI/Info.plist` bằng Xcode (chọn Target `ShopAI` → tab **Info** → mục **URL Types** → bấm dấu `+`), hoặc sửa trực tiếp file XML:

```xml
<!-- ios/ShopAI/Info.plist -->
<key>CFBundleURLTypes</key>
<array>
  <dict>
    <key>CFBundleURLName</key>
    <string>com.shopai.app</string>
    <key>CFBundleURLSchemes</key>
    <array>
      <string>shopai</string>
    </array>
  </dict>
</array>
```

| Khóa                 | Ý nghĩa                                                                                                                                                    |
| -------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `CFBundleURLName`    | Định danh nội bộ cho khai báo URL này — theo quy ước, đặt trùng `Bundle Identifier` của App (đã thấy ở Chương 9, `com.shopai.app`)                         |
| `CFBundleURLSchemes` | Mảng các tiền tố (scheme) mà App sẽ "lắng nghe" — ở đây là `shopai`, khớp đúng với `prefixes: ['shopai://']` đã khai báo trong `linking` ở Sprint 5 Bước 7 |

### 2. Cấu hình Native BẮT BUỘC — Android: khai báo `intent-filter` trong `AndroidManifest.xml`

Mở `android/app/src/main/AndroidManifest.xml`, tìm đúng `<activity android:name=".MainActivity" ...>` (Activity chính của App), thêm `<intent-filter>` mới vào bên trong:

```xml
<!-- android/app/src/main/AndroidManifest.xml -->
<activity
  android:name=".MainActivity"
  android:exported="true"
  android:launchMode="singleTask"
  ...>

  <!-- Intent-filter mặc định của RN CLI — GIỮ NGUYÊN, không xoá -->
  <intent-filter>
    <action android:name="android.intent.action.MAIN" />
    <category android:name="android.intent.category.LAUNCHER" />
  </intent-filter>

  <!-- ➕ MỚI: Intent-filter cho Deep Linking -->
  <intent-filter android:autoVerify="true">
    <action android:name="android.intent.action.VIEW" />
    <category android:name="android.intent.category.DEFAULT" />
    <category android:name="android.intent.category.BROWSABLE" />
    <data android:scheme="shopai" />
  </intent-filter>
</activity>
```

| Thuộc tính                        | Ý nghĩa                                                                                                                                                                                 |
| --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `android.intent.action.VIEW`      | Khai báo "Activity này có thể MỞ RA để xem 1 nội dung được trỏ tới từ bên ngoài" (khác với `MAIN`/`LAUNCHER` chỉ dùng để mở App từ màn hình Home)                                       |
| `category.BROWSABLE`              | Cho phép trình duyệt/App khác (Zalo, Facebook, Chrome) gọi được link này                                                                                                                |
| `android.launchMode="singleTask"` | Nếu App ShopAI đang chạy sẵn, bấm thêm 1 Deep Link nữa sẽ dùng LẠI đúng instance đang chạy thay vì mở chồng thêm 1 bản App mới — tránh hiện tượng "2 App ShopAI cùng chạy song song"    |
| `data android:scheme="shopai"`    | Khai báo đúng tiền tố `shopai://` — phải khớp 100% với `prefixes` trong `linking` (JS) và `CFBundleURLSchemes` (iOS)                                                                    |
| `android:autoVerify="true"`       | Yêu cầu Android tự xác thực quyền sở hữu link (cần thêm bước `assetlinks.json` nếu dùng App Links `https://` thật — không bắt buộc với scheme tùy chỉnh `shopai://` dùng trong lớp học) |

### 3. Test Deep Linking sau khi Build lại App

> [!IMPORTANT]
> Cả 2 thay đổi trên (`Info.plist`, `AndroidManifest.xml`) đều là mã Native — **Hot Reload/Fast Refresh KHÔNG áp dụng được.** Bắt buộc build lại App hoàn toàn: `npm run ios` / `npm run android` (giống nguyên tắc đã học ở Chương 4/5 mỗi khi cài thư viện có mã Native).

**Cách 1 — dùng `npx uri-scheme` (tiện nhất, chạy được cả 2 nền tảng từ 1 câu lệnh):**

```bash
npx uri-scheme open "shopai://product/123" --ios
npx uri-scheme open "shopai://product/123" --android
```

**Cách 2 — dùng công cụ gốc của từng hệ điều hành:**

```bash
# iOS Simulator — dùng xcrun simctl
xcrun simctl openurl booted "shopai://product/123"

# Android Emulator/Thiết bị thật đã bật USB Debugging — dùng adb
adb shell am start -W -a android.intent.action.VIEW -d "shopai://product/123" com.shopai.app
```

Nếu cấu hình đúng, App ShopAI (đang chạy nền hoặc đang tắt) sẽ tự mở lên và nhảy thẳng vào `ProductDetailScreen` với `productId: '123'` — đúng luồng đã mô tả ở đầu Phần 5.4 và khớp với `linking.config` ở Sprint 5 Bước 7.

> [!WARNING]
> **Bảng lỗi thường gặp khi cấu hình Deep Linking Native:**
>
> | Triệu chứng                                                             | Nguyên nhân                                                                                           | Cách sửa                                                                                                                    |
> | ----------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------- |
> | Chạy `uri-scheme open` không thấy App mở lên                            | Quên Build lại App sau khi sửa `Info.plist`/`AndroidManifest.xml`                                     | Build lại hoàn toàn (`npm run ios`/`android`), không chỉ Reload                                                             |
> | App mở lên nhưng vào thẳng `HomeScreen`, không nhảy vào `ProductDetail` | `scheme` ở Native khớp nhưng `config.screens` trong `linking` (JS) khai báo sai tên Route/Param       | Đối chiếu lại tên `HomeTab`/`ProductDetail` trong `linking` với đúng tên khai báo ở `MainTabNavigator`/`HomeStackNavigator` |
> | Android báo `Activity not found`                                        | Đặt `<intent-filter>` mới nhầm ra NGOÀI thẻ `<activity>` chính, hoặc sai tên `.MainActivity`          | Đảm bảo `<intent-filter>` Deep Link nằm LỒNG bên trong đúng `<activity android:name=".MainActivity">`                       |
> | iOS: link mở Safari thay vì mở App                                      | Thiếu khai báo `CFBundleURLTypes` trong `Info.plist`, hoặc gõ sai `scheme` (VD: `shopai:` thiếu `//`) | Kiểm tra lại chính tả `CFBundleURLSchemes`, rebuild App                                                                     |

---

## 🗄️ PHẦN 5.5: DRAWER NAVIGATOR & KIẾN TRÚC ĐIỀU HƯỚNG TÙY BIẾN (Đề cương 4.1.4, 4.2.2)

### 1. Drawer Navigation — Khi nào dùng, khi nào không?

Đã nhắc sơ ở Phần 5.1 mục 3: Drawer là menu trượt ra từ cạnh (thường là trái) màn hình, chứa danh sách các mục điều hướng xếp dọc. Giờ ta so sánh kỹ hơn với Tab để biết lúc nào nên chọn cái nào.

| Tiêu chí            | Bottom Tab                          | Drawer                                                                   |
| ------------------- | ----------------------------------- | ------------------------------------------------------------------------ |
| Số lượng mục tối ưu | 3-5 mục (không gian đáy hẹp)        | Không giới hạn — cuộn được (Cài đặt, Trợ giúp, Điều khoản, Đăng xuất...) |
| Tốc độ truy cập     | Rất nhanh — luôn hiện sẵn           | Cần 1 lần vuốt/bấm để mở ra                                              |
| Chuẩn nền tảng      | iOS + Android đều quen thuộc        | Android/Material Design ưa chuộng, iOS ít dùng làm điều hướng chính      |
| ShopAI nên dùng cho | Trang chủ, Giỏ hàng — dùng liên tục | Hồ sơ, Cài đặt, Đơn hàng của tôi, Đăng xuất — dùng không thường xuyên    |

> [!TIP]
> Thực tế Enterprise hay **kết hợp cả 2**: Bottom Tab cho 3-4 tính năng lõi dùng liên tục, Drawer lồng ở tầng ngoài cùng chứa thêm các mục phụ mà không làm chật Tab bar. Đây chính là tinh thần "Custom Navigation Architecture" — lồng nhiều Navigator vào nhau theo đúng nhu cầu UX, không có 1 khuôn cố định cho mọi app.

### 2. Cài đặt Drawer Navigator

```bash
npm install @react-navigation/drawer
npm install react-native-gesture-handler react-native-reanimated
```

> `react-native-reanimated` đã được cài ở Chương 4 (cho hiệu ứng Fade-in của `ProductCard`) — chạy lại lệnh trên vẫn an toàn, npm tự bỏ qua nếu đã có. `react-native-gesture-handler` là thư viện MỚI, bắt buộc để bắt cử chỉ vuốt-mở Drawer.

**Bắt buộc với iOS (Link Native Code):**

```bash
cd ios && pod install && cd ..
```

**Bắt buộc — khai báo `react-native-gesture-handler` ở dòng ĐẦU TIÊN của `index.js`** (trước cả `import App`):

```js
import "react-native-gesture-handler"; // Phải là dòng import đầu tiên của toàn bộ app
import { AppRegistry } from "react-native";
import App from "./App";
// ...
```

### 3. Code mẫu: `Drawer.Navigator` với Home + Profile

```tsx
// src/navigation/RootDrawerNavigator.tsx — ví dụ minh hoạ, KHÔNG bắt buộc thay MainTabNavigator
import React from "react";
import { createDrawerNavigator } from "@react-navigation/drawer";
import MainTabNavigator from "@navigation/MainTabNavigator";
import ProfileScreen from "@screens/ProfileScreen";

const Drawer = createDrawerNavigator();

interface Props {
  onLogout: () => void;
}

const RootDrawerNavigator = ({ onLogout }: Props) => {
  return (
    <Drawer.Navigator
      screenOptions={{
        headerShown: true,
        drawerActiveTintColor: "#FF4D4F", // Trùng COLORS.primary trong theme.ts
      }}
    >
      {/* Toàn bộ MainTabNavigator (Home + Cart) được nhồi vào làm 1 "trang" của Drawer */}
      <Drawer.Screen name="MainApp" options={{ title: "ShopAI" }}>
        {() => <MainTabNavigator onLogout={onLogout} />}
      </Drawer.Screen>
      <Drawer.Screen
        name="Profile"
        component={ProfileScreen}
        options={{ title: "Hồ sơ của tôi" }}
      />
    </Drawer.Navigator>
  );
};

export default RootDrawerNavigator;
```

> [!NOTE]
> Để ý: `Drawer.Navigator` **bọc bên ngoài** `MainTabNavigator`, còn `MainTabNavigator` lại bọc bên ngoài `HomeStackNavigator` (đã dựng ở Sprint 5, Bước 4). Đây chính là mô hình **Navigator lồng Navigator (Nested Navigators)** — mỗi tầng đảm nhiệm đúng 1 việc: Drawer lo menu phụ, Tab lo 3-4 tính năng lõi dùng liên tục, Stack lo Push/Pop chi tiết bên trong từng Tab.

### 4. Custom Navigation — Tùy biến Header & tư duy "kiến trúc lồng"

Ngoài Drawer, "Custom Navigation" còn bao gồm việc tùy biến sâu Header của từng Navigator bằng `options`/`screenOptions`:

```tsx
<Stack.Screen
  name="ProductDetail"
  component={ProductDetailScreen}
  options={() => ({
    title: "Chi tiết sản phẩm",
    headerRight: () => (
      <ShopButton
        title="♡"
        onPress={() => {
          /* thêm vào Wishlist */
        }}
        style={{ width: 40, height: 32, backgroundColor: "transparent" }}
      />
    ),
  })}
/>
```

Kết hợp với việc lồng Navigator (Stack trong Tab, và Tab có thể lồng trong Drawer như vừa xem ở mục 3), bạn có toàn quyền thiết kế "bản đồ điều hướng" phù hợp với từng ứng dụng — không nhất thiết phải theo đúng 1 công thức có sẵn.

---

## 🗺️ PHẦN 5.6: XU HƯỚNG ĐIỀU HƯỚNG 2025–2026 — EXPO ROUTER VS REACT NAVIGATION

### 1. File-based Routing — Xu hướng đang lên

`React Navigation` (đang dùng trong ShopAI) là kiểu **Code-based Routing**: bạn tự tay khai báo từng `Screen` trong `Stack.Navigator`/`Tab.Navigator` bằng code, như đã làm xuyên suốt chương này.

**Expo Router** đi theo triết lý khác — **File-based Routing** (giống Next.js bên Web): cấu trúc thư mục `app/` quyết định luôn cấu trúc điều hướng, không cần khai báo `Stack.Screen` thủ công:

```
app/
  _layout.tsx        →  Layout gốc (tương đương NavigationContainer + Stack.Navigator)
  index.tsx           →  Route "/"  (màn hình Home)
  product/[id].tsx     →  Route "/product/123" (tự động nhận id qua useLocalSearchParams)
  (tabs)/_layout.tsx    →  Định nghĩa Bottom Tab chỉ bằng cách đặt tên thư mục (tabs)
  (tabs)/cart.tsx      →  Tab "Giỏ hàng"
```

Chỉ cần tạo đúng file/thư mục theo quy ước, Expo Router tự sinh ra Route + hỗ trợ **Deep Linking mặc định** cho mọi màn hình (không cần khai báo `linking` thủ công như Phần 5.4) — vì bản chất mỗi file đã là 1 URL sẵn.

### 2. ShopAI chọn React Navigation V7 — Vì sao đây vẫn là lựa chọn ĐÚNG?

| Tiêu chí                              | React Navigation (Code-based)                               | Expo Router (File-based)                                         |
| ------------------------------------- | ----------------------------------------------------------- | ---------------------------------------------------------------- |
| Cách khai báo Route                   | Viết `Stack.Screen` bằng tay                                | Tạo file theo quy ước thư mục                                    |
| Deep Linking                          | Cấu hình thủ công (`linking` — Phần 5.4)                    | Có sẵn mặc định theo tên file                                    |
| Độ linh hoạt kiến trúc lồng Navigator | Rất cao — tự do lồng Stack/Tab/Drawer bất kỳ đâu (Phần 5.5) | Bị ràng buộc theo quy ước thư mục của Expo Router                |
| Yêu cầu hạ tầng                       | Chạy tốt trên cả Bare RN CLI lẫn Expo                       | Cần chạy trên nền Expo (Expo Router phụ thuộc chặt vào Expo SDK) |
| Độ phổ biến tuyển dụng                | Chuẩn công nghiệp lâu năm, đa số dự án Enterprise/Bare RN   | Đang tăng nhanh, mạnh ở các dự án Expo-first mới                 |

> [!IMPORTANT]
> **ShopAI là dự án Bare RN CLI** (đã `react-native init` từ Chương 1, chỉ mượn "Expo Modules API" cho vài thư viện lẻ như `expo-secure-store` ở Chương 8) — không phải dự án Expo-first. **React Navigation V7 là lựa chọn đúng đắn và tiêu chuẩn của toàn ngành cho kiến trúc này.** Nếu bạn khởi tạo một dự án MỚI bằng `npx create-expo-app` (Expo thuần từ đầu), Expo Router lúc đó mới là lựa chọn tự nhiên và được khuyến nghị hàng đầu.

### 3. Khi nào Expo Router tỏa sáng?

Expo Router hợp nhất với các dự án **Expo-first** (khởi tạo bằng `create-expo-app`, không cần "thoát" ra Bare RN CLI để dùng Native Module tùy biến sâu): tốc độ dựng MVP nhanh, Deep Linking miễn phí, cấu trúc thư mục tự nói lên bản đồ điều hướng — rất hợp cho App vừa/nhỏ, đội ngũ nhỏ, hoặc Prototype cần ra mắt nhanh.

> [!NOTE]
> **Không cần chuyển đổi ShopAI sang Expo Router** — biết sự tồn tại và điểm mạnh của nó để tự tin lựa chọn đúng công cụ ở dự án tương lai, và để trả lời phỏng vấn khi được hỏi "Expo Router khác gì React Navigation?".

---

## 🚀 THỰC CHIẾN SHOPAI (SPRINT 5: AUTH FLOW, BOTTOM TAB & CHI TIẾT SẢN PHẨM)

**User Story:** _"Là một Kỹ sư trưởng, tôi muốn cài đặt bộ khung Điều hướng an toàn (AuthStack: Đăng nhập + Đăng ký tách biệt luồng Ứng dụng chính) với Thanh Tab dưới đáy, cho phép Khách hàng bấm vào sản phẩm để xem Chi tiết, để chặn đứng nguy cơ rò rỉ dữ liệu cho người chưa xác thực."_

### 📋 Khung thực hành chương (đọc trước khi gõ code)

> Đây là **bài thực hành của Chương 5** (không phải “lab mỗi ngày”). Làm hết Sprint này = đạt mục tiêu chương. Hoàn thành đủ 11 Sprint = sản phẩm ShopAI theo `SHOPAI_HOAN_THIEN.md`.

| Hạng mục                 | Nội dung                                                                                               |
| ------------------------ | ------------------------------------------------------------------------------------------------------ |
| **Thời lượng gợi ý**     | 5–7 tiết                                                                                               |
| **Độ khó chương**        | ★★★★☆                                                                                                  |
| **Đầu vào bắt buộc**     | Sprint 4 PASS — Home FlashList + ProductCard.                                                          |
| **Đầu ra sản phẩm**      | Auth Flow (Login **+ Register**) + Bottom Tab (icon/badge) + Detail theo productId + Deep Link native. |
| **Cách làm**             | Làm **tuần tự từng Bước**. Gặp mốc ✓ bên dưới mà FAIL → dừng, sửa, rồi mới sang bước sau.              |
| **Nghiệm thu cuối khóa** | Đối chiếu `SHOPAI_HOAN_THIEN.md` — mỗi Sprint chỉ tích thêm ô, không phá tính năng cũ.                 |

### ✓ Kiểm chứng theo mốc (trong lúc làm)

- **Sau Bước 2–2.5:** Login ↔ Register trong AuthStack; validate form đăng ký.
- **Sau Bước 3–5:** Login → vào Tab; Tab có icon; Cart placeholder.
- **Sau Bước 6:** Bấm SP → Detail đúng id; **vẫn giữ** pull-to-refresh nếu đã làm Ch4.
- **Sau Bước 7–7b:** Deep Link `shopai://...` mở được (sau rebuild native).

> [!TIP]
> Xong Sprint 5, mở `SHOPAI_HOAN_THIEN.md` và tick các ô thuộc chương này. Mục tiêu cuối khóa: **mọi ô A/B/C/D (+ E đề cương) đều xanh** trong `SHOPAI_HOAN_THIEN.md` — đó mới là ShopAI hoàn thiện đẳng cấp.

### Yêu cầu Nghiệm thu:

1. Cài đặt thành công React Navigation V7 kèm `@react-navigation/bottom-tabs`.
2. `LoginScreen` dùng `ShopInput` (Email + Mật khẩu) của UI Kit Chương 3, có validate cơ bản (Email phải chứa `@`, Mật khẩu ≥ 6 ký tự).
3. Có **`RegisterScreen`** trong cùng `AuthStack`: Họ tên + Email + Mật khẩu + Xác nhận mật khẩu; validate khớp mật khẩu; liên kết qua lại với Login (`navigate('Register')` / `navigate('Login')`). Đăng ký thành công (giả lập ở Ch.5) → vào Main như đăng nhập. _(API thật `POST /api/auth/register` ở Chương 9.)_
4. Sau khi đăng nhập/đăng ký, vào thẳng **Bottom Tab Navigator** gồm Tab "Trang chủ" và Tab "Giỏ hàng" (Placeholder, sẽ hoàn thiện ở Chương 6).
5. Bấm vào một `ProductCard` ở Home → mở `ProductDetailScreen`, nhận `productId` qua Route Params (KHÔNG gửi nguyên Object sản phẩm).
6. Auth Flow State Machine vẫn đảm bảo: Chưa đăng nhập thì không cách nào (kể cả bấm Back) thấy được Tab Navigator.
7. Có cấu hình Deep Linking tối giản khai báo trên `NavigationContainer`, **kèm cấu hình Native thật** ở cả iOS (`Info.plist`) lẫn Android (`AndroidManifest.xml`), test được bằng `npx uri-scheme` hoặc `xcrun`/`adb` (Phần 5.4, Bước 7b).
8. `MainTabNavigator` có `tabBarIcon` cho cả 2 Tab (dùng `react-native-vector-icons`, Bước 4.5) và `tabBarBadge` hiển thị số lượng ở Tab "Giỏ hàng" (Bước 5).
9. Có ví dụ `navigation.reset()` (Phần 5.2) để hiểu kỹ thuật thay thế khi không dùng kiến trúc 2-cây-riêng-biệt.
10. _(Tuỳ chọn — áp dụng lý thuyết Phần 5.5)_ Có `ProfileScreen` placeholder và thử nghiệm bọc `MainTabNavigator` bằng `Drawer.Navigator` (không nhất thiết phải giữ trong bản chính thức của ShopAI).

### Hướng dẫn thực thi Step-by-Step:

#### Bước 1: Cài đặt thư viện React Navigation V7 + Bottom Tabs

Mở Terminal và chạy các lệnh sau (Cài đặt core, Stack, Tab và các thư viện Native hỗ trợ cử chỉ vuốt):

```bash
npm install @react-navigation/native @react-navigation/native-stack @react-navigation/bottom-tabs
npm install react-native-screens react-native-safe-area-context
```

> `react-native-safe-area-context` có thể bạn đã cài ở Chương 4 (cho `SafeAreaView`) — chạy lại lệnh trên vẫn an toàn, npm sẽ tự bỏ qua nếu đã có.

**Bắt buộc đối với iOS (Link Native Code):**
Vì các thư viện trên có chứa code C/Objective-C, ta phải liên kết chúng vào Xcode:

```bash
cd ios
pod install
cd ..
```

#### Bước 2: Nâng cấp LoginScreen dùng ShopInput

Tạo/cập nhật file `src/screens/LoginScreen.tsx`, thay nút bấm đơn độc bằng 2 ô nhập liệu chuẩn UI Kit:

```tsx
import React, { useState } from "react";
import { View, Text, StyleSheet, Pressable } from "react-native";
import ShopButton from "@components/ShopButton";
import ShopInput from "@components/ui/ShopInput";
import { COLORS, SIZES } from "@constants/theme";

// Chú ý: Ở bài này ta truyền giả lập onLogin qua Props để hiểu Auth Flow.
// Ở chương sau ta sẽ đổi sang dùng Zustand để tránh Prop Drilling.
const LoginScreen = ({
  onLogin,
  onGoRegister,
}: {
  onLogin: (token: string) => void;
  onGoRegister: () => void;
}) => {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [errors, setErrors] = useState<{ email?: string; password?: string }>(
    {},
  );
  const [loading, setLoading] = useState(false);

  // Validate đơn giản: Email phải chứa @, Mật khẩu tối thiểu 6 ký tự
  const validate = () => {
    const next: { email?: string; password?: string } = {};
    if (!email.includes("@")) next.email = "Email không hợp lệ (phải chứa @)";
    if (password.length < 6) next.password = "Mật khẩu phải có ít nhất 6 ký tự";
    setErrors(next);
    return Object.keys(next).length === 0;
  };

  const handleLogin = () => {
    if (!validate()) return;
    setLoading(true);
    // Giả lập gọi API server
    setTimeout(() => {
      setLoading(false);
      onLogin("mock_token_123"); // Cấp token
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

      {/* Liên kết sang màn Đăng ký trong cùng AuthStack (Bước 2.5) */}
      <Pressable onPress={onGoRegister} style={styles.registerLink}>
        <Text style={styles.registerLinkText}>
          Chưa có tài khoản?{" "}
          <Text style={styles.registerLinkBold}>Đăng ký</Text>
        </Text>
      </Pressable>
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
  title: {
    fontSize: 40,
    fontWeight: "900",
    color: COLORS.primary,
    textAlign: "center",
    marginBottom: 10,
  },
  subtitle: {
    fontSize: SIZES.body1,
    color: COLORS.textLight,
    textAlign: "center",
    marginBottom: 32,
  },
  loginBtn: {
    marginTop: 8,
  },
  registerLink: {
    marginTop: 20,
    alignItems: "center",
  },
  registerLinkText: {
    fontSize: SIZES.body2,
    color: COLORS.textLight,
  },
  registerLinkBold: {
    color: COLORS.primary,
    fontWeight: "700",
  },
});

export default LoginScreen;
```

#### Bước 2.5: Tạo `RegisterScreen` — hoàn thiện AuthStack thương mại

App thương mại không chỉ có Đăng nhập. Tạo `src/screens/RegisterScreen.tsx`:

```tsx
import React, { useState } from "react";
import { View, Text, StyleSheet, Pressable, ScrollView } from "react-native";
import ShopButton from "@components/ShopButton";
import ShopInput from "@components/ui/ShopInput";
import { COLORS, SIZES } from "@constants/theme";

const RegisterScreen = ({
  onRegistered,
  onGoLogin,
}: {
  onRegistered: (token: string) => void;
  onGoLogin: () => void;
}) => {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirm, setConfirm] = useState("");
  const [errors, setErrors] = useState<{
    name?: string;
    email?: string;
    password?: string;
    confirm?: string;
  }>({});
  const [loading, setLoading] = useState(false);

  const validate = () => {
    const next: typeof errors = {};
    if (name.trim().length < 2) next.name = "Họ tên tối thiểu 2 ký tự";
    if (!email.includes("@")) next.email = "Email không hợp lệ (phải chứa @)";
    if (password.length < 6) next.password = "Mật khẩu phải có ít nhất 6 ký tự";
    if (confirm !== password) next.confirm = "Xác nhận mật khẩu không khớp";
    setErrors(next);
    return Object.keys(next).length === 0;
  };

  const handleRegister = () => {
    if (!validate()) return;
    setLoading(true);
    // Ch.5: giả lập đăng ký thành công → cấp token như login.
    // Ch.9: đổi thành POST /api/auth/register thật (bcrypt + Prisma).
    setTimeout(() => {
      setLoading(false);
      onRegistered("mock_token_123");
    }, 1200);
  };

  return (
    <ScrollView
      contentContainerStyle={styles.container}
      keyboardShouldPersistTaps="handled"
    >
      <Text style={styles.title}>Tạo tài khoản</Text>
      <Text style={styles.subtitle}>Đăng ký để mua sắm trên ShopAI</Text>

      <ShopInput
        label="Họ tên"
        placeholder="Nguyễn Văn A"
        value={name}
        onChangeText={setName}
        error={errors.name}
      />
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
      <ShopInput
        label="Xác nhận mật khẩu"
        placeholder="Nhập lại mật khẩu"
        value={confirm}
        onChangeText={setConfirm}
        error={errors.confirm}
        secureTextEntry
      />

      <ShopButton
        title="Đăng ký ngay"
        onPress={handleRegister}
        isLoading={loading}
        style={styles.submitBtn}
      />

      <Pressable onPress={onGoLogin} style={styles.loginLink}>
        <Text style={styles.loginLinkText}>
          Đã có tài khoản? <Text style={styles.loginLinkBold}>Đăng nhập</Text>
        </Text>
      </Pressable>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flexGrow: 1,
    backgroundColor: COLORS.background,
    justifyContent: "center",
    padding: SIZES.padding,
  },
  title: {
    fontSize: 32,
    fontWeight: "900",
    color: COLORS.primary,
    textAlign: "center",
    marginBottom: 10,
  },
  subtitle: {
    fontSize: SIZES.body1,
    color: COLORS.textLight,
    textAlign: "center",
    marginBottom: 32,
  },
  submitBtn: { marginTop: 8 },
  loginLink: { marginTop: 20, alignItems: "center" },
  loginLinkText: { fontSize: SIZES.body2, color: COLORS.textLight },
  loginLinkBold: { color: COLORS.primary, fontWeight: "700" },
});

export default RegisterScreen;
```

> [!IMPORTANT]
> **Tại sao Đăng ký nằm ở Chương 5, không phải Chương 9?** Chương 5 dạy **Auth Flow / AuthStack** — học viên phải thấy đủ 2 cửa vào (Login ↔ Register) trước khi có Backend. Chương 9 chỉ **đổi nguồn dữ liệu** (mock → Nest + bcrypt), không đổi kiến trúc điều hướng.

#### Bước 3: Tạo ProductDetailScreen (nhận `productId` qua Route Params)

Đúng theo lý thuyết Phần 5.3: chỉ gửi cái **ID**, không gửi nguyên Object. Tạo file `src/screens/ProductDetailScreen.tsx`:

```tsx
import React from "react";
import { View, Text, StyleSheet, Image, ScrollView } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { RouteProp, useRoute } from "@react-navigation/native";
import ShopButton from "@components/ShopButton";
import { MOCK_PRODUCTS } from "@data/mockProducts";
import { COLORS, SIZES } from "@constants/theme";
import type { HomeStackParamList } from "@navigation/HomeStackNavigator";

type ProductDetailRouteProp = RouteProp<HomeStackParamList, "ProductDetail">;

const ProductDetailScreen = () => {
  const route = useRoute<ProductDetailRouteProp>();
  const { productId } = route.params; // Chỉ nhận đúng 1 chuỗi ID, KHÔNG nhận Object

  // Từ ID, tự tra cứu lại dữ liệu đầy đủ (Ở Chương 6 sẽ đổi thành gọi API/Global State)
  const product = MOCK_PRODUCTS.find((p) => p.id === productId);

  if (!product) {
    return (
      <SafeAreaView style={styles.safeArea}>
        <Text style={styles.notFound}>
          Không tìm thấy sản phẩm với ID: {productId}
        </Text>
      </SafeAreaView>
    );
  }

  return (
    <SafeAreaView style={styles.safeArea}>
      <ScrollView contentContainerStyle={styles.container}>
        <Image
          source={{ uri: product.image }}
          style={styles.image}
          resizeMode="cover"
        />
        <Text style={styles.name}>{product.name}</Text>
        <Text style={styles.price}>
          {new Intl.NumberFormat("vi-VN", {
            style: "currency",
            currency: "VND",
          }).format(product.price)}
        </Text>
        <Text style={styles.idNote}>Mã sản phẩm: {product.id}</Text>
        <ShopButton
          title="Thêm vào giỏ hàng"
          onPress={() => {}}
          style={styles.buyBtn}
        />
      </ScrollView>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: COLORS.background },
  container: { padding: SIZES.padding },
  image: {
    width: "100%",
    height: 320,
    borderRadius: SIZES.radius,
    marginBottom: SIZES.padding,
  },
  name: {
    fontSize: SIZES.h2,
    fontWeight: "bold",
    color: COLORS.text,
    marginBottom: 8,
  },
  price: {
    fontSize: SIZES.h1,
    fontWeight: "bold",
    color: COLORS.primary,
    marginBottom: 8,
  },
  idNote: { fontSize: SIZES.body2, color: COLORS.textLight, marginBottom: 24 },
  buyBtn: { marginTop: 8 },
  notFound: {
    padding: SIZES.padding,
    fontSize: SIZES.body1,
    color: COLORS.error,
    textAlign: "center",
  },
});

export default ProductDetailScreen;
```

#### Bước 4: Tạo HomeStackNavigator (Stack lồng trong Tab)

Home không đứng đơn độc nữa — nó là một cái Stack riêng (Home + ProductDetail), rồi cái Stack này mới được nhồi vào bên trong Tab "Trang chủ" ở Bước 5. Tạo file `src/navigation/HomeStackNavigator.tsx`:

```tsx
import React from "react";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import HomeScreen from "@screens/HomeScreen";
import ProductDetailScreen from "@screens/ProductDetailScreen";

// Khai báo kiểu dữ liệu Route Params cho toàn bộ Stack này — TypeScript sẽ tự
// báo lỗi nếu bạn quên gửi productId hoặc gửi sai kiểu khi gọi navigate()
export type HomeStackParamList = {
  Home: undefined;
  ProductDetail: { productId: string };
  // Scanner: undefined; // Sẽ bổ sung Scanner mã vạch ở chương sau
};

const Stack = createNativeStackNavigator<HomeStackParamList>();

interface Props {
  onLogout: () => void;
}

const HomeStackNavigator = ({ onLogout }: Props) => {
  return (
    <Stack.Navigator>
      <Stack.Screen name="Home" options={{ headerShown: false }}>
        {() => <HomeScreen onLogout={onLogout} />}
      </Stack.Screen>
      <Stack.Screen
        name="ProductDetail"
        component={ProductDetailScreen}
        options={{ title: "Chi tiết sản phẩm" }}
      />
    </Stack.Navigator>
  );
};

export default HomeStackNavigator;
```

#### Bước 4.5: Cài đặt Icon cho Bottom Tab (`react-native-vector-icons`)

ShopAI là dự án **Bare RN CLI thuần** (chưa cài Expo Modules API — hạ tầng đó chỉ xuất hiện từ Chương 8 khi thêm `expo-secure-store`). Vì vậy Tab Bar ở bước này dùng **`react-native-vector-icons`** thay vì `@expo/vector-icons`.

> [!NOTE]
> Nếu bạn đang học trên một dự án Expo-first (khởi tạo bằng `create-expo-app`), hoặc ShopAI của bạn **đã đi tới Chương 8** (đã có hạ tầng Expo Modules API), `@expo/vector-icons` là lựa chọn tương đương — cài bằng `npx expo install @expo/vector-icons`, API dùng gần như giống hệt (`<MaterialCommunityIcons name="..." size={size} color={color} />`), chỉ khác cách cài đặt Native (Expo Modules tự lo phần link, không cần sửa tay `Info.plist`/`build.gradle` như bên dưới).

Cài đặt thư viện:

```bash
npm install react-native-vector-icons
npm install --save-dev @types/react-native-vector-icons
```

**Bắt buộc với iOS** — link Pod:

```bash
cd ios && pod install && cd ..
```

**Bắt buộc với iOS** — khai báo Font trong `ios/ShopAI/Info.plist` (thêm khóa `UIAppFonts`, chỉ cần liệt kê đúng bộ Icon sẽ dùng — ở đây là `MaterialCommunityIcons`):

```xml
<key>UIAppFonts</key>
<array>
  <string>MaterialCommunityIcons.ttf</string>
</array>
```

**Bắt buộc với Android** — mở `android/app/build.gradle`, thêm dòng sau vào **CUỐI file** (Gradle sẽ tự động copy toàn bộ font Icon cần dùng vào bản build):

```groovy
apply from: "../../node_modules/react-native-vector-icons/fonts.gradle"
```

Vì đây là thay đổi Native (thêm Font + link Pod), phải Build lại App hoàn toàn:

```bash
npm run ios
npm run android
```

> [!TIP]
> `react-native-vector-icons` đóng gói sẵn hơn 10 bộ Icon phổ biến (MaterialCommunityIcons, Ionicons, FontAwesome5, Feather...). ShopAI chọn bộ `MaterialCommunityIcons` vì có đủ các icon dạng "outline" cần cho Tab Bar: `home-variant-outline`, `cart-outline`, `account-outline`.

#### Bước 5: Tạo CartScreen (Placeholder) và MainTabNavigator

Tạo file `src/screens/CartScreen.tsx` — Chương 6 mới xây dựng logic Giỏ hàng thật với Zustand, giờ chỉ cần khung sườn:

```tsx
import React from "react";
import { View, Text, StyleSheet } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { COLORS, SIZES } from "@constants/theme";

// Placeholder: Logic Giỏ hàng thật (thêm/xóa/tính tổng tiền) sẽ làm ở Chương 6 với Zustand
const CartScreen = () => {
  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.container}>
        <Text style={styles.emoji}>🛒</Text>
        <Text style={styles.title}>Giỏ hàng trống</Text>
        <Text style={styles.subtitle}>Sẽ làm ở Chương 6</Text>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: COLORS.background },
  container: { flex: 1, justifyContent: "center", alignItems: "center" },
  emoji: { fontSize: 48, marginBottom: 12 },
  title: { fontSize: SIZES.h2, fontWeight: "bold", color: COLORS.text },
  subtitle: { fontSize: SIZES.body2, color: COLORS.textLight, marginTop: 4 },
});

export default CartScreen;
```

Tạo file `src/navigation/MainTabNavigator.tsx` để ráp Tab "Trang chủ" (chứa cả HomeStack bên trong) và Tab "Giỏ hàng" — có kèm `tabBarIcon` (Bước 4.5) và `tabBarBadge` hiện số lượng sản phẩm trong giỏ:

```tsx
import React from "react";
import { createBottomTabNavigator } from "@react-navigation/bottom-tabs";
import Icon from "react-native-vector-icons/MaterialCommunityIcons";
import HomeStackNavigator from "@navigation/HomeStackNavigator";
import CartScreen from "@screens/CartScreen";
import { COLORS } from "@constants/theme";

const Tab = createBottomTabNavigator();

interface Props {
  onLogout: () => void;
  // Số lượng hiện trên chấm đỏ (badge) của Tab Giỏ hàng.
  // Sprint 5 (chưa có Zustand) chỉ nhận giá trị tĩnh qua Props từ App.tsx.
  // Sau Chương 6, giá trị này sẽ đọc trực tiếp từ useCartStore().totalQuantity() ngay
  // BÊN TRONG component này — xoá hẳn tầng Prop Drilling cartBadgeCount này.
  cartBadgeCount?: number;
}

const MainTabNavigator = ({ onLogout, cartBadgeCount = 0 }: Props) => {
  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarActiveTintColor: COLORS.primary,
        tabBarInactiveTintColor: COLORS.textLight,
      }}
    >
      <Tab.Screen
        name="HomeTab"
        options={{
          title: "Trang chủ",
          // tabBarIcon nhận sẵn { focused, color, size } từ React Navigation —
          // color/size đã tự động khớp với tabBarActiveTintColor/InactiveTintColor ở trên
          tabBarIcon: ({ color, size }) => (
            <Icon name="home-variant-outline" color={color} size={size} />
          ),
        }}
      >
        {/* Truyền onLogout xuyên qua Tab -> Stack -> Home (đây chính là Prop Drilling
            mà Chương 6 sẽ giải quyết triệt để bằng Zustand) */}
        {() => <HomeStackNavigator onLogout={onLogout} />}
      </Tab.Screen>

      <Tab.Screen
        name="Cart"
        component={CartScreen}
        options={{
          title: "Giỏ hàng",
          tabBarIcon: ({ color, size }) => (
            <Icon name="cart-outline" color={color} size={size} />
          ),
          // tabBarBadge: chấm đỏ số lượng hiện trên góc icon.
          // Truyền `undefined` (KHÔNG phải 0) để React Navigation tự ẩn hẳn chấm badge khi giỏ hàng trống.
          tabBarBadge: cartBadgeCount > 0 ? cartBadgeCount : undefined,
        }}
      />
    </Tab.Navigator>
  );
};

export default MainTabNavigator;
```

> [!NOTE]
> **Về `cartBadgeCount` ở Sprint 5:** Chưa có Giỏ hàng thật (Chương 6 mới xây `useCartStore` với Zustand), nên giá trị này chỉ là một con số demo truyền tĩnh từ `App.tsx` (xem Bước 7) — mục đích là để thấy `tabBarBadge` hoạt động đúng cách trên UI thật trước khi nối vào dữ liệu thật. Sau Chương 6, xoá hẳn prop `cartBadgeCount`, gọi thẳng `const totalQuantity = useCartStore((s) => s.totalQuantity());` ngay trong `MainTabNavigator` rồi gán `tabBarBadge: totalQuantity > 0 ? totalQuantity : undefined`.

#### Bước 6: Cập nhật HomeScreen — bấm vào sản phẩm để mở Chi tiết

> [!WARNING]
> **Giữ nguyên Pull-to-refresh từ Chương 4.** Nếu bạn đã làm Sprint 4 Bước 4.5 (`products` / `refreshing` / `onRefresh`), **KHÔNG** xóa hết `HomeScreen` rồi dán đè bản dưới đây một cách mù quáng. Cách đúng:
>
> 1. **GIỮ** state `products`, `refreshing`, hàm `onRefresh`, và props `refreshing`/`onRefresh` của `FlashList`.
> 2. **THÊM** `useNavigation` + bọc `ProductCard` bằng `Pressable` → `navigate('ProductDetail', { productId })`.
> 3. **THÊM** nút Logout vào header như snippet.
>
> Bản code đầy đủ bên dưới là **mẫu tối thiểu** cho học viên chưa làm refresh ở Ch4. Nếu đã có refresh: chỉ **merge** phần navigation, vẫn `data={products}` (không quay lại hardcode `MOCK_PRODUCTS` nếu bạn đã có state).

Mở file `src/screens/HomeScreen.tsx`, thêm nút Logout vào Header và bọc `ProductCard` bằng `Pressable` để điều hướng:

```tsx
import React from "react";
import { View, Text, StyleSheet, Pressable } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { useNavigation } from "@react-navigation/native";
import type { NativeStackNavigationProp } from "@react-navigation/native-stack";
import { FlashList } from "@shopify/flash-list";
import ProductCard from "@components/ProductCard";
import ShopButton from "@components/ShopButton";
import { MOCK_PRODUCTS } from "@data/mockProducts";
import { COLORS, SIZES } from "@constants/theme";
import type { HomeStackParamList } from "@navigation/HomeStackNavigator";

type HomeNavProp = NativeStackNavigationProp<HomeStackParamList, "Home">;

const HomeScreen = ({ onLogout }: { onLogout: () => void }) => {
  const navigation = useNavigation<HomeNavProp>();
  // Nếu đã có pull-to-refresh (Ch4): giữ `const [products, setProducts] = useState(MOCK_PRODUCTS)`
  // và `refreshing`/`onRefresh` — FlashList dùng data={products} + refreshing/onRefresh.

  return (
    <SafeAreaView style={styles.safeArea} edges={["top", "left", "right"]}>
      <View style={styles.container}>
        <View style={styles.header}>
          <Text style={styles.headerTitle}>Khám phá</Text>
          <ShopButton
            title="Thoát"
            onPress={onLogout}
            style={{ width: 80, height: 32, backgroundColor: COLORS.textLight }}
          />
        </View>
        <FlashList
          data={MOCK_PRODUCTS}
          keyExtractor={(item) => item.id}
          renderItem={({ item }) => (
            // Chỉ gửi productId (ID) qua navigate, không gửi nguyên object sản phẩm
            <Pressable
              onPress={() =>
                navigation.navigate("ProductDetail", { productId: item.id })
              }
            >
              <ProductCard product={item} />
            </Pressable>
          )}
          numColumns={2}
          estimatedItemSize={260}
          contentContainerStyle={{ padding: SIZES.padding / 2 }}
        />
      </View>
    </SafeAreaView>
  );
};

// ... giữ nguyên styles cũ, sửa thêm style.header:
const styles = StyleSheet.create({
  // ...
  header: {
    paddingHorizontal: SIZES.padding,
    paddingVertical: 15,
    backgroundColor: COLORS.surface,
    flexDirection: "row", // Chuyển Flexbox sang ngang
    justifyContent: "space-between", // Đẩy title và nút thoát ra xa
    alignItems: "center", // Căn giữa theo trục phụ
  },
  // ...
});
```

> [!WARNING]
> Các dấu `// ...` trong đoạn trên có nghĩa là "các thuộc tính/style khác giữ nguyên như cũ" — đây là ký hiệu RÚT GỌN để tiết kiệm chỗ trong giáo trình, **KHÔNG PHẢI code thật**. Khi áp dụng vào file `HomeScreen.tsx` của bạn: chỉ tìm và **SỬA đúng object `header` đang có sẵn** bên trong `StyleSheet.create({...})` hiện tại, rồi giữ nguyên toàn bộ các object style khác (`safeArea`, `container`, `title`,...). **Tuyệt đối không copy-paste cả khối trên rồi thay đè toàn bộ `StyleSheet.create({...})` cũ** — làm vậy sẽ xóa mất hết các style khác đang chạy tốt và gây lỗi thiếu style ở những chỗ khác trong màn hình.

#### Bước 7: Cấu hình Tối Thượng tại `App.tsx` (Auth Flow + Deep Linking)

Mở `App.tsx`, tạo State Machine để quản lý luồng, đồng thời khai báo cấu hình Deep Linking tối giản để link `shopai://product/123` mở thẳng vào đúng màn hình Chi tiết sản phẩm:

```tsx
import React, { useState } from "react";
import { NavigationContainer, LinkingOptions } from "@react-navigation/native";
import { createNativeStackNavigator } from "@react-navigation/native-stack";
import { SafeAreaProvider } from "react-native-safe-area-context";
import { ThemeProvider } from "@contexts/ThemeContext";
import LoginScreen from "@screens/LoginScreen";
import RegisterScreen from "@screens/RegisterScreen";
import MainTabNavigator from "@navigation/MainTabNavigator";

// Chỉ còn 1 Stack cho luồng Auth — luồng Main giờ do MainTabNavigator (Bottom Tab) đảm nhiệm
const AuthStack = createNativeStackNavigator();

// Cấu hình Deep Linking tối giản: shopai://product/123 -> tự navigate vào ProductDetail
// (Phần khai báo URL Scheme Native đầy đủ cho iOS/Android sẽ hoàn thiện ở giai đoạn xuất bản App)
const linking: LinkingOptions<any> = {
  prefixes: ["shopai://"],
  config: {
    screens: {
      HomeTab: {
        screens: {
          ProductDetail: "product/:productId",
        },
      },
    },
  },
};

function App(): React.JSX.Element {
  // State quản lý Token (Chương sau sẽ đưa cái này vào Zustand)
  const [userToken, setUserToken] = useState<string | null>(null);

  return (
    <SafeAreaProvider>
      {/* ThemeProvider giữ nguyên từ Sprint 3 (Chương 3) — lồng bên trong SafeAreaProvider,
          bên ngoài NavigationContainer, để mọi màn hình (Auth lẫn Main) đều dùng được useTheme() */}
      <ThemeProvider>
        {/* Bọc toàn bộ app bằng NavigationContainer, gắn thêm prop linking */}
        <NavigationContainer linking={linking}>
          {userToken == null ? (
            // LUỒNG 1: CHƯA ĐĂNG NHẬP — AuthStack: Login + Register (không Back lén vào Tab)
            <AuthStack.Navigator screenOptions={{ headerShown: false }}>
              <AuthStack.Screen name="Login">
                {({ navigation }) => (
                  <LoginScreen
                    onLogin={(token) => setUserToken(token)}
                    onGoRegister={() => navigation.navigate("Register")}
                  />
                )}
              </AuthStack.Screen>
              <AuthStack.Screen name="Register">
                {({ navigation }) => (
                  <RegisterScreen
                    onRegistered={(token) => setUserToken(token)}
                    onGoLogin={() => navigation.navigate("Login")}
                  />
                )}
              </AuthStack.Screen>
            </AuthStack.Navigator>
          ) : (
            // LUỒNG 2: ĐÃ ĐĂNG NHẬP — cấp thẳng Bottom Tab Navigator (Home + Cart)
            // cartBadgeCount={2}: giá trị DEMO tĩnh để thấy tabBarBadge chạy đúng (xem Bước 5 + Phần 5.1).
            // Chương 6 sẽ xoá dòng này, MainTabNavigator tự đọc số lượng thật từ useCartStore.
            <MainTabNavigator
              onLogout={() => setUserToken(null)}
              cartBadgeCount={2}
            />
          )}
        </NavigationContainer>
      </ThemeProvider>
    </SafeAreaProvider>
  );
}

export default App;
```

> [!NOTE]
> Vì `userToken == null` quyết định render `AuthStack.Navigator` hay `MainTabNavigator`, React sẽ **hủy hoàn toàn (Unmount)** cây Navigator cũ khi giá trị đổi. Màn hình Login/Register biến mất khỏi bộ nhớ ngay khi đăng nhập/đăng ký thành công — không hề còn sót lại trong Stack để bấm Back quay lại được.

#### Bước 7b: Cấu hình Native cho Deep Linking (bắt buộc để `linking` ở Bước 7 hoạt động thật)

Prop `linking` vừa khai báo ở Bước 7 mới chỉ là "luật chơi phía JavaScript". Theo đúng lý thuyết Phần 5.4 mục 1-2, phải khai báo thêm ở tầng Native thì hệ điều hành mới biết gọi App ShopAI dậy khi có ai bấm vào link `shopai://...`.

1. Mở `ios/ShopAI/Info.plist`, thêm khối `CFBundleURLTypes` (xem đầy đủ ở Phần 5.4 mục 1).
2. Mở `android/app/src/main/AndroidManifest.xml`, thêm `<intent-filter>` Deep Link vào bên trong `<activity android:name=".MainActivity">` (xem đầy đủ ở Phần 5.4 mục 2) — nhớ **giữ nguyên** `<intent-filter>` mặc định `MAIN`/`LAUNCHER` đã có sẵn.
3. Build lại App hoàn toàn (bắt buộc vì đây là thay đổi Native):

```bash
npm run ios
npm run android
```

4. Test thử với `uri-scheme` (xem Phần 5.4 mục 3):

```bash
npx uri-scheme open "shopai://product/prod_1" --ios
npx uri-scheme open "shopai://product/prod_1" --android
```

Nếu đúng, App tự mở lên và nhảy thẳng vào `ProductDetailScreen` với `productId: 'prod_1'`.

#### Bước 8: Build lại App và Tận hưởng

Vì bạn vừa cài thêm thư viện liên quan đến Native (iOS/Android), **TÍNH NĂNG HOT RELOAD SẼ KHÔNG CÓ TÁC DỤNG**. Bắt buộc phải Build lại mã C/Java!

- Chạy: `npm run ios` (hoặc android).
- App lên: Bạn đang ở màn hình Đăng nhập. Bấm **Đăng ký** → điền form → vào Tab; hoặc Đăng nhập Email + Mật khẩu hợp lệ → Bottom Tab -> Bấm vào 1 sản phẩm ở Home mở ra Chi tiết -> Bấm Back quay về Home -> Bấm Tab "Giỏ hàng" thấy Placeholder -> Bấm Thoát ở Home văng ra ngoài.

#### Bước 9 (TÙY CHỌN — áp dụng lý thuyết Phần 5.5): Thử nghiệm Drawer Navigator

**ShopAI bản chính thức tiếp tục dùng Bottom Tab làm điều hướng chính** — đây là bài tập để luyện Drawer, không bắt buộc đổi kiến trúc production. Không đụng đến `MainTabNavigator`/`HomeStackNavigator` đã dựng ở Bước 4-5.

1. Tạo `src/screens/ProfileScreen.tsx` (placeholder, giống cấu trúc `CartScreen` ở Bước 5):

```tsx
import React from "react";
import { View, Text, StyleSheet } from "react-native";
import { SafeAreaView } from "react-native-safe-area-context";
import { COLORS, SIZES } from "@constants/theme";

// Placeholder: Logic Hồ sơ thật (đổi ảnh, đổi tên...) sẽ làm khi cần
const ProfileScreen = () => {
  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.container}>
        <Text style={styles.emoji}>👤</Text>
        <Text style={styles.title}>Hồ sơ của tôi</Text>
        <Text style={styles.subtitle}>Bài tập Drawer Navigator — Phần 5.5</Text>
      </View>
    </SafeAreaView>
  );
};

const styles = StyleSheet.create({
  safeArea: { flex: 1, backgroundColor: COLORS.background },
  container: { flex: 1, justifyContent: "center", alignItems: "center" },
  emoji: { fontSize: 48, marginBottom: 12 },
  title: { fontSize: SIZES.h2, fontWeight: "bold", color: COLORS.text },
  subtitle: { fontSize: SIZES.body2, color: COLORS.textLight, marginTop: 4 },
});

export default ProfileScreen;
```

2. Tạo `src/navigation/RootDrawerNavigator.tsx` theo đúng mẫu ở Phần 5.5 mục 3 (bọc `MainTabNavigator` + thêm `Profile`).
3. Cài `@react-navigation/drawer` + `react-native-gesture-handler` (xem Phần 5.5 mục 2), nhớ thêm `import 'react-native-gesture-handler';` ở đầu `index.js`.
4. Trong `App.tsx`, **chỉ để thử nghiệm**, tạm đổi nhánh "đã đăng nhập" từ `<MainTabNavigator ... />` sang `<RootDrawerNavigator onLogout={...} />` để xem Drawer vuốt ra từ cạnh trái, chứa "ShopAI" (Tab bên trong) và "Hồ sơ của tôi".
5. Xem xong, đổi lại về `<MainTabNavigator ... />` nếu muốn tiếp tục theo đúng lộ trình Sprint chính (Chương 6 sẽ tiếp tục build trên nền `MainTabNavigator`, không phải Drawer).

> [!TIP]
> Vì Drawer/Tab/Stack đều nhận `onLogout`/`onLogin` qua Props giống nhau, việc "cắm" `RootDrawerNavigator` hay `MainTabNavigator` vào `App.tsx` chỉ là đổi 1 dòng — minh chứng sống cho tư duy Custom Navigation: các tầng Navigator độc lập, lắp ráp linh hoạt như Lego.

Lưu code bằng Git:

```bash
git add .
git commit -m "Sprint 5: Auth Flow, Bottom Tab Navigator, ProductDetail via Route Params, Deep Linking"
```

---

### ✅ Checklist nghiệm thu Sprint 5 (tick trước khi sang Chương 6)

- [ ] Chưa login → chỉ thấy AuthStack (Login **và** Register); login/đăng ký xong → MainTabs
- [ ] `RegisterScreen`: validate họ tên / email / mật khẩu / xác nhận khớp; liên kết qua lại với Login
- [ ] Bottom Tab có **icon**; Tab Giỏ có badge (demo hoặc số)
- [ ] Bấm sản phẩm → Detail đúng `productId` (không truyền cả object)
- [ ] **Không mất** pull-to-refresh / FlashList từ Chương 4 khi sửa Home
- [ ] Deep Link: đã khai báo native (plist + intent-filter) + `linking` JS; test được 1 URL
- [ ] `git commit` Sprint 5

## 🎯 CHUẨN BỊ CHO CHƯƠNG 6

Để ý ở Bước 5, ta phải truyền hàm `onLogout` xuyên qua 3 tầng: `MainTabNavigator` -> `HomeStackNavigator` -> `HomeScreen`. Giờ tưởng tượng nút Thanh toán nằm ở `CartScreen`, sâu thêm vài lớp Component con nữa thì phải truyền Props xuyên qua bao nhiêu tầng? (Đó gọi là **Prop Drilling** — Khoan giếng Props).
Chương 6 sẽ giải quyết triệt để nỗi đau này bằng cách đưa dữ liệu lên đám mây (Global State) với **Zustand** — hoàn thiện logic Giỏ hàng thật cho `CartScreen` — và học cách Fetch dữ liệu API chuyên nghiệp bằng **TanStack Query**!
