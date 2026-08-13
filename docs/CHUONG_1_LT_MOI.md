---
sidebar_position: 1
title: Chương 1
---

# GIÁO TRÌNH LÝ THUYẾT & THỰC CHIẾN
## CHƯƠNG 1: CÔNG CỤ, MÔI TRƯỜNG & KHỞI TẠO DỰ ÁN SHOPAI
**Thời lượng:** 3–4 tiết (Công cụ + Môi trường + Chạy được app)
**Ánh xạ đề cương chính thức:** Chương 1 mục **1.1.1 → 1.1.5** — xem `BAN_DO_DE_CUONG.md`

---

> [!IMPORTANT]
> **Thực hành chương = Sprint ShopAI cuối file.** Hoàn thành Sprint này để đạt mục tiêu chương. Hoàn thành đủ 11 chương theo `SHOPAI_HOAN_THIEN.md` = sản phẩm ShopAI **hoàn thiện đẳng cấp**.

## 📚 MỤC TIÊU HỌC TẬP

Sau khi hoàn thành chương này, học viên **từ số 0** sẽ:
- ✅ Biết dùng **Terminal, Git, Node.js/npm** đủ để chạy lệnh React Native
- ✅ Cài và dùng **Cursor / VS Code** (đề cương 1.1.5)
- ✅ Hiểu **React Native là gì**, khác React Web chỗ nào (đề cương 1.1.1–1.1.2)
- ✅ Phân biệt **Expo CLI** và **React Native CLI**, biết vì sao khóa học dùng CLI (1.1.3)
- ✅ Có hình dung **kiến trúc RN mức nhập môn** (1.1.4)
- ✅ Thiết lập môi trường build (JDK, Android Studio / Xcode)
- ✅ **Thực chiến:** `init` dự án ShopAI, chạy lên Simulator/Emulator, push GitHub

---

## 🗺️ LỘ TRÌNH CHƯƠNG NÀY (ĐỌC TRƯỚC KHI HỌC)

```
Bước A — Công cụ nền (nếu chưa biết): Terminal → Git → Node/npm → Editor
Bước B — Lý thuyết ngắn đề cương 1.1: RN là gì? vs React? Expo vs CLI? Kiến trúc sơ bộ?
Bước C — Cài môi trường build (Xcode / Android Studio)  ← BẮT BUỘC trước khi chạy app
Bước D — Sprint ShopAI: init project → chạy được → commit GitHub
```

> [!TIP]
> Nếu bạn **đã biết** Terminal/Git/Node, đọc lướt **Phần 0**, tập trung **Phần 1.1 + Phần 1.5** rồi làm Sprint.

---

## 🎯 TẠI SAO CẦN HỌC CHƯƠNG NÀY?

Không có Chương 1, bạn sẽ kẹt ở lỗi môi trường (`sdk not found`, `pod install`, JDK sai…) và không chạy được app.

**ShopAI bắt đầu từ đây:** một repo chạy được trên máy ảo. Các chương sau mới thêm màn hình, giỏ hàng, API, camera…

---

# ═══════════════════════════════════════
# PHẦN 0 — KIẾN THỨC NỀN (CÔNG CỤ)
# ═══════════════════════════════════════

> Phần này **không nằm trong đề cương chữ**, nhưng **bắt buộc** với người học từ số 0. Không biết Terminal/Git/npm thì không làm được React Native.

---

## PHẦN 0.1: TERMINAL COMMANDS CƠ BẢN

---

### **0.1.1. Terminal là gì?**

#### **A. Định nghĩa**

**Terminal** (hay **Command Line**, **CLI - Command Line Interface**) là một giao diện dòng lệnh cho phép bạn tương tác với máy tính bằng cách gõ các lệnh thay vì sử dụng chuột.

#### **B. Tại sao cần Terminal?**

**1. Nhanh hơn GUI:**
- Thực hiện nhiều thao tác chỉ bằng vài lệnh
- Không cần click chuột nhiều lần

**2. Tự động hóa:**
- Có thể viết script để tự động hóa các tác vụ
- Chạy nhiều lệnh liên tiếp

**3. Bắt buộc cho lập trình:**
- Nhiều công cụ chỉ có CLI (không có GUI)
- React Native CLI, npm, Git đều chạy qua Terminal

#### **C. Terminal trên các hệ điều hành**

| Hệ điều hành | Terminal mặc định | Cách mở |
|--------------|-------------------|---------|
| **macOS** | Terminal.app | `Cmd + Space` → gõ "Terminal" |
| **Windows** | Command Prompt hoặc PowerShell | `Win + R` → gõ "cmd" hoặc "powershell" |
| **Linux** | Terminal | `Ctrl + Alt + T` |

**Lưu ý:** Trên Windows, khuyến nghị dùng **PowerShell** hoặc **Git Bash** (cài cùng Git) thay vì Command Prompt.

---

### **0.1.2. Các lệnh Terminal cơ bản**

#### **A. Navigation (Di chuyển)**

##### **1. `pwd` - Print Working Directory**
**Mục đích:** Xem thư mục hiện tại bạn đang ở đâu

**Ví dụ:**
```bash
$ pwd
/Users/webmedia/Documents/LTDD_REACT_NATIVE
```

**Giải thích:** Lệnh này trả về đường dẫn đầy đủ của thư mục hiện tại.

---

##### **2. `ls` - List (Liệt kê)**
**Mục đích:** Xem các file và thư mục trong thư mục hiện tại

**Cú pháp:**
```bash
ls [options] [path]
```

**Ví dụ:**
```bash
# Liệt kê file và thư mục
$ ls
LY-THUYET  THUC-HANH  DE_CUONG_DA_DIEU_CHINH_THOI_GIAN.md

# Liệt kê chi tiết (long format)
$ ls -l
total 48
drwxr-xr-x  5 user  staff  160 Jan 15 10:00 LY-THUYET
drwxr-xr-x  5 user  staff  160 Jan 15 10:00 THUC-HANH
-rw-r--r--  1 user  staff  859 Jan 15 10:00 DE_CUONG_DA_DIEU_CHINH_THOI_GIAN.md

# Liệt kê tất cả (kể cả file ẩn)
$ ls -a
.  ..  .git  LY-THUYET  THUC-HANH  DE_CUONG_DA_DIEU_CHINH_THOI_GIAN.md
```

**Giải thích:**
- `-l`: Long format, hiển thị chi tiết (quyền, owner, size, ngày)
- `-a`: All, hiển thị cả file ẩn (bắt đầu bằng dấu `.`)

**Lưu ý:** Trên Windows PowerShell, dùng `dir` thay vì `ls` (hoặc dùng Git Bash).

---

##### **3. `cd` - Change Directory (Đổi thư mục)**
**Mục đích:** Di chuyển đến thư mục khác

**Cú pháp:**
```bash
cd [path]
```

**Ví dụ:**
```bash
# Di chuyển vào thư mục
$ cd LY-THUYET
$ pwd
/Users/webmedia/Documents/LTDD_REACT_NATIVE/LY-THUYET

# Di chuyển lên thư mục cha
$ cd ..
$ pwd
/Users/webmedia/Documents/LTDD_REACT_NATIVE

# Di chuyển về thư mục home
$ cd ~
# hoặc
$ cd

# Di chuyển đến thư mục tuyệt đối
$ cd /Users/webmedia/Documents
```

**Các ký hiệu đặc biệt:**
- `.` : Thư mục hiện tại
- `..` : Thư mục cha
- `~` : Thư mục home của user
- `/` : Thư mục gốc (root)

**Lưu ý:** Trên Windows, dùng `\` thay vì `/` (hoặc dùng Git Bash để dùng `/`).

---

#### **B. File Operations (Thao tác với file)**

##### **4. `mkdir` - Make Directory (Tạo thư mục)**
**Mục đích:** Tạo thư mục mới

**Cú pháp:**
```bash
mkdir [options] directory_name
```

**Ví dụ:**
```bash
# Tạo một thư mục
$ mkdir my-project

# Tạo nhiều thư mục cùng lúc
$ mkdir folder1 folder2 folder3

# Tạo thư mục lồng nhau (nếu thư mục cha chưa tồn tại)
$ mkdir -p parent/child/grandchild
```

**Giải thích:**
- `-p`: Tạo cả thư mục cha nếu chưa tồn tại (parent)

---

##### **5. `touch` - Tạo file rỗng**
**Mục đích:** Tạo một file mới (rỗng) hoặc cập nhật thời gian sửa đổi

**Cú pháp:**
```bash
touch filename
```

**Ví dụ:**
```bash
# Tạo file mới
$ touch README.md

# Tạo nhiều file cùng lúc
$ touch file1.txt file2.txt file3.txt
```

**Lưu ý:** Trên Windows, không có lệnh `touch`. Dùng:
```powershell
# PowerShell
New-Item -ItemType File -Name "README.md"
# hoặc
echo $null > README.md
```

---

##### **6. `rm` - Remove (Xóa)**
**Mục đích:** Xóa file hoặc thư mục

**Cú pháp:**
```bash
rm [options] file_or_directory
```

**Ví dụ:**
```bash
# Xóa file
$ rm file.txt

# Xóa nhiều file
$ rm file1.txt file2.txt file3.txt

# Xóa thư mục và nội dung bên trong (recursive)
$ rm -r folder

# Xóa thư mục (force, không hỏi)
$ rm -rf folder
```

**Giải thích:**
- `-r`: Recursive, xóa cả thư mục và nội dung bên trong
- `-f`: Force, không hỏi xác nhận

**⚠️ CẢNH BÁO:** Lệnh `rm -rf` rất nguy hiểm! Một khi xóa, không thể khôi phục. Luôn kiểm tra kỹ trước khi chạy.

**Lưu ý:** Trên Windows, dùng `del` (file) hoặc `rmdir` (thư mục).

---

##### **7. `cp` - Copy (Sao chép)**
**Mục đích:** Sao chép file hoặc thư mục

**Cú pháp:**
```bash
cp [options] source destination
```

**Ví dụ:**
```bash
# Sao chép file
$ cp file.txt file-backup.txt

# Sao chép thư mục (recursive)
$ cp -r folder1 folder2

# Sao chép nhiều file vào một thư mục
$ cp file1.txt file2.txt destination/
```

**Giải thích:**
- `-r`: Recursive, sao chép cả thư mục và nội dung

---

##### **8. `mv` - Move (Di chuyển/Đổi tên)**
**Mục đích:** Di chuyển file/thư mục hoặc đổi tên

**Cú pháp:**
```bash
mv source destination
```

**Ví dụ:**
```bash
# Đổi tên file
$ mv old-name.txt new-name.txt

# Di chuyển file vào thư mục
$ mv file.txt folder/

# Di chuyển và đổi tên cùng lúc
$ mv old-name.txt folder/new-name.txt
```

---

#### **C. Xem nội dung file**

##### **9. `cat` - Concatenate (Hiển thị nội dung)**
**Mục đích:** Hiển thị toàn bộ nội dung file

**Cú pháp:**
```bash
cat filename
```

**Ví dụ:**
```bash
$ cat README.md
# My Project
This is a React Native project.
```

**Lưu ý:** Chỉ dùng cho file nhỏ. Với file lớn, dùng `less` hoặc `more`.

---

##### **10. `less` / `more` - Xem file từng trang**
**Mục đích:** Xem file lớn từng trang một

**Cú pháp:**
```bash
less filename
# hoặc
more filename
```

**Các phím điều khiển:**
- `Space`: Trang tiếp theo
- `b`: Trang trước
- `q`: Thoát
- `/text`: Tìm kiếm

---

### **0.1.3. Tổng kết các lệnh Terminal cơ bản**

| Lệnh | Mục đích | Ví dụ |
|------|----------|-------|
| `pwd` | Xem thư mục hiện tại | `pwd` |
| `ls` | Liệt kê file/thư mục | `ls -la` |
| `cd` | Đổi thư mục | `cd folder` |
| `mkdir` | Tạo thư mục | `mkdir my-project` |
| `touch` | Tạo file | `touch file.txt` |
| `rm` | Xóa file/thư mục | `rm -rf folder` |
| `cp` | Sao chép | `cp file.txt backup.txt` |
| `mv` | Di chuyển/Đổi tên | `mv old.txt new.txt` |
| `cat` | Hiển thị nội dung | `cat file.txt` |

---

## PHẦN 0.2: GIT BASICS (20 phút)

---

### **0.2.1. Git là gì?**

#### **A. Định nghĩa**

**Git** là một hệ thống quản lý phiên bản phân tán (Distributed Version Control System - DVCS) được phát triển bởi Linus Torvalds.

#### **B. Tại sao cần Git?**

**1. Quản lý phiên bản:**
- Lưu lại lịch sử thay đổi code
- Có thể quay lại phiên bản cũ bất kỳ lúc nào
- Xem ai đã thay đổi gì, khi nào

**2. Làm việc nhóm:**
- Nhiều người có thể làm việc trên cùng một project
- Merge code từ nhiều người
- Giải quyết conflict khi có xung đột

**3. Backup và an toàn:**
- Code được lưu trên server (GitHub, GitLab)
- Không sợ mất code khi máy tính hỏng

**4. Branching:**
- Tạo các nhánh để phát triển tính năng mới
- Không ảnh hưởng đến code chính

#### **C. Git vs GitHub**

| Git | GitHub |
|-----|--------|
| **Công cụ** quản lý phiên bản | **Dịch vụ** lưu trữ Git trên cloud |
| Chạy trên máy tính của bạn | Website để lưu code online |
| Miễn phí, mã nguồn mở | Miễn phí cho public repo, có phí cho private |

**Tương tự:** Git = Word, GitHub = Google Docs

---

### **0.2.2. Cài đặt Git**

#### **A. Kiểm tra Git đã cài chưa**

```bash
$ git --version
git version 2.39.0
```

Nếu hiển thị version, Git đã được cài đặt.

#### **B. Cài đặt Git**

**macOS:**
```bash
# Dùng Homebrew (khuyến nghị)
$ brew install git

# Hoặc tải từ: https://git-scm.com/download/mac
```

**Windows:**
- Tải từ: https://git-scm.com/download/win
- Cài đặt với Git Bash (khuyến nghị)

**Linux:**
```bash
# Ubuntu/Debian
$ sudo apt-get install git

# Fedora
$ sudo dnf install git
```

#### **C. Cấu hình Git lần đầu**

```bash
# Cấu hình tên
$ git config --global user.name "Your Name"

# Cấu hình email
$ git config --global user.email "your.email@example.com"

# Kiểm tra cấu hình
$ git config --list
```

**Lưu ý:** Email này sẽ được dùng cho mọi commit. Nên dùng email GitHub/GitLab của bạn.

---

### **0.2.3. Các lệnh Git cơ bản**

#### **A. Khởi tạo Repository**

##### **1. `git init` - Khởi tạo repo mới**

**Mục đích:** Tạo một Git repository mới trong thư mục hiện tại

**Cú pháp:**
```bash
git init
```

**Ví dụ:**
```bash
$ mkdir my-project
$ cd my-project
$ git init
Initialized empty Git repository in /Users/webmedia/my-project/.git
```

**Giải thích:**
- Tạo thư mục `.git` (ẩn) để lưu trữ thông tin Git
- Thư mục hiện tại trở thành Git repository

---

##### **2. `git clone` - Clone repository từ remote**

**Mục đích:** Tải một repository từ GitHub/GitLab về máy

**Cú pháp:**
```bash
git clone [url]
```

**Ví dụ:**
```bash
# Clone repository công khai
$ git clone https://github.com/facebook/react-native.git

# Clone vào thư mục với tên khác
$ git clone https://github.com/facebook/react-native.git my-react-native
```

**Giải thích:**
- Tải toàn bộ code và lịch sử về máy
- Tự động tạo thư mục với tên repository

---

#### **B. Kiểm tra trạng thái**

##### **3. `git status` - Xem trạng thái**

**Mục đích:** Xem file nào đã thay đổi, file nào đã được stage

**Cú pháp:**
```bash
git status
```

**Ví dụ:**
```bash
$ git status
On branch main
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   README.md

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        new-file.txt

no changes added to commit (use "git add" and/or "git commit -a")
```

**Giải thích:**
- **Changes not staged:** File đã thay đổi nhưng chưa được stage
- **Untracked files:** File mới chưa được Git theo dõi
- **Changes to be committed:** File đã được stage, sẵn sàng commit

---

#### **C. Thêm file vào staging area**

##### **4. `git add` - Thêm file vào staging**

**Mục đích:** Thêm file vào staging area (chuẩn bị commit)

**Cú pháp:**
```bash
git add [file]
# hoặc
git add .
```

**Ví dụ:**
```bash
# Thêm một file
$ git add README.md

# Thêm nhiều file
$ git add file1.txt file2.txt

# Thêm tất cả file đã thay đổi
$ git add .

# Thêm tất cả file (kể cả file đã xóa)
$ git add -A
```

**Giải thích:**
- `git add .`: Thêm tất cả file trong thư mục hiện tại
- `git add -A`: Thêm tất cả file trong toàn bộ repository

**Lưu ý:** Sau khi `git add`, file vẫn chưa được lưu vào Git. Cần `git commit` để lưu.

---

#### **D. Commit (Lưu thay đổi)**

##### **5. `git commit` - Lưu thay đổi**

**Mục đích:** Lưu các thay đổi đã được stage vào Git repository

**Cú pháp:**
```bash
git commit -m "commit message"
```

**Ví dụ:**
```bash
$ git commit -m "Add README file"
[main abc1234] Add README file
 1 file changed, 5 insertions(+)
```

**Giải thích:**
- `-m`: Message, thông điệp mô tả thay đổi
- Mỗi commit có một hash (abc1234) để định danh

**Quy tắc viết commit message tốt:**
- Ngắn gọn, rõ ràng (dưới 50 ký tự)
- Dùng động từ: "Add", "Fix", "Update", "Remove"
- Ví dụ tốt: "Add login feature", "Fix button color bug"
- Ví dụ xấu: "update", "fix", "changes"

---

#### **E. Xem lịch sử**

##### **6. `git log` - Xem lịch sử commit**

**Mục đích:** Xem danh sách các commit đã thực hiện

**Cú pháp:**
```bash
git log
```

**Ví dụ:**
```bash
$ git log
commit abc1234def5678 (HEAD -> main)
Author: Your Name <your.email@example.com>
Date:   Mon Jan 15 10:00:00 2024 +0700

    Add README file

commit 9876543fedcba0
Author: Your Name <your.email@example.com>
Date:   Sun Jan 14 09:00:00 2024 +0700

    Initial commit
```

**Các tùy chọn hữu ích:**
```bash
# Xem ngắn gọn (một dòng)
$ git log --oneline

# Xem với graph
$ git log --graph --oneline

# Xem chỉ n commit gần nhất
$ git log -n 5
```

---

#### **F. Làm việc với Remote Repository**

##### **7. `git remote` - Quản lý remote repository**

**Mục đích:** Xem và quản lý các remote repository (GitHub, GitLab)

**Cú pháp:**
```bash
# Xem danh sách remote
git remote -v

# Thêm remote
git remote add origin [url]

# Xóa remote
git remote remove origin
```

**Ví dụ:**
```bash
$ git remote -v
origin  https://github.com/username/my-project.git (fetch)
origin  https://github.com/username/my-project.git (push)
```

**Giải thích:**
- `origin`: Tên mặc định của remote repository
- `fetch`: Lấy code từ remote
- `push`: Đẩy code lên remote

---

##### **8. `git push` - Đẩy code lên remote**

**Mục đích:** Gửi các commit lên remote repository (GitHub, GitLab)

**Cú pháp:**
```bash
git push [remote] [branch]
```

**Ví dụ:**
```bash
# Đẩy lên origin, branch main
$ git push origin main

# Lần đầu tiên, set upstream
$ git push -u origin main
```

**Giải thích:**
- `-u`: Set upstream, lần sau chỉ cần `git push`
- Cần có quyền truy cập vào repository

**Lưu ý:** Lần đầu push, có thể cần đăng nhập GitHub/GitLab.

---

##### **9. `git pull` - Lấy code từ remote**

**Mục đích:** Lấy code mới nhất từ remote repository về máy

**Cú pháp:**
```bash
git pull [remote] [branch]
```

**Ví dụ:**
```bash
# Lấy code từ origin, branch main
$ git pull origin main

# Hoặc đơn giản (nếu đã set upstream)
$ git pull
```

**Giải thích:**
- Tự động merge code từ remote vào local
- Nếu có conflict, cần giải quyết thủ công

---

### **0.2.4. Git Branching (Làm việc với nhánh)**
> [!IMPORTANT]
> **Đây là kỹ năng bắt buộc khi đi làm.** Bạn sẽ không bao giờ code trực tiếp trên nhánh `main` mà phải tạo nhánh riêng (feature branch).

#### **A. Các lệnh cơ bản**

##### **10. `git branch` - Quản lý nhánh**
- **Xem danh sách nhánh:**
  ```bash
  $ git branch
  * main
  ```
- **Tạo nhánh mới:**
  ```bash
  $ git branch feature-login
  ```

##### **11. `git checkout` - Chuyển nhánh**
- **Chuyển sang nhánh khác:**
  ```bash
  $ git checkout feature-login
  ```
- **Tạo và chuyển luôn sang nhánh mới (thường dùng nhất):**
  ```bash
  $ git checkout -b feature-signup
  ```

##### **12. `git merge` - Gộp nhánh**
Sau khi code xong ở nhánh `feature-login`, bạn cần gộp nó về `main`.
```bash
# 1. Chuyển về nhánh main
$ git checkout main

# 2. Cập nhật code mới nhất từ server (luôn nhớ bước này!)
$ git pull origin main

# 3. Merge nhánh feature vào main
$ git merge feature-login
```

---

### **0.2.5. Workflow Git cơ bản (Flow đi làm)**

#### **A. Quy trình chuẩn**

```
1. git checkout -b feature/new-feature  (Tạo nhánh mới)
   ↓
2. Code... (Sửa file, tạo file)
   ↓
3. git add .
   ↓
4. git commit -m "Add new feature"
   ↓
5. git push origin feature/new-feature  (Đẩy nhánh lên GitHub)
   ↓
6. Tạo Pull Request (trên Web GitHub) để sếp review và merge
```

#### **B. Ví dụ thực tế**

```bash
# 1. Tạo file mới
$ echo "# My Project" > README.md

# 2. Kiểm tra trạng thái
$ git status
Untracked files: README.md

# 3. Thêm vào staging
$ git add README.md

# 4. Commit
$ git commit -m "Add README file"

# 5. Push lên GitHub
$ git push origin main
```

---

## PHẦN 0.3: NODE.JS & NPM BASICS (15 phút)

---

### **0.3.1. Node.js là gì?**

#### **A. Định nghĩa**

**Node.js** là một runtime environment cho phép chạy JavaScript trên server (ngoài trình duyệt).

#### **B. Tại sao cần Node.js cho React Native?**

**1. React Native CLI chạy trên Node.js:**
- Các lệnh như `npx react-native init` cần Node.js
- Build tools, bundlers đều chạy trên Node.js

**2. Package Manager (npm/yarn):**
- Cài đặt các thư viện (packages) cho project
- Quản lý dependencies

**3. Development Server:**
- Metro bundler (React Native bundler) chạy trên Node.js
- Hot reload, debugging tools

#### **C. Node.js vs JavaScript**

| JavaScript | Node.js |
|------------|---------|
| Ngôn ngữ lập trình | Runtime environment |
| Chạy trên trình duyệt | Chạy trên server/máy tính |
| Có DOM, window object | Không có DOM, có global, process |

---

### **0.3.2. Cài đặt Node.js**

#### **A. Kiểm tra Node.js đã cài chưa**

```bash
$ node --version
v18.17.0

$ npm --version
9.6.7
```

Nếu hiển thị version, Node.js đã được cài đặt.

#### **B. Cài đặt Node.js**

**Khuyến nghị:** Dùng **nvm** (Node Version Manager) để quản lý nhiều phiên bản Node.js.

**macOS/Linux:**
```bash
# Cài nvm
$ curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Cài Node.js LTS (Long Term Support)
$ nvm install --lts
$ nvm use --lts
```

**Windows:**
- Tải từ: https://nodejs.org/
- Chọn phiên bản LTS (khuyến nghị)

**Hoặc dùng nvm-windows:**
- Tải từ: https://github.com/coreybutler/nvm-windows/releases

#### **C. Chọn phiên bản Node.js**

**Khuyến nghị:** Dùng **LTS (Long Term Support)** version
- Ổn định hơn
- Được hỗ trợ lâu dài
- Tương thích tốt với React Native

**Kiểm tra phiên bản tương thích:**
- **Khuyến nghị tối thiểu: Node.js 20 LTS.** Đây là bản khóa học dùng làm chuẩn.
- Node.js >= 18 nhiều lúc vẫn chạy được, nhưng các bản React Native mới hơn có thể yêu cầu Node 20+.
- **Luôn kiểm tra tài liệu chính thức React Native** (mục "Environment Setup") để biết yêu cầu Node mới nhất tại thời điểm bạn học, vì con số này thay đổi theo từng release RN.

---

### **0.3.3. NPM (Node Package Manager)**

#### **A. NPM là gì?**

**NPM** là package manager mặc định của Node.js, dùng để:
- Cài đặt các thư viện (packages)
- Quản lý dependencies
- Chạy scripts

#### **B. Các lệnh NPM cơ bản**

##### **1. `npm install` - Cài đặt package**

**Cú pháp:**
```bash
# Cài package vào project
npm install [package-name]

# Cài package global
npm install -g [package-name]

# Cài tất cả dependencies từ package.json
npm install
```

> [!WARNING]
> Package `react-native-cli` đã **deprecated** (ngừng phát triển) từ lâu và cài global dễ gây lỗi xung đột phiên bản. **KHÔNG** cài nó nữa. React Native chính thức khuyến nghị dùng thẳng `npx` với package theo từng lệnh — không cần cài gì global:
> ```bash
> # ĐÚNG — dùng npx, không cần cài global
> npx @react-native-community/cli@latest init ShopAI
> ```

**Ví dụ (các lệnh npm install khác vẫn dùng bình thường):**
```bash
# Cài package vào project
$ npm install axios

# Cài package với version cụ thể
$ npm install axios@1.0.0

# Cài package dev dependency
$ npm install --save-dev jest
```

**Giải thích:**
- `-g`: Global, cài vào hệ thống (dùng cho CLI tools)
- `--save-dev`: Dev dependency, chỉ cần khi development

---

##### **2. `npm init` - Khởi tạo package.json**

**Mục đích:** Tạo file `package.json` (mô tả project và dependencies)

**Cú pháp:**
```bash
npm init
# hoặc
npm init -y  # Tự động điền mặc định
```

**Ví dụ:**
```bash
$ npm init -y
{
  "name": "my-project",
  "version": "1.0.0",
  "description": "",
  "main": "index.js",
  "scripts": {
    "test": "echo \"Error: no test specified\" && exit 1"
  },
  "keywords": [],
  "author": "",
  "license": "ISC"
}
```

**Giải thích:**
- `package.json`: File mô tả project, dependencies, scripts
- Tự động tạo khi chạy `npm install` lần đầu

---

##### **3. `package.json` - File cấu hình**

**Cấu trúc cơ bản:**
```json
{
  "name": "my-project",
  "version": "1.0.0",
  "scripts": {
    "start": "react-native start",
    "android": "react-native run-android",
    "ios": "react-native run-ios"
  },
  "dependencies": {
    "react": "18.2.0",
    "react-native": "0.72.0"
  },
  "devDependencies": {
    "jest": "29.0.0"
  }
}
```

**Giải thích:**
- `name`: Tên project
- `version`: Phiên bản
- `scripts`: Các lệnh có thể chạy với `npm run`
- `dependencies`: Packages cần khi chạy app
- `devDependencies`: Packages chỉ cần khi development

---

##### **4. `npm run` - Chạy script**

**Cú pháp:**
```bash
npm run [script-name]
```

**Ví dụ:**
```bash
# Chạy script "start"
$ npm run start

# Hoặc viết tắt (nếu tên là start, test, etc.)
$ npm start
```

---

##### **5. `npm uninstall` - Gỡ package**

**Cú pháp:**
```bash
npm uninstall [package-name]
```

**Ví dụ:**
```bash
$ npm uninstall axios
```

---

### **0.3.4. Yarn vs NPM**

| NPM | Yarn |
|-----|------|
| Package manager mặc định của Node.js | Package manager của Facebook |
| Chậm hơn một chút | Nhanh hơn (caching tốt) |
| `npm install` | `yarn install` |
| `npm install package` | `yarn add package` |

**Khuyến nghị:** Dùng **NPM** (đủ cho React Native). Yarn là optional.

---

## PHẦN 0.4: EDITOR — CURSOR / VS CODE & AI PAIR-PROGRAMMING

> **Đề cương 1.1.5:** Môi trường phát triển Visual Studio Code. Khóa học dùng **Cursor** (fork của VS Code, phím tắt/extension tương thích 100%). Bạn có thể dùng VS Code thuần nếu muốn. (20 phút)

---

### **0.4.1. Tại sao lại là Cursor? (và quan hệ với VS Code)**

Trong môn học này, chúng ta KHÔNG sử dụng VS Code truyền thống. Kỷ nguyên AI đã đến, chúng ta sẽ sử dụng **Cursor IDE** (một bản sao của VS Code nhưng được nhúng AI thông minh nhất hiện nay - Claude 3.5 Sonnet / GPT-4o).

**Vì sao dùng Cursor?**
- Giao diện, phím tắt, extension y hệt VS Code (Bạn ra trường dùng VS Code công ty vẫn không bỡ ngỡ).
- AI tích hợp siêu sâu: Đọc hiểu lỗi, giải thích code, dự đoán dòng code tiếp theo với tốc độ chóng mặt.
- Đóng vai trò như một **Giảng viên 1-1 (Tutor)** túc trực bên bạn 24/7.

---

### **0.4.2. Cài đặt Cursor hoặc VS Code**

1. Truy cập: https://cursor.sh/
2. Tải về và cài đặt bình thường (miễn phí).
3. Đăng nhập bằng tài khoản Github/Google của bạn.

---

### **0.4.3. Luật sử dụng AI trong lớp học (QUAN TRỌNG)**

> [!WARNING]
> Sinh viên lạm dụng AI để viết hộ code (Ghostwriting) sẽ thất bại khi đi phỏng vấn. Chúng ta học cách dùng AI làm **Gia sư (Tutor)**.

❌ **CẤM HỎI NHƯ SAU (Tư duy thợ gõ):**
- *"Viết cho tôi chức năng giỏ hàng."* (AI viết ra, app chạy, nhưng bạn không hiểu một dòng chữ nào -> Vô dụng).
- *"Fix lỗi này đi: undefined is not an object."* (AI tự sửa, bạn không biết tại sao lại lỗi -> Lần sau gặp lại lỗi cũ).

✅ **CÁCH HỎI CHUẨN KỸ SƯ (Tư duy Pair-Programming):**
- Bôi đen đoạn code lỗi, nhấn `Cmd + L` (Hoặc `Ctrl + L`), hỏi: *"Tại sao biến data chỗ này lại bị lỗi undefined? Hãy giải thích nguyên nhân gây ra lỗi, khoan hãy đưa ra code sửa đổi, để tôi tự nghĩ."*
- Hỏi: *"Đoạn code Zustand này tôi không hiểu dòng số 15, hãy giải thích nó bằng ngôn ngữ dễ hiểu nhất."*
- Hỏi: *"Tôi muốn làm tính năng vuốt để xóa, tôi nên dùng thư viện nào? Hãy liệt kê ưu nhược điểm cho tôi."*

### **0.4.4. Extensions cần thiết cho React Native**

1. Mở ô Extensions trong Cursor: `Cmd + Shift + X` (macOS) hoặc `Ctrl + Shift + X` (Windows)
2. Tìm và cài các extensions sau:

**1. ESLint & Prettier:** Bộ đôi kiểm tra lỗi và tự động dàn trang code chuẩn chỉ.
**2. React Native Tools:** Hỗ trợ debug và syntax.
**3. GitLens:** Xem lịch sử Git, biết ai vừa viết dòng code gây lỗi.

---

### **0.4.5. Các phím tắt quan trọng**

#### **A. Navigation**

| Phím tắt | Chức năng |
|----------|-----------|
| `Cmd/Ctrl + P` | Tìm file nhanh |
| `Cmd/Ctrl + Shift + P` | Command Palette (tất cả lệnh) |
| `Cmd/Ctrl + B` | Ẩn/hiện sidebar |
| `Cmd/Ctrl + \` | Split editor |

#### **B. Editing**

| Phím tắt | Chức năng |
|----------|-----------|
| `Cmd/Ctrl + D` | Chọn từ tiếp theo giống nhau |
| `Alt + Up/Down` | Di chuyển dòng lên/xuống |
| `Shift + Alt + Up/Down` | Copy dòng lên/xuống |
| `Cmd/Ctrl + /` | Comment/uncomment |
| `Cmd/Ctrl + Shift + K` | Xóa dòng |

#### **C. Terminal**

| Phím tắt | Chức năng |
|----------|-----------|
| `Ctrl + `` | Mở/đóng Terminal |
| `Cmd/Ctrl + Shift + `` | Tạo Terminal mới |

---

### **0.4.6. Cấu hình cơ bản**

#### **A. Settings (Cài đặt)**

Mở Settings: `Cmd/Ctrl + ,`

**Các cài đặt khuyến nghị:**

```json
{
  // Format on save
  "editor.formatOnSave": true,
  
  // Default formatter
  "editor.defaultFormatter": "esbenp.prettier-vscode",
  
  // Tab size
  "editor.tabSize": 2,
  
  // Word wrap
  "editor.wordWrap": "on",
  
  // Auto save
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000
}
```

---


# ═══════════════════════════════════════
# PHẦN 1 — GIỚI THIỆU REACT NATIVE (Đề cương 1.1)
# ═══════════════════════════════════════

> Phần này trả lời: **RN là gì? khác Web chỗ nào? dùng Expo hay CLI?**

---

## PHẦN 1.1: GIỚI THIỆU (Đề cương 1.1)

---

### 1.1.1. React Native là gì?

**React Native (RN)** là framework mã nguồn mở do Meta (Facebook) phát triển, cho phép viết ứng dụng điện thoại **iOS và Android** bằng **JavaScript/TypeScript** và mô hình Component của React.

**Điểm then chốt học viên hay hiểu sai:**
- RN **không** phải “trang web bỏ vào WebView”.
- Khi bạn viết `<View>`, RN yêu cầu hệ điều hành tạo **UIView** (iOS) hoặc **ViewGroup** (Android) — tức là **UI Native thật**.
- Một codebase → chạy trên cả hai nền tảng (vẫn có chỗ phải chỉnh riêng iOS/Android khi đụng phần cứng).

**Vì sao ngành công nghiệp dùng RN?**
1. Tuyển dụng rộng, cộng đồng lớn, thư viện nhiều.
2. Hot Reload / Fast Refresh: sửa code → thấy ngay trên máy ảo (không build lại mỗi lần nhỏ).
3. Có thể dùng chung tư duy Component với React Web.
4. Đủ mạnh cho app thương mại (Shopify, Discord, một phần Facebook…).

**ShopAI trong khóa học:** app thương mại điện tử + chatbot AI tư vấn — đúng kiểu sản phẩm thực tế dùng RN.

---

### 1.1.2. React Native so với React (Web)

| Tiêu chí | React (Web) | React Native |
|----------|-------------|--------------|
| Chạy ở đâu | Trình duyệt | Điện thoại (iOS/Android) |
| Thẻ giao diện | `<div>`, `<span>`, `<input>` | `<View>`, `<Text>`, `<TextInput>` |
| Style | CSS file / className | Object JS + `StyleSheet` (không có CSS thuần) |
| Điều hướng | React Router (URL) | React Navigation (Stack/Tab — học Chương 5) |
| Kết quả | DOM HTML | Component Native của OS |
| Tư duy chung | Component, Hooks | **Giống** — đây là lợi thế lớn |

**Ví dụ cùng một ý tưởng UI:**

```tsx
// React Web
<div className="box"><span>Xin chào</span></div>

// React Native
<View style={styles.box}><Text>Xin chào</Text></View>
```

> Luật vàng: Trong RN, **mọi chữ phải nằm trong `<Text>`**. Viết `<View>Hello</View>` sẽ **crash app**.

---

### 1.1.3. Thiết lập môi trường: Expo CLI vs React Native CLI

Có **hai cửa** vào thế giới RN. Học viên phải hiểu trước khi cài đặt (Phần 1.5 bên dưới là cửa CLI).

#### A. Expo (Expo CLI / `npx create-expo-app`)

- **Ưu:** Cài nhanh, nhiều API sẵn (Camera, SecureStore…), ít đụng Xcode/Android Studio lúc đầu, có EAS Build.
- **Nhược:** Một số thư viện native “lạ” cần config thêm (dev client); hiểu sâu build native chậm hơn nếu chỉ dùng Expo Go.

#### B. React Native CLI (Bare Workflow) — **Khóa học này dùng**

- **Ưu:** Kiểm soát đầy đủ thư mục `ios/` và `android/`, đúng môi trường nhiều công ty dùng, dễ gắn Native Module tùy biến.
- **Nhược:** Phải cài Xcode (Mac) / Android Studio, dễ lỗi môi trường lần đầu.

| Câu hỏi | Expo | RN CLI (ShopAI) |
|---------|------|-----------------|
| Học viên mới muốn thấy UI nhanh? | Rất tốt | Chậm hơn lúc setup |
| Cần sửa native code / thư viện C++? | Hạn chế hơn (cần Dev Client) | Thuận lợi |
| Khóa ShopAI (Vision Camera, Firebase…)? | Làm được nhưng lộ trình khác | **Đúng lộ trình giáo trình** |

> [!IMPORTANT]
> **Quyết định khóa học:** ShopAI dùng **React Native CLI (TypeScript)**. Phần 1.5 hướng dẫn cài JDK, Android Studio, Xcode. Bạn vẫn nên **hiểu Expo** để đọc tài liệu cộng đồng và phỏng vấn.

**Lệnh khởi tạo (sẽ dùng trong Sprint):**
```bash
# React Native CLI (cửa chúng ta dùng)
npx @react-native-community/cli@latest init ShopAI

# Expo (chỉ để biết — không dùng làm bài chính)
npx create-expo-app@latest ShopAIExpo
```

---

### 1.1.4. Tổng quan kiến trúc React Native (mức nhập môn)

Ở Chương 1 chỉ cần hình dung **3 lớp**:

```
[ Code JS/TS của bạn: Component, logic, API ]
        ↓
[ Engine Hermes + React Native Runtime ]
        ↓
[ UI Native thật trên iOS / Android ]
```

1. **JavaScript Thread:** Chạy logic React (render, state, gọi API).
2. **Native / UI Thread:** Vẽ nút, chữ, nhận cảm ứng.
3. **Cơ chế nối hai thế giới:** phiên bản cũ dùng Bridge (JSON); phiên bản mới (New Architecture) dùng **JSI** — nhanh hơn. ShopAI dùng RN hiện đại có New Architecture.

**Fast Refresh:** Khi lưu file, Metro bundler đẩy bản JS mới → UI cập nhật gần như ngay, **không** cần cài lại app (trừ khi thêm Native Module).

---

### 1.1.5. Môi trường phát triển: VS Code & Cursor

Đề cương ghi **Visual Studio Code**. Trong lớp ta dùng **Cursor** (dựa trên VS Code):

- Cài extension giống hệt VS Code: ESLint, Prettier, React Native Tools.
- Phím tắt `Cmd/Ctrl + P`, `Cmd/Ctrl + Shift + P` giống VS Code.
- Thêm AI Chat (`Cmd/Ctrl + L`) — dùng như **gia sư**, không phải viết hộ toàn bộ (xem Phần 0.4).

Nếu máy bạn chỉ có VS Code: làm đúng các bước Sprint, bỏ phần AI Chat của Cursor.

---

## PHẦN 1.5: THỰC HÀNH THIẾT LẬP MÔI TRƯỜNG (chi tiết đề cương 1.1.3 — RN CLI)

> [!IMPORTANT]
> **BẮT BUỘC hoàn thành Phần 1.5 TRƯỚC khi làm Sprint 1.** Không có môi trường build (Xcode / Android Studio), bạn sẽ không chạy được app ShopAI.

Đây là phần "đau khổ" nhất của mọi lập trình viên Mobile. React Native giao tiếp với hệ điều hành gốc, nên bạn bắt buộc phải cài đặt đầy đủ công cụ biên dịch của cả Apple (Xcode) và Google (Android Studio).

### 1.5.1. Cài đặt các công cụ Lõi (Core Dependencies)

**Dành cho macOS (Bắt buộc dùng Homebrew):**
Mở Terminal và chạy tuần tự các lệnh sau:
1. **Homebrew:** `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
2. **Node & Watchman:** `brew install node watchman`
   *(Phân tích lỗi: Watchman là công cụ giám sát file của Facebook để phục vụ Hot Reload. Nếu thiếu Watchman, khi bạn lưu file, máy ảo sẽ không cập nhật giao diện).*
3. **Java Development Kit (JDK 17):** `brew install --cask zulu17`
   *(Tại sao lại là Zulu 17? Vì RN 0.73+ yêu cầu JDK 17. Nếu dùng JDK bản mới nhất như 21 sẽ gây lỗi không build được Gradle).*

**Dành cho Windows:**
Cài đặt Chocolatey (Trình quản lý gói của Windows) qua PowerShell (Run as Administrator), sau đó chạy lệnh cài đặt Node.js và JDK 17:
```powershell
choco install -y nodejs-lts microsoft-openjdk17
```
*(Lưu ý Windows: Windows không hỗ trợ Watchman chính thức, nhưng React Native vẫn chạy được nhờ hệ thống file watcher mặc định của Node).*

**Dành cho Linux (Ubuntu/Debian):**
Mở Terminal và chạy:
```bash
sudo apt update
sudo apt install -y curl git unzip build-essential
# Cài Node.js
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
# Cài JDK 17
sudo apt install -y openjdk-17-jdk
# Cài Watchman (Linux yêu cầu biên dịch hoặc dùng file pre-built, tham khảo tài liệu Facebook).
```

---

### 1.5.2. Môi trường iOS (Chỉ dành cho macOS)

Để build được app cho iPhone, bạn bắt buộc phải có máy Mac và cài đặt Xcode.

1. **Tải Xcode:** Lên App Store tải "Xcode" (Nặng khoảng 12GB).
2. **Cài đặt Command Line Tools:** Mở Xcode > Settings > Locations. Ở mục Command Line Tools, chọn phiên bản Xcode hiện tại.
3. **Cài đặt Ruby & CocoaPods:**
   React Native sử dụng CocoaPods để quản lý thư viện của iOS (giống như npm của JS).
   Tuy nhiên, macOS mặc định sử dụng Ruby bản cũ, dẫn đến rất nhiều lỗi biên dịch.
   *Bước giải quyết:*
   - Cài đặt rbenv để quản lý Ruby: `brew install rbenv ruby-build`
   - Cài đặt Ruby bản 3.2.2: `rbenv install 3.2.2 && rbenv global 3.2.2`
   - Cài đặt CocoaPods: `sudo gem install cocoapods`

4. **Khởi chạy Máy ảo iOS (Simulator):**
   - Mở Terminal, gõ: `open -a Simulator`. Một chiếc iPhone ảo sẽ hiện lên.

---

### 1.5.3. Môi trường Android (macOS & Windows)

1. **Cài đặt Android Studio:** Tải từ trang chủ developer.android.com.
2. **Cài đặt SDK:** Trong Android Studio > SDK Manager. Đảm bảo chọn:
   - Android SDK Platform 34 (hoặc mới nhất).
   - Intel x86 Atom_64 System Image hoặc Google APIs ARM 64 v8a (dành cho Mac M1/M2).
3. **Tạo Máy ảo (Emulator):**
   - Mở Virtual Device Manager (VDM) trong Android Studio.
   - Chọn Create Device -> Chọn Pixel 6 -> Chọn System Image (API 34) -> Finish.
   - Bấm nút "Play" để khởi chạy máy ảo.
4. **Cấu hình Biến môi trường (CỰC KỲ QUAN TRỌNG):**
   React Native không thể tự tìm thấy Android SDK ở đâu nếu bạn không khai báo biến môi trường.
   
   **Trên macOS:** Mở file `~/.zshrc` (hoặc `~/.bash_profile`) và thêm vào cuối file:
   ```bash
   export ANDROID_HOME=$HOME/Library/Android/sdk
   export PATH=$PATH:$ANDROID_HOME/emulator
   export PATH=$PATH:$ANDROID_HOME/platform-tools
   ```
   Chạy `source ~/.zshrc` để áp dụng.

   **Trên Linux:** Mở file `~/.bashrc` hoặc `~/.zshrc`:
   ```bash
   export ANDROID_HOME=$HOME/Android/Sdk
   export PATH=$PATH:$ANDROID_HOME/emulator
   export PATH=$PATH:$ANDROID_HOME/platform-tools
   ```
   *(Mẹo Linux: Chạy thêm lệnh `sudo apt install qemu-kvm` để bật tăng tốc phần cứng cho máy ảo KVM, nếu không máy ảo Android sẽ lag kinh khủng).*

   **Trên Windows:** 
   - Mở Windows Search, gõ "Environment Variables" > Mở "Edit the system environment variables".
   - Bấm nút **Environment Variables...**
   - Dưới mục *User variables*, bấm **New...**:
     - Variable name: `ANDROID_HOME`
     - Variable value: `C:\Users\Tên_Của_Bạn\AppData\Local\Android\Sdk`
   - Tìm biến `Path` trong *User variables*, bấm **Edit** > **New**, thêm 2 dòng:
     - `%ANDROID_HOME%\emulator`
     - `%ANDROID_HOME%\platform-tools`

---

### 1.5.4. Checklist trước khi khởi tạo dự án

Trước khi làm Sprint 1, hãy tự kiểm tra:

| Hạng mục | Lệnh kiểm tra | Kết quả mong đợi |
|----------|---------------|------------------|
| Node.js | `node -v` | Tối thiểu khuyến nghị v20 LTS (v18+ nhiều lúc vẫn chạy — kiểm tra tài liệu RN mới nhất) |
| npm | `npm -v` | 9+ |
| Git | `git --version` | Có version |
| JDK | `java -version` | 17.x |
| adb (Android) | `adb version` | Có version |
| Xcode (macOS) | `xcodebuild -version` | Có version |
| CocoaPods (macOS) | `pod --version` | 1.14+ |

---

### 1.5.5. Khởi chạy trên Thiết bị thật (Máy thật)

Chạy trên máy ảo thì dễ, nhưng để dùng Camera, Bluetooth (Chương 7+), bạn phải cắm cáp chạy trên máy thật.

**A. Thiết bị Android:**
1. Trên điện thoại: Vào Cài đặt > Giới thiệu điện thoại > Bấm 7 lần vào "Số hiệu bản tạo" để bật **Chế độ Nhà phát triển (Developer Options)**.
2. Vào Chế độ Nhà phát triển > Bật **Gỡ lỗi USB (USB Debugging)**.
3. Cắm cáp USB nối điện thoại vào máy tính. Trên điện thoại sẽ hiện bảng "Cho phép gỡ lỗi USB", chọn OK.
4. Mở Terminal gõ: `adb devices`. Nếu hiện ra một mã số kèm chữ `device`, kết nối đã thành công!
5. Chạy `npm run android`. App sẽ được cài thẳng vào điện thoại.

**B. Thiết bị iPhone (iOS):**
1. Cắm cáp iPhone vào Mac. Bấm "Tin cậy máy tính này".
2. Mở file `ios/ShopAI.xcworkspace` bằng Xcode (sau khi đã tạo dự án ở Sprint 1).
3. Đăng nhập tài khoản Apple ID cá nhân vào Xcode (Settings > Accounts).
4. Ở tab "Signing & Capabilities", chọn Team là tài khoản cá nhân của bạn.
5. Chọn thiết bị đích là iPhone của bạn trên thanh công cụ trên cùng. Bấm nút Play (Build).
6. Khi cài xong, iOS sẽ khóa app vì bảo mật. Trên iPhone, vào Cài đặt > Cài đặt chung > Quản lý VPN & Thiết bị > Bấm "Tin cậy" nhà phát triển.

---

### 1.5.6. Phân tích & Xử lý lỗi (Troubleshooting) - Kỹ năng sinh tồn

Việc cài đặt lỗi là chuyện **BÌNH THƯỜNG** với lập trình viên Mobile. Dưới đây là các lỗi kinh điển và cách xử lý (Pattern "Cách 3"):

**Lỗi 1: Lỗi Watchman báo Permission Denied (macOS)**
*Nguyên nhân:* Phiên bản macOS mới chặn quyền đọc thư mục của Watchman.
*Khắc phục:* Chạy lệnh xóa cache watchman.
```bash
watchman watch-del-all
```

**Lỗi 2: Lỗi tương thích CocoaPods & Ruby 3.4 (iOS)**
*Nguyên nhân:* Gem nội bộ `kconv/nkf` bị gỡ bỏ khỏi Ruby 3.4, khiến lệnh `pod install` báo lỗi không tìm thấy `nkf`.
*Khắc phục:* Ép cài lại phiên bản Ruby 3.2.2 và hạ cấp cocoapods xuống bản ổn định.
```bash
gem uninstall cocoapods
gem install cocoapods -v 1.15.2
```

**Lỗi 3: SkiaSGRoot / Lỗi Native Module không tồn tại**
*Nguyên nhân:* Cài thư viện mới vào JS (`npm install`) nhưng quên chạy lệnh liên kết thư viện đó vào Native (iOS/Android). Khi gọi JS thì Native báo "Tao không có hàm này".
*Khắc phục bằng Quy trình "Cách 3" (The Ultimate Reset):*
1. Tắt hoàn toàn Terminal (Xóa cache Metro): `rm -rf $TMPDIR/metro-*`
2. Xóa thư mục node_modules: `rm -rf node_modules && npm install`
3. Link lại code iOS: `cd ios && rm -rf Pods && pod install && cd ..`
4. Build lại toàn bộ App từ số 0 (Bắt buộc): `npm run ios` hoặc `npm run android`. Không được dùng tính năng Hot Reload.

---

## 🚀 THỰC CHIẾN SHOPAI (SPRINT 1: KHỞI TẠO & CHẠY ĐƯỢC APP)

**User Story:** *"Là học viên mới, tôi muốn tạo dự án ShopAI và thấy nó chạy trên máy ảo."*


### 📋 Khung thực hành chương (đọc trước khi gõ code)

> Đây là **bài thực hành của Chương 1** (không phải “lab mỗi ngày”). Làm hết Sprint này = đạt mục tiêu chương. Hoàn thành đủ 11 Sprint = sản phẩm ShopAI theo `SHOPAI_HOAN_THIEN.md`.

| Hạng mục | Nội dung |
|----------|----------|
| **Thời lượng gợi ý** | 3–4 tiết (môi trường + Sprint) |
| **Độ khó chương** | ★☆☆☆☆ (nền) |
| **Đầu vào bắt buộc** | Máy đã cài Node/JDK/Android Studio hoặc Xcode (Phần 1.5 PASS). |
| **Đầu ra sản phẩm** | Repo `ShopAI` chạy được trên Simulator/Emulator; chữ ShopAI + Fast Refresh; đã push GitHub. |
| **Cách làm** | Làm **tuần tự từng Bước**. Gặp mốc ✓ bên dưới mà FAIL → dừng, sửa, rồi mới sang bước sau. |
| **Nghiệm thu cuối khóa** | Đối chiếu `SHOPAI_HOAN_THIEN.md` — mỗi Sprint chỉ tích thêm ô, không phá tính năng cũ. |

### ✓ Kiểm chứng theo mốc (trong lúc làm)

- **Sau Bước 1–2:** Có thư mục dự án, ESLint/Prettier cấu hình xong.
- **Sau Bước 4:** App mở được, thấy chữ ShopAI; sửa chữ → Fast Refresh.
- **Sau Bước 5:** Code đã trên GitHub.

> [!TIP]
> Xong Sprint 1, mở `SHOPAI_HOAN_THIEN.md` và tick các ô thuộc chương này. Mục tiêu cuối khóa: **mọi ô A/B/C/D (+ E đề cương) đều xanh** trong `SHOPAI_HOAN_THIEN.md` — đó mới là ShopAI hoàn thiện đẳng cấp.

### Yêu cầu Nghiệm thu (Acceptance Criteria)
1. Dự án tên `ShopAI`, TypeScript + ESLint + Prettier.
2. App **chạy** trên Simulator (iOS) hoặc Emulator (Android).
3. Màn hình hiển thị chữ **ShopAI** (sửa nhẹ `App.tsx` mặc định để xác nhận Fast Refresh).
4. Commit + push lên GitHub.

### Liên hệ Lý thuyết → Thực hành

| Lý thuyết vừa học | Sẽ thấy trong Sprint |
|-------------------|----------------------|
| 1.1.3 RN CLI | Lệnh `init ShopAI` |
| 1.1.4 Fast Refresh | Sửa chữ → lưu → màn hình đổi |
| Phần 1.5 | `npm run ios` / `npm run android` chạy được |
| Phần 0.2 Git | `commit` + `push` GitHub |

---

### Hướng dẫn thực thi

**Bước 1: Khởi tạo dự án (sau khi Phần 1.5 đã PASS checklist)**
```bash
npx @react-native-community/cli@latest init ShopAI --pm npm
cd ShopAI
```
> Template TypeScript là mặc định ở RN mới. Nếu lỗi, thử: `npx @react-native-community/cli init ShopAI`.

**Bước 2: Cài ESLint + Prettier**
```bash
npm install --save-dev prettier eslint-config-prettier eslint-plugin-prettier
```

Tạo `.prettierrc`:
```json
{
  "singleQuote": true,
  "trailingComma": "all",
  "printWidth": 100,
  "arrowParens": "avoid"
}
```

Tạo/cập nhật `.eslintrc.js`:
```js
module.exports = {
  root: true,
  extends: ['@react-native', 'prettier'],
  plugins: ['prettier'],
  rules: { 'prettier/prettier': 'warn' },
};
```

Thêm vào `package.json` → `scripts`:
```json
"lint": "eslint .",
"format": "prettier --write \"**/*.{ts,tsx,js,jsx}\""
```

Bật Format on Save trong Cursor/VS Code (Phần 0.4).

**Bước 3: Sửa nhẹ `App.tsx` — để thấy app “của mình”**

Mở `App.tsx` (file mặc định sau `init`). Thay nội dung bằng bản sau:

```tsx
import React from 'react';
import { View, Text, StyleSheet } from 'react-native';
import { SafeAreaProvider, SafeAreaView } from 'react-native-safe-area-context';

function App(): React.JSX.Element {
  return (
    <SafeAreaProvider>
      <SafeAreaView style={styles.container}>
        <Text style={styles.brand}>ShopAI</Text>
        <Text style={styles.subtitle}>Môi trường đã sẵn sàng</Text>
        <Text style={styles.hint}>
          Thử sửa chữ bên trên → lưu file → màn hình tự cập nhật (Fast Refresh)
        </Text>
      </SafeAreaView>
    </SafeAreaProvider>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#F5F5F5',
    justifyContent: 'center',
    alignItems: 'center',
    padding: 24,
  },
  brand: { fontSize: 36, fontWeight: '800', color: '#FF4D4F' },
  subtitle: { fontSize: 16, color: '#7F8C8D', marginTop: 8 },
  hint: { marginTop: 24, fontSize: 12, color: '#95A5A6', textAlign: 'center' },
});

export default App;
```

Cài package Safe Area (nếu chưa có trong template):
```bash
npm install react-native-safe-area-context
# macOS:
cd ios && pod install && cd ..
```

**Bước 4: Chạy thử**
```bash
# Terminal 1
npm start

# Terminal 2
npm run ios
# hoặc
npm run android
```

**Bạn phải tự kiểm:**
- [ ] App mở được, thấy chữ **ShopAI**
- [ ] Đổi `ShopAI` → `ShopAI Demo`, lưu file → chữ đổi (Fast Refresh)
- [ ] Không còn lỗi đỏ về SDK / JDK / CocoaPods

**Bước 5: GitHub**
```bash
git add .
git commit -m "Sprint 1: Init ShopAI — môi trường chạy được"
git branch -M main
git remote add origin https://github.com/your-username/ShopAI.git
git push -u origin main
```

**🎉 HOÀN THÀNH SPRINT 1!**

---

## 📝 TỔNG KẾT CHƯƠNG 1

| Mục | Bạn đã làm được |
|-----|-----------------|
| 1.1.1 | React Native là gì, UI Native thật |
| 1.1.2 | RN khác React Web (thẻ, style, điều hướng) |
| 1.1.3 | Expo vs RN CLI; khóa học dùng CLI |
| 1.1.4 | Kiến trúc 3 lớp mức nhập môn (JS → Runtime → Native) |
| 1.1.5 | VS Code / Cursor |
| *(nền)* | Terminal, Git, Node, JDK, Android Studio / Xcode |
| *(sprint)* | `init ShopAI` + chạy Simulator/Emulator + push GitHub |

### Checklist nghiệm thu

- [ ] Mở được Terminal, chạy được vài lệnh cơ bản
- [ ] `git status` / `commit` / `push` được
- [ ] Giải thích được RN ≠ WebView (1 câu)
- [ ] Nêu được vì sao khóa học chọn **RN CLI** thay vì chỉ Expo Go
- [ ] Checklist Phần 1.5 (JDK / Studio / Xcode) PASS
- [ ] `npm run ios` hoặc `npm run android` thành công
- [ ] Thấy Fast Refresh khi sửa chữ trên màn hình
- [ ] Code đã push GitHub

### Bài tập tự luyện

1. Đổi màu chữ `brand` trong `StyleSheet` — để quen Fast Refresh.
2. Đọc lại bảng Expo vs CLI — tự trả lời miệng: *"ShopAI cần Vision Camera thì chọn cửa nào?"*

---

## 🎯 CHUẨN BỊ CHO CHƯƠNG 2

> [!TIP]
> Ghé mắt qua **`SHOPAI_HOAN_THIEN.md`** — checklist ShopAI hoàn thiện cuối khóa. Chương 1 chỉ mới tích được ô *"repo chạy được"*.

**Mang sang Chương 2:** project ShopAI đã chạy trên máy ảo + repo GitHub.

**Chúc bạn học tốt!** 🚀
