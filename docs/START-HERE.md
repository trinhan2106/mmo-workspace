# Làm việc qua nhiều chat

Mở đúng `D:/MMO-Plus-UPI/mmo-workspace` trong Codex. Python 3.12 + GitHub CLI phục vụ quản lý task; ứng dụng vẫn dùng Rust/Tauri.

Mọi task code/docs đọc `jailbreak/byPass/README.md` và `docs/CODE-STANDARDS.md`. byPass gọi engine composition nguyên bản ColdCoffee để chuẩn bị context; full source và home cài riêng giữ trong repo. Setup lần đầu: `scripts/setup-bypass.ps1` và `scripts/setup-quality.ps1`. Không suy rằng app/VM hoặc cấu hình Codex đang mở đã được thay đổi bởi bước này.

Quy tắc dùng engine gốc áp dụng cả task implementation/spec/nghiên cứu/tài liệu: compose brief, đọc output và ghi command/profile/pin trong evidence; lỗi engine phải báo rõ. Định hướng tương lai là [đóng gói tool để bán](../specs/003-commercial-tool-packaging/spec.md), hiện được lưu thành task thiết kế T020 sau MVP, không phải tính năng đã triển khai.

## Nguồn sự thật

| Dữ liệu | Nơi quản lý |
|---|---|
| Yêu cầu và nghiệm thu | `specs/<feature>/spec.md` |
| Thiết kế và phạm vi implementation | `specs/<feature>/plan.md` |
| ID, dependencies, lifecycle, owner, evidence | `project/tasks.json` |
| Link issue/item, lần sync | `project/github.json` |
| Checklist/prompt | `specs/*/tasks.md`, `docs/handoffs/NEXT.md` — sinh tự động |
| Kết quả/việc dở | `docs/handoffs/Txxx.md` |
| Quyết định lâu dài | `docs/decisions.md` |

Project là mirror: kéo thẻ trên GitHub không tự thay local. Muốn nhận thay đổi remote thì đọc, đánh giá và cập nhật registry có chủ ý.

## Bắt đầu

1. Đọc AGENTS/constitution; chạy `py -3.12 scripts/project.py status`.
2. Đối chiếu revision của prompt. Task active có owner thì tiếp tục đúng bàn giao hoặc báo owner; không tự chiếm task. Đọc spec, plan, acceptance và evidence.
3. Kiểm tra branch/dirty files; tạo branch cho công việc mới khi phù hợp, không chuyển branch làm mất việc khác.
4. Claim với revision vừa đọc ở status: `py -3.12 scripts/project.py start T002 --owner chat-toolchain-20261110 --revision <N>`. Thay `<N>` bằng revision hiện tại, không dùng số trong prompt cũ. Owner là nhãn phiên không chứa thông tin riêng tư. Script từ chối stale revision/task chưa đủ dependencies/task khác active.
5. Chỉ làm task claim. Thêm task phát sinh vào registry, không giấu trong final.

## Kết thúc

Viết `docs/handoffs/Txxx.md`: kết quả thực, file thay đổi, lệnh kiểm tra/kết quả, chưa kiểm, việc dở, commit/PR nếu có. Không ghi secrets.

```powershell
py -3.12 scripts/project.py complete T002 --owner chat-toolchain-20261110 --evidence docs/handoffs/T002.md --checks "preflight passed; no system changes" --summary "Recorded verified prerequisites"
py -3.12 scripts/project.py render
py -3.12 scripts/project.py check
py -3.12 scripts/github_sync.py --apply
```

Chỉ `complete` khi acceptance đạt; script kiểm cấu trúc chứ không thay review chất lượng. Nếu dở giữ `in_progress`, cập nhật evidence và render để prompt tiếp tục đúng task. Nếu bị chặn: `project.py block <ID> --owner <owner> --reason "..." --next-action "..."`. Chỉ `resume <ID> --revision <N>` sau khi lý do được giải quyết. Không xem blocker là done.

Python tooling thay đổi phải qua Ruff check/format và unit tests. Wrapper/profile thay đổi phải qua `node --test tests/bypass.test.cjs` và catalog check; trên sandbox cấm spawn dùng `--test-isolation=none`. Rust/TS lint/build nối thêm ở T003 sau khi có manifest, theo CODE-STANDARDS.

Final copy khối prompt từ NEXT. Nó ưu tiên task active; hết việc sẵn sàng thì nêu blocker; xong hết thì nói đã hết task.

## Thêm phạm vi với Spec Kit

Spec Kit v1.3.3 pin ở `project/tooling.json`. Gọi `$speckit-specify`, `$speckit-plan`, `$speckit-analyze` khi phù hợp; bước tasks phải dùng registry toàn repo. Extension GitHub được cài nhưng taskstoissues chuẩn không quản lý claim/revision, nên repo dùng synchronizer riêng.

Soạn entry mới theo cấu trúc registry vào `.work/new-task.json`; chạy `project.py add --file .work/new-task.json --revision <N>`. ID tăng toàn repo, không tái dùng ID. Script kiểm duplicate/dependency/cycle. Thêm task vào spec liên quan rồi render/check/sync. Task platform hiện là discovery/spec, chưa phải lệnh chạy tài khoản thật.

Source ở `.reference/spec-kit`, CLI `.tools/spec-kit-venv/Scripts/specify.exe`. Máy mới dùng `scripts/setup-spec-kit.ps1` (cần Git, uv, Python 3.12 và mạng khi cài lần đầu). Chạy `project.py render` sau checkout để chọn feature local cho Spec Kit qua `.specify/feature.json` ignored. Không sửa skill `speckit-*` sinh tự động; quy tắc riêng ở AGENTS và `workspace-handoff`.

## Giới hạn

Mutex `.work/registry.lock` chỉ khóa **một checkout**, không phải distributed lock. Một checkout hoạt động; reconcile trước khi đổi máy. Lock còn lại sau crash: đọc PID/host trong file, kiểm tiến trình đã kết thúc rồi mới xóa đúng file; không auto-timeout/takeover. Claim có owner không tự hết hạn.

Sync đọc issue mở/đóng trước mutation, đối chiếu marker ID, kiểm đúng remote và lưu mapping từng task. Sau mạng lỗi đọc lại remote; không tạo bù thủ công. Chạy không `--apply` để dry run. CLI cần quyền repo/project; không lưu token. CI kiểm registry/tài liệu sinh; không đảm bảo mọi AI client đều tuân AGENTS.
