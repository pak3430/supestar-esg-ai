# 산림 ESG 전사본 직접 요구 워크플로우

## 주 실행 화면

- [단계형 전체생태계 워크플로우](forest-esg-transcript-workflow.html)
- [첫 화면 검수 이미지](forest-esg-transcript-workflow-preview.png)
- [거래·증빙 단계 검수 이미지](forest-esg-transcript-workflow-stage7-preview.png)
- 생성 스크립트: `build_forest_esg_story_workflow.js`

첫 화면은 최근 전사본이 요구한 다음 7단계만 보여준다.

1. ESG와 경영
2. 측정과 Scope
3. SDGs 점검
4. CCM·VCM
5. 산림 ESG
6. 공식 절차
7. 거래·증빙

사용자가 단계를 선택하면 그 단계의 핵심 Identity, 다음 단계가 필요한 이유, 확인 증거와 미확정 공백만 펼친다. 거래·증빙 단계에서는 판매자·구매자·거래대상·처분권·계약·세무·결제·정산을 `PASS`, `REVIEW`, `STOP` 상태로 구분한다.

KAC는 화면 하단의 ‘마지막 실행 수단’으로만 배치한다. 산림 ESG 주제를 설명한 후에 선택된 Identity와 Skill, 실행·산출·검토 기록을 보여준다.

## 기술 보조 화면

- [147개 Identity 상세 관계도](forest-esg-identity-relation-map.html)
- [상세 관계도 검수 이미지](forest-esg-identity-relation-map-preview.png)
- 생성 스크립트: `build_forest_esg_relation_map.js`
- 원천 데이터: `../../04_ccs/source/forest_esg_identity_catalog_v1.0.json`

상세 관계도는 147개 Identity와 Relation을 검색·필터링하는 구현 검토용 화면이다. 발표 첫 화면이나 최근 전사본의 직접 답변으로 사용하지 않는다.

## 검수 기준

- 처음 본 사람이 30초 안에 7단계 인과축을 읽을 수 있어야 한다.
- 2분 안에 산림탄소의 E·S·G 또는 거래 공백 중 하나를 설명할 수 있어야 한다.
- 근거가 부족한 권리·계약·세무·결제는 확정 답변이 아니라 `REVIEW` 또는 `STOP`으로 보여야 한다.
- 화면이 브라우저 제품 자체를 주제로 삼지 않고, 산림 ESG 지식과 관계를 보여주는 증거 표면이어야 한다.
