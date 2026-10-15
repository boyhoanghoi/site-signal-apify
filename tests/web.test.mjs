import test from 'node:test';
import assert from 'node:assert/strict';
import { normalizeWebsite, parseWebsites, spreadsheetCSV, demoDataset } from '../dist/app.js';

test('normalizes bare domains and preserves public paths and queries', () => {
  assert.equal(normalizeWebsite(' Example.COM '), 'https://example.com/');
  assert.equal(normalizeWebsite('http://example.com/contact?lang=vi#email'), 'http://example.com/contact?lang=vi');
  assert.equal(normalizeWebsite('https://EXAMPLE.com./'), 'https://example.com/');
});

test('rejects unsupported protocols, local addresses, IPs and credentials', () => {
  for (const value of ['localhost', 'localhost:8000', 'http://127.0.0.1/', 'http://[::1]/',
    'http://0x7f000001/', 'https://shop.local/', 'https://fake.example/', 'ftp://example.com/',
    'javascript:alert(1)', 'https://user:secret@example.com/', '//example.com', 'not a domain']) {
    assert.throws(() => normalizeWebsite(value), /invalid_website/, value);
  }
});

test('deduplicates canonical hostname including www, paths, scheme and fragments', () => {
  const result = parseWebsites('https://www.python.org/\nhttps://www.djangoproject.com/\nhttps://www.python.org/contact\nhttp://python.org/about#team\npython.org\n');
  assert.deepEqual(result.websites, ['https://www.python.org/', 'https://www.djangoproject.com/']);
  assert.equal(result.duplicates, 3);
  assert.deepEqual(result.invalid, []);
});

test('preserves the first URL for each domain and distinguishes subdomains', () => {
  const result = parseWebsites('example.com/contact\nwww.example.com/\nshop.example.com\nEXAMPLE.com/about');
  assert.deepEqual(result.websites, ['https://example.com/contact', 'https://shop.example.com/']);
  assert.equal(result.duplicates, 2);
});

test('reports original line numbers and ignores blank lines', () => {
  const result = parseWebsites('\r\nexample.com\r\n\r\nhttps://127.0.0.1\r\n');
  assert.deepEqual(result.websites, ['https://example.com/']);
  assert.deepEqual(result.invalid, [{ line: 4, value: 'https://127.0.0.1' }]);
  assert.deepEqual(parseWebsites(' \n\t\n'), { websites: [], invalid: [], duplicates: 0 });
});

test('spreadsheet exports neutralize formulas and preserve quotes and line breaks', () => {
  const row = { ...demoDataset[0], companyName: '  =HYPERLINK("evil")', emails: ['@SUM(1)'],
    phones: ['+1-202-555-0101'], domain: 'line1\n"line2"' };
  const csv = spreadsheetCSV([row]);
  assert.ok(csv.includes('"\'  =HYPERLINK(""evil"")"'));
  assert.ok(csv.includes('"\'@SUM(1)"'));
  assert.ok(csv.includes('"\'+1-202-555-0101"'));
  assert.ok(csv.includes('"line1\n""line2"""'));
  assert.ok(csv.includes('\r\n'));
  assert.equal(row.companyName, '  =HYPERLINK("evil")');
});

test('sample output is fictional, consistent, and includes evidence for every contact', () => {
  assert.equal(demoDataset.length, 6);
  for (const row of demoDataset) {
    assert.ok(row.domain.endsWith('.example'));
    assert.equal(row.pagesChecked, row.pagesVisited.length);
    assert.ok(['ok', 'partial'].includes(row.status));
    for (const value of [...row.emails, ...row.phones, ...Object.values(row.socials).flat()]) {
      assert.ok(row.evidence.some(item => item.value === value && item.sourceUrl && item.method), value);
    }
    for (const technology of row.technologies) {
      assert.ok(technology.name && technology.category && technology.evidence && technology.sourceUrl);
      assert.ok(row.evidence.some(item => item.type === 'technology' && item.value === technology.name));
    }
  }
});
