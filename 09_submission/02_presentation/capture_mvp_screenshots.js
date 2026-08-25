'use strict';

const fs = require('fs');
const path = require('path');
const { chromium } = require('playwright');

const outDir = path.join(__dirname, 'assets');
fs.mkdirSync(outDir, { recursive: true });
const systemChrome = '/Applications/Google Chrome.app/Contents/MacOS/Google Chrome';
const baseUrl = process.env.SUPESTAR_CAPTURE_URL || 'http://127.0.0.1:4175/';

async function openApp(browser) {
  const page = await browser.newPage({ viewport: { width: 1440, height: 1000 }, deviceScaleFactor: 1, bypassCSP: true });
  await page.goto(baseUrl, { waitUntil: 'networkidle', timeout: 120000 });
  await page.emulateMedia({ reducedMotion: 'reduce' });
  return page;
}

async function ask(page, question) {
  await page.locator('#questionInput').fill(question);
  await page.locator('#chatForm').evaluate((form) => form.requestSubmit());
  await page.locator('.result-bubble').waitFor({ state: 'visible', timeout: 150000 });
}

async function focusResult(page) {
  await page.addStyleTag({ content: `
    .messages{overflow:visible!important;max-height:none!important;height:auto!important}
    .topbar,.context-panel,.quick-prompts,.composer,.composer-note,.product-disclaimer,.intro-bubble,.user-message{display:none!important}
    .workspace{display:block!important;width:960px!important;margin:0 auto!important;padding:20px!important}
    .chat-panel{border:0!important;box-shadow:none!important;min-height:0!important;overflow:visible!important}
    .chat-heading{display:none!important}.assistant-message{margin:0!important}.result-bubble{width:100%!important}
  ` });
}

async function captureAnswer(browser, filename, question) {
  const page = await openApp(browser);
  await ask(page, question);
  await focusResult(page);
  await page.locator('.human-answer').screenshot({ path: path.join(outDir, filename) });
  return page;
}

(async () => {
  const browser = await chromium.launch({ headless: true, executablePath: systemChrome });

  const home = await openApp(browser);
  await home.screenshot({ path: path.join(outDir, '01_supestar_home.png'), fullPage: false });
  await home.close();

  const esg = await captureAnswer(browser, '02_esg_answer_no_market.png', 'ESG가 무엇인가요?');
  await esg.close();

  const scope = await captureAnswer(
    browser,
    '03_scope1_proceed.png',
    '저희 회사가 소유·운영하는 보일러에서 도시가스 1,250 Nm³를 2026년 8월에 사용했고 고지서가 있습니다. Scope 몇인가요?'
  );
  await scope.locator('.technical-details > summary').click();
  await scope.addStyleTag({ content: `
    .technical-details .result-section:nth-of-type(n+4){display:none!important}
    .technical-details{max-height:none!important}.technical-body{overflow:visible!important}
    .technical-details table{table-layout:fixed!important;width:100%!important;font-size:12px!important}
    .technical-details th:nth-child(1),.technical-details td:nth-child(1){width:28%!important}
    .technical-details th:nth-child(2),.technical-details td:nth-child(2){width:48%!important}
    .technical-details th:nth-child(3),.technical-details td:nth-child(3){width:24%!important}
    .technical-details th:nth-child(n+4),.technical-details td:nth-child(n+4){display:none!important}
    .technical-details th,.technical-details td{white-space:normal!important;overflow-wrap:anywhere!important;word-break:break-word!important}
  ` });
  await scope.locator('.technical-details').screenshot({ path: path.join(outDir, '04_scope1_backstage.png') });
  await scope.close();

  const review = await captureAnswer(
    browser,
    '05_conflict_review.png',
    '회사 소유 보일러 연소이면서 한전 구매전력 사용입니다. 어느 Scope인지 하나로 확정해줘.'
  );
  await review.close();

  const market = await captureAnswer(browser, '06_market_explicit_only.png', '탄소크레딧은 어디에서 구매할 수 있나요?');
  await market.close();

  await browser.close();
  process.stdout.write(`${outDir}\n`);
})().catch((error) => {
  process.stderr.write(`${error.stack || error}\n`);
  process.exit(1);
});
