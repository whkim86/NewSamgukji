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
