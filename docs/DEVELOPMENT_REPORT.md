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

## PRE-STEP 02-A-1 / v0.2.0-alpha.2
- Baseline alpha.1: user screenshot confirms deployed actual DEM mode, 257², 131072 triangles, factor 1, displayed 59.9 FPS, five markers and attribution. Original data not independently inspected. Screenshot preserved.
- Changes: index.html, package.json, src/main.js, src/ui/style.css, src/camera/controller.js, src/camera/touch.js, src/terrain/terrain-mesh.js, tools/terrain/prepare_dem.py, tools/terrain/validate_dem.py, .github/workflows/validate-dem.yml, tests/stabilization.test.js, documentation and baseline screenshot.
- Default visual factor 3, resolution 257 unchanged. Fog 2200–3900, hemisphere 1.15, sun 2.8 at (-650,380,350); provisional aesthetic settings, not calibrated. Elevation and slope palette is not land cover. Marker screen size and overlap suppression, mobile reset/shadow controls, custom touch pointer handling, aspect-aware reset (distance capped), cache per resolution and disposal of replaced geometry/material/texture. Existing virtual terrain, preview and Pages workflow preserved.
- Tests: 9/9 Node tests (5 existing, 4 new), JS syntax, Python compile, YAML parse passed. Synthetic grids only; touch math tested, not DOM events. Vite build failed: vite not installed. GitHub DNS unavailable. No new browser screenshots, performance, GPU leak measurements or deployment. No manual user tests requested.
- Actual DEM absent from local baseline ZIP; deployed files must be retained. No raw or processed elevation files changed. New manual Validate published DEM workflow downloads originals to cache without overwriting published grids; reports native nearest-pixel comparisons at grid nodes, stats, marker-nearest grid coordinates, flipped comparisons and shared-node differences. Native nearest vs resampled values may differ; no acceptance threshold or proof of historical accuracy. Workflow unexecuted. Raw files remain temporary cache; original URLs/license documentation preserved.
- Status: code changes delivered, partial completion pending actual DEM audit, build/deployment and browser verification. No PRE-STEP 02-B work. Questions for planning: acceptable resampling error and visual defaults after actual render; no user manual test required this step.

## 통합 V2.0 — STEP 00 / PRE-STEP 02-B 중간 기록
- 기존 alpha.2 로컬 소스 복사, 원본 보존. GitHub DNS 실패, 최신 저장소 일치 미확인. DEM 디렉터리 비어 있음. Vite 미설치로 빌드 실패, lockfile 미확보.
- 기존 9/9 회귀 통과. 신규 좌표 왕복 및 거리 테스트 2/2 통과 (총 11/11). JS 신규 진입점 구문 검사 통과.
- alpha.3 후보: 역투영, Haversine 거리, DEM 메시 클릭 및 실제 고도 샘플, 두 지점 측정선, 초기화 UI 구현. 지형 변경 시 측정 초기화. 기존 마커 좌표 기준 낙양–허창 144.848km (구면 근사, 역사적 거리 아님).
- 변경: src/geo/coordinates.js, src/geo/measurement.js, src/terrain/terrain-mesh.js, src/main.js, index.html, package.json, tests/measurement.test.js, docs/DEVELOPMENT_REPORT.md, docs/CHANGELOG.md.
- 자체 결정: 클릭 이동 허용 5px, 측정선 65개 샘플, 지형 변경 시 초기화. 삭제/이동 없음.
- 미완료: 지도 축척 UI, 투영 오차 정량화, 모바일 다중 터치와 클릭 충돌 검증, 실제 DEM 비교, 브라우저/빌드/배포/성능 검증. 사용자 수동 테스트 생략. 실제 화면 없음.
- 재개 지점: PRE-STEP 02-B 잔여 기능 및 검증 후 02-C. 02-C~05 미착수. 목표 v0.5.0 미달성.

## 통합 V2.0 재개 / alpha.5 부분 구현 후보
- 원본 alpha.3 복사 보존, GitHub ls-remote DNS 실패 재확인, 실제 DEM 없음. 기존 11/11 재실행 통과. Vite 빌드 실패(vite not found). lockfile 없음.
- 02-B: 중심 카메라 거리 기반 100px 근사 축척 표시(수평 지면 축척 아님), 동서 방향 10분할 표본 투영 상대 오차 최대 1.0355%, 모바일 다중 포인터 및 드래그 측정 차단 capture listener 추가. 실제 DOM/터치 검증 없음. 실제 DEM 클릭 검증 없음.
- 02-C: 출처 필수 현대 GeoJSON LineString 수계/도로 로더, 표시/숨김, 누락 상태 표시, DEM 샘플 높이 배치. 실제 데이터, 취득/변환 스크립트, 식생 미확보/미구현. 범위 밖 선 전체 제외(클리핑 미구현). 역사적 지리 아님.
- 02-D: 잠정 속도표, 실제 고도 기반 경사/유형 분류, 이동 비용 함수, 65² 추정 비용 색상 오버레이. 경사/고도 기준 자체 결정(문서 GEO_LAYERS.md). 하천 깊이 추론 안 함. 클릭 비용 정보, 정식 통행 데이터 및 경로 인터페이스 미완료. 오버레이는 지형과 교차 가능. 실제 렌더링 미검증.
- 02-E~04 미착수. 05용 독립 프레임 통계 함수만 선행 작성, UI/실측 미구현. 목표 v0.5.0 미달성.
- 신규 테스트 4개(투영, 레이어 유효성, 이동 비용, 프레임 통계), 총 15/15 통과. JS 전체 구문 검사 통과. 실제 브라우저, FPS, GPU, 배포, 스크린샷 없음. 사용자 수동 테스트 생략. 기존 데이터/워크플로 삭제 없음.
- 변경: index.html, package.json, src/main.js, src/geo/coordinates.js, src/geo/measurement.js, docs/DEVELOPMENT_REPORT.md, docs/CHANGELOG.md. 신규: src/geo/layers.js, src/terrain/cost.js, src/terrain/overlays.js, src/core/performance.js, tests/resume.test.js, docs/GEO_LAYERS.md.
- 재개: 02-C 실제 데이터 취득/변환 및 02-D 잔여 기능, 02-E 통합 이후 03~05. 배포하지 말 것. 기존 DEM 유지 필수. 변경 ZIP은 직전 alpha.3 기준이 아닌 alpha.2 기준 누적 변경으로 제공.

## V2 continuation — v0.5.0-dev.1 (partial candidate, NOT acceptance)
- Baseline alpha.5 archive extracted; 15/15 baseline tests passed. Prior history preserved.
- 02-C: local licensed WGS84 GeoJSON clipping converter (Shapely); densified river/road line vertices. No actual river, road or vegetation dataset acquired; source/license must be verified before redistribution. No automatic acquisition workflow added.
- 02-D: point terrain information and cost-per-km interface; provisional slope/elevation only, no verified land cover or water depth. 02-E integration code updated; actual DEM and visual checks outstanding.
- 03: 4x4 terrain mesh subdivision with shared edge positions and normals, default Three.js frustum culling, zoom level display, cursor zoom option and closer camera limits. Uniform selected resolution only; no mixed LOD, streaming, per-chunk loading/unloading, pinch-centered zoom or verified collision. Near plane .001 world units and min distance .025 are experimental; depth precision and collision need validation. Existing single mesh construction used as intermediate, not selectable mode.
- 04: original primitive gate GLB generated via trimesh (meters, Y-up), GLTFLoader integration and instanced boxes (100/500/1000/5000), fallback boxes on load failure. No Blender execution, animation, other requested models, model cache or distance LOD. Test objects clustered around map center, not historical locations. No external asset license needed for original geometry.
- 05: rolling 3600-frame statistics and resource counts; no controlled 60-second benchmark, presets, real rendered model counts or measured GPU memory. No performance improvement claimed.
- Tests: baseline 15/15; new 4/4; total 19/19. JS syntax and Python syntax checked. GLB header/length tested, not browser loading. npm offline install failed (ENOTCACHED); Vite build failed (vite unavailable). No actual browser, deployment, DEM accuracy or GPU tests. User manual tests intentionally omitted, not passed.
- Developer decisions: 16 uniform chunks, 0.002-degree line densification, experimental camera limits, center test instances, 3600-frame rolling window. No game systems added. Preserve deployed DEM files; do not replace repository wholesale. Candidate not recommended for production deployment until build and runtime verification.
- Changed files: index.html, package.json, src/main.js, src/camera/controller.js, src/geo/measurement.js, src/terrain/{cost,overlays,terrain-mesh,chunks}.js, src/core/models.js, tools/terrain/prepare_layers.py, tools/models/generate_gate.py, public/assets/models/test-gate.glb, tests/next.test.js, docs/DEVELOPMENT_REPORT.md, docs/CHANGELOG.md, README.md.
- Next: actual data acquisition and licensing, build/browser verification, true mixed LOD and seam strategy, model caching and additional assets, controlled performance benchmarks. No formal phase after PRE-STEP 05 started.

## v0.5.0-dev.2 — 잔여 기능 증분 개발
- dev.1 ZIP 기준, 기존 19개 및 신규 4개 테스트 총 23/23 통과. JS/Python 구문 검사 통과.
- Natural Earth 현대 수계/도로 취득 및 변환용 수동 Actions 추가. 실제 다운로드 DNS 실패; 라이선스 원문 및 지역 커버리지 미검증. 식생 미구현. 산출물은 Actions artifact이며 자동 배포하지 않음.
- Chunk별 거리 기반 stride 1/2/4 인덱스 LOD, 전체 경계 정점 보존 및 15% 히스테리시스, 고정 GPU 인덱스 버퍼와 draw range 적용. 실제 화면 균열/팝핑, 지형과 오버레이 높이 차이 미검증. 원본 해상도 이상 정밀도 아님. 동적 타일 스트리밍 미구현.
- 자체 기본 도형 GLB 7개 추가(나무, 바위, 건물, 성벽, 병사, 장수, 말). 기존 성문 보존. 총 8개 파일 헤더 검사 통과. Blender 및 애니메이션 미실시. GLTF Promise 캐시 및 인스턴스별 geometry/material 복제; 고정 8개 원본 캐시 페이지 수명 유지. 모델별 세부 LOD 미구현.
- LOW/MEDIUM/HIGH/CUSTOM 품질 선택: 지형 해상도, 픽셀 비율, 그림자, LOD 거리, 모델 표시 거리. CUSTOM은 기존 개별 해상도/그림자 조절이며 전체 항목 편집기는 아님. 식생 밀도/안개 프리셋 미구현. 원거리 모델 그룹 숨김은 스트레스 인스턴스에도 적용.
- 자체 결정: LOD 거리 10/35,20/60,35/90km, 모델 표시 1.5/3/6km. 기본 MEDIUM. 모델은 원본 캐시에서 복제하며 텍스처 없는 자체 모델만 대상.
- npm registry DNS 실패, Vite 미설치로 빌드 실패. 브라우저, 실제 DEM, GPU, 60초 벤치마크, 배포 미검증. 사용자 수동 테스트 생략. 정식 v0.5.0 판정 보류.
- 변경: index.html, package.json, src/main.js, src/core/models.js, src/core/quality.js, src/terrain/terrain-mesh.js, src/terrain/lod.js, tests/dev2.test.js, tools/models/generate_extra.py, tools/terrain/fetch_layers.py, .github/workflows/geo-layers.yml, GLB 7개, 문서.


## V2.1 verification checkpoint (dev.2 baseline)
- Node 22.16.0, npm 10.9.2, Chromium 144 available; no node_modules, lockfile or npm cache entries. DNS lookup for GitHub/npm returned no addresses.
- Existing 23 tests passed again; JS and YAML syntax checks passed. Production build failed: vite not found. No browser game execution or performance measurements.
- Added manual non-deploy verification workflow and initial Playwright checks (desktop/mobile renderer, actual DEM/GLB, quality and fallback). Workflow not executed. Full interaction and benchmark coverage remains.
- Added procedural soldier root rocking animation demonstration, not articulated walking/running; actual playback unverified.
- Pages candidate version gate added to prevent prerelease deployment; stable release still needs final validation.
- No DEM or natural data acquired; no existing files deleted. No user manual testing.
- Resume: execute verification workflow on isolated branch with existing DEM, obtain lockfile and logs, fix integration failures, then complete streaming, vegetation, articulated animation and benchmarks. Version remains dev.2 because dev.3 scope incomplete.

## V2.1 checkpoint continuation — 2026-11-27
- Baseline checkpoint ZIP extracted; original 23 tests passed independently. Added bounded asynchronous cache (3 DEM resolutions), tile sample extraction and shared-edge test. This is not camera-driven tile streaming; existing 16 chunks retained.
- Browser check expanded with camera input, layer controls, measurement clicks and animation selection; assertions are preliminary, not full functional verification. Network errors now fail verification.
- Added opt-in 24-case benchmark (3 qualities × 4 counts × static/moving, 60 seconds each); software renderer requested. Wheel input is a provisional path, not a calibrated camera trajectory. Not executed.
- Tests 26/26 passed. Browser scripts syntax and workflow YAML parse passed. Build failed: vite not found. No repeated DNS download attempted. Chromium standalone probe produced no DOM; WebGL not confirmed. No game screenshots or measured FPS.
- Actual DEM, vegetation, articulated animation, dynamic streaming, repeated resource verification remain outstanding. Version stays dev.2; no deployment or post-PRE-05 development.
- Decisions: cache limit 3, benchmark opt-in, workflow timeout 65 minutes. No source deletion. Resume with actual dependency provisioning and browser CI, then streaming/vegetation/animation and resource checks.

## V2.1 local residency checkpoint
Baseline 26/26; current 28/28 (tile selection/retention and land-cover orientation/validation). Added local camera-based mesh creation/removal with disposal and source cleanup, optional modern land-cover lookup for clicked cost, additional rigid limb soldier with mixer clips. See STREAMING_LANDCOVER.md for schema and limitations. Existing GLBs and reports retained. No DEM or real land-cover files acquired. No DNS or EGL retry. Build attempted: vite not found. JS syntax checked; browser/benchmark/GPU lifecycle not executed. Decisions: 16 resident limit, radius max(far,2*camera Y), 15% retention, one million cover cells, separate procedural soldier. No new screenshots. Remain dev.2: network tile streaming, actual land cover rendering, repeated resource verification and external CI execution pending. Resume from this checkpoint; no formal game features.


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
