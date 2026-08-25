---
name: TAX_CLASSIFICATION
description: "세무분류의 산림 ESG 문맥상 의미와 경계를 정의한다."
derivedFromStage1: "[Stage 1 candidate](../_artifact/20260821_164823_stage1_source_linked_identity_extraction_artifact.md#identitycandidate)"
derivedFromStage2: "[Stage 2 candidate](../_artifact/stage2_identity_fragmentation_artifact.md#fragmentationrecords)"
derivedFromStage3: "[Stage 3 sequence](../_artifact/stage3_knowledge_chain_ordering_artifact.md#orderedcandidaterecords)"
fragmentedFrom: none
collapsedFrom: none
sequencePreviousIdentity: "[TRANSACTION_CONTRACT](../_artifact/stage3_knowledge_chain_ordering_artifact.md#orderedcandidaterecords)"
sequenceNextIdentity: "[PAYMENT](../_artifact/stage3_knowledge_chain_ordering_artifact.md#orderedcandidaterecords)"
---

# 세무분류

## Meaning

세무분류은(는) 산림 ESG 생태계에서 독립적으로 설명·판단되어야 하는 개념이다. 원문은 다음과 같이 이 구조적 역할을 뒷받침한다: “| G8 세무분류 | 소득·재화·용역·무형권리 등 분류 | 과세관청·전문가 검토기록 | REVIEW |”

## Boundary

- IS: 세무분류 자체의 정의, 역할, 근거, 상태를 다루는 개념.
- IS NOT: 인접 시장·기관·절차·판정 개념을 대신하는 포괄 묶음.
- Entity boundary: 실제 프로젝트·기관·사용자·거래 인스턴스는 별도 실행·기록 계층에 둔다.

## Source grounding

- source: [05_산림탄소_거래_권리_계약_세무_결제_공백구조.md](../../../ccs/_input/_document/05_%EC%82%B0%EB%A6%BC%ED%83%84%EC%86%8C_%EA%B1%B0%EB%9E%98_%EA%B6%8C%EB%A6%AC_%EA%B3%84%EC%95%BD_%EC%84%B8%EB%AC%B4_%EA%B2%B0%EC%A0%9C_%EA%B3%B5%EB%B0%B1%EA%B5%AC%EC%A1%B0.md)
- sourceLineRanges: L34-L34
- sourceSha256: 8946b8b3927ff797f766bc1eb9f6531089342cff8f84ae757fdd07f7ce100c74

## Skill Derivation

`TAX_CLASSIFICATION` definesGoal -> [세무분류 Goal](../_goal/tax_classification_goal.md).

## Provenance

- [Stage 1 candidate](../_artifact/20260821_164823_stage1_source_linked_identity_extraction_artifact.md#identitycandidate)
- [Stage 2 candidate](../_artifact/stage2_identity_fragmentation_artifact.md#fragmentationrecords)
- [Stage 3 sequence](../_artifact/stage3_knowledge_chain_ordering_artifact.md#orderedcandidaterecords)
