/**
 * Verify the standalone four-module learning lab in real Chrome without network.
 * Uses Node built-ins and Chrome DevTools Protocol; no third-party runtime packages.
 */
import assert from 'node:assert/strict';
import { spawn } from 'node:child_process';
import { existsSync } from 'node:fs';
import { mkdir, mkdtemp, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join, resolve } from 'node:path';
import { pathToFileURL } from 'node:url';
import { setTimeout as sleep } from 'node:timers/promises';

const root = resolve(import.meta.dirname, '../..');
const source = join(root, 'docs', 'index.html');
const chrome = [
  process.env.CHROME_BIN,
  '/usr/bin/google-chrome',
  '/usr/bin/google-chrome-stable',
  '/usr/bin/chromium',
  '/opt/google/chrome/chrome',
].find((value) => value && existsSync(value));
const scriptErrors = [];
const remoteRequests = [];
const findings = [];
const FIXED_QUERIES = Object.freeze({
  isReady: 'document.readyState==="complete" && document.querySelectorAll("#module-tabs [role=tab]").length===4',
  scheme: 'location.protocol',
  moduleChecks: '(() => {const values=[]; for(let i=0;i<4;i++){document.getElementById("module-tab-"+i).click();document.getElementById("preset-button").click();document.getElementById("check-button").click();values.push({status:document.getElementById("check-status").textContent, rows:[...document.querySelectorAll("#checks .check-row")].map(r=>r.className)});}return values})()',
  focusModule0: 'document.getElementById("module-tab-0").focus()',
  focusedId: 'document.activeElement.id',
  focusSliderAndValue: '(() => {const s=document.querySelector("#sliders input[type=range]");s.focus();return Number(s.value)})()',
  activeSliderValue: 'Number(document.activeElement.value)',
  openConfig: 'document.getElementById("config-button").focus();document.getElementById("config-button").click()',
  dialogOpen: 'document.getElementById("config-dialog").open',
  exportCsv: '(async()=>{const original=URL.createObjectURL;let saved;URL.createObjectURL=(blob)=>{saved=blob;return original.call(URL,blob)};try{document.getElementById("csv-button").click();const text=await saved.text();const rows=text.trim().split(/\\r?\\n/).map(r=>r.split(","));return {header:rows[0],count:rows.length-1,first:rows[1],last:rows.at(-1)}}finally{URL.createObjectURL=original}})()',
  reducedMotion: '({enabled:matchMedia("(prefers-reduced-motion: reduce)").matches,scroll:getComputedStyle(document.documentElement).scrollBehavior,transform:getComputedStyle(document.querySelector(".hero-art")).transform})',
  viewportSize: '({innerWidth:window.innerWidth,scrollWidth:document.documentElement.scrollWidth})',
});
async function until(callback, label) {
  // Host virtualization can delay Chrome's DevTools port creation; always
  // fail with actionable diagnostics rather than pretending the test passed.
  for (let i = 0; i < 300; i++) {
    const result = await callback().catch(() => null);
    if (result) return result;
    await sleep(100);
  }
  throw new Error('Timed out waiting for ' + label);
}
class CDP {
  constructor(ws) {
    this.ws = ws;
    this.sequence = 0;
    this.pending = new Map();
    ws.addEventListener('message', (event) => {
      const message = JSON.parse(event.data);
      if (message.method === 'Runtime.exceptionThrown') {
        scriptErrors.push(message.params?.exceptionDetails?.text ?? 'Unknown page exception');
      }
      if (message.method === 'Network.requestWillBeSent') {
        const url = message.params?.request?.url ?? '';
        if (/^https?:\/\//.test(url)) remoteRequests.push(url);
      }
      if (!message.id) return;
      const reply = this.pending.get(message.id);
      if (!reply) return;
      this.pending.delete(message.id);
      if (message.error) reply.reject(new Error(JSON.stringify(message.error)));
      else reply.resolve(message.result);
    });
  }
  call(method, params = {}) {
    const id = ++this.sequence;
    return new Promise((resolveResult, reject) => {
      this.pending.set(id, { resolve: resolveResult, reject });
      this.ws.send(JSON.stringify({ id, method, params }));
    });
  }
  async query(name) {
    // CDP executes only these audited, immutable test probes. No browser,
    // network or user-supplied expression can enter this API.
    if (!Object.hasOwn(FIXED_QUERIES, name)) {
      throw new Error('Unknown fixed browser QA probe');
    }
    const reply = await this.call('Runtime.evaluate', {
      expression: FIXED_QUERIES[name], returnByValue: true, awaitPromise: true,
    });
    if (reply.exceptionDetails) throw new Error(JSON.stringify(reply.exceptionDetails));
    return reply.result?.value;
  }
  async key(key) {
    // Browser-native default actions (especially Escape on <dialog>) need
    // a real CDP key code; a key-name-only event tests an incomplete input.
    const codes = { ArrowRight: 39, End: 35, Home: 36, Escape: 27 };
    const code = codes[key] ?? 0;
    const fields = {
      key, code: key, windowsVirtualKeyCode: code, nativeVirtualKeyCode: code,
    };
    await this.call('Input.dispatchKeyEvent', { type: 'rawKeyDown', ...fields });
    await this.call('Input.dispatchKeyEvent', { type: 'keyUp', ...fields });
  }
}
async function main() {
  assert.ok(existsSync(source), 'Missing required lab: ' + source);
  assert.ok(chrome, 'Chrome/Chromium is mandatory for real-browser QA');
  const profile = await mkdtemp(join(tmpdir(), 'battery-lab-cdp-'));
  const processHandle = spawn(chrome, [
    '--headless=new', '--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage',
    '--disable-background-networking', '--disable-extensions', '--no-first-run',
    '--no-default-browser-check', '--no-proxy-server',
    '--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE localhost',
    '--remote-allow-origins=*', '--remote-debugging-port=0',
    '--user-data-dir=' + profile, 'about:blank',
  ], { stdio: ['ignore', 'ignore', 'pipe'] });
  let chromeDiagnostics = '';
  processHandle.stderr?.on('data', (chunk) => {
    chromeDiagnostics = (chromeDiagnostics + String(chunk)).slice(-4000);
  });
  processHandle.on('error', (error) => {
    chromeDiagnostics = (chromeDiagnostics + String(error)).slice(-4000);
  });
  let client;
  try {
    const port = await until(async () => {
      const value = await readFile(join(profile, 'DevToolsActivePort'), 'utf8');
      return Number(value.split('\n')[0]);
    }, 'DevTools port');
    const target = await until(async () => {
      const response = await fetch('http://127.0.0.1:' + port + '/json/list');
      const targets = await response.json();
      return targets.find((item) => item.type === 'page' && item.webSocketDebuggerUrl);
    }, 'DevTools page');
    const socket = new WebSocket(target.webSocketDebuggerUrl);
    await new Promise((ok, fail) => {
      socket.addEventListener('open', ok, { once: true });
      socket.addEventListener('error', fail, { once: true });
    });
    client = new CDP(socket);
    await Promise.all([
      client.call('Page.enable'), client.call('Runtime.enable'), client.call('Network.enable'),
    ]);
    // Simulate disconnection before the first request: file:// must still work.
    await client.call('Network.emulateNetworkConditions', {
      offline: true, latency: 0, downloadThroughput: 0, uploadThroughput: 0,
    });
    await client.call('Page.navigate', { url: pathToFileURL(source).href });
    assert.ok(await until(
      () => client.query('isReady'),
      'offline file:// modules',
    ));
    assert.equal(await client.query('scheme'), 'file:');
    findings.push('network-offline file:// page load');
    const checks = await client.query('moduleChecks');
    assert.equal(checks.length, 4);
    for (const [index, item] of checks.entries()) {
      assert.equal(item.status, '2 / 2 passed', 'Module ' + (index + 1));
      assert.deepEqual(item.rows, ['check-row pass', 'check-row pass']);
    }
    findings.push('four module presets and eight successful checkpoint decisions');
    await client.query('focusModule0');
    await client.key('ArrowRight');
    assert.equal(await client.query('focusedId'), 'module-tab-1');
    await client.key('End');
    assert.equal(await client.query('focusedId'), 'module-tab-3');
    await client.key('Home');
    assert.equal(await client.query('focusedId'), 'module-tab-0');
    findings.push('module keyboard arrow, End and Home navigation');
    const before = await client.query('focusSliderAndValue');
    await client.key('ArrowRight');
    assert.ok(await client.query('activeSliderValue') > before);
    findings.push('keyboard range slider interaction');
    await client.query('openConfig');
    assert.equal(await client.query('dialogOpen'), true);
    assert.equal(await client.query('focusedId'), 'close-config');
    await client.key('Escape');
    await sleep(25);
    assert.equal(await client.query('dialogOpen'), false);
    assert.equal(await client.query('focusedId'), 'config-button');
    findings.push('accessible dialog open, Escape and focus restoration');
    const csv = await client.query('exportCsv');
    assert.equal(csv.count, 241);
    assert.equal(csv.header[0], 'model_time_min');
    assert.ok(csv.header.includes('temperatureC'));
    assert.equal(Number(csv.first[0]), 0);
    assert.equal(Number(csv.last[0]), 60);
    findings.push('CSV content, columns and 241 sample rows verified');
    await client.call('Emulation.setEmulatedMedia', {
      features: [{ name: 'prefers-reduced-motion', value: 'reduce' }],
    });
    const motion = await client.query('reducedMotion');
    assert.equal(motion.enabled, true);
    assert.equal(motion.scroll, 'auto');
    assert.equal(motion.transform, 'none');
    findings.push('reduced-motion computed CSS');
    const viewports = [];
    for (const width of [320, 375, 768, 1280]) {
      await client.call('Emulation.setDeviceMetricsOverride', {
        width, height: 850, deviceScaleFactor: 1, mobile: width < 768,
      });
      await sleep(70);
      const size = await client.query('viewportSize');
      viewports.push({ width, ...size });
      assert.ok(size.scrollWidth <= size.innerWidth + 2, 'Horizontal overflow at '+width+'px: '+JSON.stringify(size));
    }
    findings.push('320/375/768/1280px responsive overflow checks');
    assert.deepEqual(scriptErrors, [], 'Uncaught browser exceptions');
    assert.deepEqual(remoteRequests, [], 'External network request in offline mode');
    findings.push('no uncaught JS exceptions or HTTP(S) requests');
    const evidence = { status: 'passed', chrome, tests: findings, viewports,
      moduleCount: checks.length, checkpointCount: 8, csvRows: csv.count,
      externalRequests: remoteRequests.length, exceptions: scriptErrors.length };
    const folder = join(root, 'hardening-artifacts');
    await mkdir(folder, { recursive: true });
    await writeFile(join(folder, 'browser-offline-qa.json'), JSON.stringify(evidence, null, 2) + '\n');
    console.log(JSON.stringify(evidence));
  } catch (error) {
    throw new Error(
      String(error) + '; chromeExit=' + String(processHandle.exitCode) +
      '; chromeStderr=' + chromeDiagnostics,
      { cause: error },
    );
  } finally {
    client?.ws.close();
    processHandle.kill('SIGTERM');
    await rm(profile, { recursive: true, force: true, maxRetries: 3 });
  }
}
main().catch(async (error) => {
  console.error('Mandatory browser QA failed:', error.stack ?? error);
  const folder = join(root, 'hardening-artifacts');
  await mkdir(folder, { recursive: true });
  await writeFile(join(folder, 'browser-offline-qa.json'), JSON.stringify({
    status: 'failed', checksPassedBeforeFailure: findings,
    error: String(error), externalRequests: remoteRequests, exceptions: scriptErrors,
  }, null, 2) + '\n');
  process.exitCode = 1;
});
