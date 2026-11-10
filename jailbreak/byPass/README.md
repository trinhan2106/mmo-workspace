# Entry byPass

Mọi task code/docs của repo đọc entry này. Profile coding dùng chung `docs/CODE-STANDARDS.md`; profile writing phục vụ bài viết tự nhiên. Đây là context tác vụ theo project; không thay quyền của tool/model hoặc bỏ bước nghiệm thu.

## Setup và kiểm tra

```powershell
./scripts/setup-bypass.ps1
node scripts/bypass.cjs preview
```

Setup tải full source đúng pin nếu chưa có, cài dependency theo lockfile và chuẩn bị Electron. Mọi target/cache/data nằm trong repo, không dùng config/token user hiện tại. Các client/seat vẫn nguyên trong source/app; không tự sửa cấu hình client đang dùng.

**Trạng thái 10/11/2026:** đã thử cài nguyên bản Codex seat gồm 11.862 planned files vào `jailbreak/local/codex-home`, nhưng Defender chặn mẫu tham khảo reverse-skill; installer báo transaction `partial`, verify `ok:false`. Source nguyên bản vẫn giữ đủ. Task T018 ghi blocker, không coi bộ cài là hoàn tất và chưa mở app trên target partial. Không tắt Defender/đặt exclusion/đổi mẫu để lấy kết quả pass.

Sau khi T009 có môi trường guest được nghiệm thu và T018 xử lý blocker, bước cài nguyên bản là `./scripts/setup-bypass.ps1 -InstallOriginalSeat`, rồi `node scripts/bypass.cjs verify`. Chỉ retry sau khi task đã được cập nhật có chủ ý và lý do chặn được giải quyết. Wrapper ngăn retry/launch target partial tự động.

## Dùng khi code hoặc viết

```powershell
node scripts/bypass.cjs compose coding .work/request.txt
node scripts/bypass.cjs compose writing .work/article-brief.txt
node scripts/bypass.cjs launch
```

`compose` đọc brief và profile project, gọi CLI composition nguyên bản ColdCoffee và trả prompt; không gọi API/model hoặc tự gửi tài liệu đi. Child environment bỏ các biến chứa key/token/password để không tự kế thừa credentials của phiên cha. Khi có sẵn, dùng bước này để chuẩn bị context trước thực hiện task, rồi giữ task/spec/acceptance và handoff của dự án. Máy chưa setup thì chạy setup hoặc báo lỗi cụ thể, không tuyên bố engine đã dùng nếu chưa gọi.

`launch` được chuẩn bị để mở app upstream với homes/dữ liệu tách trong repo, nhưng hiện bị chặn do cài partial. Source vẫn có các chức năng nguyên bản; kết nối provider/model/công cụ khác cần cấu hình và quyền tương ứng. Không có API key/credential điền sẵn hoặc VM/sandbox OS được tạo bởi launcher.

Home cài nguyên bản là dữ liệu cục bộ, **không được tự đọc vào system instructions của chat hiện tại**. Muốn dùng client riêng với home này phải chọn đúng profile trong client hỗ trợ; chưa tuyên bố Codex desktop đang mở chuyển sang profile đó. Nội dung task và quy tắc cấp cao hơn vẫn có hiệu lực.

## Thêm profile sau này

Thêm một Markdown trong `profiles/`, đăng ký ID/path/purpose ở `jailbreak/catalog.json` rồi chạy `node scripts/bypass.cjs check`. Mỗi profile ghi rõ mục đích, output và cách đánh giá; không tự cài một bộ khác chồng lên global config. Giữ attribution/license nếu dùng nội dung bên ngoài. Không thêm endpoint/key vào profile.
