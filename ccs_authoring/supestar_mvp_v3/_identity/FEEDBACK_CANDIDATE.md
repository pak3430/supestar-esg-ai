---
name: FEEDBACK_CANDIDATE
description: "FeedbackCandidate의 산림 ESG 문맥상 의미와 경계를 정의한다."
derivedFromStage1: "[Stage 1 candidate](../_artifact/20260821_164823_stage1_source_linked_identity_extraction_artifact.md#identitycandidate)"
derivedFromStage2: "[Stage 2 candidate](../_artifact/stage2_identity_fragmentation_artifact.md#fragmentationrecords)"
derivedFromStage3: "[Stage 3 sequence](../_artifact/stage3_knowledge_chain_ordering_artifact.md#orderedcandidaterecords)"
fragmentedFrom: none
collapsedFrom: none
sequencePreviousIdentity: "[RUN_RECORD](../_artifact/stage3_knowledge_chain_ordering_artifact.md#orderedcandidaterecords)"
sequenceNextIdentity: "[COMMON_CONTEXT](../_artifact/stage3_knowledge_chain_ordering_artifact.md#orderedcandidaterecords)"
---

# FeedbackCandidate

## Meaning

FeedbackCandidate은(는) 산림 ESG 생태계에서 독립적으로 설명·판단되어야 하는 개념이다. 원문은 다음과 같이 이 구조적 역할을 뒷받침한다: “수페스타의 최소 객체 후보는 UserQuestion, UserRole, IdentityNode, RelationEdge, EvidenceClaim, ActionPath, RiskGate, ApprovalDecision, RunRecord, FeedbackCandidate이다. 최종 클래스·모듈 경계는 Build 설계에서 확정하며 이 문서에서 구현을 미리 고정하지 않는다.”

## Boundary

- IS: FeedbackCandidate 자체의 정의, 역할, 근거, 상태를 다루는 개념.
- IS NOT: 인접 시장·기관·절차·판정 개념을 대신하는 포괄 묶음.
- Entity boundary: 실제 프로젝트·기관·사용자·거래 인스턴스는 별도 실행·기록 계층에 둔다.

## Source grounding

- source: [08_ESG_AX_Concept_Build_Run_구조요구사항.md](../../../ccs/_input/_document/08_ESG_AX_Concept_Build_Run_%EA%B5%AC%EC%A1%B0%EC%9A%94%EA%B5%AC%EC%82%AC%ED%95%AD.md)
- sourceLineRanges: L78-L78
- sourceSha256: cb6b20d918a96ca8757cfc97ccf49bc7c69ee9843234a98c1af4b2026196376c

## Skill Derivation

`FEEDBACK_CANDIDATE` definesGoal -> [FeedbackCandidate Goal](../_goal/feedback_candidate_goal.md).

## Provenance

- [Stage 1 candidate](../_artifact/20260821_164823_stage1_source_linked_identity_extraction_artifact.md#identitycandidate)
- [Stage 2 candidate](../_artifact/stage2_identity_fragmentation_artifact.md#fragmentationrecords)
- [Stage 3 sequence](../_artifact/stage3_knowledge_chain_ordering_artifact.md#orderedcandidaterecords)
