# Chuẩn code chung

Áp dụng cho code do dự án duy trì, không format/sửa source upstream, skill Spec Kit được sinh hoặc file generated. Tất cả chat bắt đầu từ cùng chuẩn này.

## File và trách nhiệm

- Tổ chức theo tính năng và ranh giới nghiệp vụ, không gom vào `main`, `App`, `utils` hoặc `helpers` khổng lồ. Một file chịu một trách nhiệm có thể mô tả bằng một câu.
- Mục tiêu thường khoảng 100–300 dòng/file; trên 400 dòng cần xem lại cách tách và ghi lý do nếu giữ. Đây là tín hiệu review, không ép chia cơ học hoặc tạo hàng chục file một hàm. Entry point chỉ wiring/parse args, không chứa toàn bộ nghiệp vụ.
- Tách khi khác lý do thay đổi: schema/DTO; nghiệp vụ; database; adapter I/O; UI; formatter/presenter. Đặt tên theo hành vi cụ thể, ví dụ `job_store.rs`, `guest_transport.rs`, `mailbox_oauth.rs`; tránh tên `misc`, `common2`, `new`, `final`.
- Mỗi module có API nhỏ; import từ API công bố. Không truy cập bảng DB/private internals của module khác. Thêm abstract layer khi đã có nhiều implementation hoặc cần test boundary, không tạo framework trước nhu cầu.

## Rust / Tauri / TypeScript

- `crates/contracts` không phụ thuộc UI/hypervisor. Core không gọi Tauri/browser/vendor trực tiếp. Environment/provider adapters triển khai interface của core. Worker và platform module ở phía guest.
- Tauri command chỉ validate/authorize, gọi service và map kết quả; SQL/PowerShell/automation không nằm trong command hoặc component UI.
- Rust: `snake_case` cho module/hàm, `PascalCase` cho type/trait, `SCREAMING_SNAKE_CASE` cho constants; `Result` và lỗi có ngữ cảnh, tránh `unwrap/expect` trên input/I/O production. `unsafe` cần invariant và lý do; không thêm chỉ để né compiler.
- TypeScript: strict mode khi scaffold; không `any`/`@ts-ignore` rộng. Dùng `unknown` + validate ở biên. Component giữ UI, hook/service giữ state và side effects; không gọi shell/DB trực tiếp. Component/type PascalCase, hàm/biến camelCase, file chức năng kebab-case; một convention cho cả app.
- Chưa có Cargo/package manifest nên Rustfmt/Prettier config là chuẩn chuẩn bị. T003 phải pin toolchain, cài lint/typecheck/build scripts thật và nối CI; không báo đã chạy Rust/TS checks khi chưa có app.

## Biên dữ liệu và lỗi

- Validate input tại biên; dùng type/schema và version cho message. Core nhận secret reference thay raw token. Redact trước log, không log cookies/thẻ/mailbox thật.
- Dùng timeout/cancel rõ; phân biệt lỗi retry được, lỗi quyền, input lỗi và kết quả chưa rõ. Không retry mù thao tác có tác động; có request ID/idempotency và trạng thái phục hồi.
- Không nuốt exception bằng catch rỗng hoặc trả success giả. Resource/process/file handle phải cleanup; async không block UI. Việc hệ điều hành chỉ ở adapter được giới hạn.
- Không hardcode path cá nhân/credential/URL vendor trong core. Cấu hình có schema/default; migration có đường nâng cấp và rollback phù hợp.

## Định dạng và review

- `.editorconfig` là nền: UTF-8, LF, final newline; Rust/Python 4 spaces, TS/JS/JSON/YAML 2 spaces. Dòng code hướng tới 100 ký tự; formatter xử lý trường hợp còn lại.
- Python tooling dùng Ruff theo `pyproject.toml`, version pin tại `project/quality-requirements.txt`. Cài local bằng `scripts/setup-quality.ps1`; kiểm `ruff check scripts tests` và `ruff format --check scripts tests`.
- Rust dùng `cargo fmt --check`, `cargo clippy` và test của crate thay đổi khi đã có manifest. Frontend dùng Prettier/ESLint/typecheck/build sau scaffold; không disable warning toàn repo để làm xanh CI.
- Ưu tiên helper đã có. Comment giải thích invariant/lý do, không kể lại từng dòng. Public contract có ví dụ input/output và failure cases cần thiết.
- Diff tập trung; test logic/side effects và regression thực, không thêm test chỉ để đếm. Reviewer kiểm tên/path có tìm được, lỗi có chẩn đoán được, dependency có chiều rõ và handoff có việc dở. Không thay logic lẫn formatting không liên quan trong một diff lớn.
