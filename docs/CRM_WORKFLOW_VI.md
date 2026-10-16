# Từ danh sách website đến dữ liệu để nhập CRM

SiteSignal dành cho agency hoặc người nghiên cứu doanh nghiệp đã có danh sách
website. Công cụ đọc dữ liệu công khai, giữ nguồn để kiểm tra, rồi xuất các
trường phẳng để bạn tự ghép cột vào CRM. Công cụ không tự ghi vào CRM và không
gửi email, gọi điện hay gửi form.

## 1. Thử với một website

Mở [Actor trên Apify](https://apify.com/reliable_quatrain/business-website-contact-tech-scraper)
và chạy đầu vào nhỏ:

```json
{
  "websites": ["https://plausible.io/"],
  "maxSites": 1,
  "maxPagesPerSite": 3,
  "respectRobots": true,
  "includeTechnology": true
}
```

Đây là website công khai để thử, không phải khách hàng của dự án. Một website
đọc thành công vẫn có thể không công khai email hoặc số điện thoại.
Đặt giới hạn chi phí chạy trong Console trước khi bắt đầu. Giá hiện được cấu
hình là $0.003/website được lưu thành công; xem Pricing để kiểm tra giá đang áp dụng.

## 2. Chọn đúng tệp ở Output

| Tệp/khóa | Dùng khi nào |
| --- | --- |
| `CRM_COMPANIES` | JSON: mỗi website một dòng, các trường công ty phẳng để ghép cột trong tích hợp CRM |
| `crm-companies.csv` | Cùng dữ liệu công ty, tiện mở bảng tính hoặc tự ghép cột khi nhập CRM |
| `CONTACTS` | JSON: toàn bộ email, điện thoại, hồ sơ xã hội và trang form được giữ lại, mỗi liên hệ một dòng |
| `contacts.csv` | Duyệt các liên hệ và nguồn trong bảng tính |
| `RESULTS`, `results.csv` | Toàn bộ hồ sơ website, gồm công nghệ và chẩn đoán từng trang |
| `DIAGNOSTICS` | Website bị chặn, thất bại hoặc bị bỏ qua; không có phí sự kiện website thành công |

Các tệp mới chỉ là góc nhìn khác của những website đã lưu thành công, không
tính thêm sự kiện thu phí theo số liên hệ hay số tệp.

## 3. Ghép trường công ty

| Trường SiteSignal | Gợi ý ghép vào CRM |
| --- | --- |
| `companyName` | Tên doanh nghiệp; để trống nếu website không công bố tên theo nguồn hỗ trợ |
| `domain`, `website` | Tên miền và website công ty |
| `email`, `phone` | Một email và một số điện thoại quan sát được |
| `emailSourceUrls`, `phoneSourceUrls` | URL nguồn để kiểm tra lại |
| `linkedin`, `facebook`, `instagram`, `x`, `youtube`, `tiktok`, `github`, `pinterest` | Một URL hồ sơ cho từng nền tảng, nếu có |
| `contactPageUrl`, `contactFormUrl` | Trang liên hệ và trang có form |
| `technologyNames` | Tên công nghệ quan sát được, phân tách bằng dấu chấm phẩy |
| `emailCount`, `phoneCount` | Số liên hệ để biết có cần mở bản CONTACTS đầy đủ không |
| `observedAt` | Thời điểm đọc dữ liệu |

Nếu có nhiều email hoặc số điện thoại, cột đơn chọn giá trị đầu tiên theo thứ
tự chữ cái ổn định. Đây không phải đề xuất người nên liên hệ, email chính thức
đã xác minh hay thông tin người quyết định. Mở `CONTACTS` và URL nguồn để chọn
giá trị phù hợp với mục đích của bạn.

Các địa chỉ chỉ khác cách viết hoa/thường được gộp trong cùng một website theo
quy tắc của bộ trích xuất, giữ cách viết đầu tiên và nguồn của các lần xuất
hiện. Một địa chỉ xuất hiện trên hai website vẫn là hai quan sát riêng.

CSV thêm dấu nháy đơn trước các ô có thể thành công thức, bao gồm số điện thoại
bắt đầu bằng `+`. Một số CRM sẽ giữ cả dấu nháy này. Dùng JSON nếu tích hợp cần
giữ nguyên giá trị chính xác. Không tự bỏ lớp bảo vệ trong bảng tính chứa dữ
liệu chưa được kiểm tra.

## 4. Kiểm tra mức bao phủ trước khi dùng

Trong view **Coverage and failed contact pages**:

- `pagesChecked`: số trang HTML đọc và trích xuất thành công.
- `pagesAttempted`: trang đầu và các trang liên hệ đã thử, gồm cả lần bị chặn,
  lỗi hoặc chuyển hướng về trang đã đọc. Không đếm robots.txt và từng bước chuyển hướng.
- `pageDiagnostics`: URL đã thử, URL cuối nếu có, trạng thái, mã HTTP và lý do lỗi.
- `contactPageLimitReached`: còn liên kết liên hệ cùng website chưa được thử khi
  chạm giới hạn trang. Giá trị `false` không có nghĩa đã quét toàn bộ website.

Trang đầu có thể thành công nhưng trang liên hệ bị chặn. Khi đó website vẫn
được lưu và tính phí một lần, còn URL lỗi được ghi riêng trong `pageDiagnostics`.
Không nên hiểu email trống là doanh nghiệp chắc chắn không có email.

Mọi liên hệ đều là **quan sát công khai chưa xác minh**. Không kiểm tra hộp thư
có tồn tại, khả năng nhận thư, quyền sở hữu hay sự đồng ý nhận liên hệ. Các trang
cần JavaScript, đăng nhập hoặc bị chặn có thể không đọc được.
