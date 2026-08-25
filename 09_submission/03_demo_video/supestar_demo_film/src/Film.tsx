import React from 'react';
import { AbsoluteFill, Easing, Img, interpolate, staticFile, useCurrentFrame } from 'remotion';
import { ART_H, Scene } from './scenes';

const C = {
  bg: '#F7F5EE', ink: '#142922', forest: '#0D4B3D', green: '#197260', mint: '#DFF2EA', mint2: '#EEF8F4',
  line: '#BED7CF', slate: '#53645F', white: '#FFFFFF', amber: '#A86916', amberBg: '#FFF0D7',
  coral: '#C94F49', coralBg: '#FDE6E2', blue: '#2D628D', blueBg: '#E6F0FA',
};
const FONT = "'Noto Sans CJK KR','Noto Sans KR','Apple SD Gothic Neo',sans-serif";
const clamp = { extrapolateLeft: 'clamp' as const, extrapolateRight: 'clamp' as const };
const fade = (f: number, start: number, dur = 18) => interpolate(f, [start, start + dur], [0, 1], { ...clamp, easing: Easing.out(Easing.cubic) });
const rise = (f: number, start: number, dur = 18) => interpolate(f, [start, start + dur], [34, 0], { ...clamp, easing: Easing.out(Easing.cubic) });

const Base: React.FC<{ children: React.ReactNode; dark?: boolean }> = ({ children, dark }) => (
  <div style={{ position: 'absolute', inset: 0, height: ART_H, overflow: 'hidden', background: dark ? C.forest : C.bg, color: dark ? C.white : C.ink, fontFamily: FONT }}>
    {!dark && <div style={{ position: 'absolute', inset: 0, opacity: 0.28, backgroundImage: 'linear-gradient(#E4E0D4 1px, transparent 1px), linear-gradient(90deg, #E4E0D4 1px, transparent 1px)', backgroundSize: '60px 60px' }} />}
    {children}
  </div>
);

const Caption: React.FC<{ text: string }> = ({ text }) => (
  <div style={{ position: 'absolute', left: 0, right: 0, bottom: 0, height: 180, background: C.bg, borderTop: `5px solid ${C.forest}`, display: 'flex', alignItems: 'center', justifyContent: 'center', padding: '0 88px', boxSizing: 'border-box', fontFamily: FONT, fontSize: 48, lineHeight: 1.25, fontWeight: 850, color: C.ink, textAlign: 'center', letterSpacing: '-1.5px' }}>{text}</div>
);

const Kicker: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const parts = typeof children === 'string' ? children.split(' · ') : null;
  return <div style={{ position: 'absolute', left: 96, top: 62, color: C.green, fontSize: 25, fontWeight: 850, letterSpacing: '3px', display: 'flex', alignItems: 'center', gap: 12 }}>
    {parts ? <><span>{parts[0]}</span><span>/</span><span>{parts[1]}</span></> : children}
  </div>;
};
const Head: React.FC<{ children: React.ReactNode; top?: number; size?: number; color?: string }> = ({ children, top = 112, size = 52, color = C.ink }) => <div style={{ position: 'absolute', left: 96, right: 96, top, fontSize: size, fontWeight: 900, lineHeight: 1.22, color, letterSpacing: '-2px' }}>{children}</div>;

const Card: React.FC<{ title: string; body: string; active?: boolean; warning?: boolean; danger?: boolean; style?: React.CSSProperties }> = ({ title, body, active, warning, danger, style }) => {
  const fill = active ? C.forest : warning ? C.amberBg : danger ? C.coralBg : C.white;
  const accent = active ? '#83E1B3' : warning ? C.amber : danger ? C.coral : C.green;
  return <div style={{ background: fill, border: `3px solid ${active ? C.forest : C.line}`, borderLeft: `12px solid ${accent}`, borderRadius: 18, padding: '24px 28px', boxSizing: 'border-box', color: active ? C.white : C.ink, ...style }}>
    <div style={{ fontSize: 29, fontWeight: 900, marginBottom: 14 }}>{title}</div>
    <div style={{ fontSize: 23, fontWeight: 560, lineHeight: 1.48, color: active ? '#D5EEE4' : C.slate, whiteSpace: 'pre-line' }}>{body}</div>
  </div>;
};

const Screen: React.FC<{ src: string; label: string; style?: React.CSSProperties }> = ({ src, label, style }) => (
  <div style={{ position: 'absolute', background: C.white, border: `5px solid ${C.forest}`, borderRadius: 20, overflow: 'hidden', boxShadow: '0 18px 45px rgba(20,41,34,.14)', ...style }}>
    <div style={{ position: 'absolute', left: 18, top: 16, zIndex: 2, background: C.forest, color: C.white, borderRadius: 999, padding: '8px 16px', fontSize: 18, fontWeight: 800 }}>{label}</div>
    <Img src={staticFile(`images/${src}`)} style={{ width: '100%', height: '100%', objectFit: 'contain', background: C.white }} />
  </div>
);

const TitleScene: React.FC<{ f: number }> = ({ f }) => (
  <Base dark>
    <div style={{ position: 'absolute', width: 760, height: 760, borderRadius: '50%', right: -90, top: -140, background: '#185F50' }} />
    <div style={{ position: 'absolute', left: 105, top: 70, opacity: fade(f, 0), transform: `translateY(${rise(f, 0)}px)` }}>
      <div style={{ color: '#83E1B3', fontSize: 24, fontWeight: 850, letterSpacing: 4 }}>2026 ESG × AI CHALLENGE · TRACK C</div>
      <div style={{ fontSize: 94, fontWeight: 950, marginTop: 66 }}>수페스타</div>
      <div style={{ color: '#C8F4DD', fontSize: 49, lineHeight: 1.36, fontWeight: 900, marginTop: 28 }}>ESG 질문을 검증 가능한<br />다음 행동으로 바꾸는 AI</div>
      <div style={{ display: 'inline-block', background: '#1B6756', borderRadius: 999, padding: '14px 24px', fontSize: 25, fontWeight: 800, marginTop: 42 }}>Context → KAC → Skill → 판정 → 설명</div>
    </div>
    <Img src={staticFile('images/mascot.png')} style={{ position: 'absolute', right: 145, top: 185, width: 430, height: 430, objectFit: 'contain', opacity: fade(f, 20), transform: `translateY(${rise(f, 20)}px)` }} />
  </Base>
);

const ProblemScene: React.FC<{ f: number }> = ({ f }) => {
  const items = [
    ['ESG 입문자', '질문한 개념만\n이해하고 싶습니다'],
    ['기업 담당자', '우리 보일러는\nScope 몇인가요?'],
    ['산주·구매 검토자', '어떤 증거와 절차를\n확인해야 하나요?'],
  ];
  return <Base><Kicker>01 · PROBLEM</Kicker><Head>지식은 많지만, “그래서 무엇을 해야 하나요?”에서 멈춥니다</Head>
    <div style={{ position: 'absolute', left: 96, right: 96, top: 250, display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 34 }}>
      {items.map((x, i) => <div key={x[0]} style={{ opacity: fade(f, 10 + i * 12), transform: `translateY(${rise(f, 10 + i * 12)}px)` }}><Card title={x[0]} body={x[1]} style={{ height: 285 }} /></div>)}
    </div>
    <div style={{ position: 'absolute', left: 190, right: 190, top: 630, background: C.mint, color: C.forest, borderRadius: 20, padding: '28px 38px', textAlign: 'center', fontSize: 34, fontWeight: 900, opacity: fade(f, 55) }}>문제는 정보 부족이 아니라, 지식과 행동의 단절입니다.</div>
  </Base>;
};

const KacScene: React.FC<{ f: number }> = ({ f }) => {
  const nodes = ['Identity', 'Goal', 'Task', 'Knowledge', 'Method', 'Skill'];
  return <Base><Kicker>02 · WHY KAC</Kicker><Head>지식을 설명에서 끝내지 않고 실행 규칙으로 연결합니다</Head>
    <div style={{ position: 'absolute', left: 72, right: 72, top: 245, display: 'flex', alignItems: 'center', gap: 12 }}>
      {nodes.map((n, i) => <React.Fragment key={n}><div style={{ flex: 1, height: 132, borderRadius: 18, border: `3px solid ${i === 5 ? C.forest : C.line}`, background: i === 5 ? C.forest : C.white, color: i === 5 ? C.white : C.ink, display: 'flex', alignItems: 'center', justifyContent: 'center', fontFamily: 'Aptos', fontSize: 27, fontWeight: 850, opacity: fade(f, 8 + i * 7), transform: `translateY(${rise(f, 8 + i * 7)}px)` }}>{n}</div>{i < 5 && <div style={{ color: C.green, fontSize: 40, fontWeight: 900 }}>→</div>}</React.Fragment>)}
    </div>
    <div style={{ position: 'absolute', left: 96, right: 96, top: 500, display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 28 }}>
      <div style={{ opacity: fade(f, 54) }}><Card title="왜 구조화하나" body="기준·근거·제약을 흔들리지 않게 재사용" style={{ height: 180 }} /></div>
      <div style={{ opacity: fade(f, 68) }}><Card title="왜 Skill로 묶나" body="입력 검사·판정·산출물 생성을 실제 실행" style={{ height: 180 }} /></div>
      <div style={{ opacity: fade(f, 82) }}><Card title="왜 배포하나" body="검증된 행동을 반복하고 실행기록·해시 보존" style={{ height: 180 }} /></div>
    </div>
  </Base>;
};

const ArchitectureScene: React.FC<{ f: number }> = ({ f }) => {
  const flow = [
    ['1 · Context', '사용자 진술만 타입 필드로'], ['2 · Composite', '라우터 1회 · 단일 진입점'], ['3 · KAC + Skill', '체인 선택·해시 · 실행 1회'],
    ['4 · 판정', 'PROCEED · REVIEW · STOP'], ['5 · Local AI', '검증 결과만 자연어 표현'], ['6 · Risk Gate', '권한·주장·링크 재검사'],
  ];
  return <Base><Kicker>03 · ARCHITECTURE</Kicker><Head>판정은 Skill이 만들고, 로컬 AI는 검증 결과만 설명합니다</Head>
    <div style={{ position: 'absolute', left: 95, right: 95, top: 245, display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 30 }}>
      {flow.map((x, i) => <div key={x[0]} style={{ opacity: fade(f, 8 + i * 10), transform: `translateY(${rise(f, 8 + i * 10)}px)` }}><Card title={x[0]} body={x[1]} warning={i === 3} danger={i === 5} style={{ height: 165 }} /></div>)}
    </div>
    <div style={{ position: 'absolute', left: 150, right: 150, top: 655, background: C.blueBg, color: C.blue, borderRadius: 18, padding: 24, textAlign: 'center', fontSize: 31, fontWeight: 900, opacity: fade(f, 76) }}>모든 실행은 Context · KAC · Skill · 산출물 · SHA-256으로 기록됩니다.</div>
  </Base>;
};

const ProductScene: React.FC<{ f: number }> = ({ f }) => (
  <Base><Kicker>04 · PRODUCT</Kicker><Head>최종 MVP는 브라우저형 ESG 대화 서비스입니다</Head>
    <Screen src="home.png" label="실제 수페스타 브라우저 MVP" style={{ left: 76, top: 205, width: 1250, height: 640, opacity: fade(f, 5) }} />
    <div style={{ position: 'absolute', left: 1370, right: 72, top: 225, display: 'grid', gap: 24 }}>
      <div style={{ opacity: fade(f, 22) }}><Card title="앞단" body="결론 · 쉬운 설명 · 확인 이유 · 지금 할 일 · 다음 질문" style={{ height: 165 }} /></div>
      <div style={{ opacity: fade(f, 42) }}><Card title="뒷단" body="Context · KAC · 실행 Skill · 근거 · 산출물 · Run Record" style={{ height: 165 }} /></div>
      <div style={{ opacity: fade(f, 62) }}><Card title="행동 연결" body="구매처를 직접 물은 경우에만 마켓 선택지 표시" warning style={{ height: 165 }} /></div>
    </div>
  </Base>
);

const EsgScene: React.FC<{ f: number }> = ({ f }) => (
  <Base><Kicker>05 · DEMO A</Kicker><Head>“ESG가 무엇인가요?”에는 ESG만 답합니다</Head>
    <Screen src="esg.png" label="실제 답변 · 마켓 링크 없음" style={{ left: 70, top: 205, width: 1280, height: 640, opacity: fade(f, 5) }} />
    <div style={{ position: 'absolute', left: 1400, right: 70, top: 230, display: 'grid', gap: 24 }}>
      <div style={{ opacity: fade(f, 22) }}><Card title="직접 답변" body="환경 · 사회 · 지배구조의 의미" style={{ height: 145 }} /></div>
      <div style={{ opacity: fade(f, 42) }}><Card title="지식 선택" body="질문과 관련된 Identity 체인만 사용" style={{ height: 145 }} /></div>
      <div style={{ opacity: fade(f, 62) }}><Card title="비홍보 원칙" body="구매 의도가 없으므로 외부 handoff 없음" danger style={{ height: 145 }} /></div>
    </div>
  </Base>
);

const ScopeScene: React.FC<{ f: number }> = ({ f }) => (
  <Base><Kicker>06 · DEMO B</Kicker><Head>자연스러운 질문을 구조화해 Scope 1을 실행 판정합니다</Head>
    <Screen src="scope.png" label="실제 답변 · SCOPE_CLASSIFICATION" style={{ left: 70, top: 205, width: 1280, height: 640, opacity: fade(f, 5) }} />
    <div style={{ position: 'absolute', left: 1400, right: 70, top: 215, display: 'grid', gap: 18 }}>
      <div style={{ opacity: fade(f, 18) }}><Card title="Context" body={'소유·운영 · 도시가스\n1,250 Nm³ · 기간 · 고지서'} style={{ height: 145 }} /></div>
      <div style={{ opacity: fade(f, 38) }}><Card title="Run Skill" body="scope-activity-classification-run" style={{ height: 130 }} /></div>
      <div style={{ opacity: fade(f, 58) }}><Card title="실행 결과" body="PROCEED · SCOPE_1" active style={{ height: 130 }} /></div>
      <div style={{ opacity: fade(f, 76) }}><Card title="사람의 확인" body="실제 보고 전 조직경계·증빙 원문 대조" warning style={{ height: 130 }} /></div>
    </div>
  </Base>
);

const EvidenceScene: React.FC<{ f: number }> = ({ f }) => (
  <Base><Kicker>07 · EVIDENCE</Kicker><Head>답변 뒤에서 실제 실행된 KAC와 Skill을 확인할 수 있습니다</Head>
    <Screen src="backstage.png" label="실제 질문에서 생성된 뒷단 증거" style={{ left: 65, top: 205, width: 1320, height: 640, opacity: fade(f, 5) }} />
    <div style={{ position: 'absolute', left: 1430, right: 65, top: 218, display: 'grid', gap: 18 }}>
      <div style={{ opacity: fade(f, 18) }}><Card title="사용자 입력" body="출처·규칙·신뢰도와 함께 타입 필드로 승격" style={{ height: 138 }} /></div>
      <div style={{ opacity: fade(f, 36) }}><Card title="KAC 체인" body="Identity → Goal → Task → Knowledge → Method → Skill" style={{ height: 138 }} /></div>
      <div style={{ opacity: fade(f, 54) }}><Card title="불변성" body="Stage vault 변경 없음 · 파일 해시 확인" style={{ height: 138 }} /></div>
      <div style={{ opacity: fade(f, 72) }}><Card title="재검증" body="Run ID와 SHA-256으로 결과 추적" warning style={{ height: 138 }} /></div>
    </div>
  </Base>
);

const ReviewScene: React.FC<{ f: number }> = ({ f }) => (
  <Base><Kicker>08 · SAFETY</Kicker><Head>모호하거나 충돌하면 그럴듯하게 확정하지 않습니다</Head>
    <Screen src="review.png" label="실제 REVIEW 답변" style={{ left: 70, top: 205, width: 1280, height: 640, opacity: fade(f, 5) }} />
    <div style={{ position: 'absolute', left: 1400, right: 70, top: 225, display: 'grid', gap: 22 }}>
      <div style={{ opacity: fade(f, 18) }}><Card title="PROCEED" body="입력과 근거가 충분하고 충돌 없음" active style={{ height: 140 }} /></div>
      <div style={{ opacity: fade(f, 38) }}><Card title="REVIEW" body="입력 누락·상충 · 사람 확인 필요" warning style={{ height: 140 }} /></div>
      <div style={{ opacity: fade(f, 58) }}><Card title="STOP" body="실시간 시세·투자추천·가짜 증거·외부 실행" danger style={{ height: 140 }} /></div>
      <div style={{ opacity: fade(f, 74), background: C.blueBg, color: C.blue, borderRadius: 16, padding: 20, textAlign: 'center', fontSize: 23, fontWeight: 850 }}>REVIEW/STOP에서는<br />로컬 AI 자유 생성 차단</div>
    </div>
  </Base>
);

const MarketScene: React.FC<{ f: number }> = ({ f }) => (
  <Base><Kicker>09 · EXPLICIT ACTION</Kicker><Head>구매처를 직접 물은 경우에만 산림탄소마켓을 보여줍니다</Head>
    <Screen src="market.png" label="실제 답변 · 명시적 구매 질문" style={{ left: 70, top: 205, width: 1280, height: 640, opacity: fade(f, 5) }} />
    <div style={{ position: 'absolute', left: 1400, right: 70, top: 250, display: 'grid', gap: 28 }}>
      <div style={{ opacity: fade(f, 20) }}><Card title="제한된 handoff" body="구매처·구매 방법을 직접 물은 경우에만 표시" active style={{ height: 170 }} /></div>
      <div style={{ opacity: fade(f, 44) }}><Card title="최신 조건" body="프로젝트·가격·수량·인증은 마켓에서 직접 확인" style={{ height: 170 }} /></div>
      <div style={{ opacity: fade(f, 68) }}><Card title="책임 경계" body="구매·결제·등록부 변경·거래 보증은 수행하지 않음" warning style={{ height: 170 }} /></div>
    </div>
  </Base>
);

const ValidationScene: React.FC<{ f: number }> = ({ f }) => {
  const metrics = [['23', '단위·통합 테스트'], ['60', '결정론 시나리오'], ['8', '로컬 AI 근거 답변'], ['9', '지원 라우트']];
  return <Base><Kicker>10 · VALIDATION</Kicker><Head>실행 구조와 안전 경계를 최신 코드로 다시 검증했습니다</Head>
    <div style={{ position: 'absolute', left: 100, right: 100, top: 250, display: 'grid', gridTemplateColumns: 'repeat(4,1fr)', gap: 28 }}>
      {metrics.map((m, i) => <div key={m[0]} style={{ height: 240, borderRadius: 22, border: `3px solid ${C.line}`, borderTop: `14px solid ${[C.blue, C.green, C.amber, C.coral][i]}`, background: C.white, display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', opacity: fade(f, 10 + i * 12), transform: `translateY(${rise(f, 10 + i * 12)}px)` }}>
        <div style={{ fontFamily: 'Aptos', fontSize: 78, fontWeight: 900, color: C.ink }}>{m[0]}</div><div style={{ fontSize: 26, fontWeight: 800, color: C.slate, marginTop: 16 }}>{m[1]}</div><div style={{ fontSize: 21, fontWeight: 800, color: C.green, marginTop: 12 }}>PASS</div>
      </div>)}
    </div>
    <div style={{ position: 'absolute', left: 160, right: 160, top: 600, borderRadius: 18, background: C.mint, padding: 26, textAlign: 'center', fontSize: 31, fontWeight: 900, color: C.forest, opacity: fade(f, 66) }}>PROCEED · REVIEW · STOP 전부 커버 · 입력 바이트 보존 · KAC · Output Gate 확인</div>
  </Base>;
};

const CloseScene: React.FC<{ f: number }> = ({ f }) => (
  <Base dark>
    <div style={{ position: 'absolute', left: 110, top: 90, opacity: fade(f, 0), transform: `translateY(${rise(f, 0)}px)` }}>
      <div style={{ color: '#83E1B3', fontSize: 35, fontWeight: 900 }}>수페스타</div>
      <div style={{ fontSize: 66, lineHeight: 1.35, fontWeight: 950, marginTop: 40 }}>설명하는 AI를 넘어,<br />검증된 지식과 Skill이<br />실제로 실행되는 ESG AI</div>
      <div style={{ color: '#D5EEE4', fontSize: 30, lineHeight: 1.45, marginTop: 45 }}>사용자에게는 자연스러운 답변을,<br />뒷단에는 KAC · Skill · 근거 · Run Record를.</div>
    </div>
    <Img src={staticFile('images/mascot.png')} style={{ position: 'absolute', right: 170, top: 155, width: 430, height: 430, objectFit: 'contain', opacity: fade(f, 24) }} />
    <div style={{ position: 'absolute', right: 125, top: 650, width: 550, background: '#1B6756', color: '#E7FFF3', borderRadius: 999, padding: '18px 24px', textAlign: 'center', fontSize: 25, fontWeight: 850, opacity: fade(f, 52) }}>구조화 → Skill 묶음 → 배포 → 실행 증명</div>
  </Base>
);

const GRAPHIC: Record<string, React.FC<{ f: number }>> = {
  s00_title: TitleScene,
  s01_problem: ProblemScene,
  s02_kac: KacScene,
  s03_architecture: ArchitectureScene,
  s04_product: ProductScene,
  s05_esg: EsgScene,
  s06_scope: ScopeScene,
  s07_evidence: EvidenceScene,
  s08_review: ReviewScene,
  s09_market: MarketScene,
  s10_validation: ValidationScene,
  s11_close: CloseScene,
};

export const SceneView: React.FC<{ scene: Scene }> = ({ scene }) => {
  const f = useCurrentFrame();
  const Graphic = GRAPHIC[scene.id];
  return <AbsoluteFill style={{ background: C.bg, fontFamily: FONT }}><Graphic f={f} /><Caption text={scene.subtitle} /></AbsoluteFill>;
};
