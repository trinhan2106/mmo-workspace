# byPass / ColdCoffee trong dự án

Theo yêu cầu người dùng, giữ **toàn bộ source nguyên bản** [gpt6-Astra / ColdCoffee](https://github.com/3641397194-wq/gpt6-Astra/tree/3249afce6b853ff2f2133e016b223db2cf38b087) trong `jailbreak/gpt6-Astra/`, commit `3249afce6b853ff2f2133e016b223db2cf38b087`, release tham chiếu `v3.2.0-preview.9`. Không cắt prompt, bundled skill, docs hoặc thành phần có sẵn. Source checkout được ignore, tải lại theo pin khi đổi máy.

| Nơi | Nội dung |
|---|---|
| `gpt6-Astra/` | Full upstream checkout + dependency local; không sửa file tracked upstream |
| `local/codex-home/` | Target cài nguyên bản Codex seat/bundled skills, scoped trong repo |
| `local/` | Dữ liệu app/cache/homes thử; ignored, không phải VM boundary |
| `byPass/` | Entry và profile code/văn phong do dự án quản lý |
| `catalog.json` | Profile mở rộng và provenance pin |

Root upstream MIT; thành phần đi kèm giữ license riêng (gồm GPL trong subproject). Xem nguyên bản LICENSE và THIRD_PARTY_NOTICES.md trong checkout. Dự án chỉ lưu wrapper/metadata, không phân phối lại toàn bundle.

`byPass` là tên entry phát triển trong repo. Wrapper gọi composition engine nguyên bản và có thể mở app nguyên bản; nó không là model/API mới hoặc dependency lõi Rust. Cài profile vào home riêng không thay cấu hình của Codex desktop đang mở. Không hứa profile vượt quy tắc của model, cải thiện mọi task hay làm văn bản qua được AI detector. Chất lượng vẫn đo bằng code/build/test và độ đúng nội dung.

Đọc [cách dùng](byPass/README.md). Không chạy installer upstream thiếu target home: bản gốc mặc định có thể ghi vào thư mục AI của người dùng.
