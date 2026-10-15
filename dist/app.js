import * as configModule from './config.js';

const publicConfig = configModule.publicConfig || configModule.config || configModule.default || {};

const dynamicEnglish = {
  allTechnologies: 'All technologies', resultCount: '{count} of {total} companies',
  emailCount: '{count} email', emailCountPlural: '{count} emails', noPublicEmail: 'No email found',
  inspectCompany: 'Inspect {company}', sourceEvidence: 'SOURCE EVIDENCE', sample: 'SAMPLE',
  pagesChecked: '{count} pages checked', findingsCount: '{count} findings',
  emailFinding: 'Public email', phoneFinding: 'Phone link', socialFinding: 'Social profile',
  techFinding: 'Technology signal', formFinding: 'Contact form', nameFinding: 'Page title',
  inspectorNote: 'Fictional sample. A detected signal is not a guarantee. Email deliverability has not been verified.',
  noSelection: 'Select a company to inspect the sample evidence.', sourceLink: 'Sample source: {source}',
  hideRawJson: 'Hide raw JSON', downloadSuccess: 'Sample {format} downloaded ({count} companies).',
  configDownloaded: 'Run configuration downloaded. No crawl has been started.', configCopied: 'Input JSON copied.',
  copyFailed: 'Copy is unavailable here. Select the JSON text or download the file.',
  emptyInput: 'Add at least one public website, one per line.',
  invalidWebsite: 'Line {line}: “{value}” is not a supported public website. Use a domain such as example.com or an HTTP(S) URL. Local addresses, IPs, credentials, and reserved domains are not accepted.',
  tooManySites: 'Use no more than 100 unique websites in one configuration.',
  invalidMaxSites: 'Maximum sites must be a whole number from 1 to 100.',
  invalidMaxPages: 'Pages per website must be a whole number from 1 to 5.',
  limitTooLow: 'You entered {count} unique websites but set a limit of {max}. Increase the limit or shorten the list.',
  configReady: '{count} unique websites. Configuration ready; no crawl has been started.',
  duplicatesRemoved: ' {count} duplicate entries removed.', openNav: 'Open navigation', closeNav: 'Close navigation',
  openActor: 'Open Actor on Apify', actorLive: 'Live on Apify Store',
  actorLiveNote: 'Generate the configuration below, then open the Actor on Apify and paste the JSON into its input.',
  observedAt: 'Illustrative observation: {date}', emptyCsv: 'No matching sample rows to export.',
  allEvidence: 'All {count} source findings', partialSample: 'Partial sample',
};

const vietnamese = {
  skip: 'Chuyển đến nội dung', navExplore: 'Xem dữ liệu', navHow: 'Cách hoạt động', navPricing: 'Chi phí',
  getConfigShort: 'Bắt đầu', getConfig: 'Tạo cấu hình chạy',
  heroEyebrow: 'Bớt tìm kiếm thủ công. Thêm dữ liệu hữu ích.',
  heroLine1: 'Từ website.', heroLine2: 'Dữ liệu hữu ích.', heroLine3: 'Có nguồn rõ ràng.',
  heroDescription: 'Biến danh sách website thành thông tin liên hệ công khai, hồ sơ mạng xã hội và dấu hiệu công nghệ. Biết bạn tìm thấy gì — và chính xác dữ liệu đến từ đâu.',
  exploreDemo: 'Khám phá dữ liệu mẫu', heroFootnote: 'Dữ liệu công khai. Có bằng chứng. Sẵn sàng để sử dụng.',
  heroVisualLabel: 'Minh họa website được chuyển thành dữ liệu có cấu trúc', illustrativeSample: 'Mẫu minh họa',
  publicEmail: 'Email công khai', platform: 'Nền tảng', marketing: 'Marketing', evidenceAttached: 'Kèm nguồn bằng chứng',
  threePages: '3 trang', noGuessing: 'Dữ liệu có thể đối chiếu.', demoNotLive: 'Doanh nghiệp giả định · không quét trực tiếp',
  useCases: 'Trường hợp sử dụng', builtFor: 'Dành cho bước tiếp theo của bạn', useCaseAgencies: 'Nghiên cứu cho agency',
  useCaseEnrichment: 'Bổ sung dữ liệu doanh nghiệp', useCaseMarket: 'Khảo sát thị trường', useCaseTech: 'Nghiên cứu công nghệ',
  explorerEyebrow: 'MỞ DỮ LIỆU, BỚT MỞ THÊM TAB', explorerTitle: 'Thông tin hữu ích.', explorerTitleEm: 'Trong một nơi.',
  explorerIntro: 'Xem trước cấu trúc dữ liệu trước khi chạy. Chọn một doanh nghiệp để kiểm tra nguồn.',
  sampleDataset: 'Dữ liệu mẫu', demoBadge: 'MẪU',
  demoNotice: 'Chỉ để minh họa. Tất cả doanh nghiệp, liên hệ và kết quả .example đều giả định. Trang này chưa quét website nào.',
  searchLabel: 'Tìm trong dữ liệu mẫu', searchPlaceholder: 'Tìm doanh nghiệp, tên miền, công nghệ…',
  technologyFilter: 'Lọc theo công nghệ', allTechnologies: 'Tất cả công nghệ', hasEmail: 'Có email công khai',
  company: 'Doanh nghiệp', contacts: 'Liên hệ', technology: 'Công nghệ', inspect: 'Xem chi tiết',
  resultsTableLabel: 'Bảng dữ liệu mẫu có thể cuộn', noResults: 'Không có doanh nghiệp phù hợp với bộ lọc.', clearFilters: 'Xóa bộ lọc',
  clickToInspect: 'CHỌN MỘT DÒNG ĐỂ XEM ↗', inspectorLabel: 'Nguồn của doanh nghiệp được chọn',
  exportsFiltered: 'Tải xuống các dòng mẫu đang được lọc.', viewRawJson: 'Xem JSON gốc', hideRawJson: 'Ẩn JSON gốc',
  evidenceEyebrow: 'NGỮ CẢNH TẠO NÊN KHÁC BIỆT', evidenceTitle: 'Tìm thấy là một bước.', evidenceTitleEm: 'Có nguồn mới dùng được.',
  evidenceDescription: 'Một địa chỉ email thiếu ngữ cảnh chỉ là một ô trong bảng tính. SiteSignal giữ lại trang công khai và cách phát hiện cùng kết quả, để bạn kiểm tra trước khi quyết định bước tiếp theo.',
  inspectSample: 'Kiểm tra một kết quả mẫu', contactsHeading: 'Tìm cách liên hệ công khai',
  contactsDescription: 'Email được đăng công khai, liên kết điện thoại, biểu mẫu liên hệ và mạng xã hội. Không đoán email hay dùng cơ sở dữ liệu riêng tư.',
  techHeading: 'Hiểu nền tảng của website', techDescription: 'Nhận diện dấu hiệu CMS, bán hàng, phân tích và marketing trong HTML. Dấu hiệu phát hiện được không phải là sự bảo đảm.',
  workflowHeading: 'Tiếp nối quy trình của bạn', workflowDescription: 'Lấy JSON hoặc CSV từ bộ dữ liệu Actor. Kiểm tra kết quả chưa đầy đủ và nguồn trước khi đưa vào công cụ của bạn.',
  configureEyebrow: 'ĐẦU VÀO GỌN. BƯỚC TIẾP THEO RÕ RÀNG.', configureTitle: 'Bắt đầu với', configureTitleEm: 'website của bạn.',
  configureIntro: 'Chuẩn bị đầu vào cho Apify Actor SiteSignal. Trang này tạo cấu hình ngay trong trình duyệt; việc quét thật được thực hiện trên Apify.',
  publicationPending: 'Actor đang chờ xuất bản', publicationNote: 'Bạn có thể xem dữ liệu mẫu và tải cấu hình ngay bây giờ. Liên kết Actor sẽ xuất hiện sau khi được xuất bản.',
  localPrivacy: 'Website bạn nhập được giữ trong trình duyệt ở trang này. Biểu mẫu không gửi dữ liệu lên máy chủ.',
  inputStep: '01 — Cấu hình', websiteLabel: 'URL website', websiteHint: 'Mỗi dòng một website công khai. Có thể nhập tên miền. Tối đa 100 website.',
  pagesLabel: 'Số trang mỗi website', maxSitesLabel: 'Giới hạn website', robotsNote: 'Tôn trọng robots.txt luôn được bật trong cấu hình này.',
  generateConfig: 'Tạo cấu hình', copyConfig: 'Sao chép JSON đầu vào', downloadConfig: 'Tải JSON đầu vào',
  configPlaceholder: 'Cấu hình chạy của bạn sẽ xuất hiện ở đây.', openActor: 'Mở Actor trên Apify',
  howEyebrow: 'GIỮ QUY TRÌNH ĐƠN GIẢN', howTitle: 'Từ danh sách đến bộ dữ liệu.',
  howIntro: 'Ba bước có chủ đích. Bạn kiểm soát đầu vào, giới hạn và cách sử dụng kết quả.',
  stepOneTitle: 'Chuẩn bị website', stepOneDescription: 'Nhập tên miền doanh nghiệp công khai bạn muốn nghiên cứu. Bắt đầu với giới hạn số trang nhỏ.',
  stepTwoTitle: 'Chạy Actor', stepTwoDescription: 'Dán JSON đã tạo vào Actor trên Apify rồi bắt đầu chạy. Actor lấy dữ liệu từ những trang công khai được phép truy cập.',
  stepThreeTitle: 'Kiểm tra rồi sử dụng', stepThreeDescription: 'Đối chiếu nguồn, kiểm tra kết quả chưa đầy đủ rồi xuất dữ liệu. Chọn thông tin phù hợp với quy trình của bạn.',
  pricingEyebrow: 'CHI PHÍ KHỞI ĐẦU RÕ RÀNG', pricingTitle: 'Nhỏ để dễ thử.', pricingTitleEm: 'Hữu ích để dùng tiếp.',
  pricingDescription: 'Actor tính phí theo mức sử dụng, dành cho các đợt nghiên cứu nhỏ và lặp lại. Bắt đầu với vài website rồi xem kết quả.',
  pricingDisclaimer: 'Tính phí cho mỗi website xử lý thành công, kể cả khi không có liên hệ công khai. Website lỗi, bị chặn và trùng đích chuyển hướng không bị tính phí. Xem giá hiện hành và chi phí nền tảng nếu có trên Apify.',
  launchPricing: 'GIÁ ACTOR', payAsYouGo: 'DÙNG ĐẾN ĐÂU TRẢ ĐẾN ĐÓ', perSites: '/ 1.000 website',
  priceUnit: '$0,003 cho mỗi website xử lý thành công.', priceFeature1: 'Liên hệ công khai và mạng xã hội',
  priceFeature2: 'Dấu hiệu công nghệ kèm nguồn', priceFeature3: 'Đầu ra JSON và CSV có cấu trúc', priceFeature4: 'Tùy chỉnh giới hạn quét',
  noPaymentHere: 'Không thu thập thông tin thanh toán tại đây.', faqEyebrow: 'TRƯỚC KHI CHẠY', faqTitle: 'Điều bạn cần biết.',
  faqIntro: 'Kỳ vọng rõ ràng giúp dữ liệu hữu ích hơn.', faq1Q: 'Trang này có quét website không?',
  faq1A: 'Không. Trang này cho phép xem dữ liệu giả định và tạo đầu vào Actor ngay trong trình duyệt. Mở Actor trên Apify, dán JSON đầu vào rồi bắt đầu chạy để quét website thật.',
  faq2Q: 'Có tìm được mọi email và công nghệ không?',
  faq2A: 'Không. Kết quả phụ thuộc vào những trang công khai được truy cập và dấu hiệu trong HTML. Email không được đoán hoặc xác minh khả năng nhận thư. Nhận diện công nghệ có thể thiếu hoặc chưa chắc chắn; hãy kiểm tra bằng chứng. Không tìm thấy dữ liệu không có nghĩa doanh nghiệp không có liên hệ hay không dùng công nghệ đó.',
  faq3Q: 'Website được bảo vệ hoặc chạy JavaScript thì sao?',
  faq3A: 'Nội dung chỉ được tạo bằng JavaScript có thể không có trong quá trình quét HTML. Actor tôn trọng robots.txt theo mặc định; không vượt qua đăng nhập, CAPTCHA, giới hạn truy cập hay bảo vệ chống bot. Kết quả bị chặn hoặc chưa đầy đủ cần được xem xét lại.',
  faq4Q: 'Có thể dùng dữ liệu để tiếp thị không?',
  faq4A: 'Công khai không đồng nghĩa với cho phép gửi quảng cáo. Hãy xem điều khoản website, quy định bảo vệ dữ liệu và tiếp thị áp dụng, cùng mục đích xử lý dữ liệu của bạn. SiteSignal không gửi tin nhắn hay tự động spam.',
  faq5Q: 'Website này lưu những gì?',
  faq5A: 'Biểu mẫu URL, bộ lọc và tải xuống chạy trong trình duyệt. Trang không tải đầu vào biểu mẫu lên máy chủ. Lựa chọn ngôn ngữ có thể được lưu cục bộ. Các lượt chạy Actor và dữ liệu được Apify xử lý trong tài khoản của bạn theo cài đặt lưu trữ.',
  closingTitle: 'Bớt chuyển tab.', closingTitleEm: 'Thêm ngữ cảnh hữu ích.', footerTagline: 'Tìm dữ liệu. Giữ lại nguồn.',
  runConfiguration: 'Cấu hình chạy', sourceOnGithub: 'Mã nguồn GitHub', footerNote: 'Công cụ nghiên cứu độc lập. Không liên kết với Apify.',
  resultCount: '{count} / {total} doanh nghiệp', emailCount: '{count} email', emailCountPlural: '{count} email', noPublicEmail: 'Chưa tìm thấy email',
  inspectCompany: 'Xem chi tiết {company}', sourceEvidence: 'NGUỒN BẰNG CHỨNG', sample: 'MẪU', pagesChecked: 'Đã kiểm tra {count} trang',
  findingsCount: '{count} kết quả', emailFinding: 'Email công khai', phoneFinding: 'Liên kết điện thoại', socialFinding: 'Hồ sơ mạng xã hội',
  techFinding: 'Dấu hiệu công nghệ', formFinding: 'Biểu mẫu liên hệ', nameFinding: 'Tiêu đề trang',
  inspectorNote: 'Dữ liệu giả định. Dấu hiệu không phải là bảo đảm. Chưa xác minh email có nhận được thư hay không.',
  noSelection: 'Chọn một doanh nghiệp để xem nguồn mẫu.', sourceLink: 'Nguồn minh họa: {source}',
  downloadSuccess: 'Đã tải {format} mẫu ({count} doanh nghiệp).', configDownloaded: 'Đã tải cấu hình. Chưa bắt đầu quét website.',
  configCopied: 'Đã sao chép JSON đầu vào.', copyFailed: 'Không thể sao chép tại đây. Hãy chọn văn bản JSON hoặc tải file.',
  emptyInput: 'Nhập ít nhất một website công khai, mỗi dòng một địa chỉ.',
  invalidWebsite: 'Dòng {line}: “{value}” chưa phải website công khai được hỗ trợ. Dùng tên miền như example.com hoặc URL HTTP(S). Không nhận địa chỉ nội bộ, IP, thông tin đăng nhập hay tên miền dành riêng.',
  tooManySites: 'Mỗi cấu hình chỉ nhận tối đa 100 website khác nhau.', invalidMaxSites: 'Giới hạn website phải là số nguyên từ 1 đến 100.',
  invalidMaxPages: 'Số trang mỗi website phải là số nguyên từ 1 đến 5.',
  limitTooLow: 'Bạn nhập {count} website khác nhau nhưng giới hạn là {max}. Hãy tăng giới hạn hoặc rút gọn danh sách.',
  configReady: '{count} website khác nhau. Cấu hình đã sẵn sàng; chưa bắt đầu quét.', duplicatesRemoved: ' Đã bỏ {count} địa chỉ trùng lặp.',
  openNav: 'Mở điều hướng', closeNav: 'Đóng điều hướng', actorLive: 'Đã xuất bản trên Apify Store',
  actorLiveNote: 'Tạo cấu hình bên dưới, mở Actor trên Apify rồi dán JSON vào phần đầu vào.', observedAt: 'Thời điểm mẫu: {date}',
  emptyCsv: 'Không có dòng mẫu phù hợp để tải xuống.', allEvidence: 'Toàn bộ {count} nguồn bằng chứng', partialSample: 'Mẫu chưa đầy đủ',
};

function makeSample(slug, companyName, emails, phones, techData, options = {}) {
  const domain = `${slug}.example`;
  const url = `https://${domain}/`;
  const contactUrl = `${url}contact`;
  const linkedin = options.linkedin ? [`https://www.linkedin.com/company/sitesignal-fictional-${slug}`] : [];
  const instagram = options.instagram ? [`https://www.instagram.com/sitesignal_fictional_${slug}/`] : [];
  const technologies = techData.map(([name, category, evidence]) => ({ name, category, evidence, sourceUrl: url }));
  const pagesVisited = options.pages === 2 ? [url, contactUrl] : [url, contactUrl, `${url}about`];
  const evidence = [
    ...emails.map(value => ({ type: 'email', value, sourceUrl: contactUrl, method: 'mailto link' })),
    ...phones.map(value => ({ type: 'phone', value, sourceUrl: contactUrl, method: 'tel link' })),
    ...technologies.map(item => ({ type: 'technology', value: item.name, sourceUrl: item.sourceUrl, method: item.evidence })),
    ...linkedin.map(value => ({ type: 'social', value, sourceUrl: url, method: 'anchor href' })),
    ...instagram.map(value => ({ type: 'social', value, sourceUrl: url, method: 'anchor href' })),
    ...(options.form ? [{ type: 'contactForm', value: contactUrl, sourceUrl: contactUrl, method: 'form with contact fields' }] : []),
  ];
  return { url, domain, companyName, emails, phones, socials: { linkedin, facebook: [], instagram, x: [], youtube: [] }, technologies,
    contactFormUrls: options.form ? [contactUrl] : [], pagesChecked: pagesVisited.length, pagesVisited,
    observedAt: '2026-10-01T09:00:00.000Z', status: options.partial ? 'partial' : 'ok', evidence };
}

export const demoDataset = [
  makeSample('northstarcoffee', 'Northstar Coffee', ['hello@northstarcoffee.example', 'wholesale@northstarcoffee.example'], ['+1-202-555-0101'], [
    ['Shopify', 'Ecommerce', 'script src: cdn.shopify.com'], ['Klaviyo', 'Marketing', 'script src: static.klaviyo.com'], ['Google Analytics', 'Analytics', 'script src: googletagmanager.com/gtag/js'],
  ], { linkedin: true, instagram: true, form: true }),
  makeSample('formandfield', 'Form & Field', ['studio@formandfield.example'], ['+1-202-555-0102'], [
    ['WordPress', 'CMS', 'HTML path: /wp-content/'], ['WooCommerce', 'Ecommerce', 'HTML class: woocommerce'],
  ], { instagram: true, form: true }),
  makeSample('harboraccounting', 'Harbor Accounting', [], ['+1-202-555-0103'], [
    ['Webflow', 'CMS', 'HTML attribute: data-wf-site'],
  ], { linkedin: true, form: true, pages: 2 }),
  makeSample('atlasbikes', 'Atlas Bikes', ['workshop@atlasbikes.example'], ['+1-202-555-0104'], [
    ['Shopify', 'Ecommerce', 'script src: cdn.shopify.com'], ['Meta Pixel', 'Analytics', 'script src: connect.facebook.net/en_US/fbevents.js'],
  ], { instagram: true, form: true }),
  makeSample('littleroots', 'Little Roots', ['care@littleroots.example'], [], [
    ['Squarespace', 'CMS', 'meta generator: Squarespace'],
  ], { instagram: true, pages: 2 }),
  makeSample('copperworks', 'Copperworks Studio', [], [], [
    ['Next.js', 'Framework', 'script src path: /_next/static/'], ['Google Analytics', 'Analytics', 'script src: googletagmanager.com/gtag/js'],
  ], { linkedin: true, form: true, partial: true }),
];

/** Validate syntax only. The Actor must still resolve DNS and enforce its network policy. */
export function normalizeWebsite(input) {
  const value = String(input).trim();
  if (!value || /\s/.test(value) || value.startsWith('//')) throw new Error('invalid_website');
  const hasScheme = /^[a-z][a-z\d+.-]*:/i.test(value);
  let parsed;
  try { parsed = new URL(hasScheme ? value : `https://${value}`); } catch { throw new Error('invalid_website'); }
  if (!['http:', 'https:'].includes(parsed.protocol) || parsed.username || parsed.password) throw new Error('invalid_website');
  const hostname = parsed.hostname.toLowerCase().replace(/\.$/, '');
  const labels = hostname.split('.');
  if (labels.length < 2 || hostname.length > 253 || hostname.includes(':') || /^\d+(?:\.\d+)*$/.test(hostname)) throw new Error('invalid_website');
  if (labels.some(label => !/^[a-z\d](?:[a-z\d-]{0,61}[a-z\d])?$/.test(label))) throw new Error('invalid_website');
  if (['localhost', 'local', 'internal', 'lan', 'home', 'test', 'invalid', 'example', 'onion'].includes(labels.at(-1))) throw new Error('invalid_website');
  if (/^\d+$/.test(labels.at(-1))) throw new Error('invalid_website');
  parsed.hostname = hostname;
  parsed.hash = '';
  return parsed.href;
}

export function parseWebsites(text) {
  const websites = []; const invalid = []; const seen = new Set(); let duplicates = 0;
  String(text).split(/\r\n|\r|\n/).forEach((line, index) => {
    if (!line.trim()) return;
    try {
      const url = normalizeWebsite(line);
      const domain = new URL(url).hostname.replace(/^www\./, '');
      if (seen.has(domain)) duplicates += 1;
      else { seen.add(domain); websites.push(url); }
    } catch { invalid.push({ line: index + 1, value: line.trim().slice(0, 150) }); }
  });
  return { websites, invalid, duplicates };
}

/** Spreadsheet export: neutralize formula-leading cells, including whitespace prefixes. */
export function spreadsheetCSV(rows) {
  const headers = ['url', 'domain', 'companyName', 'emails', 'phones', 'linkedin', 'facebook', 'instagram', 'technologies', 'contactFormUrls', 'pagesChecked', 'pagesVisited', 'observedAt', 'status'];
  const cell = value => {
    let text = value == null ? '' : String(value);
    if (/^[\s\u0000-\u001f]*[=+\-@]/.test(text)) text = `'${text}`;
    return `"${text.replace(/"/g, '""')}"`;
  };
  const values = rows.map(row => [row.url, row.domain, row.companyName, row.emails.join('; '), row.phones.join('; '),
    (row.socials.linkedin || []).join('; '), (row.socials.facebook || []).join('; '), (row.socials.instagram || []).join('; '),
    row.technologies.map(item => item.name).join('; '), row.contactFormUrls.join('; '), row.pagesChecked, row.pagesVisited.join('; '), row.observedAt, row.status]);
  return [headers, ...values].map(row => row.map(cell).join(',')).join('\r\n');
}

if (typeof document !== 'undefined') init();

function init() {
  const english = { ...dynamicEnglish };
  document.querySelectorAll('[data-i18n]').forEach(element => { english[element.dataset.i18n] ??= element.textContent.trim(); });
  document.querySelectorAll('[data-i18n-placeholder]').forEach(element => { english[element.dataset.i18nPlaceholder] ??= element.getAttribute('placeholder'); });
  document.querySelectorAll('[data-i18n-aria]').forEach(element => { english[element.dataset.i18nAria] ??= element.getAttribute('aria-label'); });
  let language = 'en';
  try { const saved = localStorage.getItem('sitesignal-language'); if (saved === 'en' || saved === 'vi') language = saved; } catch { /* Storage is optional. */ }
  let selectedDomain = demoDataset[0].domain;
  let currentInput = null;
  let currentError = null;
  let lastParsed = null;
  let toastTimer;
  const $ = id => document.getElementById(id);
  const t = (key, values = {}) => {
    const text = (language === 'vi' ? vietnamese[key] : english[key]) ?? english[key] ?? key;
    return text.replace(/\{(\w+)\}/g, (_, name) => String(values[name] ?? ''));
  };
  const element = (tag, className, text) => {
    const node = document.createElement(tag);
    if (className) node.className = className;
    if (text !== undefined) node.textContent = text;
    return node;
  };
  const safePublicLink = value => {
    if (!value || typeof value !== 'string') return null;
    try { const url = new URL(value); return ['https:', 'http:'].includes(url.protocol) && !url.username && !url.password ? url.href : null; } catch { return null; }
  };
  const actorUrl = safePublicLink(publicConfig.actorUrl);
  const githubUrl = safePublicLink(publicConfig.githubUrl);

  const technologies = [...new Set(demoDataset.flatMap(company => company.technologies.map(item => item.name)))].sort();
  technologies.forEach(name => { const option = element('option', '', name); option.value = name; $('technology-filter').append(option); });

  function filteredRows() {
    const query = $('company-search').value.trim().toLocaleLowerCase();
    const technology = $('technology-filter').value;
    const hasEmail = $('email-filter').checked;
    return demoDataset.filter(row => (!hasEmail || row.emails.length > 0)
      && (!technology || row.technologies.some(item => item.name === technology))
      && (!query || [row.companyName, row.domain, ...row.emails, ...row.technologies.map(item => item.name)].join(' ').toLocaleLowerCase().includes(query)));
  }

  function avatar(company, index) {
    const colors = [['#eee7d7','#7c6b45'],['#e6e8df','#5c6b58'],['#dde6e6','#567276'],['#e6e6d6','#71814e'],['#e5eada','#76905d'],['#ebe0d8','#9a7155']];
    const node = element('span', 'table-avatar', company.companyName[0]);
    node.style.setProperty('--avatar-bg', colors[index % colors.length][0]);
    node.style.setProperty('--avatar-ink', colors[index % colors.length][1]);
    node.setAttribute('aria-hidden', 'true');
    return node;
  }

  function renderExplorer() {
    const rows = filteredRows();
    if (!rows.some(row => row.domain === selectedDomain)) selectedDomain = rows[0]?.domain || null;
    const fragment = document.createDocumentFragment();
    rows.forEach(company => {
      const index = demoDataset.indexOf(company);
      const tr = element('tr', company.domain === selectedDomain ? 'selected' : '');
      const select = () => { selectedDomain = company.domain; renderExplorer(); };
      tr.addEventListener('click', select);
      const companyCell = element('td');
      const companyWrap = element('div', 'company-cell');
      const companyText = element('div');
      const companyButton = element('button', 'company-name', company.companyName);
      companyButton.type = 'button'; companyButton.setAttribute('aria-label', t('inspectCompany', { company: company.companyName }));
      companyButton.setAttribute('aria-pressed', String(company.domain === selectedDomain));
      companyButton.addEventListener('click', event => {
        event.stopPropagation();
        selectedDomain = company.domain;
        renderExplorer();
        const selectedButton = $('results-body').querySelector('button[aria-pressed="true"]');
        selectedButton?.focus({ preventScroll: true });
      });
      companyText.append(companyButton, element('span', 'company-domain', company.domain));
      companyWrap.append(avatar(company, index), companyText); companyCell.append(companyWrap);
      const contacts = element('td');
      if (company.emails.length) {
        const count = element('span', 'contact-count');
        const icon = element('span', '', '✉'); icon.setAttribute('aria-hidden', 'true');
        count.append(icon, document.createTextNode(t(company.emails.length === 1 ? 'emailCount' : 'emailCountPlural', { count: company.emails.length })));
        contacts.append(count);
      } else contacts.append(element('span', 'contact-empty', t('noPublicEmail')));
      const techCell = element('td'); const techWrap = element('div', 'technology-chips');
      company.technologies.slice(0, 2).forEach(tech => techWrap.append(element('span', 'tech-chip', tech.name)));
      if (company.technologies.length > 2) { const more = element('span', 'tech-chip', `+${company.technologies.length - 2}`); more.title = company.technologies.slice(2).map(tech => tech.name).join(', '); techWrap.append(more); }
      techCell.append(techWrap);
      const arrow = element('td', 'row-arrow', '↗'); arrow.setAttribute('aria-hidden', 'true');
      tr.append(companyCell, contacts, techCell, arrow); fragment.append(tr);
    });
    $('results-body').replaceChildren(fragment);
    $('empty-state').hidden = rows.length !== 0;
    $('result-count').textContent = t('resultCount', { count: rows.length, total: demoDataset.length });
    $('download-csv').disabled = rows.length === 0;
    $('download-json').disabled = rows.length === 0;
    $('json-preview-code').textContent = JSON.stringify(rows, null, 2);
    renderInspector(rows.find(row => row.domain === selectedDomain));
  }

  function renderInspector(company) {
    const inspector = $('source-inspector');
    if (!company) { inspector.replaceChildren(element('p', 'inspector-note', t('noSelection'))); return; }
    const overline = element('div', 'inspector-overline'); overline.append(element('span', '', t('sourceEvidence')), element('span', 'badge badge-green', t('sample')));
    const heading = element('div', 'inspector-company');
    const name = element('div'); name.append(element('h3', '', company.companyName), element('p', '', company.domain));
    heading.append(avatar(company, demoDataset.indexOf(company)), name);
    const summary = element('div', 'inspector-summary');
    summary.append(element('span', '', t('pagesChecked', { count: company.pagesChecked })), element('span', '', t('findingsCount', { count: company.evidence.length })));
    if (company.status === 'partial') summary.append(element('span', 'partial-status', t('partialSample')));
    const list = element('ul', 'inspector-evidence');
    // Show a contact, a technology, another technology, and a form/social finding.
    const contact = company.evidence.find(item => item.type === 'email') || company.evidence.find(item => item.type === 'phone');
    const tech = company.evidence.filter(item => item.type === 'technology').slice(0, 2);
    const other = company.evidence.find(item => item.type === 'contactForm') || company.evidence.find(item => item.type === 'social');
    const featured = [contact, ...tech, other].filter(Boolean);
    featured.forEach(finding => {
      const li = element('li');
      const typeKeys = { email: 'emailFinding', phone: 'phoneFinding', social: 'socialFinding', technology: 'techFinding', contactForm: 'formFinding', companyName: 'nameFinding' };
      const label = element('div', 'finding-label', t(typeKeys[finding.type] || 'sourceEvidence'));
      const value = finding.type === 'contactForm' ? new URL(finding.value).pathname : finding.value;
      const method = element('div', 'finding-method', finding.method);
      const source = element('div', 'finding-source');
      const sourcePath = new URL(finding.sourceUrl).pathname;
      const link = element('a', '', `${company.domain}${sourcePath === '/' ? '/' : sourcePath}`);
      link.href = finding.sourceUrl; link.target = '_blank'; link.rel = 'noopener noreferrer'; link.title = t('sourceLink', { source: finding.sourceUrl });
      source.append(link); li.append(label, element('div', 'finding-value', value), method, source); list.append(li);
    });
    const note = element('p', 'inspector-note', t('inspectorNote'));
    const details = element('details', 'all-evidence');
    details.append(element('summary', '', t('allEvidence', { count: company.evidence.length })));
    const evidenceJSON = element('pre', '', JSON.stringify(company.evidence, null, 2));
    evidenceJSON.tabIndex = 0;
    details.append(evidenceJSON);
    inspector.replaceChildren(overline, heading, summary, list, details, note);
  }

  function configureLinks() {
    document.querySelectorAll('[data-actor-link]').forEach(link => {
      link.href = actorUrl || '#configure';
      link.querySelector('[data-actor-label]').textContent = t(actorUrl ? 'openActor' : (link.closest('.header-actions') ? 'getConfigShort' : 'getConfig'));
      if (actorUrl) { link.target = '_blank'; link.rel = 'noopener noreferrer'; }
    });
    if (actorUrl) {
      $('publication-state').classList.add('published');
      $('publication-state').querySelector('span:last-child').textContent = t('actorLive');
      $('publication-note').textContent = t('actorLiveNote');
      const actorLink = $('actor-output-link'); actorLink.href = actorUrl; actorLink.target = '_blank'; actorLink.rel = 'noopener noreferrer'; actorLink.hidden = !currentInput;
    }
    document.querySelectorAll('[data-github-link]').forEach(link => {
      link.hidden = !githubUrl;
      if (githubUrl) { link.href = githubUrl; link.target = '_blank'; link.rel = 'noopener noreferrer'; }
    });
  }

  function setLanguage(next) {
    language = next;
    document.documentElement.lang = language;
    document.title = language === 'vi' ? 'SiteSignal — Dữ liệu hữu ích. Có nguồn rõ ràng.' : 'SiteSignal — Useful leads. With evidence.';
    document.querySelectorAll('[data-i18n]').forEach(node => { node.textContent = t(node.dataset.i18n); });
    document.querySelectorAll('[data-i18n-placeholder]').forEach(node => node.setAttribute('placeholder', t(node.dataset.i18nPlaceholder)));
    document.querySelectorAll('[data-i18n-aria]').forEach(node => node.setAttribute('aria-label', t(node.dataset.i18nAria)));
    document.querySelectorAll('[data-language]').forEach(button => button.setAttribute('aria-pressed', String(button.dataset.language === language)));
    $('technology-filter').setAttribute('aria-label', t('technologyFilter'));
    $('nav-toggle').setAttribute('aria-label', t($('nav-toggle').getAttribute('aria-expanded') === 'true' ? 'closeNav' : 'openNav'));
    $('toggle-json').querySelector('span:first-child').textContent = t($('json-preview').hidden ? 'viewRawJson' : 'hideRawJson');
    if (!currentInput) $('input-json').textContent = t('configPlaceholder');
    renderError(); renderInputStatus(); configureLinks(); renderExplorer();
    try { localStorage.setItem('sitesignal-language', language); } catch { /* The page also works without storage. */ }
  }

  function showToast(message) {
    clearTimeout(toastTimer); $('toast').textContent = message; $('toast').hidden = false;
    toastTimer = setTimeout(() => { $('toast').hidden = true; }, 4500);
  }

  function download(filename, text, type) {
    const url = URL.createObjectURL(new Blob([text], { type }));
    const link = document.createElement('a'); link.href = url; link.download = filename; document.body.append(link); link.click(); link.remove();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }

  async function copyText(text) {
    try { if (navigator.clipboard?.writeText) { await navigator.clipboard.writeText(text); return true; } } catch { /* Fall back for preview contexts without clipboard permissions. */ }
    const textarea = document.createElement('textarea'); textarea.value = text; textarea.style.cssText = 'position:fixed;left:-9999px;top:0';
    document.body.append(textarea); textarea.select(); let success = false;
    try { success = document.execCommand('copy'); } catch { success = false; }
    textarea.remove(); return success;
  }

  function renderError() {
    $('website-error').hidden = !currentError;
    $('website-error').textContent = currentError ? t(currentError.key, currentError.values) : '';
    $('website-input').setAttribute('aria-invalid', String(Boolean(currentError && ['emptyInput', 'invalidWebsite', 'tooManySites', 'limitTooLow'].includes(currentError.key))));
  }

  function renderInputStatus() {
    $('configuration-status').hidden = !currentInput;
    if (currentInput) $('configuration-status').textContent = t('configReady', { count: currentInput.websites.length }) + (lastParsed?.duplicates ? t('duplicatesRemoved', { count: lastParsed.duplicates }) : '');
  }

  function invalidateInput() {
    currentInput = null; currentError = null; lastParsed = null;
    $('copy-config').disabled = true; $('download-config').disabled = true;
    $('input-json').textContent = t('configPlaceholder'); $('actor-output-link').hidden = true;
    renderError(); renderInputStatus();
  }

  $('configuration-form').addEventListener('submit', event => {
    event.preventDefault();
    const parsed = parseWebsites($('website-input').value);
    const maxSites = Number($('max-sites').value); const maxPages = Number($('max-pages').value);
    currentError = null;
    if (!Number.isInteger(maxSites) || maxSites < 1 || maxSites > 100) currentError = { key: 'invalidMaxSites' };
    else if (!Number.isInteger(maxPages) || maxPages < 1 || maxPages > 5) currentError = { key: 'invalidMaxPages' };
    else if (parsed.invalid.length) currentError = { key: 'invalidWebsite', values: parsed.invalid[0] };
    else if (!parsed.websites.length) currentError = { key: 'emptyInput' };
    else if (parsed.websites.length > 100) currentError = { key: 'tooManySites' };
    else if (parsed.websites.length > maxSites) currentError = { key: 'limitTooLow', values: { count: parsed.websites.length, max: maxSites } };
    renderError();
    if (currentError) { $(currentError.key === 'invalidMaxSites' ? 'max-sites' : currentError.key === 'invalidMaxPages' ? 'max-pages' : 'website-input').focus(); return; }
    currentInput = { websites: parsed.websites, maxPagesPerSite: maxPages, maxSites, respectRobots: true };
    lastParsed = parsed;
    $('input-json').textContent = JSON.stringify(currentInput, null, 2);
    $('copy-config').disabled = false; $('download-config').disabled = false;
    renderInputStatus(); configureLinks();
  });
  ['website-input', 'max-sites', 'max-pages'].forEach(id => $(id).addEventListener('input', invalidateInput));
  $('max-pages').addEventListener('change', invalidateInput);
  $('copy-config').addEventListener('click', async () => {
    if (!currentInput) return;
    const copied = await copyText(JSON.stringify(currentInput, null, 2));
    showToast(t(copied ? 'configCopied' : 'copyFailed'));
    $('copy-config').focus({ preventScroll: true });
  });
  $('download-config').addEventListener('click', () => {
    if (!currentInput) return;
    download('sitesignal-input.json', `${JSON.stringify(currentInput, null, 2)}\n`, 'application/json;charset=utf-8');
    showToast(t('configDownloaded'));
  });
  $('download-csv').addEventListener('click', () => {
    const rows = filteredRows(); if (!rows.length) return showToast(t('emptyCsv'));
    download('sitesignal-fictional-sample.csv', `\uFEFF${spreadsheetCSV(rows)}`, 'text/csv;charset=utf-8');
    showToast(t('downloadSuccess', { format: 'CSV', count: rows.length }));
  });
  $('download-json').addEventListener('click', () => {
    const rows = filteredRows(); if (!rows.length) return showToast(t('emptyCsv'));
    download('sitesignal-fictional-sample.json', `${JSON.stringify(rows, null, 2)}\n`, 'application/json;charset=utf-8');
    showToast(t('downloadSuccess', { format: 'JSON', count: rows.length }));
  });
  $('company-search').addEventListener('input', renderExplorer);
  $('technology-filter').addEventListener('change', renderExplorer);
  $('email-filter').addEventListener('change', renderExplorer);
  $('reset-filters').addEventListener('click', () => { $('company-search').value = ''; $('technology-filter').value = ''; $('email-filter').checked = false; renderExplorer(); $('company-search').focus(); });
  $('toggle-json').addEventListener('click', () => {
    $('json-preview').hidden = !$('json-preview').hidden;
    $('toggle-json').setAttribute('aria-expanded', String(!$('json-preview').hidden));
    $('toggle-json').querySelector('span:first-child').textContent = t($('json-preview').hidden ? 'viewRawJson' : 'hideRawJson');
  });
  document.querySelectorAll('[data-language]').forEach(button => button.addEventListener('click', () => setLanguage(button.dataset.language)));
  function closeNavigation() {
    $('main-nav').classList.remove('open'); $('nav-toggle').setAttribute('aria-expanded', 'false'); $('nav-toggle').setAttribute('aria-label', t('openNav'));
  }
  $('nav-toggle').addEventListener('click', () => {
    const open = $('nav-toggle').getAttribute('aria-expanded') !== 'true';
    $('main-nav').classList.toggle('open', open); $('nav-toggle').setAttribute('aria-expanded', String(open)); $('nav-toggle').setAttribute('aria-label', t(open ? 'closeNav' : 'openNav'));
  });
  $('main-nav').querySelectorAll('a').forEach(link => link.addEventListener('click', closeNavigation));
  document.addEventListener('keydown', event => { if (event.key === 'Escape' && $('nav-toggle').getAttribute('aria-expanded') === 'true') { closeNavigation(); $('nav-toggle').focus(); } });
  document.addEventListener('click', event => { if (!$('main-nav').contains(event.target) && !$('nav-toggle').contains(event.target)) closeNavigation(); });
  setLanguage(language);
}
