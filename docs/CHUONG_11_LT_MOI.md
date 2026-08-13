---
sidebar_position: 11
title: Chương 11
---

# GIÁO TRÌNH LÝ THUYẾT & THỰC CHIẾN
## CHƯƠNG 11: KIỂM THỬ ĐỈNH CAO (TESTING) VÀ TỰ ĐỘNG HÓA PHÁT HÀNH (CI/CD)
**Thời lượng:** 6 tiết Lý thuyết + 5 tiết Thực hành

---

> [!IMPORTANT]
> **Thực hành chương = Sprint ShopAI cuối file.** Hoàn thành Sprint này để đạt mục tiêu chương. Hoàn thành đủ 11 chương theo `SHOPAI_HOAN_THIEN.md` = sản phẩm ShopAI **hoàn thiện đẳng cấp**.

## 📚 MỤC TIÊU HỌC TẬP

Sau khi hoàn thành chương này, học viên sẽ:
- ✅ Hiểu mô hình **Testing Pyramid (Kim tự tháp kiểm thử)** và phân biệt rõ Unit Test, Integration Test, E2E Test.
- ✅ Viết thành thạo **Jest Unit Test** (mở rộng từ hàm `formatCurrency`) cho các hàm thuần túy trong dự án.
- ✅ Làm chủ **React Native Testing Library (RNTL)** để viết Integration Test — kiểm tra Component thật (render, bấm nút, giả lập tương tác người dùng) mà không cần mở máy ảo.
- ✅ Làm chủ **Maestro (Robot kiểm thử E2E)** để tự động hóa việc vuốt, chạm, nhập liệu trên điện thoại thật thay vì phải test bằng tay.
- ✅ Biết cách bật và dùng **React Native DevTools** (built-in từ RN 0.73+) và **Flipper** (công cụ debug/inspect truyền thống) để soi Network, State, UI Layout khi App đang chạy.
- ✅ Am hiểu kiến trúc của **CI/CD Pipelines (Tích hợp liên tục và Triển khai liên tục)**.
- ✅ Biết khái niệm dùng **Fastlane** và **GitHub Actions** để tự động nén APK/IPA và đẩy lên kho ứng dụng Apple/Google hoàn toàn tự động.
- ✅ Làm chủ **Jest Mocking**: giả lập `fetch`, giả lập Zustand Store, giả lập Native Module — điều kiện bắt buộc để test được code có gọi mạng.
- ✅ Viết test cho **Custom Hook** bằng `renderHook` và `act`.
- ✅ Đo **Code Coverage**, đặt **ngưỡng tối thiểu (threshold)** và hiểu vì sao "100% coverage" là một mục tiêu sai.
- ✅ So sánh **Detox / Maestro / Appium** để chọn đúng công cụ E2E cho từng loại dự án.
- ✅ Nắm khái niệm **Visual Regression Testing** — bắt lỗi giao diện mà mọi loại test khác đều bỏ sót.
- ✅ Viết một **Fastfile** hoàn chỉnh cho luồng phát hành Beta Android.
- ✅ Nâng cấp **GitHub Actions** với Matrix nhiều phiên bản Node, Cache và Upload Artifact.
- ✅ Thiết lập **Pre-commit Hook** bằng Husky + lint-staged để chặn code lỗi ngay từ máy lập trình viên.
- ✅ Viết được một **Test Plan** (Kế hoạch kiểm thử) cho toàn bộ tính năng ShopAI.
- ✅ **Kiểm thử Backend NestJS:** Viết Jest Unit Test cho `AuthService`/`OrderService` và E2E Test bằng **Supertest** cho `POST /api/auth/login` và `POST /api/orders` (bảo vệ bằng JWT Guard, kiểm tra đúng 401 khi thiếu Token và 201 khi có Token hợp lệ).
- ✅ **Tổng kết khóa học:** Chúc mừng bạn đã tiến hóa từ một Coder nghiệp dư thành Software Engineer tiêu chuẩn toàn cầu.

> [!NOTE]
> **Ánh xạ đề cương chính thức (Chương 7 "Kiểm thử & Debug"):** Jest Unit Test, RNTL Integration Test, React Native Debugger/DevTools, Flipper — **TẤT CẢ được dạy đủ trong chương này**. Maestro E2E và CI/CD (GitHub Actions, Fastlane) là kiến thức nâng cao, mở rộng thêm ngoài đề cương chính thức.

---

### 0. Nhìn tổng thể trước khi đọc sâu

Đây là chương cuối cùng — thay vì thêm tính năng mới, Chương 11 dạy bạn cách **đảm bảo mọi tính năng đã xây từ Chương 1–10 không bị hỏng âm thầm** mỗi khi sửa code. Kim tự tháp kiểm thử dưới đây là xương sống của cả chương.

**Sơ đồ tổng quan — Kim tự tháp kiểm thử Jest → RNTL → Maestro:**

```
                        ▲
                       ╱ ╲          E2E Test — MAESTRO
                      ╱   ╲         Robot bấm/vuốt/gõ như người dùng thật
                     ╱     ╲        Chậm nhất, ít bài test nhất, "đắt" nhất
                    ╱───────╲
                   ╱         ╲      Integration Test — RNTL
                  ╱           ╲     Render Component thật, giả lập bấm nút/nhập liệu
                 ╱             ╲    Vừa nhanh vừa mô phỏng khá thật
                ╱───────────────╲
               ╱                 ╲  Unit Test — JEST
              ╱                   ╲ Test từng hàm thuần túy (formatCurrency, getShippingTier...)
             ╱                     ╲Rẻ nhất, nhanh nhất, nên viết NHIỀU nhất
            ╱_________________________╲

   Càng lên đỉnh: càng chậm, càng giống thật, càng nên viết ÍT.
   Càng xuống đáy: càng nhanh, càng rẻ, càng nên viết NHIỀU.
```

**Sau chương này, bạn sẽ làm được gì:**
- ✅ Phân biệt rạch ròi Unit / Integration / E2E Test và biết nên viết mỗi loại bao nhiêu là đủ.
- ✅ Viết Jest Unit Test cho hàm thuần túy và Jest Mocking cho `fetch`/Zustand Store/Native Module.
- ✅ Dùng RNTL để test Component thật: render, bấm nút, kiểm tra kết quả — không cần mở máy ảo.
- ✅ Viết kịch bản Maestro (file YAML) để robot tự vuốt/chạm/gõ chữ trên điện thoại thay bạn.
- ✅ Dựng một pipeline CI/CD cơ bản bằng GitHub Actions và hiểu vai trò của Fastlane trong phát hành tự động.

**Lộ trình đọc gợi ý (lý thuyết → thực chiến):**
1. Đọc kỹ Phần 11.1 để nắm chắc Kim tự tháp — mọi phần sau chỉ là "đào sâu" một tầng trong hình trên.
2. Đọc Phần 11.2 (RNTL) và tự tay chạy thử bài test `ShopButton` mẫu trước khi viết test riêng của mình.
3. Đọc Phần 11.4 (Maestro) song song lúc cài đặt công cụ — đây là kiến thức mới, nên vừa đọc vừa gõ lệnh thử.
4. Đọc kỹ phần Jest Mocking + Test Custom Hook trước khi test bất kỳ màn hình nào có gọi API.
5. Đọc Phần 11.15 (Kiểm thử Backend NestJS) trước khi làm Sprint — đây là phần **CRITICAL**: viết Unit/E2E Test cho `AuthModule` + `Orders` (JWT + Prisma) đã dựng thật ở Chương 9.
6. Làm Sprint 11 — Sprint cuối cùng của khoá học — rồi đọc phần Tổng kết để nhìn lại toàn bộ hành trình 11 chương.

> [!TIP]
> **Nhầm lẫn thường gặp nhất chương này:** học viên mới hay nghĩ "viết càng nhiều E2E Test càng tốt vì nó giống thật nhất". Ngược lại — E2E chạy chậm, dễ bị Flaky (lúc pass lúc fail vô cớ), và tốn RAM/thời gian CI. Nguyên tắc đúng là viết THẬT NHIỀU Unit Test, kha khá Integration Test, và chỉ vài kịch bản E2E cho những luồng quan trọng nhất (VD: Đăng nhập → Đặt hàng thành công).

---

## 🧪 PHẦN 11.1: KIM TỰ THÁP KIỂM THỬ (TESTING PYRAMID)

Bạn sửa một lỗi nhỏ ở Màn hình Đăng nhập, hôm sau Màn hình Thanh toán tự nhiên lăn đ ra chết (Lỗi hồi quy - Regression Bug). Việc con người tự tay lấy điện thoại mở từng màn hình ra bấm bấm mỗi khi thay đổi mã nguồn là bất khả thi trong dự án lớn. Máy móc phải làm thay con người.

**Kim tự tháp Kiểm thử gồm 3 tầng:**

1. **Unit Test (Dưới cùng - Rộng nhất):** Test từng khối code nhỏ li ti. (VD: Test hàm `formatTienTe(1500)` xem nó có nhả ra chữ `1.500 đ` không). Chạy cực nhanh (1 giây chạy 1000 test). Công cụ: **Jest**.
2. **Integration Test (Khúc giữa):** Test xem các Component có nói chuyện được với nhau không. (VD: Component Form nhập liệu có kết nối đúng với Redux/Zustand không). Công cụ: **React Native Testing Library (RTL)**.
3. **E2E Test (Đỉnh tháp - End-to-End):** Test toàn diện như một người dùng thật cầm máy. Robot sẽ mở app, bấm nút Login, gõ mật khẩu, vuốt màn hình. Chạy cực chậm, tốn RAM, nhưng mô phỏng thật nhất. Công cụ: **Maestro, Appium, Detox**.

---

## 🧩 PHẦN 11.2: INTEGRATION TEST VỚI REACT NATIVE TESTING LIBRARY (RNTL)

Unit Test (Jest thuần) chỉ test được các hàm thuần túy (`formatCurrency`, `calculateTotal`...) — nó KHÔNG "render" giao diện thật. Nhưng phần lớn lỗi thực tế xảy ra ở tầng Component: người dùng bấm nút mà không có gì xảy ra, nhập liệu mà State không cập nhật... Đây là lý do tầng giữa Kim tự tháp cần **React Native Testing Library (RNTL)** — thư viện cho phép "giả lập" một Component thật (render ảo, không cần máy ảo/điện thoại), rồi thao tác lên nó như người dùng thật (bấm, gõ chữ) và kiểm tra kết quả.

### 1. Cài đặt

RNTL thường đi kèm sẵn trong template React Native CLI mới (`@testing-library/react-native`), nếu chưa có thì cài thêm:

```bash
npm install --save-dev @testing-library/react-native
```

Đảm bảo `jest.config.js`/`package.json` có `preset: 'react-native'` (mặc định RN CLI đã cấu hình sẵn).

### 2. Triết lý của RNTL: Test như người dùng nhìn thấy, không test chi tiết cài đặt bên trong

RNTL cố ý KHÔNG cho bạn truy cập trực tiếp vào State/Props nội bộ của Component (khác với thư viện cũ Enzyme). Bạn chỉ được phép truy vấn Component **giống hệt cách người dùng nhìn thấy màn hình**: tìm theo Text hiển thị, theo Role, theo `testID`. Điều này giúp Test không bị vỡ khi bạn refactor code bên trong mà hành vi bên ngoài không đổi.

### 3. Ví dụ: Test `ShopButton` (đã xây ở Chương 3)

Tạo file `src/components/__tests__/ShopButton.test.tsx`:

```tsx
import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react-native';
import ShopButton from '../ShopButton';

describe('ShopButton', () => {
  it('hiển thị đúng title được truyền vào', () => {
    render(<ShopButton title="Xác nhận thanh toán" onPress={() => {}} />);
    expect(screen.getByText('Xác nhận thanh toán')).toBeTruthy();
  });

  it('gọi đúng hàm onPress khi người dùng bấm vào nút', () => {
    const handlePress = jest.fn(); // Hàm giả (Mock) để theo dõi có bị gọi hay không
    render(<ShopButton title="Đăng nhập ngay" onPress={handlePress} />);

    fireEvent.press(screen.getByText('Đăng nhập ngay')); // Giả lập người dùng bấm nút

    expect(handlePress).toHaveBeenCalledTimes(1); // Kiểm tra đã bấm đúng 1 lần
  });

  it('KHÔNG gọi onPress khi nút đang ở trạng thái disabled', () => {
    const handlePress = jest.fn();
    render(<ShopButton title="Đang xử lý" onPress={handlePress} disabled />);

    fireEvent.press(screen.getByText('Đang xử lý'));

    expect(handlePress).not.toHaveBeenCalled(); // Nút bị khóa -> Không được gọi
  });
});
```

Chạy Test:
```bash
npx jest src/components/__tests__/ShopButton.test.tsx
```

> [!TIP]
> Khác với Unit Test (chỉ test 1 hàm đơn lẻ), RNTL test **hành vi tương tác** của cả Component — đúng nghĩa "Integration Test" (kiểm tra Component + logic bên trong nó có phối hợp đúng không). Học viên sẽ viết thêm một bài test tương tự cho `ShopButton`/`Typography` ngay ở Sprint 11 phía dưới.

---

## 🔬 PHẦN 11.3: DEBUG TRỰC QUAN VỚI REACT NATIVE DEVTOOLS & FLIPPER

Khi App chạy sai (UI lệch, State không đúng, Request mạng bị lỗi), `console.log` chỉ giúp được phần nào. Cần công cụ debug trực quan để soi toàn bộ "nội tạng" App đang chạy: cây Component, State/Props hiện tại, Network Request, Log Native.

### 1. React Native DevTools (built-in từ RN 0.73+) — Khuyến nghị dùng hiện nay

Từ phiên bản **React Native 0.73**, Facebook/Meta tích hợp sẵn **React Native DevTools** ngay trong Metro — không cần cài thêm extension hay app riêng. Cách bật:

1. Chạy App ở chế độ Debug (`npm run android`/`npm run ios`).
2. Trong Terminal đang chạy Metro, nhấn phím `j` (hoặc mở Dev Menu trên điện thoại — lắc máy/`Cmd+D` trên iOS Simulator, `Cmd+M`/`Ctrl+M` trên Android Emulator — rồi chọn **"Open DevTools"**).
3. Một cửa sổ giống Chrome DevTools sẽ mở ra, có đủ 2 tab quan trọng:
   - **Components**: Xem cây Component, State, Props hiện tại — giống React DevTools trên Web.
   - **Profiler**: Đo hiệu năng render, phát hiện Component nào Re-render vô tội vạ (liên hệ trực tiếp bài học `React.memo`/`useCallback` ở Chương 3).

> [!NOTE]
> Đây là công cụ **được khuyến nghị chính thức** cho các dự án React Native hiện đại (0.73+ trở lên, và bắt buộc với Kiến trúc mới New Architecture/Bridgeless). Cách debug cũ dùng "Debug with Chrome" đã bị loại bỏ hoàn toàn từ RN 0.73.

### 2. Flipper — Công cụ Debug truyền thống (vẫn cần biết vì nhiều dự án cũ còn dùng)

**Flipper** (do Meta phát triển trước khi có RN DevTools) là một ứng dụng Desktop riêng biệt, cắm vào App qua một "cầu nối" (Flipper SDK), cho phép xem nhiều thứ hơn cả DevTools: Network Inspector chi tiết (Header, Body, Response Time từng Request Axios), Layout Inspector (đo khoảng cách UI như Chrome Inspect Element), Crash Reporter, và hỗ trợ Plugin mở rộng của bên thứ ba.

**Cách cài đặt (tham khảo — nhiều dự án RN mới không còn bật sẵn Flipper theo mặc định):**
```bash
# Tải Flipper Desktop App tại: https://fbflipper.com/
# Trong dự án RN CLI (Android), đảm bảo build.gradle có debugImplementation cho flipper-integration
# Với RN 0.73+, Flipper KHÔNG còn được bật mặc định trong template mới — cần enable tay
```

Sau khi App debug kết nối được vào Flipper Desktop, bạn có thể mở tab **Network** để xem trực tiếp mọi Request `axiosClient` (đã học ở Chương 6) đi/về, kiểm tra Header `Authorization: Bearer <token>` do Interceptor tự gắn có đúng không.

> [!IMPORTANT]
> **Flipper đang dần "deprecated-ish"** (không còn được ưu tiên phát triển tích cực) trong các phiên bản React Native mới nhất, do React Native DevTools built-in đã thay thế phần lớn tính năng phổ biến nhất (Component tree, Network cơ bản). Học viên **cần biết CẢ HAI**: Flipper (di sản, vẫn gặp trong dự án cũ/doanh nghiệp lớn) và React Native DevTools (hiện đại, mặc định cho dự án mới) — đúng chuẩn đề cương Chương 7.

---

## 🤖 PHẦN 11.4: KỶ NGUYÊN KIỂM THỬ E2E VỚI MAESTRO

Ngày xưa, cả ngành công nghiệp phải dùng **Appium** (rất rườm rà, cài đặt lỗi liên tục) hoặc **Detox** (setup rất khó, dễ bị chập chờn - Flaky test).
Gần đây, thư viện **Maestro** ra đời và trở thành vị cứu tinh.
- Viết kịch bản test bằng file YAML siêu đơn giản (không cần code JS/Java phức tạp).
- Không cần cấu hình lằng nhằng vào mã nguồn RN.
- Chạy siêu tốc và hiểu được độ trễ (Network delay) của App.

**Ví dụ kịch bản YAML của Maestro:**
```yaml
appId: com.shopai.app
---
- launchApp
- tapOn: "you@example.com" # Tap vào ô Email qua placeholder hiển thị trên UI, không phải nhãn "Email"
- inputRandomEmail
- tapOn: "Ít nhất 6 ký tự" # Ô Mật khẩu chỉ hiện placeholder này, KHÔNG có label "Mật khẩu" hiển thị trên UI
- inputText: "secret123"
- tapOn: "Đăng nhập ngay"
- assertVisible: "Khám phá" # Kiểm tra xem đã nhảy vào HomeScreen chưa
- scroll
```
Robot sẽ đọc file này, bật máy ảo lên và tự động lấy "ngón tay ảo" bấm đúng y như những gì bạn viết.

---

## 🚀 PHẦN 11.5: TỰ ĐỘNG HÓA PHÁT HÀNH (CI/CD VÀ FASTLANE)

### 1. Nỗi đau Build App Thủ Công
Để đưa 1 bản update lên App Store. Bạn phải: Mở Xcode -> Bấm Archive (Chờ 20 phút) -> Bấm Verify -> Vào web Apple Developer tạo phiên bản -> Upload file lên. Tốn cả tiếng đồng hồ mòn mỏi ngồi canh.

### 2. CI/CD (Continuous Integration / Continuous Deployment)
**CI/CD** là việc đưa hệ thống rô bốt lên Đám mây (như **GitHub Actions** hoặc Bitbucket Pipelines).
- Mỗi khi bạn gõ lệnh `git push origin main` đẩy code lên Github. 
- Đám mây Github tự động tải máy ảo Mac về, tự động chạy Unit Test xem code bạn có phá hỏng cái gì không.
- Nếu Test xanh (Pass), nó sẽ gọi **Fastlane**.

### 3. Fastlane (Tên lửa đẩy)
Fastlane là một công cụ viết bằng Ruby. Nó thay thế 100% bàn tay con người. Nó tự động nén code của bạn thành file `.apk` và `.ipa`, tự động đăng nhập vào tài khoản Apple/Google của công ty, tự động viết Release Note (Chi tiết bản cập nhật), và tự động bấm nút Submit (Đẩy lên Chợ ứng dụng).

Bạn đẩy code xong, đi uống một ly Cafe, quay lại thấy App đã lên Store cho 1 triệu người tải. Đó là quyền năng của DevOps.

---

## 🎭 PHẦN 11.6: JEST MOCKING — GIẢ LẬP THẾ GIỚI BÊN NGOÀI

Hàm `formatCurrency` rất dễ test vì nó **thuần khiết**: cùng đầu vào luôn cho cùng đầu ra, không phụ thuộc gì bên ngoài. Nhưng phần lớn code thật thì không như vậy — nó gọi mạng, đọc ổ cứng, mở camera. Ba vấn đề nảy sinh ngay:

1. **Chậm:** mỗi test gọi API thật mất vài trăm mili-giây; 200 test là 2 phút chờ.
2. **Chập chờn (Flaky):** Server NestJS chưa bật → test đỏ, dù code hoàn toàn đúng.
3. **Không kiểm soát được:** làm sao ép Server trả về lỗi `500` để test nhánh xử lý lỗi?

**Mocking** giải quyết cả ba: thay thế thứ thật bằng một bản giả do bạn điều khiển hoàn toàn.

### 1. `jest.fn()` — viên gạch nền

```ts
const mockFn = jest.fn();              // Hàm giả, không làm gì cả
const mockAdd = jest.fn((a, b) => a + b);   // Hàm giả có hành vi
const mockApi = jest.fn().mockResolvedValue({ id: 1 }); // Hàm giả trả về Promise

mockFn('xin chào');

expect(mockFn).toHaveBeenCalled();               // Đã bị gọi chưa?
expect(mockFn).toHaveBeenCalledTimes(1);         // Gọi đúng mấy lần?
expect(mockFn).toHaveBeenCalledWith('xin chào'); // Gọi với tham số gì?
```

Đây chính là thứ đã dùng ở Phần 11.2 với `const handlePress = jest.fn()`.

### 2. Mock `fetch` — kỹ thuật dùng nhiều nhất

`fetch` là biến toàn cục, ta ghi đè thẳng lên nó:

```ts
// src/api/__tests__/fetchProducts.test.ts
import { fetchProductsAPI } from '../fetchProducts';

describe('fetchProductsAPI', () => {
  beforeEach(() => {
    // Dọn sạch mock trước MỖI test — nếu không, số lần gọi sẽ cộng dồn giữa các test
    // và bạn sẽ mất cả buổi để hiểu vì sao test thứ hai luôn đỏ.
    jest.clearAllMocks();
  });

  it('trả về danh sách sản phẩm khi Server phản hồi 200', async () => {
    const fakeProducts = [
      { id: 'p1', name: 'iPhone 15', price: 25000000, image: 'https://x.com/a.jpg' },
    ];

    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => fakeProducts,
    }) as jest.Mock;

    const result = await fetchProductsAPI();

    expect(result).toHaveLength(1);
    expect(result[0].name).toBe('iPhone 15');
    expect(global.fetch).toHaveBeenCalledWith(expect.stringContaining('/api/products'));
  });

  it('ném lỗi khi Server trả về 500', async () => {
    global.fetch = jest.fn().mockResolvedValue({ ok: false, status: 500 }) as jest.Mock;

    // Đây là nhánh gần như KHÔNG THỂ test bằng tay — bạn đâu thể bắt Server thật sập theo ý mình
    await expect(fetchProductsAPI()).rejects.toThrow('Lỗi mạng từ Server NestJS');
  });

  it('ném lỗi khi Zod phát hiện dữ liệu bẩn', async () => {
    // Server trả về đúng 200 nhưng thiếu trường 'price' — mô phỏng lỗi Backend đổi API
    global.fetch = jest.fn().mockResolvedValue({
      ok: true,
      json: async () => [{ id: 'p1', name: 'Thiếu giá' }],
    }) as jest.Mock;

    await expect(fetchProductsAPI()).rejects.toThrow(/Zod/);
  });
});
```

> [!TIP]
> Test thứ ba là ví dụ đắt giá nhất: nó chứng minh **trạm kiểm soát Zod** bạn dựng từ Chương 6 thực sự hoạt động. Ngoài đời, để tái hiện tình huống này bạn phải nhờ anh Backend cố tình làm hỏng API — với mock thì chỉ mất 3 dòng.

### 3. Mock Zustand Store

Component gọi `useCartStore()` sẽ đọc Store thật, mang theo dữ liệu còn sót lại từ test trước. Ba cách xử lý, từ đơn giản đến bài bản:

**Cách A — Reset Store thật giữa các test (khuyến nghị, gần thực tế nhất):**
```ts
import { useCartStore } from '@store/useCartStore';

beforeEach(() => {
  useCartStore.setState({ items: [] }); // Zustand cho phép set State trực tiếp từ bên ngoài React
});
```

**Cách B — Mock toàn bộ Module:**
```ts
jest.mock('@store/useCartStore', () => ({
  useCartStore: jest.fn((selector) =>
    selector({
      items: [{ id: 'p1', name: 'iPhone 15', price: 25000000, quantity: 2 }],
      addItem: jest.fn(),
      removeItem: jest.fn(),
      clearCart: jest.fn(),
      totalQuantity: () => 2,
      totalPrice: () => 50000000,
    }),
  ),
}));
```

**Cách C — Mock `persist` middleware** để test không đụng tới ổ cứng:
```ts
jest.mock('@react-native-async-storage/async-storage', () =>
  require('@react-native-async-storage/async-storage/jest/async-storage-mock'),
);
```

> [!IMPORTANT]
> Ưu tiên **Cách A**. Mock toàn bộ Store (Cách B) khiến test không còn kiểm tra được logic thật bên trong Store — nếu bạn viết sai công thức `totalPrice`, test vẫn xanh vì nó đang đọc con số giả bạn tự điền. Chỉ mock những thứ thuộc **thế giới bên ngoài** (mạng, ổ cứng, phần cứng), đừng mock **logic của chính mình**.

### 4. Mock Native Module — bắt buộc với ShopAI

ShopAI dùng nhiều thư viện Native (Chương 7-10) mà môi trường Jest (chạy trên Node, không có Android/iOS) không thể nạp được. Không mock, mọi test đều đỏ ngay dòng `import`.

Tạo `jest.setup.js` ở gốc dự án:
```js
// Firebase Crashlytics (Chương 10)
jest.mock('@react-native-firebase/crashlytics', () => () => ({
  log: jest.fn(),
  recordError: jest.fn(),
  setUserId: jest.fn(),
  setAttributes: jest.fn(),
  crash: jest.fn(),
}));

// expo-secure-store (Chương 8)
jest.mock('expo-secure-store', () => ({
  getItemAsync: jest.fn(() => Promise.resolve(null)),
  setItemAsync: jest.fn(() => Promise.resolve()),
  deleteItemAsync: jest.fn(() => Promise.resolve()),
}));

// expo-updates (Chương 10)
jest.mock('expo-updates', () => ({
  checkForUpdateAsync: jest.fn(() => Promise.resolve({ isAvailable: false })),
  fetchUpdateAsync: jest.fn(),
  reloadAsync: jest.fn(),
}));

// Reanimated (Chương 4)
jest.mock('react-native-reanimated', () => require('react-native-reanimated/mock'));

// Vision Camera (Chương 7)
jest.mock('react-native-vision-camera', () => ({
  Camera: 'Camera',
  useCameraDevice: jest.fn(() => ({ id: 'back' })),
  useCodeScanner: jest.fn(),
}));
```

Khai báo file này trong `package.json`:
```json
"jest": {
  "preset": "react-native",
  "setupFiles": ["<rootDir>/jest.setup.js"],
  "transformIgnorePatterns": [
    "node_modules/(?!(@react-native|react-native|@react-navigation|expo|@expo|react-native-reanimated)/)"
  ]
}
```

> [!WARNING]
> `transformIgnorePatterns` là dòng cấu hình gây đau đầu nhất khi mới setup Jest cho React Native. Mặc định Jest **bỏ qua** toàn bộ `node_modules` khi biên dịch, nhưng nhiều thư viện RN lại phát hành mã ES Modules chưa biên dịch. Triệu chứng: `SyntaxError: Cannot use import statement outside a module`. Cách chữa: thêm tên thư viện đó vào danh sách ngoại lệ `(?!(...))` ở trên.

---

## 🪝 PHẦN 11.7: TEST CHO CUSTOM HOOK VỚI `renderHook`

Hook không phải component (không render ra gì) cũng không phải hàm thuần (dùng State, Effect). Không thể gọi thẳng `useCartStore()` trong file test — React sẽ ném lỗi *"Invalid hook call"*.

Giải pháp: `renderHook` — nó tạo một component rỗng chỉ để chứa Hook, rồi trả về giá trị Hook trả ra.

```tsx
import { renderHook, act } from '@testing-library/react-native';
import { useCartStore } from '@store/useCartStore';

describe('useCartStore', () => {
  beforeEach(() => {
    useCartStore.setState({ items: [] }); // Mỗi test bắt đầu từ giỏ hàng trống
  });

  it('thêm sản phẩm vào giỏ hàng', () => {
    const { result } = renderHook(() => useCartStore());

    // MỌI thay đổi State phải bọc trong act() — báo cho React "sắp có cập nhật,
    // hãy xử lý xong hết rồi mới cho tôi đọc kết quả". Thiếu act(), bạn sẽ đọc phải State cũ.
    act(() => {
      result.current.addItem({
        id: 'p1', name: 'iPhone 15', price: 25000000, image: 'https://x.com/a.jpg',
      });
    });

    expect(result.current.items).toHaveLength(1);
    expect(result.current.totalQuantity()).toBe(1);
  });

  it('tăng số lượng thay vì thêm dòng mới khi sản phẩm đã có trong giỏ', () => {
    const { result } = renderHook(() => useCartStore());
    const product = { id: 'p1', name: 'iPhone 15', price: 25000000, image: 'https://x.com/a.jpg' };

    act(() => {
      result.current.addItem(product);
      result.current.addItem(product);
    });

    expect(result.current.items).toHaveLength(1); // Vẫn chỉ 1 dòng...
    expect(result.current.items[0].quantity).toBe(2); // ...nhưng số lượng là 2
  });
});
```

### `waitFor` — chờ những thứ bất đồng bộ

Với Hook gọi API (như `useQuery` của React Query, Chương 6), giá trị không có ngay lập tức:

```tsx
import { renderHook, waitFor } from '@testing-library/react-native';

it('tải xong danh sách sản phẩm', async () => {
  const { result } = renderHook(() => useProductsQuery(), { wrapper: QueryWrapper });

  // waitFor thử đi thử lại điều kiện bên trong cho tới khi đúng, hoặc hết 5 giây thì báo lỗi
  await waitFor(() => expect(result.current.isSuccess).toBe(true));

  expect(result.current.data).toHaveLength(20);
});
```

Với React Query, Hook cần sống bên trong `QueryClientProvider`, nên phải truyền `wrapper`:
```tsx
const QueryWrapper = ({ children }: { children: React.ReactNode }) => {
  const queryClient = new QueryClient({
    defaultOptions: { queries: { retry: false } }, // Tắt retry để test lỗi không phải chờ 3 lần thử lại
  });
  return <QueryClientProvider client={queryClient}>{children}</QueryClientProvider>;
};
```

> [!TIP]
> Quy tắc phân biệt hai hàm: **`act`** dùng khi *bạn* chủ động thay đổi State (bấm nút, gọi hàm). **`waitFor`** dùng khi *hệ thống* sẽ thay đổi State vào một lúc nào đó (API trả về, timer chạy xong).

---

## 📊 PHẦN 11.8: CODE COVERAGE — ĐO ĐỘ PHỦ CỦA TEST

### 1. Bốn chỉ số

Chạy `npx jest --coverage`, bạn nhận được bảng:

```
------------------------|---------|----------|---------|---------|-------------------
File                    | % Stmts | % Branch | % Funcs | % Lines | Uncovered Line #s
------------------------|---------|----------|---------|---------|-------------------
All files               |   72.41 |    58.33 |   66.67 |   71.92 |
 utils/formatCurrency.ts|     100 |      100 |     100 |     100 |
 store/useCartStore.ts  |   85.71 |       75 |   83.33 |   85.71 | 42,58
 screens/CheckoutScreen |   31.25 |    16.66 |      25 |   30.76 | 28-45,52-70
------------------------|---------|----------|---------|---------|-------------------
```

| Chỉ số | Đo cái gì |
|---|---|
| **Statements** | Bao nhiêu % câu lệnh đã được chạy qua |
| **Branch** | Bao nhiêu % nhánh `if/else`, `? :`, `&&` đã được thử **cả hai chiều** |
| **Functions** | Bao nhiêu % hàm đã được gọi ít nhất một lần |
| **Lines** | Bao nhiêu % dòng code đã chạy |

**Branch là chỉ số quan trọng nhất và cũng là chỉ số thấp nhất ở hầu hết dự án.** Lý do: ai cũng test "đường hạnh phúc" (đặt hàng thành công) và quên "đường đau khổ" (Server lỗi, mạng rớt) — mà bug thì gần như luôn nằm ở đường đau khổ.

### 2. Đặt ngưỡng tối thiểu (Threshold)

Coverage chỉ có ích khi nó **không được phép tụt xuống**. Cấu hình trong `package.json`:

```json
"jest": {
  "collectCoverageFrom": [
    "src/**/*.{ts,tsx}",
    "!src/**/*.d.ts",
    "!src/**/__tests__/**",
    "!src/types/**"
  ],
  "coverageThreshold": {
    "global": {
      "statements": 50,
      "branches": 40,
      "functions": 50,
      "lines": 50
    },
    "./src/utils/": {
      "statements": 90,
      "branches": 80
    }
  }
}
```

Coverage tụt dưới ngưỡng → `jest` thoát với mã lỗi khác 0 → CI báo đỏ → Pull Request bị chặn.

Chú ý mục `"./src/utils/"`: ta đặt ngưỡng **cao hơn** cho thư mục chứa hàm thuần, vì chúng dễ test nên không có lý do gì để phủ thấp. Ngược lại, đặt ngưỡng 90% cho toàn bộ màn hình UI là phi thực tế.

### 3. Vì sao "100% coverage" là mục tiêu SAI

> [!WARNING]
> Coverage đo **code đã được CHẠY QUA**, không đo **code đã được KIỂM TRA ĐÚNG**. Đoạn test sau đạt 100% coverage mà không kiểm tra một điều gì:
>
> ```ts
> it('chạy hàm', () => {
>   formatCurrency(1000); // Chạy qua rồi -> 100% coverage
>   // ...nhưng không hề có expect() nào. Hàm trả về "sai bét" vẫn xanh.
> });
> ```
>
> Đội ngũ bị ép chỉ tiêu 100% thường viết ra hàng loạt test vô nghĩa như trên: tốn công bảo trì, cho cảm giác an toàn giả tạo, và không bắt được bug nào.

**Ngưỡng hợp lý trong thực tế:**

| Loại code | Ngưỡng nên đặt | Lý do |
|---|---|---|
| Hàm thuần (`utils/`) | 90-100% | Dễ test, rẻ, giá trị cao |
| Store / Logic nghiệp vụ | 70-85% | Đây là nơi bug gây thiệt hại nhất |
| Component dùng lại (`ShopButton`) | 60-80% | Test hành vi, không test style |
| Màn hình (`Screens`) | 30-50% | Nên để E2E lo, test đơn vị ở đây rất giòn |
| Cấu hình / hằng số | Loại trừ hẳn | Không có logic để mà test |

Xem báo cáo trực quan (mở file HTML, click vào từng file để thấy dòng nào chưa được phủ, tô đỏ):
```bash
npx jest --coverage && open coverage/lcov-report/index.html
```

---

## ⚔️ PHẦN 11.9: DETOX vs MAESTRO vs APPIUM — CHỌN CÔNG CỤ E2E

| Tiêu chí | **Maestro** | **Detox** | **Appium** |
|---|---|---|---|
| Ngôn ngữ kịch bản | YAML | JavaScript/TypeScript | Java, Python, JS, Ruby... |
| Thời gian cài đặt | ~5 phút, một lệnh `curl` | Vài giờ (sửa cả Gradle + Xcode) | Nửa ngày (Appium Server, driver, SDK) |
| Phải sửa mã nguồn App? | Không | Có (thêm cấu hình build riêng) | Không |
| Cơ chế đồng bộ | Tự động thử lại tới khi thấy phần tử | "Grey box" — biết App đang bận, chờ chính xác | Ngủ/chờ thủ công, hay chập chờn |
| Độ ổn định (Flakiness) | Thấp | Rất thấp (ổn định nhất) | Cao |
| Tốc độ chạy | Nhanh | Nhanh | Chậm |
| Hỗ trợ nền tảng | Android, iOS, React Native, Flutter, Web | Chỉ React Native | Mọi thứ: Native, Hybrid, Web, cả Windows |
| Chạy song song nhiều máy | Có (bản Cloud trả phí) | Có | Có (Selenium Grid) |
| Độ dốc học tập | Rất thoải | Trung bình | Dốc |
| Cộng đồng | Đang lên nhanh | Ổn định trong giới RN | Lớn nhất, lâu đời nhất |

### Nên chọn cái nào?

- **Maestro** — mặc định cho hầu hết dự án hiện nay, và là lựa chọn của giáo trình này. Viết một flow mất 5 phút, người không biết code (QA, PM) cũng đọc và sửa được file YAML. Đánh đổi: khó biểu diễn logic phức tạp (vòng lặp, điều kiện rẽ nhánh nhiều tầng).
- **Detox** — khi bạn cần độ ổn định tuyệt đối trong CI chạy hàng trăm lần mỗi ngày. Cơ chế "grey box" của nó *biết* App đang chờ animation hay chờ network nên không bao giờ bấm hụt. Đánh đổi: cấu hình ban đầu rất mệt, chỉ dùng được với React Native.
- **Appium** — khi công ty có **cả app Native lẫn app RN lẫn web** và muốn một đội QA dùng chung một công cụ. Đánh đổi: chậm và hay chập chờn nhất.

Cùng một kịch bản đăng nhập, viết bằng ba công cụ:

```yaml
# Maestro — 6 dòng, đọc là hiểu
- launchApp
- tapOn: "you@example.com"
- inputText: "demo@shopai.com"
- tapOn: "Đăng nhập ngay"
- assertVisible: "Khám phá"
```
```js
// Detox — cần testID gắn sẵn trong mã nguồn
await element(by.id('email-input')).typeText('demo@shopai.com');
await element(by.id('login-button')).tap();
await expect(element(by.text('Khám phá'))).toBeVisible();
```
```js
// Appium — rườm rà nhất, phải tự quản lý driver và chờ đợi
const emailField = await driver.$('~email-input');
await emailField.setValue('demo@shopai.com');
await (await driver.$('~login-button')).click();
await driver.waitUntil(async () => (await driver.$('~home-title')).isDisplayed());
```

---

## 🖼️ PHẦN 11.10: VISUAL REGRESSION TESTING (KHÁI NIỆM)

Có một loại bug mà **không một công cụ nào ở trên bắt được**: giao diện vỡ.

Bạn đổi `SIZES.padding` từ `16` thành `24` trong file theme. Toàn bộ Jest test vẫn xanh (logic không đổi). Maestro vẫn PASS (chữ "Đăng nhập ngay" vẫn tồn tại, vẫn bấm được). Nhưng trên màn hình iPhone SE, nút "Thanh toán" vừa bị đẩy tụt xuống dưới mép màn hình — không ai mua hàng được nữa.

**Visual Regression Testing** giải quyết đúng vấn đề đó: chụp ảnh màn hình, so sánh từng điểm ảnh với ảnh chuẩn (baseline) đã duyệt.

```
1. Lần chạy đầu: chụp ảnh -> lưu làm ảnh chuẩn (baseline), commit vào Git
2. Lần chạy sau:  chụp ảnh mới -> so sánh với ảnh chuẩn
3. Khác nhau > ngưỡng cho phép (VD 0.1% số điểm ảnh) -> BÁO ĐỎ, đính kèm ảnh so sánh
4. Con người xem ảnh: đúng ý đồ -> duyệt ảnh mới làm chuẩn. Vỡ layout -> sửa code.
```

### Các công cụ phổ biến

| Công cụ | Đặc điểm |
|---|---|
| **Jest Snapshot** (`toMatchSnapshot`) | Miễn phí, có sẵn. Nhưng chỉ so sánh **cây JSON của component**, KHÔNG phải hình ảnh thật |
| **Maestro `assertVisualDiff`** | Tích hợp thẳng vào flow E2E bạn đã viết |
| **Chromatic / Percy / Applitools** | Dịch vụ đám mây, có giao diện duyệt ảnh, tích hợp CI. Trả phí |
| **react-native-owl** | Mã nguồn mở, chụp ảnh thật trên giả lập |

### Snapshot Test — họ hàng gần, dùng được ngay

```tsx
it('giao diện ShopButton không thay đổi ngoài ý muốn', () => {
  const tree = render(<ShopButton title="Mua ngay" onPress={() => {}} />).toJSON();
  expect(tree).toMatchSnapshot(); // Lần đầu tạo file .snap, lần sau so sánh với nó
});
```

> [!WARNING]
> **Cạm bẫy lớn nhất của Snapshot Test:** khi test đỏ, phản xạ tự nhiên của lập trình viên là gõ `jest -u` để cập nhật snapshot cho xanh trở lại — mà không hề đọc xem cái gì đã thay đổi. Làm vậy vài lần, snapshot mất sạch giá trị. Quy tắc: **mỗi lần snapshot đỏ, phải đọc `git diff` của file `.snap` và tự trả lời "đây có đúng là thay đổi mình mong muốn không?"** trước khi cập nhật.

> [!NOTE]
> Visual Regression **không bắt buộc** trong Sprint 11 (cần hạ tầng chụp ảnh và kho lưu ảnh chuẩn). Nhưng bạn cần biết nó tồn tại — đây là mảnh ghép cuối cùng của Kim tự tháp, phủ đúng khoảng trống mà Unit/Integration/E2E đều bỏ sót.

---

## 🏭 PHẦN 11.11: GITHUB ACTIONS NÂNG CAO — MATRIX, CACHE, ARTIFACT

Pipeline cơ bản ở Phần 11.5 chỉ chạy Lint + Test trên một phiên bản Node. Dự án thật cần hơn thế.

### 1. Matrix — chạy song song trên nhiều cấu hình

```yaml
jobs:
  test:
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false          # Một cấu hình đỏ, các cấu hình khác VẪN chạy tiếp
      matrix:
        node-version: [18.x, 20.x, 22.x]
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'
      - run: npm ci
      - run: npm test
```

GitHub tự dựng **3 máy ảo chạy song song**. Bạn biết ngay App có chạy được trên Node 18 (bản LTS mà nhiều công ty vẫn dùng) hay không, mà không tốn thêm thời gian chờ.

`fail-fast: false` rất quan trọng: mặc định GitHub hủy toàn bộ khi một cấu hình đỏ, khiến bạn không biết lỗi chỉ xảy ra ở Node 22 hay ở tất cả.

### 2. Cache — cắt giảm thời gian chờ

`npm ci` tải lại toàn bộ `node_modules` mỗi lần chạy, mất 2-4 phút. Cache lại:

```yaml
      - name: Cache node_modules
        uses: actions/cache@v4
        with:
          path: ~/.npm
          # Khóa cache dựa trên nội dung package-lock.json:
          # lock file không đổi -> dùng lại cache; đổi -> tự tải mới. Không bao giờ lỗi thời.
          key: ${{ runner.os }}-node-${{ hashFiles('**/package-lock.json') }}
          restore-keys: ${{ runner.os }}-node-

      - name: Cache Gradle
        uses: actions/cache@v4
        with:
          path: |
            ~/.gradle/caches
            ~/.gradle/wrapper
          key: ${{ runner.os }}-gradle-${{ hashFiles('**/*.gradle*') }}
```

Cache Gradle đặc biệt đáng giá: build Android lần đầu mất 8-10 phút, có cache chỉ còn 2-3 phút.

### 3. Artifact — giữ lại sản phẩm của mỗi lần chạy

```yaml
      - name: Chạy test kèm coverage
        run: npm test -- --coverage

      - name: Lưu báo cáo coverage
        uses: actions/upload-artifact@v4
        if: always()        # Lưu cả khi test ĐỎ — lúc đó mới cần xem báo cáo nhất
        with:
          name: coverage-report
          path: coverage/
          retention-days: 7

      - name: Build APK debug
        run: cd android && ./gradlew assembleDebug

      - name: Lưu APK cho QA tải về
        uses: actions/upload-artifact@v4
        with:
          name: shopai-debug-apk
          path: android/app/build/outputs/apk/debug/app-debug.apk
```

Sau mỗi lần chạy, đội QA vào tab Actions của GitHub, tải thẳng file APK về máy để kiểm thử — không cần làm phiền lập trình viên build tay.

### 4. Ghép thành Pipeline nhiều job có phụ thuộc

```yaml
jobs:
  lint:
    runs-on: ubuntu-latest
    steps: [...]

  test:
    needs: lint          # Lint đỏ thì không tốn tài nguyên chạy test
    runs-on: ubuntu-latest
    steps: [...]

  build-android:
    needs: test          # Chỉ build khi test đã xanh
    if: github.ref == 'refs/heads/main'   # Và chỉ build trên nhánh main
    runs-on: ubuntu-latest
    steps: [...]
```

Kết quả là một đồ thị công việc rõ ràng: `lint → test → build-android`, mỗi bước là một cổng chất lượng (Quality Gate).

---

## 🚄 PHẦN 11.12: FASTLANE — FASTFILE HOÀN CHỈNH CHO ANDROID BETA

Phần 11.5 mới chỉ phác thảo Fastlane. Dưới đây là một `Fastfile` đầy đủ cho luồng phát hành Beta Android — đọc để hiểu cấu trúc, **không cần chạy trong lớp học**.

### 1. Cài đặt

```bash
brew install fastlane          # macOS
# hoặc: gem install fastlane

cd android
fastlane init                  # Sinh thư mục fastlane/ với Fastfile + Appfile
```

### 2. `android/fastlane/Appfile`

```ruby
json_key_file("fastlane/google-play-service-account.json") # Khóa Service Account của Google Play
package_name("com.shopai.app")  # Trùng với applicationId ở Chương 10
```

### 3. `android/fastlane/Fastfile`

```ruby
default_platform(:android)

platform :android do

  desc "Chạy toàn bộ Unit Test của phần Android"
  lane :test do
    gradle(task: "test")
  end

  desc "Build và đẩy lên kênh Internal Testing của Google Play"
  lane :beta do
    # 1. Đảm bảo cây Git sạch — tránh đóng gói nhầm code đang sửa dở
    ensure_git_status_clean

    # 2. Tự tăng versionCode theo số bản build gần nhất trên Play Console
    #    (áp dụng chiến lược versioning ở Chương 10, Phần 10.10)
    previous_build_number = google_play_track_version_codes(
      track: "internal",
    ).max
    increment_version_code(
      gradle_file_path: "app/build.gradle",
      version_code: previous_build_number + 1,
    )

    # 3. Dọn sạch bản build cũ
    gradle(task: "clean")

    # 4. Đóng gói AAB đã ký (dùng Keystore đã tạo ở Chương 10, Phần 10.6)
    gradle(
      task: "bundle",
      build_type: "Release",
      properties: {
        "android.injected.signing.store.file" => ENV["KEYSTORE_PATH"],
        "android.injected.signing.store.password" => ENV["KEYSTORE_PASSWORD"],
        "android.injected.signing.key.alias" => ENV["KEY_ALIAS"],
        "android.injected.signing.key.password" => ENV["KEY_PASSWORD"],
      },
    )

    # 5. Tải lên Google Play, kênh internal
    upload_to_play_store(
      track: "internal",
      aab: "app/build/outputs/bundle/release/app-release.aab",
      skip_upload_metadata: true,
      skip_upload_images: true,
      skip_upload_screenshots: true,
      release_status: "completed",
    )

    # 6. Báo cho cả đội biết trên Slack
    slack(
      message: "🚀 ShopAI Beta mới đã lên Google Play Internal Testing!",
      success: true,
    ) if ENV["SLACK_URL"]
  end

  desc "Thăng cấp bản internal hiện tại lên kênh Production"
  lane :promote_to_production do
    upload_to_play_store(
      track: "internal",
      track_promote_to: "production",
      skip_upload_aab: true,      # Không upload lại file, chỉ đổi kênh phát hành
      rollout: "0.1",             # Phát hành từ từ cho 10% người dùng trước
    )
  end

  # Tự động chạy khi có bất kỳ lane nào lỗi
  error do |lane, exception|
    slack(
      message: "❌ Fastlane lane #{lane} thất bại: #{exception.message}",
      success: false,
    ) if ENV["SLACK_URL"]
  end
end
```

Chạy:
```bash
cd android
fastlane beta
fastlane promote_to_production
```

> [!TIP]
> **Chú ý `rollout: "0.1"` (Staged Rollout).** Đây là thực hành bắt buộc ở mọi công ty nghiêm túc: phát hành cho 10% người dùng trước, theo dõi Dashboard Crashlytics (Chương 10) vài giờ. Tỉ lệ không-crash vẫn trên 99.5% → tăng dần lên 25%, 50%, 100%. Phát hiện crash → dừng phát hành ngay, chỉ 10% người dùng bị ảnh hưởng thay vì toàn bộ. Đây chính là lúc mọi thứ bạn học ở Chương 10 và 11 ghép lại thành một hệ thống hoàn chỉnh.

### 4. Gọi Fastlane từ GitHub Actions

```yaml
  deploy-beta:
    needs: test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: ruby/setup-ruby@v1
        with: { ruby-version: '3.2', bundler-cache: true }

      - name: Giải mã Keystore từ GitHub Secrets
        run: echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 -d > android/app/release.keystore

      - name: Chạy Fastlane beta
        working-directory: android
        env:
          KEYSTORE_PATH: app/release.keystore
          KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
          KEY_ALIAS: ${{ secrets.KEY_ALIAS }}
          KEY_PASSWORD: ${{ secrets.KEY_PASSWORD }}
        run: bundle exec fastlane beta
```

> [!CAUTION]
> File Keystore **không bao giờ** được commit lên Git (Chương 10, Phần 10.6). Cách chuẩn để đưa nó vào CI: mã hóa Base64 (`base64 -i shopai-release.keystore | pbcopy`), dán chuỗi đó vào **GitHub Secrets**, rồi giải mã lúc chạy như đoạn trên. Mật khẩu cũng để trong Secrets, không bao giờ để trong file YAML.

---

## 🪝 PHẦN 11.13: PRE-COMMIT HOOK — CHẶN LỖI NGAY TỪ MÁY LẬP TRÌNH VIÊN

CI bắt lỗi sau khi đã push — tức là bạn phải chờ 3-5 phút mới biết mình quên format code. **Git Hook** bắt lỗi ngay lúc commit, phản hồi trong 3 giây.

### 1. Husky + lint-staged

```bash
npm install --save-dev husky lint-staged
npx husky init
```

Tạo `.husky/pre-commit`:
```bash
npx lint-staged
```

Cấu hình trong `package.json`:
```json
"lint-staged": {
  "src/**/*.{ts,tsx}": [
    "eslint --fix",
    "prettier --write"
  ],
  "src/**/*.{json,md}": [
    "prettier --write"
  ]
}
```

**Điểm mấu chốt nằm ở chữ "staged"**: `lint-staged` chỉ kiểm tra những file bạn vừa `git add`, không quét cả dự án. Nhờ vậy hook chạy trong 1-3 giây thay vì 30 giây — đủ nhanh để không ai muốn bỏ qua nó.

### 2. Thêm hook cho commit message

```bash
npm install --save-dev @commitlint/cli @commitlint/config-conventional
```

`commitlint.config.js`:
```js
module.exports = { extends: ['@commitlint/config-conventional'] };
```

`.husky/commit-msg`:
```bash
npx --no -- commitlint --edit $1
```

Từ giờ commit message phải theo chuẩn **Conventional Commits**:
```
feat: them man hinh AI Chat
fix: sua loi crash khi gio hang rong
test: them unit test cho useCartStore
chore: cap nhat dependencies
```

Lợi ích không chỉ là đẹp: từ những tiền tố này, công cụ có thể **tự sinh CHANGELOG** và **tự quyết định tăng số version** (`feat` → tăng MINOR, `fix` → tăng PATCH — đúng chuẩn Semantic Versioning ở Chương 10, Phần 10.10).

### 3. Chạy test trước khi push

`.husky/pre-push`:
```bash
npm test -- --onlyChanged
```

Cờ `--onlyChanged` chỉ chạy các test liên quan tới file bạn vừa đổi — vài giây thay vì vài phút.

> [!IMPORTANT]
> **Hook không thay thế được CI.** Bất kỳ ai cũng có thể bỏ qua hook bằng `git commit --no-verify`, và hook chỉ chạy trên máy đã cài `npm install`. Hãy xem hook là **lớp phòng thủ thứ nhất** (nhanh, thân thiện, bắt lỗi vặt) còn CI là **lớp phòng thủ cuối cùng** (chậm hơn nhưng không ai lách được).

---

## 📋 PHẦN 11.14: TEST PLAN — KẾ HOẠCH KIỂM THỬ CHO SHOPAI

Trước khi viết dòng test đầu tiên, một kỹ sư chuyên nghiệp trả lời ba câu hỏi: **Test cái gì? Test ở tầng nào? Bao nhiêu là đủ?**

### 1. Ma trận phủ kiểm thử cho ShopAI

| Tính năng | Chương | Unit (Jest) | Integration (RNTL) | E2E (Maestro) | Ưu tiên |
|---|---|---|---|---|---|
| `formatCurrency` | 6, 11 | ✅ Bắt buộc | — | — | Cao |
| `useCartStore` (thêm/xóa/tổng tiền) | 6 | ✅ Bắt buộc | — | — | **Rất cao** (liên quan tiền) |
| `ShopButton` (press, disabled) | 3 | — | ✅ Bắt buộc | — | Cao |
| `ShopInput` (nhập liệu, lỗi) | 3 | — | ⭕ Nên có | — | Trung bình |
| Đăng nhập | 5 | — | ⭕ Nên có | ✅ Bắt buộc | Cao |
| Danh sách sản phẩm | 6, 9 | ✅ (mock fetch) | ⭕ Nên có | ✅ Bắt buộc | Cao |
| Chi tiết sản phẩm | 5, 9 | ⭕ (mock 404) | — | ⭕ Nên có | Trung bình |
| Thêm vào giỏ hàng | 6 | ✅ Bắt buộc | ⭕ Nên có | ✅ Bắt buộc | **Rất cao** |
| Đặt hàng (Checkout) | 6, 9 | ✅ (mock API lỗi) | — | ✅ Bắt buộc | **Rất cao** (liên quan tiền) |
| Quét mã QR | 7 | — | — | ❌ Không khả thi | Thấp (cần phần cứng) |
| Chatbot AI | 8, 9 | ⭕ (mock reply) | — | ⭕ Nên có | Trung bình |

Chú thích: ✅ Bắt buộc — ⭕ Nên có — ❌ Không khả thi

### 2. Nguyên tắc quyết định "test ở tầng nào"

- Logic thuần, không có UI → **Unit Test**. Rẻ nhất, chạy nhanh nhất, viết trước tiên.
- Component có tương tác → **Integration Test (RNTL)**. Test *hành vi*, không test màu sắc hay khoảng cách.
- Luồng đi xuyên nhiều màn hình → **E2E (Maestro)**. Đắt và chậm, chỉ dành cho các luồng **sinh ra tiền**.

> [!TIP]
> Câu hỏi lọc rất hiệu quả: *"Nếu tính năng này hỏng mà không ai phát hiện trong 24 giờ, công ty mất bao nhiêu tiền?"* Mất nhiều → đầu tư test kỹ ở nhiều tầng. Mất ít → một test đơn giản là đủ. Đây là lý do luồng Giỏ hàng và Đặt hàng của ShopAI được đánh dấu "Rất cao" còn màn hình quét QR chỉ ở mức "Thấp".

### 3. Ca kiểm thử phải viết cho mỗi tính năng

Với mỗi tính năng, luôn nghĩ theo bốn nhóm:

| Nhóm | Ví dụ với "Thêm vào giỏ hàng" |
|---|---|
| **Đường hạnh phúc** | Thêm 1 sản phẩm → giỏ có 1 món, tổng tiền đúng |
| **Trường hợp biên** | Thêm cùng sản phẩm 2 lần → 1 dòng, quantity = 2 |
| **Đường lỗi** | Thêm sản phẩm không có giá → không làm sập App |
| **Trạng thái rỗng** | Giỏ hàng trống → nút Thanh toán bị khóa |

Đa số lập trình viên mới chỉ viết nhóm đầu tiên. Ba nhóm còn lại mới là nơi bug thật sự ẩn nấp.

### 4. Bảng Quality Gates của ShopAI

| Cổng | Chạy khi nào | Điều kiện phải đạt | Ai chịu trách nhiệm |
|---|---|---|---|
| Pre-commit | Mỗi lần `git commit` | ESLint + Prettier sạch | Lập trình viên |
| Pre-push | Mỗi lần `git push` | Test liên quan đều xanh | Lập trình viên |
| CI — Lint | Mỗi Pull Request | 0 lỗi ESLint | CI tự động |
| CI — Unit + Integration | Mỗi Pull Request | 100% test xanh, coverage ≥ ngưỡng | CI tự động |
| CI — Build | Merge vào `main` | Build APK thành công | CI tự động |
| E2E | Trước mỗi lần phát hành | Các flow Maestro trọng yếu PASS | QA |
| Staged Rollout | Sau khi phát hành | Tỉ lệ không-crash > 99.5% | DevOps |

---

## 🖥️ PHẦN 11.15: KIỂM THỬ BACKEND NESTJS (JEST UNIT TEST + SUPERTEST E2E)

Toàn bộ Kim tự tháp kiểm thử ở Phần 11.1 vừa học áp dụng cho **Mobile** (React Native). Nhưng ShopAI còn có nguyên một **Server NestJS** (`shopai-backend`, dựng ở Chương 9) đứng giữa Mobile và thế giới bên ngoài (dữ liệu sản phẩm, đơn hàng, Gemini AI). Nếu không test tầng này, một lần sửa nhầm công thức tính tiền trong `OrderService` có thể âm thầm cho phép đặt hàng với giá `0đ` mà không ai phát hiện ra cho tới khi xem báo cáo doanh thu cuối tháng.

Tin vui: Backend NestJS có **kiến trúc kiểm thử y hệt** Mobile, chỉ khác đúng 1 công cụ ở tầng trên cùng:

| Tầng | Mobile (đã học Phần 11.1-11.10) | Backend NestJS |
|---|---|---|
| Unit | Jest thuần trên hàm/Zustand Store | Jest thuần trên **Service** (logic nghiệp vụ: tính tiền, kiểm tra mật khẩu...) |
| Integration/E2E | RNTL (render Component) / Maestro (robot chạm màn hình) | **Supertest** — gọi thẳng HTTP Request vào một Server NestJS ảo dựng trong RAM, không cần mở Postman hay máy ảo |

> [!TIP]
> **Tin cực vui cho Backend:** `nest new` (Chương 9) đã tự cấu hình sẵn Jest trong `package.json` VÀ tự sinh sẵn 1 file test mẫu `test/app.e2e-spec.ts` — không cần cài thêm `@testing-library`, không cần viết `jest.setup.js` mock Native Module như bên Mobile (Phần 11.6). Backend chạy trên Node thuần, không có khái niệm "Native Module" cần giả lập.

### 1. Sprint 9 đã có JWT + Prisma — Sprint 11 CHỈ viết Test

> [!IMPORTANT]
> **Không dựng lại `AuthModule`.** Sprint 9 đã triển khai thật: `AuthModule`, `JwtAuthGuard`, Prisma `User`, `POST /api/auth/login`, Orders có Guard. Sprint 11 **chỉ thêm** file `*.spec.ts` / e2e — **cấm** tạo `users.data.ts` in-memory hay ghi đè `auth.service.ts` của Chương 9 (sẽ mất user đã seed và phá DB).

Trước khi viết test, xác nhận nhanh (Server đang chạy):
```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@shopai.com","password":"123456"}'
# -> phải có accessToken (đúng tài khoản seed Chương 9)
```

Nếu login fail: quay lại Sprint 9 (migrate + seed), **không** copy Auth in-memory ở dưới đây (đã xóa khỏi giáo trình).

### 2. Chiến lược mock khi Unit Test `AuthService` (Prisma)

`AuthService` Chương 9 tiêm `PrismaService` + `JwtService`. Unit Test **không** nối DB thật — mock Prisma:

```typescript
// Ý tưởng (chi tiết đầy đủ ở mục 3):
{
  provide: PrismaService,
  useValue: {
    user: {
      findUnique: jest.fn(), // giả lập user tìm thấy / không thấy
    },
  },
}
```

E2E (Supertest) thì gọi HTTP thật vào Nest TestingModule — dùng cùng `DATABASE_URL` sqlite test hoặc DB dev đã seed (đơn giản cho lớp: seed `demo@shopai.com` trước khi chạy e2e).

### 3. Unit Test cho `AuthService` bằng `Test.createTestingModule` của NestJS

NestJS có bộ công cụ test riêng (`@nestjs/testing`) — thay vì `jest.mock()` cả Module như bên Mobile (Phần 11.6), NestJS cho phép **ghi đè (override) từng Provider** ngay trong Dependency Injection Container, tận dụng đúng cơ chế DI đã học ở Phần 9.2.

Tạo file `src/auth/auth.service.spec.ts` (quy ước NestJS: file test Unit đặt CÙNG CẤP với file nguồn, hậu tố `.spec.ts` — khác quy ước `__tests__/` bên Mobile). **Mock `PrismaService`** — đúng `AuthService` Chương 9 (không dùng `users.data.ts`):

```typescript
// src/auth/auth.service.spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { JwtService } from '@nestjs/jwt';
import { UnauthorizedException } from '@nestjs/common';
import * as bcrypt from 'bcrypt';
import { AuthService } from './auth.service';
import { PrismaService } from '../prisma/prisma.service';

describe('AuthService', () => {
  let service: AuthService;
  let jwtService: JwtService;
  let prisma: { user: { findUnique: jest.Mock } };

  const passwordHash = bcrypt.hashSync('123456', 10); // khớp seed Sprint 9

  beforeEach(async () => {
    prisma = {
      user: {
        findUnique: jest.fn(),
      },
    };

    const module: TestingModule = await Test.createTestingModule({
      providers: [
        AuthService,
        { provide: PrismaService, useValue: prisma },
        {
          provide: JwtService,
          useValue: { sign: jest.fn().mockReturnValue('fake.jwt.token') },
        },
      ],
    }).compile();

    service = module.get(AuthService);
    jwtService = module.get(JwtService);
  });

  describe('login', () => {
    it('trả về accessToken khi email và mật khẩu đều đúng', async () => {
      prisma.user.findUnique.mockResolvedValue({
        id: 'u_001',
        email: 'demo@shopai.com',
        passwordHash,
      });

      const result = await service.login('demo@shopai.com', '123456');

      expect(result.accessToken).toBe('fake.jwt.token');
      expect(result.user.email).toBe('demo@shopai.com');
      expect(jwtService.sign).toHaveBeenCalled();
    });
  });

  describe('validateUser', () => {
    it('ném UnauthorizedException khi email không tồn tại', async () => {
      prisma.user.findUnique.mockResolvedValue(null);
      await expect(service.validateUser('khong_ton_tai@shopai.com', '123456')).rejects.toThrow(
        UnauthorizedException,
      );
    });

    it('ném UnauthorizedException khi sai mật khẩu', async () => {
      prisma.user.findUnique.mockResolvedValue({
        id: 'u_001',
        email: 'demo@shopai.com',
        passwordHash,
      });
      await expect(service.validateUser('demo@shopai.com', 'sai_mat_khau')).rejects.toThrow(
        UnauthorizedException,
      );
    });
  });
});
```

**Giải thích các khối quan trọng:**

| Khối | Giải thích |
|---|---|
| `Test.createTestingModule({ providers: [...] })` | Tương đương `@Module({...})` nhưng chỉ để phục vụ TEST |
| `{ provide: PrismaService, useValue: prisma }` | **Mock DB** — không đụng SQLite thật; `findUnique` do bạn quyết định trả user / `null` |
| `{ provide: JwtService, useValue: { sign: jest.fn()... } }` | Không cần `JWT_SECRET` thật khi Unit Test |
| `rejects.toThrow(UnauthorizedException)` | Đúng loại lỗi Nest sẽ dịch thành HTTP `401` |

Chạy test:
```bash
npx jest auth.service.spec.ts
```

> [!TIP]
> Viết thêm `src/order/order.service.spec.ts` (mock repository/Prisma) để Unit Test công thức "Server tự tính lại tổng tiền" (Phần 9.12) — logic liên quan **tiền**, cùng mức ưu tiên cao như `useCartStore` ở Mobile.

### 4. E2E Test bằng Supertest cho `POST /api/auth/login` và `POST /api/orders`

**Supertest** là thư viện gọi HTTP Request thẳng vào một Server Node đang chạy **trong bộ nhớ** — không cần `npm run start` thật, không tốn cổng mạng thật, không cần Postman. NestJS tự tạo ra Server đó thông qua `app.getHttpServer()`.

Tạo file `test/auth-orders.e2e-spec.ts` (thư mục `test/` ở gốc `shopai-backend`, đúng quy ước Nest CLI đã tạo sẵn từ Chương 9):
```typescript
// test/auth-orders.e2e-spec.ts
import { Test, TestingModule } from '@nestjs/testing';
import { INestApplication, ValidationPipe } from '@nestjs/common';
import * as request from 'supertest';
import { AppModule } from '../src/app.module';

describe('Auth + Orders (e2e)', () => {
  let app: INestApplication;
  let accessToken: string; // Lưu lại Token từ nhóm test Login, dùng tiếp cho nhóm test Orders bên dưới

  beforeAll(async () => {
    // Dựng TOÀN BỘ App thật (import AppModule) — khác Unit Test ở mục 3 chỉ dựng 1 Module nhỏ
    const moduleFixture: TestingModule = await Test.createTestingModule({
      imports: [AppModule],
    }).compile();

    app = moduleFixture.createNestApplication();
    // Phải bật lại ValidationPipe giống hệt main.ts (Chương 9, Bước 7b) — TestingModule
    // KHÔNG tự đọc cấu hình từ main.ts, phải khai báo lại thủ công ở đây
    app.useGlobalPipes(new ValidationPipe({ whitelist: true, forbidNonWhitelisted: true }));
    await app.init();
  });

  afterAll(async () => {
    await app.close(); // Đóng Server ảo sau khi test xong — thiếu dòng này Jest sẽ treo, không tự thoát
  });

  describe('POST /api/auth/login', () => {
    it('trả về 201 kèm accessToken khi đăng nhập đúng', async () => {
      const res = await request(app.getHttpServer())
        .post('/api/auth/login')
        .send({ email: 'demo@shopai.com', password: '123456' });

      expect(res.status).toBe(201); // NestJS mặc định trả 201 cho @Post(), KHÔNG phải 200 như GET
      expect(res.body.accessToken).toEqual(expect.any(String));

      accessToken = res.body.accessToken; // Giữ lại để nhóm test Orders bên dưới dùng
    });

    it('trả về 401 khi sai mật khẩu', async () => {
      const res = await request(app.getHttpServer())
        .post('/api/auth/login')
        .send({ email: 'demo@shopai.com', password: 'sai_mat_khau' });

      expect(res.status).toBe(401);
    });

    it('trả về 400 khi email sai định dạng (ValidationPipe chặn trước khi vào AuthService)', async () => {
      const res = await request(app.getHttpServer())
        .post('/api/auth/login')
        .send({ email: 'khong-phai-email', password: '123456' });

      expect(res.status).toBe(400);
    });
  });

  describe('POST /api/orders (bảo vệ bằng JwtAuthGuard)', () => {
    // Khớp đúng dữ liệu mẫu backend_prod_0 và công thức tính tiền Server đã dùng ở Chương 9 (curl mẫu, Bước 7d)
    const validOrder = {
      items: [{ productId: 'backend_prod_0', quantity: 2 }],
      total: 2000000,
    };

    it('trả về 401 khi KHÔNG gửi kèm Token', async () => {
      const res = await request(app.getHttpServer()).post('/api/orders').send(validOrder);

      expect(res.status).toBe(401);
    });

    it('trả về 401 khi gửi Token SAI/giả mạo', async () => {
      const res = await request(app.getHttpServer())
        .post('/api/orders')
        .set('Authorization', 'Bearer token_gia_mao_khong_hop_le')
        .send(validOrder);

      expect(res.status).toBe(401);
    });

    it('trả về 201 khi gửi kèm Token hợp lệ', async () => {
      const res = await request(app.getHttpServer())
        .post('/api/orders')
        .set('Authorization', `Bearer ${accessToken}`) // Token thật lấy từ nhóm test Login ở trên
        .send(validOrder);

      expect(res.status).toBe(201);
      expect(res.body.orderId).toEqual(expect.stringContaining('ORD-'));
      expect(res.body.total).toBe(2000000);
    });
  });
});
```

**Giải thích từng khối:**

| Khối | Giải thích |
|---|---|
| `Test.createTestingModule({ imports: [AppModule] })` | Khác Unit Test ở mục 3 (chỉ dựng 1 Module nhỏ), E2E Test dựng **TOÀN BỘ** cây Module thật của App — đúng tinh thần "test như 1 Request thật đi từ đầu tới cuối" |
| `app.getHttpServer()` | Trả về Server HTTP nội bộ mà Nest vừa tạo — Supertest gọi Request thẳng vào đây, không qua mạng thật, nên chạy rất nhanh |
| `beforeAll`/`afterAll` (thay vì `beforeEach`) | Chỉ cần dựng App **1 LẦN DUY NHẤT** cho cả file test (dựng App tốn thời gian hơn Unit Test khá nhiều), các `it()` bên trong dùng chung 1 App |
| `accessToken` khai báo ở ngoài `describe` | Kỹ thuật "test có thứ tự phụ thuộc" — nhóm test Login chạy trước, lưu lại Token thật, nhóm test Orders dùng lại đúng Token đó để mô phỏng luồng thật (Đăng nhập xong mới Đặt hàng được) |
| `res.status).toBe(201)` cho Login | Dễ nhầm với `200` — NestJS mặc định trả **201 Created** cho mọi method `@Post()` trừ khi bạn tự đổi bằng `@HttpCode()` |

Chạy E2E Test (Nest CLI đã cấu hình sẵn script `test:e2e` từ lúc `nest new` ở Chương 9):
```bash
npm run test:e2e
```

> [!WARNING]
> **Bẫy hay gặp nhất khi mới viết E2E Test cho NestJS:** quên gọi `app.useGlobalPipes(new ValidationPipe(...))` trong `beforeAll`. `TestingModule` chỉ dựng lại cây Module (Controller/Service/Provider), **KHÔNG** tự đọc lại các dòng cấu hình toàn cục nằm trong `main.ts` (`ValidationPipe`, `helmet()`, `SwaggerModule`...) — mọi cấu hình toàn cục cần dùng trong lúc test phải khai báo lại thủ công ngay trong file test.

> [!TIP]
> So sánh nhanh 2 tầng vừa viết: Unit Test (mục 3) trả lời câu hỏi *"Công thức trong `AuthService` có đúng không?"* — chạy trong mili-giây, không đụng HTTP/Database. E2E Test (mục 4) trả lời câu hỏi *"Toàn bộ dây chuyền Guard → Pipe → Controller → Service có phối hợp đúng không?"* — chạy chậm hơn nhưng bắt được lỗi ở tầng "nối dây" (VD: quên gắn `@UseGuards`, quên đăng ký Module) mà Unit Test không bao giờ phát hiện ra.

### 5. Wire vào CI — thêm job `backend-test` (tùy chọn)

Nếu `shopai-backend` nằm CHUNG repository với App Mobile (monorepo), có thể thêm 1 job **độc lập** vào `.github/workflows/ci.yml` đã dựng ở Phần 11.11 (Bước 10b), chạy song song với job `test` của Mobile — vì 2 project không đụng chạm code của nhau nên không cần khai báo `needs` giữa chúng:

```yaml
  # ===== JOB MỚI: Test Backend NestJS (độc lập với job `test` của Mobile) =====
  backend-test:
    name: Backend NestJS Test (Jest + Supertest)
    runs-on: ubuntu-latest
    defaults:
      run:
        working-directory: shopai-backend   # Thư mục con chứa project NestJS riêng biệt trong repo
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
          cache-dependency-path: shopai-backend/package-lock.json

      - run: npm ci

      - name: Unit Test (AuthService, OrderService...)
        run: npm test

      - name: E2E Test (Supertest — login + orders)
        env:
          JWT_SECRET: test_secret_chi_dung_trong_ci_khong_dung_that
          JWT_EXPIRES_IN: 1d
        run: npm run test:e2e
```

> [!NOTE]
> **Vì sao đánh dấu "tùy chọn"?** Nếu `shopai-backend` sống ở một **repository RIÊNG** (không phải monorepo chung với Mobile), job này nên nằm trong file `.github/workflows/ci.yml` của CHÍNH repository đó, không nhét chung vào workflow của App Mobile. Cấu trúc job (checkout → setup-node → npm ci → test → test:e2e) giữ nguyên, chỉ bỏ `working-directory` vì lúc đó `package.json` đã nằm ngay gốc repo.

> [!IMPORTANT]
> Biến `JWT_SECRET` trong CI chỉ cần là một chuỗi bất kỳ (không cần trùng với `.env` thật) — mục đích của job này là kiểm tra LOGIC (Guard có chặn đúng không, Token có ký/giải mã khớp không), không phải kiểm tra bảo mật của chuỗi bí mật thật. Chuỗi `JWT_SECRET` dùng ở Production phải khác hoàn toàn và nằm trong GitHub Secrets — không bao giờ hard-code vào file YAML (đúng nguyên tắc đã học ở Phần 11.12 với Keystore).

---

## 🚀 THỰC CHIẾN SHOPAI (SPRINT 11: MAESTRO E2E, JEST UNIT TEST, RNTL INTEGRATION TEST & CI/CD)

**User Story:** *"Là một Kỹ sư trưởng, tôi muốn thiết lập một hệ thống tự động: mỗi khi có ai đó đẩy code lên GitHub, Robot phải tự chạy kiểm tra chất lượng code (Lint, Unit Test) và mô phỏng một người dùng thật đăng nhập vào ShopAI (E2E), để tôi không bao giờ phải lo lắng một dòng code mới sẽ làm sập tính năng cũ mà không ai biết."*


### 📋 Khung thực hành chương (đọc trước khi gõ code)

> Đây là **bài thực hành của Chương 11** (không phải “lab mỗi ngày”). Làm hết Sprint này = đạt mục tiêu chương. Hoàn thành đủ 11 Sprint = sản phẩm ShopAI theo `SHOPAI_HOAN_THIEN.md`.

| Hạng mục | Nội dung |
|----------|----------|
| **Thời lượng gợi ý** | 6–9 tiết |
| **Độ khó chương** | ★★★★★ |
| **Đầu vào bắt buộc** | Sprint 9–10 PASS — app gần hoàn thiện. |
| **Đầu ra sản phẩm** | Jest+RNTL+Maestro Mobile; Unit+Supertest Nest; CI GitHub Actions — ShopAI đạt checklist `SHOPAI_HOAN_THIEN.md`. |
| **Cách làm** | Làm **tuần tự từng Bước**. Gặp mốc ✓ bên dưới mà FAIL → dừng, sửa, rồi mới sang bước sau. |
| **Nghiệm thu cuối khóa** | Đối chiếu `SHOPAI_HOAN_THIEN.md` — mỗi Sprint chỉ tích thêm ô, không phá tính năng cũ. |

### ✓ Kiểm chứng theo mốc (trong lúc làm)

- **Sau Bước 3–6b:** Maestro login PASS; cart store test PASS.
- **Sau Bước 8–10b:** ShopButton RNTL PASS; CI lint+test xanh.
- **Sau Bước 11d–11f:** Auth Nest không bị ghi đè; e2e 401/201 PASS.

> [!TIP]
> Xong Sprint 11, mở `SHOPAI_HOAN_THIEN.md` và tick các ô thuộc chương này. Mục tiêu cuối khóa: **mọi ô A/B/C/D (+ E đề cương) đều xanh** trong `SHOPAI_HOAN_THIEN.md` — đó mới là ShopAI hoàn thiện đẳng cấp.

### Yêu cầu Nghiệm thu (Acceptance Criteria):
1. Cài đặt thành công Maestro CLI, viết được kịch bản `.maestro/login_home.yaml` mô phỏng đúng luồng Đăng nhập → Trang chủ của ShopAI (dùng đúng chữ hiển thị trên UI thật của Chương 5/6).
2. Chạy `maestro test .maestro/login_home.yaml` và kịch bản PASS trên máy giả lập/máy thật.
3. Tách hàm `formatCurrency` ra file riêng `src/utils/formatCurrency.ts`, có ít nhất 1 file Jest Unit Test PASS cho hàm này.
4. **[Đề cương]** Có ít nhất 1 file Integration Test dùng **React Native Testing Library** cho `ShopButton` (render + `fireEvent.press` + kiểm tra `onPress`/`disabled`), PASS khi chạy `npx jest`.
5. **[Đề cương]** Biết mở và dùng được **React Native DevTools** (phím `j` trong Metro/Dev Menu) để xem cây Component và Profiler; hiểu vai trò của **Flipper** (Network Inspector) dù không bắt buộc cài đặt đầy đủ trong lớp học.
6. Có file `.github/workflows/ci.yml` tự động chạy Lint + Test mỗi khi `git push`.
7. Hiểu vì sao Fastlane tự động Submit lên Store là bước "advanced" cần tài khoản Apple/Google thật, không bắt buộc chạy được trong lớp học.
8. Có Jest Test cho **`useCartStore`** (Zustand, Chương 6) kiểm tra được `addItem`, gộp số lượng, `totalPrice` và `clearCart` — đây là logic liên quan tới **tiền**, ưu tiên cao nhất trong Test Plan (Phần 11.14).
9. Có Maestro flow **`cart_checkout.yaml`** đi hết luồng Đăng nhập → Trang chủ → Tab Giỏ hàng.
10. `package.json` có script **`test:coverage`** và cấu hình **`coverageThreshold`** (Phần 11.8).
11. *(Tùy chọn)* Cài **Husky + lint-staged** chặn code chưa format ngay lúc `git commit`.
12. **[CRITICAL — Backend]** Xác nhận `AuthModule` + `JwtAuthGuard` từ Sprint 9 còn nguyên; viết Unit Test + Supertest (Phần 11.15) — **không** ghi đè Auth bằng in-memory.
13. **[CRITICAL — Backend]** Có Jest Unit Test cho `AuthService` (hoặc `OrderService`), PASS khi chạy `npx jest` trong `shopai-backend` (Phần 11.15 mục 3).
14. **[CRITICAL — Backend]** Có Supertest E2E Test kiểm chứng đúng: `POST /api/auth/login` trả về `accessToken`; `POST /api/orders` trả `401` khi thiếu Token và `201` khi có Token hợp lệ (Phần 11.15 mục 4).
15. *(Tùy chọn)* Có job `backend-test` độc lập trong CI chạy Unit Test + E2E Test của `shopai-backend` (Phần 11.15 mục 5).

---

### PHẦN 1: Kiểm thử E2E với Maestro cho luồng ShopAI thật

#### Bước 1: Cài đặt Maestro CLI (macOS)
Mở Terminal, chạy lệnh cài đặt chính thức của Maestro:
```bash
curl -Ls "https://get.maestro.mobile.dev" | bash
```
Sau khi cài xong, mở lại Terminal (hoặc chạy `source ~/.zshrc`/`source ~/.bashrc`) rồi kiểm tra:
```bash
maestro --version
```
*(Yêu cầu máy đã cài Java JDK — nếu thiếu, Maestro sẽ nhắc cài qua `brew install openjdk`).*

#### Bước 2: Xác định đúng `appId` của ShopAI
Kịch bản Maestro cần biết chính xác `appId` (Android) / Bundle Identifier (iOS) để mở đúng App. Mở file `android/app/build.gradle`, tìm dòng:
```groovy
android {
    defaultConfig {
        applicationId "com.shopai.app"   // ⬅️ Đây chính là appId cần dùng cho Maestro
        ...
    }
}
```
*(Trên iOS, mở `ios/ShopAI.xcodeproj` bằng Xcode, xem `Bundle Identifier` ở tab General — thường được đặt trùng với `applicationId` để đồng bộ 2 nền tảng).*

#### Bước 3: Viết kịch bản `.maestro/login_home.yaml`
Tạo thư mục `.maestro/` ở gốc dự án, tạo file `login_home.yaml`. Kịch bản này mô phỏng đúng những gì học viên đã xây ở Chương 5 (`LoginScreen` dùng `ShopInput` với placeholder "you@example.com" / "Ít nhất 6 ký tự", nút "Đăng nhập ngay") và Chương 6 (`HomeScreen` có header "Khám phá"):

```yaml
appId: com.shopai.app
---
- launchApp
# ShopInput hiển thị placeholder khi trống -> Maestro tìm text placeholder để tap đúng ô nhập
- tapOn: "you@example.com"
- inputText: "demo@shopai.com"
- tapOn: "Ít nhất 6 ký tự"
- inputText: "123456"
- tapOn: "Đăng nhập ngay"
# Chờ chuyển màn hình rồi kiểm tra đã vào đúng HomeScreen
- assertVisible: "Khám phá"
```

> [!TIP]
> Maestro tìm phần tử theo **text hiển thị trên màn hình**, không cần biết `testID` hay cấu trúc code bên trong — đúng tinh thần "test như người dùng thật cầm máy" đã học ở Phần 11.1. Tuy nhiên **PHẢI tap đúng vào placeholder nằm bên trong ô nhập** (`"you@example.com"`, `"Ít nhất 6 ký tự"`), **KHÔNG được tap vào `label`** (VD chữ "Email"/"Mật khẩu" hiển thị phía trên ô). Nhìn lại cấu trúc `ShopInput` ở Chương 3: `label` là một `<Typography>` và `TextInput` là 2 phần tử **anh em (sibling)** cùng nằm trong `<View style={styles.wrap}>`, KHÔNG lồng vào nhau — bấm vào chữ `label` chỉ chạm trúng cái `Text` vô tri đó, ô nhập bên dưới sẽ **không được Focus** và bước `inputText` ngay sau đó sẽ thất bại hoặc gõ nhầm chỗ.

#### Bước 4: Chạy kịch bản test
Đảm bảo App đang chạy trên máy giả lập/máy thật (từ `npm run android`/`npm run ios`), sau đó chạy:
```bash
maestro test .maestro/login_home.yaml
```
Bạn sẽ thấy Maestro tự động điều khiển "ngón tay ảo", gõ Email/Mật khẩu, bấm nút, và báo `✅ Flow Passed` nếu luồng Login → Home hoạt động đúng như thiết kế. Nếu ai đó lỡ sửa hỏng `LoginScreen`, kịch bản này sẽ báo `❌ Failed` ngay lập tức.

#### Bước 4b (tùy chọn): Mở rộng Flow — kiểm tra luôn Tab Giỏ hàng có hiển thị
Kịch bản `login_home.yaml` mới chỉ dừng ở việc "vào được Trang chủ". Để kiểm tra luôn `MainTabNavigator` (Chương 5) có dựng đúng không, tạo thêm file `.maestro/login_home_cart_tab.yaml`, tái sử dụng đúng 6 bước Login ở trên rồi nối thêm 1 dòng `assertVisible` cho Tab Giỏ hàng:

```yaml
appId: com.shopai.app
---
- launchApp
- tapOn: "you@example.com"
- inputText: "demo@shopai.com"
- tapOn: "Ít nhất 6 ký tự"
- inputText: "123456"
- tapOn: "Đăng nhập ngay"
- assertVisible: "Khám phá"
# ➕ MỚI: kiểm tra luôn Bottom Tab "Giỏ hàng" (MainTabNavigator, Chương 5) có hiển thị sau khi đăng nhập
- assertVisible: "Giỏ hàng"
```

Chạy thử:
```bash
maestro test .maestro/login_home_cart_tab.yaml
```

> [!TIP]
> Đây là bài tập **mở rộng tùy chọn**, không nằm trong Yêu cầu Nghiệm thu bắt buộc của Sprint 11 — mục tiêu là luyện thói quen viết Flow E2E dài hơn, kiểm tra được nhiều tầng UI trong 1 lượt chạy (Login → Home → Bottom Tab), đúng tinh thần "test như người dùng thật cầm máy đi hết một luồng" đã học ở Phần 11.1.

#### Bước 4c: Flow `cart_checkout.yaml` — đi sâu vào luồng Giỏ hàng

Theo Test Plan ở Phần 11.14, Giỏ hàng và Đặt hàng là hai tính năng ưu tiên **Rất cao** vì liên quan trực tiếp tới tiền. Ta viết một flow riêng cho chúng.

**Tách phần Đăng nhập ra dùng lại** — tạo `.maestro/subflows/login.yaml`:
```yaml
appId: com.shopai.app
---
- tapOn: "you@example.com"
- inputText: "demo@shopai.com"
- tapOn: "Ít nhất 6 ký tự"
- inputText: "123456"
- tapOn: "Đăng nhập ngay"
- assertVisible: "Khám phá"
```

Tạo `.maestro/cart_checkout.yaml`:
```yaml
appId: com.shopai.app
---
- launchApp:
    clearState: true   # Xóa sạch dữ liệu cũ -> mỗi lần chạy đều bắt đầu từ trạng thái giống hệt nhau

# Dùng lại subflow đăng nhập ở trên — không copy-paste 6 dòng ở mọi file
- runFlow: subflows/login.yaml

# ===== BƯỚC 1: Kiểm tra danh sách sản phẩm đã tải xong từ NestJS (Chương 9) =====
- assertVisible: "Khám phá"
- extendedWaitUntil:
    visible: "Sản phẩm từ NestJS Server 0"
    timeout: 10000     # Chờ tối đa 10 giây — đủ cho Server LAN phản hồi, tránh test chập chờn

# ===== BƯỚC 2: Thêm sản phẩm vào giỏ =====
- tapOn: "Sản phẩm từ NestJS Server 0"
- assertVisible: "Thêm vào giỏ hàng"
- tapOn: "Thêm vào giỏ hàng"
- back                 # Quay lại Trang chủ

# ===== BƯỚC 3: Chuyển sang Tab Giỏ hàng (MainTabNavigator, Chương 5) =====
- tapOn: "Giỏ hàng"
- assertVisible: "Giỏ hàng"
- assertVisible: "Tổng cộng"
- assertVisible:
    text: "Sản phẩm từ NestJS Server 0"   # Sản phẩm vừa thêm phải có mặt trong giỏ

# ===== BƯỚC 4: Mở Modal Thanh toán (RootStackNavigator, Chương 6) =====
- tapOn: "Thanh toán"
- assertVisible: "Xác nhận đơn hàng"
- assertVisible: "Xác nhận đặt hàng"

# ===== BƯỚC 5: Đặt hàng thật lên NestJS (Chương 9, Bước 9c) =====
- tapOn: "Xác nhận đặt hàng"
- extendedWaitUntil:
    visible: "Đặt hàng thành công!"
    timeout: 15000     # Đặt hàng cần gọi mạng thật -> cho thời gian chờ rộng rãi hơn
- assertVisible:
    text: "Mã đơn: ORD-.*"                # Regex: chỉ cần đúng định dạng, không cần đúng mã cụ thể
```

Chạy:
```bash
maestro test .maestro/cart_checkout.yaml
```

Chạy toàn bộ thư mục flow một lượt:
```bash
maestro test .maestro/
```

> [!IMPORTANT]
> **Flow này yêu cầu Server NestJS (Chương 9) đang chạy.** Nếu Server tắt, bước "Xác nhận đặt hàng" sẽ hiện lỗi đỏ thay vì "Đặt hàng thành công!" và flow báo FAIL — điều này **đúng như thiết kế**. Đây chính là lý do E2E thường được chạy trong một môi trường Staging có Backend thật, tách riêng khỏi pipeline Unit Test nhẹ nhàng chạy trên mọi Pull Request.

> [!TIP]
> **Ba kỹ thuật Maestro đáng nhớ trong flow trên:**
> - `clearState: true` — xóa dữ liệu App trước khi chạy, khiến test **có thể lặp lại được** (chạy 10 lần cho 10 kết quả giống nhau). Nếu không có nó, giỏ hàng đã `persist` từ lần chạy trước sẽ làm sai lệch kết quả.
> - `runFlow` — tách các đoạn dùng lại thành subflow, tránh sửa mật khẩu ở 5 file khác nhau.
> - `extendedWaitUntil` — chờ thông minh, thử lại liên tục tới khi thấy phần tử. Đây là vũ khí chống **flaky test** hiệu quả nhất, tốt hơn hẳn việc chèn `- wait: 5000` cứng nhắc.

**Gỡ lỗi khi flow FAIL:** dùng Maestro Studio, một công cụ trực quan cho phép bạn xem cây UI và thử từng lệnh ngay lập tức:
```bash
maestro studio
```

---

### PHẦN 2: Unit Test tối thiểu với Jest

#### Bước 5: Tách `formatCurrency` thành Util dùng chung
Ở Chương 6, hàm `formatCurrency` đang được viết "chết cứng" bên trong `CartScreen.tsx`. Một hàm thuần túy (Pure Function) như vậy xứng đáng được tách ra để tái sử dụng VÀ để viết Test được. Tạo file `src/utils/formatCurrency.ts`:

```ts
export const formatCurrency = (value: number): string =>
  new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(value);
```

Sau đó ở `CartScreen.tsx`, xóa hàm `formatCurrency` viết tay cũ, thay bằng:
```tsx
import { formatCurrency } from '@utils/formatCurrency';
```

> [!TIP]
> `ProductCard.tsx` (Chương 6) cũng đang tự gọi `new Intl.NumberFormat('vi-VN', ...)` viết tay để hiển thị giá — tiện tay sửa luôn dòng đó thành `import { formatCurrency } from '@utils/formatCurrency';` rồi dùng `formatCurrency(product.price)`, để cả App chỉ có DUY NHẤT một hàm định dạng tiền tệ, tránh lệch định dạng giữa `CartScreen` và `ProductCard`.

#### Bước 6: Viết Jest Test cho `formatCurrency`
Tạo file `src/utils/__tests__/formatCurrency.test.ts` (hoặc `formatCurrency.test.ts` cùng cấp):

```ts
import { formatCurrency } from '../formatCurrency';

describe('formatCurrency', () => {
  it('định dạng đúng số tiền VND có dấu phân cách hàng nghìn', () => {
    expect(formatCurrency(1500)).toBe('1.500 ₫');
  });

  it('xử lý đúng giá trị 0 đồng', () => {
    expect(formatCurrency(0)).toBe('0 ₫');
  });

  it('xử lý đúng số tiền lớn (sản phẩm giá cao)', () => {
    expect(formatCurrency(19990000)).toBe('19.990.000 ₫');
  });
});
```

> [!WARNING]
> Định dạng chuỗi trả về của `Intl.NumberFormat` có thể lệch khoảng trắng/ký hiệu `₫` tùy phiên bản Hermes/Node. Nếu Test báo Fail vì sai khác nhỏ (dấu cách, thứ tự ký hiệu), hãy `console.log(formatCurrency(1500))` để xem chuỗi thật máy bạn trả về rồi cập nhật lại `expect(...)` cho khớp — đây chính là bài học thực tế về tính "không ổn định 100% giữa môi trường" của `Intl`.

Chạy test:
```bash
npx jest src/utils/__tests__/formatCurrency.test.ts
```

#### Bước 6b: Unit Test cho `useCartStore` — bảo vệ logic liên quan tới TIỀN

Theo Test Plan (Phần 11.14), đây là hạng mục ưu tiên **Rất cao**: một lỗi trong công thức `totalPrice` nghĩa là khách hàng bị tính sai tiền — hậu quả nghiêm trọng hơn nhiều so với một nút bị lệch 2 pixel.

Nhắc lại `useCartStore` từ Chương 6 có: `items`, `addItem`, `removeItem`, `totalQuantity()`, `totalPrice()`, `clearCart()`.

Trước hết, chuẩn bị mock cho `AsyncStorage` (vì Store có lớp `persist` bọc ngoài) — thêm vào `jest.setup.js` đã tạo ở Phần 11.6:
```js
jest.mock('@react-native-async-storage/async-storage', () =>
  require('@react-native-async-storage/async-storage/jest/async-storage-mock'),
);
```

Tạo `src/store/__tests__/useCartStore.test.ts`:

```ts
import { useCartStore } from '../useCartStore';

// Dữ liệu mẫu — khai báo một chỗ, dùng lại ở mọi test
const iphone = { id: 'p1', name: 'iPhone 15', price: 25000000, image: 'https://x.com/a.jpg' };
const airpods = { id: 'p2', name: 'AirPods Pro', price: 6000000, image: 'https://x.com/b.jpg' };

describe('useCartStore', () => {
  beforeEach(() => {
    // Zustand cho phép set State trực tiếp từ ngoài React — cách reset sạch nhất giữa các test.
    // Thiếu dòng này, giỏ hàng của test trước sẽ "chảy" sang test sau và gây lỗi rất khó hiểu.
    useCartStore.setState({ items: [] });
  });

  // ===== NHÓM 1: ĐƯỜNG HẠNH PHÚC =====
  describe('addItem', () => {
    it('thêm một sản phẩm mới vào giỏ hàng trống', () => {
      useCartStore.getState().addItem(iphone);

      const { items } = useCartStore.getState();
      expect(items).toHaveLength(1);
      expect(items[0].id).toBe('p1');
      expect(items[0].quantity).toBe(1);
    });

    it('thêm hai sản phẩm KHÁC NHAU tạo ra hai dòng riêng biệt', () => {
      useCartStore.getState().addItem(iphone);
      useCartStore.getState().addItem(airpods);

      expect(useCartStore.getState().items).toHaveLength(2);
    });

    // ===== NHÓM 2: TRƯỜNG HỢP BIÊN — nơi bug hay ẩn nấp nhất =====
    it('thêm CÙNG một sản phẩm 2 lần thì gộp số lượng, KHÔNG tạo dòng mới', () => {
      useCartStore.getState().addItem(iphone);
      useCartStore.getState().addItem(iphone);

      const { items } = useCartStore.getState();
      expect(items).toHaveLength(1);   // Vẫn 1 dòng
      expect(items[0].quantity).toBe(2); // Nhưng số lượng là 2
    });
  });

  describe('totalPrice', () => {
    it('trả về 0 khi giỏ hàng trống', () => {
      expect(useCartStore.getState().totalPrice()).toBe(0);
    });

    it('tính đúng tổng tiền của một sản phẩm', () => {
      useCartStore.getState().addItem(iphone);
      expect(useCartStore.getState().totalPrice()).toBe(25000000);
    });

    it('tính đúng tổng tiền khi có nhiều sản phẩm và nhiều số lượng', () => {
      useCartStore.getState().addItem(iphone);   // 25.000.000 x 2
      useCartStore.getState().addItem(iphone);
      useCartStore.getState().addItem(airpods);  //  6.000.000 x 1

      // 25.000.000 * 2 + 6.000.000 * 1 = 56.000.000
      expect(useCartStore.getState().totalPrice()).toBe(56000000);
    });
  });

  describe('totalQuantity', () => {
    it('đếm TỔNG SỐ MÓN, không phải số dòng trong giỏ', () => {
      useCartStore.getState().addItem(iphone);
      useCartStore.getState().addItem(iphone);
      useCartStore.getState().addItem(airpods);

      expect(useCartStore.getState().items).toHaveLength(2);      // 2 dòng
      expect(useCartStore.getState().totalQuantity()).toBe(3);    // nhưng 3 món
    });
  });

  describe('removeItem', () => {
    it('xóa đúng sản phẩm được chỉ định', () => {
      useCartStore.getState().addItem(iphone);
      useCartStore.getState().addItem(airpods);

      useCartStore.getState().removeItem('p1');

      const { items } = useCartStore.getState();
      expect(items).toHaveLength(1);
      expect(items[0].id).toBe('p2');
    });

    // ===== NHÓM 3: ĐƯỜNG LỖI =====
    it('không làm sập App khi xóa một id không tồn tại', () => {
      useCartStore.getState().addItem(iphone);

      expect(() => useCartStore.getState().removeItem('id_khong_ton_tai')).not.toThrow();
      expect(useCartStore.getState().items).toHaveLength(1);
    });
  });

  describe('clearCart', () => {
    it('xóa sạch giỏ hàng sau khi đặt hàng thành công (Chương 9, Bước 9c)', () => {
      useCartStore.getState().addItem(iphone);
      useCartStore.getState().addItem(airpods);

      useCartStore.getState().clearCart();

      expect(useCartStore.getState().items).toHaveLength(0);
      expect(useCartStore.getState().totalPrice()).toBe(0);
      expect(useCartStore.getState().totalQuantity()).toBe(0);
    });
  });
});
```

Chạy:
```bash
npx jest src/store/__tests__/useCartStore.test.ts
```

> [!TIP]
> Để ý cách các test được nhóm bằng `describe` lồng nhau theo đúng **bốn nhóm ca kiểm thử** ở Phần 11.14: đường hạnh phúc, trường hợp biên, đường lỗi, trạng thái rỗng. Khi test đỏ, Jest in ra đường dẫn đầy đủ `useCartStore > addItem > thêm CÙNG một sản phẩm 2 lần...` — bạn biết ngay chỗ hỏng mà không cần mở file.

> [!NOTE]
> Ở đây ta gọi `useCartStore.getState()` thay vì `renderHook` (Phần 11.7). Lý do: Zustand cho phép truy cập Store **bên ngoài React** — logic thuần thì test theo cách thuần, nhanh và đơn giản hơn. Chỉ dùng `renderHook` khi cần kiểm tra việc component có **re-render đúng lúc** hay không.

#### Bước 6c: Thêm script Coverage và ngưỡng tối thiểu

Mở `package.json`, bổ sung khối `scripts` và cấu hình Jest (Phần 11.8):

```json
{
  "scripts": {
    "test": "jest",
    "test:watch": "jest --watch",
    "test:coverage": "jest --coverage",
    "test:ci": "jest --coverage --ci --maxWorkers=2",
    "lint": "eslint . --ext .js,.jsx,.ts,.tsx",
    "lint:fix": "eslint . --ext .js,.jsx,.ts,.tsx --fix",
    "e2e": "maestro test .maestro/"
  },
  "jest": {
    "preset": "react-native",
    "setupFiles": ["<rootDir>/jest.setup.js"],
    "collectCoverageFrom": [
      "src/**/*.{ts,tsx}",
      "!src/**/*.d.ts",
      "!src/**/__tests__/**",
      "!src/types/**",
      "!src/constants/**"
    ],
    "coverageThreshold": {
      "global": {
        "statements": 40,
        "branches": 30,
        "functions": 40,
        "lines": 40
      },
      "./src/utils/": {
        "statements": 90,
        "branches": 80,
        "functions": 90,
        "lines": 90
      },
      "./src/store/": {
        "statements": 70,
        "branches": 60,
        "functions": 70,
        "lines": 70
      }
    }
  }
}
```

Chạy và xem báo cáo trực quan:
```bash
npm run test:coverage
open coverage/lcov-report/index.html   # macOS; Windows dùng: start coverage\lcov-report\index.html
```

Thêm `coverage/` vào `.gitignore` — đây là file sinh ra tự động, không commit.

> [!TIP]
> Ngưỡng toàn cục ở trên cố tình đặt **thấp và thực tế** (40%) vì ShopAI có nhiều màn hình UI chưa test. Nhưng `src/utils/` và `src/store/` được đặt cao hơn hẳn — đúng nguyên tắc ở Phần 11.8: siết chặt nơi có logic quan trọng, nới lỏng nơi chủ yếu là giao diện. Khi viết thêm test, hãy **nâng dần** ngưỡng lên; con số chỉ được phép đi lên, không bao giờ đi xuống.

> [!WARNING]
> Cờ `--maxWorkers=2` trong `test:ci` không phải trang trí: máy ảo GitHub Actions miễn phí chỉ có 2 nhân. Để Jest tự do sinh worker theo số nhân ảo sẽ khiến nó tranh nhau tài nguyên và **chạy chậm hơn** hoặc bị kill vì hết RAM.

---

### PHẦN 3: [Đề cương] Integration Test với React Native Testing Library cho `ShopButton`

#### Bước 7: Cài đặt RNTL (nếu template RN CLI chưa có sẵn)
```bash
npm install --save-dev @testing-library/react-native
```

#### Bước 8: Viết file test `src/components/__tests__/ShopButton.test.tsx`
Đúng theo lý thuyết ở Phần 11.2 — test `ShopButton` (đã xây từ Chương 3) theo 3 khía cạnh: hiển thị đúng `title`, gọi đúng `onPress` khi bấm, và KHÔNG gọi `onPress` khi `disabled`:

```tsx
import React from 'react';
import { render, fireEvent, screen } from '@testing-library/react-native';
import ShopButton from '../ShopButton';

describe('ShopButton', () => {
  it('hiển thị đúng title được truyền vào', () => {
    render(<ShopButton title="Xác nhận thanh toán" onPress={() => {}} />);
    expect(screen.getByText('Xác nhận thanh toán')).toBeTruthy();
  });

  it('gọi đúng hàm onPress khi người dùng bấm vào nút', () => {
    const handlePress = jest.fn();
    render(<ShopButton title="Đăng nhập ngay" onPress={handlePress} />);

    fireEvent.press(screen.getByText('Đăng nhập ngay'));

    expect(handlePress).toHaveBeenCalledTimes(1);
  });

  it('KHÔNG gọi onPress khi nút đang ở trạng thái disabled', () => {
    const handlePress = jest.fn();
    render(<ShopButton title="Đang xử lý" onPress={handlePress} disabled />);

    fireEvent.press(screen.getByText('Đang xử lý'));

    expect(handlePress).not.toHaveBeenCalled();
  });
});
```

Chạy test:
```bash
npx jest src/components/__tests__/ShopButton.test.tsx
```

#### Bước 9: Thử soi App bằng React Native DevTools / Flipper
Chạy App ở chế độ Debug, mở Metro Terminal, nhấn `j` để bật **React Native DevTools** (Phần 11.3) — thử vào tab **Components** xem cây `HomeScreen -> ProductCard -> ShopButton`, và tab **Profiler** để soi Component nào Re-render khi bấm "Mua ngay" (liên hệ lại bài `React.memo` Chương 3). Nếu có Flipper cài sẵn, mở tab **Network** để xem trực tiếp Request `axiosClient` (Chương 6) có gắn đúng Header `Authorization` không.

---

### PHẦN 4: CI/CD tối giản với GitHub Actions (và bản phác thảo Fastlane)

#### Bước 10: Tạo Pipeline GitHub Actions
Tạo file `.github/workflows/ci.yml` ở gốc dự án:

```yaml
name: ShopAI CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v4

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'

      - name: Cài đặt dependencies
        run: npm ci

      - name: Kiểm tra Lint
        run: npm run lint

      - name: Chạy Unit Test (Jest)
        run: npm test
```

Từ giờ, mỗi khi `git push`, GitHub sẽ tự động dựng một máy ảo Ubuntu, cài dependencies, chạy Lint và toàn bộ Jest Test — bao gồm cả `formatCurrency.test.ts` (Unit Test, Bước 6) **và** `ShopButton.test.tsx` (Integration Test RNTL, Bước 8). Nếu bất kỳ bước nào đỏ (Fail), Pull Request sẽ bị đánh dấu cảnh báo — chặn đứng code lỗi trước khi nó chạm vào nhánh `main`.

> [!TIP]
> Bài học CI ở đây **chưa chạy Maestro trên GitHub Actions** — vì Maestro cần máy ảo Android/iOS thật (rất tốn phí và cấu hình runner phức tạp). Trong môi trường doanh nghiệp thật, đội DevOps thường tách riêng 1 Pipeline khác (dùng máy ảo macOS/self-hosted runner) chỉ để chạy E2E, tách biệt với Pipeline Lint/Unit Test nhẹ nhàng chạy trên mọi Pull Request.

#### Bước 10b: Nâng cấp Pipeline — Matrix, Cache, Coverage Artifact

Pipeline ở Bước 10 đã chạy được, giờ áp dụng ba kỹ thuật ở Phần 11.11 để nó nhanh hơn và hữu ích hơn. Thay toàn bộ nội dung `.github/workflows/ci.yml`:

```yaml
name: ShopAI CI

on:
  push:
    branches: [main, develop]
  pull_request:
    branches: [main, develop]

jobs:
  # ===== JOB 1: Kiểm tra chất lượng mã nguồn =====
  lint:
    name: Lint & TypeScript
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: '20'
          cache: 'npm'
      - run: npm ci
      - name: ESLint
        run: npm run lint
      - name: Kiểm tra kiểu TypeScript
        run: npx tsc --noEmit   # Bắt lỗi kiểu mà ESLint bỏ qua

  # ===== JOB 2: Chạy test trên nhiều phiên bản Node song song =====
  test:
    name: Test (Node ${{ matrix.node-version }})
    needs: lint            # Lint đỏ thì không tốn tài nguyên chạy test
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false     # Node 18 đỏ vẫn chạy tiếp Node 20, 22 để biết lỗi ở đâu
      matrix:
        node-version: ['18.x', '20.x', '22.x']
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: ${{ matrix.node-version }}
          cache: 'npm'

      - name: Cache node_modules
        uses: actions/cache@v4
        with:
          path: ~/.npm
          key: ${{ runner.os }}-node-${{ matrix.node-version }}-${{ hashFiles('**/package-lock.json') }}
          restore-keys: ${{ runner.os }}-node-${{ matrix.node-version }}-

      - run: npm ci

      - name: Chạy toàn bộ test kèm coverage
        run: npm run test:ci

      # Chỉ tải báo cáo lên một lần, tránh 3 bản trùng nhau từ 3 phiên bản Node
      - name: Lưu báo cáo coverage
        if: always() && matrix.node-version == '20.x'
        uses: actions/upload-artifact@v4
        with:
          name: coverage-report
          path: coverage/
          retention-days: 7

  # ===== JOB 3: Build APK cho QA tải về =====
  build-android:
    name: Build Debug APK
    needs: test
    if: github.ref == 'refs/heads/main'   # Chỉ build trên nhánh main, không build mọi PR
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with: { node-version: '20', cache: 'npm' }
      - uses: actions/setup-java@v4
        with: { distribution: 'temurin', java-version: '17' }

      - name: Cache Gradle
        uses: actions/cache@v4
        with:
          path: |
            ~/.gradle/caches
            ~/.gradle/wrapper
          key: ${{ runner.os }}-gradle-${{ hashFiles('**/*.gradle*') }}

      - run: npm ci
      - name: Đóng gói APK
        run: cd android && ./gradlew assembleDebug --no-daemon

      - name: Lưu APK cho QA
        uses: actions/upload-artifact@v4
        with:
          name: shopai-debug-apk
          path: android/app/build/outputs/apk/debug/app-debug.apk
          retention-days: 14
```

Kết quả: một đồ thị `lint → test (×3 Node) → build-android`. Mỗi mũi tên là một **Quality Gate** (Phần 11.14) — code lỗi không thể đi tiếp sang bước sau.

> [!TIP]
> Sau khi push, vào tab **Actions** trên GitHub, mở lần chạy mới nhất, kéo xuống mục **Artifacts** — bạn sẽ thấy `coverage-report` và `shopai-debug-apk` tải về được. Đội QA từ giờ tự lấy bản build mà không cần nhắn tin nhờ lập trình viên build tay nữa.

#### Bước 10c (tùy chọn): Husky + lint-staged — chặn lỗi ngay tại máy

Áp dụng Phần 11.13. Bước này **không bắt buộc** nhưng rất đáng làm: nó rút thời gian phát hiện lỗi format từ 3 phút (chờ CI) xuống 3 giây.

```bash
npm install --save-dev husky lint-staged
npx husky init
```

Lệnh `husky init` tạo thư mục `.husky/` và tự thêm script `prepare` vào `package.json`. Mở `.husky/pre-commit`, thay nội dung mặc định bằng:
```bash
npx lint-staged
```

Thêm cấu hình vào `package.json`:
```json
"lint-staged": {
  "src/**/*.{ts,tsx}": [
    "eslint --fix",
    "prettier --write"
  ],
  "src/**/*.{json,md}": ["prettier --write"]
}
```

Thử nghiệm: cố tình viết một dòng code lệch thụt đầu dòng trong `src/utils/formatCurrency.ts`, rồi `git add . && git commit -m "test husky"`. Husky sẽ chạy `eslint --fix` + `prettier --write`, tự sửa file, và commit đi tiếp với code đã sạch.

Thêm hook chạy test trước khi push — tạo `.husky/pre-push`:
```bash
npm test -- --onlyChanged --passWithNoTests
```

> [!NOTE]
> `--passWithNoTests` tránh việc push bị chặn oan khi bạn chỉ sửa file README (không có test nào liên quan để mà chạy). Thiếu cờ này, Jest thoát với mã lỗi vì "không tìm thấy test nào" và hook sẽ chặn nhầm.

> [!IMPORTANT]
> Nhắc lại từ Phần 11.13: hook có thể bị bỏ qua bằng `git commit --no-verify`. Nó là hàng rào **tiện lợi**, không phải hàng rào **an ninh**. CI ở Bước 10b mới là nơi không ai lách được.

#### Bước 11: Phác thảo Fastlane (KHÔNG cần chạy trong lớp)
Fastlane tự động hóa bước build + submit lên Store, nhưng để chạy thật, bạn cần tài khoản Apple Developer (trả phí) và App Store Connect API Key — những thứ học viên thường chưa có trong môi trường học tập. Dưới đây là bản phác thảo `fastlane/Fastfile` để bạn hiểu cấu trúc, KHÔNG cần thực thi:

```ruby
# fastlane/Fastfile — CHỈ ĐỂ THAM KHẢO, không chạy trong lớp học
default_platform(:ios)

platform :ios do
  desc "Build và đẩy bản Beta lên TestFlight"
  lane :beta do
    increment_build_number             # Tự tăng số Build
    build_app(scheme: "ShopAI")        # Archive giống Xcode -> tạo file .ipa
    upload_to_testflight(              # Cần API Key của Apple Developer
      api_key_path: "fastlane/api_key.json"
    )
  end
end
```

> [!WARNING]
> `upload_to_testflight` / `upload_to_play_store` bắt buộc phải có credentials thật (API Key Apple, Service Account Key Google) — đây là lý do Sprint này KHÔNG yêu cầu học viên chạy thật lệnh `fastlane beta`. Mục tiêu là hiểu **cấu trúc** một Pipeline CD hoàn chỉnh: `GitHub Actions (Test) → Fastlane (Build) → Store (Submit)`, để khi đi làm thực tế, bạn biết chính xác nên tìm hiểu thư viện nào.

---

### PHẦN 5: Kiểm thử Backend NestJS — Jest Unit Test + Supertest E2E (Phần 11.15)

Bốn Phần trước đều xoay quanh App Mobile. Phần này áp dụng lý thuyết Phần 11.15 lên Server `shopai-backend` (Chương 9) — **chỉ viết Test** cho Auth/Orders đã có JWT + Prisma, không dựng lại Module.

#### Bước 11d: Xác nhận Auth/Orders từ Sprint 9 còn nguyên (KHÔNG tạo lại)

1. Mở `shopai-backend` — xác nhận đã có: `src/auth/*`, `JwtAuthGuard` trên `POST /api/orders`, Prisma schema + seed.
2. **Không** tạo `users.data.ts`. **Không** ghi đè `auth.service.ts` / `auth.module.ts`.
3. Chạy 3 lệnh `curl` (login → orders không token = 401 → orders có token = 201) như checklist Sprint 9. Dùng đúng user seed (`demo@shopai.com` / mật khẩu seed Ch9).
4. Nếu thiếu Guard/JWT: quay lại làm nốt Sprint 9, rồi mới sang Bước 11e.

#### Bước 11e: Viết Jest Unit Test cho `AuthService`

Tạo `src/auth/auth.service.spec.ts` theo Phần 11.15 mục 3 — **mock `PrismaService.user.findUnique`** + `JwtService` (không import `users.data.ts`). Kiểm tra `login` thành công + nhánh sai email/sai mật khẩu ném `UnauthorizedException`.

Chạy:
```bash
npx jest auth.service.spec.ts
```

> [!TIP]
> Nếu muốn thực hành thêm, viết tương tự `src/order/order.service.spec.ts` để Unit Test công thức "Server tự tính lại tổng tiền, từ chối `total` gian lận" (Phần 9.12) — đây là lựa chọn `OrdersService` mà đề bài Sprint 11 cho phép chọn thay `AuthService`.

#### Bước 11f: Viết Supertest E2E Test cho `POST /api/auth/login` và `POST /api/orders`

Tạo `test/auth-orders.e2e-spec.ts` đúng nguyên văn ở Phần 11.15 mục 4 — đủ 2 nhóm `describe`, đủ 3 kịch bản Login (đúng/sai mật khẩu/sai định dạng email) và 3 kịch bản Orders (không Token/Token giả/Token đúng).

Chạy:
```bash
npm run test:e2e
```

Kết quả mong đợi: cả 6 `it()` đều PASS, đặc biệt 2 dòng cốt lõi theo đúng yêu cầu đề bài:
- `POST /api/orders` không kèm Token → `401`
- `POST /api/orders` kèm Token hợp lệ (lấy từ `POST /api/auth/login` ngay trước đó) → `201`

#### Bước 11g (tùy chọn): Wire vào GitHub Actions — job `backend-test`

Nếu `shopai-backend` nằm chung repo với App Mobile, mở lại `.github/workflows/ci.yml` (đã dựng ở Bước 10b), thêm job `backend-test` đúng nguyên văn ở Phần 11.15 mục 5 — job này chạy **song song, độc lập** với job `test` của Mobile.

> [!NOTE]
> Nếu `shopai-backend` là repository riêng, bỏ qua bước "thêm job vào workflow chung" — thay vào đó tạo file `.github/workflows/ci.yml` **của riêng repo Backend** với đúng nội dung job `backend-test` (bỏ `working-directory`).

#### Bước 12: Lưu toàn bộ thành quả Sprint 11
```bash
git add .
git commit -m "Sprint 11: Add Maestro E2E flows, Jest unit tests (formatCurrency + useCartStore), RNTL integration test, coverage thresholds, advanced GitHub Actions CI, and NestJS backend testing (AuthModule + Jest + Supertest)"
```

### ✅ Checklist Nghiệm thu Sprint 11

**Tầng 1 — Unit Test (Jest):**
- [ ] `formatCurrency` đã được tách khỏi `CartScreen.tsx`, sống ở `src/utils/formatCurrency.ts`, có Unit Test PASS.
- [ ] `useCartStore.test.ts` PASS, phủ được `addItem` (gồm cả trường hợp gộp số lượng), `removeItem`, `totalPrice`, `totalQuantity`, `clearCart`.
- [ ] `jest.setup.js` mock đủ các Native Module (Crashlytics, SecureStore, AsyncStorage, Reanimated) — không test nào đỏ vì lỗi `import`.

**Tầng 2 — Integration Test (RNTL):**
- [ ] **[Đề cương]** `ShopButton.test.tsx` PASS, kiểm tra được cả `onPress` và `disabled`.

**Tầng 3 — E2E (Maestro):**
- [ ] `maestro test .maestro/login_home.yaml` chạy PASS, mô phỏng đúng UI thật của ShopAI (không phải UI giả định).
- [ ] `maestro test .maestro/cart_checkout.yaml` chạy PASS với Server NestJS (Chương 9) đang bật.
- [ ] `appId` trong kịch bản Maestro khớp với `applicationId` thật trong `android/app/build.gradle`.

**Coverage & công cụ:**
- [ ] `npm run test:coverage` chạy được, sinh ra thư mục `coverage/`.
- [ ] `coverageThreshold` đã cấu hình, và toàn bộ test hiện tại vượt ngưỡng.
- [ ] `coverage/` đã có trong `.gitignore`.
- [ ] **[Đề cương]** Biết mở React Native DevTools (`j` trong Metro) và hiểu vai trò Network Inspector của Flipper.

**CI/CD:**
- [ ] `.github/workflows/ci.yml` tự động chạy khi `git push`, có bước Lint và Test.
- [ ] Pipeline có Matrix nhiều phiên bản Node, có Cache, và upload được Artifact coverage.
- [ ] *(Tùy chọn)* Husky + lint-staged chạy được khi `git commit`.
- [ ] Hiểu rõ ranh giới: CI (Test tự động) là bắt buộc phải nắm; CD (Fastlane Submit Store) là kiến thức mở rộng, cần thiết lập tài khoản riêng khi đi làm thật.

**Tầng 4 — Backend NestJS (Jest + Supertest, CRITICAL):**
- [ ] `AuthModule` + Prisma + `JwtAuthGuard` từ Sprint 9 còn nguyên (không bị thay bằng `users.data.ts` in-memory).
- [ ] `src/auth/auth.service.spec.ts` PASS — kiểm chứng `login` thành công và `validateUser` ném đúng `UnauthorizedException` ở cả 2 nhánh sai email/sai mật khẩu.
- [ ] `test/auth-orders.e2e-spec.ts` PASS — `POST /api/auth/login` trả `accessToken`; `POST /api/orders` trả `401` khi thiếu Token, `201` khi có Token hợp lệ.
- [ ] `npm run test:e2e` (trong `shopai-backend`) chạy sạch, không bị treo (đã có `afterAll(() => app.close())`).
- [ ] *(Tùy chọn)* Job `backend-test` chạy được trong CI, độc lập với job `test` của Mobile.

### 🧯 Sổ tay gỡ lỗi Sprint 11

| Triệu chứng | Nguyên nhân | Cách xử lý |
|---|---|---|
| `SyntaxError: Cannot use import statement outside a module` | Thư viện phát hành ES Modules chưa biên dịch | Thêm tên thư viện vào `transformIgnorePatterns` (Phần 11.6) |
| `Invariant Violation: Native module cannot be null` | Chưa mock Native Module | Bổ sung mock vào `jest.setup.js` |
| Test đơn lẻ thì xanh, chạy cả bộ thì đỏ | State rò rỉ giữa các test | Thêm `useCartStore.setState({ items: [] })` vào `beforeEach` |
| `formatCurrency` test lệch ký tự `₫` | `Intl` khác nhau giữa Node và Hermes | Xem cảnh báo ở Bước 6 |
| Maestro không tìm thấy ô nhập | Đang tap vào `label` thay vì `placeholder` | Xem lưu ý ở Bước 3 |
| Maestro chạy lần 2 thì FAIL | Giỏ hàng cũ còn `persist` lại | Thêm `launchApp: clearState: true` |
| CI đỏ vì coverage | Vừa thêm code mới mà chưa thêm test | Viết thêm test, hoặc điều chỉnh ngưỡng có cân nhắc |
| `Error: secretOrPrivateKey must have a value` khi test Backend | Thiếu biến `JWT_SECRET` trong môi trường chạy test (`.env` hoặc `env:` của CI) | Thêm `JWT_SECRET` vào `.env` (local) hoặc khối `env:` của job `backend-test` (CI) |
| E2E Backend PASS hết nhưng Jest treo mãi không tự thoát | Quên gọi `await app.close()` trong `afterAll` | Thêm `afterAll(async () => { await app.close(); })` đúng như Phần 11.15 mục 4 |
| `POST /api/orders` luôn trả `401` dù Token đúng | `Authorization` Header thiếu chữ `Bearer ` (có khoảng trắng) phía trước Token, hoặc Token đã hết hạn (`JWT_EXPIRES_IN` quá ngắn) | Kiểm tra định dạng `Bearer <token>`; tăng `JWT_EXPIRES_IN` khi debug |
| Unit Test `AuthService` báo lỗi `Cannot read properties of undefined (reading 'get')` | `ConfigService`/`JwtService` chưa được mock trong `Test.createTestingModule` | Ghi đè bằng `{ provide: JwtService, useValue: {...} }` đúng như Phần 11.15 mục 3, không dùng `JwtService` thật trong Unit Test |

---

## 🏆 TỔNG KẾT KHÓA HỌC LẬP TRÌNH REACT NATIVE ENTERPRISE

Giáo trình này không dạy bạn trở thành một "Thợ gõ code" (Coder). Giáo trình này đã trang bị cho bạn tư duy của một **Kỹ sư Phần mềm (Software Engineer)** thực thụ.

Hãy nhìn lại hành trình bạn đã đi qua suốt 11 Chương:
1. **(Chương 1-2):** Bạn hiểu được The Bridge, JSI, Memory Leak, Closure Trap. Nắm bản chất chứ không học vẹt.
2. **(Chương 3-4):** Bạn tối ưu Re-render với Memoization, tái chế bộ nhớ với List Virtualization, đánh bóng UI với Reanimated.
3. **(Chương 5-6):** Bạn cấu trúc luồng Auth bảo mật, bỏ rơi Redux cồng kềnh để tiếp nạp Zustand và React Query.
4. **(Chương 7-8):** Bạn điều khiển phần cứng bằng Native Modules, mã hóa Keystore và tích hợp Trí tuệ Nhân tạo AI.
5. **(Chương 9):** Bạn phá vỡ giới hạn Mobile, code luôn Backend NestJS để ShopAI có dữ liệu thật.
6. **(Chương 10):** Bạn học cách giám sát lỗi Production với Firebase Crashlytics và vá lỗi tức thời qua OTA (EAS Update) — mà không đánh đổi bất kỳ tính năng nào đã xây.
7. **(Chương 11):** Bạn phủ đủ **cả 4 mảng Kiểm thử & Debug theo đề cương chính thức** — Jest Unit Test, Integration Test với React Native Testing Library, Debug trực quan bằng React Native DevTools & Flipper — rồi còn học thêm kiến thức nâng cao ngoài đề cương: Mocking, Coverage, Kiểm thử E2E với Maestro và dựng Pipeline CI với GitHub Actions, hiểu cả ranh giới của CD tự động Submit Store bằng Fastlane.

---

### 🚦 Bảy cổng chất lượng của ShopAI — bức tranh toàn cảnh

Mọi thứ bạn học ở Chương 10 và 11 ghép lại thành một dây chuyền phòng thủ nhiều lớp. Một dòng code lỗi muốn chạm tới người dùng cuối phải vượt qua đủ bảy cửa ải:

```
 Lập trình viên gõ code
        │
        ▼
 ┌──────────────────────────────────────────────────────────────┐
 │ CỔNG 1 — IDE           TypeScript + ESLint báo đỏ ngay khi gõ │  < 1 giây
 ├──────────────────────────────────────────────────────────────┤
 │ CỔNG 2 — Pre-commit    Husky + lint-staged tự format          │  ~3 giây
 ├──────────────────────────────────────────────────────────────┤
 │ CỔNG 3 — Pre-push      Jest chạy các test liên quan           │  ~15 giây
 ├──────────────────────────────────────────────────────────────┤
 │ CỔNG 4 — CI Lint       ESLint + tsc --noEmit trên máy sạch    │  ~1 phút
 ├──────────────────────────────────────────────────────────────┤
 │ CỔNG 5 — CI Test       Toàn bộ Jest + ngưỡng Coverage         │  ~3 phút
 ├──────────────────────────────────────────────────────────────┤
 │ CỔNG 6 — E2E           Maestro chạy các luồng trọng yếu       │  ~10 phút
 ├──────────────────────────────────────────────────────────────┤
 │ CỔNG 7 — Staged Rollout  Phát hành 10% + theo dõi Crashlytics │  vài giờ
 └──────────────────────────────────────────────────────────────┘
        │
        ▼
  Người dùng cuối
```

**Nguyên tắc kinh tế đằng sau sơ đồ này:** chi phí sửa một lỗi tăng theo cấp số nhân qua từng cổng. Bắt được ở Cổng 1 tốn 10 giây. Lọt tới Cổng 7 thì tốn cả một cuộc họp khẩn, một bản hotfix, và niềm tin của người dùng. Đó là lý do các cổng phía trước tuy "nhẹ" nhưng lại có giá trị lớn nhất — chúng rẻ và bắt được phần lớn lỗi.

**Nếu bạn chỉ có thời gian làm ba việc**, hãy chọn: Cổng 5 (CI chạy test tự động), Cổng 7 (phát hành từ từ + giám sát Crashlytics), và một bộ Unit Test cho phần logic liên quan tới tiền. Ba thứ đó đã chặn được phần lớn thảm hoạ trong thực tế.

---

### 📦 ShopAI hoàn thiện — Danh sách tính năng đầy đủ

Sau 11 Chương, ShopAI không còn là một App demo rời rạc — nó là một sản phẩm thương mại điện tử **đầy đủ vòng đời**, ghép lại từ tất cả những gì bạn vừa học:

| Nhóm tính năng | Cụ thể trong ShopAI | Học ở Chương |
|---|---|---|
| **Đăng nhập/Đăng xuất** | `LoginScreen`, Token lưu `SecureStore` (Keystore phần cứng), tự động đăng nhập lại khi mở App | 5, 8 |
| **Trang chủ** | `HomeScreen` — Grid sản phẩm bằng `FlashList`, Loading/Error, chấm "Server Online" (tùy chọn) | 4, 6, 9 |
| **Chi tiết sản phẩm** | `ProductDetailScreen` theo `productId` qua Route Params | 5 |
| **Giỏ hàng có Persist** | `CartStore` (Zustand) + MMKV — thêm/xóa/tổng tiền, sống sót qua việc tắt App | 6 |
| **Thanh toán** | `CheckoutScreen` giả lập — xác nhận đơn, xóa giỏ hàng sau khi hoàn tất | 6 (mở rộng) |
| **Quét mã vạch/QR** | `ScannerScreen` — Vision Camera + Code Scanner, khóa chống quét lặp, ML Kit on-device | 7 |
| **Trợ lý AI** | `AIChatScreen` — Gemini qua NestJS Proxy, System Prompt chống Prompt Injection | 8, 9 |
| **Backend riêng** | `shopai-backend` (NestJS) — `/api/products`, `/api/ai/chat`, `/api/health` (tùy chọn) | 9 |
| **Giám sát Production** | Firebase Crashlytics (Crash + Non-Fatal), Firebase Performance (khái niệm), EAS Update (OTA) | 10 |
| **Kiểm thử tự động** | Jest Unit Test, RNTL Integration Test, Maestro E2E (Mobile) + Jest/Supertest cho `AuthModule`/`OrderService` (Backend), CI GitHub Actions | 11 |

> [!IMPORTANT]
> **Danh sách trên chỉ là bản tóm tắt.** Checklist nghiệm thu **đầy đủ và chi tiết nhất** của toàn bộ ShopAI — bao gồm Luồng người dùng chuẩn, Kiến trúc cây Provider cuối khóa, và các ô tick nghiệm thu Chạy được / Tính năng / Chất lượng / Đề cương — nằm ở file **`SHOPAI_HOAN_THIEN.md`** (cùng thư mục `LY-THUYET/`). Đây chính là **"kim chỉ nam"** để bạn (hoặc giảng viên) tự chấm xem ShopAI của mình đã hoàn thiện đến đâu sau khi học xong 11 Chương.

---

### 🧰 Bảng tổng hợp Stack công nghệ hiện đại của ShopAI

| Lớp | Công nghệ | Vai trò |
|---|---|---|
| Kiến trúc RN | New Architecture (JSI/Fabric), Hermes | Nền tảng hiệu năng cao, không qua Bridge JSON cũ |
| UI List | FlashList (Shopify) | Virtualization danh sách sản phẩm, mượt hơn `FlatList` |
| Camera | `react-native-vision-camera` + Code Scanner (ML Kit on-device) | Quét Barcode/QR thời gian thực, offline |
| State Client | Zustand + MMKV (persist) | Auth Token (RAM) + Giỏ hàng (persist), nhẹ hơn Redux |
| State Server | TanStack Query (React Query) | Cache, `staleTime`, tự động refetch dữ liệu sản phẩm |
| Validate dữ liệu | Zod | Chặn dữ liệu bẩn từ Server trước khi vào UI |
| Bảo mật | `expo-secure-store` (Keystore/Keychain phần cứng) | Lưu Token, không bao giờ dùng `AsyncStorage` cho Secret |
| AI | Google Gemini API (qua NestJS Proxy) | Chatbot tư vấn, giấu Key hoàn toàn khỏi Client |
| Backend | NestJS (DI/IoC, Controller-Service-Module) | Server thật, RESTful, lá chắn bảo mật cho AI Key |
| DevOps | Firebase Crashlytics + Performance, EAS Update (OTA) | Giám sát lỗi/hiệu năng Production, vá JS không cần Store review |
| Kiểm thử (Mobile) | Jest, React Native Testing Library, Maestro | Unit → Integration → E2E theo đúng Kim tự tháp kiểm thử |
| Kiểm thử (Backend) | Jest (`@nestjs/testing`) + Supertest | Unit Test `AuthService`/`OrderService`; E2E Test HTTP thật cho `/api/auth/login` và `/api/orders` (401/201) |
| CI/CD | GitHub Actions (bắt buộc học) + Fastlane (nhận biết) | Tự động Lint/Test mỗi lần push (job Mobile + job `backend-test`); hiểu cấu trúc CD Submit Store |

**Bạn đã sẵn sàng để ứng tuyển vào bất kỳ công ty công nghệ lớn (Tech Giant) nào với vị trí Mobile Engineer.**
*Cảm ơn bạn đã đồng hành. Chúc bạn một sự nghiệp rực rỡ và liên tục phá vỡ giới hạn của bản thân!*

---
*(End of Curriculum)*
