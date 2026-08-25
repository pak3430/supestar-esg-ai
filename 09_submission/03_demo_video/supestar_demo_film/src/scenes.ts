/** 장면·시간·자막·내레이션의 단일 기준 파일 */
export const FPS = 30;
export const WIDTH = 1920;
export const HEIGHT = 1080;
export const ART_H = 900;

export type Scene = {
  id: string;
  durationSec: number;
  subtitle: string;
  narration: string;
};

export const SCENES: Scene[] = [
  {
    id: 's00_title', durationSec: 12,
    subtitle: 'KAC 지식과 실행 Skill로 ESG 질문을 검증 가능한 다음 행동으로 바꿉니다',
    narration: '수페스타는 지식행동사슬과 실행 스킬로 ESG 질문을 검증 가능한 행동으로 바꾸는 로컬 챗봇입니다.',
  },
  {
    id: 's01_problem', durationSec: 15,
    subtitle: '문제는 정보 부족이 아니라, 지식과 행동의 단절입니다',
    narration: 'ESG 정보는 많지만 필요한 기준과 확인 순서, 다음 행동을 찾기 어렵습니다. 정의만 알아서는 실제 판단으로 이어지지 않습니다.',
  },
  {
    id: 's02_kac', durationSec: 17,
    subtitle: '구조화하고, Skill로 묶고, 배포해야 실행을 반복 검증할 수 있습니다',
    narration: '지식행동사슬은 아이덴티티에서 목표, 태스크, 지식, 방법, 스킬까지 연결합니다. 구조화는 기준을 지키고, 묶음과 배포는 행동을 반복하게 합니다.',
  },
  {
    id: 's03_architecture', durationSec: 18,
    subtitle: '판정은 Skill이 만들고, 로컬 AI는 검증 결과만 설명합니다',
    narration: '질문에서 사용자가 말한 사실만 컨텍스트로 만들고, 지식행동사슬과 스킬을 실행합니다. 판정은 프로시드, 리뷰, 스톱으로 남고, 로컬 에이아이는 결과만 설명합니다.',
  },
  {
    id: 's04_product', durationSec: 17,
    subtitle: '최종 MVP는 브라우저형 ESG 대화 서비스입니다',
    narration: '사용자에게는 브라우저형 대화 서비스로 보입니다. 앞단에는 자연스러운 답변이, 뒷단에는 컨텍스트, 케이 에이 씨, 스킬, 근거와 실행 기록이 남습니다.',
  },
  {
    id: 's05_esg', durationSec: 18,
    subtitle: '“ESG가 무엇인가요?”에는 ESG만 답합니다',
    narration: 'ESG가 무엇인지 물으면 환경, 사회, 지배구조의 의미만 답합니다. 구매 의도가 없으므로 산림탄소마켓 링크는 나오지 않고, 관련 지식만 선택됩니다.',
  },
  {
    id: 's06_scope', durationSec: 22,
    subtitle: '자연스러운 질문을 구조화해 Scope 1을 실행 판정합니다',
    narration: '회사 소유 운영 보일러와 도시가스 사용량, 기간, 고지서를 말하면 활동과 소유 관계, 수량과 증거를 구조화합니다. 스코프 분류 스킬이 실행되어 프로시드와 스코프 원 후보를 만듭니다.',
  },
  {
    id: 's07_evidence', durationSec: 20,
    subtitle: '답변 뒤에서 실제 실행된 KAC와 Skill을 확인할 수 있습니다',
    narration: '답변 근거를 펼치면 승격된 사용자 입력, 선택된 아이덴티티 체인과 스킬 파일, 해시를 볼 수 있습니다. 정적 예시가 아니라 실제 질문 실행에서 생성된 기록입니다.',
  },
  {
    id: 's08_review', durationSec: 19,
    subtitle: '모호하거나 충돌하면 REVIEW하고, 고위험 요청은 STOP합니다',
    narration: '보일러 연소와 구매전력을 한 질문에 섞으면 하나로 확정하지 않습니다. 리뷰로 멈추고 활동을 나눠 확인하도록 묻습니다. 고위험 요청은 스톱하며 자유 생성을 차단합니다.',
  },
  {
    id: 's09_market', durationSec: 17,
    subtitle: '명시적 구매 질문에서만 산림탄소마켓을 선택지로 보여줍니다',
    narration: '탄소크레딧 구매처를 직접 물은 경우에만 산림탄소마켓을 보여줍니다. 구매와 결제를 대신하지 않으며 최신 조건은 마켓에서 확인하게 합니다.',
  },
  {
    id: 's10_validation', durationSec: 17,
    subtitle: '35 tests · 63 scenarios · 10 local-AI cases · 9 routes',
    narration: '최신 검증은 자동 테스트 서른다섯 건, 결정론 예순세 건, 로컬 에이아이 열 건을 통과했습니다. 아홉 라우트와 프로시드, 리뷰, 스톱도 확인했습니다.',
  },
  {
    id: 's11_close', durationSec: 14,
    subtitle: '검증된 지식과 Skill이 실제로 실행되고 기록되는 ESG AI',
    narration: '수페스타는 설명하는 에이아이를 넘어, 검증된 지식과 스킬이 실제로 실행되고 기록되는 ESG 에이아이를 보여줍니다.',
  },
];

export const frames = (sec: number) => Math.round(sec * FPS);
export const startFrameOf = (i: number) => frames(SCENES.slice(0, i).reduce((a, s) => a + s.durationSec, 0));
export const totalFrames = () => frames(SCENES.reduce((a, s) => a + s.durationSec, 0));
export const totalSec = () => SCENES.reduce((a, s) => a + s.durationSec, 0);
