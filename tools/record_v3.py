from pathlib import Path
import json,hashlib
r=Path(__file__).resolve().parents[1]
entry='''

## V3.0 인수 및 안정화 — 2026-11-27 KST / TASK 00–05 검증 기록

- 사용자 V3.0 지시서를 docs/V3_INSTRUCTIONS.md에 보존. 기술 기반 TASK 00–07은 중간 승인 없이 진행하며 기존 AGENTS의 단계 승인 제한을 이 범위에서 대체. 정식 게임 시스템은 추가하지 않음.
- TASK 00: 원본 73파일 ZIP 백업 확보. SHA-256 07665612074af40bb376189f7b70fff750d76db77a080dbcd68aa56ed6144eef. 원격 저장소를 별도 NewSamgukji_remote_V3에 clone, 기준 커밋 767c23712b6e30087896f8e24fa2ba3cd8162d29 / 38개 파일. 로컬은 더 발전한 기술 소스이며 원격의 실제 DEM 3종과 metadata를 그대로 복사. 기존 파일 삭제 없음. 기존 테스트 28/28 실제 재실행 통과. 상세 변경 목록은 verification/handoff-audit.json.
- TASK 01: Node v24.19.0 / npm 11.17.0. 기존 Three 0.170.0, Vite 5.4.21 유지. npm 설치 및 package-lock.json 확보. 기존 브라우저 스크립트 버전 Playwright 1.51.1을 devDependency로 고정. 샌드박스의 상위 디렉터리 접근 제한으로 esbuild 첫 실행 실패, 동일 소스를 승인된 실행 환경에서 빌드 성공. dist 경로 검사 통과. 로그 verification/build.log, dist.log. 소스 기능 제거로 빌드를 우회하지 않음. 번들 500KB 경고는 잔존.
- TASK 02: Chromium 134에서 첫 SwiftShader 검증 8/8 통과. 실제 GPU(ANGLE Intel HD Graphics 630 / D3D11) 검증 8/8 통과, console errors=[] / network=[]. 실제 DEM, GLB 8종, 측정, 카메라, 해상도/배율, 레이어, LOD/네트워크 타일, 자원 반복, 관절 애니메이션 회전 변화, 모바일 레이아웃 및 CDP touch 이동 확인. GTX 1050 렌더링 검증으로 기록하지 않음. 실제 모바일 하드웨어 검증 아님. verification/stability.json 및 PNG 보존.
- TASK 03: 원본 Copernicus COG 9개 확보, 기존 DEM 덮어쓰기 없이 비교. 513² 고도 min45.29655/max2064.92358/mean236.87292m. 원본 최근접 대비 MAE5.318/RMSE11.186m(다운샘플 vs 최근접 차이, 지표면 실측 정확도 아님). 방향 뒤집기 비교와 5개 대표 마커 비교 기록. Natural Earth 현대 수계3개(황하 포함)/도로203개. ESA WorldCover 2021 원본2개 확보, 실제 시험영역170,000셀(500×340,0.005도 최근접 축소). 습지 셀 미검출. 출처·라이선스·해시 docs/V3_DATA_PROVENANCE.md와 verification/data-audit.json. 현대 데이터이며 삼국시대 지리 아님.
- TASK 04: 16 Chunk/3단계 LOD/15% 히스테리시스/인덱스 재사용 유지. 개별 f32 타일48개와 tiles.json 생성. 카메라 우선순위, 동시요청3, 최대16개 디테일 캐시, 중복 방지, 원거리 캐시해제, AbortController 취소, 실패 후 저해상도 대체, 재진입 재시도. 전체 지역 저해상도 대체면 유지. 타일 표본48/48 원본과 완전일치 및 해시 검사. 공유경계와 고도 원본 불변성 확인. 근거리 LOD를 Chunk 중심 대신 경계까지의 거리로 수정. 전체 CPU 고도/법선 격자와 3해상도 쿼리 캐시는 유지하므로 전체 CPU DEM을 타일 단위로 해제하는 시스템은 아님. 초기 격자·메시 생성은 동기식이며 대규모 세계 스트리밍 완성 아님.
- TASK 05: 자체 GLB8개 보존, 관절 병사 idle/walk/run 회전값 변화 확인 및 캡처. 원본 GLB 캐시8개 고정, 인스턴스100/500/1000/5000 선택 유지. onBeforeRender로 실제 렌더링된 모델/인스턴스를 계수. Mixer stopAllAction/uncacheRoot 유지. 품질3종과 가상/실제 모드를4회 반복한 동일 조건에서 geometry48/texture2 유지(Three renderer 자원 수, GPU바이트 아님). 실제 실행 스크린샷으로 모델 크기 및 관절 동작 확인. 스키닝/실사 캐릭터 미제작.
- 발견/수정: Windows CP949 GeoJSON 디코딩 오류→UTF-8 명시. 해상도별 리샘플링 차이(공유점 최대248.778m)→실제 고도조회 기준513² 분리. 표시 지형은 선택 해상도 유지. 토지피복 취득 후 비용 오버레이 미갱신→분류 재계산. 레이어 오프셋 .15/.3 world units로 병사 가림→미터 단위 p.scale 적용. 모바일 패널 과대→기본 접힘/스크롤. favicon404→inline icon. 선별206 Draw Calls→레이어별 LineSegments2회. 카메라 급이동시 배경 공백→상주 저해상도 대체면.
- 자동 테스트31/31(기존28보존+네트워크타일3) 통과. 데이터감사 DEM3종/파생타일48개/실제토지피복/수계도로 통과. 실제 Production Build 및 dist 검사 통과. screenshots: henan-map, mountains-lod, measurement, movement-cost, animation-0/1/2, mobile-final. 최신 production 재검증과60초×24조건 벤치마크는 TASK06/07 기록에서 별도 확정.
- 자체 결정: 513² 쿼리 기준, 최대800개 절차적 숲 기호,3개 동시요청/16개 디테일 캐시, 전체 지역 저해상도 대체면, dev.3 유지. 원본73개 삭제/이동 없음. 임시 개발 보조 스크립트는 제출 소스에서 제외하고 verification에 보관 예정.
- 남은 검증: Production 재실행, 24조건60초 성능, 실패/취소 네트워크 브라우저 검증, GitHub Actions 실행, 정상 버전을 보호한 배포 판단. GTX1050 실제 선택·실기 모바일·GPU바이트 메모리·장시간 soak는 미검증. 정식 v0.5.0 및 PRE05 최종완료를 아직 선언하지 않음.
'''
p=r/'docs/DEVELOPMENT_REPORT.md';s=p.read_text(encoding='utf-8');
if '## V3.0 인수 및 안정화' not in s:p.write_text(s+entry,encoding='utf-8')
p=r/'docs/CHANGELOG.md';s=p.read_text(encoding='utf-8');
if '## v0.5.0-dev.3 — V3' not in s:p.write_text(s+'\n\n## v0.5.0-dev.3 — V3 실제 실행 및 안정화\n기존 DEM 복구, 의존성/lockfile 및 실제 빌드 성공, 실제 현대 수계·도로·WorldCover 취득, 네트워크 디테일 타일48개/우선순위·취소·캐시·대체면, 고도조회 기준 분리, 토지피복 표시와 비용 갱신, 숲 기호, 근거리LOD·표면 오프셋·모바일 패널·선 레이어 병합 수정. 자동31개 및 GPU 통합8개 검증. 최종 성능/CI/배포 상태는 docs/V3_FINAL_REPORT.md 참조.\n',encoding='utf-8')
p=r/'docs/STREAMING_LANDCOVER.md';s=p.read_text(encoding='utf-8');s+='\n\n## V3.0 superseding checkpoint\n실제 네트워크 detail tiles와 토지피복을 확보했다. 개별16타일×3해상도, bounded async loader(동시3/캐시16), stale 요청취소, 원거리캐시해제, 저해상도 배경 및 실패대체. CPU query용 격자는 별도 상주한다. 실제 ESA 2021 500×340 축소표본을 표면색/비용/최대800개 절차적 숲기호에 연결했다. 상세 출처와 제한은 V3_DATA_PROVENANCE.md. 위 미확보/미구현 기록은 이전 checkpoint 이력으로 보존한다.\n';p.write_text(s,encoding='utf-8')
