---
name: transaction_evidence_pack_knowledge
description: "거래 증빙팩 판단에 필요한 정의·관계·증거·금지 경계를 정리한다."
---

# 거래 증빙팩 Knowledge

- Definition: 거래 증빙팩은(는) 원문이 독립 구조 단위로 사용하는 개념이다.
- Evidence: 05_산림탄소_거래_권리_계약_세무_결제_공백구조.md L46-L46; SHA-256 8946b8b3927ff797f766bc1eb9f6531089342cff8f84ae757fdd07f7ce100c74.
- Decision rule: 필수 근거와 경계가 모두 있으면 PROCEED, 공식 확인이 필요하면 REVIEW, 핵심 증거가 없거나 금지행위에 닿으면 STOP.
- Prohibition: 실제 거래, 자동결제, 가격·수익 추천, 법률·세무 자문, 인증 자동판정을 수행하지 않는다.

## Chain position

- ← requiresKnowledge — [거래 증빙팩 Task](../_task/transaction_evidence_pack_task.md)
- → appliedThrough — [거래 증빙팩 Method](../_method/transaction_evidence_pack_method.md)
