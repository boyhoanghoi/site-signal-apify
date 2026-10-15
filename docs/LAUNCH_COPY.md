# SiteSignal — bản nháp nội dung ra mắt

Nội dung bên dưới là bản nháp. Chỉ dùng mô tả đúng tính năng bản phát hành đã kiểm thử. Thay các placeholder bằng URL thật sau khi deploy; không đăng nguyên placeholder. Chưa có tuyên bố khách hàng, doanh thu hoặc đánh giá nào.

## Apify Store title

**Website Contact & Tech Scraper | Emails, Socials, CMS**

Tên sản phẩm: **SiteSignal**. Slug gợi ý: `website-contact-tech-scraper`.

## Short description

Turn business websites into clean contact profiles: public emails, phones, social links and technology signals, with source evidence. One row per domain. Shallow HTTP crawl, no login or paid enrichment API.

## English README copy

### What does SiteSignal do?

SiteSignal turns a list of business websites into a structured contact and technology dataset. Use it to enrich an existing CRM, research partners or prepare a spreadsheet for manual review.

It reads publicly accessible HTML, follows a limited number of relevant pages on the same site, and returns one result per website. Source links let you check where extracted information came from.

### What can it extract?

- Public email addresses observed on the pages it reads.
- Published phone links and social profile links.
- Organization name and contact page information where available.
- Recognizable CMS, ecommerce, analytics and other technology signals in HTML.
- Extraction status and crawl metadata, including unsuccessful websites.

Technology matches are evidence of a signature in the fetched page, not a complete or verified inventory of a company's software. An email observed on a website has not been tested for mailbox existence or deliverability.

### How to use it

1. Open the Actor's Input tab and add the business website URLs you want to process.
2. Start with a small page budget and a few domains.
3. Run the Actor, inspect its dataset and check source links for a sample of the records.
4. Export the dataset through Apify as JSON, CSV or Excel, or use the Actor API from your workflow.

Start with the sample supplied in the input form. Use the API examples generated in your published Actor's API tab so the Actor ID and authentication are correct.

Example input (replace the demonstration domains with websites you want to process):

```json
{
  "websites": ["https://example.com", "https://www.iana.org"],
  "maxPagesPerSite": 3,
  "maxSites": 100,
  "concurrency": 5,
  "timeoutSeconds": 20,
  "respectRobots": true,
  "minDelaySeconds": 0.5,
  "includeTechnology": true
}
```

You can also supply URL objects such as `{"url":"https://example.com"}` in `websites`. Duplicate domains are processed once. The maximum page budget is five pages per site.

### Output fields

| Field | Meaning |
| --- | --- |
| `url`, `finalUrl`, `domain` | Input, final landing URL and normalized domain |
| `companyName`, `title`, `description` | Organization and page metadata when present |
| `emails`, `phones`, `socials` | Observed contact values and social profiles grouped by platform |
| `contactFormUrls` | Pages where contact forms were observed |
| `technologies` | Matches with name, category, evidence and source URL |
| `evidence` | Contact evidence containing type, value, source URL and method |
| `pagesVisited`, `pagesChecked`, `observedAt` | Scope and time of the observation |
| `status`, `warnings` | Extraction outcome and important limitations |

Failed website diagnostics are available in `OUTPUT`, with statuses such as `blocked`, `timeout`, `robots_disallowed`, `http_error` or `network_error`. Check this record as well as the successful results dataset when reconciling an input list.

### Run locally

After installing this repository's dependencies as described in its main README:

```powershell
python -m sitesignal run --input examples/input.json --output ./output
```

Local processing does not activate Apify billing or publish the Actor. For remote API access, open the published Actor's API tab and use its generated request with your account's token stored outside the repository.

### Pricing

Proposed launch pricing is **$3 per 1,000 successfully processed domains** ($0.003 each). The published Pricing tab is authoritative; this draft does not activate billing.

One successfully processed website produces one billing event. An accessible website may publish no email; an empty email list is still a completed extraction. Failed or blocked websites are reported separately and are not billed as successful domains. Check the released implementation and Pricing tab for the exact event and configured price before publishing this section.

### Limitations

This Actor uses ordinary HTTP requests. It does not run JavaScript, log into websites, solve CAPTCHAs, bypass access restrictions or query a private contact database. Some websites will expose only a contact form, block automated requests or render their details with JavaScript.

No email, phone number, contact person or technology is guaranteed to be found. Site owners can change their pages. Shallow crawling trades coverage for a predictable crawl budget. Always review extraction status instead of interpreting every empty field as proof that information does not exist.

Only process sites and data you are authorized to use, and use the output responsibly. The Actor extracts data; it does not send outreach messages.

### Support

Open an issue through the Actor's Issues tab. Include the public website URL, run ID, expected field and what you observed. Remove tokens, private customer data and personal documents from reports.

## Bài giới thiệu tiếng Việt

Mình làm SiteSignal cho việc bổ sung thông tin từ danh sách website doanh nghiệp: email công khai, social và dấu hiệu CMS/analytics, kèm link nguồn để kiểm tra lại. Đầu ra một dòng/domain, xuất được CSV qua Apify.

Tool đọc HTML và crawl nông; website dùng JavaScript hoặc chặn crawler có thể không lấy được. Không xác minh email có nhận thư hay không.

Mình đang tìm phản hồi từ người có workflow CRM/Excel thực tế. Nếu cộng đồng cho phép, bạn có thể thử vài domain và cho mình biết cột nào hữu ích, cột nào còn sai. Giá và điều kiện tính phí nằm ở tab Pricing của Actor.

Link Actor: `[THAY_BANG_URL_STORE_THAT]`

## English launch post

I built SiteSignal to turn an existing list of company websites into contact and technology profiles, with source links for checking the results. It returns one row per domain and exports through Apify.

The first version uses a shallow HTML crawl. It can miss JavaScript-rendered details, and it does not verify email deliverability or bypass blocked websites.

If you already enrich CRM or spreadsheet records, I would appreciate feedback on a small test with your own website list: which fields save you time, and where does the output need correction?

Actor: `[REPLACE_WITH_LIVE_STORE_URL]`

Chỉ đăng bài trong nơi cho phép self-promotion hoặc kênh bạn sở hữu. Không sử dụng danh sách email trích xuất để quảng cáo tool hàng loạt.
