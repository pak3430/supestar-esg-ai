'use strict';

const path = require('path');
const pptxgen = require('pptxgenjs');
const pptx = new pptxgen();

pptx.layout = 'LAYOUT_WIDE';
pptx.author = '초 ROK · 박상훈';
pptx.company = '초 ROK';
pptx.subject = '2026 ESG × AI 챌린지 해커톤 수페스타 발표자료';
pptx.title = '수페스타 — KAC 지식과 실행 Skill 기반 로컬 ESG AI';
pptx.lang = 'ko-KR';

const FONT = 'Apple SD Gothic Neo';
const C = {
  ink: '142922', forest: '0D4B3D', green: '197260', mint: 'DFF2EA', mint2: 'EEF8F4',
  line: 'BED7CF', slate: '53645F', coral: 'C94F49', coralBg: 'FDE6E2',
  amber: 'A86916', amberBg: 'FFF0D7', blue: '2D628D', blueBg: 'E6F0FA', white: 'FFFFFF',
};

pptx.theme = { headFontFace: FONT, bodyFontFace: FONT, lang: 'ko-KR' };
pptx.defineSlideMaster({
  title: 'MASTER', background: { color: 'F7F5EE' },
  objects: [
    { line: { x: 0.52, y: 7.10, w: 12.25, h: 0, line: { color: 'C9D9D5', width: 0.7 } } },
    { text: { text: '초 ROK · 수페스타', options: { x: 0.56, y: 7.15, w: 2.7, h: 0.16, fontFace: FONT, fontSize: 7.5, color: '6C7C78', margin: 0 } } },
    { text: { text: '2026 ESG × AI CHALLENGE', options: { x: 9.7, y: 7.15, w: 2.95, h: 0.16, fontFace: 'Aptos', fontSize: 7.5, color: '6C7C78', align: 'right', margin: 0 } } },
  ],
  slideNumber: { x: 12.82, y: 7.13, w: 0.22, h: 0.18, fontFace: 'Aptos', fontSize: 7.5, color: '6C7C78', align: 'right', margin: 0 },
});

const assets = path.join(__dirname, 'assets');
const mascot = path.join(assets, '00_supestar_mascot.png');
const home = path.join(assets, '01_supestar_home.png');
const esg = path.join(assets, '02_esg_answer_no_market.png');
const scope = path.join(assets, '03_scope1_proceed.png');
const backstage = path.join(assets, '04_scope1_backstage.png');
const review = path.join(assets, '05_conflict_review.png');
const market = path.join(assets, '06_market_explicit_only.png');
const out = path.join(__dirname, '초ROK_수페스타_발표자료.pptx');

function title(slide, kicker, heading, sub = '') {
  slide.addText(kicker, { x: 0.60, y: 0.40, w: 5.2, h: 0.25, fontFace: 'Aptos', fontSize: 9.5, bold: true, color: C.green, charSpacing: 1.2, margin: 0 });
  slide.addText(heading, { x: 0.60, y: 0.75, w: 12.0, h: 0.55, fontFace: FONT, fontSize: 25, bold: true, color: C.ink, margin: 0, fit: 'shrink' });
  if (sub) slide.addText(sub, { x: 0.61, y: 1.35, w: 11.9, h: 0.36, fontFace: FONT, fontSize: 11.5, color: C.slate, margin: 0, fit: 'shrink' });
}

function card(slide, x, y, w, h, heading, body, accent = C.green, fill = C.white) {
  slide.addShape(pptx.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.08, fill: { color: fill }, line: { color: C.line, width: 0.8 } });
  slide.addShape(pptx.ShapeType.rect, { x, y, w: 0.07, h, fill: { color: accent }, line: { color: accent } });
  slide.addText(heading, { x: x + 0.22, y: y + 0.16, w: w - 0.38, h: 0.32, fontFace: FONT, fontSize: 12.5, bold: true, color: C.ink, margin: 0, fit: 'shrink' });
  slide.addText(body, { x: x + 0.22, y: y + 0.56, w: w - 0.38, h: h - 0.72, fontFace: FONT, fontSize: 10.2, color: C.slate, margin: 0.01, fit: 'shrink', valign: 'top' });
}

function pill(slide, text, x, y, w, fill = C.mint, color = C.green) {
  slide.addShape(pptx.ShapeType.roundRect, { x, y, w, h: 0.35, rectRadius: 0.08, fill: { color: fill }, line: { color: fill } });
  slide.addText(text, { x, y: y + 0.01, w, h: 0.29, fontFace: FONT, fontSize: 9, bold: true, color, align: 'center', valign: 'mid', margin: 0, fit: 'shrink' });
}

function imageBox(slide, imgPath, x, y, w, h) {
  slide.addShape(pptx.ShapeType.roundRect, { x, y, w, h, rectRadius: 0.06, fill: { color: C.white }, line: { color: C.line, width: 0.8 } });
  slide.addImage({ path: imgPath, x: x + 0.07, y: y + 0.07, w: w - 0.14, h: h - 0.14, sizing: 'contain' });
}

{
  const s = pptx.addSlide('MASTER'); s.background = { color: C.forest };
  s.addShape(pptx.ShapeType.ellipse, { x: 8.66, y: 0.18, w: 4.42, h: 4.42, fill: { color: '185F50' }, line: { color: '185F50' } });
  s.addText('2026 ESG × AI CHALLENGE · TRACK C', { x: 0.75, y: 0.72, w: 6.2, h: 0.28, fontFace: 'Aptos', fontSize: 11, bold: true, color: '83E1B3', charSpacing: 1.2, margin: 0 });
  s.addText('수페스타', { x: 0.75, y: 1.38, w: 6.8, h: 0.92, fontFace: FONT, fontSize: 40, bold: true, color: C.white, margin: 0 });
  s.addText('ESG 질문을 검증 가능한\n다음 행동으로 바꾸는 AI', { x: 0.78, y: 2.46, w: 7.2, h: 1.15, fontFace: FONT, fontSize: 25, bold: true, color: 'C8F4DD', margin: 0, fit: 'shrink' });
  s.addText('KAC 지식을 질문별로 선택하고 실행 Skill을 실제로 수행한 뒤,\n로컬 AI가 검증 결과만 자연어로 설명합니다.', { x: 0.78, y: 3.92, w: 7.15, h: 0.88, fontFace: FONT, fontSize: 14, color: 'E4F3ED', margin: 0, fit: 'shrink' });
  pill(s, '질문 → Context → KAC → Skill → 판정 → 설명', 0.78, 5.20, 4.75, '1B6756', 'E7FFF3');
  s.addImage({ path: mascot, x: 8.62, y: 1.38, w: 3.25, h: 3.25, sizing: 'contain' });
  s.addText('팀 초 ROK · 박상훈', { x: 0.78, y: 6.20, w: 3.4, h: 0.28, fontFace: FONT, fontSize: 11, color: 'C8DAD4', margin: 0 });
}

{
  const s = pptx.addSlide('MASTER'); title(s, '01 · PROBLEM', 'ESG 지식은 많지만, “그래서 무엇을 해야 하나”가 끊겨 있습니다', '정의 검색만으로는 사용자의 상황에 맞는 확인 순서와 책임 있는 다음 행동을 정하기 어렵습니다.');
  card(s, 0.72, 2.02, 3.78, 2.48, 'ESG 입문자', '“ESG가 정확히 무엇인가요?”\n\n관련 없는 탄소시장 이야기 없이 질문한 개념만 이해하고 싶습니다.');
  card(s, 4.78, 2.02, 3.78, 2.48, '기업 담당자', '“우리 보일러는 Scope 몇인가요?”\n\n활동·조직경계·소유통제·증빙을 함께 확인해야 합니다.');
  card(s, 8.84, 2.02, 3.78, 2.48, '산주·구매 검토자', '“절차는 어디까지 왔고 무엇을 확인해야 하나요?”\n\n등록·권리·검증·거래 조건이 서로 연결돼 있습니다.');
  s.addShape(pptx.ShapeType.roundRect, { x: 0.84, y: 5.10, w: 11.68, h: 0.92, rectRadius: 0.08, fill: { color: C.mint }, line: { color: C.mint } });
  s.addText('문제는 정보 부족이 아니라, 지식이 판단과 행동으로 이어지지 않는 구조입니다.', { x: 1.05, y: 5.38, w: 11.25, h: 0.34, fontFace: FONT, fontSize: 17, bold: true, color: C.forest, align: 'center', margin: 0, fit: 'shrink' });
}

{
  const s = pptx.addSlide('MASTER'); title(s, '02 · PRODUCT', '정확히 만드는 것은 브라우저형 ESG 대화 서비스입니다', '사용자는 자연스러운 답변을 보고, 필요할 때만 근거·Skill·실행기록을 펼쳐봅니다.');
  imageBox(s, home, 0.64, 1.90, 7.84, 4.85);
  card(s, 8.80, 1.92, 3.78, 1.18, '앞단', '결론 · 쉬운 설명 · 확인 이유 · 지금 할 일 · 다음 질문');
  card(s, 8.80, 3.30, 3.78, 1.18, '뒷단', 'Context · KAC · 실행 Skill · 근거 · 산출물 · Run Record', C.blue);
  card(s, 8.80, 4.68, 3.78, 1.18, '행동 연결', '구매처를 직접 물은 경우에만 산림탄소마켓을 선택지로 표시', C.amber);
  pill(s, '일반 ESG 답변은 마켓으로 흐르지 않음', 8.94, 6.23, 3.48, C.coralBg, C.coral);
}

{
  const s = pptx.addSlide('MASTER'); title(s, '03 · WHY KAC', '지식을 설명에서 끝내지 않고, 실행 규칙으로 연결합니다', 'KAC는 사용자의 상황과 목표에 맞춰 지식이 어떤 확인·판단·행동으로 이어지는지 고정합니다.');
  const nodes = ['Identity', 'Goal', 'Task', 'Knowledge', 'Method', 'Skill'];
  nodes.forEach((n, i) => {
    const x = 0.64 + i * 2.08;
    s.addShape(pptx.ShapeType.roundRect, { x, y: 2.06, w: 1.73, h: 1.18, rectRadius: 0.08, fill: { color: i === 5 ? C.forest : C.white }, line: { color: i === 5 ? C.forest : C.line } });
    s.addText(n, { x: x + 0.10, y: 2.43, w: 1.53, h: 0.30, fontFace: 'Aptos', fontSize: 13.5, bold: true, color: i === 5 ? C.white : C.ink, align: 'center', margin: 0, fit: 'shrink' });
    if (i < 5) s.addText('→', { x: x + 1.76, y: 2.45, w: 0.30, h: 0.28, fontFace: 'Aptos', fontSize: 18, bold: true, color: C.green, align: 'center', margin: 0 });
  });
  card(s, 0.78, 4.02, 3.66, 1.48, '왜 구조화하나', '같은 기준을 질문마다 흔들리지 않게 재사용하고, 원문 근거와 제약을 함께 보존하기 위해');
  card(s, 4.84, 4.02, 3.66, 1.48, '왜 Skill로 묶나', '지식 설명을 입력 검사·판정·산출물 생성이 가능한 실행 단위로 바꾸기 위해');
  card(s, 8.90, 4.02, 3.66, 1.48, '왜 배포하나', '검증된 행동 체인을 서비스에서 반복 실행하고 매 실행의 기록과 해시를 남기기 위해');
  s.addText('수페스타는 KAC 지식을 근거로 사용하고, KAC에서 구조화·배포한 Skill을 실행 규칙으로 사용합니다.', { x: 1.10, y: 6.10, w: 11.1, h: 0.38, fontFace: FONT, fontSize: 14.5, bold: true, color: C.forest, align: 'center', margin: 0, fit: 'shrink' });
}

{
  const s = pptx.addSlide('MASTER'); title(s, '04 · ARCHITECTURE', '판정은 Skill이 만들고, 로컬 AI는 검증 결과만 설명합니다', 'UI와 서버는 별도 Runtime 코드이며, Stage Skill만으로 챗봇 전체가 자동 생성됐다고 주장하지 않습니다.');
  const flow = [
    ['1', 'Context', '사용자 진술만\n타입 필드로'], ['2', 'Composite', '라우터 1회\n단일 진입점'], ['3', 'KAC + Skill', '체인 선택·해시\n도메인 실행 1회'],
    ['4', '판정', 'PROCEED\nREVIEW · STOP'], ['5', 'Local AI', '검증 결과만\n자연어 표현'], ['6', 'Risk Gate', '권한·주장·링크\n재검사'],
  ];
  flow.forEach((f, i) => {
    const positions = [
      [0.80, 1.94], [4.98, 1.94], [9.16, 1.94],
      [9.16, 4.02], [4.98, 4.02], [0.80, 4.02],
    ];
    const [x, y] = positions[i];
    card(s, x, y, 3.56, 1.52, `${f[0]} · ${f[1]}`, f[2], i === 3 ? C.amber : i === 5 ? C.coral : C.green, i === 3 ? C.amberBg : C.white);
    if (i === 0 || i === 1) s.addText('→', { x: x + 3.64, y: y + 0.58, w: 0.35, h: 0.35, fontFace: 'Aptos', fontSize: 17, bold: true, color: C.green, align: 'center', margin: 0 });
    if (i === 2) s.addText('↓', { x: x + 1.60, y: y + 1.60, w: 0.35, h: 0.35, fontFace: 'Aptos', fontSize: 17, bold: true, color: C.green, align: 'center', margin: 0 });
    if (i === 3 || i === 4) s.addText('←', { x: x - 0.43, y: y + 0.58, w: 0.35, h: 0.35, fontFace: 'Aptos', fontSize: 17, bold: true, color: C.green, align: 'center', margin: 0 });
  });
  s.addShape(pptx.ShapeType.roundRect, { x: 0.86, y: 5.80, w: 11.62, h: 0.64, rectRadius: 0.08, fill: { color: C.blueBg }, line: { color: C.blueBg } });
  s.addText('모든 실행은 Context · KAC · Skill · 산출물 · SHA-256이 포함된 Run Record로 남습니다.', { x: 1.08, y: 5.98, w: 11.18, h: 0.28, fontFace: FONT, fontSize: 13, bold: true, color: C.blue, align: 'center', margin: 0, fit: 'shrink' });
}

{
  const s = pptx.addSlide('MASTER'); title(s, '05 · DEMO A', '“ESG가 무엇인가요?”에는 ESG만 답합니다', '질문과 직접 관련된 KAC만 선택하며 산림탄소마켓 링크는 표시하지 않습니다.');
  imageBox(s, esg, 0.64, 1.88, 8.22, 4.90);
  card(s, 9.18, 1.98, 3.28, 1.24, '직접 답변', 'E·S·G의 의미와 탄소가 환경 영역의 한 주제라는 점만 설명');
  card(s, 9.18, 3.46, 3.28, 1.24, '지식 선택', '85개 Identity·Concept Skill 중 질문과 관련된 체인만 사용', C.blue);
  card(s, 9.18, 4.94, 3.28, 1.24, '비홍보 원칙', '구매 의도가 없으므로 외부 마켓 handoff 없음', C.coral);
}

{
  const s = pptx.addSlide('MASTER'); title(s, '06 · DEMO B', '자연스러운 질문을 구조화해 Scope 1을 실행 판정합니다', '“저희 회사가 소유·운영하는 보일러에서 도시가스 1,250 Nm³를 사용했고 고지서가 있습니다. Scope 몇인가요?”');
  imageBox(s, scope, 0.64, 1.88, 8.18, 4.90);
  card(s, 9.10, 1.94, 3.42, 1.05, 'Context', '소유·운영 · 도시가스 · 1,250 Nm³ · 2026년 8월 · 고지서');
  card(s, 9.10, 3.20, 3.42, 1.05, 'Run Skill', 'scope-activity-classification-run', C.blue);
  card(s, 9.10, 4.46, 3.42, 1.05, '실행 결과', 'SCOPE_CLASSIFICATION · PROCEED · SCOPE_1', C.green, C.mint2);
  card(s, 9.10, 5.72, 3.42, 0.90, '사람의 확인', '실제 보고 전 조직경계·증빙 원문 대조', C.amber, C.amberBg);
}

{
  const s = pptx.addSlide('MASTER'); title(s, '07 · EVIDENCE', '답변 뒤에서 실제 실행된 KAC와 Skill을 확인할 수 있습니다', '정적 예시가 아니라 브라우저 질문 실행에서 생성된 구조화 입력·체인·해시·판정 기록입니다.');
  imageBox(s, backstage, 0.64, 1.88, 8.52, 4.90);
  card(s, 9.47, 1.94, 3.04, 1.04, '사용자 입력', '추정하지 않고 출처·규칙·신뢰도와 함께 타입 필드로 승격');
  card(s, 9.47, 3.18, 3.04, 1.04, 'KAC 체인', 'Identity → Goal → Task → Knowledge → Method → Skill', C.blue);
  card(s, 9.47, 4.42, 3.04, 1.04, '불변성', 'Stage vault 변경 없음 · 선택 파일 해시 확인', C.green);
  card(s, 9.47, 5.66, 3.04, 0.94, '재검증', 'Run ID와 SHA-256으로 결과 추적', C.amber, C.amberBg);
}

{
  const s = pptx.addSlide('MASTER'); title(s, '08 · SAFETY', '모호하거나 충돌하면 그럴듯하게 확정하지 않습니다', '보일러 연소와 구매전력을 한 질문에 섞으면 두 활동을 분리하도록 REVIEW합니다.');
  imageBox(s, review, 0.64, 1.88, 8.18, 4.90);
  card(s, 9.10, 1.94, 3.42, 1.14, 'PROCEED', '필요한 입력과 근거가 충분하고 충돌이 없을 때 실행 결과 제시', C.green, C.mint2);
  card(s, 9.10, 3.34, 3.42, 1.14, 'REVIEW', '입력 누락·상충·공시 판단처럼 사람 확인이 필요한 경우 보완 질문', C.amber, C.amberBg);
  card(s, 9.10, 4.74, 3.42, 1.14, 'STOP', '실시간 시세·투자추천·무근거 계산·우회·가짜 증거·외부 실행 차단', C.coral, C.coralBg);
  pill(s, 'REVIEW/STOP에서는 로컬 AI 자유 생성 차단', 9.16, 6.26, 3.28, C.blueBg, C.blue);
}

{
  const s = pptx.addSlide('MASTER'); title(s, '09 · ACTION & VALIDATION', '구매처를 직접 물은 경우에만 실제 행동 지점을 보여줍니다', '산림탄소마켓은 제품의 종착점이 아니라, 명시적 구매 의도에서만 나타나는 제한된 handoff입니다.');
  imageBox(s, market, 0.64, 1.88, 7.28, 4.92);
  card(s, 8.22, 1.92, 2.10, 1.12, '35', '자동 테스트\n전부 PASS', C.blue, C.blueBg);
  card(s, 10.54, 1.92, 2.10, 1.12, '63', '결정론 시나리오\n전부 PASS', C.green, C.mint2);
  card(s, 8.22, 3.28, 2.10, 1.12, '10', '로컬 AI 근거 답변\n전부 PASS', C.amber, C.amberBg);
  card(s, 10.54, 3.28, 2.10, 1.12, '9', '지원 라우트\n전부 커버', C.coral, C.coralBg);
  s.addShape(pptx.ShapeType.roundRect, { x: 8.22, y: 4.72, w: 4.42, h: 1.34, rectRadius: 0.08, fill: { color: C.white }, line: { color: C.line } });
  s.addText('검증된 범위', { x: 8.48, y: 4.92, w: 3.9, h: 0.26, fontFace: FONT, fontSize: 12.5, bold: true, color: C.ink, margin: 0 });
  s.addText('PROCEED · REVIEW · STOP\n입력 바이트 보존 · KAC · Output Gate · 마켓 링크 1건', { x: 8.48, y: 5.30, w: 3.88, h: 0.52, fontFace: FONT, fontSize: 10.2, color: C.slate, margin: 0, fit: 'shrink' });
  pill(s, '안내와 준비는 AI · 최종 거래 판단은 사람', 8.42, 6.32, 4.02, C.amberBg, C.amber);
}

{
  const s = pptx.addSlide('MASTER'); s.background = { color: C.forest };
  s.addText('수페스타', { x: 0.78, y: 0.80, w: 4.5, h: 0.65, fontFace: FONT, fontSize: 25, bold: true, color: '83E1B3', margin: 0 });
  s.addText('설명하는 AI를 넘어,\n검증된 지식과 Skill이\n실제로 실행되는 ESG AI', { x: 0.78, y: 1.62, w: 7.6, h: 2.42, fontFace: FONT, fontSize: 34, bold: true, color: C.white, margin: 0, fit: 'shrink' });
  s.addText('사용자에게는 자연스러운 답변을,\n뒷단에는 KAC · 실행 Skill · 근거 · Run Record를.', { x: 0.82, y: 4.58, w: 6.85, h: 0.84, fontFace: FONT, fontSize: 15, color: 'D5EEE4', margin: 0, fit: 'shrink' });
  s.addImage({ path: mascot, x: 8.65, y: 1.40, w: 3.25, h: 3.25, sizing: 'contain' });
  pill(s, '구조화 → Skill 묶음 → 배포 → 실행 증명', 8.42, 5.08, 3.76, '1B6756', 'E7FFF3');
  s.addText('팀 초 ROK · 박상훈\ngithub.com/pak3430/supestar-esg-ai', { x: 8.50, y: 6.04, w: 3.65, h: 0.58, fontFace: FONT, fontSize: 9.5, color: 'C8DAD4', align: 'center', margin: 0, fit: 'shrink' });
}

pptx.writeFile({ fileName: out }).then(() => process.stdout.write(out + '\n'));
