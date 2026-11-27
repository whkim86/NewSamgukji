# GitHub Pages 최초 배포 및 업데이트
## 최초 1회 (브라우저만 사용)
1. github.com 로그인 → New repository → 이름 NewSamgukji → Public → Create repository. README 자동 생성은 선택하지 않아도 된다.
2. 이 ZIP을 풀고 NewSamgukji 폴더 내부 파일을 저장소 루트에 업로드한다. 상위 폴더 자체를 넣지 않는다. Add file → Upload files → Commit changes. 브랜치는 main. 공개 저장소에 비밀키나 개인정보를 넣지 않는다.
3. 숨김 폴더 .github가 업로드되지 않았다면 Add file → Create new file → 파일명 `.github/workflows/pages.yml` 입력 → 제공된 workflow 내용 전체 붙여넣기 → Commit changes. vite.config.js, src/bootstrap.js, tests/dist-check.js 및 public/data도 확인한다.
4. Settings → Pages → Build and deployment → Source → GitHub Actions 선택.
5. Actions → Deploy Three.js game → Run workflow → main → Run workflow. 최초 push가 설정 전에 실행되어 실패했다면 다시 실행한다. Actions가 비활성화된 경우 Settings → Actions → General에서 허용한다.
6. build 및 deploy가 모두 성공한 후 Settings → Pages의 Visit site 또는 deploy job의 실제 URL로 접속한다. 예상 주소 형식은 https://<계정>.github.io/<저장소>/ 이며 실제 주소는 GitHub에서 확인한다.
## 이후 업데이트
같은 저장소 main에 변경 파일을 동일 경로로 덮어쓰고 커밋한다. 삭제 파일은 별도로 삭제한다. Actions가 테스트 및 빌드 후 dist만 배포한다. 주소는 저장소 이름/계정/Pages 설정이 유지되는 한 동일하다. 실패하면 Actions 로그를 전달한다. 이전 정상 커밋으로 되돌려 재배포 가능하다.
## 검증
Chrome/Edge에서 3D 표시, 좌클릭 이동, 우클릭 회전, 휠 줌, 그림자 토글, FPS, F12 Console 확인. Network에서 JS/CSS/config 200 응답 확인. 새로고침 전 DevTools Request blocking으로 게임 JS chunk를 차단하여 오류 표시 확인 후 차단 해제. bootstrap 자체가 차단되면 기존 HTML error listener 또는 로딩 상태로 남을 수 있다. WebGL2 미지원/컨텍스트 손실은 별도 오류 표시. 1920×1080에서 FPS 및 화면 캡처 전달.
## 제약
GitHub Actions에서 npm 설치 필요. 플레이어는 CDN/npm/Node 설치 불필요. lockfile 미확보로 npm install 사용; 최초 성공 환경에서 lockfile 생성 후 커밋하고 npm ci로 전환 권장. 실제 배포 및 브라우저 검증은 아직 미실시.
