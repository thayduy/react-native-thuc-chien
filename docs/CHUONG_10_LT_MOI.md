---
sidebar_position: 10
title: Chương 10
---

# GIÁO TRÌNH LÝ THUYẾT & THỰC CHIẾN
## CHƯƠNG 10: VẬN HÀNH (DEVOPS), CẬP NHẬT OTA (EAS UPDATE) VÀ BẪY LỖI (CRASHLYTICS)
**Thời lượng:** 6 tiết Lý thuyết + 5 tiết Thực hành

---

> [!IMPORTANT]
> **Thực hành chương = Sprint ShopAI cuối file.** Hoàn thành Sprint này để đạt mục tiêu chương. Hoàn thành đủ 11 chương theo `SHOPAI_HOAN_THIEN.md` = sản phẩm ShopAI **hoàn thiện đẳng cấp**.

## 📚 MỤC TIÊU HỌC TẬP

Sau khi hoàn thành chương này, học viên sẽ:
- ✅ Giải phẫu quá trình biên dịch (Compile) của React Native (Từ JSX -> AST -> Bundle -> Bytecode).
- ✅ Am hiểu **nguyên lý cốt lõi của cập nhật Over-The-Air (OTA)** — bắn bản vá JS Bundle qua mây, Bypass (lách luật hợp lệ) việc chờ App Store review — và biết dùng **EAS Update** (Expo) làm công cụ OTA hiện đại chạy thật trên ShopAI.
- ✅ Biết cách thiết lập trạm thu phát tín hiệu lỗi (Firebase Crashlytics).
- ✅ Hiểu kỹ thuật **Symbolication** (Dịch ngược mã nguồn): Cách dùng file dSYM (iOS) và ProGuard mapping (Android) để biến mã nhị phân thành code người đọc được khi lỗi văng App xảy ra.
- ✅ Tự tay **tạo Keystore** và ký (Sign) bản Release Android — hiểu vì sao mất file Keystore đồng nghĩa với mất luôn quyền cập nhật App.
- ✅ Cấu hình **ProGuard/R8** đúng cách cho dự án React Native mà không làm App crash sau khi thu nhỏ mã.
- ✅ Nắm quy trình **Archive & TestFlight** trên iOS ở mức tổng quan, kèm checklist thực chiến (Bundle ID, Certificate, Automatic Signing).
- ✅ Thiết lập **Environment Flavors** (DEV / STAGING / PROD) để một mã nguồn chạy được trên 3 môi trường khác nhau.
- ✅ Áp dụng chiến lược **Versioning** chuẩn (`versionName`/`versionCode`, `CFBundleShortVersionString`/`CFBundleVersion`).
- ✅ So sánh **EAS Build** với build Release thủ công tại máy, biết khi nào chọn cái nào, và tự chạy được `eas build --platform android/ios` thật.
- ✅ Viết **Breadcrumbs** và **Non-Fatal** có hệ thống để đọc được "câu chuyện" dẫn tới mỗi lần Crash.

---

### 0. Nhìn tổng thể trước khi đọc sâu

Chương 10 trả lời câu hỏi: *"App chạy ngon trên máy tôi rồi — giờ làm sao đưa nó đến tay người dùng thật, và khi nó nổ ở xa thì tôi biết bằng cách nào?"* Đây là bức tranh vận hành (DevOps) mà Sprint 10 sẽ dựng.

**Sơ đồ tổng quan — Chương 10 xây gì cho ShopAI:**

```
   Code của bạn                                          Người dùng thật
        │                                                        ▲
        ▼                                                        │
┌────────────────┐   build Native (Chặng 5)   ┌───────────────┐  │
│  Metro + Hermes  │ ──────────────────────────▶│ .aab / .ipa    │──┘ (nộp Store,
│  (JS → Bytecode) │                             │ (đã ký Keystore)│    review 1-7 ngày)
└────────┬─────────┘                             └───────────────┘
         │
         │  EAS Update — chỉ vá JS, vài giây, KHÔNG qua Store duyệt lại
         ▼
┌───────────────────┐        Crash / lỗi mạng        ┌────────────────────────┐
│  App đang chạy      │ ──────────────────────────────▶│ Firebase Crashlytics    │
│  trên máy người dùng│   kèm Breadcrumbs + Custom Keys │ (Dashboard giám sát)    │
└───────────────────┘                                  └────────────────────────┘
```

**Sau chương này, bạn sẽ làm được gì:**
- ✅ Giải thích được vì sao OTA chỉ vá được JS, không bao giờ vá được thay đổi ở tầng Native.
- ✅ Gắn Firebase Crashlytics vào ShopAI mà không đụng đến Navigation/Zustand/Query đang chạy ổn định.
- ✅ Tự tạo Keystore, ký bản Release Android và hiểu vì sao mất file này là mất luôn khả năng cập nhật app.
- ✅ Đẩy một bản vá lỗi qua EAS Update và biết cách rollback khẩn cấp khi bản vá đó có lỗi.
- ✅ Tách cấu hình theo 3 môi trường (development/staging/production) thay vì hardcode IP LAN.

**Lộ trình đọc gợi ý (lý thuyết → thực chiến):**
1. Đọc Phần 10.1 để hiểu đường ống biên dịch — đây là nền tảng giải thích mọi thứ ở các phần phía sau.
2. Đọc Phần 10.2–10.3 (OTA + Crashlytics) trước khi làm Phần A/C của Sprint.
3. Đọc thật kỹ Phần 10.6–10.7 (Keystore, R8) trước khi chạy lệnh `keytool` — sai một bước là mất trắng khả năng cập nhật app vĩnh viễn.
4. Đọc Phần 10.9–10.10 (Environment Flavors, Versioning) trước khi làm Bước 0 của Sprint.
5. Làm Sprint 10 theo đúng thứ tự Phần A0 → A → B → C → D → E → F, đừng nhảy cóc sang ký bản Release khi chưa xong Crashlytics.
6. Phần E (iOS) chỉ làm được nếu có máy Mac + tài khoản Apple Developer; nếu không, đọc để nắm quy trình rồi tập trung vào Phần F (EAS Build) để vẫn có một bản build hợp lệ.

> [!TIP]
> **Nhầm lẫn thường gặp nhất chương này:** học viên hay tưởng "đẩy OTA là sửa được mọi lỗi". Sai — nếu bạn vừa cài thêm một thư viện Native mới (có thư mục `android/`/`ios/`) hoặc sửa `Podfile`/`build.gradle`, OTA **bó tay hoàn toàn**, bắt buộc phải build lại và nộp Store duyệt lại từ đầu (xem lại Phần 10.1 mục 3 và Phần 10.2).

---

## ⚙️ PHẦN 10.1: GIẢI PHẪU ĐƯỜNG ỐNG BIÊN DỊCH — TỪ JSX ĐẾN BYTECODE

Trước khi App lên Store, hàng chục ngàn dòng code JavaScript/TypeScript của bạn không được gửi nguyên si lên đó. Chúng đi qua một dây chuyền 5 chặng.

### 1. Sơ đồ đường ống đầy đủ

```
┌─────────────────────────────────────────────────────────────────────┐
│  CHẶNG 1 — MÃ NGUỒN CỦA BẠN                                          │
│  src/**/*.tsx  (JSX + TypeScript + import/export ES Modules)        │
└────────────────────────────────┬────────────────────────────────────┘
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│  CHẶNG 2 — BABEL (metro-react-native-babel-preset)                  │
│  • Bóc bỏ toàn bộ Type của TypeScript (Type chỉ tồn tại lúc code)   │
│  • Dịch JSX  <View/>  →  React.createElement(View, ...)             │
│  • Hạ cấp cú pháp mới (optional chaining, async/await) cho Hermes   │
│  • Chạy các Babel Plugin: react-native-reanimated/plugin (Ch4),     │
│    module-resolver (bí danh @screens, @components — Chương 3)       │
│  Kết quả: JavaScript ES5/ES6 thuần                                  │
└────────────────────────────────┬────────────────────────────────────┘
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│  CHẶNG 3 — METRO BUNDLER                                            │
│  • Bắt đầu từ index.js, đi theo TỪNG import để dựng cây phụ thuộc   │
│  • Tree Shaking nhẹ: loại bớt module không ai import tới            │
│  • Minify (bỏ khoảng trắng, rút gọn tên biến) khi build Release     │
│  • Gom TẤT CẢ thành MỘT file duy nhất: index.android.bundle         │
│  • Gom ảnh/font vào thư mục assets                                  │
│  Kết quả: 1 file .bundle (~2-8 MB tuỳ dự án)                        │
└────────────────────────────────┬────────────────────────────────────┘
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│  CHẶNG 4 — HERMES COMPILER (hermesc)                                │
│  • Đọc file .bundle, phân tích cú pháp thành AST                    │
│  • Biên dịch Ahead-Of-Time (AOT) thành BYTECODE nhị phân (.hbc)     │
│  • Sinh kèm SOURCE MAP — "từ điển" để Symbolication (Phần 10.3)     │
│  Kết quả: index.android.bundle dạng nhị phân + index.js.map         │
└────────────────────────────────┬────────────────────────────────────┘
                                 ▼
┌─────────────────────────────────────────────────────────────────────┐
│  CHẶNG 5 — ĐÓNG GÓI NATIVE (Gradle / Xcode)                         │
│  • Biên dịch Java/Kotlin (Android) hoặc Objective-C/Swift (iOS)     │
│  • R8/ProGuard thu nhỏ + làm rối mã Java (Phần 10.6)                │
│  • Nhồi file bytecode + assets vào trong gói ứng dụng               │
│  • Ký số bằng Keystore (Android) / Provisioning Profile (iOS)       │
│  Kết quả: app-release.aab (Android) hoặc ShopAI.ipa (iOS)           │
└─────────────────────────────────────────────────────────────────────┘
```

### 2. Vì sao Hermes lại thay đổi cuộc chơi?

Các JS Engine truyền thống (JSC — JavaScriptCore) hoạt động theo kiểu **JIT (Just-In-Time)**: mỗi lần người dùng mở App, Engine mới bắt đầu đọc file JS, phân tích cú pháp, rồi mới chạy. Với một bundle 5 MB, riêng bước "đọc và phân tích" đã ngốn hàng trăm mili-giây — người dùng nhìn màn hình trắng suốt thời gian đó.

Hermes dùng **AOT (Ahead-Of-Time)**: việc phân tích cú pháp được làm **một lần duy nhất trên máy của lập trình viên lúc build**. Thiết bị của người dùng nhận về bytecode đã sẵn sàng chạy, chỉ việc nạp thẳng vào bộ nhớ.

| Tiêu chí | JSC (cũ) | Hermes |
|---|---|---|
| Thời điểm phân tích cú pháp | Mỗi lần mở App, trên máy người dùng | Một lần, lúc build, trên máy dev |
| TTI (Time To Interactive) | Chậm hơn ~2 lần | Nhanh, thường giảm 40-50% |
| Kích thước App | Lớn hơn | Nhỏ hơn đáng kể |
| RAM tiêu thụ | Cao | Thấp (thiết kế riêng cho thiết bị yếu) |
| Đọc lén được code không? | Có — bundle là JS văn bản | Khó — bytecode nhị phân |
| Debug | Chrome DevTools cũ | React Native DevTools (Chương 11) |

Từ React Native 0.70, Hermes là engine **mặc định** trên cả hai nền tảng. Kiểm tra nhanh App của bạn có đang dùng Hermes không bằng đúng một dòng:
```js
console.log('Hermes đang bật?', !!global.HermesInternal); // true nếu đang chạy Hermes
```

### 3. Hệ quả trực tiếp lên hai chủ đề của chương này

Hiểu đường ống trên giúp bạn nắm được **hai điều cốt lõi** mà cả chương này xoay quanh:

- **Vì sao OTA chỉ vá được JS (Phần 10.2):** OTA thay thế sản phẩm của **Chặng 4** (file bytecode). Nó hoàn toàn không đụng được vào **Chặng 5** (mã Native đã biên dịch). Thêm một thư viện Camera nghĩa là đổi Chặng 5 → OTA bó tay.
- **Vì sao cần Symbolication (Phần 10.3):** Chặng 3 rút gọn tên biến, Chặng 4 biến code thành nhị phân, Chặng 5 làm rối mã Java. Sau ba lớp biến đổi đó, log lỗi gửi về chỉ còn là những con số vô nghĩa. Source Map và `mapping.txt` chính là bản ghi chép của quá trình biến đổi, dùng để lần ngược trở lại.

---

## ☁️ PHẦN 10.2: CẬP NHẬT XUYÊN KHÔNG (OVER-THE-AIR - OTA)

### 1. Nỗi đau của Quy trình Release truyền thống
Khi bạn phát hiện một lỗi chính tả cực kỳ ngu ngốc làm sập màn hình thanh toán.
- **Làm App Native thuần (Swift/Kotlin):** Bạn sửa dòng code đó, nén lại thành file .ipa / .aab, tải lên App Store (Apple) và chờ đội ngũ kiểm duyệt duyệt mất từ **2 ngày đến 1 tuần**. Trong 1 tuần đó, công ty mất hàng chục tỷ doanh thu vì lỗi thanh toán.

### 2. Nguyên lý bá đạo của OTA (Over-The-Air Update)
App React Native có 2 phần: Khung xương Native (C++/Java/Swift) và Linh hồn Logic (JavaScript Bundle).
Apple quy định: Cấm thay đổi tính năng ứng dụng (Phần Native) mà không qua review. Nhưng **cho phép cập nhật các bản vá lỗi giao diện JavaScript** qua đám mây mà không cần xét duyệt lại — vì bản chất đó chỉ là "dữ liệu nội dung" (content), không phải thay đổi mã máy Native.

**Quy trình OTA hoạt động (nguyên lý chung, áp dụng cho mọi công cụ OTA):**
1. Bạn sửa lỗi chính tả ở Frontend.
2. Gõ một lệnh CLI, đẩy gói lệnh sửa lỗi (JS Bundle update) lên một Server/Đám mây trung gian.
3. Người dùng vừa mở điện thoại, App âm thầm tải file sửa lỗi từ Đám mây về. Bùm! Chớp mắt 5 giây, giao diện tự thay đổi và lỗi biến mất. Apple không hề hay biết và cũng không cấm điều này.
*(Đây là một trong những tính năng siêu việt nhất mà Native thuần không bao giờ có thể làm được).*

> [!CAUTION]
> **Lịch sử cần biết: Microsoft CodePush (App Center) đã bị khai tử vào tháng 3/2025.** Đây từng là công cụ OTA phổ biến nhất cho React Native trong nhiều năm, nhưng Microsoft đã chính thức đóng cửa toàn bộ dịch vụ App Center (bao gồm CodePush) — CLI `appcenter-cli` và các lệnh `appcenter codepush ...` **KHÔNG CÒN HOẠT ĐỘNG**. Giáo trình này chỉ nhắc đến CodePush như một **mốc lịch sử để hiểu nguyên lý OTA**, tuyệt đối KHÔNG hướng dẫn cài đặt hay chạy thật CodePush/App Center trong Sprint dưới đây. Công cụ OTA hiện đại thay thế là **EAS Update** (nếu dùng Expo modules — phù hợp với ShopAI đã có sẵn ở Chương 8) hoặc tự triển khai **`code-push-server`** mã nguồn mở (self-hosted, kiến thức nâng cao).

> [!WARNING]
> **Giới hạn OTA (áp dụng cho MỌI công cụ, không riêng CodePush):** Bạn KHÔNG THỂ dùng OTA nếu bạn cập nhật hoặc cài thêm một Native Module mới (Ví dụ cài thêm thư viện Camera ở Chương 7), hoặc đổi cấu hình `Podfile`/`build.gradle`. Vì OTA chỉ cập nhật được luồng JS, không thể cập nhật mã C++/Java/Swift đã được biên dịch sẵn trong file `.ipa`/`.aab`. Lúc này bắt buộc phải build lại và nộp bản cập nhật lên App Store/Google Play để duyệt lại từ đầu.

---

## 🐞 PHẦN 10.3: BẪY LỖI VÀ DỊCH NGƯỢC (CRASHLYTICS & SYMBOLICATION)

Khi App chạy trên máy thật, nếu Crash, nó văng một cái phụt ra ngoài màn hình chính. Người dùng không hề có "Terminal đỏ lòm" để chụp màn hình gửi cho bạn. 
Ta phải gắn **Firebase Crashlytics** vào hệ thống. Khi App Crash, nó sẽ gói báo cáo lỗi và gửi qua mạng về Dashboard cho bạn.

### Khái niệm Symbolication (Giải mã lỗi)
Báo cáo lỗi gửi về trông như thế này:
`Fatal signal 11 (SIGSEGV) at 0x0000000000000010 (code=1), thread 2555`
`0x101a1c432 <Unknown> + 144`

Bạn không thể đọc được lỗi này vì code của bạn lúc biên dịch ra Store đã bị "Làm rối" (Obfuscate) và dịch ra mã máy để chống Hacker.
**Symbolication** là quá trình ánh xạ ngược. Lúc biên dịch App, máy tính của bạn sinh ra 1 file **Từ Điển**:
- File `.dSYM` (Trên iOS).
- File `mapping.txt` của ProGuard (Trên Android).

Bạn phải ném file "Từ điển" này lên Firebase. Firebase sẽ lấy mã lỗi rác ở trên, soi vào Từ Điển và dịch ngược ra tiếng người:
`Lỗi NULL tại src/screens/HomeScreen.tsx: Dòng 145.`
Nhờ đó bạn biết chính xác vị trí Crash để sửa!

### Ba loại "Từ điển" khác nhau — đừng nhầm lẫn

Một App React Native bản Release thực chất có **ba tầng mã** bị biến đổi, mỗi tầng cần một từ điển riêng:

| Tầng | Ngôn ngữ gốc | File từ điển | Ai sinh ra nó |
|---|---|---|---|
| JavaScript | TS/JSX của bạn | `index.android.bundle.map` (Source Map) | Metro + Hermes ở Chặng 3-4 |
| Java/Kotlin (Android) | Mã Native Android | `mapping.txt` | R8/ProGuard ở Chặng 5 |
| Objective-C/Swift (iOS) | Mã Native iOS | `ShopAI.app.dSYM` | Xcode lúc Archive |

Lỗi JS (đa số lỗi bạn gặp: `undefined is not an object`) cần Source Map. Lỗi Native (`SIGSEGV`, lỗi trong thư viện Camera ở Chương 7) mới cần `mapping.txt`/`dSYM`.

### Quy trình thực tế: đẩy "Từ điển" lên Firebase

**Android — tự động hoá bằng Gradle (khuyến nghị):**

Plugin `firebase-crashlytics-gradle` (bạn sẽ khai báo ở Bước 1 của Sprint) có thể tự upload mỗi lần build. Bật trong `android/app/build.gradle`:
```groovy
android {
    buildTypes {
        release {
            minifyEnabled true
            shrinkResources true

            firebaseCrashlytics {
                mappingFileUploadEnabled true  // Tự upload mapping.txt sau mỗi lần build release
                nativeSymbolUploadEnabled false // Bật true nếu App có thư viện C++ (.so) riêng
            }
        }
    }
}
```

Nếu cần upload thủ công (VD file mapping của một bản build cũ):
```bash
cd android
./gradlew uploadCrashlyticsMappingFileRelease
```

File mapping nằm ở `android/app/build/outputs/mapping/release/mapping.txt`.

> [!CAUTION]
> **Hãy lưu trữ `mapping.txt` của MỌI bản đã phát hành.** Mỗi lần build lại, R8 sinh ra một mapping hoàn toàn khác. Nếu người dùng đang chạy bản `1.2.0` mà bạn chỉ còn giữ mapping của bản `1.3.0`, log lỗi của họ sẽ **vĩnh viễn không dịch được**. Thực tế đi làm: nén `mapping.txt` kèm số version rồi lưu vào kho artifact của CI (Chương 11).

**iOS — upload file dSYM:**

Xcode sinh `dSYM` khi Archive ở chế độ Release. Cách tự động: thêm một **Build Phase** script trong Xcode (Target ShopAI → Build Phases → New Run Script Phase), đặt **sau** phase "Copy Bundle Resources":
```bash
"${PODS_ROOT}/FirebaseCrashlytics/upload-symbols" \
  -gsp "${PROJECT_DIR}/ShopAI/GoogleService-Info.plist" \
  -p ios "${DWARF_DSYM_FOLDER_PATH}/${DWARF_DSYM_FILE_NAME}"
```

Cách thủ công khi Firebase báo "Missing dSYM":
```bash
# 1. Tải file .dSYM về từ App Store Connect (mục Activity -> chọn build -> Download dSYM)
# 2. Upload lên Firebase
./Pods/FirebaseCrashlytics/upload-symbols \
  -gsp ios/ShopAI/GoogleService-Info.plist -p ios ~/Downloads/appDsyms.zip
```

**JavaScript Source Map:** với thiết lập mặc định của `@react-native-firebase/crashlytics`, stack trace JS thường đã đọc được ở mức chấp nhận được. Khi cần chính xác tuyệt đối, sinh Source Map thủ công:
```bash
npx react-native bundle \
  --platform android --dev false \
  --entry-file index.js \
  --bundle-output /tmp/index.android.bundle \
  --sourcemap-output /tmp/index.android.bundle.map
```

> [!TIP]
> **Cách kiểm tra bạn đã làm đúng:** vào Firebase Console → Crashlytics. Nếu thấy banner vàng *"This app has unsymbolicated crashes"* hoặc stack trace toàn `<Unknown> + 144`, nghĩa là từ điển chưa lên tới nơi. Stack trace đúng phải hiện được tên file `.tsx` và số dòng.

---

## 📈 PHẦN 10.4: GIÁM SÁT HIỆU NĂNG — FIREBASE PERFORMANCE MONITORING (KHÁI NIỆM)

Crashlytics chỉ báo cho bạn biết App có **Crash** hay không, nhưng không nói cho bạn biết App có đang chạy **chậm** hay không — ví dụ Server trả dữ liệu chậm 8 giây nhưng vẫn "thành công" về mặt kỹ thuật, User vẫn phải ngồi nhìn màn hình Loading và có thể bỏ App trước khi bạn kịp phát hiện ra vấn đề. **Firebase Performance Monitoring** chính là người bạn đồng hành hiện đại của Crashlytics: tự động đo thời gian khởi động App (App Start Time), thời gian màn hình hiển thị xong (Screen Rendering), và thời gian mỗi Network Request (`fetch`/`axios` gọi vào Server NestJS ở Chương 9) mất bao lâu để hoàn thành — tất cả được đẩy lên cùng một Dashboard Firebase mà bạn đã dựng ở Phần 10.3. ShopAI trong khóa học chỉ dừng ở mức **hiểu khái niệm** (không bắt buộc cài đặt `@react-native-firebase/perf` trong Sprint 10 dưới đây), nhưng khi đi làm thực tế, đây thường là bước tiếp theo tự nhiên ngay sau khi đã tích hợp xong Crashlytics.

---

## 🍞 PHẦN 10.5: BREADCRUMBS VÀ NON-FATAL — ĐỌC ĐƯỢC "CÂU CHUYỆN" DẪN TỚI CRASH

Biết được App crash **ở đâu** mới chỉ giải quyết một nửa vấn đề. Câu hỏi khó hơn nhiều là: **người dùng đã làm gì để dẫn tới đó?**

### 1. Breadcrumbs — rắc vụn bánh mì để lần ngược đường về

Ý tưởng mượn từ truyện cổ tích: rắc vụn bánh mì dọc đường để tìm lối về. Trong lập trình, **Breadcrumb** là một dòng log ngắn ghi lại từng hành động của người dùng. Khi crash xảy ra, Crashlytics đính kèm **toàn bộ 64 dòng log gần nhất** vào báo cáo — bạn đọc được cả hành trình dẫn tới thảm hoạ.

```tsx
crashlytics().log('Mở màn hình Giỏ hàng');
crashlytics().log('Bấm Thanh toán, tổng tiền = 3.050.000');
crashlytics().log('Gọi POST /api/orders');
// 💥 CRASH tại đây
```

Đọc báo cáo, bạn hiểu ngay: crash xảy ra khi đặt hàng với giỏ có 3 món — tái hiện lại lỗi trong 30 giây thay vì đoán mò cả buổi.

**Bốn nhóm sự kiện đáng ghi Breadcrumb trong ShopAI:**

| Nhóm | Ví dụ trong ShopAI | Vì sao hữu ích |
|---|---|---|
| Điều hướng | `Điều hướng: Home → ProductDetail(backend_prod_3)` | Biết người dùng đang ở màn hình nào lúc crash |
| Gọi mạng | `API POST /api/orders → 400` | Phân biệt lỗi do Server hay do App |
| Hành động quan trọng | `Thêm vào giỏ: iPhone 15 x2` | Tái hiện đúng trạng thái dữ liệu |
| Chuyển trạng thái | `App vào background`, `Đăng xuất` | Bắt các lỗi liên quan vòng đời App |

**Nguyên tắc vàng — TUYỆT ĐỐI không log dữ liệu nhạy cảm:**
```tsx
// ❌ SAI NGHIÊM TRỌNG — vi phạm quyền riêng tư, có thể phạm luật (GDPR/Nghị định 13)
crashlytics().log(`Đăng nhập: ${email} / ${password}`);
crashlytics().log(`Token: ${token}`);

// ✅ ĐÚNG — đủ để debug, không lộ thông tin cá nhân
crashlytics().log('Đăng nhập thành công');
crashlytics().setUserId(hashedUserId); // Dùng ID đã băm, không dùng email
```

### 2. Ba mức độ ghi nhận — dùng đúng chỗ

| API | Loại | Khi nào dùng | Ảnh hưởng người dùng |
|---|---|---|---|
| `crashlytics().log(msg)` | Breadcrumb | Ghi lại mọi hành động thường ngày | Không có, chỉ đính kèm khi có crash |
| `crashlytics().recordError(err)` | **Non-Fatal** | Lỗi đã bắt được bằng `try/catch` nhưng vẫn cần theo dõi | App vẫn chạy bình thường |
| Exception không bắt được | **Fatal** | Bug thật, không lường trước | App văng ra ngoài |

**Non-Fatal là loại bị bỏ quên nhiều nhất — và cũng giá trị nhất.** Một App có thể có 0 crash nhưng vẫn mất khách hàng, vì 30% lượt đặt hàng thất bại do lỗi mạng mà không ai biết. Ba chỗ trong ShopAI nhất định phải có `recordError`:

```tsx
// 1. Fetch sản phẩm thất bại (đã làm ở Bước 4 của Sprint)
// 2. Đặt hàng thất bại — mất tiền thật, ưu tiên cao nhất (Bước 4b)
// 3. Kiểm tra bản OTA thất bại (Bước 6)
```

### 3. Custom Keys — gắn "hồ sơ bệnh án" vào mỗi báo cáo

Breadcrumb kể *câu chuyện*, Custom Key mô tả *bối cảnh* tại thời điểm crash:

```tsx
crashlytics().setAttributes({
  screen: 'CheckoutScreen',
  cart_item_count: String(totalQuantity),
  app_env: APP_ENV,                 // dev / staging / production (Phần 10.9)
  api_base_url: API_BASE_URL,       // Cực hữu ích: biết ngay app đang trỏ nhầm Server nào
});
```

Trên Dashboard Firebase, bạn có thể **lọc crash theo Custom Key** — ví dụ phát hiện "98% crash đến từ `app_env = staging`", vậy là bản Production vẫn an toàn, thở phào.

> [!TIP]
> **Chiến lược thực dụng:** đừng cố log mọi thứ ngay từ đầu (nhiễu và tốn công). Bắt đầu bằng 3 chỗ: chuyển màn hình, gọi API thất bại, và các hành động liên quan tới tiền. Khi gặp một bug khó tái hiện, hãy thêm Breadcrumb quanh khu vực nghi ngờ rồi chờ báo cáo tiếp theo.

---

## 🔑 PHẦN 10.6: KÝ SỐ BẢN RELEASE ANDROID — KEYSTORE

Đến đây bạn mới chỉ chạy `npm run android`, tức là bản **Debug**. Bản Debug được ký tự động bằng một chứng chỉ dùng chung của Android SDK — tiện cho phát triển nhưng **Google Play tuyệt đối từ chối** nhận nó.

### 1. Vì sao App bắt buộc phải được ký?

Chữ ký số của Android trả lời một câu hỏi duy nhất: *"Bản cập nhật này có đúng do tác giả ban đầu phát hành không?"*

Khi người dùng cài bản 1.1 đè lên bản 1.0, hệ điều hành so sánh chữ ký. Khớp → cho cập nhật, giữ nguyên dữ liệu. Không khớp → **từ chối cài đặt**. Cơ chế này ngăn kẻ xấu phát tán một bản ShopAI giả mạo có mã độc để đè lên App thật của bạn.

### 2. Keystore là gì?

**Keystore** là một file nhị phân (`.keystore` / `.jks`) chứa cặp khoá công khai–bí mật dùng để ký. Nó được bảo vệ bằng hai mật khẩu: mật khẩu của file (store password) và mật khẩu của khoá bên trong (key password).

> [!CAUTION]
> **ĐÂY LÀ CẢNH BÁO QUAN TRỌNG NHẤT CHƯƠNG 10.** Mất file Keystore hoặc quên mật khẩu = **bạn VĨNH VIỄN không thể cập nhật App đó trên Google Play nữa**. Không có nút "Quên mật khẩu", không có bộ phận hỗ trợ nào khôi phục được. Lựa chọn duy nhất còn lại là đăng một App hoàn toàn mới với `applicationId` khác, mất trắng toàn bộ người dùng, đánh giá và thứ hạng tìm kiếm. Đã có những công ty mất hàng triệu người dùng chỉ vì một lập trình viên nghỉ việc mang theo file này trong laptop cá nhân.

### 3. Sinh Keystore bằng `keytool`

`keytool` đi kèm sẵn với JDK (bạn đã cài từ Chương 1):

```bash
keytool -genkeypair -v \
  -storetype PKCS12 \
  -keystore shopai-release.keystore \
  -alias shopai-key-alias \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000
```

Giải nghĩa từng tham số:

| Tham số | Ý nghĩa |
|---|---|
| `-genkeypair` | Sinh một cặp khoá mới |
| `-storetype PKCS12` | Định dạng chuẩn công nghiệp hiện nay (JKS cũ đã lỗi thời) |
| `-keystore` | Tên file sẽ được tạo ra |
| `-alias` | Tên định danh của khoá bên trong file — **phải ghi nhớ**, Gradle cần nó |
| `-keyalg RSA -keysize 2048` | Thuật toán và độ dài khoá — mức Google khuyến nghị |
| `-validity 10000` | Hiệu lực ~27 năm. Google Play **yêu cầu** khoá còn hạn ít nhất tới năm 2033 |

Lệnh sẽ hỏi lần lượt: mật khẩu keystore, họ tên, đơn vị, thành phố, mã quốc gia (`VN`). Các thông tin này chỉ mang tính mô tả, không ảnh hưởng chức năng — nhưng **mật khẩu thì phải lưu cẩn thận**.

### 4. Cấu hình Gradle để dùng Keystore

Đặt file `shopai-release.keystore` vào `android/app/`. Sau đó khai báo mật khẩu — **không viết thẳng vào `build.gradle`** vì file này được commit lên Git. Cách đúng là dùng `android/gradle.properties` (đã nằm trong `.gitignore`):

```properties
# android/gradle.properties — TUYỆT ĐỐI KHÔNG COMMIT FILE NÀY
MYAPP_RELEASE_STORE_FILE=shopai-release.keystore
MYAPP_RELEASE_KEY_ALIAS=shopai-key-alias
MYAPP_RELEASE_STORE_PASSWORD=matkhau_cua_ban
MYAPP_RELEASE_KEY_PASSWORD=matkhau_cua_ban
```

Rồi trong `android/app/build.gradle`:
```groovy
android {
    signingConfigs {
        release {
            if (project.hasProperty('MYAPP_RELEASE_STORE_FILE')) {
                storeFile file(MYAPP_RELEASE_STORE_FILE)
                storePassword MYAPP_RELEASE_STORE_PASSWORD
                keyAlias MYAPP_RELEASE_KEY_ALIAS
                keyPassword MYAPP_RELEASE_KEY_PASSWORD
            }
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release  // Đổi từ signingConfigs.debug mặc định
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

### 5. Google Play App Signing — tấm lưới an toàn

Từ năm 2021, Google khuyến khích (và bắt buộc với App mới) dùng **Play App Signing**: bạn tải lên file `.aab` được ký bằng *Upload Key* của mình, Google **ký lại** bằng *App Signing Key* do chính Google giữ hộ trong hạ tầng bảo mật của họ.

Lợi ích cực lớn: nếu lỡ mất **Upload Key**, bạn có thể yêu cầu Google cấp lại — App vẫn sống. Rủi ro "mất trắng App" ở mục 2 nhờ đó giảm đi rất nhiều. Đây cũng là lý do định dạng nộp lên Play Store hiện nay là **`.aab` (Android App Bundle)** chứ không còn là `.apk`.

| Định dạng | Dùng để làm gì |
|---|---|
| `.apk` | Cài trực tiếp lên máy để test, gửi tay cho đồng nghiệp |
| `.aab` | **Định dạng bắt buộc** để nộp lên Google Play; Google tự cắt ra APK tối ưu cho từng loại máy |

Lệnh build bản release tại máy:
```bash
cd android
./gradlew assembleRelease   # -> app/build/outputs/apk/release/app-release.apk  (để test)
./gradlew bundleRelease     # -> app/build/outputs/bundle/release/app-release.aab (để nộp Store)
```

---

## 📦 PHẦN 10.7: PROGUARD / R8 — THU NHỎ VÀ LÀM RỐI MÃ ANDROID

### 1. R8 làm 4 việc

**R8** (từ Android Gradle Plugin 3.4 đã thay thế ProGuard, nhưng vẫn đọc file cấu hình cú pháp ProGuard) chạy ở Chặng 5 của đường ống:

1. **Shrinking (Thu nhỏ):** xoá các class/hàm không ai gọi tới. Riêng việc này thường giảm 20-40% kích thước phần Java.
2. **Optimization (Tối ưu):** gộp hàm, nội tuyến (inline) các hàm nhỏ.
3. **Obfuscation (Làm rối):** đổi `class ProductRepository` thành `class a`, `getUserToken()` thành `b()` — vừa nhỏ hơn vừa khó dịch ngược.
4. **Desugaring:** hạ cấp cú pháp Java mới cho máy Android đời cũ.

Bật bằng đúng hai dòng đã thấy ở Phần 10.6: `minifyEnabled true` và `shrinkResources true`.

### 2. Vì sao R8 hay làm App crash — và crash theo cách khó chịu nhất

R8 quyết định "class này không ai gọi" bằng cách đọc mã Java tĩnh. Nhưng React Native thì gọi mã Native theo kiểu **động, thông qua tên chuỗi tại thời điểm chạy** (Reflection). R8 hoàn toàn không nhìn thấy những lời gọi đó, nên nó xoá nhầm hoặc đổi tên nhầm.

Hậu quả kinh điển: **App chạy hoàn hảo ở bản Debug, nhưng crash ngay khi mở bản Release.** Đây là loại bug làm nhiều lập trình viên mới mất cả ngày, vì môi trường phát triển không bao giờ tái hiện được nó.

### 3. File `proguard-rules.pro` cho dự án React Native

Mở `android/app/proguard-rules.pro`:

```proguard
# ============ React Native lõi ============
-keep class com.facebook.react.** { *; }
-keep class com.facebook.jni.** { *; }
-keep class com.facebook.hermes.** { *; }
-dontwarn com.facebook.react.**

# Giữ mọi phương thức được gọi từ JavaScript qua Bridge/JSI
-keepclassmembers class * {
    @com.facebook.react.bridge.ReactMethod <methods>;
}
-keep @com.facebook.react.module.annotations.ReactModule class * { *; }

# ============ Hermes ============
-keep class com.facebook.hermes.unicode.** { *; }
-keep class com.facebook.jni.** { *; }

# ============ Các thư viện ShopAI đang dùng ============
# Vision Camera (Chương 7)
-keep class com.mrousavy.camera.** { *; }
# Firebase / Crashlytics (Chương 10)
-keep class com.google.firebase.** { *; }
-keepattributes SourceFile,LineNumberTable   # BẮT BUỘC để Symbolication đọc được số dòng
-keep public class * extends java.lang.Exception
# MMKV (Chương 6)
-keep class com.tencent.mmkv.** { *; }
# Reanimated (Chương 4)
-keep class com.swmansion.reanimated.** { *; }

# ============ Giữ tên lớp cho thư viện dùng Reflection ============
-keepattributes *Annotation*
-keepattributes Signature
```

> [!IMPORTANT]
> Dòng `-keepattributes SourceFile,LineNumberTable` là **bắt buộc** nếu bạn muốn Crashlytics hiển thị được số dòng. Thiếu nó, R8 xoá sạch thông tin dòng và báo cáo lỗi trở nên vô dụng — dù bạn đã upload `mapping.txt` đúng cách.

### 4. Quy tắc làm việc an toàn với R8

- **Luôn test bản Release trên máy thật trước khi nộp Store:** `npx react-native run-android --mode=release`. Đây là bước bắt buộc, không phải tuỳ chọn.
- Khi App crash ở Release nhưng chạy tốt ở Debug, nghi ngờ R8 **đầu tiên**. Cách kiểm chứng nhanh: tạm đặt `minifyEnabled false`, build lại. Hết crash → đúng là R8, giờ chỉ việc tìm class nào cần `-keep`.
- Mỗi khi cài thêm thư viện Native mới, kiểm tra tài liệu của nó xem có yêu cầu quy tắc ProGuard riêng không. Đa số thư viện lớn đã tự đóng gói sẵn quy tắc (`consumer-rules.pro`), nhưng không phải tất cả.

---

## 🍎 PHẦN 10.8: iOS ARCHIVE VÀ TESTFLIGHT (TỔNG QUAN)

Phía Apple, ba khái niệm dưới đây thay thế cho vai trò của Keystore bên Android:

| Khái niệm | Vai trò |
|---|---|
| **Certificate** (Chứng chỉ) | Chứng minh danh tính nhà phát triển. Có 2 loại: Development và Distribution |
| **App ID / Bundle Identifier** | Định danh duy nhất của App (`com.shopai.app`) — tương đương `applicationId` |
| **Provisioning Profile** | Tờ giấy phép gộp: Certificate + App ID + danh sách thiết bị được phép cài |

### Quy trình Archive → TestFlight

```
1. Xcode: chọn Scheme "ShopAI", Destination = "Any iOS Device (arm64)"
      ↓  (không chọn Simulator — Simulator không Archive được)
2. Menu Product → Archive   (mất 10-20 phút)
      ↓
3. Organizer tự mở → chọn bản Archive vừa tạo → "Distribute App"
      ↓
4. Chọn "App Store Connect" → "Upload"
      ↓
5. Xcode tự ký lại bằng Distribution Certificate, sinh .ipa và tải lên
      ↓
6. App Store Connect xử lý (15-60 phút) → build xuất hiện ở tab TestFlight
      ↓
7. Mời tester qua email → họ cài App TestFlight → tải bản build về dùng thử
```

### TestFlight — hai nhóm tester

| Nhóm | Số lượng tối đa | Cần Apple duyệt? | Dùng khi nào |
|---|---|---|---|
| **Internal Testing** | 100 người (thành viên team) | Không — có ngay sau khi xử lý xong | QA nội bộ, kiểm tra nhanh mỗi bản build |
| **External Testing** | 10.000 người | Có — Beta App Review, 1-2 ngày | Beta công khai, thu thập phản hồi thị trường |

Mỗi bản build trên TestFlight sống được **90 ngày**, sau đó tự hết hạn.

> [!NOTE]
> Toàn bộ quy trình iOS **bắt buộc** phải có máy macOS + tài khoản Apple Developer (99 USD/năm). Đây là lý do Sprint 10 không yêu cầu học viên thực hiện phần này — nhưng bạn cần nắm được sơ đồ trên, vì đây là câu hỏi phỏng vấn rất phổ biến cho vị trí Mobile Engineer.

> [!TIP]
> **Liên hệ với EAS Build (Phần 10.11):** nếu bạn dùng Windows/Linux và không có máy Mac, `eas build --platform ios` sẽ mượn máy Mac trên đám mây của Expo để làm hộ toàn bộ bước 1-5 ở trên. Bạn vẫn cần tài khoản Apple Developer, nhưng không cần mua máy Mac.

---

## 🌍 PHẦN 10.9: ENVIRONMENT FLAVORS — MỘT MÃ NGUỒN, BA MÔI TRƯỜNG

### 1. Vấn đề rất thật

Ở Chương 9, `API_BASE_URL` đang được hardcode là `http://192.168.1.15:3000`. Điều gì xảy ra khi bạn build bản Production và quên sửa dòng đó? **App phát hành cho hàng nghìn người dùng sẽ cố gọi vào IP LAN trong nhà bạn.** Không ai mua được hàng, và bạn chỉ phát hiện ra sau khi Store đã duyệt xong.

Giải pháp là tách cấu hình ra khỏi mã nguồn, chia theo ba môi trường tiêu chuẩn:

| Môi trường | Backend trỏ tới | Crashlytics | OTA | Ai dùng |
|---|---|---|---|---|
| **development** | IP LAN máy dev | Tắt | Tắt | Lập trình viên |
| **staging** | Server test trên mây | Bật (dự án riêng) | Branch `staging` | QA, khách hàng nội bộ |
| **production** | Server thật | Bật | Branch `production` | Người dùng cuối |

### 2. Hai cách triển khai

**Cách A — `react-native-config` (đầy đủ nhất):** đọc được biến môi trường ở **cả ba tầng**: JS, Android (`build.gradle`, `AndroidManifest`) và iOS (`Info.plist`). Cần thiết khi bạn muốn đổi cả tên App, icon, `applicationId` theo môi trường.

```bash
npm install react-native-config
```
Tạo `.env.production`, `.env.staging`, `.env.development` ở gốc dự án Mobile:
```
API_BASE_URL=https://api.shopai.com
APP_ENV=production
ENABLE_CRASHLYTICS=true
```
Dùng trong code:
```tsx
import Config from 'react-native-config';
console.log(Config.API_BASE_URL);
```
Chạy với môi trường cụ thể:
```bash
ENVFILE=.env.staging npx react-native run-android
```

**Cách B — file hằng số TypeScript thuần (đơn giản, không cần cài gì):** đủ dùng cho ShopAI và là cách Sprint 10 sẽ áp dụng. Ưu điểm: không đụng vào tầng Native, không rủi ro build lỗi giữa buổi học, lại có đầy đủ gợi ý kiểu từ TypeScript.

### 3. Cạm bẫy bảo mật cần nhớ

> [!CAUTION]
> **Mọi giá trị trong `.env` phía Mobile đều nằm bên trong file APK/IPA và có thể bị đọc.** `react-native-config` chỉ giúp *quản lý* cấu hình, nó **không mã hoá** gì cả. Dịch ngược APK là thấy hết. Vì vậy: URL Server, tên môi trường, cờ bật/tắt tính năng → được phép để. API Key, mật khẩu, chuỗi bí mật → **tuyệt đối không**, phải nằm ở Backend (đúng bài học Chương 8-9).

---

## 🔢 PHẦN 10.10: CHIẾN LƯỢC ĐÁNH SỐ PHIÊN BẢN (VERSIONING)

Mỗi bản phát hành mang **hai con số hoàn toàn khác nhau về mục đích**, và nhầm lẫn giữa chúng là lỗi phổ biến của người mới.

| Nền tảng | Số cho NGƯỜI ĐỌC | Số cho MÁY ĐỌC |
|---|---|---|
| Android | `versionName` = `"1.2.0"` | `versionCode` = `10200` |
| iOS | `CFBundleShortVersionString` = `"1.2.0"` | `CFBundleVersion` = `"10200"` |

- **Số cho người đọc** hiện trên trang Store và trong màn hình "Giới thiệu" của App. Nó theo chuẩn **Semantic Versioning** `MAJOR.MINOR.PATCH`:
  - `MAJOR` (1.x.x): thay đổi lớn, phá vỡ tương thích — VD đổi toàn bộ giao diện.
  - `MINOR` (x.2.x): thêm tính năng mới — VD thêm màn hình Chatbot AI.
  - `PATCH` (x.x.3): chỉ sửa lỗi.
- **Số cho máy đọc** là số nguyên, dùng để so sánh "bản nào mới hơn". Nó **bắt buộc phải tăng nghiêm ngặt** ở mỗi lần tải lên Store, kể cả khi bạn chỉ sửa một dấu chấm. Nộp lại cùng một `versionCode` sẽ bị Google Play từ chối thẳng.

### Công thức sinh `versionCode` tự động

Đừng tự tăng tay — rất dễ quên hoặc trùng. Hãy suy ra từ `versionName`:

```
versionCode = MAJOR × 10000 + MINOR × 100 + PATCH
```

| versionName | versionCode |
|---|---|
| 1.0.0 | 10000 |
| 1.2.0 | 10200 |
| 1.2.15 | 10215 |
| 2.0.0 | 20000 |

Công thức này đảm bảo số luôn tăng, dễ đọc ngược, và không bao giờ trùng.

Áp dụng trong `android/app/build.gradle`:
```groovy
def versionMajor = 1
def versionMinor = 2
def versionPatch = 0

android {
    defaultConfig {
        applicationId "com.shopai.app"
        versionName "${versionMajor}.${versionMinor}.${versionPatch}"
        versionCode versionMajor * 10000 + versionMinor * 100 + versionPatch
    }
}
```

### Versioning và OTA — mối quan hệ dễ gây tai nạn

> [!WARNING]
> Bản vá OTA (Phần 10.2) **không** làm thay đổi `versionName`/`versionCode` — vì đó là thông tin nằm trong gói Native đã cài trên máy. Hệ quả: người dùng có thể đang chạy code JS của bản `1.2.3` trong khi màn hình "Giới thiệu" vẫn ghi `1.2.0`. Cách xử lý chuyên nghiệp là hiển thị thêm mã bản OTA lấy từ `Updates.updateId`, ví dụ `ShopAI v1.2.0 (OTA a1b2c3)` — nhờ vậy khi người dùng báo lỗi, bạn biết chính xác họ đang chạy tổ hợp nào.

---

## ⚖️ PHẦN 10.11: EAS BUILD SO VỚI BUILD RELEASE TẠI MÁY

**EAS Build** là dịch vụ build trên đám mây của Expo: bạn đẩy mã nguồn lên, máy chủ của Expo (bao gồm cả máy macOS cho iOS) biên dịch hộ rồi trả về file `.aab`/`.ipa`.

| Tiêu chí | **Build tại máy** | **EAS Build (đám mây)** |
|---|---|---|
| Cần máy Mac để build iOS | Bắt buộc | Không — Expo cho mượn máy Mac |
| Thời gian cài đặt ban đầu | Vài giờ (Android Studio, Xcode, JDK, CocoaPods) | ~10 phút (`npm i -g eas-cli`) |
| Thời gian mỗi lần build | 3-10 phút | 10-25 phút (gồm thời gian xếp hàng chờ) |
| Chi phí | Miễn phí (nhưng tốn điện, tốn máy) | Có gói miễn phí giới hạn; trả phí khi build nhiều |
| Quản lý chứng chỉ/Keystore | Bạn tự lo, tự sao lưu | EAS giữ hộ và tự động hoá |
| Môi trường build | Máy bạn — "trên máy tôi chạy được" | Sạch và giống hệt nhau mỗi lần |
| Phù hợp cho | Học tập, lặp nhanh, công ty có hạ tầng CI riêng | Đội nhỏ, không có máy Mac, muốn CI/CD ngay |
| Chạy được khi không có mạng | Có | Không |

**Nguyên tắc chọn:**
- Đang **học và lặp nhanh** → build tại máy (`./gradlew assembleRelease`), phản hồi nhanh nhất.
- Không có máy Mac nhưng **cần bản iOS** → EAS Build, gần như là lựa chọn duy nhất hợp lý.
- Công ty đã có **CI riêng** (Chương 11) → build tại máy chạy trên runner của CI, chủ động và không phụ thuộc bên thứ ba.

> [!TIP]
> Đừng nhầm hai dịch vụ cùng họ: **EAS Build** đóng gói lại **phần Native** (Chặng 5 — chậm, phải nộp Store lại). **EAS Update** chỉ bắn **bundle JS** (Chặng 4 — vài giây, không cần Store duyệt). Sprint 10 dưới đây dùng **EAS Update**; EAS Build là kiến thức để bạn biết lựa chọn khi đi làm.

---

---

## 🐳 PHẦN 10.12: DOCKER VÀ SENTRY - DEVOPS CHO BACKEND

Khi dự án đưa lên môi trường Production, việc chạy `npm run start` trên server là tối kỵ. Mọi thứ phải được container hóa và giám sát tự động.

### 1. Docker & Docker Compose
- **Docker:** Đóng gói toàn bộ mã nguồn Backend (NestJS), thư viện (node_modules), và môi trường (Node.js) vào một "cục" gọi là Container. Chạy ở máy nào cũng giống nhau, chấm dứt câu nói "Ở máy em chạy được mà".
- **Docker Compose:** Kịch bản để chạy nhiều Container cùng lúc. Ở ShopAI, chúng ta cần: 1 Container cho NestJS, 1 Container cho PostgreSQL (Database), 1 Container cho Redis (Cache). Tất cả chạy chung một mạng nội bộ ảo, không cần cài đặt rườm rà.

### 2. Sentry (Performance & Error Tracking)
Crashlytics chuyên dùng cho Mobile (Frontend). Ở Backend, khi một API lỗi 500, ta cần biết ngay dòng code nào gây ra lỗi.
- **Sentry:** Nền tảng chuyên bắt lỗi cho Backend và Web.
- **Tích hợp:** Ở NestJS, tạo một toàn cục `AllExceptionsFilter` (đã học ở Chương 9) và ném đối tượng `error` sang `Sentry.captureException()`. Khi có người đặt hàng lỗi, bạn sẽ nhận được tin nhắn trên Slack/Email kèm theo dòng code gây lỗi.

---

## 🚀 THỰC CHIẾN SHOPAI (SPRINT 10: FIREBASE CRASHLYTICS & OTA VỚI EAS UPDATE)

**User Story:** *"Là một Quản lý Dự án, tôi muốn tự động bắt mọi lỗi văng App (Crash) của người dùng ở Production, gửi về hệ thống giám sát trung tâm, và có khả năng vá lỗi giao diện tức thời qua mây (OTA) — mà KHÔNG được đụng vào, xóa bỏ hay làm gián đoạn bất kỳ tính năng nào (Navigation, Zustand, React Query) đang chạy ổn định của ShopAI."*

> [!WARNING]
> **Nguyên tắc bất biến của Sprint này:** Ta chỉ **THÊM** (Add), không **XÓA** (Delete). `App.tsx` hiện tại đang có cấu trúc `SafeAreaProvider` > `QueryClientProvider` > `NavigationContainer` > `AuthStack` / `MainTabNavigator` (Zustand). Toàn bộ cấu trúc này phải được giữ nguyên 100% sau Sprint 10.


### 📋 Khung thực hành chương (đọc trước khi gõ code)

> Đây là **bài thực hành của Chương 10** (không phải “lab mỗi ngày”). Làm hết Sprint này = đạt mục tiêu chương. Hoàn thành đủ 11 Sprint = sản phẩm ShopAI theo `SHOPAI_HOAN_THIEN.md`.

| Hạng mục | Nội dung |
|----------|----------|
| **Thời lượng gợi ý** | 5–8 tiết (phụ thuộc Firebase/Apple) |
| **Độ khó chương** | ★★★★☆ |
| **Đầu vào bắt buộc** | Sprint 9 PASS — luồng mua hàng + AI qua Nest ổn. |
| **Đầu ra sản phẩm** | Crashlytics ghi crash/non-fatal; EAS Update cấu hình; ít nhất 1 đường build Release (local hoặc EAS). |
| **Cách làm** | Làm **tuần tự từng Bước**. Gặp mốc ✓ bên dưới mà FAIL → dừng, sửa, rồi mới sang bước sau. |
| **Nghiệm thu cuối khóa** | Đối chiếu `SHOPAI_HOAN_THIEN.md` — mỗi Sprint chỉ tích thêm ô, không phá tính năng cũ. |

### ✓ Kiểm chứng theo mốc (trong lúc làm)

- **Sau Bước 1–4b:** Test crash lên Firebase; lỗi fetch/checkout có recordError.
- **Sau Bước 7–8 hoặc 14–15:** eas.json đủ profile; có minh chứng Update hoặc build preview.

> [!TIP]
> Xong Sprint 10, mở `SHOPAI_HOAN_THIEN.md` và tick các ô thuộc chương này. Mục tiêu cuối khóa: **mọi ô A/B/C/D (+ E đề cương) đều xanh** trong `SHOPAI_HOAN_THIEN.md` — đó mới là ShopAI hoàn thiện đẳng cấp.

### Yêu cầu Nghiệm thu (Acceptance Criteria):
1. Firebase Crashlytics được tích hợp vào App ShopAI hiện có, không xóa bất kỳ màn hình, Store hay Provider nào.
2. Có một cơ chế test crash AN TOÀN (ẩn, chỉ chạy ở `__DEV__`), không phải là màn hình thay thế toàn bộ App.
3. Khi `HomeScreen` fetch dữ liệu thất bại, lỗi phải được ghi nhận về Firebase qua `crashlytics().recordError()` — dạng lỗi **Non-Fatal** (không làm sập App, người dùng vẫn thấy UI lỗi bình thường).
4. Hiểu được quy trình đẩy 1 bản vá JS qua **EAS Update** (khuyến nghị chính — ShopAI có sẵn Expo modules từ Chương 8) hoặc `code-push-server` tự triển khai (nâng cao), và nắm rõ giới hạn: OTA không bao giờ vá được thay đổi ở tầng Native. **Không** dùng Microsoft App Center/CodePush vì dịch vụ này đã ngừng hoạt động từ 3/2025.
5. Có file `src/constants/env.ts` khai báo `APP_ENV` (dev/staging/production) và `API_BASE_URL` suy ra theo môi trường — chấm dứt việc hardcode IP LAN của Chương 9 vào bản Production.
6. `CheckoutScreen` (Chương 9) ghi nhận `recordError` kèm Breadcrumb khi `POST /api/orders` thất bại — lỗi liên quan tới **tiền** phải được giám sát chặt nhất.
7. Tạo được **Keystore release Android** và cấu hình Gradle ký bản Release (không commit mật khẩu lên Git).
8. Có file `eas.json` với đủ 3 profile `development` / `preview` / `production`.

---

### PHẦN A0: Dựng hằng số môi trường `APP_ENV` (làm trước tiên)

Trước khi gắn bất cứ công cụ giám sát nào, ta phải trả lời được câu hỏi: *"App này đang chạy ở môi trường nào?"* — vì Crashlytics, OTA và địa chỉ Server đều phụ thuộc vào câu trả lời đó.

#### Bước 0: Tạo `src/constants/env.ts`

Áp dụng **Cách B** ở Phần 10.9 — file hằng số TypeScript thuần, không cần cài thư viện Native nào:

```ts
// src/constants/env.ts
export type AppEnv = 'development' | 'staging' | 'production';

// __DEV__ là biến toàn cục của React Native: true khi chạy qua Metro, false ở bản build Release.
// Nhờ nó, chỉ một dòng này đã tự phân biệt được máy dev với máy người dùng thật.
export const APP_ENV: AppEnv = __DEV__ ? 'development' : 'production';

// Bảng địa chỉ Server cho từng môi trường — thay cho việc hardcode IP LAN ở Chương 9
const API_URLS: Record<AppEnv, string> = {
  // Đổi IP LAN này khi bạn đổi mạng Wifi (xem lại bẫy Localhost ở Chương 9, Phần 9.4)
  development: 'http://192.168.1.15:3000',
  staging: 'https://staging-api.shopai.com',
  production: 'https://api.shopai.com',
};

export const API_BASE_URL = API_URLS[APP_ENV];

// Cờ bật/tắt tính năng theo môi trường — tránh làm nhiễu dữ liệu thật bằng log lúc đang code
export const ENABLE_CRASHLYTICS = APP_ENV !== 'development';
export const ENABLE_OTA_UPDATE = APP_ENV !== 'development';

// Hiển thị ở màn hình Giới thiệu / góc dưới HomeScreen (xem Phần 10.10)
export const APP_VERSION = '1.0.0';
```

Sau đó cập nhật `src/constants/api.ts` (file đã tạo ở Chương 9) để **không còn hai nguồn sự thật**:
```ts
// src/constants/api.ts — giờ chỉ đóng vai trò tái xuất, mọi cấu hình về env.ts
export { API_BASE_URL } from './env';
```

> [!TIP]
> Nhờ cách tái xuất này, **mọi file đang `import { API_BASE_URL } from '@constants/api'` ở Chương 9 đều không cần sửa một dòng nào** — `HomeScreen`, `AIChatScreen`, `ProductDetailScreen`, `CheckoutScreen` chạy y nguyên, nhưng từ giờ tự động trỏ đúng Server theo môi trường. Đây chính là lợi ích thực tế của nguyên tắc "một nguồn sự thật" đã nhấn mạnh ở Chương 9.

> [!WARNING]
> Nhắc lại cảnh báo ở Phần 10.9: file này nằm trong bundle JS và **hoàn toàn có thể bị đọc** sau khi dịch ngược APK. Chỉ được để URL, tên môi trường, cờ bật/tắt. Gemini API Key vẫn phải nằm trong `.env` của NestJS như Chương 9 đã làm.

---

### PHẦN A: Tích hợp Firebase Crashlytics (không đụng Navigation/Zustand/Query)

*(Lưu ý: Để Firebase Crashlytics hoạt động, bạn bắt buộc phải có tài khoản Google Firebase và tải file `google-services.json`/`GoogleService-Info.plist` dán vào lõi Android/iOS. Quá trình này đòi hỏi thao tác trên Web Firebase khá nhiều).*

#### Bước 1: Tạo dự án Firebase và Cài đặt lõi
1. Vào `console.firebase.google.com` tạo dự án `ShopAI`.
2. Tải `google-services.json` bỏ vào thư mục `android/app/`.
3. Tải `GoogleService-Info.plist` bỏ vào thư mục `ios/ShopAI/`.

Chạy lệnh cài đặt thư viện:
```bash
npm install @react-native-firebase/app @react-native-firebase/crashlytics
# Bắt buộc Link Code iOS
cd ios && pod install && cd ..
```

> [!IMPORTANT]
> **Bước bắt buộc riêng cho Android — khai báo 2 Gradle Plugin, thiếu là Build lỗi ngay:** `@react-native-firebase` trên Android không tự hoạt động chỉ bằng `npm install`, bạn phải khai báo thêm plugin Gradle ở 2 file cấu hình:
>
> Trong `android/build.gradle` (cấp gốc dự án Android), thêm vào `dependencies` của khối `buildscript`:
> ```groovy
> buildscript {
>   dependencies {
>     classpath 'com.google.gms:google-services:4.4.2'        // Đọc file google-services.json
>     classpath 'com.google.firebase:firebase-crashlytics-gradle:3.0.2' // Sinh mapping.txt cho Symbolication
>   }
> }
> ```
>
> Trong `android/app/build.gradle` (file cấp app), thêm 2 dòng `apply plugin` — đặt ngay **đầu file**, sau dòng `apply plugin: "com.facebook.react"`:
> ```groovy
> apply plugin: 'com.google.gms.google-services'
> apply plugin: 'com.google.firebase.firebase-crashlytics'
> ```
> Thiếu 2 dòng `apply plugin` này, App vẫn build được nhưng Crashlytics sẽ **KHÔNG BAO GIỜ** gửi được báo cáo lỗi về Dashboard — một lỗi cấu hình rất phổ biến và khó nhận ra vì không có thông báo lỗi rõ ràng lúc build.

**Cấu hình chi tiết cho từng Build Type** — vẫn trong `android/app/build.gradle`, bổ sung khối `firebaseCrashlytics` vào `buildTypes` (áp dụng đúng lý thuyết Symbolication ở Phần 10.3):

```groovy
android {
    buildTypes {
        debug {
            // Tắt Crashlytics ở bản Debug: tránh làm nhiễu Dashboard bằng những lần
            // crash cố ý lúc đang code. Đồng bộ với cờ ENABLE_CRASHLYTICS ở Bước 0.
            firebaseCrashlytics {
                mappingFileUploadEnabled false
            }
        }
        release {
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'

            firebaseCrashlytics {
                mappingFileUploadEnabled true   // Tự upload mapping.txt mỗi lần build release
                nativeSymbolUploadEnabled false // Chỉ cần true khi App có thư viện C++ (.so) riêng
            }
        }
    }
}
```

Đồng thời mở `android/app/proguard-rules.pro`, thêm quy tắc tối thiểu cho Crashlytics (Phần 10.7):
```proguard
-keepattributes SourceFile,LineNumberTable   # Không có dòng này, báo cáo lỗi sẽ MẤT số dòng
-keep public class * extends java.lang.Exception
-keep class com.google.firebase.** { *; }
```

> [!TIP]
> **Cách kiểm chứng plugin đã ăn:** chạy `cd android && ./gradlew :app:dependencies | grep crashlytics`. Nếu thấy các dòng `com.google.firebase:firebase-crashlytics`, plugin đã được nạp đúng. Nếu không thấy gì, kiểm tra lại thứ tự `apply plugin` — nó phải nằm **sau** plugin React Native.

#### Bước 2: Khởi tạo Crashlytics ở `App.tsx` — CHỈ THÊM, KHÔNG XÓA
Mở lại `App.tsx` (đang có `SafeAreaProvider` / `QueryClientProvider` / `AuthStack` / `MainTabNavigator`). **Chỉ thêm** import Crashlytics + `useEffect` ghi log — giữ nguyên 100% Navigation:

```tsx
import React, { useEffect } from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import crashlytics from '@react-native-firebase/crashlytics'; // ➕ MỚI
import LoginScreen from '@screens/LoginScreen';
import MainTabNavigator from '@navigation/MainTabNavigator';
import { useAuthStore } from '@store/useAuthStore';

const AuthStack = createNativeStackNavigator();
const queryClient = new QueryClient({
  defaultOptions: { queries: { staleTime: 1000 * 60 * 5, retry: 2 } },
});

function App(): React.JSX.Element {
  const token = useAuthStore(state => state.token);

  // ➕ MỚI: Ghi log khởi động — không ảnh hưởng UI/Navigation
  useEffect(() => {
    crashlytics().log('App ShopAI đã khởi động.');
  }, []);

  return (
    <SafeAreaProvider>
      <QueryClientProvider client={queryClient}>
        <NavigationContainer>
          {token == null ? (
            <AuthStack.Navigator screenOptions={{ headerShown: false }}>
              <AuthStack.Screen name="Login" component={LoginScreen} />
            </AuthStack.Navigator>
          ) : (
            <MainTabNavigator />
          )}
        </NavigationContainer>
      </QueryClientProvider>
    </SafeAreaProvider>
  );
}

export default App;
```

#### Bước 3: Gắn nút test Crash ẨN vào `HomeScreen` (chỉ chạy khi `__DEV__`)
Thay vì đập bỏ cả App để làm màn hình test Crash riêng, ta gắn một dòng chữ phiên bản ở cuối `HomeScreen` — Nhấn giữ (Long Press) 2 giây vào đó mới gây Crash. Biến toàn cục `__DEV__` của React Native đảm bảo đoạn code này **tự động biến mất khi Build bản Production** đưa lên Store, tránh User thật vô tình bấm trúng.

Mở `src/screens/HomeScreen.tsx`, thêm import và 1 đoạn JSX nhỏ vào cuối `container`:
```tsx
import { Pressable } from 'react-native'; // ➕ Thêm Pressable vào import react-native có sẵn
import crashlytics from '@react-native-firebase/crashlytics'; // ➕ MỚI

// ...bên trong return, đặt ngay dưới FlatList, vẫn trong <View style={styles.container}>
{__DEV__ && (
  <Pressable
    onLongPress={() => {
      crashlytics().log('Dev nhấn giữ vào version text để test crash...');
      crashlytics().setUserId('dev_tester_999');
      crashlytics().crash(); // Chỉ chạy được vì __DEV__ === true
    }}
    style={{ padding: 8 }}
  >
    <Text style={{ textAlign: 'center', fontSize: 10, color: '#ccc' }}>
      ShopAI v1.0.0 (Dev: nhấn giữ 2s để test Crashlytics)
    </Text>
  </Pressable>
)}
```

> [!TIP]
> Chữ nhỏ xíu, màu xám mờ, chỉ hiện khi `__DEV__` — người dùng thật trên Store sẽ không bao giờ thấy hoặc bấm trúng dòng này. Đây là cách các đội DevOps chuyên nghiệp cài "cửa sau" gỡ lỗi an toàn.

---

### PHẦN B: Ghi log lỗi Non-Fatal (không làm sập App)

#### Bước 4: Bọc `fetchProductsAPI` bằng try/catch + `recordError`
Vẫn ở `HomeScreen.tsx`, hàm `fetchProductsAPI` (đã nối vào Server NestJS thật từ Chương 9) hiện chỉ ném lỗi (`throw`) cho React Query tự xử lý UI, nhưng ta **không hề biết** lỗi đó xảy ra ngoài đời thực với ai, khi nào. Bổ sung `crashlytics().recordError()` để gửi báo cáo lỗi KHÔNG-Crash về Firebase:

```tsx
import { API_BASE_URL } from '@constants/api'; // Dùng đúng hằng số IP LAN đã tạo ở Chương 9 — KHÔNG hardcode lại IP ở đây
import { Product, ProductListSchema } from '@types/product.schema'; // Vẫn giữ nguyên trạm kiểm soát Zod từ Chương 6/9

const API_URL = `${API_BASE_URL}/api/products`;

const fetchProductsAPI = async (): Promise<Product[]> => {
  try {
    const response = await fetch(API_URL);
    if (!response.ok) {
      throw new Error('Lỗi mạng từ Server NestJS');
    }
    const rawData = await response.json();
    const result = ProductListSchema.safeParse(rawData);
    if (!result.success) {
      throw new Error('Dữ liệu sản phẩm từ Server không hợp lệ (Zod validation failed)!');
    }
    return result.data;
  } catch (error) {
    // ➕ MỚI: Ghi lại lỗi Non-Fatal — App KHÔNG sập, nhưng Firebase vẫn nhận được báo cáo
    crashlytics().recordError(error as Error);
    throw error; // Ném lại để React Query biết Query lỗi (isError = true), UI vẫn hiển thị thông báo cho user
  }
};
```

> [!TIP]
> Đổi `API_URL` thành hardcode như bản cũ là một bước lùi — hãy luôn tái sử dụng `API_BASE_URL` từ `src/constants/api.ts` (Chương 9) làm nguồn sự thật duy nhất cho địa chỉ Server, dù bạn gọi bằng `fetch` thuần hay `axiosClient`.

> [!TIP]
> **Phân biệt 2 loại báo cáo:** `crashlytics().crash()` (Bước 3) mô phỏng lỗi **Fatal** — App văng thật. `crashlytics().recordError()` (Bước 4) là lỗi **Non-Fatal** — App vẫn sống, chỉ ghi nhận "có gì đó bất thường xảy ra" để bạn theo dõi xu hướng lỗi mạng, lỗi Server theo thời gian trên Dashboard.

#### Bước 4b: Giám sát lỗi ĐẶT HÀNG ở `CheckoutScreen` — ưu tiên cao nhất

Lỗi tải danh sách sản phẩm gây khó chịu. Lỗi **đặt hàng** gây mất tiền. Đây là chỗ trong ShopAI cần giám sát chặt nhất, nhưng lại hay bị bỏ quên vì `try/catch` ở đó "trông có vẻ đã xử lý xong rồi".

Mở `src/screens/CheckoutScreen.tsx` (bản đã nối API thật ở Chương 9, Bước 9c), bổ sung Breadcrumb + Custom Keys + `recordError` theo đúng lý thuyết Phần 10.5:

```tsx
import crashlytics from '@react-native-firebase/crashlytics'; // ➕ MỚI
import { APP_ENV, API_BASE_URL } from '@constants/env';       // ➕ MỚI (Bước 0)

const handleConfirm = async () => {
  setIsPlacing(true);
  setErrorMessage(null);

  // ➕ Breadcrumb: rắc vụn bánh mì TRƯỚC khi làm việc nguy hiểm
  crashlytics().log(`Checkout: bắt đầu đặt hàng, ${items.length} loại sản phẩm`);

  // ➕ Custom Keys: gắn bối cảnh vào MỌI báo cáo phát sinh từ đây trở đi
  crashlytics().setAttributes({
    screen: 'CheckoutScreen',
    cart_item_count: String(items.length),
    cart_total: String(totalPrice),
    app_env: APP_ENV,
    api_base_url: API_BASE_URL, // Cực giá trị: phát hiện ngay App bản Store trỏ nhầm IP LAN
  });

  try {
    const order = await placeOrderAPI(items, totalPrice);

    crashlytics().log(`Checkout: đặt hàng THÀNH CÔNG, orderId = ${order.orderId}`);
    setOrderId(order.orderId);
    setIsDone(true);
    clearCart();
    setTimeout(() => navigation.goBack(), 1500);
  } catch (error) {
    const err = error as Error;

    // ➕ Ghi nhận Non-Fatal: App không sập, người dùng vẫn thấy thông báo lịch sự,
    //    nhưng đội kỹ thuật biết ngay có bao nhiêu đơn hàng đang thất bại ngoài đời thực.
    crashlytics().log(`Checkout: đặt hàng THẤT BẠI - ${err.message}`);
    crashlytics().recordError(err, 'CheckoutOrderFailed'); // Tham số 2: đặt tên nhóm lỗi cho dễ lọc

    setErrorMessage(err.message);
  } finally {
    setIsPlacing(false);
  }
};
```

> [!IMPORTANT]
> Tham số thứ hai của `recordError(error, jsErrorName)` đặt tên cho nhóm lỗi trên Dashboard. Không có nó, mọi lỗi mạng của cả App bị gộp chung vào một dòng `Error` khổng lồ, không phân biệt được lỗi tải sản phẩm với lỗi đặt hàng. Đặt tên rõ ràng (`CheckoutOrderFailed`, `ProductFetchFailed`) giúp bạn ưu tiên đúng việc cần sửa trước.

> [!TIP]
> **Cách test nhanh:** tắt Server NestJS (Chương 9), thêm sản phẩm vào giỏ rồi bấm "Xác nhận đặt hàng". App phải hiện lỗi đỏ, **giỏ hàng còn nguyên**, và vài phút sau Dashboard Crashlytics xuất hiện một Non-Fatal tên `CheckoutOrderFailed` — mở ra sẽ thấy đủ chuỗi Breadcrumb dẫn tới nó cùng các Custom Key về giỏ hàng.

---

### PHẦN C: Cập nhật xuyên không với OTA — EAS Update (khuyến nghị) hoặc `code-push-server` tự lưu trữ (nâng cao)

> [!CAUTION]
> **Không dùng Microsoft CodePush/App Center — dịch vụ đã CHÍNH THỨC ĐÓNG CỬA từ tháng 3/2025.** Trước đây giáo trình này (và rất nhiều tài liệu React Native cũ trên mạng) dạy `appcenter-cli` + `react-native-code-push`, nhưng lệnh `appcenter codepush release-react ...` giờ sẽ **báo lỗi kết nối/tài khoản** vì backend không còn tồn tại. Đừng cài `appcenter-cli` hay chạy các lệnh đó trong lớp học — chỉ nên biết CodePush là **mốc lịch sử** đã khai sinh ra khái niệm OTA cho React Native.
>
> **Hai lối đi thay thế thật, chọn 1 phù hợp với ShopAI:**
> - **EAS Update (khuyến nghị chính):** Dịch vụ OTA chính chủ của Expo. Vì ShopAI đã cài một số **Expo Module** từ Chương 8 (VD các thư viện `expo-*`), tích hợp EAS Update là lựa chọn tự nhiên, ít cấu hình nhất, có Dashboard theo dõi bản update giống Firebase.
> - **`code-push-server` tự triển khai (nâng cao):** Bản mã nguồn mở tương thích ngược với thư viện Client `react-native-code-push` (Client giữ nguyên, chỉ đổi Server đích). Phù hợp nếu công ty muốn tự lưu trữ (self-hosted) toàn bộ hạ tầng OTA, không phụ thuộc Expo. Đòi hỏi tự dựng và vận hành 1 Server Node.js riêng — không bắt buộc chạy trong lớp học, chỉ cần hiểu nguyên lý.

#### Bước 5: Cài đặt `expo-updates` (lối đi EAS Update)
```bash
npx expo install expo-updates
```
*(`expo-updates` là thư viện Client OTA của Expo — vẫn cài được trên dự án React Native CLI thường, không buộc phải chuyển hẳn sang Expo Managed Workflow, miễn là bạn đã có sẵn native module Expo từ Chương 8).*

#### Bước 6: Bật kiểm tra bản mới ở `App.tsx` — CHỈ THÊM `useEffect`, không đổi cấu trúc cũ
Khác với CodePush (cần bọc HOC ở dòng export), `expo-updates` chỉ cần 1 `useEffect` gọi API kiểm tra bản mới — không đụng đến cấu trúc `SafeAreaProvider`/`QueryClientProvider`/`NavigationContainer` đã có từ Bước 2:

```tsx
import * as Updates from 'expo-updates'; // ➕ MỚI

function App(): React.JSX.Element {
  const token = useAuthStore(state => state.token);

  useEffect(() => {
    crashlytics().log('App ShopAI đã khởi động.');
  }, []);

  // ➕ MỚI: Kiểm tra bản vá OTA mỗi khi App khởi động — không ảnh hưởng Navigation/Zustand/Query
  useEffect(() => {
    async function checkForUpdate() {
      if (__DEV__) return; // Không kiểm tra update khi đang chạy Dev — tránh nhiễu lúc code
      try {
        const update = await Updates.checkForUpdateAsync();
        if (update.isAvailable) {
          await Updates.fetchUpdateAsync();
          await Updates.reloadAsync(); // Tải xong, khởi động lại App ngay với bản mới
        }
      } catch (error) {
        crashlytics().recordError(error as Error); // Lỗi kiểm tra update cũng là Non-Fatal — ghi nhận về Firebase
      }
    }
    checkForUpdate();
  }, []);

  return (
    // ...toàn bộ JSX giữ nguyên 100% như Bước 2...
  );
}

export default App; // Không cần HOC bọc export như CodePush — export như bình thường
```

> [!NOTE]
> **Nếu chọn lối đi nâng cao `code-push-server` tự lưu trữ:** Cấu trúc `App.tsx` sẽ quay lại đúng dạng HOC như CodePush cũ (`import codePush from 'react-native-code-push'; export default codePush(options)(App);`), chỉ khác duy nhất ở Bước 7 là bạn tự cấu hình `serverUrl` của thư viện Client trỏ về địa chỉ Server `code-push-server` tự triển khai, thay vì trỏ về `api.appcenter.ms` (nay đã chết, dịch vụ App Center ngừng hoạt động 3/2025).

#### Bước 7: Thiết lập EAS đầy đủ và đẩy bản vá JS lên mây

**7.1. Cài EAS CLI và đăng nhập:**
```bash
npm install -g eas-cli
eas login          # Cần tài khoản Expo miễn phí, đăng ký tại expo.dev
eas whoami         # Kiểm tra đã đăng nhập đúng tài khoản
```

**7.2. Khởi tạo dự án EAS** — lệnh này sinh ra một `projectId` và ghi vào `app.json`:
```bash
eas init
```

**7.3. Cấu hình EAS Update:**
```bash
eas update:configure
```

**7.4. Viết `eas.json`** ở gốc dự án Mobile. Đây là file mô tả **các profile build/update**, ánh xạ đúng ba môi trường đã định nghĩa ở Bước 0:

```json
{
  "cli": {
    "version": ">= 5.9.0",
    "appVersionSource": "remote"
  },
  "build": {
    "development": {
      "developmentClient": true,
      "distribution": "internal",
      "channel": "development",
      "android": { "buildType": "apk" },
      "env": { "APP_ENV": "development" }
    },
    "preview": {
      "distribution": "internal",
      "channel": "staging",
      "android": { "buildType": "apk" },
      "env": { "APP_ENV": "staging" }
    },
    "production": {
      "channel": "production",
      "autoIncrement": true,
      "android": { "buildType": "app-bundle" },
      "env": { "APP_ENV": "production" }
    }
  },
  "submit": {
    "production": {
      "android": {
        "serviceAccountKeyPath": "./google-play-service-account.json",
        "track": "internal"
      },
      "ios": {
        "appleId": "you@example.com",
        "ascAppId": "1234567890"
      }
    }
  }
}
```

Giải nghĩa các khoá quan trọng:

| Khoá | Ý nghĩa |
|---|---|
| `channel` | "Kênh" nối bản build Native với luồng update. Một bản build gắn `channel: production` chỉ nhận update đẩy vào branch được ánh xạ tới kênh đó |
| `distribution: internal` | Sinh file cài trực tiếp cho tester, không qua Store |
| `buildType: apk` vs `app-bundle` | `apk` để cài tay lúc test; `app-bundle` (`.aab`) để nộp Store (Phần 10.6) |
| `autoIncrement` | Tự tăng `versionCode`/`buildNumber` mỗi lần build — giải quyết đúng vấn đề ở Phần 10.10 |
| `appVersionSource: remote` | Để EAS giữ và quản lý số phiên bản, tránh xung đột khi nhiều người cùng build |

**7.5. Hiểu quan hệ Channel ↔ Branch** — đây là điểm gây nhầm lẫn nhiều nhất:

```
 Bản build Native đã cài trên máy người dùng
        │  (gắn cứng lúc build: channel = "production")
        ▼
   CHANNEL "production"  ──ánh xạ──►  BRANCH "production"
                                            │
                                            ▼
                              Các bản update lần lượt đẩy vào branch này
                              update #1 → update #2 → update #3 (mới nhất thắng)
```

- **Channel** nằm trong gói Native, **không đổi được** sau khi build.
- **Branch** nằm trên đám mây, **đổi ánh xạ được bất cứ lúc nào**.

Nhờ tách hai khái niệm này, bạn có thể trỏ toàn bộ người dùng Production sang một branch cũ chỉ bằng một lệnh — chính là cơ chế **rollback khẩn cấp** ở mục 7.7.

**7.6. Đẩy một bản vá:**

Giả sử bạn vừa sửa một lỗi chính tả ở `HomeScreen.tsx`. Thay vì build lại App và nộp Store:
```bash
# Đẩy lên môi trường staging để QA kiểm tra trước
eas update --branch staging --message "Sua loi chinh ta HomeScreen"

# QA duyệt xong, đẩy tiếp lên production
eas update --branch production --message "Sua loi chinh ta HomeScreen"
```

Vài giây sau, App của người dùng (khi mở lại hoặc resume) sẽ âm thầm tải bản vá này về — không cần qua App Store/Google Play review lại.

Xem lịch sử các bản đã đẩy:
```bash
eas update:list --branch production
```

**7.7. Rollback khẩn cấp — kỹ năng cứu mạng lúc 2 giờ sáng:**

Bản vá bạn vừa đẩy lại gây ra lỗi mới còn tệ hơn. Đừng hoảng, có hai cách quay đầu:

```bash
# Cách 1: Đẩy lại chính xác một bản update cũ đã biết là tốt
eas update:republish --branch production --group <UPDATE_GROUP_ID>

# Cách 2: Trỏ toàn bộ kênh production về một branch an toàn khác
eas channel:edit production --branch production-safe
```

> [!TIP]
> **Đây chính là siêu năng lực thật sự của OTA.** Với quy trình Store truyền thống, một bản lỗi phát hành lúc nửa đêm sẽ tàn phá người dùng suốt 2 ngày chờ duyệt bản vá. Với OTA, bạn quay đầu trong 30 giây ngay trên điện thoại của mình.

**7.8. Cấu hình chính sách cập nhật** trong `app.json`:
```json
{
  "expo": {
    "updates": {
      "enabled": true,
      "checkAutomatically": "ON_LOAD",
      "fallbackToCacheTimeout": 3000,
      "url": "https://u.expo.dev/<PROJECT_ID>"
    },
    "runtimeVersion": { "policy": "appVersion" }
  }
}
```

`runtimeVersion` là **chốt an toàn quan trọng nhất** của OTA: nó đánh dấu "phiên bản tầng Native". EAS chỉ gửi bản update tới những App có `runtimeVersion` **khớp**. Nhờ vậy, một bản JS mới cần thư viện Camera sẽ không bao giờ bị đẩy nhầm xuống bản App cũ chưa có Camera — tránh đúng kiểu crash hàng loạt mà giới hạn OTA ở dưới cảnh báo.

> [!WARNING]
> **Giới hạn OTA không thể phá vỡ:** Nếu bản sửa của bạn có cài thêm Native Module mới (ví dụ thêm thư viện Camera ở Chương 7) hoặc đổi cấu hình `Podfile`/`build.gradle`, EAS Update/`code-push-server` **KHÔNG THỂ** đẩy lên được. Lúc đó buộc phải build lại `.ipa`/`.aab` và nộp lên Store để Apple/Google duyệt lại từ đầu. Dấu hiệu nhận biết: bạn vừa chạy `npm install` một thư viện có thư mục `android/`/`ios/` bên trong, hoặc vừa chạy `pod install`.

#### Bước 8: Build & Kiểm chứng toàn bộ
Vì cài thêm thư viện Native (Firebase + `expo-updates`), bạn phải Build lại thô một lần cuối:
`npm run android` hoặc `npm run ios`.

Kiểm chứng theo đúng thứ tự:
1. App khởi động → vẫn thấy màn hình Đăng nhập/Trang chủ như cũ, KHÔNG có gì bị mất.
2. Đăng nhập, vào `HomeScreen`, cuộn xuống cuối, nhấn giữ 2 giây vào chữ "ShopAI v1.0.0" → App văng thật (Crash cố ý).
3. Mở lại App, chờ vài phút, vào Dashboard Firebase Crashlytics trên trình duyệt → thấy báo cáo Crash mới.
4. Tắt mạng máy chủ NestJS (Chương 9), mở lại HomeScreen → thấy dòng lỗi mạng hiển thị bình thường (App không sập) và Dashboard Crashlytics ghi nhận thêm 1 lỗi Non-Fatal.

Bạn đã chính thức vận hành App chuyên nghiệp như một Enterprise — vừa giám sát lỗi, vừa có khả năng vá lỗi từ xa — mà không hề đánh đổi bất kỳ tính năng nào của ShopAI.

---

### PHẦN D: Ký số và đóng gói bản Release Android

Phần này áp dụng lý thuyết Keystore (Phần 10.6) và R8 (Phần 10.7) vào chính dự án ShopAI. Đây cũng là lần đầu tiên bạn tạo ra một file có thể nộp lên Google Play.

#### Bước 9: Tạo Keystore cho ShopAI

Mở Terminal tại **gốc dự án Mobile**, chạy:
```bash
cd android/app

keytool -genkeypair -v \
  -storetype PKCS12 \
  -keystore shopai-release.keystore \
  -alias shopai-key-alias \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000
```

Terminal sẽ hỏi lần lượt (gõ và ghi lại cẩn thận):
```
Enter keystore password:           <- Đặt mật khẩu mạnh. GHI VÀO TRÌNH QUẢN LÝ MẬT KHẨU NGAY.
Re-enter new password:
What is your first and last name?  <- Nguyen Van A
What is the name of your organizational unit?  <- Mobile Team
What is the name of your organization?         <- ShopAI
What is the name of your City or Locality?     <- Ha Noi
What is the name of your State or Province?    <- Ha Noi
What is the two-letter country code for this unit?  <- VN
Is CN=..., correct?  <- yes
```

Kiểm tra Keystore vừa tạo:
```bash
keytool -list -v -keystore shopai-release.keystore -alias shopai-key-alias
```
Bạn sẽ thấy các vân tay chứng chỉ (SHA-1, SHA-256) — chuỗi **SHA-1** này chính là thứ cần dán vào Firebase Console (mục Project Settings → Your apps) để Crashlytics và các dịch vụ Google khác nhận diện được bản Release.

> [!CAUTION]
> **DỪNG LẠI VÀ LÀM NGAY 3 VIỆC SAU trước khi đi tiếp:**
> 1. **Sao lưu** file `shopai-release.keystore` vào ít nhất 2 nơi an toàn (kho mật khẩu của công ty, ổ cứng mã hoá). **Không** để nó chỉ nằm trên một chiếc laptop.
> 2. **Lưu mật khẩu** vào trình quản lý mật khẩu, không ghi ra giấy nhớ dán màn hình.
> 3. **Kiểm tra `.gitignore`** đã chặn nó chưa. Đây là bước dễ quên nhất và hậu quả nghiêm trọng nhất.
>
> Đọc lại cảnh báo ở Phần 10.6 mục 2 nếu bạn còn thấy ba việc này là thừa.

Mở `android/.gitignore` (hoặc `.gitignore` gốc), đảm bảo có đủ:
```
*.keystore
*.jks
android/gradle.properties
!android/app/debug.keystore
```
Dòng cuối cùng có dấu `!` là ngoại lệ có chủ đích: `debug.keystore` **nên** được commit để cả đội cùng dùng chung một chứng chỉ debug, tránh phải gỡ cài đặt App mỗi khi đổi máy.

#### Bước 10: Cấu hình Gradle và build bản Release

**10.1. Khai báo mật khẩu ở `android/gradle.properties`** (file này vừa được `.gitignore` chặn ở trên):
```properties
MYAPP_RELEASE_STORE_FILE=shopai-release.keystore
MYAPP_RELEASE_KEY_ALIAS=shopai-key-alias
MYAPP_RELEASE_STORE_PASSWORD=mat_khau_ban_vua_dat
MYAPP_RELEASE_KEY_PASSWORD=mat_khau_ban_vua_dat
```

**10.2. Cập nhật `android/app/build.gradle`** — thêm `signingConfigs` và sửa `buildTypes.release`:
```groovy
def versionMajor = 1
def versionMinor = 0
def versionPatch = 0

android {
    defaultConfig {
        applicationId "com.shopai.app"
        // Áp dụng công thức versioning ở Phần 10.10 — không bao giờ phải tự tăng tay nữa
        versionName "${versionMajor}.${versionMinor}.${versionPatch}"
        versionCode versionMajor * 10000 + versionMinor * 100 + versionPatch
    }

    signingConfigs {
        release {
            if (project.hasProperty('MYAPP_RELEASE_STORE_FILE')) {
                storeFile file(MYAPP_RELEASE_STORE_FILE)
                storePassword MYAPP_RELEASE_STORE_PASSWORD
                keyAlias MYAPP_RELEASE_KEY_ALIAS
                keyPassword MYAPP_RELEASE_KEY_PASSWORD
            }
        }
    }

    buildTypes {
        release {
            signingConfig signingConfigs.release  // Mặc định RN để signingConfigs.debug — PHẢI đổi
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
            firebaseCrashlytics { mappingFileUploadEnabled true }
        }
    }
}
```

**10.3. Build và kiểm chứng:**
```bash
cd android

# APK để cài tay lên máy thật mà test
./gradlew assembleRelease
# -> android/app/build/outputs/apk/release/app-release.apk

# AAB để nộp Google Play (Phần 10.6 mục 5)
./gradlew bundleRelease
# -> android/app/build/outputs/bundle/release/app-release.aab

# Kiểm tra file .aab đã được ký đúng chưa
jarsigner -verify -verbose -certs app/build/outputs/bundle/release/app-release.aab | head -n 20
```

Cài bản Release lên máy thật để test:
```bash
cd ..
npx react-native run-android --mode=release
```

> [!IMPORTANT]
> **Bước test bản Release này là BẮT BUỘC, không phải tuỳ chọn.** Đây là lần đầu tiên R8 thực sự chạy trên mã của bạn (Phần 10.7 mục 2). Nếu App crash ngay khi mở, mà bản Debug lại chạy tốt, thủ phạm gần như chắc chắn là R8 đã xoá nhầm một class nào đó — quay lại `proguard-rules.pro` bổ sung quy tắc `-keep` cho thư viện tương ứng.

**10.4. Ba lỗi build Release phổ biến nhất:**

| Lỗi | Nguyên nhân | Cách xử lý |
|---|---|---|
| `Keystore file not found` | Đường dẫn trong `gradle.properties` sai gốc | Đường dẫn tính từ `android/app/`, không phải từ gốc dự án |
| `Failed to read key ... wrong password` | Nhầm store password với key password | Kiểm tra lại cả hai dòng trong `gradle.properties` |
| App mở lên là văng, chỉ ở bản Release | R8 xoá nhầm class dùng Reflection | Tạm `minifyEnabled false` để xác nhận, rồi thêm `-keep` đúng thư viện |

```bash
git add .
git commit -m "Sprint 10: Integrate Firebase Crashlytics (breadcrumbs + non-fatal), APP_ENV config, EAS Update OTA, and Android release signing"
```

---

### PHẦN E: iOS — Checklist thực chiến Archive & TestFlight

Phần 10.8 đã giải thích khái niệm. Đây là checklist **thực hành từng bước**, dành cho học viên có máy macOS + tài khoản Apple Developer (99 USD/năm). Nếu bạn không có máy Mac, hãy đọc kỹ để nắm quy trình (câu hỏi phỏng vấn rất hay gặp) và chuyển sang **PHẦN F (EAS Build)** để có đường build iOS không cần máy Mac.

#### Bước 11: Checklist chuẩn bị (làm 1 lần cho cả đời dự án)

| # | Việc cần làm | Ở đâu | Ghi chú |
|---|---|---|---|
| 1 | Đăng ký **Apple Developer Program** | developer.apple.com | 99 USD/năm, xử lý 24-48h |
| 2 | Xác định **Bundle Identifier** duy nhất | Xcode → Target ShopAI → Signing & Capabilities | Dùng đúng format ngược tên miền, VD `com.shopai.app` — phải khớp với `applicationId` bên Android để đồng bộ thương hiệu |
| 3 | Bật **Automatic Signing** | Cùng tab Signing & Capabilities, tick "Automatically manage signing" | Xcode tự tạo Certificate + Provisioning Profile hộ bạn — cách dễ nhất, khuyến nghị cho học viên mới |
| 4 | Chọn đúng **Team** (Apple Developer Team) | Cùng tab, dropdown "Team" | Nếu trống, đăng nhập lại Apple ID ở Xcode → Settings → Accounts |
| 5 | Đặt đúng **Display Name**, App Icon, Version/Build number | `Info.plist` + Assets.xcassets | Áp dụng công thức Versioning ở Phần 10.10 cho `CFBundleShortVersionString`/`CFBundleVersion` |
| 6 | Tạo App trên **App Store Connect** (appstoreconnect.apple.com) | Web | Khai đúng Bundle ID vừa tạo ở bước 2, điền tên App, ngôn ngữ chính |

> [!TIP]
> **Automatic Signing vs Manual Signing:** Automatic (mục 3) để Xcode tự lo Certificate/Provisioning Profile — đủ dùng cho 95% trường hợp kể cả dự án thật. Manual Signing chỉ cần khi công ty có quy trình ký duyệt tập trung qua nhiều Team, hoặc dùng CI/CD build không có Xcode UI (Chương 11) — lúc đó phải tự tạo Certificate `.p12` và Provisioning Profile `.mobileprovision` rồi truyền vào qua biến môi trường.

#### Bước 12: Build Release cục bộ để kiểm chứng trước khi Archive

Trước khi tốn 10-20 phút Archive, hãy chắc chắn bản Release chạy được trên máy thật bằng lệnh nhanh hơn nhiều:

```bash
npx react-native run-ios --mode Release
```

Lệnh này biên dịch bản Release thật (bật Hermes AOT, tắt code debug) và cài thẳng lên thiết bị/Simulator đang chọn — **không** ký bằng Distribution Certificate nên không dùng để nộp Store được, nhưng là cách nhanh nhất để phát hiện sớm các lỗi chỉ xảy ra ở bản Release (y hệt tinh thần "test Release trước khi nộp" đã nhấn mạnh ở Phần 10.7 mục 4 cho Android).

> [!CAUTION]
> Nếu `run-ios --mode Release` crash ngay khi mở nhưng bản Debug (`npx react-native run-ios`) chạy tốt, nghi ngờ đầu tiên là cấu hình `Podfile`/Native Module thiếu cấu hình Release — kiểm tra lại Bước cài đặt các thư viện Native đã làm ở Chương 7-8 (Vision Camera, Firebase) có dòng nào chỉ áp dụng cho Debug hay không.

#### Bước 13: Archive trên Xcode & Upload TestFlight (mô tả từng bước)

Không có ảnh chụp màn hình ở đây (giáo trình dạng văn bản) — nhưng mỗi bước dưới đây tương ứng đúng một màn hình rất dễ nhận ra trong Xcode:

```
1. Mở ios/ShopAI.xcworkspace (KHÔNG mở .xcodeproj — luôn mở qua CocoaPods workspace)
      ↓
2. Ở thanh công cụ trên cùng, đổi Destination từ "iPhone Simulator" sang
   "Any iOS Device (arm64)" — Simulator KHÔNG Archive được, đây là lỗi #1 người mới gặp
      ↓
3. Menu Product → Archive (mất 10-20 phút, máy compile toàn bộ mã Native)
      ↓
4. Cửa sổ "Organizer" tự bật lên, hiện danh sách các bản Archive theo thời gian
      ↓
5. Chọn đúng bản vừa tạo (trên cùng) → bấm nút "Distribute App"
      ↓
6. Chọn "App Store Connect" → "Upload" (không chọn "Export" trừ khi bạn cần file .ipa để gửi tay)
      ↓
7. Xcode hỏi lại về Signing → chọn "Automatically manage signing" (khớp Bước 11 mục 3)
      ↓
8. Xcode tự ký lại bằng Distribution Certificate, đóng gói .ipa, tải thẳng lên Apple
      ↓
9. Đợi Apple xử lý ở App Store Connect (15-60 phút, có email báo khi xong)
      ↓
10. Vào App Store Connect → tab TestFlight → build vừa tải lên xuất hiện
      ↓
11. Thêm Internal Tester (email trong cùng team, có ngay không cần duyệt — xem lại Phần 10.8)
      ↓
12. Tester cài app "TestFlight" từ App Store → nhận lời mời qua email → tải bản build về dùng thử
```

> [!IMPORTANT]
> **Điểm hay bị bỏ sót nhất:** mỗi lần Archive lại để nộp bản mới, `CFBundleVersion` (Build number) **bắt buộc phải tăng**, kể cả khi `CFBundleShortVersionString` (version hiển thị) giữ nguyên — App Store Connect từ chối thẳng build trùng số, y hệt nguyên tắc `versionCode` của Android ở Phần 10.10.

#### Yêu cầu Nghiệm thu (bổ sung — iOS)

9. Hoàn thành Checklist Bước 11 (Bundle ID, Automatic Signing, Team, App tạo trên App Store Connect) — nếu không có máy Mac/tài khoản Apple Developer, ghi rõ lý do và chuyển sang minh chứng bằng EAS Build (Phần F) hoặc build Android.
10. Chạy thành công `npx react-native run-ios --mode Release` trên máy thật/Simulator (nếu có máy Mac).

---

### PHẦN F: EAS Build thực chiến — Cloud hay Local?

Phần 10.11 đã so sánh lý thuyết. Đây là bước **chạy thật** ít nhất một lần, đúng yêu cầu Nghiệm thu của Sprint này: cấu hình xong `eas.json` (đã có sẵn ở Bước 7.4) **và** có ít nhất một đường build thành công — Cloud (EAS) hoặc Local (Android Studio/Xcode) đều được chấp nhận.

#### Bước 14: Build thử bản Android qua EAS (Cloud) — không cần máy mạnh

Vì `eas.json` đã được tạo đầy đủ 3 profile ở Bước 7.4 (Phần C), bạn chỉ cần một lệnh:

```bash
# Đăng nhập nếu chưa làm ở Bước 7.1
eas login

# Build bản Android profile "preview" — sinh file .apk cài tay được ngay, không cần Google Play
eas build --platform android --profile preview
```

Lệnh này đẩy mã nguồn lên máy chủ Expo, xếp hàng chờ (vài phút nếu dùng gói miễn phí), biên dịch toàn bộ Native (Chặng 5 của đường ống Phần 10.1), rồi trả về đường link tải file `.apk`. Quét mã QR mà CLI in ra hoặc mở link bằng trình duyệt trên điện thoại Android để tải và cài trực tiếp.

```bash
# Theo dõi tiến trình build đang chạy hoặc đã hoàn tất
eas build:list --platform android --limit 5
```

#### Bước 15: Build thử bản iOS qua EAS (Cloud) — không cần máy Mac

Đây chính là giá trị lớn nhất của EAS Build: bạn **không cần sở hữu máy Mac** vẫn build được `.ipa`:

```bash
eas build --platform ios --profile preview
```

Lần đầu chạy, EAS CLI sẽ hỏi bạn có muốn để **Expo tự quản lý Credentials** (Certificate + Provisioning Profile) không — chọn **Yes** là lựa chọn đơn giản nhất, tương đương "Automatic Signing" của Xcode ở Bước 11 mục 3 nhưng chạy trên đám mây. Bạn vẫn cần nhập tài khoản Apple Developer khi được hỏi.

> [!NOTE]
> **Không có tài khoản Apple Developer?** Không sao — theo đúng nguyên tắc "Required acceptance" của Sprint này, chỉ cần **một trong hai** nền tảng build thành công là đủ đạt yêu cầu. Hoàn thành Bước 14 (Android qua EAS Cloud) hoặc build Release cục bộ (`./gradlew bundleRelease` ở Bước 10.3) là đã thoả điều kiện nghiệm thu, không bắt buộc phải có cả Android lẫn iOS.

#### Bước 16: Chọn Cloud hay Local cho lần build tiếp theo?

Ôn lại bảng so sánh ở Phần 10.11 và áp dụng ngay cho tình huống của chính bạn:

| Tình huống của bạn | Nên chọn |
|---|---|
| Đang học, có sẵn Android Studio, muốn lặp nhanh | **Local** — `./gradlew assembleRelease` (Bước 10.3), vài phút là xong |
| Không có máy Mac nhưng cần bản `.ipa` để test trên iPhone | **EAS Build (Cloud)** — gần như lựa chọn duy nhất hợp lý |
| Cả lớp cùng build trên máy yếu, mạng chậm | **EAS Build (Cloud)** — máy chủ Expo build hộ, chỉ cần tải kết quả về |
| Công ty đã có CI riêng (Chương 11) | **Local**, chạy trên runner CI, chủ động không phụ thuộc Expo |

```bash
git add .
git commit -m "Sprint 10 (bonus): iOS release checklist (Archive/TestFlight) + EAS Build cloud/local documentation"
```

### ✅ Checklist Nghiệm thu Sprint 10

**Cấu hình môi trường:**
- [ ] `src/constants/env.ts` tồn tại, khai báo đủ `APP_ENV`, `API_BASE_URL`, `ENABLE_CRASHLYTICS`.
- [ ] Không còn chỗ nào hardcode IP LAN ngoài `env.ts`.

**Crashlytics:**
- [ ] Firebase Crashlytics hoạt động, Dashboard nhận được Test Crash.
- [ ] Nút test Crash chỉ tồn tại trong `__DEV__`, không xuất hiện ở bản Production.
- [ ] Lỗi fetch ở `HomeScreen` được ghi nhận Non-Fatal qua `recordError`, App không bị sập khi mất mạng.
- [ ] Lỗi đặt hàng ở `CheckoutScreen` được ghi nhận với tên nhóm `CheckoutOrderFailed`, kèm Breadcrumb và Custom Keys.
- [ ] `mappingFileUploadEnabled true` đã bật cho `buildTypes.release`.

**Không phá vỡ tính năng cũ:**
- [ ] `App.tsx` vẫn còn đầy đủ `SafeAreaProvider`, `QueryClientProvider`, `NavigationContainer`, `AuthStack`, `MainTabNavigator` như trước Sprint 10.
- [ ] Toàn bộ luồng Chương 9 (sản phẩm, chi tiết, đặt hàng, chat AI) vẫn chạy đúng.

**Release & OTA:**
- [ ] Đã tạo `shopai-release.keystore`, **đã sao lưu**, và `.gitignore` đã chặn nó.
- [ ] `./gradlew bundleRelease` chạy thành công, sinh ra `app-release.aab` đã ký.
- [ ] Bản Release chạy được trên máy thật (R8 không làm crash).
- [ ] `eas.json` có đủ 3 profile `development` / `preview` / `production`.
- [ ] Hiểu rõ: EAS Update/`code-push-server` chỉ vá được JS, không vá được thay đổi Native. Không dùng CodePush/App Center vì đã ngừng hoạt động từ 3/2025.
- [ ] Biết cách rollback một bản OTA lỗi bằng `eas update:republish` hoặc `eas channel:edit`.

**iOS & EAS Build (Phần E/F):**
- [ ] Hoàn thành checklist Bundle ID + Automatic Signing + Team trên Xcode (nếu có máy Mac), HOẶC ghi rõ lý do bỏ qua.
- [ ] Chạy được `npx react-native run-ios --mode Release` (nếu có máy Mac) hoặc nắm rõ quy trình Archive → TestFlight bằng lời.
- [ ] Chạy thành công **ít nhất một** trong hai: `eas build --platform android --profile preview` (Cloud) HOẶC build Release cục bộ (`./gradlew bundleRelease`) — đúng yêu cầu nghiệm thu tối thiểu của Sprint.
- [ ] Biết chọn Cloud (EAS Build) hay Local cho từng tình huống cụ thể (bảng ở Phần F, Bước 16).

---

## 🎯 CHUẨN BỊ CHO CHƯƠNG CUỐI CÙNG (CHƯƠNG 11)
Bạn không thể cứ thêm tính năng mới là lấy điện thoại ra tự lấy ngón tay bấm thử từng nút xem app có hỏng không (kể cả nút test Crash ẩn bạn vừa làm ở Sprint 10 — vẫn phải bấm tay!). Sức người có hạn.
Chương 11 - Chương cuối cùng, sẽ dạy bạn **Tự động hóa toàn bộ** quá trình Kiểm thử (Testing) bằng Robot Maestro, viết Unit Test bằng Jest, và CI/CD Pipelines đẩy App lên thẳng chợ ứng dụng chỉ bằng 1 dòng lệnh. Đẳng cấp của Kỹ sư Siêu Sao!
