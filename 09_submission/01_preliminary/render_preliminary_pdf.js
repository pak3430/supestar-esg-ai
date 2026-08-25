'use strict';

const fs = require('fs');
const path = require('path');
const { pathToFileURL } = require('url');
const { marked } = require('marked');
const { chromium } = require('playwright');

const root = __dirname;
const source = path.join(root, '01_수페스타_예선기획서.md');
const htmlPath = path.join(root, '초ROK_수페스타_예선기획서.html');
const pdfPath = path.join(root, '초ROK_수페스타_예선기획서.pdf');

const markdown = fs.readFileSync(source, 'utf8').replace(/^# [^\n]+\n\n> [^\n]+\n\n(?:[^\n]+\n){3}\n/, '');
const body = marked.parse(markdown, { gfm: true });
const html = `<!doctype html>
<html lang="ko">
<head>
<meta charset="utf-8">
<title>초ROK 수페스타 예선기획서</title>
<style>
@font-face{font-family:'NotoKR';src:url('file:///Library/Fonts/NotoSansCJKkr-Regular.otf') format('opentype');font-weight:400}
@font-face{font-family:'NotoKR';src:url('file:///Library/Fonts/NotoSansCJKkr-Bold.otf') format('opentype');font-weight:700}
@page{size:A4;margin:18mm 17mm 19mm}
*{box-sizing:border-box}
html,body{margin:0;color:#172033;background:#fff;font-family:'NotoKR','Apple SD Gothic Neo',sans-serif;font-size:10.4pt;line-height:1.55;word-break:keep-all}
.cover{height:258mm;display:flex;flex-direction:column;justify-content:center;align-items:center;text-align:center;page-break-after:always;border-top:8px solid #175f5b}
.cover .eyebrow{font-size:11pt;letter-spacing:.16em;color:#6b7788;margin-bottom:18px}
.cover h1{font-size:34pt;line-height:1.15;margin:0;color:#123f3d}
.cover h2{font-size:17pt;line-height:1.45;margin:18px 0 46px;color:#315c5a;font-weight:500}
.cover .meta{font-size:11pt;color:#34475a;line-height:1.8}
main{max-width:100%}
h1{font-size:19pt;line-height:1.25;color:#123f3d;border-bottom:2px solid #62a7a0;padding-bottom:6px;margin:24px 0 12px;break-after:avoid}
h2{font-size:13.5pt;color:#175f5b;margin:18px 0 7px;break-after:avoid}
h3{font-size:11.5pt;color:#315c5a;margin:14px 0 5px;break-after:avoid}
p{margin:5px 0 9px}
blockquote{margin:8px 0 14px;padding:12px 15px;border-left:5px solid #2d827b;background:#edf7f5;color:#123f3d;font-weight:700;break-inside:avoid}
table{width:100%;border-collapse:collapse;margin:9px 0 15px;font-size:9.3pt;break-inside:avoid}
thead{display:table-header-group}
th{background:#dcefea;color:#123f3d;font-weight:700}
th,td{border:1px solid #a9c7c3;padding:6px 8px;text-align:left;vertical-align:top}
ul,ol{margin:6px 0 12px;padding-left:22px}
li{margin:2px 0}
code{font-family:ui-monospace,SFMono-Regular,Menlo,monospace;background:#eef2f5;padding:1px 4px;border-radius:3px;font-size:.92em}
a{color:#176a82;text-decoration:none}
main>h2:first-child{margin-top:0}
</style>
</head>
<body>
<section class="cover">
  <div class="eyebrow">2026 ESG × AI 챌린지 해커톤 · TRACK C</div>
  <h1>수페스타</h1>
  <h2>KAC 지식과 실행 Skill로 ESG 질문을<br>검증 가능한 다음 행동으로 바꾸는 지식행동 AI 챗봇</h2>
  <div class="meta">팀 초 ROK · 박상훈<br>2026.08.25</div>
</section>
<main>${body}</main>
</body>
</html>`;

fs.writeFileSync(htmlPath, html, 'utf8');

(async () => {
  const systemChrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
  const browser = await chromium.launch({
    headless: true,
    executablePath: fs.existsSync(systemChrome) ? systemChrome : chromium.executablePath(),
  });
  const page = await browser.newPage();
  await page.goto(pathToFileURL(htmlPath).href, { waitUntil: 'networkidle' });
  await page.pdf({
    path: pdfPath,
    format: 'A4',
    printBackground: true,
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate: '<div style="width:100%;font-size:8px;color:#6b7788;text-align:center;font-family:sans-serif"><span class="pageNumber"></span></div>',
    margin: { top: '18mm', right: '17mm', bottom: '19mm', left: '17mm' },
    preferCSSPageSize: true,
  });
  await browser.close();
  process.stdout.write(pdfPath + '\n');
})();
