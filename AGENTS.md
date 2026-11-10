# MMO Workspace

- Trả lời tiếng Việt; issue, PR và review trên GitHub dùng tiếng Anh.
- Repo sản phẩm là `trinhan2106/mmo-workspace`. Thư mục cha chứa nghiên cứu riêng và dự án khác: không copy hàng loạt, không áp workflow AMS, không đưa dữ liệu account/payment vào repo public.
- Trước khi code: đọc `docs/START-HERE.md`, `.specify/memory/constitution.md`, chạy `py -3.12 scripts/project.py status`, rồi đọc spec/plan của task.
- Dùng `.agents/skills/workspace-handoff/SKILL.md` khi bắt đầu/tiếp tục/kết thúc task. Chỉ một task active trên checkout. Không tự chiếm task hoặc xóa lock; giữ công việc dở của người khác.
- `project/tasks.json` là nguồn lifecycle duy nhất. `specs/*/tasks.md` và `docs/handoffs/NEXT.md` được sinh bằng script. GitHub là mirror. Không dùng `$speckit-github-taskstoissues` để tạo issue; dùng `scripts/github_sync.py` để giữ ID toàn repo, kể cả issue đã đóng.
- Dùng skill `speckit-*` để soạn spec/plan/phân rã; đăng ký task bằng `project.py add`, giữ ID cũ rồi `render`. Không ghi đè checklist sinh từ registry. Mỗi chat làm một task đã claim, không tự chạy implement hết backlog.
- Stack: Rust core + Tauri 2/TypeScript UI + SQLite. OS isolation là persistent Windows VM, Hyper-V cần preflight. Browser/tool native chạy guest; profile/Tauri không thay VM. Proxy rotation do người dùng quản lý, ngoài lõi.
- Task foundation không bao gồm chạy tool bên thứ ba, tạo account/trial hoặc payment thật. Module tương lai chỉ thao tác tài nguyên được cấp quyền và điều kiện dịch vụ thực. Không hứa trial/không dấu vết; không xây bypass.
- Thay đổi nhỏ, kiểm tra liên quan. Không tự đổi Windows/Hyper-V/reboot. Quyết định bền vững vào `docs/decisions.md`; evidence vào `docs/handoffs/<ID>.md`. Workflow changes: chạy `py -3.12 -m unittest discover -s tests -v` và `project.py check`.
- Cuối chat cập nhật registry, `render` + `check`, sync GitHub khi có mạng/quyền. Lỗi sync ghi pending, không tạo issue lại thủ công. Final gồm kết quả, kiểm tra, phần dở và **prompt nguyên văn từ `docs/handoffs/NEXT.md`**; prompt cũ phải đối chiếu revision trước claim.
- Không commit secrets/cookies/token/mailbox thật/profile/đĩa VM. `.reference/`, `.tools/`, `.work/` ignored. Không đổi Codex config toàn cục hoặc bật memory tự động.
