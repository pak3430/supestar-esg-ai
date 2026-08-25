---
name: forest-carbon-procedure-guidance
description: "Guide the next official forest-carbon project procedure from the project's claimed current stage and available evidence, including responsible actors, prerequisites, required artifacts, official confirmation questions, and a PROCEED/REVIEW/STOP record. Use for procedure sequencing; not for concept assessment or E/S/G impact-responsibility mapping."
---

# Forest Carbon Procedure Guidance

Guide a forest-carbon project from its evidenced current position to the next official procedural step. Keep the user's claimed stage separate from stages proven complete by supplied evidence, and never infer that a missing prerequisite has been completed.

## Scope

Use this skill to answer: “Given this project's current state, what official step comes next, who is involved, what must already be true, and what artifact is needed?”

This skill does only procedure sequencing and evidence-gap guidance. It does not:

- reassess the meaning or boundary of `FOREST_CARBON_PROJECT`;
- produce an environmental, social, and governance impact/actor/responsibility map;
- submit documents, contact an institution, register a project, verify or certify a result, execute a transaction, or mutate a registry;
- declare an official registration, verification, certification, transaction, use-completion, legal, contractual, or tax result.

Its `PROCEED`, `REVIEW`, and `STOP` values describe the guidance record, not an authority's approval or decision.

## Inputs

Obtain these fields before claiming a current official state.

| field | requirement | handling rule |
| --- | --- | --- |
| `projectType` | required | Preserve the user's known project type; use `UNKNOWN` when unclear and do not infer scheme applicability. |
| `currentStage` | required | Accept only `PLANNING`, `ELIGIBILITY`, `REGISTERED`, `IMPLEMENTING`, `MONITORING`, `VERIFIED`, `CERTIFIED`, `REGISTRY_MANAGED`, `UNKNOWN`. This is a claim, not completion evidence. |
| `availableDocuments` | optional | Record the supplied plan, eligibility, registration, implementation, monitoring, verification, certification, use, and registry materials. An uninspected title is not completion evidence. |
| `intendedUse` | required | Preserve transaction, non-transactional use, learning, or undecided intent. Do not infer tradability or permitted claims from intent. |
| `asOfDate` | required | Use this date for registration, verification, certification, and registry validity. If absent, current validity remains unresolved. |

If `projectType` or `currentStage` is unknown, keep `UNKNOWN`. If `intendedUse` or `asOfDate` is missing, ask for it; if it remains unavailable, record the gap and use `REVIEW` rather than inventing a value.

## Fixed official sequence

Always walk this sequence from the beginning:

`사업계획 → 타당성·적격성 검토 → 사업등록 → 실행 → 모니터링 → 독립 검증 → 인증 → 거래 또는 비거래 활용 → 등록부 상태관리`

Do not create a new input enum for 거래 또는 비거래 활용. Use the official Korean stage name in `blockedStage` or `nextStage` when that stage is relevant.

## Stage knowledge

Use the following as a procedural evidence map, not as a substitute for the current official rules of a particular scheme.

| stage | actors within the supported public-role boundary | prerequisite | required artifact or completion evidence |
| --- | --- | --- | --- |
| 사업계획 | 사업자·산주 | 사업유형·목적, 대상지와 사업 권한, activity/methodology choice | 사업계획서 covering 대상지·권리·활동·방법론·기준선·모니터링·예상성과, plus authority evidence |
| 타당성·적격성 검토 | 사업자, the applicable scheme operator; 한국임업진흥원·산림탄소센터 only within published duties | reviewable plan and scheme-applicability basis | submission/receipt and official eligibility or review result; confirm exact body, form, and criteria officially |
| 사업등록 | 사업자, applicable operator, 산림탄소등록부 | completed eligibility review and registration requirements | project identifier, registration decision or registry record, and status as of `asOfDate` |
| 실행 | 사업자·산주 | evidenced valid registration and registered plan | activity, field, authority, and change records |
| 모니터링 | 사업자·산주 | implementation records and confirmed methodology/boundary/period/baseline | activity/field/calculation data and monitoring report |
| 독립 검증 | 독립 검증기관, 사업자 | verifiable monitoring/calculation package and officially confirmed verifier eligibility | verification report, correction/closure records, and status as of `asOfDate` |
| 인증 | applicable scheme operator and applicant | independent verification result and scheme requirements | official certification decision/document or registry certification status; confirm scope and validity officially |
| 거래 또는 비거래 활용 | 권리 보유자·사업자, counterparty and registry operator where applicable | valid certification/registry status, use route, rights, and permitted expression | transfer record or approved non-transactional-use basis; use-completion status when claimed |
| 등록부 상태관리 | registry operator, 사업자·권리 보유자 | target record and evidence for the status-changing event | holding, transfer, use-completion, invalidation history and current status |

Treat 산림청 as the policy/law/certification-system authority described by the grounding, not as an automatic decider of an individual transaction or tax outcome. Describe 한국임업진흥원·산림탄소센터 only within published system-operation, registration/evaluation/certification-support, and information-management duties. A registry record supports status history; it does not settle every right, contract, or tax meaning.

## Procedure

### 1. Create an evidence ledger

Create all nine stages in order. For each stage record:

- the user's claim, if any;
- `evidenceState`: `CONFIRMED`, `UNVERIFIED`, or `MISSING`;
- the supplied evidence references and the specific facts they support;
- missing facts or validity questions;
- prerequisites, actors, and required artifacts.

Use `CONFIRMED` only when the supplied material identifies the relevant project and supports the stage, responsible or issuing party, date/period, and completion or current status needed for that stage. Use `UNVERIFIED` for a document title or assertion whose content, party, subject, date, or status cannot be checked. Use `MISSING` when no evidence was supplied. Never fill a gap from general knowledge or from a later-stage document.

### 2. Determine completed, blocked, and next stages

Walk from 사업계획 forward.

1. Add only the contiguous `CONFIRMED` prefix to `completedStages`.
2. If a prerequisite stage at or before the claimed current stage is `UNVERIFIED` or `MISSING`, make the earliest such stage `blockedStage`. Keep any later material visible as out-of-sequence evidence, but do not treat it as proof that the gap was passed.
3. Compare the input `currentStage` with the evidenced prefix and record any mismatch.
4. If blocked, make confirmation or completion of that blocked stage the `nextStage`. Otherwise, use the first official stage after the completed prefix.
5. If all nine stages are confirmed, set `nextStage` to `null` and place continued registry-status monitoring in the checklist.

### 3. Attach next-step requirements

For the blocked and next stages, identify:

- `actors`: only supported public roles and the concrete next preparation or confirmation action;
- prerequisites: what must already be evidenced;
- `requiredArtifacts`: the document or record, its purpose, and its evidence state.

When the exact responsible body, current form, submission items, review standard, scheme applicability, or validity cannot be established from supplied evidence, set `confirmationNeeded: true` and convert the gap into an official confirmation question. Do not guess a private institutional judgment.

### 4. Ask only relevant official confirmation questions

For each unresolved item, name the target, the question, and the gap it resolves. Cover the applicable items among:

- official project type and current scheme/methodology applicability;
- documents establishing site, project, management, and disposition authority;
- registration identifier and validity as of `asOfDate`;
- official owner of the next stage, current form, submission fields, and correction/review requirements;
- verifier eligibility and current verification-result status;
- certification scope, status, and validity;
- transaction versus non-transactional route and permitted external wording;
- registry holding, transfer, use-completion, invalidation, and double-use-prevention history.

Do not send these questions or act on the user's behalf.

### 5. Assign one status

Apply this precedence:

1. `STOP` — the request asks to assert tradability, use-completion, or official certification without evidence of prerequisite registration, independent verification, and certification.
2. `REVIEW` — project type/current stage is unknown; sequential evidence or `asOfDate` is insufficient; or scheme applicability, registration/certification validity, use route, permitted wording, or an exact official requirement needs confirmation.
3. `PROCEED` — the claimed current stage matches the contiguous completion evidence and the next actors, prerequisites, and artifacts can be guided without an unresolved official judgment essential to that guidance.

Missing evidence by itself does not authorize an external result claim. `STOP` blocks the unsupported assertion, while the output must still preserve confirmed facts, gaps, and the safe next confirmation step.

## Outputs

Produce all of the following.

### `procedure_path.json`

```json
{
  "currentStage": "<input enum>",
  "completedStages": ["<contiguously evidenced official stage>"],
  "blockedStage": "<earliest unsupported prerequisite stage or null>",
  "nextStage": "<official next stage or null>",
  "actors": [
    {
      "actor": "<actor>",
      "publicRole": "<supported role>",
      "nextAction": "<preparation or confirmation action>",
      "confirmationNeeded": true
    }
  ],
  "requiredArtifacts": [
    {
      "stage": "<stage>",
      "artifact": "<document or record>",
      "purpose": "<prerequisite or state to establish>",
      "evidenceState": "CONFIRMED|UNVERIFIED|MISSING"
    }
  ]
}
```

### `procedure_checklist.md`

List all nine stages in order with the columns `단계 | 증거상태 | 근거 | 선행조건 | 담당주체 | 필요 산출물 | 다음 행동`. Do not check off `UNVERIFIED` or `MISSING` stages.

### `official_confirmation_questions.md`

Use `확인 대상 | 질문 | 해소할 공백`. Omit questions already answered by inspected evidence.

### `status` and `RunRecord`

Return exactly one `status`: `PROCEED`, `REVIEW`, or `STOP`. The `RunRecord` must preserve:

- `asOfDate`, `projectType`, input `currentStage`, `intendedUse`;
- each supplied document's evidence state, supported fact, and gap;
- `completedStages`, `blockedStage`, and `nextStage`;
- `status` and its reason;
- identifiers for the three named output artifacts.

The record must make the current state, evidence, next stage, and verdict reproducible.

## Required behavior checks

- `PROCEED`: registration and all earlier sequential evidence, implementation records, and monitoring material align with the claimed stage, and the user asks how to prepare for independent verification. Guide the verifier role, prerequisites, and verification package; do not claim verification has occurred.
- `REVIEW`: project type and current registration status are unclear. Preserve both unknowns and ask the operator/registry questions needed to establish applicability and current status.
- `STOP`: the user asks to declare a tradable unit without verification and certification evidence. Refuse that declaration and record the missing verification, certification, and registry confirmations as next actions.

## Grounding

- [Forest-carbon procedure authoring contract](../../../../05_identity_pipeline/06_atomic_skills/_authoring_specs/05_forest_carbon_procedure_guidance_authoring_contract.md)
- [Local official-procedure grounding](../../../../ccs/_input/_document/04_%EC%82%B0%EB%A6%BC_ESG_E_S_G_%EB%B0%8F_%EC%9E%84%EC%97%85%EC%A7%84%ED%9D%A5%EC%9B%90_%EC%83%9D%ED%83%9C%EA%B3%84.md#4-%EC%82%B0%EB%A6%BC%ED%83%84%EC%86%8C-%EA%B3%B5%EC%8B%9D-%EC%A0%88%EC%B0%A8)
- [Local official-confirmation questions](../../../../ccs/_input/_document/04_%EC%82%B0%EB%A6%BC_ESG_E_S_G_%EB%B0%8F_%EC%9E%84%EC%97%85%EC%A7%84%ED%9D%A5%EC%9B%90_%EC%83%9D%ED%83%9C%EA%B3%84.md#5-%EC%82%B0%EB%A6%BC%ED%83%84%EC%86%8C%EC%97%90%EC%84%9C-%EB%B0%98%EB%93%9C%EC%8B%9C-%ED%95%A8%EA%BB%98-%EB%AC%BB%EB%8A%94-%EC%A7%88%EB%AC%B8)

## Derivation

← developsSkill — [forest_carbon_procedure_guidance Method](../../_method/forest_carbon_procedure_guidance_method.md)

[FOREST_CARBON_PROJECT](../../_identity/FOREST_CARBON_PROJECT.md) → [forest_carbon_procedure_guidance Goal](../../_goal/forest_carbon_procedure_guidance_goal.md) → [forest_carbon_procedure_guidance Task](../../_task/forest_carbon_procedure_guidance_task.md) → [forest_carbon_procedure_guidance Knowledge](../../_knowledge/forest_carbon_procedure_guidance_knowledge.md) → [forest_carbon_procedure_guidance Method](../../_method/forest_carbon_procedure_guidance_method.md) → `forest-carbon-procedure-guidance`

The Skill is the terminal node and has no outgoing chain edge.

## Execution provenance

- observedOwner: `/root/author_forest_procedure_build_chain_v2/procedure_chain_derivation`
- carriagePath: `/Users/gesia/hackerton_projects/01_ESG_AI_Challenge/ccs_authoring_runs/2026-08-21_build_05_forest_carbon_procedure_guidance_v1/FOREST_CARBON_PROJECT_forest_carbon_procedure_guidance_facet_reservation_carriage.md`
- carriageSha256: `4cf40f597d841cb6da18c925b39208489962ef6e354aa77bacfc042d40992bad`
- carriageOutcome: `binding record emitted`
