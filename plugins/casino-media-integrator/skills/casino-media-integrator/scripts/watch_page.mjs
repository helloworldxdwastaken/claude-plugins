// Watch the real player page in a MUTED headless Chrome and log what actually paints.
//
// Usage: node watch_page.mjs URL [seconds=90] [--mbps N] [--selector CSS] [--keys renderer,wheelCamera] [--match REGEX]
//
// - Muted (--mute-audio): a headless browser otherwise plays the programme through the
//   owner's speakers on top of whatever they are listening to.
// - Run it against the deployed public URL, not only localhost: localhost hides download
//   time, and per-viewer clips that arrive in 0 ms locally can blank for seconds online.
//   --mbps throttles the download link (e.g. 30) to imitate a home connection.
// - Logs every change of the canvas dataset keys with the source frame (video.currentTime*fps),
//   counts frames per state, lists runs where the renderer was "loading", and lists requests
//   matching --match (default: mp4|m4a|flac) with status and seconds to finish.
// Chrome: $CHROME, else Playwright's headless shell, else Google Chrome.
import {spawn} from 'node:child_process';
import {existsSync, mkdtempSync, readdirSync, rmSync} from 'node:fs';
import {tmpdir, homedir} from 'node:os';
import {join} from 'node:path';

const args = process.argv.slice(2), opt = (k, d) => {const i = args.indexOf(k); return i >= 0 ? args.splice(i, 2)[1] : d;};
const mbps = Number(opt('--mbps', 0)), selector = opt('--selector', 'canvas.program-camera-canvas');
const keys = opt('--keys', 'renderer,wheelCamera').split(','), match = opt('--match', 'mp4|m4a|flac'), fps = Number(opt('--fps', 24));
const [url, secs = '90'] = args;
if (!url) {console.error('usage: node watch_page.mjs URL [seconds] [--mbps N] [--selector CSS] [--keys a,b] [--match REGEX]'); process.exit(2);}
const shell = (() => {const root = join(homedir(), 'Library/Caches/ms-playwright');
  for (const d of existsSync(root) ? readdirSync(root).filter(n => n.startsWith('chromium_headless_shell')) : []) {
    for (const p of [join(root, d, 'chrome-headless-shell-mac-arm64/chrome-headless-shell'), join(root, d, 'chrome-linux/headless_shell')]) if (existsSync(p)) return p;}
  return null;})();
const bin = process.env.CHROME || shell || '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const profile = mkdtempSync(join(tmpdir(), 'watch-page-')), port = 9300 + Math.floor(Math.random() * 500);
const chrome = spawn(bin, [`--remote-debugging-port=${port}`, '--headless=new', '--mute-audio', '--autoplay-policy=no-user-gesture-required',
  '--window-size=1280,800', `--user-data-dir=${profile}`, 'about:blank'], {stdio: 'ignore'});
const sleep = ms => new Promise(r => setTimeout(r, ms));
const done = code => {chrome.kill('SIGKILL'); rmSync(profile, {recursive: true, force: true}); process.exit(code);};
try {
  let tabs; for (let i = 0; i < 50 && !tabs; i++) {try {tabs = await (await fetch(`http://127.0.0.1:${port}/json`)).json();} catch {await sleep(200);}}
  const ws = new WebSocket(tabs.find(t => t.type === 'page').webSocketDebuggerUrl); await new Promise(r => ws.onopen = r);
  let id = 0; const pending = new Map(), requests = new Map(), t0 = Date.now(), re = new RegExp(match);
  ws.onmessage = e => {const m = JSON.parse(e.data); if (pending.has(m.id)) {pending.get(m.id)(m); pending.delete(m.id); return;}
    const p = m.params, now = (Date.now() - t0) / 1000;
    if (m.method === 'Network.requestWillBeSent' && re.test(p.request.url)) requests.set(p.requestId, {url: p.request.url.replace(/^https?:\/\/[^/]+/, ''), start: now});
    if (m.method === 'Network.responseReceived' && requests.has(p.requestId)) requests.get(p.requestId).status = p.response.status;
    if (m.method === 'Network.loadingFinished' && requests.has(p.requestId)) requests.get(p.requestId).end = now;
    if (m.method === 'Network.loadingFailed' && requests.has(p.requestId)) Object.assign(requests.get(p.requestId), {end: now, failed: p.errorText});};
  const send = (method, params = {}) => new Promise(r => {const i = ++id; pending.set(i, r); ws.send(JSON.stringify({id: i, method, params}));});
  await send('Network.enable');
  if (mbps) await send('Network.emulateNetworkConditions', {offline: false, latency: 40, downloadThroughput: mbps * 125000, uploadThroughput: 2e6});
  await send('Page.navigate', {url}); await sleep(12000);
  const expr = `(async()=>{const c=document.querySelector(${JSON.stringify(selector)}),v=document.querySelector('video');if(!c)return JSON.stringify({error:'selector not found'});
   const keys=${JSON.stringify(keys)},log=[],stats={},runs=[];let last='',run=null;const t0=performance.now();
   await new Promise(res=>{const tick=()=>{const k=keys.map(x=>c.dataset[x]||'').join('|'),f=v?Math.floor(v.currentTime*${fps}):-1;stats[k]=(stats[k]||0)+1;
    if(k!==last){last=k;log.push(f+' '+k+' t='+((performance.now()-t0)/1000).toFixed(1));}
    if(c.dataset.renderer==='loading'){if(!run)run={frame:f,n:0};run.n++;}else if(run){runs.push(run);run=null;}
    if(performance.now()-t0<${Number(secs)}*1000)requestAnimationFrame(tick);else{if(run)runs.push(run);res();}};tick();});
   return JSON.stringify({log,stats,loadingRuns:runs});})()`;
  const r = await send('Runtime.evaluate', {expression: expr, awaitPromise: true, returnByValue: true, timeout: (Number(secs) + 30) * 1000});
  const out = JSON.parse(r.result?.result?.value ?? '{"error":"evaluation failed"}');
  if (out.error) {console.error(out.error); done(1);}
  console.log('--- changes (frame state t=seconds)'); out.log.forEach(l => console.log(l));
  console.log('--- frames per state'); Object.entries(out.stats).sort((a, b) => b[1] - a[1]).forEach(([k, n]) => console.log(String(n).padStart(6), k));
  console.log('--- loading runs (start frame, animation frames)', JSON.stringify(out.loadingRuns));
  console.log('--- media requests (status, seconds, path)');
  for (const q of requests.values()) console.log(q.failed ? 'FAIL ' + q.failed : q.status ?? '...', q.end ? (q.end - q.start).toFixed(2) + 's' : 'open', q.url);
  done(0);
} catch (error) {console.error(error); done(1);}
