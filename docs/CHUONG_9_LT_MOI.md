---
sidebar_position: 9
title: Chương 9
---

# GIÁO TRÌNH LÝ THUYẾT & THỰC CHIẾN
## CHƯƠNG 9: BACKEND NESTJS - MẢNH GHÉP HOÀN HẢO CỦA FULLSTACK ENGINEER
**Thời lượng:** 8 tiết Lý thuyết + 6 tiết Thực hành

---

> [!IMPORTANT]
> **Thực hành chương = Sprint ShopAI cuối file.** Hoàn thành Sprint này để đạt mục tiêu chương. Hoàn thành đủ 11 chương theo `SHOPAI_HOAN_THIEN.md` = sản phẩm ShopAI **hoàn thiện đẳng cấp**.

## 📚 MỤC TIÊU HỌC TẬP

Sau khi hoàn thành chương này, học viên sẽ:
- ✅ Hiểu rõ tại sao kỹ sư Mobile hiện đại bắt buộc phải am hiểu Backend (Tự chủ luồng dữ liệu).
- ✅ Nắm vững nguyên lý cốt lõi của **Kỹ thuật phần mềm Enterprise**: Dependency Injection (DI) và Inversion of Control (IoC).
- ✅ Am hiểu kiến trúc chuẩn của NestJS: Controller (Điều phối), Service (Nghiệp vụ), Module (Đóng gói).
- ✅ Thiết kế **RESTful API** đạt chuẩn quốc tế (Hiểu mã lỗi HTTP 200, 400, 401, 500).
- ✅ Tránh được cái bẫy **Localhost Network Trap** cực kỳ kinh điển khi kết nối App điện thoại thật với Server máy tính.
- ✅ Viết **DTO + Validation** ở Backend bằng `class-validator` / `class-transformer` và bật `ValidationPipe` toàn cục — lớp phòng thủ song sinh với Zod bên Mobile.
- ✅ Ném lỗi đúng chuẩn bằng **HTTP Exceptions** (`NotFoundException`, `BadRequestException`) và hiểu vai trò của **Exception Filter**.
- ✅ Triển khai **JWT Authentication** và **Guards** thật: dựng `AuthModule` (`login` + **`register`** → ký JWT → `JwtAuthGuard` chặn request) — không còn dừng ở khái niệm.
- ✅ Hiểu tầng **Database**: vì sao Mock Data không thể sống mãi, dựng **Prisma ORM** thật với SQLite (`schema.prisma`, `migrate`, `PrismaService`), và áp dụng **Repository Pattern** để đổi từ in-memory sang Prisma chỉ bằng một dòng `providers`.
- ✅ Tự sinh tài liệu API bằng **Swagger/OpenAPI**, và biết 2 lớp bảo vệ tối thiểu của Production: **Helmet** và **Rate Limiting**.
- ✅ Thiết kế **Orders API** đầy đủ vòng đời thương mại: `POST` tạo đơn `PENDING` → `GET` lịch sử / chi tiết hóa đơn (theo user) → `POST …/pay` giả lập **`PENDING` → `PAID`** — nối vào UI Chương 6.
- ✅ **Thực chiến:** Xây dựng Server NestJS lấy dữ liệu sản phẩm, chi tiết sản phẩm, đăng ký/đăng nhập, đặt hàng + thanh toán giả lập và proxy AI; gọi toàn bộ API này từ App React Native ShopAI.

---

### 0. Nhìn tổng thể trước khi đọc sâu

Từ chương này, ShopAI chính thức có "hai chân": Mobile và Backend. Dưới đây là luồng request chuẩn mà mọi endpoint bạn viết trong Sprint 9 đều đi theo — hãy nhìn kỹ trước khi đọc từng phần lý thuyết.

**Sơ đồ tổng quan — luồng Request Client → NestJS → DB:**

```
┌──────────┐  Authorization:   ┌───────────────────────────────────────────┐   Repository   ┌───────────┐
│  Mobile   │  Bearer <JWT>    │              NESTJS SERVER                  │──────────────▶│    DB      │
│ (Client)  │ ─────────────────▶│  Guard(JWT) ─▶ Controller ─▶ Service ─▶Repo │                │  SQLite    │
│           │   axiosClient    │  (soát vé)    (tiếp tân)   (đầu bếp)  (kho) │◀───────────────│  qua Prisma│
│           │◀───────────────── │                                             │                └───────────┘
└──────────┘   JSON Response    └───────────────────────────────────────────┘
                                        ▲
                                        │
                         ValidationPipe lọc dữ liệu bẩn (DTO + class-validator)
                         Exception Filter chuẩn hoá lỗi trả về (401/404/400/500)
```

**Sau chương này, bạn sẽ làm được gì:**
- ✅ Tự dựng một Server NestJS theo đúng kiến trúc Controller–Service–Module.
- ✅ Viết DTO + `class-validator` để chặn dữ liệu bẩn từ Client, y hệt cách Zod chặn dữ liệu bẩn từ Server ở Chương 6.
- ✅ Kết nối App Mobile với Server qua IP LAN mà không dính bẫy "Localhost Network Trap".
- ✅ Xoá sổ hoàn toàn API Key Gemini khỏi Mobile, chuyển hết logic AI xuống Backend.
- ✅ Thiết kế Orders API tự tính lại tổng tiền ở Server — chặn đứng gian lận dữ liệu từ Client.
- ✅ Bảo vệ Orders API bằng JWT thật: không có Token hợp lệ thì không đặt được đơn.
- ✅ Restart Server không còn làm mất đơn hàng — dữ liệu nằm trong SQLite qua Prisma, không còn trong RAM.

**Lộ trình đọc gợi ý (lý thuyết → thực chiến):**
1. Đọc Phần 9.1–9.2 để hiểu Dependency Injection và mô hình 3 lớp — đây là "ngôn ngữ" xuyên suốt cả chương.
2. Đọc thật kỹ Phần 9.4 (Localhost Trap) TRƯỚC khi mở Terminal chạy Server — phần lớn lỗi "Network request failed" của học viên nằm ở đây.
3. Đọc Phần 9.5–9.6 (DTO, Validation, Exception) song song lúc làm Bước 7b của Sprint.
4. Đọc kỹ Phần 9.7 (JWT + Guards) và Phần 9.8 (Prisma + Repository Pattern) TRƯỚC Bước 7d — hai phần này giờ là code thật sẽ gõ tay ở Sprint, không còn là lý thuyết suông.
5. Làm Sprint 9 theo đúng các bước, dùng bảng "Sổ tay gỡ lỗi" ở cuối Sprint ngay khi bị kẹt thay vì đoán mò.

> [!TIP]
> **Nhầm lẫn thường gặp nhất chương này:** rất nhiều học viên gọi `http://localhost:3000` từ điện thoại thật rồi báo "Server bị lỗi". Server không hề lỗi — `localhost` trên điện thoại trỏ vào chính điện thoại đó, không phải máy tính của bạn. Luôn dùng IP LAN (`http://192.168.x.x:3000`) và nhớ Server phải `listen(3000, '0.0.0.0')` (xem lại Phần 9.4 và Bước 7 của Sprint).

---

## 🌐 PHẦN 9.1: SỰ CHUYỂN MÌNH THÀNH FULLSTACK ENGINEER

Tại sao học Mobile lại phải học viết Backend?
Trong thực tế đi làm, Đội ngũ Mobile và Đội ngũ Backend thường xuyên "Đổ lỗi" (Blame) cho nhau khi App bị lỗi. Backend bảo API chạy đúng, Mobile bảo gọi API không ra.
Hơn nữa, ở Chương 8, việc ta để lộ API Key của Gemini AI ngay trong mã nguồn Mobile (Frontend) là một **LỖI BẢO MẬT NGHIÊM TRỌNG**. Kẻ gian sẽ dịch ngược file APK, cướp API Key và xài ké tiền của bạn.

**Giải pháp:** Ta cần dựng một máy chủ (Backend Server) làm lớp khiên bảo vệ ở giữa.
`[Mobile App] <----> [Backend Server (NestJS)] <----> [Database / Google AI]`
Mobile App sẽ không bao giờ biết API Key là gì, nó chỉ gọi lên Backend, Backend sẽ dùng API Key (lưu an toàn trên Server) gọi sang Google AI rồi trả kết quả về cho Mobile.

---

## 🧱 PHẦN 9.2: KIẾN TRÚC ENTERPRISE CỦA NESTJS

Node.js (với Express) là framework phổ biến nhưng viết code rất lộn xộn. Mỗi người viết một kiểu. 
**NestJS** ra đời để giải quyết việc đó. Nó ép mọi lập trình viên tuân thủ kiến trúc chặt chẽ của Angular. Nó được sử dụng ở mọi tập đoàn lớn.

### 1. Dependency Injection (DI) & Inversion of Control (IoC)
Đây là kiến thức hàn lâm có trong môn "Kiến trúc thiết kế phần mềm".
- **Cách viết code truyền thống (Tự Sinh - Tự Diệt):** Nếu Xe Ô tô cần Động cơ. Trong class Ô tô, bạn viết `const engine = new Engine()`. Ô tô bị gắn chết với cái Động cơ đó. Rất khó để thay thế thành Động cơ Điện.
- **Dependency Injection (Tiêm phụ thuộc):** Class Ô tô không tự tạo Động cơ nữa. Bạn truyền Động cơ cho nó qua tham số `constructor(private engine: Engine)`. 
- **Inversion of Control (Đảo ngược quyền điều khiển):** NestJS cung cấp một cái Hộp chứa (IoC Container). Cái hộp này tự động tạo ra sẵn một cái Động cơ từ trước. Bất cứ khi nào bạn báo *"Tôi cần khởi tạo Ô tô"*, NestJS sẽ tự động **Tiêm (Inject)** cái Động cơ vào Ô tô cho bạn.

Điều này giúp mã nguồn phân tách hoàn toàn, cực kỳ dễ bảo trì và viết Unit Test.

### 2. Mô hình 3 lớp thần thánh của NestJS
1. **Controller (Người tiếp tân):** Chỉ nhận HTTP Request từ Mobile, kiểm tra xem dữ liệu Mobile gửi có đúng định dạng không, gọi Service xử lý, rồi trả HTTP Response về.
2. **Service (Đầu bếp):** Nơi chứa toàn bộ não bộ tính toán (Business Logic). Nó xử lý dữ liệu, cộng trừ nhân chia, nói chuyện với Database.
3. **Module (Thùng chứa):** Nơi gói ghém Controller và Service lại thành một khối. (VD: `ProductModule` chứa `ProductController` và `ProductService`).

---

## 🛜 PHẦN 9.3: RESTFUL API VÀ HTTP STATUS CODES

Là một kỹ sư, bạn không thể code Backend trả về `{ error: true, msg: "Sai mk" }` kèm mã lỗi 200 OK. Hệ thống mạng toàn cầu có một ngôn ngữ chung gọi là RESTful.

**1. Các phương thức (Methods):**
- **GET:** Lấy dữ liệu về (VD: Lấy danh sách sản phẩm).
- **POST:** Tạo dữ liệu mới (VD: Gửi thông tin Đăng ký tài khoản).
- **PUT / PATCH:** Cập nhật dữ liệu (VD: Đổi mật khẩu).
- **DELETE:** Xóa dữ liệu.

**2. Mã trạng thái chuẩn quốc tế (Status Codes):**
- **2xx (Thành công):** `200 OK`, `201 Created` (Vừa tạo thành công).
- **4xx (Lỗi do thằng Mobile gọi ngu):** `400 Bad Request` (Gửi thiếu ID), `401 Unauthorized` (Chưa đăng nhập), `403 Forbidden` (Đăng nhập rồi nhưng không phải Admin), `404 Not Found`.
- **5xx (Lỗi do Server ngu):** `500 Internal Server Error` (Backend code lỗi gây Crash).

---

## ⚠️ PHẦN 9.4: LOCALHOST NETWORK TRAP (CÁI BẪY MẠNG NỘI BỘ)

Đây là bẫy kinh điển làm 99% sinh viên gục ngã khi tích hợp Mobile và Backend.
- Bạn chạy Backend NestJS trên máy tính: `http://localhost:3000`
- Bạn lấy điện thoại thật bật app React Native lên, viết code Axios gọi vào `http://localhost:3000/api/products`.
**KẾT QUẢ: LỖI NETWORK ERROR!**

**Giải thích học thuật:**
Chữ `localhost` (hoặc IP `127.0.0.1`) có nghĩa là **Chính thiết bị của tôi**.
- Trên máy tính, `localhost` trỏ vào ổ cứng máy tính.
- Trên điện thoại thật, `localhost` trỏ vào BỘ NHỚ TRONG CỦA ĐIỆN THOẠI. Điên thoại của bạn đâu có chạy Server NestJS? Do đó nó không tìm thấy gì cả!

**Cách giải quyết:**
Bạn phải dùng **IP LAN** của máy tính (VD: `http://192.168.1.5:3000`). Đồng thời máy tính và điện thoại phải kết nối **CÙNG MỘT MẠNG WIFI**.

**Bảng tra cứu nhanh — địa chỉ nào cho môi trường nào:**

| Bạn đang chạy App ở đâu? | Địa chỉ Backend phải điền vào `API_BASE_URL` | Vì sao |
|---|---|---|
| Máy ảo Android (Emulator) | `http://10.0.2.2:3000` | `10.0.2.2` là "cửa sổ" đặc biệt mà Android Emulator mở ra để nhìn về máy tính chủ |
| Máy ảo iOS (Simulator) | `http://localhost:3000` | Simulator dùng chung card mạng với máy Mac, nên `localhost` vẫn đúng |
| Điện thoại Android/iOS **thật** | `http://192.168.1.x:3000` (IP LAN) | Điện thoại là một máy tính riêng biệt, phải gọi qua Wifi bằng địa chỉ mạng thật |
| Server đã deploy lên mây | `https://api.shopai.com` | Có domain thật, có HTTPS, không còn khái niệm IP LAN |

> [!TIP]
> Cách lấy IP LAN: trên macOS/Linux gõ `ifconfig | grep "inet "`, trên Windows gõ `ipconfig` rồi tìm dòng `IPv4 Address` của card Wi-Fi. IP này **đổi mỗi khi bạn đổi mạng Wifi** (về nhà, ra quán cafe) — nên đây là dòng code bạn sẽ sửa nhiều nhất trong Chương 9. Đó chính là lý do ta gom nó vào đúng một file hằng số `API_BASE_URL` ở Sprint bên dưới.

---

## 🧾 PHẦN 9.5: DTO VÀ VALIDATION — TRẠM KIỂM SOÁT PHÍA SERVER

Ở Chương 6, ta đã dựng **Zod** ở phía Mobile để chặn dữ liệu bẩn từ Server đi vào UI. Nhưng chiều ngược lại thì sao? Mobile gửi lên Server một cục JSON — Server có được phép tin tưởng không?

**Tuyệt đối KHÔNG.** Đây là nguyên tắc số 1 của bảo mật Backend: *"Never trust the client"* (Đừng bao giờ tin thằng Client). Lý do rất đơn giản: một kẻ tấn công không cần dùng App của bạn, họ chỉ cần mở Postman và bắn thẳng vào `POST /api/orders` với `{ "total": -5000000 }` để tạo đơn hàng âm tiền. Nếu Server không kiểm tra, cơ sở dữ liệu của bạn sẽ tan nát.

### 1. DTO là gì?

**DTO (Data Transfer Object — Đối tượng truyền dữ liệu)** là một Class TypeScript mô tả **chính xác hình dạng dữ liệu mà Client được phép gửi lên**. Nó đóng 3 vai trò cùng lúc:
1. **Tài liệu sống:** Nhìn vào file DTO là biết ngay API này nhận những trường nào.
2. **Bộ lọc:** Những trường lạ Client cố tình nhét thêm (VD `isAdmin: true`) sẽ bị loại bỏ.
3. **Bộ kiểm duyệt:** Kết hợp với `class-validator` để tự động chặn dữ liệu sai định dạng.

### 2. Hai thư viện song sinh: `class-validator` và `class-transformer`

- **`class-validator`:** Cung cấp các Decorator gắn lên từng thuộc tính để mô tả luật (`@IsString()`, `@IsNumber()`, `@Min(0)`, `@IsNotEmpty()`, `@IsArray()`...).
- **`class-transformer`:** Biến cục JSON thô (`plain object`) thành **instance của Class DTO** — bước bắt buộc, vì Decorator chỉ hoạt động trên Class thật, không hoạt động trên JSON thuần. Nó còn tự ép kiểu: chuỗi `"5"` từ URL param có thể tự biến thành số `5`.

```typescript
import { IsNotEmpty, IsNumber, IsString, Min, MaxLength } from 'class-validator';

export class CreateProductDto {
  @IsString()
  @IsNotEmpty({ message: 'Tên sản phẩm không được để trống' }) // Có thể tự viết thông báo lỗi tiếng Việt
  @MaxLength(200)
  name: string;

  @IsNumber()
  @Min(0, { message: 'Giá sản phẩm không được âm' })
  price: number;
}
```

### 3. `ValidationPipe` toàn cục — bật một lần, bảo vệ mọi Endpoint

**Pipe** trong NestJS là một "cái phễu" mà dữ liệu phải chui qua **trước khi** chạm tới hàm trong Controller. `ValidationPipe` là Pipe có sẵn của Nest, chuyên đọc các Decorator của `class-validator` rồi tự động chặn Request sai.

```typescript
app.useGlobalPipes(
  new ValidationPipe({
    whitelist: true,            // Tự động XÓA mọi trường không khai báo trong DTO
    forbidNonWhitelisted: true, // Hoặc gắt hơn: thấy trường lạ thì báo lỗi 400 luôn
    transform: true,            // Bật class-transformer: ép JSON thành instance DTO, tự ép kiểu
  }),
);
```

Khi bật xong, bạn **không cần viết một dòng `if` kiểm tra nào** trong Controller nữa. Client gửi `{ name: "", price: -100 }` sẽ nhận về ngay `400 Bad Request` kèm danh sách lỗi chi tiết:

```json
{
  "statusCode": 400,
  "message": ["Tên sản phẩm không được để trống", "Giá sản phẩm không được âm"],
  "error": "Bad Request"
}
```

> [!IMPORTANT]
> **Zod (Mobile) và class-validator (Backend) KHÔNG thay thế được cho nhau** — chúng bảo vệ hai hướng khác nhau của cùng một đường ống. Zod bảo vệ App khỏi Server trả dữ liệu hỏng (tránh crash UI). `class-validator` bảo vệ Server khỏi Client gửi dữ liệu độc (tránh hỏng dữ liệu). Một kỹ sư Fullstack phải cài **cả hai đầu**, vì mỗi đầu đều có thể bị thay thế bởi kẻ xấu.

---

## 🚨 PHẦN 9.6: EXCEPTION FILTER VÀ HTTP EXCEPTIONS

Ở Phần 9.3 ta đã học các mã lỗi HTTP. Giờ là cách **ném** chúng ra đúng chuẩn trong NestJS.

### 1. Ném lỗi bằng Class có sẵn, đừng tự chế

NestJS cung cấp sẵn một bộ Exception ứng với từng mã HTTP. Bạn chỉ cần `throw` ra, Nest tự động biến nó thành HTTP Response đúng định dạng:

```typescript
import {
  NotFoundException,      // 404 — Không tìm thấy tài nguyên
  BadRequestException,    // 400 — Client gửi dữ liệu sai
  UnauthorizedException,  // 401 — Chưa đăng nhập / Token sai
  ForbiddenException,     // 403 — Đã đăng nhập nhưng không đủ quyền
  ConflictException,      // 409 — Xung đột (VD: email đã tồn tại)
} from '@nestjs/common';

getProductById(id: string) {
  const product = this.products.find((p) => p.id === id);
  if (!product) {
    // KHÔNG return null! Trả null khiến Mobile nhận 200 OK kèm body rỗng -> rất khó debug.
    throw new NotFoundException(`Không tìm thấy sản phẩm có id = ${id}`);
  }
  return product;
}
```

Mobile sẽ nhận đúng `404` với body:
```json
{ "statusCode": 404, "message": "Không tìm thấy sản phẩm có id = xyz", "error": "Not Found" }
```

Và ở phía Mobile, đoạn `if (!response.ok) throw new Error(...)` mà bạn đã viết ở Chương 6 sẽ **tự động bắt được** lỗi này, hiển thị UI lỗi cho người dùng — hai đầu ăn khớp hoàn hảo.

### 2. Exception Filter — người gác cổng cuối cùng

**Exception Filter** là lớp bọc ngoài cùng, bắt **mọi** lỗi chưa được xử lý trước khi nó thoát ra khỏi Server. Vai trò thực tế của nó trong dự án đi làm:
- **Chuẩn hóa format lỗi:** Mọi lỗi trả về đều có cùng cấu trúc `{ statusCode, message, path, timestamp }` — Mobile chỉ cần viết một hàm xử lý lỗi duy nhất.
- **Che giấu thông tin nhạy cảm:** Lỗi Database (`ER_DUP_ENTRY: Duplicate entry 'admin@shop.com' for key 'users.email'`) tuyệt đối không được lọt ra ngoài — nó tiết lộ cả tên bảng, tên cột cho hacker.
- **Ghi log tập trung:** Mọi lỗi 500 đều được ghi vào một chỗ để đội DevOps theo dõi (giống Crashlytics của Mobile ở Chương 10).

```typescript
import { ArgumentsHost, Catch, ExceptionFilter, HttpException, HttpStatus } from '@nestjs/common';
import { Response, Request } from 'express';

@Catch() // Không truyền tham số = bắt TẤT CẢ mọi loại lỗi
export class AllExceptionsFilter implements ExceptionFilter {
  catch(exception: unknown, host: ArgumentsHost) {
    const ctx = host.switchToHttp();
    const response = ctx.getResponse<Response>();
    const request = ctx.getRequest<Request>();

    const status =
      exception instanceof HttpException
        ? exception.getStatus()
        : HttpStatus.INTERNAL_SERVER_ERROR; // Lỗi lạ không rõ nguồn gốc -> quy về 500

    response.status(status).json({
      statusCode: status,
      path: request.url,
      timestamp: new Date().toISOString(),
      message:
        exception instanceof HttpException
          ? exception.getResponse()
          : 'Đã có lỗi xảy ra phía máy chủ', // Che lỗi thật, không lộ chi tiết Database
    });
  }
}
```

Đăng ký một dòng trong `main.ts`: `app.useGlobalFilters(new AllExceptionsFilter());`

> [!NOTE]
> Exception Filter là kiến thức **nên biết** nhưng **không bắt buộc** trong Sprint 9 — NestJS đã có sẵn một Filter mặc định làm khá tốt việc này. Chỉ khi cần format lỗi riêng cho App của bạn thì mới viết Filter tùy chỉnh.

---

## 🔐 PHẦN 9.7: JWT AUTHENTICATION VÀ GUARDS — TỪ LÝ THUYẾT ĐẾN CODE THẬT

Ở Chương 5, 6 và 8, `LoginScreen` của ShopAI mới chỉ **giả lập** đăng nhập — bấm nút là `login('mock_token_123')`, một chuỗi bịa ra chứ không phải Token thật do Server ký. Nó đủ để dạy Zustand + SecureStore, nhưng có một sự thật trần trụi: **chuỗi `mock_token_123` sẽ không bao giờ qua được một Guard thật**, vì Guard thật kiểm tra chữ ký mã hoá chứ không kiểm tra "có Token hay không". Phần này ta dựng `AuthModule` thật, sinh JWT thật, và dùng nó khoá `POST /api/orders` lại — đúng như một Server thương mại điện tử thật phải làm.

### 1. Vấn đề: HTTP không có trí nhớ

HTTP là giao thức **Stateless** — mỗi Request là một cuộc gặp gỡ hoàn toàn xa lạ. Server không hề nhớ rằng 2 giây trước bạn vừa đăng nhập thành công. Vậy làm sao Request thứ hai chứng minh được "tôi chính là người vừa login"?

### 2. JWT (JSON Web Token) — tấm vé xem phim có dấu niêm phong

JWT là một chuỗi ký tự gồm 3 phần nối bằng dấu chấm: `header.payload.signature`

```
eyJhbGciOiJIUzI1NiJ9  .  eyJzdWIiOiJ1XzAwMSIsIm5hbWUiOiJBbiJ9  .  4pcPyMD09olPSyXn
     (Header)                        (Payload)                        (Signature)
   Thuật toán ký           Dữ liệu: userId, tên, hạn dùng        Chữ ký niêm phong
```

- **Header + Payload** chỉ là JSON được mã hóa Base64 — **ai cũng đọc được** (thử dán vào trang `jwt.io`). Vì vậy **tuyệt đối không nhét mật khẩu, số thẻ tín dụng vào Payload**.
- **Signature** mới là thứ quan trọng: Server dùng một chuỗi bí mật (`JWT_SECRET`, chỉ Server biết) để ký. Nếu hacker sửa `"role": "user"` thành `"role": "admin"` trong Payload, chữ ký sẽ không còn khớp, Server phát hiện ngay và từ chối.

**Vì sao JWT tiện?** Server không cần lưu Token vào Database. Nó chỉ cần kiểm tra chữ ký là biết Token thật hay giả — gọi là *stateless authentication*, cực kỳ dễ mở rộng ra nhiều máy chủ.

### 3. Luồng đi của Token

```
[Mobile] POST /api/auth/login { email, password }
    ↓
[Server] Kiểm tra mật khẩu (đã hash bằng bcrypt) → Đúng → Ký JWT → trả { accessToken }
    ↓
[Mobile] Lưu Token vào expo-secure-store (Chương 8 — Keystore phần cứng, KHÔNG dùng AsyncStorage)
    ↓
[Mobile] Mọi Request sau đó gắn Header: Authorization: Bearer <accessToken>
         (đúng chỗ mà Axios Interceptor ở Chương 6 đang làm tự động)
    ↓
[Server] Guard chặn Request lại, mở Token ra kiểm tra chữ ký + hạn dùng
         → Hợp lệ: cho đi tiếp vào Controller, gắn kèm thông tin user
         → Không hợp lệ: ném UnauthorizedException (401)
```

### 4. Guard — người soát vé đứng trước cửa Controller

**Guard** trả lời đúng một câu hỏi: *"Request này có được phép đi tiếp không?"* — trả `true` là cho qua, `false`/throw là chặn lại. Cú pháp NestJS chuẩn (Passport strategy tên `'jwt'`) trông như sau — đây chính xác là dòng ta sẽ gắn lên `OrderController` thật ở Bước 7f:

```typescript
import { Controller, Post, UseGuards } from '@nestjs/common';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';

@Controller('api/orders')
export class OrderController {
  @Post()
  @UseGuards(JwtAuthGuard) // Chỉ 1 dòng này: ai không có Token hợp lệ sẽ nhận 401 ngay, Controller không cần if nào
  create(/* ... */) {
    /* ... */
  }
}
```

**Thứ tự các "trạm gác" mà một Request phải đi qua trong NestJS** — nhớ đúng thứ tự này sẽ giúp bạn debug rất nhanh:

```
Request → Middleware (Helmet) → Guard (Auth) → Interceptor → Pipe (Validation) → Controller → Service
```

> [!IMPORTANT]
> Sprint 9 **đã triển khai JWT thật** (không còn là khái niệm suông) — xem đủ 8 bước dựng `AuthModule` ngay bên dưới. `POST /api/orders` sẽ được khoá bằng `JwtAuthGuard` thật ở Bước 7f: gọi mà không đính `Authorization: Bearer <token>` hợp lệ sẽ nhận đúng `401 Unauthorized`, không có ngoại lệ "để đơn giản cho lớp học" nào ở đây cả — đây chính là hành vi bắt buộc khi đi làm.

### 5. Dựng `AuthModule` thật — sinh JWT và xác thực mật khẩu

Mục tiêu: `POST /api/auth/login` nhận `{ email, password }`, so khớp với mật khẩu đã **hash bằng bcrypt** trong Database (Phần 9.8), rồi ký một JWT thật trả về cho Mobile.

**5.1. Cài đặt thư viện:**
```bash
npm install @nestjs/jwt @nestjs/passport passport passport-jwt bcrypt
npm install -D @types/passport-jwt @types/bcrypt
```

**5.2. Khai báo bí mật ký Token trong `.env`** (thêm vào file đã có từ Bước 6.2):
```
JWT_SECRET=doi-chuoi-nay-thanh-mot-chuoi-that-dai-va-ngau-nhien
JWT_EXPIRES_IN=7d
```

> [!WARNING]
> `JWT_SECRET` là chìa khoá của toàn bộ hệ thống xác thực — ai có chuỗi này có thể tự ký Token giả mạo bất kỳ user nào. Tuyệt đối không commit `.env`, không hardcode chuỗi này trong code, và ở Production phải dùng một chuỗi ngẫu nhiên dài (VD sinh bằng `openssl rand -base64 32`).

**5.3. `LoginDto`** — tạo `src/auth/dto/login.dto.ts`:
```typescript
import { IsEmail, IsString, MinLength } from 'class-validator';

export class LoginDto {
  @IsEmail({}, { message: 'Email không đúng định dạng' })
  email: string;

  @IsString()
  @MinLength(6, { message: 'Mật khẩu phải có ít nhất 6 ký tự' })
  password: string;
}
```

| Khối lệnh | Giải thích |
|---|---|
| `@IsEmail()` | Chặn `email: "khong-phai-email"` ngay tại `ValidationPipe`, trước khi chạm Controller |
| `@MinLength(6)` | Khớp đúng luật `password.length < 6` mà `LoginScreen` (Chương 6) đã validate ở phía Client — **hai đầu phải đồng bộ luật** |

**5.4. `AuthService`** — nơi xác thực mật khẩu và ký Token. Tạo `src/auth/auth.service.ts`:
```typescript
import { Injectable, UnauthorizedException } from '@nestjs/common';
import { JwtService } from '@nestjs/jwt';
import * as bcrypt from 'bcrypt';
import { PrismaService } from '../prisma/prisma.service';
import { LoginDto } from './dto/login.dto';

@Injectable()
export class AuthService {
  constructor(
    private readonly prisma: PrismaService,
    private readonly jwtService: JwtService,
  ) {}

  // Bước 1: tra User trong DB bằng email, so khớp mật khẩu đã hash
  async validateUser(email: string, password: string) {
    const user = await this.prisma.user.findUnique({ where: { email } });
    if (!user) return null;

    // bcrypt.compare tự hash lại "password" vừa gõ rồi so với chuỗi hash lưu sẵn — KHÔNG BAO GIỜ so sánh chuỗi thường
    const isMatch = await bcrypt.compare(password, user.password);
    if (!isMatch) return null;

    return user;
  }

  // Bước 2: nếu đúng, ký một JWT chứa "sub" (subject = userId) và email
  async login(dto: LoginDto) {
    const user = await this.validateUser(dto.email, dto.password);
    if (!user) {
      // Cố tình dùng CHUNG một thông báo cho cả 2 trường hợp "sai email" và "sai mật khẩu"
      // -> tránh lộ cho hacker biết email nào đã tồn tại trong hệ thống (User Enumeration)
      throw new UnauthorizedException('Email hoặc mật khẩu không đúng');
    }

    const payload = { sub: user.id, email: user.email };
    return {
      accessToken: this.jwtService.sign(payload), // Ký bằng JWT_SECRET đã đăng ký ở AuthModule
      user: { id: user.id, email: user.email, name: user.name },
    };
  }
}
```

| Khối lệnh | Giải thích |
|---|---|
| `bcrypt.compare(password, user.password)` | So khớp mật khẩu người dùng gõ với chuỗi **đã hash** trong DB. Không dùng `===` vì DB không bao giờ lưu mật khẩu dạng thường (Phần 9.8 mục seed User sẽ hash trước khi lưu) |
| `payload = { sub: user.id, email }` | `sub` (subject) là tên trường chuẩn JWT dùng để lưu định danh chủ thể Token — mai này `JwtStrategy` đọc lại đúng trường này |
| `this.jwtService.sign(payload)` | `JwtService` (từ `@nestjs/jwt`, cấu hình ở `AuthModule` mục 5.8) tự động ráp `header.payload.signature` bằng `JWT_SECRET` |
| Thông báo lỗi dùng chung | Nguyên tắc bảo mật: không cho hacker dò được "email này có tồn tại hay không" qua 2 thông báo lỗi khác nhau |

**5.5. `JwtStrategy`** — "người phiên dịch" cho Passport biết cách lấy và kiểm tra Token. Tạo `src/auth/jwt.strategy.ts`:
```typescript
import { Injectable } from '@nestjs/common';
import { PassportStrategy } from '@nestjs/passport';
import { ConfigService } from '@nestjs/config';
import { ExtractJwt, Strategy } from 'passport-jwt';

@Injectable()
export class JwtStrategy extends PassportStrategy(Strategy) {
  constructor(configService: ConfigService) {
    super({
      // Đọc đúng định dạng Header "Authorization: Bearer <token>" mà axiosClient (Chương 6) đang tự gắn
      jwtFromRequest: ExtractJwt.fromAuthHeaderAsBearerToken(),
      ignoreExpiration: false, // Token hết hạn (JWT_EXPIRES_IN) phải bị từ chối, không được du di
      secretOrKey: configService.get<string>('JWT_SECRET'), // Cùng bí mật đã dùng để ký ở AuthService
    });
  }

  // Passport TỰ ĐỘNG gọi hàm này SAU KHI xác minh chữ ký hợp lệ và Token chưa hết hạn.
  // Giá trị return ở đây sẽ được Nest gắn thẳng vào `request.user` cho MỌI Controller phía sau Guard.
  async validate(payload: { sub: string; email: string }) {
    return { userId: payload.sub, email: payload.email };
  }
}
```

| Khối lệnh | Giải thích |
|---|---|
| `ExtractJwt.fromAuthHeaderAsBearerToken()` | Tự tách chuỗi `<token>` ra khỏi Header `Authorization: Bearer <token>` — đúng định dạng Mobile gửi lên (Phần 9.7 mục 3) |
| `ignoreExpiration: false` | Nếu để `true`, Token hết hạn vẫn được chấp nhận — một lỗ hổng bảo mật kinh điển, đừng bao giờ bật |
| Hàm `validate()` | Chỉ chạy khi chữ ký ĐÃ hợp lệ. Đây là nơi duy nhất, nếu cần, có thể tra thêm DB xem User có bị khoá tài khoản hay không trước khi cho qua |

**5.6. `JwtAuthGuard`** — lớp vỏ mỏng để `@UseGuards` gọi cho gọn. Tạo `src/auth/jwt-auth.guard.ts`:
```typescript
import { Injectable } from '@nestjs/common';
import { AuthGuard } from '@nestjs/passport';

// AuthGuard('jwt') tự động dùng đúng JwtStrategy đã đăng ký ở trên (tên mặc định của Strategy là 'jwt')
@Injectable()
export class JwtAuthGuard extends AuthGuard('jwt') {}
```

**5.7. `AuthController`** — tạo `src/auth/auth.controller.ts`:
```typescript
import { Body, Controller, HttpCode, HttpStatus, Post } from '@nestjs/common';
import { ApiOperation, ApiTags } from '@nestjs/swagger';
import { AuthService } from './auth.service';
import { LoginDto } from './dto/login.dto';
import { RegisterDto } from './dto/register.dto';

@ApiTags('Auth')
@Controller('api/auth')
export class AuthController {
  constructor(private readonly authService: AuthService) {}

  @Post('login') // POST /api/auth/login
  @HttpCode(HttpStatus.OK) // Mặc định NestJS trả 201 cho POST, ta ép về 200 vì đây là "đăng nhập" chứ không "tạo mới"
  @ApiOperation({ summary: 'Đăng nhập bằng email + mật khẩu, trả về accessToken JWT' })
  login(@Body() dto: LoginDto) {
    return this.authService.login(dto);
  }

  @Post('register') // POST /api/auth/register — nối RegisterScreen (Ch.5/6)
  @ApiOperation({ summary: 'Đăng ký tài khoản mới (hash bcrypt), trả accessToken như login' })
  register(@Body() dto: RegisterDto) {
    return this.authService.register(dto);
  }
}
```

**5.7b. `RegisterDto` + `AuthService.register`** — tạo `src/auth/dto/register.dto.ts`:

```typescript
import { IsEmail, IsOptional, IsString, MinLength } from 'class-validator';

export class RegisterDto {
  @IsEmail()
  email: string;

  @IsString()
  @MinLength(6)
  password: string;

  @IsOptional()
  @IsString()
  @MinLength(2)
  name?: string;
}
```

Thêm vào `AuthService` (cùng file mục 5.4):

```typescript
import { ConflictException, Injectable, UnauthorizedException } from '@nestjs/common';
import * as bcrypt from 'bcrypt';
import { RegisterDto } from './dto/register.dto';

// trong class AuthService:
async register(dto: RegisterDto) {
  const exists = await this.prisma.user.findUnique({ where: { email: dto.email } });
  if (exists) {
    throw new ConflictException('Email đã được đăng ký');
  }
  const hash = await bcrypt.hash(dto.password, 10);
  await this.prisma.user.create({
    data: {
      email: dto.email,
      password: hash,
      name: dto.name ?? null,
    },
  });
  // Đăng ký xong → đăng nhập luôn (cùng contract { accessToken, user } như login)
  return this.login({ email: dto.email, password: dto.password });
}
```

> [!TIP]
> `ConflictException` → HTTP **409**. Mobile `RegisterScreen` nên hiện message rõ khi email trùng.

**5.8. `AuthModule`** — ráp tất cả lại, tạo `src/auth/auth.module.ts`:
```typescript
import { Module } from '@nestjs/common';
import { JwtModule } from '@nestjs/jwt';
import { PassportModule } from '@nestjs/passport';
import { ConfigModule, ConfigService } from '@nestjs/config';
import { AuthController } from './auth.controller';
import { AuthService } from './auth.service';
import { JwtStrategy } from './jwt.strategy';

@Module({
  imports: [
    PassportModule,
    // registerAsync vì JWT_SECRET nằm trong .env, cần đợi ConfigService đọc xong mới cấu hình được
    JwtModule.registerAsync({
      imports: [ConfigModule],
      inject: [ConfigService],
      useFactory: (config: ConfigService) => ({
        secret: config.get<string>('JWT_SECRET'),
        signOptions: { expiresIn: config.get<string>('JWT_EXPIRES_IN') ?? '7d' },
      }),
    }),
  ],
  controllers: [AuthController],
  providers: [AuthService, JwtStrategy],
  exports: [JwtStrategy], // Không bắt buộc, nhưng tiện nếu Module khác cần tái sử dụng Strategy này
})
export class AuthModule {}
```

Đăng ký `AuthModule` vào `src/app.module.ts` (chỉ **thêm** vào mảng `imports` đã có):
```typescript
imports: [ConfigModule.forRoot({ isGlobal: true }), PrismaModule, ProductModule, AiModule, OrderModule, AuthModule],
```

### 6. Bearer Token khớp nối với Mobile như thế nào — không cần viết thêm dòng code Mobile nào

Đây là điểm đẹp nhất của thiết kế: **Mobile đã sẵn sàng cho JWT thật từ tận Chương 6**, ta không cần sửa cơ chế gửi Token — chỉ cần đổi nguồn gốc của Token đó.

| Lớp | Đã có từ Chương nào | Việc nó làm | Có cần sửa ở Sprint 9 không? |
|---|---|---|---|
| `useAuthStore` (Zustand) | Ch.6, nâng cấp Ch.8 | Giữ `token` trong RAM + mã hoá vào `SecureStore` | Không sửa cơ chế — chỉ đổi **giá trị** truyền vào `login()` từ chuỗi giả sang `accessToken` thật (Bước 9d) |
| `axiosClient` Request Interceptor | Ch.6 (Phần 6.6) | Tự đọc `useAuthStore.getState().token`, gắn `Authorization: Bearer <token>` vào MỌI request | Không sửa gì — Interceptor không quan tâm Token là giả hay thật |
| `JwtStrategy.jwtFromRequest` | Sprint 9 (mục 5.5) | Tách đúng chuỗi sau chữ `Bearer ` ra khỏi Header đó | Là phần mới, khớp 100% với định dạng axiosClient đã gửi sẵn |
| `axiosClient` Response Interceptor | Ch.6 (Phần 6.6) | Bắt `401` → tự động `logout()` | Giờ mới thật sự "sống": Token hết hạn (`JWT_EXPIRES_IN`) → Guard trả 401 → Mobile tự đăng xuất |

> [!TIP]
> Chính vì `axiosClient` đã được dựng đúng chuẩn từ Chương 6 (baseURL tập trung + Interceptor tự gắn Token), việc "thêm JWT thật" ở Sprint 9 gần như không đụng đến Mobile — bằng chứng rõ nhất cho việc tách lớp (Interceptor) đúng ngay từ đầu sẽ tiết kiệm cực nhiều công sức về sau. Việc cần làm duy nhất ở Mobile: đổi `CheckoutScreen` từ `fetch` thô sang `axiosClient` (Bước 9c) và cho `LoginScreen` gọi API thật thay vì Token giả (Bước 9d).

---

## 🗄️ PHẦN 9.8: TẦNG DATABASE — DỰNG PRISMA THẬT, KHÔNG CÒN CHỈ LÀ MINH HOẠ

Ở Bước 3 của Sprint, `ProductService` trả về 20 sản phẩm sinh bằng `Array.from(...)`, còn Orders (nếu để in-memory) sẽ nằm trong một mảng RAM. Điều này có 3 vấn đề chí tử khi đưa vào thực tế:
1. **Dữ liệu bốc hơi:** Restart Server là mọi thay đổi biến mất — đơn hàng khách vừa đặt cũng mất theo.
2. **Không chia sẻ được:** Chạy 2 máy chủ song song để chịu tải, mỗi máy có một bộ dữ liệu riêng, khách hàng lúc thấy đơn lúc không.
3. **Không truy vấn được:** Tìm "sản phẩm giá dưới 5 triệu, sắp xếp theo lượt bán" bằng vòng `for` trên 1 triệu bản ghi là không khả thi.

Phần này ta giải quyết dứt điểm vấn đề #1 cho Orders và User bằng **Prisma thật**, chạy trên **SQLite** — một file Database gọn nhẹ, không cần cài Server riêng, cực hợp với môi trường lớp học.

### 1. ORM là gì và vì sao không viết SQL tay?

**ORM (Object-Relational Mapping)** là lớp phiên dịch giữa Class TypeScript và bảng trong Database. Bạn viết `prisma.product.findMany({ where: { price: { lt: 5000000 } } })`, ORM tự dịch thành `SELECT * FROM products WHERE price < 5000000`.

Lợi ích lớn nhất không phải là "khỏi viết SQL", mà là **an toàn kiểu (Type Safety)**: gõ sai tên cột, TypeScript báo đỏ ngay lúc code chứ không đợi đến khi chạy thật mới sập. Ngoài ra ORM còn tự động chống **SQL Injection** — lỗ hổng bảo mật cổ điển nhất của web.

### 2. Prisma vs TypeORM — chọn cái nào?

| Tiêu chí | **Prisma** (khuyến nghị cho người mới, dùng trong Sprint 9) | **TypeORM** |
|---|---|---|
| Cách mô tả dữ liệu | File `schema.prisma` riêng, cú pháp tự nhiên dễ đọc | Decorator `@Entity()`, `@Column()` gắn trên Class |
| Type Safety | Xuất sắc — tự sinh Type từ Schema, IDE gợi ý đến từng cột | Khá, đôi chỗ phải tự ép kiểu |
| Migration | `prisma migrate dev` — rất mượt, tự sinh file SQL | `typeorm migration:generate` — nhiều thao tác hơn |
| Tích hợp NestJS | Cần tự viết một `PrismaService` nhỏ (~10 dòng) | Có sẵn `@nestjs/typeorm` chính chủ |
| Hợp với ai | Dự án mới, đội trẻ, ưu tiên tốc độ phát triển | Dự án cũ, đội quen với Java Hibernate |

### 3. Vì sao chọn SQLite cho lớp học (không phải PostgreSQL/MySQL)?

Prisma hỗ trợ nhiều `provider` trong khối `datasource` (`postgresql`, `mysql`, `sqlite`...) — chỉ đổi đúng một dòng là chuyển hẳn hệ quản trị Database mà không sửa code Service/Controller nào. Ở Production, đội Backend thật thường chọn `postgresql`. Nhưng cho **lớp học**, ta chọn `provider = "sqlite"` vì:
- **Không cần cài Server Database riêng** — SQLite là một **file** (`dev.db`) nằm ngay trong thư mục dự án, ai cũng chạy được ngay lập tức, không tốn công cài Docker/Postgres.
- **Đủ mạnh cho bài toán của Sprint 9** — vài chục sản phẩm, vài chục đơn hàng không cần một Server Database chuyên dụng.
- **Dễ reset:** lỡ dữ liệu rối tung, chỉ cần xoá file `prisma/dev.db` và chạy lại `migrate` là có Database sạch tinh.

> [!NOTE]
> Đây là lựa chọn **vì đơn giản hoá cho lớp học**, không phải giới hạn kỹ thuật. Muốn nâng cấp lên PostgreSQL cho Production, chỉ cần đổi `provider = "postgresql"` và `DATABASE_URL` trỏ vào chuỗi kết nối Postgres — toàn bộ code Prisma Client (`prisma.order.create(...)`) giữ nguyên không đổi một chữ.

### 4. `schema.prisma` — bản thiết kế Database của ShopAI

Đây là schema thật sẽ dùng ở Bước 7d, mô tả đủ 4 bảng: `User` (đăng nhập), `Product` (catalog), `Order` + `OrderItem` (đơn hàng và các dòng sản phẩm trong đơn):

```prisma
// prisma/schema.prisma

datasource db {
  provider = "sqlite"                // Đổi thành "postgresql" khi lên Production, giữ nguyên phần còn lại
  url      = env("DATABASE_URL")     // Đọc từ .env, KHÔNG hardcode đường dẫn
}

generator client {
  provider = "prisma-client-js"
}

model User {
  id        String   @id @default(uuid())
  email     String   @unique          // Không cho 2 tài khoản trùng email
  password  String                    // Chuỗi ĐÃ HASH bằng bcrypt — tuyệt đối không lưu plain text
  name      String?
  createdAt DateTime @default(now())
  orders    Order[]                   // Một User có nhiều Order (quan hệ 1-n)
}

model Product {
  id        String   @id              // Giữ nguyên id dạng "backend_prod_0" (Bước 7c) khi seed, KHÔNG auto uuid
  name      String
  price     Int                       // Lưu tiền VND bằng số nguyên, KHÔNG dùng Float (tránh sai số dấu phẩy động)
  image     String
  createdAt DateTime @default(now())
}

model Order {
  id        String      @id           // Giữ định dạng "ORD-<timestamp>" quen thuộc (Sprint tự sinh, xem Bước 7f)
  userId    String
  user      User        @relation(fields: [userId], references: [id])
  total     Int                       // Luôn là con số SERVER tự tính (Phần 9.12), không phải Client gửi
  status    String      @default("PENDING")
  createdAt DateTime    @default(now())
  items     OrderItem[]               // Một Order có nhiều OrderItem (quan hệ 1-n)
}

model OrderItem {
  id        String  @id @default(uuid())
  orderId   String
  order     Order   @relation(fields: [orderId], references: [id])
  productId String                    // Cố ý KHÔNG đặt quan hệ cứng (@relation) tới Product — xem ghi chú bên dưới
  quantity  Int
  price     Int                       // Giá SNAPSHOT tại thời điểm đặt hàng, không tra lại giá Product hiện tại
}
```

> [!NOTE]
> **Vì sao `OrderItem.productId` không có `@relation` tới `Product`?** Ở Sprint 9 bắt buộc, catalog `Product` vẫn được phục vụ bởi `ProductService` in-memory (Bước 7c) để không phải viết lại toàn bộ phần đã học — chỉ `User` và `Order`/`OrderItem` bắt buộc chạy qua Prisma. Việc để `productId` là một trường string thường (không ràng buộc khoá ngoại) phản ánh đúng một pattern có thật ở Production: đơn hàng cũ lưu lại `price` snapshot tại thời điểm mua, kể cả khi Product gốc bị xoá/đổi giá sau này, đơn hàng cũ **vẫn đọc được** dữ liệu đúng lúc mua. Nếu làm phần tuỳ chọn "seed Product vào Prisma" (Bước 7d.6), bạn hoàn toàn có thể nâng cấp thêm `@relation` thật giữa hai bảng.

### 5. Repository Pattern — cây cầu để đổi sang Database mà không đau

Đây là kỹ thuật kiến trúc quan trọng nhất của Phần này, và Sprint 9 sẽ **áp dụng thật** kỹ thuật này chứ không chỉ minh hoạ. Ý tưởng: **Service không được biết dữ liệu đến từ đâu.** Nó chỉ nói chuyện với một "Kho" (Repository) qua một bản hợp đồng (Interface) cố định.

```typescript
// Bản hợp đồng — mô tả "Kho đơn hàng phải làm được những việc gì"
export interface IOrderRepository {
  save(order: CreateOrderInput): Promise<OrderRecord>;
  findAll(): Promise<OrderRecord[]>;
  findByUserId(userId: string): Promise<OrderRecord[]>;
  findById(orderId: string): Promise<OrderRecord | null>;
  updateStatus(orderId: string, status: string): Promise<OrderRecord>;
}
```

Ở phiên bản đầu (nếu bạn từng học/thử qua), người ta hay cắm vào một `InMemoryOrderRepository` (mảng trong RAM) để chạy nhanh cho có. Sprint 9 đi thẳng tới bản thật: viết `PrismaOrderRepository` **implement đúng Interface đó**, rồi khai báo đúng **một dòng** trong `providers` của Module:

```typescript
providers: [
  OrderService,
  { provide: 'IOrderRepository', useClass: PrismaOrderRepository }, // Đổi mỗi dòng này để chuyển nguồn dữ liệu
]
```

`OrderService` và `OrderController` **không phải sửa một ký tự nào** cho việc đổi từ RAM sang Database thật. Đây chính là sức mạnh thật sự của Dependency Injection đã học ở Phần 9.2 — không phải trò chơi cú pháp, mà là khả năng thay thế cả tầng hạ tầng mà không đụng vào logic nghiệp vụ. Code đầy đủ của `PrismaOrderRepository` nằm ở Bước 7d.4 của Sprint.

> [!TIP]
> Restart Server (`Ctrl+C` rồi `npm run start:dev` lại) và gọi `GET /api/orders` — đơn hàng cũ **vẫn còn nguyên**, vì giờ dữ liệu nằm trong file `prisma/dev.db` trên ổ cứng, không còn trong RAM tự xoá theo vòng đời tiến trình Node.js.

---

## 📖 PHẦN 9.9: SWAGGER / OPENAPI — TÀI LIỆU API TỰ VIẾT CHÍNH NÓ

Câu hỏi kinh điển trong mọi công ty: *"Anh Backend ơi, API đặt hàng nhận những field gì vậy?"* — và câu trả lời thường là một file Word cập nhật từ 3 tháng trước, đã sai bét.

**OpenAPI** (trước đây tên là Swagger) là một chuẩn quốc tế để mô tả REST API bằng JSON/YAML. **Swagger UI** là trang web tự động dựng từ mô tả đó, cho phép **bấm nút "Try it out" gọi thử API ngay trên trình duyệt** — không cần Postman.

Điểm tuyệt vời khi dùng với NestJS: bạn **đã viết DTO ở Phần 9.5 rồi**, Swagger tự đọc luôn DTO đó để sinh tài liệu. Tài liệu và code không bao giờ lệch nhau, vì chúng là **cùng một nguồn**.

```typescript
// main.ts
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger';

const config = new DocumentBuilder()
  .setTitle('ShopAI API')
  .setDescription('API phục vụ App React Native ShopAI')
  .setVersion('1.0')
  .addBearerAuth() // Hiện ô nhập JWT Token khi sau này có Guard (Phần 9.7)
  .build();

SwaggerModule.setup('api/docs', app, SwaggerModule.createDocument(app, config));
```

Mở `http://localhost:3000/api/docs` là thấy toàn bộ danh sách endpoint, kèm mẫu Request/Response.

Một vài Decorator hay dùng để tài liệu đẹp hơn:

| Decorator | Gắn ở đâu | Tác dụng |
|---|---|---|
| `@ApiTags('Products')` | Trên Class Controller | Gom nhóm các endpoint cùng chủ đề |
| `@ApiOperation({ summary: '...' })` | Trên hàm | Mô tả ngắn endpoint này làm gì |
| `@ApiProperty({ example: 199000 })` | Trên thuộc tính DTO | Sinh dữ liệu mẫu cho khung "Try it out" |
| `@ApiResponse({ status: 404 })` | Trên hàm | Liệt kê các trường hợp lỗi có thể xảy ra |

> [!TIP]
> Swagger UI thay thế được Postman trong 90% trường hợp test tay ở giai đoạn phát triển. Đây cũng là nơi bạn kiểm chứng cực nhanh xem `ValidationPipe` (Phần 9.5) có đang chặn đúng dữ liệu bẩn hay không — điền `price: -100` rồi bấm Execute là thấy ngay `400`.

---

## 🛡️ PHẦN 9.10: HELMET VÀ RATE LIMITING — HAI LỚP GIÁP TỐI THIỂU

Một Server vừa mở ra Internet công cộng sẽ bị bot quét trong vòng vài phút. Có hai thứ **bắt buộc** phải bật trước khi deploy.

### 1. Helmet — chỉnh lại các HTTP Header cho an toàn

`helmet` là một Middleware đặt hàng loạt Header bảo mật mà mặc định Express không có:

```bash
npm install helmet
```
```typescript
import helmet from 'helmet';
app.use(helmet()); // Đặt ngay dòng đầu trong bootstrap(), trước mọi thứ khác
```

| Header Helmet đặt | Chặn được điều gì |
|---|---|
| `X-Content-Type-Options: nosniff` | Trình duyệt tự đoán sai kiểu file và thực thi nhầm script |
| `X-Frame-Options: DENY` | Clickjacking — nhúng trang của bạn vào iframe web lừa đảo |
| `Strict-Transport-Security` | Ép mọi kết nối phải qua HTTPS |
| Ẩn `X-Powered-By: Express` | Không khoe cho hacker biết bạn dùng công nghệ gì |

### 2. Rate Limiting — chống spam và chống "cháy ví"

Nếu không giới hạn, một script đơn giản có thể gọi `POST /api/ai/chat` **10.000 lần/phút**. Vì endpoint này gọi sang Gemini và **bạn là người trả tiền**, hóa đơn cuối tháng sẽ là một cú sốc thật sự. Đây là rủi ro trực tiếp với chính "Vệ sĩ AI" bạn sắp dựng ở Bước 6.

```bash
npm install @nestjs/throttler
```
```typescript
// app.module.ts
import { ThrottlerModule, ThrottlerGuard } from '@nestjs/throttler';
import { APP_GUARD } from '@nestjs/core';

@Module({
  imports: [
    ThrottlerModule.forRoot([{ ttl: 60000, limit: 30 }]), // Tối đa 30 request / 60 giây / mỗi IP
  ],
  providers: [{ provide: APP_GUARD, useClass: ThrottlerGuard }], // Áp dụng cho TOÀN BỘ endpoint
})
export class AppModule {}
```

Vượt ngưỡng, Client nhận `429 Too Many Requests`. Với endpoint AI đắt tiền, có thể siết riêng chặt hơn bằng `@Throttle({ default: { limit: 5, ttl: 60000 } })` gắn thẳng lên Controller đó.

> [!WARNING]
> Đây là bài học nối tiếp trực tiếp Chương 8: ta đã giấu được API Key khỏi Client, nhưng nếu endpoint proxy mở toang không giới hạn thì kẻ xấu vẫn "xài ké" được hạn mức Gemini của bạn — chỉ là qua Server của bạn thay vì dùng Key trực tiếp. **Giấu Key mà không Rate Limit là mới khóa được một nửa cánh cửa.**

---

## 📁 PHẦN 9.11: CẤU TRÚC THƯ MỤC BACKEND CHUẨN

Khi dự án lớn lên 50 module, cách sắp xếp thư mục quyết định bạn có tìm nổi file hay không. NestJS khuyến nghị chia theo **tính năng (feature)**, không chia theo **loại file**.

```
shopai-backend/
├── src/
│   ├── main.ts                     # Điểm khởi động: Pipe, CORS, Swagger, Helmet, listen
│   ├── app.module.ts               # Module gốc, gom tất cả module con
│   │
│   ├── common/                     # Dùng chung cho MỌI module — không thuộc về nghiệp vụ nào
│   │   ├── filters/                #   Exception Filter (Phần 9.6)
│   │   ├── guards/                 #   Guard xác thực (Phần 9.7)
│   │   ├── interceptors/           #   Logging, biến đổi response
│   │   └── dto/                    #   DTO dùng chung (VD PaginationDto)
│   │
│   ├── config/                     # Đọc & kiểm tra biến môi trường
│   │
│   ├── product/                    # ── Một feature = một thư mục khép kín ──
│   │   ├── dto/
│   │   │   └── create-product.dto.ts
│   │   ├── entities/
│   │   │   └── product.entity.ts
│   │   ├── product.controller.ts   #   Tầng HTTP (Phần 9.2)
│   │   ├── product.service.ts      #   Tầng nghiệp vụ
│   │   ├── product.repository.ts   #   Tầng dữ liệu (Phần 9.8)
│   │   └── product.module.ts       #   Gói tất cả lại
│   │
│   ├── order/                      # Cùng cấu trúc y hệt product/
│   ├── ai/                         # Proxy Gemini
│   └── health.controller.ts
│
├── .env                            # Bí mật thật — KHÔNG BAO GIỜ commit
├── .env.example                    # Bản mẫu rỗng — commit lên Git cho đồng đội
└── package.json
```

**Ba nguyên tắc vàng:**
1. **Một feature = một thư mục khép kín.** Muốn xóa tính năng "Order"? Xóa thư mục `order/` và một dòng import — xong.
2. **`common/` chỉ chứa thứ thật sự dùng chung.** Nếu chỉ Product dùng, để trong `product/`.
3. **Controller phải mỏng, Service phải dày.** Controller chỉ nhận và trả; mọi tính toán nằm ở Service. Controller dài quá 15 dòng cho một endpoint là dấu hiệu logic đang đặt sai chỗ.

---

## 🛒 PHẦN 9.12: THIẾT KẾ ORDERS API — NỐI LẠI VỚI CHECKOUTSCREEN CHƯƠNG 6

Nhớ lại Chương 6, trong `CheckoutScreen.tsx` ta đã để lại một lời hứa ngay trong comment:

```tsx
// Giả lập gọi API đặt hàng — Chương 9 sẽ thay bằng POST /orders thật lên NestJS
setTimeout(() => { ... }, 1500);
```

Đã đến lúc thực hiện lời hứa đó. `setTimeout` giả lập chỉ dạy được cách hiển thị Loading; nó không dạy được điều gì xảy ra khi **mạng chập chờn, Server từ chối, hoặc đơn hàng bị trùng**.

### 1. Hợp đồng dữ liệu giữa hai đầu

**Request Mobile gửi lên** — chỉ gửi thứ Server không thể tự biết:
```json
{
  "items": [
    { "productId": "backend_prod_1", "quantity": 2 },
    { "productId": "backend_prod_5", "quantity": 1 }
  ],
  "total": 3050000
}
```

**Response Server trả về:**
```json
{ "orderId": "ORD-1735689600000", "status": "PENDING", "total": 3050000, "createdAt": "2025-..." }
```

### 2. Vì sao Server phải TỰ TÍNH LẠI tổng tiền?

Ta có gửi `total` lên, nhưng đó chỉ để **đối chiếu**, tuyệt đối không dùng để ghi vào đơn hàng. Lý do đúng bằng nguyên tắc ở Phần 9.5: Client hoàn toàn có thể bị giả mạo. Một người dùng chỉnh gói tin, gửi `{ items: [iPhone 30 triệu], total: 1000 }` — nếu Server tin, bạn vừa bán iPhone giá một nghìn đồng.

Quy trình đúng ở Server: đọc danh sách `productId` → tra giá **thật** trong kho dữ liệu → nhân với `quantity` → cộng ra tổng của riêng mình. Nếu lệch với `total` Client gửi, ném `BadRequestException` (dấu hiệu client cũ hoặc bị can thiệp).

### 3. Trạng thái đơn hàng (Order Status)

Đơn hàng thật không chỉ có "thành công". Nó đi qua một vòng đời:

```
PENDING (chờ xử lý) → CONFIRMED (đã xác nhận) → SHIPPING (đang giao) → DELIVERED (đã giao)
                    ↘ CANCELLED (đã hủy)
```

ShopAI trong khóa học dừng ở `PENDING` — đủ để minh họa việc Server sinh và lưu trạng thái, phần chuyển trạng thái là bài toán của hệ thống quản trị đơn hàng, ngoài phạm vi môn học.

### 4. Tính bất biến khi mạng chập chờn (Idempotency — khái niệm)

Người dùng bấm "Xác nhận đặt hàng", mạng lag, họ sốt ruột bấm thêm 2 lần nữa → **3 đơn hàng giống hệt nhau**. Cách xử lý chuyên nghiệp: Mobile sinh một `Idempotency-Key` (UUID) gắn vào Header; Server thấy Key đã xử lý rồi thì trả lại đúng kết quả cũ thay vì tạo đơn mới.

Sprint 9 dùng cách đơn giản hơn nhưng bắt buộc phải có: **khóa nút bấm bằng cờ `isPlacing`** — đúng như `CheckoutScreen` đã làm ở Chương 6 (`isPlacing ? <ActivityIndicator/> : <ShopButton/>`). Đây cũng là lý do đoạn code đó được thiết kế như vậy ngay từ đầu.

---

## 💳 PHẦN 9.13: THANH TOÁN (PAYMENT GATEWAY), REAL-TIME (SOCKET.IO) & CACHE (REDIS)

Để ShopAI vươn tầm thành một dự án Enterprise (chuẩn Shopee), Backend cần xử lý được bộ 3 bài toán: Tiền bạc, Thời gian thực và Chịu tải.

### 1. Cổng Thanh Toán (Payment Gateway - VNPay/Stripe)
- **Quy trình:**
  1. Frontend (Mobile) gửi Request thanh toán lên Backend kèm mã đơn hàng (Ví dụ `orderId`).
  2. Backend dùng SDK (như `stripe-node` hoặc thuật toán Hash của VNPay) để tạo URL Thanh Toán an toàn.
  3. Frontend mở URL này trên WebView hoặc Browser nội bộ.
  4. Sau khi thanh toán xong, Cổng thanh toán gọi một API **Webhook** (POST `/api/payment/webhook`) báo cho Backend biết trạng thái.
  5. Backend cập nhật Order Status từ `PENDING` thành `PAID`.
- **Nguyên tắc:** Frontend tuyệt đối không giao tiếp trực tiếp với cổng thanh toán để xác nhận trạng thái. Mọi thay đổi trạng thái đơn hàng đều do Backend làm thông qua Webhook ký điện tử.

### 2. Thông Báo Thời Gian Thực (Socket.IO)
- Ngay khi Webhook báo đơn hàng đã `PAID`, làm sao Mobile biết để nhảy thông báo "Thanh toán thành công"?
- Dùng **WebSockets** (qua Socket.IO). Backend và Frontend giữ một kết nối 2 chiều liên tục.
- Backend emit sự kiện: `socket.emit('order_status_changed', { orderId, status: 'PAID' })`. Frontend lắng nghe và tự động chuyển màn hình.

### 3. Tăng Tốc Độ & Chịu Tải (Redis Cache & Rate Limit)
- Các API như lấy danh sách sản phẩm trang chủ (`/api/products`) bị gọi liên tục khi hàng vạn User vào App. Việc query DB (PostgreSQL/Prisma) quá nhiều sẽ làm nghẽn Server.
- **Giải pháp:** Cài **Redis** (In-memory Database). Khi gọi API lần 1, lưu JSON danh sách sản phẩm vào Redis với thời gian hết hạn (TTL) 5 phút. Lần gọi thứ 2, Backend lấy trực tiếp từ Redis trong < 10ms.
- **Rate Limit:** Cũng dùng Redis để đếm số lần gọi API của mỗi IP. Nếu gọi > 100 lần/phút, chặn ngay với mã lỗi `429 Too Many Requests`.

---

## 🚀 THỰC CHIẾN SHOPAI (SPRINT 9: TÍCH HỢP NESTJS API + JWT AUTH + PRISMA + VỆ SĨ AI GEMINI)

**User Story:** *"Là một Kỹ sư Fullstack, tôi muốn tự dựng một API Server bằng NestJS trả về danh sách sản phẩm, có xác thực đăng nhập bằng JWT thật, lưu đơn hàng vào Database thật qua Prisma để restart Server không mất dữ liệu, và có thêm một endpoint bảo mật để Server thay Mobile gọi Gemini AI — chấm dứt việc lộ API Key ra ngoài Client như ở Chương 8. Sau đó sửa lại App Mobile để đăng nhập lấy Token thật, đặt hàng có đính kèm Token, fetch sản phẩm và gọi Chatbot AI đều thông qua Server này."*


### 📋 Khung thực hành chương (đọc trước khi gõ code)

> Đây là **bài thực hành của Chương 9** (không phải “lab mỗi ngày”). Làm hết Sprint này = đạt mục tiêu chương. Hoàn thành đủ 11 Sprint = sản phẩm ShopAI theo `SHOPAI_HOAN_THIEN.md`.

| Hạng mục | Nội dung |
|----------|----------|
| **Thời lượng gợi ý** | 8–12 tiết (một chương fullstack — xếp nhiều buổi) |
| **Độ khó chương** | ★★★★★ |
| **Đầu vào bắt buộc** | Sprint 6+8 PASS — có axiosClient, SecureStore, AIChat UX. |
| **Đầu ra sản phẩm** | NestJS + JWT (login+register) + Prisma; Orders list/detail/pay; Mobile nối Register/Orders/Pay; không lộ Gemini Key. |
| **Cách làm** | Làm **tuần tự từng Bước**. Gặp mốc ✓ bên dưới mà FAIL → dừng, sửa, rồi mới sang bước sau. |
| **Nghiệm thu cuối khóa** | Đối chiếu `SHOPAI_HOAN_THIEN.md` — mỗi Sprint chỉ tích thêm ô, không phá tính năng cũ. |

### ✓ Kiểm chứng theo mốc (trong lúc làm)

- **Sau Bước 7d–7f:** curl login/register → JWT; orders 401/201 PENDING; pay → PAID; restart server đơn còn.
- **Sau Bước 8–9f:** Mobile Register/Login/Checkout/Orders/Pay qua Nest; AI qua Nest + giữ UX Ch8.

> [!TIP]
> Xong Sprint 9, mở `SHOPAI_HOAN_THIEN.md` và tick các ô thuộc chương này. Mục tiêu cuối khóa: **mọi ô A/B/C/D (+ E đề cương) đều xanh** trong `SHOPAI_HOAN_THIEN.md` — đó mới là ShopAI hoàn thiện đẳng cấp.

### Yêu cầu Nghiệm thu:
1. Server NestJS trả về danh sách sản phẩm qua `GET /api/products`.
2. Server NestJS có thêm endpoint `POST /api/ai/chat`: nhận `{ message }`, gọi Gemini bằng Key giấu trong `.env` ở Backend, trả về `{ reply }`.
3. `HomeScreen` trên Mobile fetch sản phẩm thật từ Server (không còn Mock Data).
4. `AIChatScreen` trên Mobile gọi thẳng vào `/api/ai/chat` của Server NestJS — **xóa bỏ hoàn toàn** SDK `@google/generative-ai` và file `geminiConfig.ts` phía Client. Mobile từ giờ không hề biết Gemini API Key là gì.
5. Bật **`ValidationPipe` toàn cục** (Phần 9.5) và có ít nhất 1 file DTO (`CreateProductDto`) minh họa `class-validator`.
6. Có endpoint `GET /api/products/:id` ném đúng **`NotFoundException` (404)** khi id không tồn tại (Phần 9.6); `ProductDetailScreen` trên Mobile fetch dữ liệu thật từ endpoint này.
7. Đã cài **Prisma + chạy migrate thành công** (Phần 9.8), dữ liệu `Order` lưu vào **SQLite** — restart Server (`Ctrl+C` rồi chạy lại) **không còn mất đơn hàng**.
8. Có endpoint `POST /api/auth/login` và **`POST /api/auth/register`**, trả về `{ accessToken }` là **JWT thật** được ký bằng `JWT_SECRET` (Phần 9.7).
9. Endpoint Orders được bảo vệ bằng `JwtAuthGuard`: `POST` tạo đơn **`PENDING`**, `GET` lịch sử + chi tiết theo user, `POST /:id/pay` → **`PAID`**. Server **tự tính lại tổng tiền** (Phần 9.12).
10. `LoginScreen` / `RegisterScreen` gọi API Auth thật; `OrdersScreen` / `OrderDetailScreen` (Ch.6) nối Nest thay store local.
11. `CheckoutScreen` gọi đặt hàng thật qua `axiosClient`, đặt hàng thành công mới xóa giỏ hàng; invalidate cache `orders`.
12. Có **Swagger UI** tại `/api/docs` và file **`.env.example`** được commit — **không commit** `.env` lẫn `prisma/dev.db`.
13. *(Tuỳ chọn)* Có script seed ít nhất 1 User demo và/hoặc Product vào Database qua Prisma (Phần 9.8 mục seed).

### 🗺️ Bản đồ Sprint 9 — các bước chính + bước tùy chọn

| Nhóm | Bước | Nội dung |
|---|---|---|
| **Dựng khung Backend** | 1 → 5 | Khởi tạo NestJS, sinh Product Module, viết Service/Controller, soát Module |
| **Bảo mật AI** | 6 | Module AI proxy Gemini, giấu Key trong `.env` |
| **Cấu hình Server** | 7, 7b | CORS + `0.0.0.0` + `ValidationPipe` + DTO |
| **Database thật** | 7c, 7d | `GET /products/:id`, cài Prisma + `schema.prisma` + migrate + seed |
| **Auth + Orders bảo mật** | 7e, 7f | `AuthModule` (JWT login), Orders API dùng Prisma + `JwtAuthGuard` |
| **Tài liệu & cấu hình** | 7g, 7h | Swagger (đủ Bearer Auth), `.env.example` |
| **Nối Mobile** | 8 → 9d | Fetch products, chat AI, product detail, đăng nhập thật, đặt hàng có Bearer Token |
| **Kiểm chứng** | 10 | Chạy toàn hệ thống 2 chiều, kiểm tra cả đường JWT + Prisma |
| **Tùy chọn** | 11, 12 | Health check + chấm "Server Online" |

### Hướng dẫn thực thi Step-by-Step:

#### Bước 1: Khởi tạo Backend NestJS
Bạn mở một cửa sổ Terminal mới hoàn toàn (Không nằm trong thư mục React Native). Chạy lệnh cài công cụ Nest:
```bash
npm i -g @nestjs/cli
nest new shopai-backend
```
*(Chọn npm làm package manager, quá trình tải sẽ mất 1 phút).*

#### Bước 2: Tạo Product Module
Di chuyển vào thư mục backend vừa tạo, dùng CLI để sinh code tự động (Cực nhàn!):
```bash
cd shopai-backend
nest g module product
nest g controller product
nest g service product
```
Lúc này trong thư mục `src/product` đã có đầy đủ 3 file kiến trúc.

#### Bước 3: Viết Logic tại Product Service (Đầu bếp)
Mở file `src/product/product.service.ts`:
```typescript
import { Injectable } from '@nestjs/common';

// @Injectable() biến Class này thành một Service có thể Tiêm (Inject) được.
@Injectable()
export class ProductService {
  
  // Hàm xử lý nghiệp vụ trả về danh sách sản phẩm
  getAllProducts() {
    // Tạo 20 sản phẩm ảo (Sau này ta sẽ kết nối MySQL/MongoDB ở đây)
    return Array.from({ length: 20 }).map((_, i) => ({
      id: `backend_prod_${i}`,
      name: `Sản phẩm từ NestJS Server ${i}`,
      price: 1000000 + (i * 10000),
      image: `https://picsum.photos/id/${200 + i}/400/400`
    }));
  }
}
```

#### Bước 4: Viết API Endpoint tại Product Controller (Tiếp tân)
Mở file `src/product/product.controller.ts`:
```typescript
import { Controller, Get } from '@nestjs/common';
import { ProductService } from './product.service';

@Controller('api/products') // Khai báo đường dẫn URL
export class ProductController {
  
  // Áp dụng Dependency Injection: Tiêm cái Service vào đây!
  constructor(private readonly productService: ProductService) {}

  @Get() // Khi Mobile gọi Method GET vào URL trên
  getProducts() {
    // Nhờ Đầu bếp làm món ăn và bưng ra cho Mobile
    return this.productService.getAllProducts();
  }
}
```

#### Bước 5: Kiểm tra khai báo Product Module (đăng ký Controller & Service vào "Hộp chứa")
Khi bạn dùng lệnh `nest g module/controller/service`, Nest CLI **tự động** khai báo hộ 3 file này vào nhau. Nhưng một Kỹ sư giỏi phải hiểu rõ chuyện gì đang xảy ra bên dưới — mở `src/product/product.module.ts` để kiểm chứng:

```typescript
import { Module } from '@nestjs/common';
import { ProductController } from './product.controller';
import { ProductService } from './product.service';

@Module({
  controllers: [ProductController], // Đăng ký "người tiếp tân" của Module này
  providers: [ProductService],      // Đăng ký Service vào IoC Container để có thể Inject được
})
export class ProductModule {}
```
> Nếu thiếu dòng `providers: [ProductService]`, NestJS sẽ báo lỗi ngay lúc khởi động: `Nest can't resolve dependencies of the ProductController`. Đây là lỗi DI kinh điển nhất khi mới học Nest — nhớ mặt nó!

#### Bước 6: Dựng "Vệ sĩ AI" — Module bảo mật Gemini trên Backend

Đây là bước quan trọng nhất của cả Sprint: khép lại lỗ hổng bảo mật để lộ Key ở Chương 8. Từ giờ, chỉ **Server** được biết Gemini API Key — Mobile chỉ nói chuyện với Server của chính bạn.

**6.1. Cài thêm 2 thư viện:** `@nestjs/config` (đọc file `.env`) và `@google/generative-ai` (gọi Gemini):
```bash
npm install @nestjs/config @google/generative-ai
```

**6.2. Tạo file `.env`** tại thư mục gốc `shopai-backend` (cùng cấp `package.json`):
```
GEMINI_API_KEY=ĐIỀN_API_KEY_THẬT_CỦA_BẠN_VÀO_ĐÂY
```
> ⚠️ Mở file `.gitignore` của backend, thêm dòng `.env` vào (nếu chưa có sẵn) để không bao giờ đẩy Key thật lên Git/GitHub công khai.

**6.3. Bật `ConfigModule`** để toàn bộ App đọc được biến môi trường trong `.env`. Mở `src/app.module.ts`:
```typescript
import { Module } from '@nestjs/common';
import { ConfigModule } from '@nestjs/config';
import { ProductModule } from './product/product.module';
import { AiModule } from './ai/ai.module';

@Module({
  imports: [
    ConfigModule.forRoot({ isGlobal: true }), // isGlobal: dùng ConfigService ở BẤT KỲ Module nào, không cần import lại
    ProductModule,
    AiModule,
  ],
})
export class AppModule {}
```

**6.4. Sinh code Module AI** bằng CLI (giống cách bạn đã làm với Product ở Bước 2):
```bash
nest g module ai
nest g controller ai
nest g service ai
```

**6.5. Viết Đầu bếp AI** — mở `src/ai/ai.service.ts`, đây là nơi DUY NHẤT trong toàn hệ thống được cầm Gemini API Key. **Giữ ngữ cảnh hội thoại** như Chương 8 (`startChat` + `history`), không rút về `generateContent` một câu rời:

```typescript
import { Injectable } from '@nestjs/common';
import { ConfigService } from '@nestjs/config';
import { GoogleGenerativeAI, Content } from '@google/generative-ai';

export type ChatHistoryItem = { role: 'user' | 'model'; text: string };

@Injectable()
export class AiService {
  private readonly genAI: GoogleGenerativeAI;

  constructor(private readonly configService: ConfigService) {
    const apiKey = this.configService.get<string>('GEMINI_API_KEY');
    this.genAI = new GoogleGenerativeAI(apiKey as string);
  }

  async chat(message: string, history: ChatHistoryItem[] = []): Promise<string> {
    const model = this.genAI.getGenerativeModel({
      model: 'gemini-1.5-flash',
      systemInstruction:
        'Bạn là nhân viên bán hàng của ShopAI. Chỉ tư vấn về đồ công nghệ. Trả lời cực ngắn dưới 30 chữ. Không nói chuyện chính trị.',
    });

    // Đổi { role, text } từ Mobile thành định dạng Gemini Content[]
    const geminiHistory: Content[] = history.slice(-10).map((h) => ({
      role: h.role,
      parts: [{ text: h.text }],
    }));

    const chat = model.startChat({ history: geminiHistory });
    const result = await chat.sendMessage(message);
    const response = await result.response;
    return response.text();
  }
}
```

**6.6. Viết Tiếp tân AI** — mở `src/ai/ai.controller.ts` (nhận thêm `history` tùy chọn):
```typescript
import { Body, Controller, Post } from '@nestjs/common';
import { AiService, ChatHistoryItem } from './ai.service';

@Controller('api/ai')
export class AiController {
  constructor(private readonly aiService: AiService) {}

  @Post('chat')
  async chat(
    @Body() body: { message: string; history?: ChatHistoryItem[] },
  ) {
    const reply = await this.aiService.chat(body.message, body.history ?? []);
    return { reply };
  }
}
```

**6.7. Kiểm tra `ai.module.ts`** (CLI tự sinh, chỉ cần soát lại cho chắc):
```typescript
import { Module } from '@nestjs/common';
import { AiController } from './ai.controller';
import { AiService } from './ai.service';

@Module({
  controllers: [AiController],
  providers: [AiService],
})
export class AiModule {}
```

#### Bước 7: Bật CORS (để test bằng Web/Postman), lắng nghe mọi card mạng (0.0.0.0) và Khởi chạy Server

> [!IMPORTANT]
> **Đính chính quan trọng: CORS chỉ tồn tại trên Trình duyệt (Browser), KHÔNG áp dụng cho Mobile App.** CORS (Cross-Origin Resource Sharing) là một cơ chế bảo mật do chính **Trình duyệt** (Chrome, Safari...) tự đặt ra dựa vào Header `Origin` mà chỉ trình duyệt mới tự động gắn. Hàm `fetch`/`axios` chạy trong React Native (JSI/Native Module) **không hề bị CORS chặn** — vì đó không phải là trình duyệt, không có khái niệm "cùng domain hay khác domain". Nói cách khác: dù bạn **không** gọi `app.enableCors()`, App di động của bạn ở Bước 8 vẫn gọi Server bình thường, không hề bị lỗi CORS.
>
> Vậy tại sao ta vẫn bật `enableCors()`? Vì hai lý do thực tế sau, không liên quan gì đến Mobile:
> 1. **Tiện test API bằng công cụ chạy trên trình duyệt:** Postman (bản Web/Chrome Extension), hoặc bạn tự mở `http://<ip>:3000/api/products` ngay trên Chrome để xem JSON — những công cụ này CHẠY TRONG trình duyệt nên vẫn bị CORS chi phối.
> 2. **Chuẩn bị cho tương lai có Admin Web:** Nếu công ty làm thêm một trang quản trị (Admin Dashboard) bằng ReactJS/NextJS chạy trên domain khác để gọi vào cùng Server NestJS này, trang Web đó (chạy trong trình duyệt) sẽ CẦN CORS được bật thì mới gọi API thành công.
>
> Tóm lại: `enableCors()` là một thói quen tốt (không hại gì khi bật, có thể siết chặt domain cụ thể sau), nhưng đừng hiểu sai rằng nó là "lá chắn bắt buộc" giúp App Mobile gọi được Server — Mobile chưa bao giờ bị CORS cản đường cả.

Đồng thời, để **điện thoại thật** trong cùng Wifi truy cập được, Server phải lắng nghe ở địa chỉ `0.0.0.0` (tất cả card mạng) chứ không chỉ `127.0.0.1` (chính máy tính) — đây mới là cấu hình **thực sự bắt buộc** cho Mobile, khác hẳn với CORS. Mở `src/main.ts`:
```typescript
import { NestFactory } from '@nestjs/core';
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.enableCors(); // Bật để test qua Postman Web/Chrome hoặc phòng khi có Admin Web sau này — KHÔNG phải để "mở khóa" cho Mobile.

  // "0.0.0.0" = lắng nghe TẤT CẢ card mạng (Wifi, LAN...) của máy tính.
  // Nếu chỉ ghi app.listen(3000) mặc định là 127.0.0.1 -> Điện thoại thật
  // trong cùng Wifi sẽ KHÔNG BAO GIỜ kết nối được, dù IP có đúng! (Đây mới là bẫy thật của Mobile — xem lại Phần 9.4)
  await app.listen(3000, '0.0.0.0');
}
bootstrap();
```
Chạy Server:
```bash
npm run start:dev
```
*Server đang chạy! Bạn có thể lấy IP LAN của máy tính (VD: `192.168.1.15`) và mở trình duyệt web: `http://192.168.1.15:3000/api/products` để thấy cục JSON API khổng lồ hiện ra.*

#### Bước 7b: Bật `ValidationPipe` toàn cục và viết DTO đầu tiên

Áp dụng đúng lý thuyết Phần 9.5. Cài 2 thư viện song sinh:
```bash
npm install class-validator class-transformer
```

Tạo file `src/product/dto/create-product.dto.ts`:
```typescript
import { IsNotEmpty, IsNumber, IsString, IsUrl, MaxLength, Min } from 'class-validator';

export class CreateProductDto {
  @IsString()
  @IsNotEmpty({ message: 'Tên sản phẩm không được để trống' })
  @MaxLength(200, { message: 'Tên sản phẩm tối đa 200 ký tự' })
  name: string;

  @IsNumber({}, { message: 'Giá phải là một con số' })
  @Min(0, { message: 'Giá sản phẩm không được âm' })
  price: number;

  @IsUrl({}, { message: 'Ảnh sản phẩm phải là một URL hợp lệ' })
  image: string;
}
```

Nâng cấp `src/main.ts` — **chỉ thêm** `useGlobalPipes`, giữ nguyên `enableCors()` và `listen(3000, '0.0.0.0')` đã viết ở Bước 7:
```typescript
import { NestFactory } from '@nestjs/core';
import { ValidationPipe } from '@nestjs/common'; // ➕ MỚI
import { AppModule } from './app.module';

async function bootstrap() {
  const app = await NestFactory.create(AppModule);
  app.enableCors();

  // ➕ MỚI: Trạm kiểm soát dữ liệu vào — áp dụng cho TOÀN BỘ endpoint, không cần khai báo lại từng chỗ
  app.useGlobalPipes(
    new ValidationPipe({
      whitelist: true,            // Client gửi thừa field lạ -> tự động cắt bỏ
      forbidNonWhitelisted: true, // Gửi field lạ thì báo lỗi 400 luôn cho minh bạch
      transform: true,            // Bật class-transformer: JSON -> instance DTO, tự ép kiểu
    }),
  );

  await app.listen(3000, '0.0.0.0');
}
bootstrap();
```

Để **thấy nó hoạt động thật**, thêm tạm một endpoint `POST` vào `src/product/product.controller.ts`:
```typescript
import { Body, Controller, Get, Post } from '@nestjs/common';
import { CreateProductDto } from './dto/create-product.dto';

  @Post() // POST /api/products — chỉ để minh họa ValidationPipe, ShopAI chưa dùng đến
  createProduct(@Body() dto: CreateProductDto) {
    // Đến được dòng này nghĩa là dữ liệu ĐÃ hợp lệ 100%.
    // Không cần một dòng if kiểm tra nào — ValidationPipe đã chặn hết ở ngoài cửa.
    return { message: 'Dữ liệu hợp lệ, đã nhận sản phẩm', data: dto };
  }
```

Test bằng `curl` (hoặc Swagger ở Bước 7e) với dữ liệu bẩn:
```bash
curl -X POST http://localhost:3000/api/products \
  -H "Content-Type: application/json" \
  -d '{"name":"","price":-100,"image":"khong-phai-url"}'
```
Kết quả trả về `400 Bad Request` với đủ 3 thông báo lỗi tiếng Việt bạn vừa viết — đây chính là "Zod của phía Backend".

#### Bước 7c: `GET /api/products/:id` — Route Param và `NotFoundException`

`ProductDetailScreen` (Chương 5/6) đang mượn cache của `HomeScreen`. Giờ ta cho nó một endpoint thật để fetch trực tiếp. Trước hết, tách dữ liệu ra một chỗ dùng chung trong `src/product/product.service.ts`:

```typescript
import { Injectable, NotFoundException } from '@nestjs/common';

@Injectable()
export class ProductService {
  // Kho dữ liệu tạm, sinh MỘT LẦN lúc Service được khởi tạo (thay vì sinh lại mỗi request
  // như bản Bước 3) — nhờ vậy id luôn ổn định, ProductDetail tra cứu mới ra kết quả.
  private readonly products = Array.from({ length: 20 }).map((_, i) => ({
    id: `backend_prod_${i}`,
    name: `Sản phẩm từ NestJS Server ${i}`,
    price: 1000000 + i * 10000,
    image: `https://picsum.photos/id/${200 + i}/400/400`,
  }));

  getAllProducts() {
    return this.products;
  }

  // ➕ MỚI
  getProductById(id: string) {
    const product = this.products.find((p) => p.id === id);
    if (!product) {
      // Đúng chuẩn Phần 9.6: KHÔNG return null, phải ném đúng mã 404
      throw new NotFoundException(`Không tìm thấy sản phẩm có id = ${id}`);
    }
    return product;
  }

  // Dùng lại ở Orders API (Bước 7f) để Server tự tra giá thật
  findRawById(id: string) {
    return this.products.find((p) => p.id === id) ?? null;
  }
}
```

Thêm endpoint vào `src/product/product.controller.ts`:
```typescript
import { Controller, Get, Param } from '@nestjs/common';

  @Get(':id') // GET /api/products/backend_prod_3
  getProductById(@Param('id') id: string) {
    // @Param trích đoạn ':id' trong URL ra thành biến — tương đương Route Params của
    // React Navigation ở Chương 5, chỉ khác là nó đi qua đường dây mạng.
    return this.productService.getProductById(id);
  }
```

> [!WARNING]
> **Thứ tự khai báo Route rất quan trọng.** `@Get(':id')` khớp với *mọi* chuỗi, nên nếu sau này bạn thêm `@Get('featured')` mà đặt **bên dưới** `@Get(':id')`, NestJS sẽ hiểu nhầm chữ `featured` là một `id` và không bao giờ chạy tới hàm kia. Quy tắc: **route tĩnh khai báo trước, route động (`:id`) khai báo sau cùng.**

Kiểm chứng nhanh:
```bash
curl http://localhost:3000/api/products/backend_prod_3   # -> 200, trả về đúng 1 sản phẩm
curl http://localhost:3000/api/products/khong_ton_tai    # -> 404 kèm message tiếng Việt
```

#### Bước 7d: Cài đặt Prisma ORM + Migrate Database (SQLite)

Đây là bước biến Phần 9.8 từ lý thuyết thành Database thật. Làm đúng thứ tự sau, đừng nhảy cóc.

**7d.1. Cài thư viện** (cài luôn `bcrypt` vì script seed User ở bước 7d.6 cần hash mật khẩu, và `AuthModule` ở Bước 7e cũng sẽ dùng lại):
```bash
npm install prisma --save-dev
npm install @prisma/client bcrypt
npm install -D @types/bcrypt ts-node
```

**7d.2. Khởi tạo Prisma:**
```bash
npx prisma init --datasource-provider sqlite
```
Lệnh này tự sinh `prisma/schema.prisma` (bản trống) và thêm dòng `DATABASE_URL` vào `.env`. Mở `.env`, sửa lại đúng dòng đó (SQLite lưu file ngay trong thư mục `prisma/`):
```
DATABASE_URL="file:./dev.db"
```

**7d.3. Dán đúng schema đã thiết kế ở Phần 9.8 mục 4** vào `prisma/schema.prisma` (đủ 4 model `User`, `Product`, `Order`, `OrderItem` — xem lại nội dung đầy đủ ở đó, không lặp lại ở đây để tránh copy sai bản cũ).

**7d.4. Chạy Migration** — lệnh này đọc `schema.prisma`, tự sinh file SQL, tạo Database SQLite thật, và sinh Prisma Client (bộ Type TypeScript khớp 100% với Schema):
```bash
npx prisma migrate dev --name init
```
Nếu chạy thành công, bạn sẽ thấy thư mục `prisma/migrations/` mới xuất hiện và file `prisma/dev.db` đã được tạo — đó chính là Database SQLite của bạn, xem được trực tiếp bằng lệnh `npx prisma studio` (mở giao diện Web xem/sửa dữ liệu như phpMyAdmin).

**7d.5. `PrismaService`** — lớp cầu nối để Nest quản lý vòng đời kết nối Database. Tạo `src/prisma/prisma.service.ts`:
```typescript
import { Injectable, OnModuleDestroy, OnModuleInit } from '@nestjs/common';
import { PrismaClient } from '@prisma/client';

@Injectable()
export class PrismaService extends PrismaClient implements OnModuleInit, OnModuleDestroy {
  async onModuleInit() {
    await this.$connect(); // Mở kết nối khi NestJS khởi động Module này
  }

  async onModuleDestroy() {
    await this.$disconnect(); // Đóng kết nối gọn gàng khi Server tắt
  }
}
```

Tạo `src/prisma/prisma.module.ts` — đánh dấu `@Global()` để **mọi** Module khác (Order, Auth...) dùng được `PrismaService` mà không cần `import` lại nhiều lần:
```typescript
import { Global, Module } from '@nestjs/common';
import { PrismaService } from './prisma.service';

@Global()
@Module({
  providers: [PrismaService],
  exports: [PrismaService],
})
export class PrismaModule {}
```

Đăng ký vào `src/app.module.ts` (chỉ **thêm**, giữ nguyên phần cũ):
```typescript
import { PrismaModule } from './prisma/prisma.module'; // ➕ MỚI

imports: [ConfigModule.forRoot({ isGlobal: true }), PrismaModule, ProductModule, AiModule],
```

**7d.6. Script seed — tạo sẵn 1 User demo để đăng nhập** (bắt buộc, để Bước 7e có tài khoản mà test). Tạo `prisma/seed.ts`:
```typescript
import { PrismaClient } from '@prisma/client';
import * as bcrypt from 'bcrypt';

const prisma = new PrismaClient();

async function main() {
  const hashedPassword = await bcrypt.hash('123456', 10); // 10 = độ phức tạp (salt rounds)

  await prisma.user.upsert({
    where: { email: 'demo@shopai.com' },
    update: {},
    create: {
      email: 'demo@shopai.com',
      password: hashedPassword, // Lưu bản ĐÃ HASH, không bao giờ lưu '123456' dạng thường
      name: 'Học viên Demo',
    },
  });

  console.log('✅ Đã seed User demo: demo@shopai.com / 123456');

  // ➕ TÙY CHỌN: seed luôn Product vào Database (Yêu cầu Nghiệm thu mục 13).
  // Ở Sprint 9 bắt buộc, Product vẫn phục vụ bằng in-memory (Bước 7c) nên đoạn dưới có thể bỏ qua.
  // const productCount = await prisma.product.count();
  // if (productCount === 0) {
  //   await prisma.product.createMany({
  //     data: Array.from({ length: 20 }).map((_, i) => ({
  //       id: `backend_prod_${i}`,
  //       name: `Sản phẩm từ NestJS Server ${i}`,
  //       price: 1000000 + i * 10000,
  //       image: `https://picsum.photos/id/${200 + i}/400/400`,
  //     })),
  //   });
  //   console.log('✅ Đã seed 20 Product vào Database');
  // }
}

main()
  .catch((e) => {
    console.error(e);
    process.exit(1);
  })
  .finally(() => prisma.$disconnect());
```

Khai báo lệnh seed trong `package.json` (thêm khối `prisma` ở cấp gốc, ngang hàng với `scripts`):
```json
"prisma": {
  "seed": "ts-node prisma/seed.ts"
}
```

Chạy seed:
```bash
npx prisma db seed
```

> [!TIP]
> Chạy `npx prisma studio` để mở một trang Web (mặc định `http://localhost:5555`) xem trực tiếp bảng `User` vừa seed — thấy rõ cột `password` là một chuỗi hash dài ngoằng bắt đầu bằng `$2b$...` (định dạng bcrypt), không phải `123456`. Đây là cách kiểm chứng trực quan nhất rằng mật khẩu không hề được lưu dạng thường.

#### Bước 7e: `AuthModule` thật — `POST /api/auth/login` trả JWT

Toàn bộ code chi tiết của bước này đã trình bày đầy đủ ở **Phần 9.7 mục 5** — bước này là lúc bạn gõ đúng các file đó vào dự án `shopai-backend`. Tạo đủ 6 file sau:

| File | Nội dung | Xem lại ở |
|---|---|---|
| `.env` | Thêm `JWT_SECRET`, `JWT_EXPIRES_IN` | Phần 9.7 mục 5.2 |
| `src/auth/dto/login.dto.ts` | `LoginDto` (`email`, `password` + `class-validator`) | Phần 9.7 mục 5.3 |
| `src/auth/dto/register.dto.ts` | `RegisterDto` (`email`, `password`, `name?`) | Phần 9.7 mục 5.7b |
| `src/auth/auth.service.ts` | `validateUser` + `login` + **`register`** (bcrypt + ConflictException) | Phần 9.7 mục 5.4 + 5.7b |
| `src/auth/jwt.strategy.ts` | `JwtStrategy` — đọc Header `Bearer`, xác minh chữ ký | Phần 9.7 mục 5.5 |
| `src/auth/jwt-auth.guard.ts` | `JwtAuthGuard` — lớp vỏ để `@UseGuards` | Phần 9.7 mục 5.6 |
| `src/auth/auth.controller.ts` | `POST login` + **`POST register`** | Phần 9.7 mục 5.7 |
| `src/auth/auth.module.ts` | Ráp `JwtModule` + `PassportModule` + tất cả lại | Phần 9.7 mục 5.8 |

Sinh khung Module trước bằng CLI cho nhanh (CLI tự tạo `auth.module.ts`, bạn chỉ cần sửa lại đúng nội dung ở bảng trên):
```bash
nest g module auth
nest g controller auth
nest g service auth
```

Đăng ký `AuthModule` vào `src/app.module.ts` (chỉ **thêm**):
```typescript
imports: [ConfigModule.forRoot({ isGlobal: true }), PrismaModule, ProductModule, AiModule, AuthModule],
```

Test bằng `curl` với đúng User đã seed ở Bước 7d.6:
```bash
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@shopai.com","password":"123456"}'
# -> { "accessToken": "eyJhbGciOiJIUzI1NiJ9...", "user": { "id": "...", "email": "demo@shopai.com", "name": "Học viên Demo" } }

# Thử sai mật khẩu:
curl -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@shopai.com","password":"sai-mat-khau"}'
# -> 401 { "message": "Email hoặc mật khẩu không đúng" }
```

> [!TIP]
> Copy chuỗi `accessToken` vừa nhận, dán vào ô decode ở `jwt.io` — bạn sẽ thấy đúng `payload` chứa `sub` (userId) và `email` như đã ký ở Phần 9.7 mục 5.4, đúng cấu trúc `header.payload.signature` đã học ở Phần 9.7 mục 2.

#### Bước 7e.5: `POST /api/auth/register` — nối RegisterScreen (Ch.5/6)

Gõ đủ `RegisterDto` + `AuthService.register` + route `POST register` như **Phần 9.7 mục 5.7b**. Test:

```bash
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"new@shopai.com","password":"123456","name":"Học viên mới"}'
# -> { "accessToken": "...", "user": { ... } }

# Trùng email -> 409
curl -i -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@shopai.com","password":"123456"}'
```

#### Bước 7f: Orders API — `POST /api/orders` với Prisma Repository, bảo vệ bằng `JwtAuthGuard`

Đây là bước hợp nhất cả `Phần 9.7` (Guard) và `Phần 9.8` (Prisma + Repository Pattern) vào đúng một endpoint — thực hiện trọn vẹn lời hứa từ Chương 6 (Phần 9.12), lần này với dữ liệu thật và có bảo vệ thật. Sinh Module bằng CLI:
```bash
nest g module order
nest g controller order
nest g service order
```

**7f.1. DTO cho đơn hàng** — tạo `src/order/dto/create-order.dto.ts` (giữ nguyên như bản trước, không đổi gì — `ValidationPipe` không quan tâm dữ liệu sẽ lưu vào đâu):
```typescript
import { Type } from 'class-transformer';
import { ArrayNotEmpty, IsArray, IsNumber, IsString, Min, ValidateNested } from 'class-validator';

export class OrderItemDto {
  @IsString()
  productId: string;

  @IsNumber()
  @Min(1, { message: 'Số lượng tối thiểu là 1' })
  quantity: number;
}

export class CreateOrderDto {
  @IsArray()
  @ArrayNotEmpty({ message: 'Giỏ hàng đang trống, không thể đặt hàng' })
  @ValidateNested({ each: true })  // Kiểm tra TỪNG phần tử bên trong mảng
  @Type(() => OrderItemDto)        // BẮT BUỘC: báo cho class-transformer biết kiểu phần tử là gì
  items: OrderItemDto[];

  @IsNumber()
  @Min(0)
  total: number; // Chỉ dùng để ĐỐI CHIẾU, không dùng để ghi vào đơn (Phần 9.12 mục 2)
}
```

> [!IMPORTANT]
> Thiếu dòng `@Type(() => OrderItemDto)`, `class-transformer` không biết mảng chứa kiểu gì nên sẽ **bỏ qua toàn bộ validation bên trong** — Client gửi `items: [{ quantity: -99 }]` vẫn lọt qua. Đây là cái bẫy im lặng phổ biến nhất khi validate dữ liệu lồng nhau.

**7f.2. `PrismaOrderRepository`** — tạo `src/order/order.repository.ts`. Đây chính là "bản nâng cấp" của Repository Pattern đã học ở Phần 9.8 mục 5 — cùng một Interface, đổi hẳn phần triển khai bên trong sang Prisma:
```typescript
import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma/prisma.service';

export interface CreateOrderInput {
  id: string;
  userId: string;
  total: number;
  items: { productId: string; quantity: number; price: number }[];
}

export interface OrderRecord {
  id: string;
  userId: string;
  total: number;
  status: string;
  createdAt: Date;
  items: { productId: string; quantity: number; price: number }[];
}

// Bản hợp đồng GIỮ NGUYÊN như Phần 9.8 mục 5 — chỉ phần triển khai bên dưới là mới
export interface IOrderRepository {
  save(input: CreateOrderInput): Promise<OrderRecord>;
  findAll(): Promise<OrderRecord[]>;
  findByUserId(userId: string): Promise<OrderRecord[]>;
  findById(orderId: string): Promise<OrderRecord | null>;
  updateStatus(orderId: string, status: string): Promise<OrderRecord>;
}

@Injectable()
export class PrismaOrderRepository implements IOrderRepository {
  constructor(private readonly prisma: PrismaService) {}

  async save(input: CreateOrderInput): Promise<OrderRecord> {
    // "items: { create: [...] }" là cú pháp Prisma để tạo Order VÀ toàn bộ OrderItem con
    // trong CÙNG một câu lệnh/transaction — không sợ tạo được Order mà thiếu Item giữa chừng.
    return this.prisma.order.create({
      data: {
        id: input.id,
        userId: input.userId,
        total: input.total,
        status: 'PENDING',
        items: { create: input.items },
      },
      include: { items: true }, // Trả kèm luôn danh sách items trong response
    });
  }

  async findAll(): Promise<OrderRecord[]> {
    return this.prisma.order.findMany({
      include: { items: true },
      orderBy: { createdAt: 'desc' }, // Đơn mới nhất lên đầu — tiện giảng viên nghiệm thu
    });
  }

  async findByUserId(userId: string): Promise<OrderRecord[]> {
    return this.prisma.order.findMany({
      where: { userId },
      include: { items: true },
      orderBy: { createdAt: 'desc' },
    });
  }

  async findById(orderId: string): Promise<OrderRecord | null> {
    return this.prisma.order.findUnique({ where: { id: orderId }, include: { items: true } });
  }

  async updateStatus(orderId: string, status: string): Promise<OrderRecord> {
    return this.prisma.order.update({
      where: { id: orderId },
      data: { status },
      include: { items: true },
    });
  }
}
```

**7f.3. Order Service** — nơi thực thi nguyên tắc "Server tự tính lại tiền" (Phần 9.12), giờ nhận thêm `userId` lấy từ Token đã xác thực. Mở `src/order/order.service.ts`:
```typescript
import { BadRequestException, Inject, Injectable } from '@nestjs/common';
import { ProductService } from '../product/product.service';
import { CreateOrderDto } from './dto/create-order.dto';
import { IOrderRepository } from './order.repository';

@Injectable()
export class OrderService {
  constructor(
    private readonly productService: ProductService,
    // Tiêm qua token chuỗi 'IOrderRepository' (khai báo ở order.module.ts) chứ không tiêm thẳng Class —
    // đây chính là kỹ thuật cho phép đổi triển khai (Prisma/In-memory) mà không sửa dòng nào ở đây.
    @Inject('IOrderRepository') private readonly orderRepository: IOrderRepository,
  ) {}

  async createOrder(dto: CreateOrderDto, userId: string) {
    let serverTotal = 0;
    const enrichedItems: { productId: string; quantity: number; price: number }[] = [];

    for (const item of dto.items) {
      const product = this.productService.findRawById(item.productId);
      if (!product) {
        throw new BadRequestException(`Sản phẩm ${item.productId} không còn tồn tại`);
      }
      serverTotal += product.price * item.quantity; // Giá lấy từ KHO CỦA SERVER, không lấy từ Client
      enrichedItems.push({ ...item, price: product.price });
    }

    // Đối chiếu với con số Mobile gửi lên (Phần 9.12 mục 2) — không đổi gì so với bản trước
    if (serverTotal !== dto.total) {
      throw new BadRequestException(
        `Tổng tiền không khớp. Server tính ${serverTotal}, Client gửi ${dto.total}. Vui lòng tải lại giỏ hàng.`,
      );
    }

    return this.orderRepository.save({
      id: `ORD-${Date.now()}`, // Thực tế nên dùng uuid; Date.now() đủ dùng cho lớp học
      userId, // ➕ MỚI: biết chính xác đơn này của ai, lấy từ req.user do JwtAuthGuard gắn vào
      total: serverTotal, // Luôn ghi con số của SERVER
      items: enrichedItems,
    });
  }

  async getOrdersForUser(userId: string) {
    return this.orderRepository.findByUserId(userId);
  }

  async getOrderForUser(orderId: string, userId: string) {
    const order = await this.orderRepository.findById(orderId);
    if (!order || order.userId !== userId) {
      throw new NotFoundException('Không tìm thấy hóa đơn');
    }
    return order;
  }

  async payOrder(orderId: string, userId: string) {
    const order = await this.getOrderForUser(orderId, userId);
    if (order.status === 'PAID') {
      return order; // Idempotent — bấm Pay lần 2 không lỗi
    }
    if (order.status !== 'PENDING') {
      throw new BadRequestException(`Không thể thanh toán đơn ở trạng thái ${order.status}`);
    }
    // Giả lập cổng thanh toán (Momo/VNPay/Stripe) — Production sẽ verify webhook
    return this.orderRepository.updateStatus(orderId, 'PAID');
  }

  async getAllOrders() {
    return this.orderRepository.findAll();
  }
}
```

> [!NOTE]
> Thêm import `NotFoundException` vào đầu `order.service.ts` (cùng chỗ `BadRequestException`).

**7f.4. Order Controller** — nơi gắn `JwtAuthGuard` (Phần 9.7 mục 4):
```typescript
import { Body, Controller, Get, Param, Post, Req, UseGuards } from '@nestjs/common';
import { ApiBearerAuth, ApiTags } from '@nestjs/swagger';
import { JwtAuthGuard } from '../auth/jwt-auth.guard';
import { CreateOrderDto } from './dto/create-order.dto';
import { OrderService } from './order.service';

@ApiTags('Orders')
@Controller('api/orders')
@UseGuards(JwtAuthGuard) // Toàn bộ Orders API yêu cầu JWT — kể cả GET lịch sử
@ApiBearerAuth()
export class OrderController {
  constructor(private readonly orderService: OrderService) {}

  @Post() // POST /api/orders → tạo đơn status PENDING
  async create(@Body() dto: CreateOrderDto, @Req() req: any) {
    return this.orderService.createOrder(dto, req.user.userId);
  }

  @Get() // GET /api/orders — lịch sử đơn CỦA user đang đăng nhập (không lộ đơn người khác)
  async findMine(@Req() req: any) {
    return this.orderService.getOrdersForUser(req.user.userId);
  }

  @Get(':id') // GET /api/orders/:id — chi tiết hóa đơn
  async findOne(@Param('id') id: string, @Req() req: any) {
    return this.orderService.getOrderForUser(id, req.user.userId);
  }

  @Post(':id/pay') // POST /api/orders/:id/pay — giả lập thanh toán PENDING → PAID
  async pay(@Param('id') id: string, @Req() req: any) {
    return this.orderService.payOrder(id, req.user.userId);
  }
}
```

> [!IMPORTANT]
> Bản cũ `GET /api/orders` **không** Guard (để giảng viên xem nhanh) đã **thay** bằng bản có JWT + lọc theo `userId`. Muốn soi toàn DB lúc demo lớp: dùng `npx prisma studio` — **không** mở API public lộ đơn hàng người khác.
**7f.5. Ráp Module** — `src/order/order.module.ts`. Chú ý dòng `providers` áp dụng đúng Repository Pattern (Phần 9.8 mục 5):
```typescript
import { Module } from '@nestjs/common';
import { ProductModule } from '../product/product.module';
import { OrderController } from './order.controller';
import { PrismaOrderRepository } from './order.repository';
import { OrderService } from './order.service';

@Module({
  imports: [ProductModule], // Mượn ProductService từ Module hàng xóm (PrismaModule đã @Global, không cần import lại)
  controllers: [OrderController],
  providers: [
    OrderService,
    { provide: 'IOrderRepository', useClass: PrismaOrderRepository }, // Đổi useClass thành InMemoryOrderRepository là quay lại bản cũ — không sửa gì ở OrderService/Controller
  ],
})
export class OrderModule {}
```

Và `ProductModule` phải **cho phép** mượn bằng cách khai báo `exports`:
```typescript
@Module({
  controllers: [ProductController],
  providers: [ProductService],
  exports: [ProductService], // ➕ MỚI — thiếu dòng này, OrderModule sẽ báo lỗi "can't resolve dependencies"
})
export class ProductModule {}
```

Cuối cùng đăng ký `OrderModule` vào `src/app.module.ts` — đây là danh sách `imports` **đầy đủ** sau khi hoàn thành hết Bước 7d–7f:
```typescript
imports: [
  ConfigModule.forRoot({ isGlobal: true }),
  PrismaModule,
  ProductModule,
  AiModule,
  AuthModule,
  OrderModule,
],
```

Test lại toàn bộ luồng bằng `curl`:
```bash
# 1) Không có Token -> phải bị chặn
curl -i -X POST http://localhost:3000/api/orders \
  -H "Content-Type: application/json" \
  -d '{"items":[{"productId":"backend_prod_0","quantity":2}],"total":2000000}'
# -> 401 Unauthorized

# 2) Đăng nhập lấy Token thật (Bước 7e)
TOKEN=$(curl -s -X POST http://localhost:3000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"demo@shopai.com","password":"123456"}' | python3 -c "import sys,json;print(json.load(sys.stdin)['accessToken'])")

# 3) Đặt hàng kèm Bearer Token -> phải thành công
curl -X POST http://localhost:3000/api/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"items":[{"productId":"backend_prod_0","quantity":2}],"total":2000000}'
# -> { "id": "ORD-1735...", "userId": "...", "status": "PENDING", "total": 2000000, "items": [...] }

# 4) Thử gian lận tổng tiền (vẫn có Token hợp lệ) -> vẫn phải bị chặn bởi Phần 9.12
curl -X POST http://localhost:3000/api/orders \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $TOKEN" \
  -d '{"items":[{"productId":"backend_prod_0","quantity":2}],"total":1000}'
# -> 400 "Tổng tiền không khớp..."

# 5) Lịch sử đơn của CHÍNH user (cần Bearer)
curl -H "Authorization: Bearer $TOKEN" http://localhost:3000/api/orders
# -> [ { "id": "ORD-...", "status": "PENDING", ... } ]

# 6) Chi tiết hóa đơn
ORDER_ID=$(curl -s -H "Authorization: Bearer $TOKEN" http://localhost:3000/api/orders | python3 -c "import sys,json;print(json.load(sys.stdin)[0]['id'])")
curl -H "Authorization: Bearer $TOKEN" http://localhost:3000/api/orders/$ORDER_ID

# 7) Thanh toán giả lập PENDING → PAID
curl -X POST -H "Authorization: Bearer $TOKEN" http://localhost:3000/api/orders/$ORDER_ID/pay
# -> { ..., "status": "PAID" }

# 8) Restart Server (Ctrl+C, chạy lại npm run start:dev), rồi GET lại với Token — đơn VẪN CÒN (Prisma)
```

#### Bước 7g: Swagger — tài liệu API tự sinh

Cài thư viện:
```bash
npm install @nestjs/swagger
```

Thêm vào `src/main.ts` (đặt **trước** `app.listen`):
```typescript
import { DocumentBuilder, SwaggerModule } from '@nestjs/swagger'; // ➕ MỚI

  const swaggerConfig = new DocumentBuilder()
    .setTitle('ShopAI API')
    .setDescription('Backend phục vụ App React Native ShopAI (Chương 9)')
    .setVersion('1.0')
    .addBearerAuth() // Hiện ô nhập JWT — dùng thật ngay ở đây vì Guard (Phần 9.7) đã hoạt động
    .build();
  SwaggerModule.setup('api/docs', app, SwaggerModule.createDocument(app, swaggerConfig));
```

Để tài liệu có ví dụ đẹp, gắn thêm `@ApiProperty` vào DTO (`create-order.dto.ts`):
```typescript
import { ApiProperty } from '@nestjs/swagger';

export class OrderItemDto {
  @ApiProperty({ example: 'backend_prod_0' })
  @IsString()
  productId: string;

  @ApiProperty({ example: 2, minimum: 1 })
  @IsNumber()
  @Min(1)
  quantity: number;
}
```

`@ApiTags('Orders')` và `@ApiTags('Auth')` đã được gắn sẵn ở Bước 7e/7f — mở lại kiểm tra nếu Swagger UI thiếu nhóm nào.

Mở trình duyệt `http://localhost:3000/api/docs` — bạn có một trang tài liệu API đầy đủ 4 nhóm **Auth / Products / Orders / Ai**. Bấm nút **"Authorize"** ở góc trên bên phải, dán `accessToken` lấy từ `POST /api/auth/login` (Bước 7e) vào, bấm Authorize — từ giờ mọi request "Try it out" của `POST /api/orders` sẽ tự động đính kèm đúng `Authorization: Bearer <token>`, y hệt cách `axiosClient` làm phía Mobile.

> [!TIP]
> Đây là lúc kiểm chứng `ValidationPipe` sướng nhất: điền `quantity: -5` vào khung Try it out, bấm Execute, thấy ngay `400` kèm message tiếng Việt. Thử bấm "Try it out" của `POST /api/orders` mà **chưa** bấm "Authorize" — bạn sẽ thấy ngay `401`, bằng chứng trực quan `JwtAuthGuard` đang hoạt động thật.

#### Bước 7h: `.env.example` — bản mẫu cấu hình cho đồng đội

File `.env` chứa Key thật nên bị `.gitignore` chặn (Bước 6.2). Hậu quả: đồng đội `git clone` về sẽ **không biết cần khai báo những biến gì**, Server chạy lỗi mà không hiểu tại sao. Giải pháp chuẩn của ngành: commit một file mẫu rỗng.

Tạo `.env.example` ở gốc `shopai-backend`:
```bash
# ============================================
# ShopAI Backend — Bản mẫu biến môi trường
# Cách dùng: cp .env.example .env  rồi điền giá trị thật vào .env
# File .env KHÔNG BAO GIỜ được commit. File .env.example thì PHẢI commit.
# ============================================

# Cổng Server lắng nghe. Nhớ dùng cùng cổng này trong API_BASE_URL bên Mobile.
PORT=3000

# API Key của Google Gemini — lấy tại https://aistudio.google.com/app/apikey
# Đây là bí mật ĐẮT TIỀN: lộ ra là người khác xài hết hạn mức của bạn (xem Phần 9.10).
GEMINI_API_KEY=

# Chuỗi bí mật ký JWT — BẮT BUỘC từ Sprint 9 (Phần 9.7 mục 5.2, dùng ở AuthModule Bước 7e).
JWT_SECRET=
JWT_EXPIRES_IN=7d

# Chuỗi kết nối Database Prisma — BẮT BUỘC từ Sprint 9 (Phần 9.8, dùng ở Bước 7d).
# SQLite dùng cho lớp học: chỉ là một file nằm trong thư mục prisma/, không cần cài Server riêng.
DATABASE_URL="file:./dev.db"
```

Kiểm tra `.gitignore` của backend có đủ các dòng sau (thêm 2 dòng cuối cho Prisma — file Database SQLite và cache migrate cục bộ **không** commit lên Git, nhưng thư mục `prisma/migrations/` thì **phải** commit vì nó là lịch sử Schema của cả team):
```
.env
.env.local
/prisma/dev.db
/prisma/dev.db-journal
```

> [!TIP]
> Quy tắc phân biệt dễ nhớ: **`.env` chứa GIÁ TRỊ (bí mật, không commit) — `.env.example` chứa TÊN BIẾN (công khai, phải commit).** Khi vào công ty, việc đầu tiên sau khi clone repo backend luôn là `cp .env.example .env` rồi `npx prisma migrate dev` để tự tạo lại Database rỗng từ lịch sử migration đã commit.

#### Bước 8: Mobile kết nối vào Server sản phẩm NestJS
Quay lại dự án React Native ShopAI. Để dùng chung 1 địa chỉ IP cho cả Product API và AI API, tạo file `src/constants/api.ts`:
```ts
// Đổi IP LAN này thành IP thật của máy tính bạn (xem bằng lệnh ipconfig / ifconfig).
// Máy tính và điện thoại phải chung 1 mạng Wifi (nhắc lại bẫy Localhost ở Phần 9.4).
export const API_BASE_URL = 'http://192.168.1.15:3000';
```

Mở file `src/screens/HomeScreen.tsx`, cập nhật lại hàm `fetchProductsAPI` để gọi thẳng vào Server NestJS thay vì Mock Data cũ. **Giữ nguyên trạm kiểm soát Zod (`ProductListSchema.safeParse`) đã dựng ở Chương 6** — dữ liệu thật từ Server qua mạng lại càng cần bị nghi ngờ và kiểm tra nghiêm ngặt hơn dữ liệu Mock giả lập:

```tsx
import { API_BASE_URL } from '@constants/api';
import { Product, ProductListSchema } from '@types/product.schema'; // Tái sử dụng đúng Schema đã dựng ở Chương 6

const API_URL = `${API_BASE_URL}/api/products`;

const fetchProductsAPI = async (): Promise<Product[]> => {
  const response = await fetch(API_URL);
  if (!response.ok) {
    throw new Error('Lỗi mạng từ Server NestJS');
  }
  const rawData = await response.json(); // Dữ liệu thô — chưa hề được tin tưởng, dù nó đến từ Server "của mình"

  // TRẠM KIỂM SOÁT ZOD (giống hệt Chương 6): không vì Server là "hàng nhà mình" mà bỏ qua bước kiểm duyệt này
  const result = ProductListSchema.safeParse(rawData);
  if (!result.success) {
    console.error('❌ Zod chặn dữ liệu bẩn từ Server NestJS:', result.error.format());
    throw new Error('Dữ liệu sản phẩm từ Server không hợp lệ (Zod validation failed)!');
  }

  return result.data; // Đã được Zod đảm bảo 100% đúng kiểu, an toàn tuyệt đối
};
```

> [!IMPORTANT]
> **Bắt buộc: cập nhật `baseURL` của `axiosClient`.** Mở `src/api/axiosClient.ts` (dựng ở Chương 6, Phần 6.6), sửa `baseURL: 'https://api.shopai.com'` (domain giả lập) thành `baseURL: API_BASE_URL` import từ `@constants/api`. Đây không còn là gợi ý tùy chọn: `axiosClient` đã có sẵn Interceptor tự gắn `Authorization: Bearer <token>` (Chương 6), và **Bước 9d + 9c** dưới đây sẽ dùng đúng `axiosClient` này để gọi `POST /api/auth/login` và `POST /api/orders` thật. Nếu quên đổi `baseURL`, mọi request qua `axiosClient` sẽ bay vào một domain ảo không tồn tại. Nguyên tắc "một nguồn sự thật" (Single Source of Truth) cho địa chỉ Server áp dụng cho cả `fetch` thuần và `axiosClient`.

#### Bước 9: Mobile gọi "Vệ sĩ AI" thay vì gọi trực tiếp Google — chốt vòng bảo mật

> [!IMPORTANT]
> **Giữ nguyên UX Chương 8.** Không rút `AIChatScreen` về bản tối giản chỉ còn `fetch` một câu. Vẫn giữ: lịch sử hội thoại, typing indicator, nút Thử lại, gợi ý câu hỏi, cuộn xuống tin mới. **Chỉ đổi** chỗ gọi: từ `askShopAI()` (SDK client) → `axiosClient.post('/api/ai/chat', { message, history })`. Xóa `geminiConfig.ts` và SDK `@google/generative-ai` phía Mobile.

**9.1. Cập nhật `src/services/geminiService.ts` (hoặc đổi tên thành `aiChatService.ts`)** — bỏ SDK Google, giữ helper chuyển lỗi thân thiện + build history:

```ts
import axiosClient from '@api/axiosClient';

/** Cùng tinh thần ChatTurn Chương 8 — đơn giản hóa khi gửi Nest */
export type ChatTurn = {
  role: 'user' | 'model';
  parts?: { text: string }[];
  text?: string;
};

/** Gọi NestJS /api/ai/chat — Server cầm Gemini Key */
export const askShopAI = async (
  question: string,
  history: ChatTurn[] = [],
): Promise<string> => {
  const { data } = await axiosClient.post<{ reply: string }>('/api/ai/chat', {
    message: question,
    history: history.map((h) => ({
      role: h.role,
      text: h.parts?.[0]?.text ?? h.text ?? '',
    })),
  });
  return data.reply;
};

// GIỮ NGUYÊN toFriendlyError từ Chương 8 (copy nguyên hàm cũ vào đây)
```

> Nếu `ChatTurn` của Ch8 dùng đúng format Gemini `{ role, parts: [{ text }] }`, map sang `{ role, text }` như trên trước khi gửi Nest. **Không xóa** `AI_SUGGESTIONS` / `AI_GREETING` trong `@constants/aiPrompt`.

**9.2. `AIChatScreen.tsx`:** giữ gần như nguyên file Chương 8 — chỉ đổi import `askShopAI` sang bản mới (gọi Nest). **Không** thay bằng bản chat "1 ô nhập + 1 FlatList tối giản". Checklist nghiệm thu Ch8 (Thử lại, gợi ý, nhớ ngữ cảnh) vẫn phải PASS sau bước này. Xóa file `src/constants/geminiConfig.ts`.

```tsx
// Pseudo — trong sendMessage/coreSend của Ch8, thay khối gọi cũ bằng:
const reply = await askShopAI(question, buildHistory(historySource));
// Phần còn lại (setMessages, isTyping, retry, suggestions) GIỮ NGUYÊN như Chương 8.
```

> Có thể dùng `axiosClient` (đã gắn Bearer) hoặc `fetch` + `API_BASE_URL` — ưu tiên `axiosClient` để đồng bộ Interceptor.

> ✅ **Kiểm chứng vòng lặp bảo mật đã khép:** mở file APK/IPA build ra, dịch ngược thoải mái — sẽ không còn tìm thấy bất kỳ chuỗi Gemini API Key nào nữa. Key giờ chỉ tồn tại trong file `.env` trên máy Server, không hề được đóng gói vào app.

#### Bước 9b: `ProductDetailScreen` fetch dữ liệu thật theo `id`

Ở Chương 6 (Bước 8.5), `ProductDetailScreen` đang **mượn cache** của `HomeScreen` qua `queryClient.getQueryData(['productsList'])`. Cách này nhanh và tiết kiệm request, nhưng có một lỗ hổng thật: nếu người dùng mở app từ **Deep Link** `shopai://product/backend_prod_3` (đã cấu hình ở Chương 5) mà chưa hề vào Trang chủ, cache rỗng → màn hình trắng.

Giờ Backend đã có `GET /api/products/:id` (Bước 7c), ta cho `ProductDetailScreen` tự fetch, đồng thời **vẫn tận dụng cache** làm dữ liệu hiển thị tạm.

Trước hết bổ sung Schema cho một sản phẩm đơn lẻ trong `src/types/product.schema.ts` (file đã tạo ở Chương 6):
```ts
// ProductSchema và ProductListSchema đã có sẵn từ Chương 6 — chỉ cần export thêm ProductSchema
// nếu trước đó bạn mới chỉ export mỗi ProductListSchema.
export const ProductListSchema = z.array(ProductSchema);
```

Mở `src/screens/ProductDetailScreen.tsx`:
```tsx
import React from 'react';
import { View, Text, Image, ActivityIndicator, StyleSheet } from 'react-native';
import { useRoute, RouteProp } from '@react-navigation/native';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import ShopButton from '@components/ShopButton';
import { useCartStore } from '@store/useCartStore';
import { API_BASE_URL } from '@constants/api';
import { Product, ProductSchema } from '@types/product.schema';
import { formatCurrency } from '@utils/formatCurrency';
import { COLORS, SIZES } from '@constants/theme';
import { HomeStackParamList } from '@navigation/HomeStackNavigator';

const fetchProductById = async (id: string): Promise<Product> => {
  const response = await fetch(`${API_BASE_URL}/api/products/${id}`);

  // Bắt đúng mã 404 mà NestJS ném ra ở Bước 7c — hai đầu ăn khớp nhau
  if (response.status === 404) {
    throw new Error('Sản phẩm này không còn tồn tại trên hệ thống');
  }
  if (!response.ok) {
    throw new Error('Lỗi mạng khi tải chi tiết sản phẩm');
  }

  const raw = await response.json();
  const result = ProductSchema.safeParse(raw); // Vẫn giữ trạm kiểm soát Zod từ Chương 6
  if (!result.success) {
    throw new Error('Dữ liệu chi tiết sản phẩm không hợp lệ (Zod)');
  }
  return result.data;
};

const ProductDetailScreen = () => {
  const route = useRoute<RouteProp<HomeStackParamList, 'ProductDetail'>>();
  const { productId } = route.params;
  const queryClient = useQueryClient();
  const addItem = useCartStore((state) => state.addItem);

  const { data: product, isLoading, isError, error } = useQuery({
    queryKey: ['product', productId], // Mỗi sản phẩm có ô cache riêng
    queryFn: () => fetchProductById(productId),

    // Mẹo hay: lấy tạm dữ liệu từ cache danh sách mà HomeScreen đã tải, hiển thị NGAY
    // trong lúc request chi tiết đang bay. Người dùng không thấy màn hình Loading chớp nháy.
    placeholderData: () =>
      queryClient
        .getQueryData<Product[]>(['productsList'])
        ?.find((p) => p.id === productId),
  });

  if (isLoading && !product) {
    return <ActivityIndicator size="large" color={COLORS.primary} style={styles.center} />;
  }

  if (isError || !product) {
    return (
      <View style={styles.center}>
        <Text style={styles.errorText}>{(error as Error)?.message ?? 'Không tìm thấy sản phẩm'}</Text>
      </View>
    );
  }

  return (
    <View style={styles.container}>
      <Image source={{ uri: product.image }} style={styles.image} />
      <Text style={styles.name}>{product.name}</Text>
      <Text style={styles.price}>{formatCurrency(product.price)}</Text>
      <ShopButton title="Thêm vào giỏ hàng" onPress={() => addItem(product)} />
    </View>
  );
};

const styles = StyleSheet.create({
  container: { flex: 1, padding: SIZES.padding, backgroundColor: COLORS.background },
  center: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  image: { width: '100%', height: 300, borderRadius: SIZES.radius, marginBottom: 16 },
  name: { fontSize: SIZES.h2, fontWeight: 'bold', color: COLORS.text, marginBottom: 8 },
  price: { fontSize: SIZES.h2, color: COLORS.primary, fontWeight: 'bold', marginBottom: 24 },
  errorText: { color: COLORS.danger, fontSize: SIZES.body1, textAlign: 'center' },
});

export default ProductDetailScreen;
```

> [!TIP]
> `placeholderData` là một kỹ thuật React Query rất được ưa chuộng trong app thương mại điện tử: người dùng bấm vào Card sản phẩm, ảnh và tên hiện ra **tức thì** (lấy từ cache danh sách), rồi vài trăm mili-giây sau dữ liệu đầy đủ từ Server âm thầm thay thế. Cảm giác app "nhanh như chớp" đến từ những chi tiết như thế này, không phải từ đường truyền mạnh hơn.

#### Bước 9c: `CheckoutScreen` đặt hàng thật lên NestJS — qua `axiosClient` kèm Bearer Token

Đây là bước thực hiện lời hứa trong comment ở Chương 6. Mở `src/screens/CheckoutScreen.tsx`, thay khối `setTimeout` giả lập bằng một lời gọi API thật. Chú ý: từ giờ ta dùng **`axiosClient`** (Chương 6, Phần 6.6) thay vì `fetch` thô — vì `POST /api/orders` giờ **bắt buộc** phải có `Authorization: Bearer <token>` (Bước 7f), và `axiosClient` đã có sẵn Interceptor tự làm việc đó, ta không cần tự tay gắn Header.

**9c.1. Viết hàm gọi API** (đặt ngay trên component):
```tsx
import axiosClient from '@api/axiosClient'; // ĐỔI: dùng axiosClient thay vì fetch thô
import { CartItem } from '@store/useCartStore';

type CreateOrderResponse = { id: string; status: string; total: number; createdAt: string };

const placeOrderAPI = async (items: CartItem[], total: number): Promise<CreateOrderResponse> => {
  // KHÔNG cần tự gắn header Authorization — Request Interceptor của axiosClient (Chương 6, Phần 6.6)
  // tự động đọc useAuthStore.getState().token và gắn "Bearer <token>" vào MỌI request qua axiosClient.
  const response = await axiosClient.post('/api/orders', {
    // Chỉ gửi productId + quantity — KHÔNG gửi giá. Server tự tra giá thật (Phần 9.12 mục 2).
    items: items.map((item) => ({ productId: item.id, quantity: item.quantity })),
    total,
  });

  return response.data;
};
```

> [!IMPORTANT]
> **Vì sao không cần bắt lỗi thủ công như bản `fetch` cũ?** Axios tự động `throw` một `AxiosError` khi status không phải `2xx` — khác với `fetch` (`fetch` chỉ báo lỗi khi mất mạng, còn `404`/`400`/`401` vẫn coi là "thành công" và phải tự kiểm tra `response.ok`). Nghĩa là khối `try/catch` ở bước 9c.2 bên dưới sẽ tự bắt được cả lỗi `400` (sai tổng tiền) lẫn `401` (chưa đăng nhập/Token hết hạn) mà không cần viết thêm `if`.

**9c.2. Nối vào `handleConfirm`** — thay toàn bộ khối `setTimeout` cũ, đọc đúng message tiếng Việt từ lỗi Axios:
```tsx
const items = useCartStore((state) => state.items); // ➕ MỚI: cần danh sách item để gửi lên Server
const [errorMessage, setErrorMessage] = useState<string | null>(null); // ➕ MỚI
const [orderId, setOrderId] = useState<string | null>(null);           // ➕ MỚI

const handleConfirm = async () => {
  setIsPlacing(true);
  setErrorMessage(null);

  try {
    const order = await placeOrderAPI(items, totalPrice);

    setOrderId(order.id);
    setIsDone(true);
    clearCart(); // ⚠️ CHỈ xóa giỏ SAU KHI Server xác nhận thành công — xem cảnh báo bên dưới
    setTimeout(() => navigation.goBack(), 1500);
  } catch (error: any) {
    // error.response.data.message là body lỗi mà NestJS trả về (VD "Tổng tiền không khớp...", hoặc
    // "Unauthorized" nếu Token hết hạn — lúc đó Response Interceptor ở Chương 6 đã tự bắn logout() rồi)
    const serverMessage = error?.response?.data?.message;
    const message = Array.isArray(serverMessage)
      ? serverMessage.join(', ')   // ValidationPipe trả về MẢNG message
      : serverMessage ?? 'Đặt hàng thất bại, vui lòng thử lại';
    setErrorMessage(message);
  } finally {
    setIsPlacing(false); // Mở khóa nút bấm dù thành công hay thất bại
  }
};
```

**9c.3. Hiển thị mã đơn hàng và thông báo lỗi** — sửa nhẹ phần JSX:
```tsx
if (isDone) {
  return (
    <SafeAreaView style={styles.safeArea}>
      <View style={styles.center}>
        <Text style={styles.successIcon}>✅</Text>
        <Text style={styles.successText}>Đặt hàng thành công!</Text>
        {/* ➕ MỚI: khoe mã đơn hàng do Server sinh ra — bằng chứng dữ liệu đã đi hết một vòng */}
        <Text style={styles.orderIdText}>Mã đơn: {orderId}</Text>
      </View>
    </SafeAreaView>
  );
}

// ...trong phần return chính, đặt ngay trên nút Xác nhận:
{errorMessage && <Text style={styles.errorText}>⚠️ {errorMessage}</Text>}
```

Thêm 2 style mới:
```tsx
orderIdText: { marginTop: 8, fontSize: SIZES.body2, color: COLORS.textLight },
errorText: { marginTop: 16, color: COLORS.danger, fontSize: SIZES.body2, textAlign: 'center' },
```

> [!WARNING]
> **Đừng bao giờ gọi `clearCart()` trước khi Server xác nhận.** Bản Chương 6 xóa giỏ ngay trong `setTimeout` vì khi đó không có Server nào để mà thất bại. Giờ thì có: nếu mạng rớt giữa chừng mà bạn đã xóa giỏ, người dùng vừa **mất sạch giỏ hàng vừa không có đơn nào** — lỗi nghiêm trọng nhất có thể xảy ra trong một app bán hàng. Thứ tự đúng luôn là: gọi API → chờ thành công → mới xóa dữ liệu cục bộ.

> [!TIP]
> **Cách test đường thất bại (rất nên làm):** tắt Server NestJS (`Ctrl+C`) rồi bấm "Xác nhận đặt hàng". App phải hiện dòng lỗi đỏ, **giỏ hàng vẫn còn nguyên**, và nút bấm được mở khóa để thử lại. Thử thêm: đăng xuất rồi tìm cách gọi lại `placeOrderAPI` (VD sửa tạm `useAuthStore` để `token = null`) — phải nhận `401` và hiện lỗi lịch sự, không được crash app.

#### Bước 9d: `LoginScreen` đăng nhập thật — nhận JWT thật thay vì Token giả

Đây là mắt xích cuối cùng khép kín Sprint 9: từ Chương 6, `LoginScreen` vẫn đang `login('mock_token_123')` — một chuỗi bịa ra. Từ bây giờ, `JwtAuthGuard` ở Backend (Bước 7f) kiểm tra chữ ký thật, nên Token giả sẽ luôn bị từ chối với `401`. Ta cần `LoginScreen` gọi đúng `POST /api/auth/login` (Bước 7e) và dùng `accessToken` thật trả về.

Mở `src/screens/LoginScreen.tsx` (đã dựng ở Chương 6 Bước 6, dùng `useAuthStore().login`), sửa đúng hàm `handleLogin` — **UI Kit `ShopInput`/`ShopButton` và phần `validate()` giữ nguyên 100%**:
```tsx
import axiosClient from '@api/axiosClient'; // ➕ MỚI

// ... trong component LoginScreen, thay thế toàn bộ hàm handleLogin cũ ...
const [serverError, setServerError] = useState<string | null>(null); // ➕ MỚI: lỗi từ Server (sai mật khẩu...)

const handleLogin = async () => {
  if (!validate()) return; // Validate phía Client GIỮ NGUYÊN như Chương 5 — chặn sớm trước khi tốn 1 request
  setLoading(true);
  setServerError(null);

  try {
    // ĐÃ XÓA: setTimeout giả lập của Chương 6
    const response = await axiosClient.post('/api/auth/login', { email, password });
    login(response.data.accessToken); // Bắn Token THẬT lên mây — App.tsx tự động phát hiện và đổi trang!
  } catch (error: any) {
    // 401 từ AuthService (Phần 9.7 mục 5.4): "Email hoặc mật khẩu không đúng"
    setServerError(error?.response?.data?.message ?? 'Đăng nhập thất bại, vui lòng thử lại');
  } finally {
    setLoading(false);
  }
};
```

Hiển thị `serverError` ngay dưới 2 ô nhập (thêm 1 dòng JSX, style tái sử dụng như `CheckoutScreen`):
```tsx
{serverError && <Text style={styles.errorText}>⚠️ {serverError}</Text>}
```

Đăng nhập thử với đúng tài khoản đã seed ở Bước 7d.6: email `demo@shopai.com`, mật khẩu `123456`.

#### Bước 9e: `RegisterScreen` gọi `POST /api/auth/register` thật

Mở `src/screens/RegisterScreen.tsx` (Ch.5/6). Trong `handleRegister`, **đổi** `setTimeout` / `login('mock_token_123')` thành:

```tsx
try {
  const response = await axiosClient.post('/api/auth/register', {
    email,
    password,
    name: name.trim(),
  });
  login(response.data.accessToken);
} catch (error: any) {
  const msg = error?.response?.data?.message;
  setServerError(Array.isArray(msg) ? msg.join(', ') : msg ?? 'Đăng ký thất bại');
} finally {
  setLoading(false);
}
```

Nghiệm thu: đăng ký `new@shopai.com` → vào Main; thử lại cùng email → thấy lỗi 409.

#### Bước 9f: Lịch sử đơn + Pay — nối Nest (thay `useOrderStore` local)

UI Tab Đơn hàng / `OrderDetailScreen` đã có từ **Chương 6 Bước 9.6**. Ở đây chỉ đổi **nguồn dữ liệu**.

**9f.1. `OrdersScreen` — `useQuery` thay vì `useOrderStore`:**

```tsx
import { useQuery } from '@tanstack/react-query';
import axiosClient from '@api/axiosClient';

const { data: orders = [], isLoading, isError, refetch } = useQuery({
  queryKey: ['orders'],
  queryFn: async () => {
    const res = await axiosClient.get('/api/orders');
    return res.data as Array<{
      id: string;
      total: number;
      status: string;
      createdAt: string;
    }>;
  },
});
```

Map `orders` vào `FlatList` như cũ; thêm Pull-to-refresh `refetch`.

**9f.2. `OrderDetailScreen` — GET chi tiết + mutation Pay:**

```tsx
const { data: order, isLoading } = useQuery({
  queryKey: ['order', orderId],
  queryFn: async () => (await axiosClient.get(`/api/orders/${orderId}`)).data,
});

const queryClient = useQueryClient();
const payMutation = useMutation({
  mutationFn: async () => (await axiosClient.post(`/api/orders/${orderId}/pay`)).data,
  onSuccess: () => {
    queryClient.invalidateQueries({ queryKey: ['order', orderId] });
    queryClient.invalidateQueries({ queryKey: ['orders'] });
  },
});

// Nút: onPress={() => payMutation.mutate()} khi order.status === 'PENDING'
```

**9f.3. `CheckoutScreen` `onSuccess`:** sau khi đặt hàng Nest thành công, gọi `queryClient.invalidateQueries({ queryKey: ['orders'] })` — **có thể bỏ** `useOrderStore.addOrder` local (hoặc giữ tạm song song rồi xóa hẳn khi ổn định).

#### Bước 10: Tận hưởng siêu hệ thống 2 chiều
Khởi động lại Backend (`npm run start:dev`) và Mobile, rồi đi hết một vòng nghiệm thu theo đúng thứ tự sau:

1. **Trang chủ:** kéo xuống load lại — tên sản phẩm đã đổi thành `"Sản phẩm từ NestJS Server"`.
2. **Chi tiết sản phẩm:** bấm vào một Card — ảnh/tên hiện ra tức thì (nhờ `placeholderData`), dữ liệu đầy đủ đến ngay sau đó từ `GET /api/products/:id`.
3. **Đăng ký / Đăng nhập thật:** đăng ký user mới **hoặc** đăng nhập `demo@shopai.com` / `123456` — JWT thật vào SecureStore.
4. **Giỏ hàng → Thanh toán:** thêm SP → Checkout → mã đơn `ORD-...`, status **`PENDING`**, giỏ tự xóa.
5. **Tab Đơn hàng:** thấy đơn vừa tạo từ Nest; mở **Chi tiết hóa đơn** → bấm **Thanh toán giả lập** → status **`PAID`**.
6. **Kiểm chứng JWT:** không Token → `401` trên `POST/GET /api/orders`.
7. **Prisma bền vững:** restart Server → `GET /api/orders` (có Bearer) vẫn còn đơn `PAID`.
8. **Chatbot AI** qua Nest proxy — không lộ Gemini Key trên Mobile.
9. **Swagger** `/api/docs` — Auth (login+register) / Products / Orders (create+list+detail+pay) / AI.
10. **Đường thất bại:** tắt Server, đặt hàng lại — báo lỗi, giỏ còn nguyên.

Bạn vừa thiết lập thành công đường cao tốc dữ liệu 2 chiều, khép lại lỗ hổng bảo mật để lộ Key ở Chương 8, khoá chặt Orders API bằng JWT thật, chuyển dữ liệu đơn hàng sang Database bền vững qua Prisma, VÀ hoàn tất vòng đời mua sắm thương mại (Register → Order `PENDING` → Pay `PAID`). Bạn đã không còn là một thợ gõ giao diện, bạn đã chính thức bước lên đẳng cấp **Fullstack Software Engineer**.

```bash
# Lưu thành quả ở CẢ HAI repo
cd shopai-backend && git add . && git commit -m "Sprint 9: Nest register, JWT orders list/detail/pay PENDING-PAID, Prisma, AI proxy"
cd ../ShopAI && git add . && git commit -m "Sprint 9: real register/login, Nest checkout, orders history + pay"
```

### ✅ Checklist Nghiệm thu Sprint 9

**Backend `shopai-backend`:**
- [ ] `GET /api/products` trả về danh sách 20 sản phẩm, id **ổn định** giữa các lần gọi.
- [ ] `GET /api/products/:id` trả `200` với id hợp lệ và `404` (kèm message tiếng Việt) với id sai.
- [ ] `POST /api/products` với `price: -100` bị `ValidationPipe` chặn, trả `400` kèm danh sách lỗi.
- [ ] `npx prisma migrate dev` chạy thành công, có thư mục `prisma/migrations/` và file `prisma/dev.db`.
- [ ] Đã seed được ít nhất 1 User (`npx prisma db seed`), xem được bằng `npx prisma studio`.
- [ ] `POST /api/auth/login` với đúng email/mật khẩu trả về `{ accessToken }` là JWT thật (dán vào `jwt.io` đọc được payload).
- [ ] `POST /api/auth/login` với sai mật khẩu trả `401`.
- [ ] `POST /api/auth/register` tạo user mới + trả JWT; email trùng → `409`.
- [ ] `POST /api/orders` **không có** `Authorization: Bearer` trả `401` (Guard hoạt động).
- [ ] `POST /api/orders` **có** Token hợp lệ: tạo đơn `PENDING`, tự tính lại tổng tiền, từ chối `total` gian lận bằng `400`.
- [ ] `GET /api/orders` (có JWT) chỉ trả đơn của user; `GET /api/orders/:id` chi tiết hóa đơn; `POST …/pay` → `PAID`.
- [ ] Restart Server xong đơn **vẫn còn** (Prisma + SQLite).
- [ ] `POST /api/ai/chat` trả `{ reply }`, Key chỉ nằm trong `.env` phía Server.
- [ ] Swagger chạy tại `/api/docs`, đủ nhóm Auth/Products/Orders/Ai, nút "Authorize" hoạt động; `.env.example` đã được commit, `.env` và `prisma/dev.db` thì không.
- [ ] `main.ts` có đủ: `enableCors()`, `useGlobalPipes(ValidationPipe)`, `listen(3000, '0.0.0.0')`.

**Mobile `ShopAI`:**
- [ ] Chỉ có **duy nhất một nơi** khai báo địa chỉ Server: `src/constants/api.ts`; `axiosClient.baseURL` đã trỏ đúng `API_BASE_URL`.
- [ ] `LoginScreen` gọi `POST /api/auth/login` thật; `RegisterScreen` gọi `POST /api/auth/register` thật — không còn `mock_token_123`.
- [ ] `HomeScreen` fetch sản phẩm thật, vẫn qua trạm kiểm soát Zod.
- [ ] `ProductDetailScreen` fetch theo `id` từ Server, xử lý được trường hợp `404`.
- [ ] `CheckoutScreen` gọi `POST /api/orders` qua `axiosClient`, hiển thị mã đơn `PENDING`, **chỉ xóa giỏ khi thành công**.
- [ ] Tab Đơn hàng + Chi tiết HĐ lấy từ Nest; nút Pay gọi `POST …/pay` → `PAID`.
- [ ] `AIChatScreen` không còn import `@google/generative-ai`; file `geminiConfig.ts` đã bị xóa.
### 🧯 Sổ tay gỡ lỗi Sprint 9 — các lỗi hay gặp nhất

| Triệu chứng | Nguyên nhân thường gặp | Cách xử lý |
|---|---|---|
| `Network request failed` trên điện thoại thật | Dùng `localhost` thay vì IP LAN, hoặc Server chưa `listen('0.0.0.0')` | Xem lại Phần 9.4 + Bước 7; bật chấm Health ở Bước 12 để chẩn đoán nhanh |
| `Nest can't resolve dependencies of the OrderService` | Quên `exports: [ProductService]` trong `ProductModule` | Xem lại Bước 7f.5 |
| `POST /api/orders` luôn trả `400` dù dữ liệu đúng | `forbidNonWhitelisted: true` đang chặn field lạ Mobile gửi thừa | Chỉ gửi đúng `items` + `total`, không gửi cả object sản phẩm |
| Validation trong `items[]` không chạy | Thiếu `@Type(() => OrderItemDto)` | Xem cảnh báo ở Bước 7f.1 |
| Chi tiết sản phẩm luôn `404` | Bản `getAllProducts` cũ sinh lại mảng mỗi lần gọi → id không ổn định | Chuyển mảng thành `private readonly products` như Bước 7c |
| Swagger mở ra trắng trang | `SwaggerModule.setup` đặt **sau** `app.listen()` | Đưa lên trước dòng `listen` |
| `POST /api/orders` luôn trả `401` dù đã đăng nhập | `LoginScreen` (Bước 9d) chưa đổi từ `login('mock_token_123')`, hoặc `axiosClient.baseURL` (Bước 8) chưa trỏ đúng `API_BASE_URL` nên Token không lấy được | Kiểm tra `useAuthStore` bằng `console.log`, xác nhận `token` là chuỗi JWT dài (3 đoạn cách nhau dấu chấm) chứ không phải `mock_token_123` |
| `PrismaClientKnownRequestError: Unique constraint failed on the fields: (email)` | Seed script chạy 2 lần với `create` thay vì `upsert` | Dùng `prisma.user.upsert(...)` như Bước 7d.6, hoặc xoá `prisma/dev.db` rồi `migrate dev` lại |
| `npx prisma migrate dev` báo lỗi không đọc được `DATABASE_URL` | Thiếu file `.env` hoặc gõ sai định dạng `file:./dev.db` | Xem lại Bước 7d.2, đảm bảo `.env` nằm đúng thư mục gốc `shopai-backend` |
| Đăng nhập đúng mật khẩu vẫn báo lỗi | Seed User chưa chạy (`npx prisma db seed`), Database rỗng chưa có User nào | Chạy lại Bước 7d.6, kiểm tra bằng `npx prisma studio` |

---

> [!NOTE]
> **Nâng cấp tương lai — Endpoint Streaming (liên hệ Phần 8.4):** Ở Chương 8 ta đã học khái niệm AI Streaming (trả từng "token" chữ một, giống ChatGPT) — xu hướng 2025+. Nếu muốn nâng `POST /api/ai/chat` hiện tại (one-shot) lên Streaming, NestJS hỗ trợ sẵn decorator `@Sse()` (Server-Sent Events, trả về `Observable`) hoặc set `Content-Type: text/event-stream` viết tay qua `@Res()`. Đây là kiến thức **nâng cao, không bắt buộc trong Yêu cầu Nghiệm thu Sprint 9** — ShopAI vẫn dùng one-shot `{ reply }` cho đơn giản và ổn định với System Prompt trả lời ngắn.

### PHẦN TÙY CHỌN: HEALTH CHECK — GIÚP MOBILE BIẾT "SERVER ONLINE"

Bước này **không bắt buộc** trong Yêu cầu Nghiệm thu, nhưng cực kỳ hữu ích để debug cái bẫy mạng LAN đã học ở Phần 9.4 — một chấm tròn xanh/đỏ trên `HomeScreen` giúp học viên biết ngay Server có "sống" hay không, thay vì đoán mò tại sao danh sách sản phẩm mãi không tải được.

#### Bước 11 (tùy chọn): Tạo `HealthController` ở Backend
Endpoint này quá đơn giản để cần cả một Module riêng — sinh trực tiếp 1 Controller độc lập ngay tại `src/`:
```bash
nest g controller health --flat --no-spec
```
Mở `src/health.controller.ts`:
```typescript
import { Controller, Get } from '@nestjs/common';

@Controller('api/health')
export class HealthController {
  @Get()
  check() {
    // Trả về nhanh, không đụng Database/Gemini — chỉ để xác nhận Server đang "thức"
    return { status: 'ok', timestamp: new Date().toISOString() };
  }
}
```
Đăng ký vào `src/app.module.ts` (chỉ **thêm**, giữ nguyên `imports` cũ từ Bước 6):
```typescript
import { HealthController } from './health.controller'; // ➕ MỚI

@Module({
  imports: [ConfigModule.forRoot({ isGlobal: true }), ProductModule, AiModule],
  controllers: [HealthController], // ➕ MỚI — AppModule vốn không có controllers riêng, giờ thêm 1 cái
})
export class AppModule {}
```

#### Bước 12 (tùy chọn): Vẽ chấm tròn "Server Online" ở HomeScreen
Mở `src/screens/HomeScreen.tsx`, thêm 1 `useEffect` gọi `/api/health` ngay khi màn hình vừa mount, lưu kết quả vào 1 state cờ nhỏ (không đụng gì đến `useQuery` sản phẩm đã có):
```tsx
const [isServerOnline, setIsServerOnline] = useState<boolean | null>(null);

useEffect(() => {
  fetch(`${API_BASE_URL}/api/health`) // Dùng đúng API_BASE_URL — nguồn sự thật duy nhất cho IP LAN
    .then((res) => setIsServerOnline(res.ok))
    .catch(() => setIsServerOnline(false));
}, []);
```
Rồi vẽ 1 chấm tròn nhỏ cạnh tiêu đề Header:
```tsx
<View
  style={{
    width: 10,
    height: 10,
    borderRadius: 5,
    backgroundColor: isServerOnline ? '#4CD964' : '#FF3B30', // Xanh = Online, Đỏ = Offline/sai IP
    marginLeft: 6,
  }}
/>
```

> [!TIP]
> Chấm xanh nghĩa là Server NestJS đang chạy **và** điện thoại đang gõ đúng IP LAN (Phần 9.4). Chấm đỏ báo ngay 1 trong 2 khả năng: Server chưa `npm run start:dev`, hoặc `API_BASE_URL` đang trỏ sai IP (thường do đổi mạng Wifi) — tiết kiệm rất nhiều thời gian debug so với việc ngồi đoán tại sao `HomeScreen` cứ treo mãi ở trạng thái Loading.

---

## 🎯 CHUẨN BỊ CHO CHƯƠNG 10
App đã chạy hoàn hảo và bảo mật đã được khép kín! Nhưng làm sao để đưa nó đến tay hàng triệu người dùng? Nếu App lỡ bị lỗi Văng app (Crash) trên máy khách hàng ở xa thì làm sao ta biết dòng code nào gây lỗi? 
Làm sao để sửa lỗi giao diện và cập nhật tới khách hàng trong 5 giây mà không cần lạy lục Apple/Google duyệt app mất 2 ngày?
Chương 10 sẽ mở khóa quyền năng DevOps: **Bắn cập nhật qua mây (OTA với EAS Update) và Bẫy lỗi Crashlytics.**
