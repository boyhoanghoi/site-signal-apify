# SiteSignal: thị trường và giả thuyết cần kiểm chứng

Ngày kiểm tra nguồn: **15/10/2026**. Đây là nghiên cứu ban đầu để chọn một Actor có thể bán, không phải dự báo doanh thu.

Trạng thái triển khai: [SiteSignal đã công khai trên Apify Store](https://apify.com/reliable_quatrain/business-website-contact-tech-scraper), PPE **`website-enriched`, $0.003/domain thành công ($3/1.000)** đang active, được xác nhận qua API chính thức và Console. Chưa có doanh thu khách hàng được xác minh; lượt chủ tài khoản chạy thử không phải bằng chứng nhu cầu trả phí. KYC vẫn đang chờ xét duyệt theo ảnh Console mới nhất.

## Sản phẩm và khách hàng đầu tiên

**SiteSignal — Website Contact, Social & Tech Extractor** nhận danh sách website doanh nghiệp và tạo bảng thông tin để bổ sung dữ liệu CRM: email công khai, điện thoại, mạng xã hội, dấu hiệu công nghệ và URL nguồn. Website đọc thành công có một dòng dataset, kể cả khi không thấy email. Website lỗi, bị chặn hoặc được bỏ qua có diagnostics riêng, không được tính như kết quả thành công.

Khách phù hợp để kiểm chứng: freelancer làm dữ liệu, agency web/marketing và người vận hành workflow n8n/Make đã có danh sách website. Họ cần tiết kiệm thời gian mở từng trang, chép thông tin và tìm lại nguồn. Actor không tự tìm danh sách khách, gửi email hoặc hứa tìm được người ra quyết định.

## Quan sát trên Apify Store

Số liệu dưới đây là những gì trang sản phẩm hiển thị khi kiểm tra; số làm tròn như 63K không phải số chính xác từng tài khoản. Giá “from” có thể phụ thuộc gói khách hàng. Monthly active users là mức sử dụng, **không chứng minh số khách trả tiền hay lợi nhuận của tác giả**.

| Actor | Tổng người dùng | Người dùng/tháng | Đánh giá | Giá hiển thị từ |
| --- | ---: | ---: | --- | --- |
| [vdrmota/contact-info-scraper](https://apify.com/vdrmota/contact-info-scraper) | 63K | 2.9K | 4.7/5, 92 đánh giá | $1.05/1.000 trang |
| [rp_openpro.ai/contact-details-scraper](https://apify.com/rp_openpro.ai/contact-details-scraper) | 322 | 28 | 5/5, 1 đánh giá | $1.60/1.000 domain |
| [poidata/contact-details-scraper](https://apify.com/poidata/contact-details-scraper) | 291 | 23 | Không ghi nhận trong bản đọc | $1.25/1.000 domain |
| [solidscrape/contact-details-scraper](https://apify.com/solidscrape/contact-details-scraper) | 43 | 31 | Chưa có đánh giá | $1.25/1.000 kết quả |
| [italy/ats-jobs-scraper](https://apify.com/italy/ats-jobs-scraper) | 2 | 1 | Chưa có đánh giá | $3/1.000 tin việc |
| [egeusta/ats-job-scraper](https://apify.com/egeusta/ats-job-scraper) | 2 | 1 | Chưa có đánh giá | $0.75/1.000 tin việc |

**Suy luận:** website enrichment có dấu hiệu sử dụng thực tế ở cả đối thủ lớn và nhỏ, rõ hơn các Actor multi-ATS tìm được. Đổi lại, cạnh tranh cao; chỉ có mặt trên Store chưa đủ thu hút khách. Đối thủ rẻ hơn đã tồn tại nên không cạnh tranh bằng lời hứa “rẻ nhất”.

## Điểm khác biệt cần chứng minh bằng kết quả

- Có bằng chứng nguồn để người dùng kiểm tra email, social và công nghệ, thay vì một bảng không rõ xuất xứ.
- Một dòng/domain, loại trùng đầu vào, phù hợp nhập CRM và bảng tính.
- Kết quả phân biệt không tìm thấy, lỗi mạng, bị chặn và robots; không gộp thành “website không có email”.
- Ngân sách crawl nhỏ, giá dễ hiểu; không phụ thuộc API enrichment bên ngoài.

Đây là tiêu chí sản phẩm, không phải tuyên bố độc quyền. Chỉ quảng bá những mục đã được kiểm thử trong bản triển khai.

## Kiểm chứng trong 7 ngày sau khi xuất bản

1. Chạy bộ 20–30 website đa dạng: HTML thường, có/không có email, form liên hệ, chuyển hướng, trang dùng JavaScript, trang từ chối crawler. Kiểm tra thủ công bằng chứng và ghi chi phí.
2. Cho 3–5 người đúng nhóm dùng thử trên danh sách họ có quyền sử dụng; hỏi họ định dùng cột nào và còn phải sửa tay gì.
3. Đo: tỷ lệ hoàn tất, thông tin sai, chi phí/100 domain, người quay lại và lượt chạy của khách gói trả phí. Không coi test của mình là khách hàng.
4. Nếu không ai cần đầu ra, điều chỉnh một workflow cụ thể trước khi thêm tính năng. Nếu chặn/JavaScript là nhu cầu chính, phải tính lại giá và chi phí trước khi thêm trình duyệt.

Mức giá **$3/1.000 domain xử lý thành công** đã active. Khả năng thu hút khách và biên lợi nhuận vẫn cần kiểm chứng bằng khách thật và chi phí thực tế. Kế hoạch tìm khách và phép tính trong [FIRST_5_DOLLARS.md](FIRST_5_DOLLARS.md); nguồn trạng thái phát hành trong [LAUNCH_STATUS.md](LAUNCH_STATUS.md).
