# Quyết định dự án

Khởi tạo 2026-11-10, Asia/Bangkok.

| ID | Quyết định | Lý do / giới hạn |
|---|---|---|
| ADR-001 | Windows standalone; Rust + Tauri 2/TypeScript + SQLite | Theo lựa chọn người dùng; phiên bản app dependency chốt ở scaffold |
| ADR-002 | Persistent Windows VM, kiểm Hyper-V đầu tiên | Cần browser/tool native trong guest; edition Professional đọc được, phần cứng/Hyper-V chưa xác minh |
| ADR-003 | Không arbitrary module execution trên host | Worker guest + capability; UI/browser profile không là OS boundary |
| ADR-004 | Proxy rotation ngoài MVP | Người dùng tự quản; không thêm anti-detect/fingerprint spoofing |
| ADR-005 | SDK/worker protocol có version; providers tách platform | Thêm Gmail/ChatGPT/Gemini không sửa core theo từng nền tảng |
| ADR-006 | Registry canonical, GitHub mirror, một active task | Giữ liên tục qua chat, không tuyên bố distributed lock |
| ADR-007 | Spec Kit v1.3.3 local, Codex skills | Không global hooks/memory |
| ADR-008 | Giữ repo Public; Project private | Chỉ code/docs/sample; không chuyển private research vào repo |
| ADR-009 | Chuẩn code chung, file theo trách nhiệm, formatter/lint pin | CODE-STANDARDS + EditorConfig/Rustfmt/Prettier; Ruff cho tooling hiện có; không cắt file theo số dòng máy móc |
| ADR-010 | byPass là entry phát triển project-local, giữ full ColdCoffee upstream | Theo yêu cầu bổ sung: source nguyên bản + Codex seat/bundle cài vào repo-local home; composition dùng engine gốc. Không đổi global AI config hoặc coi đây là model/VM mới |
| ADR-011 | Mọi task dùng composition gpt6-Astra gốc qua byPass, có evidence thực | Xác nhận lại của user 10/11/2026: ghi command/profile/pin, báo lỗi nếu chưa chạy; không giả vờ thay engine hoặc gỡ blocker T018 |
| ADR-012 | Hướng tới đóng gói tool/module để bán sau MVP | T020 đặc tả product manifest, lựa chọn standalone/bundle, allowlist phát hành, notices, update/activation options; dev tooling và dữ liệu riêng tách khỏi gói khách hàng |

Chưa chốt: console nhúng hay cửa sổ riêng, guest OS/license, worker transport, thư viện automation/OAuth. Chỉ quyết định khi task có bằng chứng.
