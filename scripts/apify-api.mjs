// Authenticated account API helper using the official CLI's OS-keyring entry.
// Credentials exist only in this process, never in command arguments or output.
import { createRequire } from 'node:module';
import { readFileSync } from 'node:fs';
import { homedir } from 'node:os';
import path from 'node:path';

try {
  const input = JSON.parse(readFileSync(0, 'utf8'));
  const entry = process.env.APIFY_CLI_ENTRY;
  if (!entry) throw new Error('APIFY_CLI_ENTRY must point to the installed official Apify CLI.');
  const auth = JSON.parse(readFileSync(path.join(homedir(), '.apify', 'auth.json'), 'utf8'));
  let token;
  if (auth.secretsBackend === 'file') token = auth.token;
  else {
    const require = createRequire(entry);
    const { Entry } = require('@napi-rs/keyring');
    token = new Entry('com.apify.cli', 'token').getPassword();
  }
  if (!token) throw new Error('No Apify login found. Run apify login first.');
  const url = new URL('https://api.apify.com/v2/' + input.endpoint.replace(/^\/+/, ''));
  if (url.origin !== 'https://api.apify.com') throw new Error('Only the official Apify API is supported.');
  for (const [key, value] of Object.entries(input.params || {})) url.searchParams.set(key, String(value));
  const response = await fetch(url, {
    method: input.method,
    headers: { Authorization: `Bearer ${token}`, 'Content-Type': 'application/json' },
    body: input.body == null ? undefined : JSON.stringify(input.body),
    redirect: 'error', signal: AbortSignal.timeout(75000),
  });
  const data = await response.json();
  if (!response.ok) {
    process.stderr.write(JSON.stringify({status: response.status, error: data.error || data}) + '\n');
    process.exitCode = 1;
  } else process.stdout.write(JSON.stringify(data) + '\n');
} catch (error) {
  process.stderr.write(String(error.message) + '\n');
  process.exitCode = 1;
}
