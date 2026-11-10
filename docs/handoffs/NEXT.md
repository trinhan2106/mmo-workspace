# Prompt cho chat kế tiếp

Registry revision: 11. Sinh tự động; đọc lại state trước khi làm.

```text
Tiếp tục dự án tại D:/MMO-Plus-UPI/mmo-workspace. Đọc AGENTS.md và docs/START-HERE.md; dùng skill workspace-handoff.
Dùng entry byPass ở jailbreak/byPass/README.md và chuẩn code docs/CODE-STANDARDS.md; source/profile chỉ setup trong repo này.
Chạy py -3.12 scripts/project.py status và đối chiếu registry hiện tại. Prompt cũ không thay trạng thái mới.
Giữ các blocker hiện có: T018. Đọc reason/next_action trong registry; không tự đánh dấu hoàn tất hoặc bỏ qua điều kiện.
Task dự kiến: T002 — Read-only Windows and Rust/Tauri toolchain preflight. Đọc specs/001-workspace-foundation/spec.md và specs/001-workspace-foundation/plan.md, acceptance trong registry và docs/handoffs/T002.md nếu có.
Nếu T002 vẫn ready và chưa có task active, chọn branch phù hợp rồi claim bằng project.py start T002 --owner <nhãn-chat-mới> --revision <revision-vừa-đọc>.
Chỉ làm task này, kiểm tra đúng phạm vi, cập nhật evidence/registry. Chạy render/check và sync GitHub khi có quyền; cuối chat trả prompt mới từ docs/handoffs/NEXT.md.
```
