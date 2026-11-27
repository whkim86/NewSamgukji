# 누적 개발 및 테스트 보고서
## PRE-STEP 01 / v0.1.0
1. 목적: WebGL2 통합 월드 기술 검증.
2. 구현: 원근 카메라, 절차적 평야/산/강, 조명/그림자, OrbitControls, resize, FPS, 오류 표시, 카메라 초기화.
3. 파일: index.html, package.json, src/main.js, src/terrain/{height,world}.js, src/camera/controller.js, src/ui/style.css, public/data/world_config.json, tests/terrain.test.js, START.bat, README.md, AGENTS.md, docs/*.
4. 실행: README 참조. Node.js 및 최초 npm 설치 필요.
5. 실제 화면: 미확보. screenshots 폴더에 사용자 캡처 추가 예정.
6. 테스트: Node 22.16.0, npm 10.9.2. 지형 테스트 3/3 통과 (강 중심 높이, 유한 높이 14641점, 산 높이). JS 구문 검사 통과. 브라우저 실행/빌드/카메라/resize/오류 UI/Windows BAT는 미검증.
7. 성능: 사용자 PC 측정 필요. FPS/Draw calls/삼각형 표시 코드만 구현.
8. 장애: registry.npmjs.org DNS 해석 실패. 의존성 설치 불가. lockfile 및 dist 미생성.
9. 미구현: 실제 지리, 도시, GLB, 군대, 전투, 시간, 내정 등 후속 범위.
10. 편차: TypeScript 대신 JavaScript ES modules (기획서 허용). 마스터 원문 대신 요약 포함. 실행 가능한 빌드 미제공, 소스와 실행 BAT 제공.
11. 임시 결정: 1200×1200 가상 단위, 160분할, 그림자 1024, 픽셀 비율 최대 1.5, 카메라 거리 65~1800. 줌은 화면 중심 기반이며 마우스 위치 중심 줌은 PRE03 예정.
12. 질문: 초기 화면 및 FPS 적절한가? 카메라 조작 방향/속도 선호? 그림자 켜고 끌 때 차이?
13. 다음: 사용자 실행 확인 및 수정 후 승인 시 PRE02. 현재 단계 승인 대기.

## PRE-STEP 01-A / v0.1.1-preview
- 목적: 설치 없는 미리보기 추가. 기존 모듈 소스 변경 없음.
- 추가: preview/index.html (기존 지형, 카메라, 렌더러 코드 인라인화, CDN import map, 설정 내장). 파일 직접 열기 또는 정적 호스팅용. 인터넷 필요.
- 대화창 미리보기는 별도 Canvas 기반 원근 투영 대체 구현이며 Three.js/WebGL 및 실제 그림자 맵과 동일하지 않음. 실제 실행 검증 불가.
- 테스트: 기존 지형 테스트 재실행, 인라인 JS 구문 검사. 브라우저/CDN/사용자 FPS/스크린샷 미검증. 실제 배포 없음.
- 임시 결정: CDN jsDelivr, 기존 Three.js 버전 유지. 대화창 대체 구현은 저해상도 지형 및 면 조명 사용.
- 질문: 대화창 조작 가능 여부, HTML 실행 여부 및 FPS. 다음 단계 승인 전 PRE02 금지.

## PRE-STEP 01-B / v0.1.2
- 목적: 정식 Three.js 단일 엔진의 GitHub Pages 배포 준비. 신규 게임 기능 없음.
- 변경: .github/workflows/pages.yml, vite.config.js, .gitignore, src/bootstrap.js, src/main.js(설정 URL), index.html(진입점/버전), package.json, tests/dist-check.js, README, AGENTS, docs/GITHUB_PAGES.md 및 보고서/변경 이력.
- 기존 지형/카메라/스타일/단일 HTML 보존. Canvas 대화창 버전은 기존 대화에 참고용 보존.
- 실행: docs/GITHUB_PAGES.md 참조. main push → npm install → 테스트 → Vite 빌드 → 정적 경로 검사 → Pages 배포. 플레이어는 설치 불필요.
- 테스트: 지형 3/3 통과, 변경 JS 4개 구문 검사 통과, workflow YAML 파싱 통과. 빌드 시도 실패(vite 미설치), 오프라인 설치 불가. dist 검사 및 Actions 실제 실행 미검증.
- 실제 화면/스크린샷/FPS: 미확보. Three.js 로딩, 지형, 이동/회전/줌, 조명/그림자, 콘솔, 로딩 실패 UI 모두 실제 브라우저 미검증.
- 장애/제약: 의존성 및 lockfile 미확보, 실제 GitHub 저장소 권한/배포 없음. bootstrap 동적 import 실패 대응 추가, HTML 자체 실패는 대응 불가.
- 임시 결정: 공개 저장소, main 브랜치, Node 22 CI, 상대 base, npm install 사용. CDN 대신 빌드 번들 제공 예정. 단일 HTML은 이전 버전 그대로 유지.
- 미구현: PRE02 이후 전부. 질문: Pages 실제 URL 및 Actions 로그, 화면/FPS/콘솔 결과 요청. 승인 후 다음 단계.

## PRE-STEP 01-B 사용자 확인 추가
2026-11-27 사용자 제공 모바일 화면: Pages 주소 접속 성공, v0.1.2 가상 지형 표시, 표시 FPS 60.0. 지속 FPS, PC, 조작, 콘솔, 그림자는 미검증.
## PRE-STEP 02-A / v0.2.0-alpha.1 (부분 완료)
기존 ZIP 기반, 실제 저장소 동기화 미검증. Copernicus GLO-90 선정, 출처/조건은 TERRAIN_DATA_SOURCES.md 참조. DNS 실패로 원본/가공 DEM 없음. 가상 모드 유지. 신규 DEM loader, mesh, 좌표 변환, 지역 설정, Python 변환, 별도 수동 Actions 데이터 생성, UI 해상도/배율/모드 추가. 가상 강은 DEM 모드에서 숨김. 기본 257, 1배, 중심 위도 근사 좌표계, 마커는 검증 전 근사치. 1025 및 수계 미구현. 결측은 보간 강행 없이 거부. 신규 자동 테스트 2개 및 기존 3개 통과; JS 구문 검사 및 Python 구문 검사 통과. 최초 신규 테스트 구문 오류 수정. Vite 미설치로 빌드 실패. 실제 DEM 고도/방향/마커 정확도, 브라우저, FPS, 스크린샷, Actions 모두 미검증. lockfile 없음. 기존 Pages workflow 및 preview 보존. 데이터 생성 workflow 성공 여부와 실제 지형 확인 필요. PRE02-B 진행 금지. 기획실 질문: 근사 투영/마커 허용 및 90m 데이터 채택 확인.
