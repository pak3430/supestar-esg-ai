---
name: TRANSACTION_EVIDENCE_PACK
description: "거래 증빙팩의 산림 ESG 문맥상 의미와 경계를 정의한다."
derivedFromStage1: "[Stage 1 candidate](../_artifact/20260821_164823_stage1_source_linked_identity_extraction_artifact.md#identitycandidate)"
derivedFromStage2: "[Stage 2 candidate](../_artifact/stage2_identity_fragmentation_artifact.md#fragmentationrecords)"
derivedFromStage3: "[Stage 3 sequence](../_artifact/stage3_knowledge_chain_ordering_artifact.md#orderedcandidaterecords)"
fragmentedFrom: none
collapsedFrom: none
sequencePreviousIdentity: "[USE_COMPLETION](../_artifact/stage3_knowledge_chain_ordering_artifact.md#orderedcandidaterecords)"
sequenceNextIdentity: "[APPROVED_EXTERNAL_CLAIM](../_artifact/stage3_knowledge_chain_ordering_artifact.md#orderedcandidaterecords)"
groundingVersion: "v3"
groundingApproval: "[APPROVED_WITH_SCOPE_LIMITS](../../../ccs_authoring_runs/2026-08-21_transaction_evidence_grounding_v1/GROUNDING_APPROVAL_RECORD.md)"
---

# 거래 증빙팩

## Meaning

거래 증빙팩은 산림탄소 거래의 주체·대상·권리·계약·세무검토·결제·정산·등록부 상태변경·사용상태·외부 주장에 관한 증거를 하나의 실행 이력으로 재현하기 위해 묶은 증거 집합이다. 결제 영수증 하나나 인증서 하나가 전체 증빙팩을 대신하지 않는다.

## Boundary

- IS: 거래 주체·대상·권리·인증·계약·대금·세무검토·등록부 상태·주장 승인 증거와 각 증거의 존재·누락·미확정 상태를 묶는 내부 준비도 판단 단위.
- IS NOT: 법령상 필수서류 목록, 법률·세무·계약상 효력의 자동 확정, 결제 성공의 거래 완결 간주, 등록부 이전 또는 실제 거래 실행.
- Evidence boundary: 없는 문서·권리·공식 회신은 추정으로 채우지 않으며 `PROCEED`도 법적 유효성이나 세무 적정성을 뜻하지 않는다.
- Entity boundary: 실제 프로젝트·기관·사용자·거래 인스턴스와 원문 증거 파일은 별도 실행·기록 계층에 둔다.

## Source grounding

- source: [05_산림탄소_거래_권리_계약_세무_결제_공백구조.md](../../../ccs/_input/_document/05_%EC%82%B0%EB%A6%BC%ED%83%84%EC%86%8C_%EA%B1%B0%EB%9E%98_%EA%B6%8C%EB%A6%AC_%EA%B3%84%EC%95%BD_%EC%84%B8%EB%AC%B4_%EA%B2%B0%EC%A0%9C_%EA%B3%B5%EB%B0%B1%EA%B5%AC%EC%A1%B0.md)
- sourceLineRanges: L18-L20; L23-L44; L46-L80
- sourceSha256: 8946b8b3927ff797f766bc1eb9f6531089342cff8f84ae757fdd07f7ce100c74
- grounds: 11개 내부 준비도 게이트, 거래 워크플로우, 증빙팩 묶음, 공식 질의 대상, `PROCEED`·`REVIEW`·`STOP` 경계

## Official corroboration boundary

- [한국임업진흥원 산림탄소상쇄제도 운영](https://www.kofpi.or.kr/intro/bizGuide_04_02.do): 사업등록·모니터링·검증·인증·거래의 단계성과 산림탄소등록부 역할을 확인한다.
- [산림탄소등록부](https://carbonregistry.forest.go.kr/): 사업·인증·거래 상태가 등록부 관리 대상임을 확인한다.
- [탄소흡수원 유지 및 증진에 관한 법률](https://www.law.go.kr/): 인증된 흡수량, 등록부, 거래·사용의 법적 기반을 확인한다.
- officialLimit: 공식 자료는 인증·등록부·거래계정·거래 절차의 필요성을 corroborate할 뿐, 내부 G1~G11 전체를 법정 요건으로 만들거나 세무·계약 결론을 대신하지 않는다.

## Skill Derivation

`TRANSACTION_EVIDENCE_PACK` definesGoal -> [거래 증빙팩 Goal](../_goal/transaction_evidence_pack_goal.md).
`TRANSACTION_EVIDENCE_PACK` definesGoal -> [산림탄소 거래 준비도 Goal](../_goal/forest_carbon_transaction_readiness_goal.md).

## Provenance

- [Stage 1 candidate](../_artifact/20260821_164823_stage1_source_linked_identity_extraction_artifact.md#identitycandidate)
- [Stage 2 candidate](../_artifact/stage2_identity_fragmentation_artifact.md#fragmentationrecords)
- [Stage 3 sequence](../_artifact/stage3_knowledge_chain_ordering_artifact.md#orderedcandidaterecords)
- [Grounding approval record](../../../ccs_authoring_runs/2026-08-21_transaction_evidence_grounding_v1/GROUNDING_APPROVAL_RECORD.md)
