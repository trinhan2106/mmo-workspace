# Nguồn tái sử dụng

Kiểm metadata/commit gốc ngày 2026-11-10; [manifest](manifest.json) pin mốc tham khảo. License dựa trên khai báo upstream, chưa audit code/chạy integration. Dùng package release ổn định + lockfile khi chọn dependency; không mặc định dùng head tham khảo làm dependency app.

| Repo | Dùng ở đâu | License khai báo |
|---|---|---|
| [Spec Kit](https://github.com/github/spec-kit) | Đã tải và cài CLI local v1.3.3, Codex skills | MIT |
| [Tauri](https://github.com/tauri-apps/tauri) | Desktop shell | MIT / Apache-2.0 |
| [windows-rs](https://github.com/microsoft/windows-rs) | Windows API adapter | MIT / Apache-2.0 |
| [Virtualization Documentation](https://github.com/MicrosoftDocs/Virtualization-Documentation) | Hyper-V docs/samples | CC-BY-4.0 docs, MIT code |
| [chromiumoxide](https://github.com/mattsse/chromiumoxide) | Candidate Rust browser worker | MIT / Apache-2.0 |
| [async-imap](https://github.com/chatmail/async-imap) | Mailbox provider | MIT / Apache-2.0 |
| [oauth2-rs](https://github.com/ramosbugs/oauth2-rs) | OAuth | MIT / Apache-2.0 |
| [Playwright](https://github.com/microsoft/playwright) | Candidate Node browser worker/tests | Apache-2.0 |

Source Spec Kit, windows-rs và Virtualization Documentation đã có trong `.reference/`. Tải source ứng viên khi cần đọc: `py -3.12 scripts/fetch_reference.py chromiumoxide`. Script tải đúng commit vào `.reference/<name>`, không cài dependency, browser, hook hoặc chạy repo đó. Metadata `local` chỉ ghi trạng thái lúc thiết lập, không kiểm inventory của mọi máy.

Không vendor toàn bộ repo vào code sản phẩm hoặc thêm cả chromiumoxide và Playwright trước PoC so sánh. Tài liệu Microsoft nêu sample không là bản triển khai production. Khi chép code cụ thể, giữ license/notice/attribution tương ứng. Chưa thêm repo đăng ký/trial không rõ nguồn: chỉ reference không biến nó thành code được phép chạy hay bảo đảm quyền sử dụng.
