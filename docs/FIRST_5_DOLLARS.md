# Kế hoạch đạt doanh thu đầu tiên với SiteSignal

Mục tiêu là có **người dùng thật trả tiền cho Actor hữu ích**. Không có cam kết thời hạn hay thu nhập. Website giới thiệu và mã nguồn không tự tạo doanh thu; Actor cần được xuất bản, bật billing đúng và có khách dùng.

## Trước khi nhận khách

1. Chạy local và kiểm thử theo README gốc. Chọn 20–30 website mẫu công khai, kiểm tra thủ công kết quả và bằng chứng. Ghi riêng trang bị chặn, trang chỉ có form và trang dùng JavaScript.
2. Đăng nhập tài khoản Apify của bạn. Nếu môi trường chưa xác thực, dùng `apify login` tại máy của bạn; không gửi token hoặc giấy tờ qua chat và không commit bí mật vào GitHub.
3. Deploy Actor theo README; chạy thử bằng tài khoản của bạn, đọc log và kiểm tra CSV/JSON. Chỉ công bố link Store sau khi link thực sự hoạt động.
4. Trong Actor → Publishing, cấu hình monetization PPE. Giá **đề xuất**, chưa mặc định được bật chỉ vì có trong tài liệu: `$0.003` cho mỗi domain xử lý thành công, tức `$3/1.000`. Tên sự kiện billing phải khớp code. Kiểm tra giới hạn số kết quả và giới hạn charge hoạt động.
5. Đối chiếu bảng giá Store với lượt chạy thực tế: trùng domain không tính hai lần; đầu vào lỗi và website không đọc được không phát sinh sự kiện trả phí. Website đọc thành công nhưng không công khai email vẫn là một kết quả đã xử lý; mô tả rõ trước khi thu tiền.

Tham khảo [thiết lập monetization của Apify](https://docs.apify.com/actors/monetize/set-up-monetization). Trạng thái publish/billing phải được xác nhận trong Console; tài liệu này không thay thế bước đó.

## Phân biệt $5 doanh thu, lợi nhuận và tiền rút

Theo [cách Apify tính PPE](https://docs.apify.com/actors/publishing/monetize/pricing-and-costs), phần của tác giả được tính bằng `0.8 × doanh thu đủ điều kiện − chi phí nền tảng`. Lượt của khách gói Free không tạo doanh thu tác giả trong phép tính này. Vì vậy, lượt thử miễn phí giúp kiểm chứng sản phẩm nhưng không được cộng nhầm thành tiền kiếm được.

Với giá giả định `$0.003/domain`:

| Mốc | Số domain thành công cần có |
| --- | ---: |
| $5 khách bị tính phí, trước chia sẻ/chi phí | `ceil(5 / 0.003)` = **1.667** |
| $5 lợi nhuận tác giả, giả sử chi phí bằng 0 | `ceil(5 / 0.0024)` = **2.084** |
| $5 lợi nhuận, giả sử chi phí $0.0005/domain | `ceil(5 / 0.0019)` = **2.632** |

Chi phí `$0.0005/domain` chỉ là **ví dụ toán học, chưa phải benchmark**. Hãy lấy chi phí thực từ run Apify. Nếu chi phí bình quân là `c`, lợi nhuận/domain là `0.0024 − c`. Nếu kết quả không dương, phải giảm ngân sách crawl hoặc điều chỉnh giá; thêm lượt chạy không giải quyết được biên lợi nhuận âm. Chưa tính phí nhận tiền và nghĩa vụ thuế cá nhân.

**Có $5 lợi nhuận chưa đủ rút PayPal.** [Quy định payout hiện tại](https://docs.apify.com/actors/publishing/monetize/monthly-payouts) đặt ngưỡng $20 cho PayPal/Wise, yêu cầu thông tin thanh toán và xác minh danh tính; lịch phát lệnh thường ngày 21–25 hằng tháng. Các khoản chưa đủ ngưỡng được chuyển kỳ. Tình trạng đủ điều kiện và khoản thực nhận phải kiểm tra trong Console.

## Những việc chủ tài khoản phải tự hoàn tất

- Điền thông tin billing hợp lệ và chọn phương thức thanh toán được hỗ trợ cho tài khoản của mình.
- Tự thực hiện KYC trong Apify và thiết lập PayPal/Wise; kiểm tra tên, quốc gia, phí và khả năng nhận tiền của chính tài khoản.
- Bảo quản token, bật xác thực tài khoản phù hợp, kiểm tra hóa đơn/lịch payout và xử lý nghĩa vụ thuế liên quan.

Code có thể chuẩn bị deploy và billing nhưng không thay bạn xác minh danh tính hoặc tạo điều kiện thanh toán hợp lệ.

## Tìm 1–3 người dùng đầu tiên

Chỉ đăng ở kênh bạn sở hữu, cộng đồng bạn đã tham gia cho phép giới thiệu sản phẩm, hoặc thread self-promotion được quản trị cho phép. Đọc quy định từng nơi. Nội dung trong [LAUNCH_COPY.md](LAUNCH_COPY.md) là bản nháp để bạn xem rồi tự đăng; dự án không chứa bot spam hay tự nhắn khách.

1. Chuẩn bị video/GIF 30–60 giây: dán 5 domain → chạy → xem nguồn → xuất CSV. Dùng dữ liệu mẫu công khai, che dữ liệu tài khoản, ghi rõ giới hạn HTML/JavaScript.
2. Chọn đúng một nhóm: người đang làm sạch dữ liệu CRM hoặc agency cần bổ sung website cho khách. Chia sẻ đầu ra và câu hỏi cụ thể: “Với bảng website hiện tại, cột này có tiết kiệm công chép tay cho bạn không?”.
3. Mời tự nguyện thử một danh sách nhỏ trên tài khoản Apify của họ. Ghi lại lỗi và sửa tính chính xác trước. Không hứa tặng tiền, không yêu cầu tạo tài khoản giả hay đánh giá có thưởng.
4. Nếu họ dùng được, đề nghị chạy danh sách thật qua Actor theo giá công khai. Không gửi hàng loạt hoặc lấy danh sách liên hệ của Actor để tự quảng cáo.
5. Sau 7 ngày, xem nguồn truy cập, người thử, lượt quay lại, số domain đủ điều kiện tính phí, chi phí và lợi nhuận. Nếu chỉ có lượt dùng miễn phí, cần cải thiện giá trị/tiếp cận; không gọi đó là doanh thu.

Mốc hoàn thành đầu tiên nên là **một lượt chạy trả phí có kết quả đúng và phản hồi cụ thể**, rồi mới theo dõi $5 lợi nhuận và ngưỡng payout. Đừng mua proxy, quảng cáo hoặc server trước khi đã đo được nhu cầu và biên lợi nhuận.
