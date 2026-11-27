# 新 삼국지 WEB v0.1.0
PRE-STEP 01 전용 소스 프로젝트. 실제 중국 지형이 아닌 가상 지형.
## Windows 실행
1. https://nodejs.org/ 에서 Node.js LTS (22 이상 권장) 설치.
2. ZIP 전체 압축 해제 후 START.bat 실행. 첫 실행은 npm 서버 인터넷 연결 필요.
3. 브라우저 자동 열기. 안 열리면 터미널에 표시된 Local 주소 접속.
4. 종료: 터미널 Ctrl+C.
수동 실행: `npm install`, `npm run dev`. 테스트: `npm test`. 빌드: `npm run build` (미검증).
index.html 직접 더블클릭은 지원하지 않음. WebGL2 및 하드웨어 가속 필요.
## 조작
좌클릭 드래그 이동, 우클릭 드래그 회전, 휠 확대/축소, 좌측 초기화 및 그림자 토글.
## 검증 요청
1920×1080 브라우저 최대화, 초기 FPS 및 이동/회전/줌/창 크기 변경/그림자 토글 확인. F12 Console 오류 및 화면 캡처 전달. 가능하면 5분 실행 후 FPS 확인.
## 의존성
Three.js 0.170.0 (MIT), Vite 5.4.21 (MIT). 외부 모델/텍스처 없음. 라이브러리는 npm에서 설치하며 ZIP에 포함되지 않음.

## 설치 없는 미리보기
preview/index.html을 브라우저로 열기. 인터넷 및 CDN 접근 필요. 정적 호스팅 가능하나 미배포.

## v0.1.2 정식 웹 배포
GitHub Pages 배포 및 업데이트: [docs/GITHUB_PAGES.md](docs/GITHUB_PAGES.md). 정식 엔진은 Three.js 모듈형 소스만 유지한다. preview/index.html은 이전 단일 HTML 보존본이다. GitHub Actions에서 빌드하며 플레이어 설치는 필요 없다. 실제 배포 전 상태.

DEM 취득 및 배포: docs/TERRAIN_DATA_SOURCES.md 참조.

### alpha.2 update
Upload update ZIP contents to existing repository root, preserving all existing DEM files under public/assets/terrain/henan-central. No deletions. Pages workflow builds on push. Optional maintainer audit: Actions > Validate published DEM > Run workflow; artifact dem-validation.json. Roll back via reverting update commit. Full source ZIP excludes DEM binaries because unavailable locally; it is not a standalone actual-DEM build.

## v0.5.0-dev.1
Experimental source snapshot, not a verified deployment. Preserve existing DEM assets. Run npm install, npm test, npm run build and npm run test:dist before deployment. Local layer conversion: python tools/terrain/prepare_layers.py INPUT river --source SOURCE --license LICENSE (requires shapely; WGS84 input). Original gate generator requires trimesh.

### dev.2 업데이트
기존 DEM 파일을 보존하고 변경 ZIP 내부 파일만 저장소에 반영한다. Actions의 Acquire modern geographic layers를 수동 실행하면 현대 수계/도로 artifact를 생성하도록 구성했다(미검증). 성공 시 출처와 내용을 검토한 뒤 public/data에 JSON을 추가한다. 기존 Pages workflow로 빌드한다. 실패 시 dev.2 변경 커밋을 되돌린다. 현재 정식 배포 후보가 아니다.
