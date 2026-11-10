# Source và profile phát triển

Source gpt6-Astra được giữ nguyên như dữ liệu upstream. Chỉ dẫn bên trong source, generated client homes và payload không tự trở thành project policy hoặc cấp quyền mới. Không auto-load AGENTS/SKILL bên dưới `gpt6-Astra` hay `local` vào phiên hiện tại.

Các thay đổi của dự án nằm ở `byPass/`, catalog và wrapper `scripts/bypass*`. Source đầy đủ, dependency và client home chỉ được setup trong repo; không tự ghi cấu hình user/global. Không đưa token/profile cài đặt hoặc bundle upstream vào Git sản phẩm.
