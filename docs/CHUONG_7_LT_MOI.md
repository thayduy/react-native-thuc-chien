---
sidebar_position: 7
title: Chương 7
---

# GIÁO TRÌNH LÝ THUYẾT & THỰC CHIẾN
## CHƯƠNG 7: NATIVE MODULES, PHẦN CỨNG & QUYỀN TRUY CẬP HỆ ĐIỀU HÀNH
**Thời lượng:** 6 tiết Lý thuyết + 4 tiết Thực hành

---

> [!IMPORTANT]
> **Thực hành chương = Sprint ShopAI cuối file.** Hoàn thành Sprint này để đạt mục tiêu chương. Hoàn thành đủ 11 chương theo `SHOPAI_HOAN_THIEN.md` = sản phẩm ShopAI **hoàn thiện đẳng cấp**.

## 📚 MỤC TIÊU HỌC TẬP

Sau khi hoàn thành chương này, học viên sẽ:
- ✅ Hiểu được cơ chế giao tiếp bí mật giữa JavaScript và Native OS thông qua **JNI (Java Native Interface)** và **Objective-C Runtime**.
- ✅ Am hiểu chính sách Sandboxing của Apple và Google, cách thao tác với **Hệ thống xin Quyền (Permissions)** ở tầng Hệ điều hành (Cấu hình Info.plist và AndroidManifest.xml).
- ✅ Nắm bắt sự bùng nổ của Hệ sinh thái **Expo Modules** và cách tích hợp chúng vào React Native CLI để tận dụng module xịn xò.
- ✅ Phân biệt **Autolinking (RN 0.60+)** với **Manual Linking** thời cổ đại, hiểu Pod/Gradle làm gì sau lưng bạn và xử lý khi Autolinking thất bại.
- ✅ Xử lý đúng chuẩn UX tình huống **người dùng từ chối quyền vĩnh viễn (Blocked)** bằng `Linking.openSettings()`.
- ✅ Biết dùng **Haptic Feedback (rung phản hồi)** đúng liều lượng để tăng cảm giác "app xịn".
- ✅ Làm chủ **Định vị GPS (Location)**: xin quyền, lấy toạ độ, và ứng dụng vào bài toán ước tính phí giao hàng của ShopAI.
- ✅ Hiểu sâu **Frame Processor & pipeline JSI của Camera** (Worklets, 60FPS, vì sao không đi qua Bridge).
- ✅ Tự **gỡ rối (Troubleshoot) lỗi build Native** kinh điển: duplicate class, pod install fail, sai JDK, cache bẩn.
- ✅ Nắm được nguyên lý **Push Notification** (FCM/APNs) và 3 trạng thái App (Foreground/Background/Killed) xử lý thông báo khác nhau ra sao.
- ✅ Nhìn thấy tận mắt **bộ khung của một Native Module tự viết** (Kotlin + Swift + JS) và phân biệt được với Turbo Module thế hệ mới.
- ✅ **Thực chiến:** Cấu hình thư viện Native Camera, xin quyền bảo mật, quét mã vạch (Barcode Scanner), rung phản hồi khi quét trúng, và hiển thị **ước tính phí ship theo vị trí GPS** trực tiếp trên điện thoại thật.

---

### 0. Nhìn tổng thể trước khi đọc sâu

Trước khi đi vào từng phần lý thuyết, hãy dừng lại 2 phút để thấy bức tranh toàn cảnh: chương này đưa ShopAI ra khỏi "thế giới ảo" của JavaScript để chạm vào phần cứng thật của điện thoại.

**Sơ đồ tổng quan — Chương 7 xây gì cho ShopAI:**

```
┌────────────┐   bấm "Quét Mã"    ┌────────────────────┐   quét trúng mã    ┌─────────────┐
│ HomeScreen │ ─────────────────▶ │  ScannerScreen       │ ─────────────────▶ │  Home nhận  │
│            │  xin quyền Camera  │  (Vision Camera JSI  │   + rung Haptic     │  scannedCode│
└────────────┘                    │   + khóa chống lặp)  │                     └─────────────┘
                                   └────────────────────┘

┌───────────────────────┐   xin quyền GPS   ┌────────────────────┐
│ useCurrentLocation      │ ────────────────▶ │  LocationBadge       │
│ (@react-native-         │                    │  (khoảng cách +      │
│  community/geolocation) │                    │   phí ship ước tính) │
└───────────────────────┘                    └────────────────────┘
```

**Sau chương này, bạn sẽ làm được gì:**
- Xin và xử lý đúng chuẩn UX ba loại quyền hệ điều hành: Camera, Location, Vibrate — kể cả khi user từ chối vĩnh viễn.
- Cài đặt và cấu hình một Native Module thật (Vision Camera) mà không bị sập vì Autolinking.
- Dựng một màn hình quét mã vạch chuyên nghiệp: có khóa chống quét lặp, tự tắt Camera khi rời màn hình.
- Phát rung phản hồi (Haptic) đúng thời điểm, đúng liều lượng, không làm phiền người dùng.
- Lấy tọa độ GPS, tính khoảng cách bằng công thức Haversine, và ước tính phí giao hàng có phương án dự phòng.

**Lộ trình đọc chương này (đừng đọc nhảy cóc):**
1. Đọc 7.1 – 7.2 để hiểu Native Module là gì và tại sao OS luôn khóa phần cứng theo mặc định.
2. Đọc 7.3 – 7.4 để hiểu Expo Modules và cơ chế Autolinking đang "nối dây" hộ bạn ra sao.
3. Đọc kỹ 7.5 — đây là phần hay bị bỏ qua nhất nhưng gây lỗi UX nhiều nhất (quyền bị chặn vĩnh viễn).
4. Đọc 7.6 – 7.7 (Haptic, Location) — kiến thức áp dụng trực tiếp vào Sprint.
5. Đọc lướt 7.8 (JSI Frame Processor) nếu mới học lần đầu — đây là kiến thức nâng cao, quay lại sau khi làm xong Sprint cũng không muộn.
6. Giữ 7.9 – 7.10 làm "sổ tay tra cứu" trong lúc code, không cần học thuộc.
7. Bắt tay vào Sprint 7 (Bước 1 → 12), quay lại đúng phần lý thuyết tương ứng khi bí.
8. Đọc 7.11 – 7.12 sau cùng (hoặc khi có thời gian rảnh) — đây là kiến thức mở rộng, gắn với Bước 13 tuỳ chọn của Sprint.

> [!TIP]
> **Nhầm lẫn phổ biến nhất chương này:** học viên hay lẫn lộn giữa trạng thái quyền `denied` (từ chối, còn xin lại được) và `blocked`/`restricted` (từ chối vĩnh viễn, phải mở Cài đặt hệ thống). Ghi nhớ: trên iOS chỉ được hỏi **đúng một lần**, trên Android được hỏi **hai lần** — sai chỗ này là cả màn hình xin quyền bị treo vô thời hạn mà không hiểu vì sao (xem lại Phần 7.5).

---

## 🛠️ PHẦN 7.1: BẢN CHẤT CỦA NATIVE MODULES

Code JavaScript/TypeScript mà bạn viết từ đầu khóa học đến giờ **KHÔNG THỂ** tự bật đèn Flash, không thể tự mở Camera, không thể tự rung điện thoại (Haptic feedback). Trình duyệt JS Engine (Hermes) bị giam lỏng trong một hộp cát (Sandbox) hoàn toàn mù lòa với phần cứng vật lý.

**Để điều khiển phần cứng, bạn cần Native Modules:**
Đây là những khối mã nguồn viết bằng C++, Java, Kotlin, Swift hoặc Objective-C, được gắn trực tiếp vào App của bạn. Nó đóng vai trò như một tên lính liên lạc:
1. JS Thread hét lên qua JSI: *"Này, bật cái Camera lên!"*
2. Lệnh truyền đến C++, C++ gọi JNI (Java Native Interface) trên Android.
3. Mã Java nhận lệnh và gọi API cấp thấp của Google Android để kích hoạt mắt kính Camera vật lý.

Chính vì phải chạy biên dịch C/Java, nên mỗi khi bạn cài một Native Module (`npm install react-native-camera`), tính năng **Hot Reload sẽ vô hiệu lực**. Bạn BẮT BUỘC phải tắt Terminal Metro và chạy lại lệnh biên dịch thô: `npm run ios` hoặc `npm run android`.

---

## 🛡️ PHẦN 7.2: SANDBOXING VÀ QUYỀN HỆ ĐIỀU HÀNH (PERMISSIONS)

Nếu một cái App đèn pin tải từ trên mạng về tự động đọc danh bạ và chụp lén người dùng, đó là thảm họa bảo mật.
Cả Apple và Google đều áp dụng nguyên tắc **Zero Trust (Không tin ai cả)**. Khi cài app, OS sẽ khóa mọi phần cứng.
App muốn dùng phải **Khai báo ý định** bằng văn bản (File cấu hình) và xin quyền khi chạy (Runtime Request).

### 1. Khai báo trên iOS (`Info.plist`)
Mọi quyền trên iOS phải đi kèm dòng chữ giải thích tại sao bạn lại cần quyền đó. Trình duyệt App Store Review sẽ từ chối app nếu dòng giải thích quá chung chung.
Mở file `ios/ShopAI/Info.plist`, phải thêm:
```xml
<key>NSCameraUsageDescription</key>
<string>ShopAI cần quyền mở Camera để quét mã vạch sản phẩm nhằm tra cứu nguồn gốc.</string>
<key>NSLocationWhenInUseUsageDescription</key>
<string>ShopAI cần vị trí của bạn để ước tính chi phí giao hàng tận nhà.</string>
```

### 2. Khai báo trên Android (`AndroidManifest.xml`)
Khác với iOS, Android cần khai báo quyền tĩnh ở file manifest trước khi cài đặt.
Mở `android/app/src/main/AndroidManifest.xml`, thêm vào ngay dưới thẻ `<manifest>`:
```xml
<uses-permission android:name="android.permission.CAMERA" />
<uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
```

### 3. Quy trình xin quyền Runtime (JS Level)
Việc khai báo văn bản chỉ là bước 1. Lúc chạy app (Runtime), bạn phải tung ra bảng Pop-up yêu cầu người dùng bấm nút "Cho phép" (Allow). Nếu người dùng bấm "Từ chối" (Deny), hàm Native sẽ quăng lỗi, app sẽ Crash nếu bạn không xử lý bằng hàm `try-catch`.

---

## 🌟 PHẦN 7.3: KỶ NGUYÊN MỚI - EXPO MODULES TRONG REACT NATIVE CLI

Ngày xưa, việc cài Native Modules trong RN CLI là một cơn ác mộng. Bạn phải đụng tay vào sửa code Java, Gradle, Swift rất nhiều.

Gần đây, **Expo** (Một công ty khởi nghiệp xây dựng Framework xoay quanh React Native) đã tạo ra một chuẩn mới gọi là **Expo Modules Architecture (Viết module bằng Swift/Kotlin rất hiện đại)**.
Facebook (Meta) và cộng đồng đã công nhận chất lượng của Expo. Giờ đây, thay vì dùng các thư viện rác từ Github, chúng ta hoàn toàn có thể cài lõi Expo vào RN CLI, để sử dụng kho vũ khí Native Modules hoàn hảo của họ (Expo Camera, Expo Location, Expo FileSystem) với sự ổn định tuyệt đối.

> [!NOTE]
> **Xu hướng công nghiệp 2025+: Quét mã bằng Model AI chạy ngay trên máy (On-device ML Kit).** Việc kết hợp Camera với một Model nhận diện mã vạch chạy **offline, ngay trên chip điện thoại** (Google ML Kit trên Android, Vision Framework trên iOS) — thay vì gửi từng khung ảnh lên Server để nhận diện — đã trở thành chuẩn công nghiệp cho bài toán Scan. Bạn không cần học thêm gì mới: `react-native-vision-camera` + `useCodeScanner` mà Sprint 7 dạy dưới đây **chính là** cách hiện thực hoá xu hướng này — xử lý từng Frame ngay trên luồng Native bằng JSI, không qua Bridge JSON, không cần mạng, và ảnh không hề rời khỏi máy (riêng tư tuyệt đối).

---

## 🔗 PHẦN 7.4: AUTOLINKING VS MANUAL LINKING — AI ĐANG NỐI DÂY CHO BẠN?

Đây là câu hỏi mà 90% học viên bỏ qua, để rồi khi build đỏ lòm màn hình thì không biết bắt đầu sửa từ đâu. Hãy cùng bóc tách.

### 1. Thời kỳ đồ đá: `react-native link` (trước RN 0.60)

Ngày xưa, mỗi lần cài một thư viện Native, bạn phải **tự tay** làm 4 việc kinh khủng sau:

| Nền tảng | Việc phải làm thủ công |
|----------|------------------------|
| iOS | Mở Xcode, kéo thả file `.xcodeproj` của thư viện vào project, thêm `libRNCamera.a` vào mục **Linked Frameworks and Libraries**, sửa **Header Search Paths** |
| Android | Sửa `settings.gradle` để `include ':react-native-camera'`, sửa `app/build.gradle` thêm `implementation project(':react-native-camera')`, sửa `MainApplication.java` thêm `new RNCameraPackage()` vào danh sách `getPackages()` |

Chỉ cần quên **một** bước, app sẽ crash với lỗi kinh điển `null is not an object (evaluating 'RNCamera.Constants')`. Đây chính là lý do React Native từng bị mang tiếng "khó cài thư viện".

### 2. Thời kỳ hiện đại: Autolinking (RN 0.60+)

Từ RN 0.60, cộng đồng tạo ra **Autolinking** — cơ chế tự động dò tìm và nối dây. Nguyên lý cực kỳ đơn giản mà thông minh:

1. Bạn chạy `npm install react-native-vision-camera` → package rơi vào `node_modules/`.
2. Trong package đó có một file khai báo `react-native.config.js` (hoặc field `codegenConfig`/`dependency` trong `package.json`) — nó tự "giới thiệu bản thân": *"Tôi là một Native Module, mã Android của tôi ở thư mục `android/`, mã iOS của tôi ở podspec `VisionCamera.podspec`"*.
3. **Trên iOS:** khi bạn chạy `pod install`, file `ios/Podfile` có dòng `use_native_modules!`. Dòng này chạy một script Node quét toàn bộ `node_modules`, gom hết các podspec tìm được, rồi tự thêm chúng vào Pods project. Kết quả ghi vào `ios/Podfile.lock`.
4. **Trên Android:** file `android/settings.gradle` có dòng gọi `applyNativeModulesSettingsGradle`, và `android/app/build.gradle` có `applyNativeModulesAppBuildGradle`. Chúng làm y hệt: quét `node_modules`, tự `include` project, tự thêm `implementation`, tự sinh ra file `PackageList.java` chứa danh sách package để nạp lúc khởi động.

> [!NOTE]
> **Vậy nên nhớ công thức vàng:** trên **iOS**, cài thư viện Native = `npm install` **+ `pod install`**. Trên **Android**, cài thư viện Native = `npm install` **+ build lại** (`npm run android`) là đủ, Gradle tự lo. Lệnh `react-native link` đã bị **khai tử**, đừng bao giờ gõ nó nữa.

### 3. Khi nào Autolinking thất bại và phải Manual Linking?

Autolinking không phải phép màu vạn năng. Bạn sẽ phải nhúng tay vào khi:

- **Thư viện quá cũ** (viết trước 2019, không có podspec/config chuẩn) → phải làm thủ công theo README của nó.
- **Thư viện cần cấu hình thêm ngoài việc nối dây**, ví dụ Vision Camera cần bạn tự thêm `VisionCamera_enableCodeScanner=true` vào `gradle.properties` (Bước 1 của Sprint dưới đây). Autolinking chỉ nối dây, nó **không đoán được** bạn muốn bật tính năng nào.
- **Bạn muốn cố tình TẮT autolink** cho một thư viện (hiếm, thường do xung đột). Lúc đó tạo file `react-native.config.js` ở gốc dự án:

```js
module.exports = {
  dependencies: {
    'react-native-thu-vien-gay-loi': {
      platforms: {
        android: null, // Bỏ qua, không autolink trên Android
        ios: null,     // Bỏ qua, không autolink trên iOS
      },
    },
  },
};
```

### 4. Cách kiểm tra Autolinking có chạy không

```bash
# Liệt kê toàn bộ Native Module mà RN CLI đang nhìn thấy
npx react-native config
```
Lệnh này in ra một cục JSON. Hãy tìm tên thư viện của bạn trong mục `dependencies`. Nếu **không thấy** tên nó ở đó → Autolinking đã bỏ sót, và bạn biết chính xác đó là gốc rễ của lỗi crash.

---

## 🚫 PHẦN 7.5: KHI NGƯỜI DÙNG TỪ CHỐI QUYỀN VĨNH VIỄN

Ở Phần 7.2 ta mới xử lý trường hợp đẹp đẽ: user bấm "Cho phép". Nhưng đời không như mơ.

### 1. Ba trạng thái (thực ra là bốn) của một quyền

| Trạng thái | Ý nghĩa | Xin lại được không? |
|------------|---------|---------------------|
| `granted` | Đã cho phép | Không cần xin nữa |
| `not-determined` / `undetermined` | Chưa hỏi lần nào | Có — Pop-up sẽ hiện |
| `denied` | Vừa từ chối | Tuỳ OS (xem dưới) |
| `blocked` / `restricted` | Từ chối vĩnh viễn, hoặc bị chặn bởi Phụ huynh/Doanh nghiệp | **KHÔNG.** Gọi request bao nhiêu lần cũng trả về `blocked` ngay lập tức, Pop-up không bao giờ hiện lại |

**Sự khác biệt oái oăm giữa hai hệ điều hành:**
- **iOS:** người dùng chỉ được hỏi **ĐÚNG MỘT LẦN** trong suốt vòng đời cài đặt của App. Bấm "Don't Allow" một lần là xong đời — muốn xin lại phải vào Cài đặt hệ thống, hoặc gỡ app cài lại.
- **Android:** được hỏi 2 lần. Từ chối lần đầu → `denied`, vẫn hỏi lại được. Từ chối lần hai (hoặc tick "Don't ask again") → hệ thống chuyển sang trạng thái *"never ask again"*, tương đương `blocked`.

### 2. Cái bẫy UX chết người

Rất nhiều app sinh viên viết như thế này:

```tsx
// ❌ SAI: user bị kẹt vĩnh viễn trong màn hình trắng, không có lối thoát
if (!hasPermission) return <Text>Đang đợi cấp quyền...</Text>;
```

Nếu user lỡ tay bấm Deny, họ sẽ nhìn thấy dòng chữ "Đang đợi cấp quyền..." **mãi mãi**, không hiểu chuyện gì xảy ra, và cho app của bạn 1 sao trên Store. Đây là lỗi bị App Store Review đánh trượt rất thường xuyên.

### 3. Giải pháp: `Linking.openSettings()`

React Native có sẵn module `Linking` — cây cầu để mở các ứng dụng khác từ app của bạn. Hàm `Linking.openSettings()` sẽ mở **thẳng trang cài đặt của chính app bạn** trong Settings hệ thống, nơi user có thể gạt công tắc bật lại quyền.

```tsx
import { Alert, Linking } from 'react-native';

const showBlockedAlert = () => {
  Alert.alert(
    'Cần quyền Camera',                                     // Tiêu đề
    'Bạn đã từ chối quyền Camera. Hãy vào Cài đặt > ShopAI > bật Camera để quét mã vạch nhé.', // Nội dung giải thích LÝ DO
    [
      { text: 'Để sau', style: 'cancel' },                  // Luôn cho user một lối thoát
      { text: 'Mở Cài đặt', onPress: () => Linking.openSettings() }, // Nút hành động
    ],
  );
};
```

> [!TIP]
> **Nguyên tắc vàng khi xin quyền (Just-in-time permission):** ĐỪNG xin hết mọi quyền ngay màn hình đầu tiên lúc mở app. Hãy xin **đúng lúc user cần tính năng đó**. User bấm nút "Quét mã" → lúc đó mới xin Camera. User bấm "Tính phí ship" → lúc đó mới xin Location. Tỉ lệ được bấm "Allow" tăng vọt vì user hiểu rõ họ đang đánh đổi quyền riêng tư để lấy cái gì.

> [!CAUTION]
> **Một chi tiết cực dễ quên:** khi user rời app sang Settings bật quyền rồi quay lại, React state của bạn **vẫn đang giữ giá trị cũ** (`hasPermission = false`). App vẫn hiện màn hình lỗi dù quyền đã được bật! Cách xử lý chuẩn là lắng nghe sự kiện app quay lại foreground bằng `AppState`, rồi kiểm tra quyền lại một lần nữa:
> ```tsx
> import { AppState } from 'react-native';
>
> useEffect(() => {
>   const sub = AppState.addEventListener('change', (nextState) => {
>     if (nextState === 'active') checkPermission(); // App vừa quay lại -> dò quyền lại
>   });
>   return () => sub.remove(); // Nhớ dọn listener, tránh rò rỉ bộ nhớ
> }, []);
> ```

---

## 📳 PHẦN 7.6: HAPTIC FEEDBACK — NGÔN NGỮ CỦA XÚC GIÁC

Bạn có để ý khi bấm nút thanh toán trên app ngân hàng, điện thoại rung một cái "tách" rất nhẹ và gọn không? Đó là **Haptic Feedback** — phản hồi xúc giác. Nó không phải là "rung chuông báo thức", mà là một cú chạm tinh tế lên da tay, xác nhận rằng *"hệ thống đã nhận lệnh của bạn"*.

### 1. Vibration vs Haptic — hai thứ khác nhau

| Tiêu chí | Vibration (Rung thô) | Haptic (Rung phản hồi) |
|----------|----------------------|------------------------|
| Phần cứng | Motor lệch tâm (ERM) rung ầm ầm | Taptic Engine (iOS) / Vibrator API mới (Android) rung sắc, ngắn |
| Thời lượng | Hàng trăm ms đến vài giây | 10–40ms, gần như tức thời |
| Dùng khi | Cuộc gọi đến, báo thức, thông báo nền | Bấm nút, quét thành công, kéo qua ngưỡng, chọn item trong picker |
| API RN có sẵn | ✅ `Vibration` (built-in, 0 cài đặt) | ❌ Cần thư viện Native |

### 2. Ba lựa chọn cho ShopAI

**A. `Vibration` API — có sẵn trong React Native, không cần cài gì:**
```tsx
import { Vibration } from 'react-native';

Vibration.vibrate(40);            // Rung 40ms — vừa đủ nhẹ, giả lập cảm giác haptic
Vibration.vibrate([0, 40, 60, 40]); // Mẫu rung: đợi 0ms, rung 40, nghỉ 60, rung 40
Vibration.cancel();                 // Dừng rung
```
> Lưu ý: trên iOS, `Vibration.vibrate(số)` **bỏ qua tham số thời lượng** (iOS không cho tuỳ chỉnh độ dài rung của motor cơ bản) — nó luôn rung một nhịp chuẩn ~400ms. Đây là hạn chế của nền tảng, không phải lỗi code của bạn.

**B. `expo-haptics` — chuẩn đẹp nhất, cần hạ tầng Expo Modules (Chương 8 sẽ cài):**
```tsx
import * as Haptics from 'expo-haptics';

Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Light);   // Chạm nhẹ (bấm nút nhỏ)
Haptics.impactAsync(Haptics.ImpactFeedbackStyle.Medium);  // Chạm vừa (bấm nút chính)
Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success); // Rung "thành công" 2 nhịp
Haptics.notificationAsync(Haptics.NotificationFeedbackType.Error);   // Rung "lỗi" 3 nhịp
Haptics.selectionAsync();                                  // Rung "tích tắc" khi lướt picker
```

**C. `react-native-haptic-feedback` — thư viện cộng đồng, chạy trên Bare RN CLI:**
```bash
npm install react-native-haptic-feedback
cd ios && pod install && cd ..
```
```tsx
import ReactNativeHapticFeedback from 'react-native-haptic-feedback';
ReactNativeHapticFeedback.trigger('notificationSuccess');
```

> [!NOTE]
> **Sprint 7 sẽ dùng phương án A (`Vibration` API built-in).** Lý do sư phạm: ở Chương 7 dự án ShopAI **chưa cài hạ tầng Expo Modules** (việc đó thuộc Chương 8, Bước 1), nên dùng API có sẵn là an toàn nhất, không phát sinh thêm một vòng build Native. Sau khi học xong Chương 8, bạn hoàn toàn có thể quay lại thay `Vibration.vibrate(40)` bằng `Haptics.notificationAsync(Success)` để nâng cấp trải nghiệm — chỉ sửa đúng 1 dòng trong file `src/utils/haptics.ts` mà ta sắp viết.

### 3. Quy tắc dùng Haptic đừng để thành tra tấn

- ✅ **Nên rung:** quét mã thành công, thêm vào giỏ hàng, thanh toán xong, kéo-để-làm-mới (pull to refresh) vượt ngưỡng, xoá item.
- ❌ **Đừng rung:** mỗi ký tự user gõ, mỗi lần cuộn danh sách, mỗi lần màn hình render. Rung quá nhiều = tốn pin + user tắt luôn haptic trong Settings + cảm giác app rẻ tiền.
- 🔋 **Nhớ:** rung tốn pin thật sự, và trên máy Android giá rẻ motor rung khá ồn. Luôn giữ tần suất thấp.
- ♿ **Trợ năng:** một số người dùng tắt hẳn haptic trong Settings hệ thống. **Không bao giờ** dùng rung làm kênh thông tin **duy nhất** — luôn phải có phản hồi thị giác (đổi màu, hiện chữ) đi kèm.

### 4. Android cần khai báo quyền rung

Đây là quyền "install-time" — chỉ cần khai báo, **không** cần Pop-up xin phép lúc chạy:
```xml
<uses-permission android:name="android.permission.VIBRATE" />
```

---

## 📍 PHẦN 7.7: ĐỊNH VỊ (LOCATION) — GPS VÀ BÀI TOÁN PHÍ SHIP

### 1. Vì sao ShopAI cần GPS?

Hãy nghĩ như một Product Owner, không phải như một coder. Một app thương mại điện tử cần vị trí để:
- **Ước tính phí giao hàng** theo khoảng cách từ kho tới nhà khách (đây là thứ ta sẽ làm ở Sprint 7).
- **Ước tính thời gian giao** ("giao trong 2 giờ nếu bạn ở nội thành").
- **Tự động điền địa chỉ** khi Checkout, đỡ cho user gõ tay.
- **Tìm cửa hàng gần nhất** để nhận hàng tại quầy.

Ở Phần 7.2 ta **đã khai báo sẵn** `NSLocationWhenInUseUsageDescription` (iOS) và `ACCESS_FINE_LOCATION` (Android) rồi — giờ là lúc dùng đến chúng.

### 2. Hai loại độ chính xác

| Quyền Android | Độ chính xác | Nguồn dữ liệu | Tốn pin |
|---------------|--------------|---------------|---------|
| `ACCESS_COARSE_LOCATION` | ~1–3 km | Trạm phát sóng di động, Wi-Fi | Rất ít |
| `ACCESS_FINE_LOCATION` | ~5–20 m | Vệ tinh GPS + GNSS | Nhiều |

Từ **Android 12 (API 31)** trở đi, khi bạn xin `ACCESS_FINE_LOCATION`, Pop-up hệ thống sẽ cho user chọn giữa **"Chính xác" (Precise)** và **"Gần đúng" (Approximate)**. User hoàn toàn có quyền chỉ cho bạn vị trí gần đúng — code của bạn phải chấp nhận điều đó mà không được crash.

Trên iOS còn phân biệt:
- **When In Use** — chỉ định vị khi app đang mở trên màn hình. ShopAI chỉ cần mức này.
- **Always** — định vị cả khi app chạy nền. Xin quyền này sẽ bị Apple soi rất kỹ lúc review, đừng xin nếu không thật sự cần (app giao hàng cho tài xế mới cần).

### 3. Chọn thư viện nào?

| Thư viện | Ưu điểm | Nhược điểm |
|----------|---------|------------|
| `@react-native-community/geolocation` | Không cần hạ tầng Expo, API giống hệt `navigator.geolocation` của trình duyệt Web, rất nhẹ | API kiểu callback cũ, phải tự bọc Promise |
| `expo-location` | API `async/await` hiện đại, có sẵn **Reverse Geocoding** (đổi toạ độ → tên đường/thành phố), có Geofencing | Cần cài hạ tầng Expo Modules trước |
| `react-native-geolocation-service` | Chính xác cao, kiểm soát tốt trên Android | Bảo trì chậm hơn, trùng chức năng với hai cái trên |

> [!NOTE]
> **Sprint 7 dùng `@react-native-community/geolocation`.** Lý do y hệt phần Haptic: Chương 7 chưa cài Expo Modules (Chương 8 mới cài), nên ta chọn con đường không gây xung đột hạ tầng. Học viên nào muốn đi trước có thể chạy `npx install-expo-modules@latest` (lệnh của Chương 8, Bước 1) rồi dùng `expo-location` — nhưng **hãy làm xong Sprint 7 theo đúng hướng dẫn trước đã**, đừng trộn hai con đường vào một lần build.

### 4. Bản xem trước API `expo-location` (dùng ở Chương 8+ hoặc dự án riêng)

Ghi lại để bạn nhận diện khi đọc tài liệu ngoài đời:
```ts
import * as Location from 'expo-location';

// 1. Xin quyền (kiểu async/await hiện đại)
const { status } = await Location.requestForegroundPermissionsAsync();
if (status !== 'granted') return;

// 2. Lấy toạ độ hiện tại
const pos = await Location.getCurrentPositionAsync({
  accuracy: Location.Accuracy.Balanced, // Cân bằng giữa độ chính xác và pin
});
console.log(pos.coords.latitude, pos.coords.longitude);

// 3. Đổi toạ độ ra địa chỉ chữ (Reverse Geocoding) — thứ community geolocation KHÔNG có
const [place] = await Location.reverseGeocodeAsync(pos.coords);
console.log(place.city, place.district, place.street);

// 4. Theo dõi vị trí liên tục (dùng cho app giao hàng)
const sub = await Location.watchPositionAsync({ distanceInterval: 50 }, (p) => console.log(p));
sub.remove(); // Nhớ dừng lại, nếu không pin tụt thấy rõ
```

### 5. Ba cái bẫy khi làm Location

1. **Emulator/Simulator không có GPS thật.** Bạn phải tự "bơm" toạ độ giả: trên Xcode Simulator vào menu `Features > Location > Custom Location`; trên Android Emulator bấm nút `...` (Extended Controls) `> Location > gõ toạ độ > Send`. Không làm bước này thì hàm `getCurrentPosition` sẽ treo và cuối cùng báo timeout — nhiều bạn tưởng code sai, thật ra code đúng.
2. **Luôn phải có `timeout`.** Trong nhà, trong hầm để xe, tín hiệu vệ tinh rất yếu, GPS có thể mất 30–60 giây hoặc không bao giờ trả về. Không đặt timeout = app đứng hình vô thời hạn.
3. **Luôn phải có phương án dự phòng.** User từ chối quyền, hoặc GPS chết → app vẫn phải chạy được, chỉ là hiện "Không xác định được vị trí, phí ship mặc định 30.000đ". **Không bao giờ** để một tính năng phụ làm sập cả màn hình chính.

---

## ⚡ PHẦN 7.8: FRAME PROCESSOR & PIPELINE JSI CỦA CAMERA

Phần này giải thích **vì sao** `react-native-vision-camera` nhanh đến vậy. Đây là kiến thức nâng cao, cực kỳ ăn điểm khi đi phỏng vấn.

### 1. Bài toán: 60 khung hình mỗi giây là bao nhiêu dữ liệu?

Một khung hình Full HD (1920×1080) ở định dạng YUV chiếm khoảng **3 MB**. Nhân với 60 khung/giây:

> 3 MB × 60 = **180 MB dữ liệu mỗi giây**.

Bây giờ hãy tưởng tượng kiến trúc React Native cũ (Bridge): mỗi khung hình phải được **serialize thành chuỗi JSON**, đẩy qua Bridge sang luồng JS, rồi deserialize lại. Chuyển 180 MB/giây qua một cây cầu JSON bất đồng bộ là chuyện **bất khả thi** — app sẽ đứng hình ngay lập tức. Đó chính xác là lý do các thư viện Camera thế hệ cũ (`react-native-camera`) chỉ chụp được ảnh tĩnh chứ không xử lý được video thời gian thực.

### 2. Lời giải: JSI — bộ nhớ dùng chung

**JSI (JavaScript Interface)** là lớp C++ cho phép JavaScript giữ **tham chiếu trực tiếp** tới một đối tượng C++ trong bộ nhớ — không copy, không serialize. Vision Camera dùng cơ chế này:

```
Cảm biến Camera (phần cứng)
   ↓ (luồng Native, ngôn ngữ Swift/Kotlin)
Frame buffer nằm trong RAM Native  ← KHÔNG hề bị copy
   ↓ (JSI HostObject — chỉ truyền một "con trỏ" nhẹ tênh)
Frame Processor (hàm JS bạn viết, chạy trên Worklet Thread)
   ↓
Kết quả gọn nhẹ (VD: chuỗi "8938505974194") mới được gửi về luồng JS chính
```

Điểm mấu chốt: **dữ liệu ảnh không bao giờ rời khỏi bộ nhớ Native**. Hàm JS của bạn chỉ cầm một cái "tay nắm" (`Frame` object) để hỏi han (`frame.width`, `frame.height`), hoặc chuyền cái tay nắm đó cho một plugin C++ khác xử lý.

### 3. Worklet — luồng JavaScript thứ hai

Nếu Frame Processor chạy trên luồng JS chính, nó sẽ giành giật CPU với việc render UI của bạn → app giật cục. Giải pháp là **Worklet** (khái niệm mượn từ `react-native-reanimated`):

```tsx
import { useFrameProcessor } from 'react-native-vision-camera';

const frameProcessor = useFrameProcessor((frame) => {
  'worklet'; // ← Chỉ thị đặc biệt! Bảo trình biên dịch: tách hàm này ra luồng riêng
  console.log(`Khung hình ${frame.width} x ${frame.height}`);
}, []);
```

Cái chỉ thị `'worklet'` ở dòng đầu tiên không phải chú thích cho vui. Plugin Babel `react-native-worklets-core` sẽ nhìn thấy nó, **cắt hàm đó ra**, biên dịch thành một đơn vị chạy được trên một **JS Runtime độc lập** (một instance Hermes thứ hai) sống trên luồng riêng của Camera. Nhờ vậy dù bạn xử lý ảnh nặng đến đâu, luồng UI chính vẫn mượt 60FPS.

Hệ quả bạn phải nhớ: bên trong hàm worklet, bạn **không** truy cập được state React bình thường, **không** gọi được `setState` trực tiếp. Muốn gửi dữ liệu về luồng JS chính, phải dùng `runOnJS` hoặc Shared Value.

### 4. Vậy `useCodeScanner` của Sprint 7 nằm ở đâu trong bức tranh này?

Câu trả lời thú vị: `useCodeScanner` là một **Frame Processor viết sẵn bằng C++ thuần**, do chính tác giả Vision Camera tối ưu. Nó chạy hoàn toàn ở tầng Native (dùng Google MLKit trên Android, Vision Framework trên iOS), **không** đi qua worklet JS, nên còn nhanh hơn nữa. Bạn chỉ nhận về kết quả cuối cùng đã gọn gàng — mảng `codes` chứa chuỗi ký tự.

> Nói cách khác: **bạn đang hưởng thành quả của kiến trúc JSI mà không phải viết một dòng C++ nào.** Đó là lý do Sprint 7 chỉ cần vài chục dòng TypeScript.

### 5. Khi nào bạn cần tự viết Frame Processor?

Khi bài toán không nằm trong danh sách có sẵn: nhận diện khuôn mặt, làm mờ nền video call, đếm số người trong khung hình, quét văn bản OCR, phát hiện vật thể bằng model TensorFlow Lite. Lúc đó bạn kết hợp Frame Processor với các plugin cộng đồng như `vision-camera-face-detector`, hoặc `react-native-fast-tflite` để chạy model AI ngay trên chip điện thoại.

> [!TIP]
> **Đừng bao giờ `console.log` trong Frame Processor ở bản Release.** 60 lần log mỗi giây sẽ làm nghẽn kênh debug và giết chết hiệu năng. Nếu cần quan sát, hãy dùng `runAtTargetFps(2, () => { ... })` của Vision Camera để chỉ chạy 2 lần/giây.

---

## 🧯 PHẦN 7.9: GỠ RỐI LỖI BUILD NATIVE (SỔ TAY CẤP CỨU)

Đây là phần bạn sẽ mở lại nhiều nhất trong cả cuốn giáo trình. Hãy đánh dấu trang này.

### 1. Bảng tra lỗi kinh điển

| Thông báo lỗi (từ khoá nhận diện) | Nguyên nhân thật sự | Cách chữa |
|---|---|---|
| `Cannot find native module 'XXX'` | Đã `npm install` nhưng chưa build lại Native, hoặc Autolinking bỏ sót | Tắt Metro → `pod install` (iOS) → `npm run ios/android` |
| `Duplicate class com.google.android.gms...` | Hai thư viện kéo về hai phiên bản khác nhau của cùng một SDK Google | Ép version trong `android/build.gradle`: `ext { playServicesVersion = "18.0.0" }`, hoặc dùng `resolutionStrategy` |
| `pod install` báo `CocoaPods could not find compatible versions` | `Podfile.lock` cũ mâu thuẫn với thư viện mới | `cd ios && rm -rf Pods Podfile.lock && pod install --repo-update` |
| `Unsupported class file major version 65` | Gradle đang chạy bằng JDK sai phiên bản (65 = JDK 21) | Cài JDK 17, trỏ `JAVA_HOME` về nó (RN 0.73–0.76 chuẩn là **JDK 17**) |
| `SDK location not found` | Thiếu file `android/local.properties` | Tạo file đó, ghi `sdk.dir=/Users/<tên-bạn>/Library/Android/sdk` |
| `Execution failed for task ':app:mergeDebugResources'` | Cache Gradle bẩn | `cd android && ./gradlew clean && cd ..` |
| `Command PhaseScriptExecution failed` (Xcode) | Script build lỗi, thường do sai đường dẫn Node | `echo "export NODE_BINARY=$(command -v node)" > ios/.xcode.env.local` |
| `error: Build input file cannot be found` | Đổi tên file nhưng Xcode còn giữ tham chiếu cũ | Xoá DerivedData (xem lệnh dưới), mở lại Xcode |
| `Metro has encountered an error: Unable to resolve module` | Cache Metro bẩn sau khi cài/đổi package | `npx react-native start --reset-cache` |
| `A problem occurred configuring project ':react-native-vision-camera'` | Thiếu cấu hình bắt buộc trong `gradle.properties` | Kiểm tra lại `VisionCamera_enableCodeScanner=true` (xem Sprint, Bước 1) |
| `The number of method references... exceeds 65536` | Vượt giới hạn DEX của Android | Bật `multiDexEnabled true` trong `android/app/build.gradle` |
| App crash trắng ngay khi mở, log `PackageList` | Autolinking sinh sai danh sách package | Xoá `android/app/build`, build lại |

### 2. Nghi thức "Dọn nhà toàn tập" (Nuclear Clean)

Khi bạn đã thử mọi cách mà vẫn lỗi, và tin chắc code JS của mình đúng — hãy chạy nghi thức sau. Nó xoá sạch mọi thứ có thể cache, buộc máy tính biên dịch lại từ số 0:

```bash
# ---- Bước 1: Dọn tầng JavaScript ----
rm -rf node_modules
npm cache clean --force
npm install

# ---- Bước 2: Dọn tầng iOS ----
cd ios
rm -rf Pods Podfile.lock build
rm -rf ~/Library/Developer/Xcode/DerivedData   # Kho cache khổng lồ của Xcode
pod install --repo-update
cd ..

# ---- Bước 3: Dọn tầng Android ----
cd android
./gradlew clean
rm -rf .gradle build app/build
cd ..

# ---- Bước 4: Dọn Metro Bundler ----
npx react-native start --reset-cache
# Mở Terminal MỚI, rồi build:
# npm run ios     (hoặc)     npm run android
```

> [!WARNING]
> Nghi thức này mất **10–20 phút** để build lại (máy phải biên dịch lại toàn bộ mã C++). Hãy pha một ly cà phê. Đừng chạy nó mỗi khi gặp lỗi nhỏ — chỉ dùng khi thật sự bế tắc.

### 3. Quy trình đọc lỗi đúng cách

Sinh viên hay copy nguyên cái log 500 dòng đỏ lòm rồi dán lên nhóm hỏi "lỗi gì vậy ạ?". Hãy làm khác đi:

1. **Cuộn lên trên, không đọc dòng cuối.** Dòng cuối thường chỉ là `Build failed` — vô nghĩa. Nguyên nhân thật nằm ở dòng đầu tiên có chữ `error:` hoặc `FAILURE:`.
2. **Xác định lỗi thuộc tầng nào:** có chữ `Gradle`/`.java`/`.kt` → tầng Android. Có `Pods`/`.m`/`.swift`/`clang` → tầng iOS. Có `Unable to resolve module` → tầng Metro/JS.
3. **Tìm tên thư viện trong log.** Nếu thấy `react-native-vision-camera` xuất hiện → mở đúng trang Troubleshooting trên GitHub của nó.
4. **Google đúng cách:** dán dòng error **cộng thêm** phiên bản RN, ví dụ `"Duplicate class" react-native 0.76 vision camera`.

### 4. Phòng bệnh hơn chữa bệnh

- **Cài từng thư viện một, build kiểm tra ngay sau mỗi lần cài.** Cài 5 thư viện rồi mới build là tự sát: khi lỗi, bạn không biết thủ phạm là ai.
- **Commit Git trước mỗi lần đụng vào Native.** Có chuyện gì thì `git checkout .` là về trạng thái sạch.
- **Đọc mục *Requirements* trong README của thư viện trước khi cài** — nhiều thư viện yêu cầu `minSdkVersion` tối thiểu (Vision Camera cần `minSdkVersion 26`).
- **Đừng nâng version React Native giữa chừng dự án học tập.** Chốt một version và đi hết khoá.

---

## 📊 PHẦN 7.10: BẢNG SO SÁNH CÁC THƯ VIỆN CAMERA

| Tiêu chí | 🥇 `react-native-vision-camera` v4 | 🥈 `expo-camera` | ⚰️ `react-native-camera` |
|---|---|---|---|
| **Tình trạng** | Đang phát triển sôi nổi, chuẩn công nghiệp | Đang phát triển, do Expo bảo trì | **ĐÃ KHAI TỬ** (deprecated 2022) |
| **Kiến trúc** | JSI + C++ thuần, hỗ trợ Fabric | Expo Modules API (Swift/Kotlin) | Bridge cũ, kiến trúc lỗi thời |
| **Yêu cầu hạ tầng** | Chạy thẳng trên Bare RN CLI | Cần Expo Modules (`npx install-expo-modules`) | — |
| **Hiệu năng Frame** | ⭐⭐⭐⭐⭐ 60FPS, Frame Processor + Worklet | ⭐⭐⭐ Đủ cho chụp ảnh/quay phim | ⭐ Chậm, hay treo |
| **Quét mã vạch** | ✅ `useCodeScanner` (MLKit/Vision, native thuần) | ✅ `onBarcodeScanned` (đủ dùng, đơn giản) | ⚠️ Có nhưng nhiều bug |
| **Tự viết xử lý ảnh AI** | ✅ Frame Processor + plugin TFLite | ❌ Không hỗ trợ | ❌ Không |
| **Độ khó cài đặt** | Trung bình (cần sửa `gradle.properties`) | Dễ nhất | Khó, nhiều bước thủ công |
| **Kích thước thêm vào app** | ~3–6 MB (kèm model MLKit) | ~2 MB | ~5 MB |
| **Tuỳ chỉnh nâng cao** | Rất sâu: FPS, ISO, độ phơi sáng, zoom, format, HDR | Cơ bản: flash, zoom, tỉ lệ | Cơ bản |
| **Nên chọn khi** | Quét mã, xử lý ảnh thời gian thực, app camera chuyên nghiệp | Chỉ cần chụp ảnh/quay video đơn giản, muốn cài nhanh | **Không bao giờ** — chỉ gặp trong dự án cũ cần bảo trì |

**Kết luận cho ShopAI:** chúng ta chọn **Vision Camera**, vì bài toán quét Barcode thời gian thực đòi hỏi xử lý frame liên tục ở 60FPS — đúng thế mạnh của kiến trúc JSI.

> [!CAUTION]
> **Nếu bạn thấy một bài blog/video hướng dẫn dùng `react-native-camera` — hãy đóng lại ngay.** Thư viện đó đã ngừng bảo trì từ năm 2022, không tương thích với New Architecture (Fabric), và sẽ khiến bạn không build được trên RN 0.7x. Trên mạng vẫn còn hàng ngàn bài viết cũ dẫn bạn vào đường cụt — luôn kiểm tra ngày đăng bài và lần commit gần nhất trên GitHub trước khi làm theo.

---

## 📲 PHẦN 7.11: PUSH NOTIFICATIONS — ĐÁNH THỨC APP TỪ ĐÁM MÂY

Camera và GPS là những tính năng "App chủ động hỏi phần cứng". Push Notification đi theo chiều **ngược lại**: Server chủ động đánh thức App của người dùng, kể cả khi App đã bị tắt hẳn. Đây là kênh giữ chân người dùng mạnh nhất mà một App thương mại điện tử có: báo "Đơn hàng đang giao", "Giỏ hàng của bạn sắp hết ưu đãi", "Sản phẩm bạn theo dõi đã giảm giá".

### 1. Hai lựa chọn cho ShopAI (Bare RN CLI)

| Tiêu chí | 🥇 `@react-native-firebase/messaging` | `expo-notifications` |
|---|---|---|
| Phù hợp dự án | **Bare RN CLI** như ShopAI — không bắt buộc cài hạ tầng Expo Modules chỉ để dùng riêng tính năng này | Cả Expo Managed lẫn Bare (nhưng Bare thì vẫn cần hạ tầng Expo Modules — xem lại Chương 8, Bước 1) |
| Hạ tầng cần có | Dự án Firebase + `google-services.json` / `GoogleService-Info.plist` | Không bắt buộc Firebase trên Android (dùng Expo Push Service) |
| Đồng bộ với phần còn lại của khoá học | ✅ Dùng chung một dự án Firebase với **Crashlytics** (Chương 10) — tạo 1 lần, dùng cho cả hai | Cần thêm một hạ tầng riêng |
| Thông báo hẹn giờ / cục bộ (không cần mạng) | Cần thêm thư viện `notifee` | Có sẵn trong cùng package |
| **Sprint 7 chọn** | ✅ | — |

> [!NOTE]
> **Vì sao chọn `@react-native-firebase/messaging` dù Chương 7 đứng trước Chương 8/10?** Vì đây là lựa chọn **tự nhiên nhất cho một dự án Bare RN CLI** — không cần đợi tới Chương 8 mới có "cầu nối" Expo Modules. Ngẫu nhiên hơn nữa, dự án Firebase bạn tạo ở đây (Bước "Cài đặt" bên dưới) chính là dự án mà **Chương 10** sẽ tái sử dụng cho Firebase Crashlytics — tạo một lần, dùng cho cả app đời.

### 2. Sơ đồ luồng — Token đi đâu, thông báo về đâu?

```
[ShopAI khởi động lần đầu]
        │
        ▼
  Xin quyền thông báo (PermissionsAndroid trên Android 13+ / messaging().requestPermission() trên iOS)
        │
        ▼
  messaging().getToken() ──▶ In FCM Token ra console.log (Sprint 7 dừng ở đây)
        │                     (Thực tế: gửi token này lên Backend, lưu theo userId)
        ▼
┌────────────────────────────────────────────────────┐
│ Admin gửi thử qua Firebase Console › Cloud Messaging │
│ (dán đúng Token vừa copy từ console.log)             │
└───────────────────────────┬──────────────────────────┘
                            ▼
              Google FCM Server (đám mây trung gian)
                            │
     ┌──────────────────────┼───────────────────────────┐
     ▼                      ▼                            ▼
App đang MỞ            App chạy NỀN                App đã TẮT HẲN
(Foreground)             (Background)                 (Killed)
onMessage()        onNotificationOpenedApp()     getInitialNotification()
App tự vẽ Alert/Toast   User bấm noti để mở app    App khởi động từ đầu do bấm noti
(OS KHÔNG tự hiện banner)
```

### 3. Cài đặt tối thiểu

```bash
npm install @react-native-firebase/app @react-native-firebase/messaging
cd ios && pod install && cd ..
```

> [!TIP]
> Nếu bạn chưa có dự án Firebase, tạo ngay bây giờ tại `console.firebase.google.com` (mất khoảng 2 phút), tải `google-services.json` bỏ vào `android/app/` và `GoogleService-Info.plist` bỏ vào `ios/ShopAI/` — đúng quy trình mà Chương 10, Bước 1 sẽ mô tả lại chi tiết hơn cho Crashlytics. Dùng chung một dự án Firebase cho cả Push lẫn Crashlytics là thực hành chuẩn.

**Android 13+ (API 33) cần xin quyền Runtime riêng cho thông báo** — đây là quyền mới, khác hẳn Camera/Location:
```xml
<!-- android/app/src/main/AndroidManifest.xml -->
<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
```

**iOS cần tài khoản Apple Developer trả phí:** bật capability "Push Notifications" + "Background Modes > Remote notifications" trong Xcode, rồi tải lên Firebase Console một **APNs Authentication Key** (mục Project Settings → Cloud Messaging). Nếu lớp học không có tài khoản Apple Developer, hoàn thành nhánh Android là đủ để đạt yêu cầu nghiệm thu.

### 4. File tối thiểu: `src/services/pushNotificationService.ts`

```ts
import messaging from '@react-native-firebase/messaging';
import { Platform, PermissionsAndroid } from 'react-native';

/** Xin quyền hiện thông báo — khác quyền Camera/Location, đây là quyền RIÊNG cho notification. */
export const requestNotificationPermission = async (): Promise<boolean> => {
  if (Platform.OS === 'android' && Platform.Version >= 33) {
    const granted = await PermissionsAndroid.request(
      PermissionsAndroid.PERMISSIONS.POST_NOTIFICATIONS,
    );
    if (granted !== PermissionsAndroid.RESULTS.GRANTED) return false;
  }

  // iOS: bung Pop-up hệ thống xin quyền banner/âm thanh/badge
  const authStatus = await messaging().requestPermission();
  return (
    authStatus === messaging.AuthorizationStatus.AUTHORIZED ||
    authStatus === messaging.AuthorizationStatus.PROVISIONAL
  );
};

/** Lấy "địa chỉ nhà" duy nhất của app trên máy này để Server gửi thông báo đích danh. */
export const getFcmToken = async (): Promise<string | null> => {
  try {
    const token = await messaging().getToken();
    console.log('[push] FCM Token:', token); // Copy dòng này dán vào Firebase Console để gửi thử
    return token;
  } catch (e) {
    console.log('[push] Không lấy được token:', e);
    return null;
  }
};

/** App đang MỞ (foreground) — FCM KHÔNG tự vẽ banner lúc này, phải tự xử lý hiển thị. */
export const registerForegroundHandler = () =>
  messaging().onMessage(async (remoteMessage) => {
    console.log('[push] Nhận thông báo lúc app đang mở:', remoteMessage.notification);
  });

/** User bấm vào thông báo lúc app đang chạy NỀN (background, chưa bị tắt hẳn). */
export const registerBackgroundOpenHandler = (onOpen: (data: Record<string, string>) => void) =>
  messaging().onNotificationOpenedApp((remoteMessage) => {
    console.log('[push] Mở app từ thông báo (background):', remoteMessage.data);
    onOpen(remoteMessage.data);
  });

/** App bị TẮT HẲN (killed), user bấm thông báo để mở app từ đầu (cold start). */
export const getInitialNotification = async (): Promise<Record<string, string> | null> => {
  const remoteMessage = await messaging().getInitialNotification();
  if (remoteMessage) {
    console.log('[push] App mở từ trạng thái Killed do bấm thông báo:', remoteMessage.data);
    return remoteMessage.data;
  }
  return null;
};
```

**Đăng ký Background Handler ở `index.js` — BẮT BUỘC đặt NGOÀI React Tree:**

```js
// index.js (file gốc, KHÔNG phải App.tsx)
import { AppRegistry } from 'react-native';
import messaging from '@react-native-firebase/messaging';
import App from './App';
import { name as appName } from './app.json';

// Đây là quy định bắt buộc của Firebase Messaging: handler chạy khi thông báo
// đến lúc app đang nền sâu hoặc đã bị "giết" hẳn — phải đăng ký TRƯỚC KHI
// AppRegistry khởi động React Tree, không thể đặt trong Component nào cả.
messaging().setBackgroundMessageHandler(async (remoteMessage) => {
  console.log('[push] Thông báo đến khi app đang nền/killed:', remoteMessage);
});

AppRegistry.registerComponent(appName, () => App);
```

> [!CAUTION]
> **Lỗi kinh điển:** đặt `setBackgroundMessageHandler` bên trong `App.tsx` hoặc trong một `useEffect`. Handler sẽ **không bao giờ chạy** khi app đã bị tắt hẳn, vì lúc đó React Tree chưa hề được dựng lên. Nó **phải** nằm ở `index.js`, chạy độc lập với vòng đời Component.

### 5. Bảng giải thích nhanh 3 trạng thái App

| Trạng thái App | Hàm lắng nghe | Ai vẽ giao diện thông báo? |
|---|---|---|
| Đang mở (Foreground) | `onMessage()` | App của bạn tự vẽ (Alert/Toast) — OS im lặng |
| Chạy nền (Background) | `onNotificationOpenedApp()` | Hệ điều hành tự vẽ banner; hàm này chạy khi user **bấm vào** banner đó |
| Đã tắt hẳn (Killed) | `getInitialNotification()` (lúc mount) + `setBackgroundMessageHandler` (ở `index.js`) | Hệ điều hành tự vẽ; app khởi động lại từ đầu khi user bấm |

> [!WARNING]
> **Không test được Push trên Android Emulator thiếu Google Play Services**, và **không test được trên iOS Simulator** (Apple không hỗ trợ APNs cho máy ảo). Bắt buộc dùng máy Android thật (hoặc Emulator có cài sẵn ảnh hệ thống kèm Play Store) / iPhone thật để kiểm thử Sprint bên dưới.

Sprint 7 vẫn giữ **Camera quét mã vạch làm trọng tâm chính** (xem Yêu cầu Nghiệm thu ở phần Thực chiến bên dưới) — Push Notification được thực hành ở **Bước 13 (tuỳ chọn/nâng cao)** cuối Sprint, sau khi bạn đã hoàn thành trọn vẹn luồng Camera + Haptic + Location.

---

## 🧩 PHẦN 7.12: HÉ LỘ BÊN TRONG NATIVE MODULE — TỰ TAY VIẾT MỘT MODULE SIÊU NHỎ

Phần 7.1 đã mô tả bằng lời cơ chế JS gọi xuống Native. Phần này cho bạn **nhìn thấy** cơ chế đó bằng cách tự viết một Native Module bé nhất có thể: `ShopAIDevice.getAppFlavor()` — trả về chuỗi `"dev"` hoặc `"production"` đọc thẳng từ tầng Native, không phải giả lập bằng JS.

> [!NOTE]
> Đây là một **skeleton (bộ khung tối giản)** để bạn thấy đúng hình dạng của Native Module — không phải một thư viện sản xuất hoàn chỉnh (không xử lý lỗi đầy đủ, không đóng gói thành package npm riêng). Mục tiêu là nhận ra "à, hoá ra bên trong `react-native-vision-camera` cũng chỉ là phiên bản đồ sộ hơn của khung này thôi".

### 1. Bốn mảnh ghép và vai trò của từng file

| File | Ngôn ngữ | Vai trò |
|---|---|---|
| `src/native/ShopAIDevice.ts` | TypeScript | Vỏ bọc phía JS — gõ kiểu cho an toàn khi gọi `NativeModules.ShopAIDevice` |
| `ShopAIDeviceModule.kt` | Kotlin (Android) | Lớp "công nhân" — nơi viết logic thật, đánh dấu hàm lộ ra ngoài bằng `@ReactMethod` |
| `ShopAIDevicePackage.kt` | Kotlin (Android) | "Danh bạ" khai báo Module này tồn tại để React Native nạp lúc khởi động |
| `ShopAIDevice.swift` + `ShopAIDevice.m` | Swift + Objective-C (iOS) | Lớp công nhân iOS (Swift) + cầu nối Objective-C bắt buộc (Bridge của RN vốn viết bằng Objective-C) |

### 2. Phía Android — Kotlin

```kotlin
// android/app/src/main/java/com/shopai/ShopAIDeviceModule.kt
package com.shopai

import com.facebook.react.bridge.Promise
import com.facebook.react.bridge.ReactApplicationContext
import com.facebook.react.bridge.ReactContextBaseJavaModule
import com.facebook.react.bridge.ReactMethod

class ShopAIDeviceModule(reactContext: ReactApplicationContext) :
    ReactContextBaseJavaModule(reactContext) {

    // Tên này chính là thứ JS gọi qua NativeModules.ShopAIDevice
    override fun getName() = "ShopAIDevice"

    @ReactMethod
    fun getAppFlavor(promise: Promise) {
        try {
            // Đây là chỗ bạn gọi API thật của Android SDK (BuildConfig, BatteryManager, v.v.)
            promise.resolve(if (BuildConfig.DEBUG) "dev" else "production")
        } catch (e: Exception) {
            promise.reject("ERR_APP_FLAVOR", e)
        }
    }
}
```

```kotlin
// android/app/src/main/java/com/shopai/ShopAIDevicePackage.kt
package com.shopai

import com.facebook.react.ReactPackage
import com.facebook.react.bridge.NativeModule
import com.facebook.react.bridge.ReactApplicationContext
import com.facebook.react.uimanager.ViewManager

class ShopAIDevicePackage : ReactPackage {
    override fun createNativeModules(reactContext: ReactApplicationContext): List<NativeModule> =
        listOf(ShopAIDeviceModule(reactContext))

    override fun createViewManagers(reactContext: ReactApplicationContext): List<ViewManager<*, *>> =
        emptyList()
}
```

Đăng ký thủ công trong `MainApplication.kt` (Module viết ngay trong app thì **không** có Autolinking lo hộ — Autolinking ở Phần 7.4 chỉ quét `node_modules`):
```kotlin
override fun getPackages(): List<ReactPackage> =
    PackageList(this).packages.apply {
        add(ShopAIDevicePackage()) // ➕ Thêm dòng này
    }
```

### 3. Phía iOS — Swift + cầu nối Objective-C

```swift
// ios/ShopAI/ShopAIDevice.swift
import Foundation

@objc(ShopAIDevice)
class ShopAIDevice: NSObject {

  @objc
  func getAppFlavor(_ resolve: RCTPromiseResolveBlock, rejecter reject: RCTPromiseRejectBlock) {
    #if DEBUG
    resolve("dev")
    #else
    resolve("production")
    #endif
  }

  @objc
  static func requiresMainQueueSetup() -> Bool { return false }
}
```

```objc
// ios/ShopAI/ShopAIDevice.m — cầu nối bắt buộc, vì Bridge gốc của RN viết bằng Objective-C
#import <React/RCTBridgeModule.h>

@interface RCT_EXTERN_MODULE(ShopAIDevice, NSObject)
RCT_EXTERN_METHOD(getAppFlavor:(RCTPromiseResolveBlock)resolve
                  rejecter:(RCTPromiseRejectBlock)reject)
@end
```

### 4. Phía JS — dùng lại như mọi Native Module khác

```ts
// src/native/ShopAIDevice.ts
import { NativeModules } from 'react-native';

type ShopAIDeviceType = { getAppFlavor(): Promise<string> };

export default NativeModules.ShopAIDevice as ShopAIDeviceType;
```

```ts
import ShopAIDevice from '@native/ShopAIDevice';

const flavor = await ShopAIDevice.getAppFlavor();
console.log('App flavor:', flavor); // 'dev' hoặc 'production' — đọc thẳng từ Native, không phải JS đoán mò
```

### 5. Native Module (Bridge) cũ và Turbo Module (kiến trúc mới) khác nhau ở đâu?

| Tiêu chí | Native Module (Bridge — vừa viết ở trên) | Turbo Module (New Architecture) |
|---|---|---|
| Cách gọi | Qua Bridge, JSON serialize hai chiều | Qua JSI trực tiếp (giống Camera Frame Processor ở Phần 7.8), không serialize |
| Đăng ký | `ReactPackage` thủ công (như trên) hoặc Autolinking cho thư viện npm | **Codegen** tự sinh code từ một file spec TypeScript (`NativeShopAIDevice.ts` kế thừa `TurboModule`) |
| Nạp lúc nào | Nạp hết mọi Module lúc App khởi động | **Lazy load** — chỉ nạp đúng Module khi JS thật sự gọi tới lần đầu, giúp khởi động App nhanh hơn |
| Độ khó tiếp cận | Dễ, đúng như 4 file vừa viết | Cần bật New Architecture (Fabric) + cấu hình Codegen, phức tạp hơn hẳn |
| Sprint 7 | ✅ Skeleton minh hoạ (mục đích học tập) | Chỉ cần **biết khái niệm** — nằm ngoài phạm vi khoá học |

> [!TIP]
> **Bài tập tuỳ chọn:** thử đổi giá trị trả về của `getAppFlavor()` thành `Build.MODEL` (tên dòng máy Android) hoặc `UIDevice.current.model` (iOS) thay vì chuỗi cứng `"dev"`/`"production"` — đây chính xác là cách các thư viện như `react-native-device-info` hoạt động bên trong: một Native Module đơn giản, chỉ khác là có hàng chục hàm thay vì một.

---

## 🚀 THỰC CHIẾN SHOPAI (SPRINT 7: TÍCH HỢP QUÉT MÃ VẠCH BẰNG CAMERA)

**User Story:** *"Là nhân viên kho, tôi muốn bấm một nút để mở giao diện Camera, đưa mã vạch của sản phẩm vào quét và hệ thống tự động đọc ra mã Barcode, giúp tôi tra cứu hàng hóa không cần gõ tay. Camera phải tắt ngay khi tôi rời màn hình, và không được quét dính 50 lần liên tiếp chỉ vì tay tôi cầm máy hơi rung. Máy phải rung một cái nhẹ khi quét trúng để tôi biết mà không cần nhìn màn hình. Ngoài ra, ở Trang chủ tôi muốn thấy ngay phí ship ước tính dựa trên vị trí GPS của mình, khỏi phải mò vào tận trang thanh toán."*


### 📋 Khung thực hành chương (đọc trước khi gõ code)

> Đây là **bài thực hành của Chương 7** (không phải “lab mỗi ngày”). Làm hết Sprint này = đạt mục tiêu chương. Hoàn thành đủ 11 Sprint = sản phẩm ShopAI theo `SHOPAI_HOAN_THIEN.md`.

| Hạng mục | Nội dung |
|----------|----------|
| **Thời lượng gợi ý** | 5–7 tiết (cần máy thật cho Camera) |
| **Độ khó chương** | ★★★★☆ |
| **Đầu vào bắt buộc** | Sprint 6 PASS — Home/Cart/Checkout data layer ổn. |
| **Đầu ra sản phẩm** | Scanner trong HomeStack; quét mã + haptic; LocationBadge ước tính ship trên Home. |
| **Cách làm** | Làm **tuần tự từng Bước**. Gặp mốc ✓ bên dưới mà FAIL → dừng, sửa, rồi mới sang bước sau. |
| **Nghiệm thu cuối khóa** | Đối chiếu `SHOPAI_HOAN_THIEN.md` — mỗi Sprint chỉ tích thêm ô, không phá tính năng cũ. |

### ✓ Kiểm chứng theo mốc (trong lúc làm)

- **Sau Bước 1–2:** Build native với quyền Camera/Location PASS.
- **Sau Bước 4–6:** Mở Scanner từ Home; quét ra mã; không spam scan.
- **Sau Bước 7–10:** Badge vị trí/phí ship hiện trên Home.

> [!TIP]
> Xong Sprint 7, mở `SHOPAI_HOAN_THIEN.md` và tick các ô thuộc chương này. Mục tiêu cuối khóa: **mọi ô A/B/C/D (+ E đề cương) đều xanh** trong `SHOPAI_HOAN_THIEN.md` — đó mới là ShopAI hoàn thiện đẳng cấp.

### Yêu cầu Nghiệm thu:
1. Cài đặt thành công React Native Vision Camera v4+ (Thư viện Camera Native đỉnh cao nhất hiện nay, dùng C++ JSI) và bật Code Scanner đúng chuẩn.
2. Khai báo quyền `Info.plist` và `AndroidManifest.xml` chính xác (Camera + Vibrate + Location).
3. Viết Màn hình `ScannerScreen` (Quét mã), có Pop-up xin quyền lúc khởi chạy, có khóa chống quét lặp (Debounce Lock), và tự tắt Camera khi rời màn hình (`useIsFocused`).
4. **Xử lý trọn vẹn trường hợp user từ chối quyền:** hiện màn hình giải thích + nút "Mở Cài đặt" (`Linking.openSettings()`), và tự dò lại quyền khi user quay về app (`AppState`).
5. **Rung phản hồi (Haptic)** đúng một nhịp ngắn khi quét thành công, gói trong một tiện ích dùng lại được (`src/utils/haptics.ts`).
6. Đọc thành công Barcode/QR Code và trả về `HomeScreen` qua Route Params.
7. **Lấy được toạ độ GPS** bằng `@react-native-community/geolocation`, bọc trong hook `useCurrentLocation`, và hiển thị component `LocationBadge` (toạ độ + phí ship ước tính) trên `HomeScreen`.
8. Toàn bộ tính năng phụ (Haptic, Location) đều có **phương án dự phòng** — hỏng cũng không được làm sập màn hình chính.

### Bản đồ file sẽ tạo/sửa trong Sprint này

| File | Việc |
|------|------|
| `src/screens/ScannerScreen.tsx` | 🆕 Tạo mới — màn hình Camera quét mã |
| `src/utils/haptics.ts` | 🆕 Tạo mới — tiện ích rung phản hồi |
| `src/hooks/useCurrentLocation.ts` | 🆕 Tạo mới — hook lấy toạ độ GPS |
| `src/components/LocationBadge.tsx` | 🆕 Tạo mới — thẻ hiển thị vị trí + phí ship |
| `src/constants/shipping.ts` | 🆕 Tạo mới — hằng số kho hàng & bảng giá ship |
| `src/navigation/HomeStackNavigator.tsx` | ✏️ Sửa — thêm route `Scanner` |
| `src/screens/HomeScreen.tsx` | ✏️ Sửa — thêm nút "Quét Mã" + `LocationBadge` |
| `ios/ShopAI/Info.plist` | ✏️ Sửa — khai báo quyền Camera + Location |
| `android/app/src/main/AndroidManifest.xml` | ✏️ Sửa — khai báo quyền Camera + Vibrate + Location |
| `android/gradle.properties` | ✏️ Sửa — bật Code Scanner của MLKit |

### Hướng dẫn thực thi Step-by-Step:

*(Lưu ý: Camera **KHÔNG THỂ** chạy trên Simulator máy ảo của Xcode, và rất lỗi trên Emulator Android. Bạn BẮT BUỘC phải cắm điện thoại thật qua cáp USB như đã học ở Chương 1, Phần 1.5.5).*

> [!NOTE]
> **Vision Camera (JSI) hay Expo Camera — chọn đường nào?** Ở Phần 7.3 ta đã nói về Expo Modules như một hệ sinh thái Native Module hiện đại, ổn định (bao gồm cả `expo-camera`). Đó là một lựa chọn **hợp lệ và dễ cài đặt hơn** cho các bài toán Camera đơn giản (chụp ảnh, xem trước). Tuy nhiên, ShopAI của chúng ta cần xử lý khung hình theo thời gian thực ở 60FPS để quét Barcode/QR mượt mà — đây là bài toán hiệu năng cao mà **`react-native-vision-camera` (kiến trúc JSI thuần C++)** làm tốt hơn hẳn nhờ xử lý Frame trực tiếp trên luồng Native, không phải đi qua Bridge JSON chậm chạp. Vì vậy, **Sprint 7 chính thức đi theo con đường Vision Camera**. Nếu dự án của bạn sau này chỉ cần Camera chụp ảnh thông thường, `expo-camera` vẫn là lựa chọn nhẹ nhàng, ít cấu hình Native hơn.

#### Bước 1: Cài đặt siêu thư viện Vision Camera và Vision Camera Code Scanner
`react-native-vision-camera` được viết hoàn toàn bằng C++ với kiến trúc mới JSI, xử lý hình ảnh theo thời gian thực (60FPS) mượt hơn cả app Native gốc.

Chạy lệnh cài đặt (Bản mới nhất hiện tại là v4+):
```bash
npm install react-native-vision-camera
```

**Bắt buộc với iOS (Liên kết Pod C++):**
```bash
cd ios && pod install && cd ..
```

> [!WARNING]
> **Riêng cho Android — Kích hoạt Code Scanner (Bắt buộc từ v3.7+/v4):** Khác với iOS (dùng API Native có sẵn), Android cần nạp thêm Model nhận diện mã vạch của Google MLKit. Mở file `android/gradle.properties`, thêm dòng:
> ```groovy
> # Bật Code Scanner, nhúng thẳng Model MLKit (~2.4MB) vào App
> # Giúp quét được trên MỌI máy Android, kể cả máy không có Google Play Services
> VisionCamera_enableCodeScanner=true
> ```
> Thiếu dòng này, hàm `useCodeScanner` ở Bước 4 có thể không hoạt động ổn định trên một số thiết bị Android.

#### Bước 2: Cấu hình Khai báo Quyền hệ điều hành (Camera + Rung + Vị trí)

Ta khai báo **một lần cho cả Sprint** — gồm cả quyền Rung và Vị trí sẽ dùng ở các bước sau — để chỉ phải build lại Native đúng một lần ở cuối.

**A. Cho iOS:** Mở file `ios/ShopAI/Info.plist`, nhét đoạn này vào trước thẻ `</dict>` cuối cùng:
```xml
	<key>NSCameraUsageDescription</key>
	<string>ShopAI cần Camera của bạn để có thể quét mã vạch sản phẩm nhanh chóng.</string>
	<key>NSLocationWhenInUseUsageDescription</key>
	<string>ShopAI cần vị trí của bạn để ước tính chính xác phí và thời gian giao hàng tới địa chỉ của bạn.</string>
```

> [!TIP]
> **Viết dòng giải thích quyền sao cho App Store không đánh trượt:** phải nêu rõ **lợi ích cụ thể cho người dùng**, không được viết chung chung. So sánh nhanh:
> - ❌ `"App cần vị trí của bạn."` → Apple từ chối, lý do *"Purpose string is not specific enough"*.
> - ✅ `"ShopAI cần vị trí của bạn để ước tính chính xác phí và thời gian giao hàng tới địa chỉ của bạn."` → Được duyệt.
> Chuỗi này chính là dòng chữ hiện trong Pop-up mà user đọc trước khi bấm Allow, nên nó cũng quyết định tỉ lệ user đồng ý.

**B. Cho Android:** Mở file `android/app/src/main/AndroidManifest.xml`, thêm vào trên cùng (ngay dưới thẻ `<manifest>`, phía trên thẻ `<application>`):
```xml
    <!-- Quyền Runtime: phải xin Pop-up lúc chạy -->
    <uses-permission android:name="android.permission.CAMERA" />
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />

    <!-- Quyền Install-time: chỉ khai báo, KHÔNG cần Pop-up -->
    <uses-permission android:name="android.permission.VIBRATE" />
```

> [!NOTE]
> **Vì sao khai báo cả `FINE` lẫn `COARSE` Location?** Từ Android 12, Pop-up cho user tự chọn "Chính xác" hay "Gần đúng". Nếu bạn chỉ khai `FINE` mà user chọn "Gần đúng", hệ thống sẽ **âm thầm cấp `COARSE`** — thiếu khai báo `COARSE` trong Manifest thì tình huống này bị từ chối thẳng. Khai cả hai là cách an toàn tiêu chuẩn. Với ShopAI, độ chính xác vài trăm mét là quá đủ để tính phí ship.

Vì bạn vừa sửa file cấu hình Gradle/Manifest ở Native, nhớ build lại App ở bước cuối cùng — Hot Reload **không** áp dụng các thay đổi này.

#### Bước 3: Viết tiện ích Rung phản hồi (`src/utils/haptics.ts`)

Trước khi vào màn hình Camera, ta chuẩn bị sẵn "đồ nghề". Theo Phần 7.6, Chương 7 chưa có hạ tầng Expo Modules nên ta dùng `Vibration` API có sẵn của React Native — **không cần cài thêm gì cả**.

Điểm quan trọng về mặt kiến trúc: ta **không** gọi thẳng `Vibration.vibrate()` rải rác khắp nơi trong code UI. Ta gói nó vào một file tiện ích trung tâm. Nhờ vậy, sau này khi học xong Chương 8 và có `expo-haptics`, bạn chỉ cần sửa **đúng một file này** là toàn bộ app được nâng cấp.

Tạo file `src/utils/haptics.ts`:

```ts
import { Vibration, Platform } from 'react-native';

/**
 * Trung tâm điều phối rung phản hồi của ShopAI.
 *
 * Vì sao phải bọc lại thay vì gọi thẳng Vibration?
 *  1. Sau này đổi sang expo-haptics chỉ cần sửa ĐÚNG file này.
 *  2. Có thể tắt toàn bộ rung bằng 1 công tắc (phục vụ Cài đặt của user).
 *  3. Mọi lỗi rung đều bị nuốt gọn — tính năng phụ KHÔNG được làm sập app.
 */

// Công tắc tổng. Sau này có thể nối vào Zustand để user tự bật/tắt trong Cài đặt.
let hapticsEnabled = true;

export const setHapticsEnabled = (value: boolean) => {
  hapticsEnabled = value;
};

/** Hàm rung lõi — mọi hàm bên dưới đều đi qua đây. */
const safeVibrate = (pattern: number | number[]) => {
  if (!hapticsEnabled) return;
  try {
    Vibration.vibrate(pattern);
  } catch (e) {
    // Máy không có motor rung, hoặc user đã tắt rung trong Cài đặt hệ thống.
    // Nuốt lỗi im lặng: thà không rung còn hơn crash app.
    console.log('[haptics] Thiết bị không hỗ trợ rung:', e);
  }
};

/** Chạm nhẹ — dùng cho các nút bấm phụ. */
export const hapticLight = () => safeVibrate(20);

/** Chạm vừa — dùng cho nút hành động chính (Thêm vào giỏ, Thanh toán). */
export const hapticMedium = () => safeVibrate(40);

/**
 * Rung "THÀNH CÔNG" — hai nhịp ngắn liền nhau, cảm giác "tích-tắc".
 * Mảng đọc là: [đợi 0ms, rung 30ms, nghỉ 60ms, rung 30ms]
 * Đây là mẫu ta dùng cho việc quét mã vạch trúng đích.
 */
export const hapticSuccess = () => {
  if (Platform.OS === 'ios') {
    // iOS bỏ qua tham số thời lượng của Vibration API (xem Phần 7.6),
    // nên chỉ rung một nhịp chuẩn. Sau Chương 8 hãy thay bằng:
    // Haptics.notificationAsync(Haptics.NotificationFeedbackType.Success)
    safeVibrate(1);
  } else {
    safeVibrate([0, 30, 60, 30]);
  }
};

/** Rung "LỖI" — ba nhịp dài hơn, cảm giác dứt khoát khó chịu. */
export const hapticError = () => safeVibrate([0, 60, 80, 60, 80, 60]);
```

> [!TIP]
> **Đây là một mẫu thiết kế bạn nên áp dụng cho MỌI thứ đụng tới Native:** luôn có một lớp bọc (wrapper) mỏng của riêng bạn ở giữa. App của bạn gọi `hapticSuccess()`, chứ không gọi `Vibration.vibrate()`. Ngày mai đổi thư viện, đổi nền tảng, hay muốn thêm log/analytics — bạn chỉ sửa một chỗ. Nguyên tắc này trong kiến trúc phần mềm gọi là **Dependency Inversion** (Đảo ngược phụ thuộc).

#### Bước 4: Viết màn hình ScannerScreen thần thánh (khóa chống quét lặp + xử lý từ chối quyền)
Tạo file `src/screens/ScannerScreen.tsx`. Đây là một kiệt tác của việc xử lý vòng đời Camera gắn liền với Navigation.

**Ba bài toán thực tế mà màn hình này phải giải cùng lúc:**

1. **Chống quét lặp.** Camera quét ở 60FPS. Nếu không kiểm soát, chỉ trong 1 giây đưa mã vạch vào khung hình, hàm `onCodeScanned` có thể bị gọi tới 50–60 lần, khiến `navigation.navigate()` bị gọi dồn dập gây lag hoặc crash Navigation Stack. Ta cần một **"cái khóa" (Lock)** bằng `useRef` để chỉ cho phép xử lý ĐÚNG 1 lần quét đầu tiên.
2. **Xử lý user từ chối quyền** (Phần 7.5). Không được để user kẹt ở màn hình "Đang đợi..." vĩnh viễn. Phải có màn hình giải thích tử tế kèm nút mở Cài đặt.
3. **Dò lại quyền khi user quay về từ Settings.** Dùng `AppState` như đã học ở Phần 7.5.

```tsx
import React, { useCallback, useEffect, useRef, useState } from 'react';
import { AppState, Alert, Linking, StyleSheet, Text, View } from 'react-native';
import { Camera, useCameraDevice, useCodeScanner } from 'react-native-vision-camera';
import { useIsFocused } from '@react-navigation/native'; // Biết màn hình có đang hiển thị hay không
import ShopButton from '@components/ShopButton';
import { COLORS } from '@constants/theme';
import { hapticSuccess } from '@utils/haptics'; // Tiện ích rung vừa viết ở Bước 3

// Ba trạng thái của "cánh cổng quyền" — thay cho biến boolean cụt ngủn ban đầu.
// 'checking' = đang hỏi OS | 'granted' = được phép | 'denied' = bị chặn
type PermissionState = 'checking' | 'granted' | 'denied';

// Nhận tham số navigation từ React Navigation V7
const ScannerScreen = ({ navigation }: any) => {
  const [permission, setPermission] = useState<PermissionState>('checking');
  const device = useCameraDevice('back'); // Chọn ống kính mặt lưng
  const isFocused = useIsFocused(); // true nếu màn hình này đang ở trên cùng

  // "CÁI KHÓA" chống quét lặp — dùng useRef vì đổi giá trị không cần re-render lại UI
  const isScanning = useRef(false);

  // 1. Hàm xin/kiểm tra quyền — tách riêng để AppState gọi lại được
  const requestPermission = useCallback(async () => {
    // getCameraPermissionStatus() đọc trạng thái HIỆN TẠI mà không bung Pop-up.
    // Gọi nó trước để tránh làm phiền user nếu quyền đã được cấp từ trước.
    const current = Camera.getCameraPermissionStatus();
    if (current === 'granted') {
      setPermission('granted');
      return;
    }

    // Chưa có quyền -> gọi thẳng xuống C++/Native OS để bung Pop-up
    const status = await Camera.requestCameraPermission();
    setPermission(status === 'granted' ? 'granted' : 'denied');
  }, []);

  // 2. Xin quyền ở Runtime khi màn hình vừa Mount
  useEffect(() => {
    requestPermission();
  }, [requestPermission]);

  // 3. Khi user rời app sang Settings bật quyền rồi quay lại -> dò lại quyền
  //    Thiếu đoạn này, app sẽ vẫn hiện màn hình lỗi dù quyền đã được bật (Phần 7.5).
  useEffect(() => {
    const sub = AppState.addEventListener('change', (nextState) => {
      if (nextState === 'active') requestPermission();
    });
    return () => sub.remove(); // Dọn listener khi rời màn hình, tránh rò rỉ bộ nhớ
  }, [requestPermission]);

  // 4. Mở thẳng trang Cài đặt của chính app ShopAI trong Settings hệ thống
  const openAppSettings = () => {
    Alert.alert(
      'Cần quyền Camera',
      'Bạn đã từ chối quyền Camera nên ShopAI không thể quét mã vạch. Hãy vào Cài đặt > ShopAI và bật lại quyền Camera nhé.',
      [
        { text: 'Để sau', style: 'cancel' },
        { text: 'Mở Cài đặt', onPress: () => Linking.openSettings() },
      ],
    );
  };

  // 5. Logic Máy Quét (Vision Scanner JSI) — có khóa Debounce + rung phản hồi
  const codeScanner = useCodeScanner({
    codeTypes: ['qr', 'ean-13', 'code-128'], // QR, mã vạch siêu thị, mã vạch kho hàng
    onCodeScanned: (codes) => {
      // Nếu đã xử lý 1 lần rồi thì bỏ qua toàn bộ các lần quét dồn dập tiếp theo
      if (isScanning.current) return;
      if (codes.length === 0) return;

      const value = codes[0].value;
      if (!value) return; // Vision Camera có thể trả về mã rỗng khi ảnh mờ

      isScanning.current = true; // Đóng khóa lại NGAY LẬP TỨC
      console.log('Phát hiện mã:', value);

      // 📳 RUNG PHẢN HỒI: user biết đã quét trúng mà không cần nhìn màn hình.
      // Đặt NGAY SAU khi đóng khóa, TRƯỚC khi navigate — để cảm giác tức thời nhất.
      hapticSuccess();

      // Quét xong, bắn dữ liệu về HomeScreen (navigate sẽ tự unmount màn hình này)
      navigation.navigate('Home', { scannedCode: value });
    },
  });

  // ---------- Các trạng thái giao diện ----------

  // A. Đang hỏi hệ điều hành
  if (permission === 'checking') {
    return (
      <View style={styles.center}>
        <Text style={styles.stateText}>Đang kiểm tra quyền Camera...</Text>
      </View>
    );
  }

  // B. Bị từ chối -> KHÔNG để user kẹt ở màn hình trắng, phải cho lối thoát rõ ràng
  if (permission === 'denied') {
    return (
      <View style={styles.center}>
        <Text style={styles.deniedTitle}>Chưa có quyền Camera</Text>
        <Text style={styles.deniedDesc}>
          ShopAI cần Camera để quét mã vạch sản phẩm. Ảnh chỉ được xử lý ngay trên máy
          của bạn và không bao giờ được gửi đi đâu cả.
        </Text>
        <ShopButton
          title="Mở Cài đặt"
          onPress={openAppSettings}
          style={{ width: 200, marginBottom: 12 }}
        />
        <ShopButton
          title="Quay lại"
          onPress={() => navigation.goBack()}
          style={{ width: 200, backgroundColor: COLORS.secondary }}
        />
      </View>
    );
  }

  // C. Có quyền nhưng máy không có ống kính sau (rất hiếm, nhưng Simulator hay dính)
  if (device == null) {
    return (
      <View style={styles.center}>
        <Text style={styles.stateText}>Thiết bị không có Camera sau!</Text>
        <Text style={styles.deniedDesc}>
          Bạn có đang chạy trên máy ảo (Simulator/Emulator) không? Camera bắt buộc phải
          chạy trên điện thoại thật.
        </Text>
        <ShopButton title="Quay lại" onPress={() => navigation.goBack()} style={{ width: 200 }} />
      </View>
    );
  }

  return (
    <View style={styles.container}>
      {/* 6. Component C++ vẽ luồng Video 60FPS thẳng lên màn hình */}
      <Camera
        style={StyleSheet.absoluteFill} // Bọc kín toàn màn hình
        device={device}
        // isActive gắn với useIsFocused: Rời màn hình (chuyển Tab/Back) -> Camera TẮT NGAY
        // Tiết kiệm Pin và RAM, tránh giữ Camera mở ngầm không cần thiết
        isActive={isFocused}
        codeScanner={codeScanner} // Gắn cỗ máy quét vào ống kính
      />

      {/* 7. Khung ngắm giúp user biết đưa mã vào đâu — thuần UI, không ảnh hưởng logic quét */}
      <View style={styles.frameWrapper} pointerEvents="none">
        <View style={styles.frame} />
      </View>

      <View style={styles.overlay}>
        <Text style={styles.instruction}>Đưa mã vạch vào khung hình</Text>
        <ShopButton
          title="Hủy bỏ"
          onPress={() => navigation.goBack()}
          style={{ width: 150, backgroundColor: COLORS.error }}
        />
      </View>
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: 'black' },
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
    backgroundColor: COLORS.background,
  },
  stateText: { fontSize: 16, marginBottom: 12, textAlign: 'center' },
  deniedTitle: { fontSize: 20, fontWeight: 'bold', marginBottom: 10, color: COLORS.error },
  deniedDesc: { fontSize: 14, textAlign: 'center', marginBottom: 24, lineHeight: 20 },
  frameWrapper: { ...StyleSheet.absoluteFillObject, justifyContent: 'center', alignItems: 'center' },
  frame: {
    width: 250,
    height: 250,
    borderWidth: 3,
    borderColor: 'rgba(255,255,255,0.8)',
    borderRadius: 16,
  },
  overlay: {
    position: 'absolute',
    bottom: 50,
    alignSelf: 'center',
    alignItems: 'center',
  },
  instruction: {
    color: 'white',
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 20,
    backgroundColor: 'rgba(0,0,0,0.5)',
    padding: 10,
    borderRadius: 8,
  },
});

export default ScannerScreen;
```

> [!NOTE]
> **Nhận diện `@utils/haptics` — Path Alias từ Chương 2.** Nếu dòng `import { hapticSuccess } from '@utils/haptics'` báo đỏ, nghĩa là dự án của bạn chưa khai báo alias `@utils`. Mở `tsconfig.json` và `babel.config.js`, thêm `"@utils/*": ["src/utils/*"]` vào `paths` giống như các alias `@components`, `@screens`, `@constants` đã có. Sau khi sửa `babel.config.js`, **bắt buộc** khởi động lại Metro với `npx react-native start --reset-cache`, nếu không Metro vẫn dùng cấu hình cũ trong cache.

> [!TIP]
> **Tại sao dùng `useRef` mà không dùng `useState` cho khóa `isScanning`?** Vì đổi giá trị của `useState` sẽ kích hoạt re-render lại Component. Trong lúc Camera đang quét ở 60FPS, ta muốn "đóng khóa" xử lý ngay lập tức, không cần chờ React render lại xong mới có hiệu lực. `useRef` thay đổi giá trị tức thời, không tốn một khung hình render nào — đúng bài toán hiệu năng cao.

> [!TIP]
> **Bài tập mở rộng tùy chọn (liên hệ Chương 5 + Chương 7):** Nếu quy ước mã vạch/QR của một sản phẩm chính là `productId` của nó (VD: dán QR lên kệ hàng chứa đúng chuỗi ID sản phẩm trong hệ thống), bạn có thể sửa `onCodeScanned` để điều hướng thẳng sang trang chi tiết thay vì luôn trả `scannedCode` về `Home`:
> ```tsx
> // Nếu scannedCode có định dạng giống productId trong hệ thống -> nhảy thẳng vào Chi tiết sản phẩm
> if (value.startsWith('backend_prod_')) {
>   navigation.navigate('ProductDetail', { productId: value }); // Tái sử dụng Route Params đã học ở Chương 5
> } else {
>   navigation.navigate('Home', { scannedCode: value });
> }
> ```
> Đây chỉ là bài tập **tùy chọn**, không bắt buộc trong Yêu cầu Nghiệm thu Sprint 7 — mục tiêu là luyện lại kỹ năng Route Params (Chương 5) kết hợp với dữ liệu thật đọc từ Camera (Chương 7).

#### Bước 5: Khai báo Scanner vào HomeStack (KHÔNG phá Bottom Tab)
Từ Chương 5–6, luồng đã đăng nhập là `MainTabNavigator` → Tab Trang chủ chứa `HomeStackNavigator`. Scanner là màn hình phụ của Home, nên đăng ký vào **Home Stack**, không tạo lại `MainStack` phẳng.

Mở `src/navigation/HomeStackNavigator.tsx`, thêm màn hình Scanner:

```tsx
import ScannerScreen from '@screens/ScannerScreen';

export type HomeStackParamList = {
  Home: { scannedCode?: string } | undefined;
  ProductDetail: { productId: string };
  Scanner: undefined;
};

// Trong Stack.Navigator:
<Stack.Screen name="Home" component={HomeScreen} options={{ headerShown: false }} />
<Stack.Screen name="ProductDetail" component={ProductDetailScreen} options={{ title: 'Chi tiết' }} />
<Stack.Screen name="Scanner" component={ScannerScreen} options={{ headerShown: false }} />
```
> [!CAUTION]
> Đừng quên `options={{ headerShown: false }}` cho `Home` — `HomeScreen` tự vẽ Header riêng của nó (xem `styles.header` ở Bước 6 dưới đây), nếu để Header mặc định của Stack Navigator hiện lên, bạn sẽ bị dính 2 tầng Header đè lên nhau.

> `App.tsx` và `MainTabNavigator` **giữ nguyên** — chỉ sửa Home Stack.

#### Bước 6: Cập nhật HomeScreen để nhận mã vạch
Mở file `src/screens/HomeScreen.tsx`. Thêm nút Mở Camera và bắt `route.params` để hiển thị mã vừa quét được. `SafeAreaView` vẫn phải import từ `react-native-safe-area-context` như đã sửa ở Chương 6 (KHÔNG lấy từ `react-native`) — chỉ thêm phần `scannedCode` và nút "Quét Mã" vào Header có sẵn, phần `FlashList`/danh sách sản phẩm phía dưới giữ nguyên như Chương 6:

```tsx
import React from 'react';
import { View, Text, StyleSheet, Pressable, ActivityIndicator } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context'; // Giữ đúng nguồn import như Chương 6
// ... các import khác (useQuery, FlashList, ProductCard, useAuthStore, useCartStore, CompositeScreenProps...) giữ nguyên như Chương 6

// Sửa Type Props: HomeStackParamList giờ có thêm route.params.scannedCode (khai báo ở Bước 5).
// Vẫn dùng CompositeScreenProps như Chương 6 vì Header còn nút "Giỏ hàng" điều hướng sang Tab Cart.
type Props = CompositeScreenProps<
  NativeStackScreenProps<HomeStackParamList, 'Home'>,
  BottomTabScreenProps<MainTabParamList>
>;

const HomeScreen = ({ navigation, route }: Props) => {
  // ... code cũ của Chương 6 giữ nguyên (useQuery, logout, totalQuantity...)

  // Lấy dữ liệu mã vạch trả về từ màn hình Scanner (nếu có)
  const scannedCode = route.params?.scannedCode;

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
            <ShopButton
              title="Quét Mã"
              onPress={() => navigation.navigate('Scanner')}
              style={{ width: 100, height: 32, backgroundColor: COLORS.secondary }}
            />
            <ShopButton title="Thoát" onPress={logout} style={{ width: 80, height: 32 }} />
          </View>
        </View>

        {/* Báo cáo nếu quét thành công */}
        {scannedCode && (
          <View style={{ backgroundColor: 'yellow', padding: 10, alignItems: 'center' }}>
            <Text style={{ fontWeight: 'bold' }}>Mã vừa quét: {scannedCode}</Text>
          </View>
        )}

        {/* Phần Loading/Error/FlashList render danh sách sản phẩm — GIỮ NGUYÊN như Chương 6, Bước 8 */}
        {isLoading && <ActivityIndicator size="large" color={COLORS.primary} style={{ marginTop: 50 }} />}
        {isError && <Text style={{ textAlign: 'center', marginTop: 50, color: 'red' }}>Lỗi mạng hoặc dữ liệu không hợp lệ!</Text>}
        {products && (
          <FlashList
            data={products}
            keyExtractor={(item) => item.id}
            renderItem={({ item }) => (
              <Pressable onPress={() => navigation.navigate('ProductDetail', { productId: item.id })}>
                <ProductCard product={item} />
              </Pressable>
            )}
            numColumns={2}
            estimatedItemSize={260}
            contentContainerStyle={{ padding: SIZES.padding }}
          />
        )}
      </View>
    </SafeAreaView>
  );
};
```

#### Bước 7: Cài thư viện Định vị & khai báo hằng số vận chuyển

Theo Phần 7.7, ta chọn `@react-native-community/geolocation` — thư viện nhẹ, chạy thẳng trên Bare RN CLI, **không** cần hạ tầng Expo Modules (thứ mà Chương 8 mới cài).

```bash
npm install @react-native-community/geolocation

# iOS: nối dây Native (Autolinking sẽ tự tìm thấy podspec — xem lại Phần 7.4)
cd ios && pod install && cd ..
```

> [!NOTE]
> **Nếu bạn "trót" muốn dùng `expo-location` ngay từ Chương 7:** bạn phải chạy `npx install-expo-modules@latest` (chính là Bước 1 của Chương 8) trước, rồi `npx expo install expo-location`. Cách này **hoàn toàn hợp lệ** và cho bạn thêm tính năng Reverse Geocoding (đổi toạ độ ra tên đường). Tuy nhiên, để cả lớp cùng build được và không ai bị kẹt, **giáo trình khuyến nghị đi theo `@react-native-community/geolocation` ở Chương 7**, rồi để Chương 8 lo phần Expo Modules một cách gọn gàng. Đừng trộn cả hai trong cùng một lần build.

Quyền `ACCESS_FINE_LOCATION` / `NSLocationWhenInUseUsageDescription` **bạn đã khai ở Bước 2 rồi** — không cần làm lại.

Bây giờ tạo file hằng số `src/constants/shipping.ts`. Đưa mọi con số "ma thuật" ra một chỗ là thói quen của kỹ sư chuyên nghiệp — sau này đổi bảng giá chỉ sửa một file, không phải lùng sục khắp code:

```ts
/** Toạ độ kho hàng trung tâm của ShopAI (giả lập: Quận 1, TP. Hồ Chí Minh). */
export const WAREHOUSE_COORDS = {
  latitude: 10.7769,
  longitude: 106.7009,
};

/** Bảng giá ship theo khoảng cách (đơn vị: VNĐ). */
export const SHIPPING_TIERS = [
  { maxKm: 5, fee: 15000, label: 'Nội thành — giao trong 2 giờ' },
  { maxKm: 20, fee: 25000, label: 'Ngoại thành — giao trong ngày' },
  { maxKm: 100, fee: 40000, label: 'Liên tỉnh gần — 1-2 ngày' },
  { maxKm: Infinity, fee: 60000, label: 'Liên tỉnh xa — 3-5 ngày' },
];

/** Phí mặc định khi KHÔNG xác định được vị trí (user từ chối quyền, GPS lỗi...). */
export const DEFAULT_SHIPPING_FEE = 30000;

/**
 * Tính khoảng cách đường chim bay giữa 2 toạ độ bằng công thức Haversine.
 * Đây là toán học thuần tuý, không đụng gì tới Native — bạn không cần thuộc công thức,
 * chỉ cần hiểu: đầu vào là 2 cặp (vĩ độ, kinh độ), đầu ra là số km.
 */
export const getDistanceKm = (
  lat1: number,
  lon1: number,
  lat2: number,
  lon2: number,
): number => {
  const R = 6371; // Bán kính Trái Đất, đơn vị km
  const toRad = (deg: number) => (deg * Math.PI) / 180;

  const dLat = toRad(lat2 - lat1);
  const dLon = toRad(lon2 - lon1);

  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRad(lat1)) * Math.cos(toRad(lat2)) * Math.sin(dLon / 2) ** 2;

  return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
};

/** Tra bảng giá: từ số km ra mức phí + nhãn mô tả. */
export const getShippingTier = (distanceKm: number) => {
  return SHIPPING_TIERS.find((tier) => distanceKm <= tier.maxKm) ?? SHIPPING_TIERS[SHIPPING_TIERS.length - 1];
};
```

#### Bước 8: Viết hook `useCurrentLocation` (bọc GPS thành API sạch sẽ)

`@react-native-community/geolocation` dùng API kiểu **callback cũ** (giống `navigator.geolocation` trên Web). Ta sẽ bọc nó thành một Custom Hook trả về đúng 4 thứ mà UI cần: `coords`, `loading`, `error`, `refresh`. Đây chính là mẫu thiết kế "lớp bọc mỏng" mà Bước 3 đã nói.

Tạo file `src/hooks/useCurrentLocation.ts`:

```ts
import { useCallback, useEffect, useState } from 'react';
import { Alert, Linking, PermissionsAndroid, Platform } from 'react-native';
import Geolocation from '@react-native-community/geolocation';

export type Coords = { latitude: number; longitude: number };

type LocationState = {
  coords: Coords | null;
  loading: boolean;
  error: string | null;
};

/**
 * Xin quyền vị trí.
 * - Android: phải tự gọi PermissionsAndroid (thư viện này không tự xin).
 * - iOS: thư viện tự bung Pop-up dựa trên Info.plist, nên ta chỉ cần trả về true.
 */
const requestLocationPermission = async (): Promise<boolean> => {
  if (Platform.OS === 'ios') {
    Geolocation.requestAuthorization(); // Đọc NSLocationWhenInUseUsageDescription trong Info.plist
    return true;
  }

  const granted = await PermissionsAndroid.request(
    PermissionsAndroid.PERMISSIONS.ACCESS_FINE_LOCATION,
    {
      title: 'ShopAI cần quyền vị trí',
      message: 'Cho phép ShopAI biết vị trí để tính chính xác phí giao hàng tới nhà bạn.',
      buttonPositive: 'Cho phép',
      buttonNegative: 'Để sau',
    },
  );

  // PermissionsAndroid trả về 3 giá trị: 'granted' | 'denied' | 'never_ask_again'
  if (granted === PermissionsAndroid.RESULTS.NEVER_ASK_AGAIN) {
    Alert.alert(
      'Quyền vị trí đã bị chặn',
      'Bạn đã chọn "Không hỏi lại". Hãy vào Cài đặt > ShopAI > Quyền > Vị trí để bật lại.',
      [
        { text: 'Để sau', style: 'cancel' },
        { text: 'Mở Cài đặt', onPress: () => Linking.openSettings() },
      ],
    );
    return false;
  }

  return granted === PermissionsAndroid.RESULTS.GRANTED;
};

export const useCurrentLocation = () => {
  const [state, setState] = useState<LocationState>({
    coords: null,
    loading: true,
    error: null,
  });

  const fetchLocation = useCallback(async () => {
    setState((s) => ({ ...s, loading: true, error: null }));

    const ok = await requestLocationPermission();
    if (!ok) {
      setState({ coords: null, loading: false, error: 'Chưa được cấp quyền vị trí' });
      return;
    }

    // Bọc API callback cũ thành Promise-style bằng cách setState trực tiếp trong callback
    Geolocation.getCurrentPosition(
      (position) => {
        setState({
          coords: {
            latitude: position.coords.latitude,
            longitude: position.coords.longitude,
          },
          loading: false,
          error: null,
        });
      },
      (err) => {
        // err.code: 1 = từ chối quyền, 2 = không bắt được tín hiệu, 3 = quá thời gian chờ
        const messages: Record<number, string> = {
          1: 'Bạn đã từ chối quyền vị trí',
          2: 'Không bắt được tín hiệu GPS',
          3: 'Quá thời gian chờ GPS (thử ra ngoài trời)',
        };
        setState({
          coords: null,
          loading: false,
          error: messages[err.code] ?? 'Không lấy được vị trí',
        });
      },
      {
        enableHighAccuracy: false, // false = ưu tiên Wi-Fi/trạm phát sóng, nhanh & tiết kiệm pin.
                                   // Tính phí ship chỉ cần chính xác vài trăm mét là quá đủ.
        timeout: 15000,            // BẮT BUỘC có timeout, nếu không app treo vô hạn (Phần 7.7)
        maximumAge: 60000,         // Chấp nhận toạ độ đã cache trong 60 giây gần nhất
      },
    );
  }, []);

  useEffect(() => {
    fetchLocation();
  }, [fetchLocation]);

  return { ...state, refresh: fetchLocation };
};
```

> [!TIP]
> **Vì sao tách thành Custom Hook mà không viết thẳng vào `HomeScreen`?** Ba lý do rất thực tế: (1) Chương 6 `CheckoutScreen` cũng cần vị trí để tính phí ship thật — chỉ cần gọi lại `useCurrentLocation()` là xong, không copy-paste một dòng nào; (2) logic xin quyền phân nhánh iOS/Android khá rối, nhốt nó vào một chỗ giúp `HomeScreen` sạch sẽ; (3) sau này muốn đổi sang `expo-location`, bạn chỉ sửa **ruột** hook này, mọi màn hình đang dùng đều không phải đụng vào.

#### Bước 9: Viết component `LocationBadge` (thẻ hiển thị vị trí + phí ship)

Tạo file `src/components/LocationBadge.tsx`. Component này phải xử lý gọn cả 3 trạng thái: đang tải, lỗi, và thành công.

```tsx
import React from 'react';
import { ActivityIndicator, Pressable, StyleSheet, Text, View } from 'react-native';
import { useCurrentLocation } from '@hooks/useCurrentLocation';
import {
  DEFAULT_SHIPPING_FEE,
  WAREHOUSE_COORDS,
  getDistanceKm,
  getShippingTier,
} from '@constants/shipping';
import { COLORS, SIZES } from '@constants/theme';

const formatVnd = (value: number) => `${value.toLocaleString('vi-VN')}đ`;

const LocationBadge = () => {
  const { coords, loading, error, refresh } = useCurrentLocation();

  // --- Trạng thái 1: Đang dò GPS ---
  if (loading) {
    return (
      <View style={styles.badge}>
        <ActivityIndicator size="small" color={COLORS.primary} />
        <Text style={styles.textMuted}>  Đang xác định vị trí của bạn...</Text>
      </View>
    );
  }

  // --- Trạng thái 2: Lỗi / bị từ chối -> KHÔNG làm sập màn hình, chỉ hạ cấp trải nghiệm ---
  if (error || !coords) {
    return (
      <Pressable style={styles.badge} onPress={refresh}>
        <Text style={styles.textMuted}>
          📍 {error ?? 'Chưa rõ vị trí'} — tạm tính phí ship {formatVnd(DEFAULT_SHIPPING_FEE)}
        </Text>
        <Text style={styles.retry}>Thử lại</Text>
      </Pressable>
    );
  }

  // --- Trạng thái 3: Thành công -> tính khoảng cách và tra bảng giá ---
  const distanceKm = getDistanceKm(
    coords.latitude,
    coords.longitude,
    WAREHOUSE_COORDS.latitude,
    WAREHOUSE_COORDS.longitude,
  );
  const tier = getShippingTier(distanceKm);

  return (
    <Pressable style={[styles.badge, styles.badgeSuccess]} onPress={refresh}>
      <View style={{ flex: 1 }}>
        <Text style={styles.title}>
          📍 Cách kho {distanceKm.toFixed(1)} km · Ship {formatVnd(tier.fee)}
        </Text>
        <Text style={styles.subtitle}>{tier.label}</Text>
        <Text style={styles.coords}>
          ({coords.latitude.toFixed(4)}, {coords.longitude.toFixed(4)})
        </Text>
      </View>
      <Text style={styles.retry}>Làm mới</Text>
    </Pressable>
  );
};

const styles = StyleSheet.create({
  badge: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#F2F2F2',
    paddingVertical: 10,
    paddingHorizontal: SIZES.padding,
  },
  badgeSuccess: { backgroundColor: '#E8F5E9' },
  title: { fontSize: 13, fontWeight: 'bold' },
  subtitle: { fontSize: 12, color: '#555', marginTop: 2 },
  coords: { fontSize: 11, color: '#888', marginTop: 2 },
  textMuted: { fontSize: 13, color: '#555', flex: 1 },
  retry: { fontSize: 12, color: COLORS.primary, fontWeight: 'bold', marginLeft: 8 },
});

export default LocationBadge;
```

> [!CAUTION]
> **Đừng quên alias `@hooks`.** Nếu `tsconfig.json` / `babel.config.js` của bạn chưa có `"@hooks/*": ["src/hooks/*"]`, hãy thêm vào ngay bây giờ rồi chạy lại Metro với cờ `--reset-cache`. Đây là lỗi số 1 mà học viên gặp ở bước này, và thông báo lỗi (`Unable to resolve module @hooks/useCurrentLocation`) trông rất giống lỗi Native khiến nhiều bạn đi sai hướng gỡ rối.

#### Bước 10: Gắn `LocationBadge` vào HomeScreen

Mở lại `src/screens/HomeScreen.tsx`, chèn `<LocationBadge />` ngay dưới Header, phía trên khối `scannedCode`:

```tsx
import LocationBadge from '@components/LocationBadge';

// ... bên trong phần return, ngay sau </View> đóng của styles.header:

{/* Thẻ vị trí + phí ship — tự dò GPS khi màn hình mount */}
<LocationBadge />

{/* Báo cáo nếu quét thành công (đã thêm ở Bước 6) */}
{scannedCode && (
  <View style={{ backgroundColor: 'yellow', padding: 10, alignItems: 'center' }}>
    <Text style={{ fontWeight: 'bold' }}>Mã vừa quét: {scannedCode}</Text>
  </View>
)}
```

Chỉ một dòng `<LocationBadge />` — toàn bộ logic xin quyền, dò GPS, tính khoảng cách, tra bảng giá đều nằm gọn bên trong. Đó chính là sức mạnh của việc tách Component và Custom Hook đúng cách.

> [!TIP]
> **Bài tập mở rộng tùy chọn (liên hệ Chương 6):** `CheckoutScreen` ở Chương 6 hiện đang tính tổng tiền = tổng giá sản phẩm. Hãy gọi `useCurrentLocation()` trong đó, cộng thêm phí ship tính từ khoảng cách thật, và hiển thị dòng "Phí vận chuyển" tách riêng trong hóa đơn. Đây là ví dụ hoàn hảo cho thấy vì sao ta bọc GPS thành Hook ở Bước 8.

#### Bước 11: Build Native App Toàn diện & Tận hưởng
Vì bạn vừa chỉnh sửa file `Info.plist`, `AndroidManifest.xml`, `gradle.properties` và cài tới hai thư viện Native (Vision Camera + Geolocation), app cũ của bạn đang chạy sẽ CHẾT NGẮC hoặc bị Crash văng màu đỏ. **Đừng hoảng sợ, đây là bản chất của Native Module** (xem lại Phần 7.4 để hiểu vì sao).

Làm theo nghi thức:
1. Tắt sạch Terminal Metro đang chạy.
2. Cắm cáp điện thoại thật.
3. Chạy `cd ios && pod install && cd ..` nếu bạn build iOS (Autolinking cần chạy lại để nối dây cả 2 thư viện mới).
4. Gõ lệnh: `npm run ios` hoặc `npm run android` để Build lại App mới từ đầu.

Nếu màn hình đỏ lòm hiện ra thay vì app — **đừng hoảng, hãy mở lại Phần 7.9** và tra bảng lỗi ở đó. 95% lỗi bạn gặp trong bước này đã nằm sẵn trong bảng.

Sau 5 phút chờ đợi máy tính biên dịch mã C++, App bung lên điện thoại thật. Trang chủ hiện ngay thẻ "Đang xác định vị trí..." rồi đổi thành "📍 Cách kho 3.2 km · Ship 15.000đ". Bạn bấm "Quét Mã", Pop-up xin quyền cấp phép OS bung ra. Bạn bấm Cho phép. Ống kính Camera 60FPS sắc nét mở ra, đưa mã vạch vào khung — máy **rung một cái "tích-tắc"** và kết quả bắn về màn hình chính ngay tức khắc!

Bạn đã chính thức chinh phục ranh giới giữa Code Web ảo và Phần cứng vật lý!

#### Bước 12: Bảng kiểm tự chấm Sprint 7

Tick từng dòng trên **điện thoại thật** trước khi commit:

| # | Hạng mục kiểm tra | Cách thử | ✅ |
|---|---|---|---|
| 1 | Camera mở được, hình ảnh mượt không giật | Bấm "Quét Mã" | ☐ |
| 2 | Quét trúng mã vạch, giá trị hiện ở Home | Quét bất kỳ mã vạch trên hộp sữa/sách | ☐ |
| 3 | Máy rung đúng **một** nhịp khi quét trúng | Chú ý cảm giác trên tay | ☐ |
| 4 | Không bị quét lặp / nhảy màn hình nhiều lần | Giữ mã trong khung 5 giây | ☐ |
| 5 | Camera **tắt** khi rời màn hình | Bấm Back, đèn báo Camera của OS phải tắt | ☐ |
| 6 | Từ chối quyền → hiện màn hình giải thích, không kẹt | Gỡ app cài lại, bấm Deny | ☐ |
| 7 | Nút "Mở Cài đặt" mở đúng trang ShopAI | Bấm thử | ☐ |
| 8 | Bật quyền trong Settings rồi quay lại → Camera tự chạy | Không cần khởi động lại app | ☐ |
| 9 | `LocationBadge` hiện toạ độ và phí ship | Nhìn Trang chủ | ☐ |
| 10 | Từ chối quyền vị trí → vẫn hiện phí mặc định, app không sập | Bấm Deny quyền Location | ☐ |
| 11 | Bấm "Làm mới" trên badge → dò lại vị trí | Bấm thử | ☐ |
| 12 | Tab Giỏ hàng, luồng Đăng nhập/Đăng xuất vẫn nguyên vẹn | Bấm dạo quanh app | ☐ |

```bash
git add .
git commit -m "Sprint 7: Vision Camera JSI scanner, haptic feedback, GPS shipping estimate and full permission UX"
```

#### Bước 13 (TÙY CHỌN — Nâng cao): Lấy FCM Token và nhận thông báo thử

Bước này áp dụng lý thuyết Phần 7.11. **Không bắt buộc** để đạt Yêu cầu Nghiệm thu Sprint 7 (Camera vẫn là trọng tâm chính), nhưng rất đáng làm nếu bạn còn thời gian — đây là nền tảng cho tính năng "Thông báo đơn hàng" của một App thương mại điện tử thật.

**13.1. Cài đặt và khai báo quyền** (xem chi tiết ở Phần 7.11 mục 3):
```bash
npm install @react-native-firebase/app @react-native-firebase/messaging
cd ios && pod install && cd ..
```
Thêm `<uses-permission android:name="android.permission.POST_NOTIFICATIONS" />` vào `AndroidManifest.xml`.

**13.2. Tạo `src/services/pushNotificationService.ts`** — copy nguyên file ở Phần 7.11 mục 4.

**13.3. Đăng ký Background Handler ở `index.js`** — copy đoạn `messaging().setBackgroundMessageHandler(...)` ở Phần 7.11 mục 4, đặt **trước** dòng `AppRegistry.registerComponent`.

**13.4. Gọi từ `HomeScreen` hoặc `App.tsx`, in Token ra console:**
```tsx
import { useEffect } from 'react';
import { requestNotificationPermission, getFcmToken, registerForegroundHandler } from '@services/pushNotificationService';

useEffect(() => {
  (async () => {
    const granted = await requestNotificationPermission();
    if (granted) await getFcmToken(); // Token in ra console.log — copy dòng này
  })();

  const unsubscribe = registerForegroundHandler();
  return unsubscribe;
}, []);
```

**13.5. Gửi thử bằng Firebase Console:**
1. Chạy app trên máy thật, mở Terminal Metro, tìm dòng log `[push] FCM Token: ...`, copy toàn bộ chuỗi.
2. Vào `console.firebase.google.com` → dự án của bạn → **Engage → Messaging** (hoặc **Cloud Messaging**) → "Tạo chiến dịch đầu tiên" → Thông báo.
3. Điền tiêu đề/nội dung, ở mục "Nhắm mục tiêu" chọn **Gửi kiểm tra** (Send test message), dán FCM Token vừa copy.
4. Bấm Gửi. Nếu app đang mở, bạn sẽ thấy `[push] Nhận thông báo lúc app đang mở` trong console (do `onMessage`). Nếu bấm Home để app chạy nền rồi gửi lại, bạn sẽ thấy banner thông báo thật của hệ điều hành hiện ra.

| # | Hạng mục kiểm tra (tuỳ chọn) | ✅ |
|---|---|---|
| 1 | Console in ra được FCM Token hợp lệ (chuỗi dài ~150+ ký tự) | ☐ |
| 2 | Gửi test từ Firebase Console → thấy log ở `onMessage` khi app đang mở | ☐ |
| 3 | Đưa app xuống nền, gửi lại → thấy banner thông báo thật của OS | ☐ |

```bash
git add .
git commit -m "Sprint 7 (bonus): FCM push notification token + test message"
```

---

## 📝 TỔNG KẾT CHƯƠNG 7

Bạn vừa đi qua một chương nặng ký nhất về mặt kỹ thuật hạ tầng. Hãy điểm lại những gì đã nắm được:

| Kiến thức | Bạn phải trả lời được |
|-----------|------------------------|
| Native Module | Vì sao cài thư viện Native thì Hot Reload vô hiệu, phải build lại? |
| Sandboxing & Permissions | Info.plist khác AndroidManifest ở điểm gì? Vì sao iOS chỉ hỏi 1 lần? |
| Autolinking (7.4) | `pod install` và Gradle làm gì sau lưng bạn? Khi nào phải Manual Link? |
| Quyền bị chặn (7.5) | `denied` khác `blocked` thế nào? Vì sao cần `AppState` sau `openSettings()`? |
| Haptic (7.6) | Vibration khác Haptic ra sao? Vì sao phải bọc vào file tiện ích riêng? |
| Location (7.7) | `FINE` khác `COARSE`? Vì sao **bắt buộc** phải có `timeout` và phương án dự phòng? |
| JSI & Frame Processor (7.8) | Vì sao 180MB/giây không thể đi qua Bridge? Chỉ thị `'worklet'` làm gì? |
| Gỡ rối build (7.9) | Đọc log lỗi Native bắt đầu từ đâu? Nghi thức "dọn nhà toàn tập" gồm mấy tầng? |
| So sánh Camera (7.10) | Vì sao ShopAI chọn Vision Camera thay vì Expo Camera? |
| Push Notification (7.11) | Vì sao `setBackgroundMessageHandler` phải đặt ở `index.js`? 3 trạng thái App khác nhau ra sao? |
| Native Module tự viết (7.12) | 4 file cần có để gọi được `ShopAIDevice.getAppFlavor()`? Native Module khác Turbo Module ở điểm nào? |

---

## 🎯 CHUẨN BỊ CHO CHƯƠNG 8
Quét mã vạch thì hay đấy, nhưng dữ liệu trả về cần phải được Mã hóa siêu an toàn (Ví dụ thẻ tín dụng). Hơn thế nữa, một App hiện đại năm 2026 không thể thiếu Trí tuệ Nhân tạo.

Chương 8 sẽ đưa bạn lên cấp độ Cao cấp nhất: **Làm chủ mã hóa phần cứng (Hardware-backed Keystore)** để chống hacker, và **Tích hợp mô hình AI** trực tiếp vào App!

**Hai điểm nối trực tiếp từ Chương 7 sang Chương 8:**
1. **Expo Modules sẽ được cài ở Bước 1 của Sprint 8** (`npx install-expo-modules@latest`). Ngay sau đó, bạn có thể quay lại nâng cấp `src/utils/haptics.ts` (Bước 3 của Sprint 7) để dùng `expo-haptics` — rung sẽ sắc và "sang" hơn hẳn. Cũng có thể đổi `useCurrentLocation` sang `expo-location` để lấy thêm tên đường/thành phố.
2. **Kỹ năng xin quyền Runtime** vừa học ở Phần 7.5 sẽ được tái sử dụng nguyên xi cho **Sinh trắc học (Face ID / vân tay)** — Chương 8 dùng đúng mẫu ba trạng thái `checking / granted / denied` và `Linking.openSettings()` mà `ScannerScreen` đang dùng.
