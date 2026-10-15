# Phạm vi và giới hạn của SiteSignal

Tài liệu bàn giao cho chủ dự án. Mô tả tính năng cuối cùng phải khớp bản release và README; tài liệu không chứng minh Actor đã được publish hoặc bật thu phí.

## Ý nghĩa của kết quả

- Email là chuỗi địa chỉ tìm thấy trên trang công khai đã đọc, không phải địa chỉ được xác minh có hộp thư hoặc nhận thư được.
- Điện thoại phụ thuộc thông tin website công khai và định dạng nguồn. Không hứa chuẩn hóa quốc tế nếu không có đủ thông tin quốc gia.
- Social profile là liên kết quan sát được; website có thể gắn link cũ hoặc link không thuộc doanh nghiệp. Phải kiểm tra bằng chứng khi cần độ chính xác cao.
- Công nghệ là dấu hiệu trong HTML như script, meta hoặc URL tài nguyên. Phát hiện không đầy đủ và có thể là mã cũ không còn hoạt động.
- Không tìm thấy chỉ có nghĩa không thấy trên những trang đã crawl. Nó khác website không tồn tại, bị chặn hoặc không truy cập được.

## Phạm vi kỹ thuật

Phiên bản đầu đọc HTML qua HTTP thông thường và chỉ thăm một số trang có liên quan. Không chạy JavaScript, đăng nhập, tìm contact trong cơ sở dữ liệu trả phí, giải CAPTCHA hay vượt tường truy cập. Không bảo đảm xử lý mọi website.

Giới hạn đầu vào, số trang/domain, timeout, dung lượng phản hồi và concurrency là cần thiết để kiểm soát chi phí. HTTPS/HTTP chuyển hướng phải được kiểm tra trước khi theo. Đầu vào và link phát hiện được không được phép trở thành đường truy cập mạng nội bộ. Không vô hiệu hóa các kiểm tra này để làm một website “chạy được”.

Cấu hình mặc định: `maxPagesPerSite: 3` (tối đa 5), `maxSites: 100`, `concurrency: 5`, `timeoutSeconds: 20`, `respectRobots: true`, `minDelaySeconds: 0.5`, `includeTechnology: true`. Danh sách `websites` chấp nhận URL hoặc object `{ "url": "https://example.com" }`. Domain trùng được loại trước khi xử lý. Kết quả không thành công được báo trong `OUTPUT`; đối chiếu record này khi số dòng dataset ít hơn số website đầu vào.

Tôn trọng chính sách robots và giới hạn tốc độ được triển khai. Quy tắc [Robots Exclusion Protocol](https://www.rfc-editor.org/rfc/rfc9309) không phải cơ chế cấp phép truy cập; người dùng vẫn phải xem xét quyền và điều khoản của nguồn mình xử lý.

## Dữ liệu và xuất bản

Chỉ xử lý dữ liệu người dùng có quyền sử dụng. Thông tin đã công khai vẫn có thể là dữ liệu cá nhân. SiteSignal không tự gửi tin, bán danh sách liên hệ hoặc bảo đảm dữ liệu phù hợp mọi mục đích.

Kết quả local nằm ở nơi lệnh chạy chỉ định. Khi chạy trên Apify, input/dataset/log và thời gian lưu phụ thuộc cấu hình tài khoản, quyền chia sẻ và cơ chế của nền tảng. Không tuyên bố “không lưu dữ liệu” cho toàn hệ thống. Xem [tài liệu storage của Apify](https://docs.apify.com/platform/storage).

Không commit token, file `.env`, thông tin PayPal, giấy tờ KYC hoặc dữ liệu khách thật vào repository công khai. Bộ dữ liệu demo chỉ nên dùng thông tin giả lập hoặc thông tin doanh nghiệp công khai đã được rà soát.

## Thu phí và giới hạn lời quảng cáo

Giá `$3/1.000 domain` là giả thuyết ban đầu; cần được cấu hình thật trong Apify và đối chiếu sự kiện billing với code. Website đọc được nhưng không có email vẫn có thể là một domain đã xử lý; nêu rõ điều đó cho khách. Đầu vào sai, trùng lặp và trang không đọc được cần được xử lý theo quy tắc billing công bố, không tính ngầm như kết quả thành công.

Không công bố số khách, đánh giá, tỷ lệ thành công, benchmark tốc độ hoặc doanh thu khi chưa có bằng chứng. Gắn nhãn “đề xuất” cho mức giá chưa bật. Không hứa Google ranking, khách hàng tiềm năng mua hàng hoặc thu nhập thụ động.

Chủ tài khoản tự đăng nhập, hoàn tất thông tin thanh toán và KYC. Chỉ đánh dấu đã deploy/publish khi có URL và run thành công để kiểm tra; chỉ đánh dấu đã nhận tiền khi có giao dịch thực tế. [Quy định nhận tiền chính thức](https://docs.apify.com/actors/publishing/monetize/monthly-payouts).
