/**
 * 시각 문법 — 규칙을 컴포넌트로 강제한다.
 *
 * 원칙: 색과 선 종류를 호출하는 쪽에서 직접 고르지 못하게 한다.
 *       `dashed` 같은 불리언이 아니라 `present` / `absent`라는 의미로 받는다.
 *
 * 이 영상에서 present / absent 는 하나만 뜻한다:
 *   present = AI 가 발견하고 호출할 수 있다
 *   absent  = 그럴 수 없다
 */
import React from 'react';

export const INK = '#141414';
export const GRAY = '#8C8C8C';
export const FAINT = '#C6C2B6';
export const BG = '#F7F4EC';
export const GRID = '#E4E0D4';
export const ACCENT = '#1D4ED8';   // 「도출되어 이어짐」에만
export const FONT = "'Noto Sans KR', 'Helvetica Neue', Helvetica, sans-serif";
export const MONO = "'SF Mono', Menlo, monospace";

export type Presence = 'present' | 'absent';

export const Box: React.FC<{
  x: number; y: number; w: number; h: number;
  presence: Presence;
  emphasis?: boolean;
  r?: number; fill?: string; op?: number;
}> = ({ x, y, w, h, presence, emphasis, r = 10, fill = 'none', op = 1 }) => {
  const absent = presence === 'absent';
  return (
    <rect
      x={x} y={y} width={w} height={h} rx={r} fill={fill} opacity={op}
      stroke={absent ? GRAY : INK}
      strokeWidth={absent ? 3 : emphasis ? 8 : 5}
      strokeDasharray={absent ? '12 11' : undefined}
      strokeLinejoin="round"
    />
  );
};

/** 글자 — 세 단계만 */
type TextRole = 'caption' | 'body' | 'label';
const ROLE_SIZE: Record<TextRole, number> = { caption: 46, body: 27, label: 25 };

export const T: React.FC<{
  x: number; y: number;
  role?: TextRole; size?: number;
  weight?: number; muted?: boolean; faint?: boolean;
  anchor?: 'start' | 'middle' | 'end'; op?: number; mono?: boolean;
  children: React.ReactNode;
}> = ({ x, y, role = 'body', size, weight = 600, muted, faint, anchor = 'start', op = 1, mono, children }) => (
  <text
    x={x} y={y} fontSize={size ?? ROLE_SIZE[role]} fontWeight={weight}
    fill={faint ? FAINT : muted ? GRAY : INK} textAnchor={anchor} opacity={op}
    fontFamily={mono ? MONO : FONT} dominantBaseline="middle"
    style={{ letterSpacing: mono ? '0px' : '-0.4px' }}
  >
    {children}
  </text>
);

/** 흐름 — 강조색은 이 컴포넌트만 쓸 수 있다 */
export const Arrow: React.FC<{
  x1: number; y1: number; x2: number; y2: number;
  op?: number; muted?: boolean; accent?: boolean; sw?: number;
}> = ({ x1, y1, x2, y2, op = 1, muted, accent, sw = 5 }) => {
  const ang = (Math.atan2(y2 - y1, x2 - x1) * 180) / Math.PI;
  const c = accent ? ACCENT : muted ? GRAY : INK;
  return (
    <g opacity={op}>
      <line x1={x1} y1={y1} x2={x2} y2={y2} stroke={c} strokeWidth={sw} strokeLinecap="round" />
      <path d="M0 0 L-20 -10 L-20 10 Z" fill={c}
        transform={`translate(${x2} ${y2}) rotate(${ang})`} />
    </g>
  );
};

export const XMark: React.FC<{ x: number; y: number; op?: number; size?: number }> = ({ x, y, op = 1, size = 11 }) => (
  <g transform={`translate(${x} ${y})`} opacity={op} stroke={GRAY} strokeWidth="5" strokeLinecap="round">
    <line x1={-size} y1={-size} x2={size} y2={size} />
    <line x1={size} y1={-size} x2={-size} y2={size} />
  </g>
);

export const Check: React.FC<{ x: number; y: number; op?: number; size?: number }> = ({ x, y, op = 1, size = 12 }) => (
  <g transform={`translate(${x} ${y})`} opacity={op} stroke={INK} strokeWidth="5"
     strokeLinecap="round" strokeLinejoin="round" fill="none">
    <path d={`M${-size} 0 L${-size * 0.2} ${size * 0.75} L${size} ${-size * 0.8}`} />
  </g>
);

/** 파일 조각 — 이 영상의 기본 단위 */
export const FileChip: React.FC<{
  x: number; y: number; w?: number; h?: number;
  name: string; presence: Presence; op?: number; emphasis?: boolean;
}> = ({ x, y, w = 340, h = 66, name, presence, op = 1, emphasis }) => (
  <g opacity={op}>
    <Box x={x} y={y} w={w} h={h} presence={presence} r={9} fill={BG} emphasis={emphasis} />
    <T x={x + 24} y={y + h / 2} size={26} weight={600} mono
       muted={presence === 'absent'}>{name}</T>
  </g>
);

/** 자막 — 장면당 한 줄, 화면 아래 고정 */
export const Caption: React.FC<{ text: string; size?: number }> = ({ text, size = 56 }) => (
  <div style={{
    position: 'absolute', left: 0, right: 0, bottom: 0, height: 180,
    borderTop: `4px solid ${INK}`, background: BG,
    display: 'flex', alignItems: 'center', justifyContent: 'center',
    padding: '0 90px', boxSizing: 'border-box',
  }}>
    <div style={{
      fontFamily: FONT, fontWeight: 700, fontSize: size, color: INK,
      lineHeight: 1.25, textAlign: 'center', letterSpacing: '-1px',
    }}>{text}</div>
  </div>
);

/** 실측 화면을 감싸는 액자 — 그래픽과 녹화를 한 문법으로 묶는다 */
export const Frame: React.FC<{
  x: number; y: number; w: number; h: number; label: string; op?: number;
  children?: React.ReactNode;
}> = ({ x, y, w, h, label, op = 1, children }) => (
  <g opacity={op}>
    <rect x={x} y={y} width={w} height={h} rx={12} fill="#fff"
      stroke={INK} strokeWidth={6} strokeLinejoin="round" />
    <T x={x} y={y - 26} size={25} weight={700} muted>{label}</T>
    {children}
  </g>
);
