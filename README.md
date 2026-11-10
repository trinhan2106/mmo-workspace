# MMO Workspace

Ứng dụng Windows có lõi Rust, giao diện Tauri và module mở rộng. Mục tiêu đầu tiên là quản lý VM để chạy browser/tool được cấp quyền và bảo vệ dữ liệu máy chính.

**Hiện trạng:** đã chuẩn bị Spec Kit, spec nền, registry và workflow bàn giao. Chưa có app chạy được; chưa xác minh Hyper-V hoặc cài Rust/MSVC trên máy này.

- [Bắt đầu một chat](docs/START-HERE.md) · [Prompt tiếp theo](docs/handoffs/NEXT.md)
- [Tasks](specs/001-workspace-foundation/tasks.md) · [GitHub Project](https://github.com/users/trinhan2106/projects/4) (private)
- [Spec](specs/001-workspace-foundation/spec.md) · [Plan](specs/001-workspace-foundation/plan.md)
- [Quyết định](docs/decisions.md) · [Nguồn tái sử dụng](references/README.md)
- [Chuẩn code chung](docs/CODE-STANDARDS.md) · [byPass / nguồn ColdCoffee local](jailbreak/byPass/README.md) — composition hoạt động; full bundle đang bị chặn ở T018

```powershell
py -3.12 scripts/project.py status
py -3.12 scripts/project.py check
py -3.12 -m unittest discover -s tests -v
```

Repo public chỉ chứa mã, tài liệu và dữ liệu mẫu. Runtime/VM/secrets ở ngoài Git. Nghiên cứu trong thư mục cha không phải nội dung sản phẩm.
