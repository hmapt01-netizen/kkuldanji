// 광고 굽기 — HyperFrames 로 무음 mp4 → ffmpeg 로 음악 붙이기 (맥 · 윈도우 공용)
//
//   node 클로드용_자료/도구/굽기.mjs 클로드용_자료/작업/012/모닝빈_12번 --음악 클로드용_자료/작업/012/음악.wav --이름 모닝빈_12번
//   node 클로드용_자료/도구/굽기.mjs 클로드용_자료/작업/012/모닝빈_12번 --draft          시험 굽기(빠름 · 화질 낮음)
//   node 클로드용_자료/도구/굽기.mjs 클로드용_자료/작업/012/모닝빈_12번_세로 --이름 모닝빈_12번_세로 --no-browser-gpu   (뒤의 - 옵션은 HyperFrames 렌더에 그대로)
//
// 결과: 완성_영상/<이름>.mp4  (이름을 안 주면 광고 폴더 이름)
// 필요: Node 22 이상 · ffmpeg · 인터넷(처음 한 번 HyperFrames 와 렌더용 크롬을 받는다)
import { spawnSync } from "node:child_process";
import fs from "node:fs";
import os from "node:os";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HF = "hyperframes@0.7.94"; // 키트에서 구워 확인한 판 — 바꿀 땐 시험 굽기부터
const KIT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), "..", ".."); // 키트 맨 위(완성_영상/ 이 여기 생긴다)
const isWin = process.platform === "win32";

function die(msg) {
  console.error("\n[멈춤] " + msg);
  process.exit(1);
}

// ── 인자 ──────────────────────────────────────────────
const argv = process.argv.slice(2);
const take = (flag) => {
  const i = argv.indexOf(flag);
  if (i < 0) return null;
  const v = argv[i + 1];
  argv.splice(i, 2);
  return v;
};
const music = take("--음악");
let name = take("--이름");
const draft = argv.includes("--draft");
const noCheck = argv.includes("--검사안함");
const rest = argv.filter((a) => a !== "--draft" && a !== "--검사안함");
const projArg = rest.find((a) => !a.startsWith("-"));
const PASS = rest.filter((a) => a.startsWith("-"));
if (!projArg) die("광고 폴더를 주세요. 예: node 클로드용_자료/도구/굽기.mjs 클로드용_자료/작업/012/모닝빈_12번 --음악 클로드용_자료/작업/012/음악.wav --이름 모닝빈_12번");

// ── Node · PATH · ffmpeg ─────────────────────────────────
const major = Number(process.versions.node.split(".")[0]);
if (major < 22) die(`Node ${process.versions.node} 입니다. HyperFrames 는 Node 22 이상이 필요합니다 — 클로드용_자료/자동설치.md 를 따라 주세요.`);
const home = os.homedir();
const extra = [
  path.dirname(process.execPath),
  path.join(home, ".local", "bin"),
  ...(isWin
    ? [path.join(process.env.LOCALAPPDATA || "", "Programs", "ffmpeg", "bin"), path.join(process.env.LOCALAPPDATA || "", "Microsoft", "WinGet", "Links")]
    : ["/opt/homebrew/bin", "/usr/local/bin"]),
].filter((p) => p && fs.existsSync(p));
const env = { ...process.env, PATH: [...extra, process.env.PATH || ""].join(path.delimiter) };

const q = (a) => (isWin && /[\s&()^]/.test(a) ? `"${a}"` : a);
function run(cmd, args, opts = {}) { if (cmd === "npx") { cmd = "node"; args = ["C:/Users/lim/AppData/Local/npm-cache/_npx/c7c4026b235a35e6/node_modules/hyperframes/bin/hyperframes.mjs", ...args.slice(2)]; }
  // 윈도우의 npx · ffmpeg 는 셸을 거쳐야 찾는다 → 빈칸이 든 인자는 따옴표로 감싼다
  const r = spawnSync(cmd, isWin ? args.map(q) : args, { cwd: KIT, env, stdio: opts.quiet ? "pipe" : "inherit", shell: isWin, encoding: "utf8" });
  if (r.error) return { ok: false, out: String(r.error.message) };
  return { ok: r.status === 0, out: (r.stdout || "") + (r.stderr || "") };
}
if (!run("ffmpeg", ["-version"], { quiet: true }).ok) die("ffmpeg 를 찾지 못했습니다 — 클로드용_자료/자동설치.md 를 따라 주세요.");

// ── 광고 폴더 준비 ────────────────────────────────────────
const proj = path.relative(KIT, path.resolve(KIT, projArg)) || ".";
const projAbs = path.join(KIT, proj);
if (!fs.existsSync(path.join(projAbs, "index.html"))) die(`${proj}/index.html 이 없습니다. 광고 코드(index.html)가 있는 폴더를 주세요.`);
const id = (name || path.basename(projAbs)).replace(/[^\p{L}\p{N}_-]+/gu, "_");
const defaults = {
  "hyperframes.json": {
    $schema: "https://hyperframes.heygen.com/schema/hyperframes.json",
    registry: "https://raw.githubusercontent.com/heygen-com/hyperframes/main/registry",
    paths: { blocks: "compositions", components: "compositions/components", assets: "assets" },
    media: { autoProxy: true },
  },
  "package.json": { name: "ad_" + Date.now().toString(36), private: true, type: "module" },
  "meta.json": { id: "ad", name: id },
};
for (const [f, v] of Object.entries(defaults)) {
  const p = path.join(projAbs, f);
  if (!fs.existsSync(p)) fs.writeFileSync(p, JSON.stringify(v, null, 2));
}
name = id;
// 글꼴: 키트의 클로드용_자료/글꼴/ 을 광고 폴더 assets/fonts 로 (없는 것만)
const fontSrc = path.join(KIT, "클로드용_자료", "글꼴");
const fontDst = path.join(projAbs, "assets", "fonts");
if (fs.existsSync(fontSrc)) {
  fs.mkdirSync(fontDst, { recursive: true });
  for (const f of fs.readdirSync(fontSrc))
    if (/\.(ttf|otf|woff2?)$/i.test(f) && !fs.existsSync(path.join(fontDst, f))) fs.copyFileSync(path.join(fontSrc, f), path.join(fontDst, f));
}

// ── 검사 → 무음 렌더 → 음악 → 확인 ───────────────────────────
const t0 = Date.now();
if (!noCheck) {
  console.log(`검사: ${proj}`);
  const c = run("npx", ["--yes", HF, "check", proj]);
  if (!c.ok) console.log("  ↳ 검사에서 문제를 알렸습니다. 글자 상자 겹침 · 넘침은 그 시각 프레임을 직접 보고 판단하세요(의도한 것이면 data-layout-allow-overlap · data-layout-allow-overflow). 렌더는 계속합니다.");
}
fs.mkdirSync(path.join(KIT, "완성_영상"), { recursive: true });
const silent = path.join(proj, "_silent.mp4");
fs.rmSync(path.join(KIT, silent), { force: true });
console.log(`렌더: ${proj} (${draft ? "draft" : "high"} · 처음 한 번은 HyperFrames · 크롬 내려받기로 몇 분 걸릴 수 있습니다)`);
if (!run("npx", ["--yes", HF, "render", proj, "-o", silent, "--fps", "30", "--quality", draft ? "draft" : "high", "--quiet", ...PASS]).ok)
  die(`HyperFrames 렌더 실패 — 위 메시지를 확인하세요. 환경 점검: npx --yes ${HF} doctor · 화면이 검거나 깨지면 --no-browser-gpu`);

const out = path.join("완성_영상", `${name}.mp4`);
let ok;
if (music) {
  if (!fs.existsSync(path.resolve(KIT, music))) die(`음악 파일이 없습니다: ${music}`);
  ok = run("ffmpeg", ["-v", "error", "-y", "-i", silent, "-i", music, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy",
    "-c:a", "aac", "-b:a", "256k", "-ar", "48000", "-ac", "2", "-shortest", "-movflags", "+faststart", out]).ok;
} else {
  console.log("음악을 주지 않아 무음으로 둡니다(--음악 파일).");
  ok = run("ffmpeg", ["-v", "error", "-y", "-i", silent, "-c", "copy", "-movflags", "+faststart", out]).ok;
}
if (!ok) die("ffmpeg 로 마무리하지 못했습니다");
fs.rmSync(path.join(KIT, silent), { force: true });

const probe = run("ffprobe", ["-v", "error", "-show_entries", "stream=codec_name,width,height,r_frame_rate,sample_rate:format=duration,size", "-of", "compact", out], { quiet: true });
console.log(`\n완료: ${out}  (${Math.round((Date.now() - t0) / 1000)}초)`);
if (probe.ok) console.log(probe.out.trim());
console.log(`점검: python3 클로드용_자료/도구/스틸.py ${out}`);


