# 변경 이력

## 0.1.0
- PRE-STEP 01 최초 소스 구현. 지형 테스트 통과. 실제 렌더링 미검증.

## v0.1.1-preview
- 설치 없는 CDN HTML 미리보기 추가.

## v0.1.2 — PRE-STEP 01-B
- GitHub Pages workflow, 상대 경로 빌드, 모듈 로딩 오류 대응, 배포 문서 추가. 실제 배포 미실시.

## v0.2.0-alpha.1
DEM 연동 준비 (실제 데이터 미확보).

## v0.2.0-alpha.2
- Visual terrain, mobile input, marker readability, DEM cache and audit workflow; partial verification only.

## v0.2.0-alpha.3 후보 (부분 구현)
- 역투영 및 거리 측정 UI 추가. 자동 테스트 11/11. 빌드 및 실제 실행 미검증.

## v0.2.0-alpha.5 (partial candidate)
- Regional scale, projection audit, touch measurement guard, optional modern line layers, provisional movement cost overlay and standalone frame statistics. Browser/build/data verification pending.

## v0.5.0-dev.1
Partial integration candidate; see DEVELOPMENT_REPORT.md for unverified and missing features.

## v0.5.0-dev.2
- Chunk index LOD, quality presets, seven primitive GLBs, model cache and geographic acquisition workflow. Build and deployment pending.

## Unreleased — V2.1 verification checkpoint
- Candidate verification workflow, initial browser checks, prerelease deployment guard, procedural animation demo.

### V2.1 checkpoint continuation (dev.2)
- Bounded DEM request cache and tile sample tests; preliminary browser interaction and opt-in benchmark scripts.
- 26 unit tests passed; production build and browser verification remain blocked.

- V2.1 checkpoint: local mesh residency, land-cover schema and clicked cost lookup, rigid limb test soldier; 28 unit tests. Build blocked; version unchanged.


## v0.5.0-dev.3 — V3 실제 실행 및 안정화
기존 DEM 복구, 의존성/lockfile 및 실제 빌드 성공, 실제 현대 수계·도로·WorldCover 취득, 네트워크 디테일 타일48개/우선순위·취소·캐시·대체면, 고도조회 기준 분리, 토지피복 표시와 비용 갱신, 숲 기호, 근거리LOD·표면 오프셋·모바일 패널·선 레이어 병합 수정. 자동31개 및 GPU 통합8개 검증. 최종 성능/CI/배포 상태는 docs/V3_FINAL_REPORT.md 참조.
