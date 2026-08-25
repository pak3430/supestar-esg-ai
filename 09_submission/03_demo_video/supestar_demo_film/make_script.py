#!/usr/bin/env python3
"""
scenes.ts 하나에서 클로바더빙 대본을 생성한다.
장면 길이·자막·내레이션이 전부 같은 파일에서 나오므로 영상과 어긋날 수 없다.
"""
import re, pathlib, sys

SRC = pathlib.Path(__file__).parent / 'src' / 'scenes.ts'
OUT = pathlib.Path(__file__).parent.parent / 'NARRATION_CLOVA_REMOTION.md'
FPS_CHARS = 5.3      # 클로바더빙 기본 속도(초당 글자)
PAD = 1.2            # 앞뒤 여백(초)

src = SRC.read_text(encoding='utf-8')
body = src[src.index('export const SCENES'):]

scenes = []
for m in re.finditer(r"\{\s*id:\s*'([^']+)',\s*durationSec:\s*(\d+),(.*?)\n\s*\},", body, re.S):
    sid, dur, rest = m.group(1), int(m.group(2)), m.group(3)
    sub = re.search(r"subtitle:\s*'((?:[^'\\]|\\.)*)'", rest)
    nar = re.search(r"narration:\s*\n?\s*'((?:[^'\\]|\\.)*)'", rest)
    clip = re.search(r"clip:\s*'([^']+)'", rest)
    scenes.append({
        'id': sid, 'dur': dur,
        'sub': (sub.group(1) if sub else '').replace("\\'", "'"),
        'nar': (nar.group(1) if nar else '').replace("\\'", "'"),
        'clip': clip.group(1) if clip else None,
    })

if not scenes:
    print('★ 장면을 읽지 못했다. scenes.ts 형식을 확인할 것.'); sys.exit(1)

def ts(x): return '%d:%04.1f' % (int(x // 60), x % 60)

# ── 검증 ──
t = 0.0
rows, over = [], []
for s in scenes:
    rec = int(max(0, s['dur'] - PAD) * FPS_CHARS)
    n = len(s['nar'])
    rows.append((s, t, rec, n))
    if n > rec: over.append((s['id'], n, rec))
    t += s['dur']

print('%-20s %-16s %6s %6s %6s  %s' % ('장면', '타임코드', '길이', '권장', '실제', '상태'))
print('-' * 74)
for s, start, rec, n in rows:
    print('%-20s %-16s %5ds %6d %6d  %s' % (
        s['id'], ts(start) + '–' + ts(start + s['dur']), s['dur'], rec, n,
        'OK' if n <= rec else '★초과 %d자' % (n - rec)))
print('-' * 74)
print('총 %s / %d장면' % (ts(t), len(scenes)))
if over:
    print('\n★ 길이 초과 장면 %d개 — scenes.ts 의 narration 을 줄일 것' % len(over))

# ── 대본 생성 ──
L = []
w = L.append
w('# 클로바더빙 내레이션 대본 — Remotion 판\n')
w('- 대상 영상: `supestar_demo_film/out/supestar_esg_user_first_silent.mp4` (%s, 무음)' % ts(t))
w('- 이 파일은 `supestar_demo_film/src/scenes.ts` 에서 **자동 생성**된다.')
w('  장면 길이·자막·내레이션이 같은 파일에서 나오므로 영상과 어긋날 수 없다.')
w('- 문구를 고치려면 `scenes.ts` 의 `narration` 을 고치고 아래를 다시 실행한다.\n')
w('```bash')
w('python3 make_script.py      # 프로젝트 폴더에서 실행')
w('```\n')
w('---\n')
w('## 사용법\n')
w('1. 클로바더빙에 영상을 올린다.')
w('2. 아래 타임코드 위치에 더빙을 추가한다.')
w('3. 해당 장면의 코드블록을 복사해 붙여넣는다.\n')
w('> 장면 시작보다 **0.5초쯤 뒤에** 음성을 두면 화면 전환과 겹치지 않는다.\n')
w('---\n')
w('## 타임코드 요약\n')
w('| # | 장면 | 시작 | 끝 | 길이 | 글자 | 화면 |')
w('|---:|---|---|---|---:|---:|---|')
for i, (s, start, rec, n) in enumerate(rows, 1):
    kind = '실측 녹화' if s['clip'] else '그래픽'
    w('| %d | %s | %s | %s | %ds | %d | %s |' % (
        i, s['id'], ts(start), ts(start + s['dur']), s['dur'], n, kind))
w('')
w('---\n')
w('# 장면별 대본\n')
for i, (s, start, rec, n) in enumerate(rows, 1):
    kind = '실측 녹화' if s['clip'] else '그래픽'
    w('## %02d. %s — %s' % (i, ts(start), s['id']))
    w('')
    w('- 자막: **%s**' % s['sub'])
    w('- 화면: %s%s' % (kind, ('  (`%s`)' % s['clip']) if s['clip'] else ''))
    w('- 길이 %ds · 권장 %d자 · 실제 %d자 %s' % (
        s['dur'], rec, n, '' if n <= rec else '← **초과**'))
    w('')
    if s['nar']:
        w('```')
        w(s['nar'])
        w('```')
    else:
        w('> 무음')
    w('')
    w('---\n')
w('# 전체 대본 (한 번에 복사용)\n')
w('줄바꿈이 장면 경계다.\n')
w('```')
for s, _, _, _ in rows:
    if s['nar']: w(s['nar'])
w('```\n')
w('---\n')
w('# 발음 표기\n')
w('한국어 TTS 가 영문·기호를 뭉개지 않도록 **독음으로 적어 두었다.**\n')
w('| 원문 | 대본 표기 |')
w('|---|---|')
for a, b in [('KAC', '케이 에이 씨'), ('Skill', '스킬'), ('Run Record', '런 레코드'),
             ('PROCEED', '프로시드'), ('REVIEW', '리뷰'),
             ('Identity / Entity', '아이덴티티 / 엔티티'),
             ('Goal · Task · Knowledge · Method', '골 · 태스크 · 널리지 · 메소드'),
             ('AI', '에이아이'), ('STOP', '스톱')]:
    w('| `%s` | %s |' % (a, b))
w('')
w('---\n')
w('# 표현 주의\n')
w('**쓰지 말 것**\n')
w('- ❌ 실제 거래·결제·등록부 변경이 구현됐다는 표현')
w('- ❌ 한국임업진흥원 공식 운영 서비스라는 표현')
w('- ❌ 목표 KPI를 달성 실적으로 표현하는 문장\n')
w('**살려야 할 것**\n')
w('- 수페스타는 질문을 실행 단위로 구조화하고, 근거가 충분할 때만 `PROCEED`한다.')
w('- 고위험·증거 부족 상황에서는 `REVIEW` 또는 `STOP`하고 누락 근거와 다음 확인 절차를 남긴다.')
w('- 현재 산출물은 해커톤 MVP이며, 기관 연계·실거래·결제·등록부 변경은 수행하지 않는다.')

OUT.write_text('\n'.join(L), encoding='utf-8')
print('\n→ %s' % OUT)
