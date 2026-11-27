"""Generate the requested A–M report from completed, saved measurements."""
from pathlib import Path
import json,os
r=Path(__file__).resolve().parents[1]
load=lambda p:json.loads((r/p).read_text(encoding='utf-8-sig'))
b=load('verification/benchmark-v3.json');assert len(b['results'])==24 and all(x['durationMs']>=60000 for x in b['results'])
version=load('package.json')['version'];complete=os.environ.get('V3_COMPLETE')=='1'
rows=[]
for q in ['LOW','MEDIUM','HIGH']:
 for n in [100,500,1000,5000]:
  a=next(x for x in b['results'] if x['quality']==q and x['count']==n and not x['moving']);c=next(x for x in b['results'] if x['quality']==q and x['count']==n and x['moving'])
  rows.append(f"|{q}|{n:,}|{a['averageFps']:.1f}|{c['averageFps']:.1f}|{a['p95Ms']:.1f} / {c['p95Ms']:.1f}|")
gpu=b['environment']['renderer'];latest=load('verification/github-actions.json')[0]
ci=f"[{latest['conclusion'] or latest['status']}]({latest['html_url']})"
status='완료 — 시험 지역 기술 기반 범위. 정식 게임 시스템 개발 승인과는 별개.' if complete else '최종 완료 보류 — 아래 미검증 및 배포 상태 참조.'
text=f'''# 신 삼국지 WEB — V3.0 기획실 제출 보고

## A. 전체 개발 결과 및 최종 버전

현재 버전 **v{version}**. PRE-STEP 05 판정: **{status}** 기존 프로젝트를 증분 수정했으며 원본 73개 파일과 원격 DEM을 보존했다. 원본 ZIP SHA-256: `07665612074af40bb376189f7b70fff750d76db77a080dbcd68aa56ed6144eef`. 원격 인수 기준 커밋 `767c23712b6e30087896f8e24fa2ba3cd8162d29`.

## B. 기존 코드 분석 및 수정

기존28개 테스트를 실제 재실행해 통과했다. 누락된 의존성과 DEM을 확보해 실제 실행했다. Windows CP949 변환 오류, 표면 오프셋의 world/metre 단위 혼동으로 병사가 레이어에 가려지는 문제, 해상도에 따라 조회 고도가 달라지는 문제, 비용 오버레이 갱신 누락, 근거리 LOD의 Chunk 중심 거리 판정, 원거리 Chunk 제거 후 배경 공백, 모바일 패널 과대, favicon404를 수정했다. 수계/도로206개 선을 레이어별 LineSegments로 합쳐 해당 선 Draw Call을206회에서2회로 줄였다.

## C. 실제 빌드 및 브라우저 검증

Node24.19.0/npm11.17.0, Three0.170.0/Vite5.4.21 유지. 고정 Playwright1.51.1과 lockfile 확보. Production Build 및 dist 경로 검사 성공. 기존28개+신규 네트워크타일3개=31개 자동 테스트 통과. 실제 GPU 통합8개 통과(오류·네트워크실패 없음), Linux SwiftShader CI: {ci}. 실제GPU와 소프트웨어 결과는 구분했다. CI Ubuntu26.04 미지원은24.04 고정으로, 모바일 접힌 패널 조작은 열기 동작 추가로 수정했다. 의도적 AbortController 취소는 별도 cancelled 항목으로 기록한다.

## D. 실제 데이터

기존 Copernicus GLO-90 DEM129/257/513 및 메타데이터를 원격에서 그대로 복구했다. 원본 COG9개와 대조해 고도통계·방향·대표5마커·리샘플링 차이를 기록했다. 513² min45.29655/max2064.92358/mean236.87291m, 원본 최근접 대비MAE5.318m/RMSE11.186m. 이는 다운샘플과 최근접 화소 차이로 실측 정확도 수치가 아니다.

Natural Earth 현대 수계3개(황하 포함), 도로203개를 확보했다. ESA WorldCover2021 COG2개에서500×340(170,000셀,0.005도) 축소표본을 생성했다. 숲/초지/농경지/시가지/나지/수역이 있으며 이 축소표본에서 습지는 검출되지 않았다. 현대 자료이며 삼국시대 지리 복원 자료가 아니다. [출처·라이선스 및 정확도 제한](V3_DATA_PROVENANCE.md), 체크섬·모든 표본 검사는 `verification/data-audit.json`, 원본 SHA는 `verification/source-hashes.json`.

## E. 스트리밍 및 LOD

16 Chunk와3단계LOD/15%히스테리시스/인덱스 버퍼 재사용을 유지했다. 48개 개별 DEM 디테일 타일과 manifest를 만들었다. 카메라 우선순위, 동시3요청, 최대16캐시, 중복방지, 원거리해제, 불필요요청취소, 실패후대체 및 재진입재시도, 상주 저해상도 배경을 적용했다. 타일48개 모든 표본이 원격 원본과 정확히 일치하며 공유 경계도 같은 원본값이다. GPU 검증에서 Chunk 감소/재접근/LOD 변화를 확인했다.

실제 고도 조회에는513² 기준을 사용하므로 해상도·고도배율·LOD를 바꿔도 조회값은 유지된다. 표시 지형은 선택 해상도를 따른다. CPU 쿼리용 전체 격자/법선은 상주한다. 무한세계 CPU 데이터 스트리밍 또는 초기 메시 생성의 완전한 비동기화를 완료했다는 뜻이 아니다.

## F. 모델 및 애니메이션

기존 자체GLB8종과 별도 관절병사를 보존했다. 실제 모델8종 및 관절 병사가 렌더링됐으며 idle/walk/run의 관절 회전값 변화를 검증했다. 그림자·지형배치·Fade 전환·Mixer 정리를 확인했다. 고정8종 원본캐시,100/500/1000/5000 InstancedMesh 테스트와 onBeforeRender 기반 실제 렌더링 계수를 기록했다. 스트레스 인스턴스는 상자이며5,000개 고품질 병사 렌더링 시험이 아니다. 스키닝·실사모델은 제작하지 않았다.

## G. 실제 실행 화면

아래 파일은 실제 Chromium 실행 캡처이다. 도시 주변은 현대 지명 마커 근처이며 도시 게임 시스템은 미구현이다.

- [허난성 전체·현대 수계/도로·토지피복](verification-v3/henan-map.png)
- [산악 확대 및 Chunk LOD](verification-v3/mountains-lod.png)
- [거리 측정](verification-v3/measurement.png), [이동 비용](verification-v3/movement-cost.png)
- [대기](verification-v3/animation-0.png), [걷기](verification-v3/animation-1.png), [달리기](verification-v3/animation-2.png)
- [모바일 화면](verification-v3/mobile-final.png), [성능 패널](verification-v3/benchmark-final.png)

## H. 성능 및 자원

Windows10 Home/i7-7700HQ(4코어8스레드)/RAM32GB/Chromium134/1920×1080。실제 렌더러: `{gpu}`. GTX1050도 설치되어 있으나 이번 브라우저는 Intel GPU를 선택했다. GTX1050 결과로 대체하지 않는다. 초기 로딩 {b['environment']['initialLoadMs']}ms(해당 로컬 실행). 각 조건60초 이상, 동일20초 주기 카메라 경로, 정지와이동을 구분했다. 이는 해당 실행 시점의 측정이며 여러 앱이 실행된 PC의 독점 실험실 측정은 아니다.

|품질|상자 수|정지 평균FPS|이동 평균FPS|P95ms 정지/이동|
|---|---:|---:|---:|---:|
'''+ '\n'.join(rows)+f'''

최소FPS·평균프레임시간·DrawCall·삼각형·Chunk·활성/실제렌더링모델·Geometry·Texture의 초별 표본은 `verification/benchmark-v3.json`에 보존했다. 목표60FPS를 모든 조건에서 충족하지 않았다. MEDIUM5000은30FPS 미만이며 LOW 선택이 유리하다. 조건별 실패와 한계는 실제 수치대로 제출한다.

품질3종과실제/가상지형을4회 반복한 동일 최종조건에서Geometry48/Texture2로 유지됐다(첫렌더링/숨김/그림자조건에 따라 수가 달라지므로 동일조건 비교). DEM캐시최대3, 디테일캐시16, 모델원본8 확인. GPU바이트 메모리는 브라우저에서 직접 측정하지 못해 산출하지 않았다.

## I. 변경 파일 및 실행

주요변경: src/main.js, terrain-mesh.js, overlays.js, 신규network-tiles.js/cover-render.js, models.js, UI, prepare_layers.py/validate_dem.py, 공개데이터·타일, 테스트/검증도구, lockfile, workflow 및문서. 전체목록은 `verification/handoff-audit.json`. 기존73개 파일 삭제/이동 없음. 새로 만든 일회성 수정스크립트는 verification/development-scripts로 옮겨 배포소스에서 제외했다.

실행: `npm ci` 후 `npm run dev`. 검증: `npm test`, `npm run test:data`, `npm run build`, `npm run test:dist`. 브라우저 설치: `npx playwright install chromium`. Production서버4174에서 `npm run test:stability`는 GAME_URL을 지정하거나 기본4173으로 실행한다. `npm run test:benchmark`는기본4174에서24조건을측정한다. START.bat도 유지했다. Python은 데이터 재취득용이며 플레이어 실행에 불필요하다.

## J. 알려진 문제 및 미검증

- GTX1050을 직접선택한 성능, 실제모바일기기, 장시간soak/드라이버별차이, GPU바이트메모리는 미검증.
- 초기 격자/메시 생성은 동기식이다. 프레임급증 및 LOD전환팝핑 가능성이 있으며 지형geomorph는 없다.
- 쿼리513² 자체도다운샘플이다. 저해상도표면은동일좌표고도가다를수있다. 시각표면과권위고도는분리되어있다.
- 지리투영은지역근사(기존동서표본최대약1.04%오차). 중국전체확장시투영/타일체계재검토필요.
- 현대토지피복축소표본·개략수계도로이며고대지도/개별실제나무가아니다. 수심·하천통행판정은추론하지않는다.
- 원본모델캐시는고정8종범위다. 향후임의에셋카탈로그에대한범용메모리예산정책은별도설계가필요하다.
- 번들633KB 수준경고는유지된다. 기존정상기능을삭제하거나불필요업그레이드로우회하지않았다.

## K. 자체 설계 결정

실제조회고도513²고정,동시요청3/캐시16,3개해상도쿼리캐시,최대800개절차적숲기호,지도패널모바일기본접힘,렌더링오프셋은미터단위,카메라근접LOD는Chunk경계거리기준. 기존독립Three.js엔진과공개에셋정책을유지했다.

## L. PRE-STEP05 최종 완료 여부

{status}

배포주소: https://whkim86.github.io/NewSamgukji/ 。실제배포및회귀결과는 `verification/deployment.json` 및누적 DEVELOPMENT_REPORT.md의TASK07기록을기준으로한다. 배포완료기록이없는경우위주소의기존정상버전은이번후보배포증거가아니다.

## M. 정식 개발 다음 단계 제안

기획실 검토 후에만 정식 게임 단계로 진행한다. 우선 허난성 소규모 거점 및 부대 데이터 스키마, 시간 진행과 실제 거리 이동 인터페이스, 지형 통행 규칙 및 경로 탐색을 설계하고 이후 전투로 확장한다. 이번 작업에서 출진/행군/A*/전투/내정/외교/경제/시나리오/멀티플레이/EXE는 추가하지 않았다.
'''
for before,after in {
 '실제GPU':'실제 GPU','소프트웨어 결과':'소프트웨어 결과','자동테스트':'자동 테스트','원본모델캐시':'원본 모델 캐시','지형배치':'지형 배치','고품질 병사':'고품질 병사','개별실제나무':'개별 실제 나무','초기 격자/메시 생성':'초기 격자/메시 생성',
 '장시간soak':'장시간 지속 실행','드라이버별차이':'드라이버별 차이','GPU바이트메모리':'GPU 메모리 바이트 수','실제모바일기기':'실제 모바일 기기','지형geomorph':'지형 geomorph','LOD전환팝핑':'LOD 전환 시 팝핑',
 '쿼리513² 자체도다운샘플이다. 저해상도표면은동일좌표고도가다를수있다. 시각표면과권위고도는분리되어있다.':'조회용 513² 격자도 다운샘플이다. 저해상도 표면은 동일 좌표의 고도가 다를 수 있다. 시각 표면과 기준 고도는 분리되어 있다.',
 '지리투영은지역근사(기존동서표본최대약1.04%오차). 중국전체확장시투영/타일체계재검토필요.':'지리 투영은 지역 근사이다(기존 동서 표본 최대 약 1.04% 오차). 중국 전체로 확장할 때 투영 및 타일 체계를 재검토해야 한다.',
 '현대토지피복축소표본·개략수계도로이며고대지도/개별 실제 나무가아니다. 수심·하천통행판정은추론하지않는다.':'현대 토지피복 축소 표본과 개략 수계·도로이다. 고대 지도나 실제 개별 나무 자료가 아니다. 수심 및 하천 통행 여부는 추론하지 않는다.',
 '실제조회고도513²고정,동시요청3/캐시16,3개해상도쿼리캐시,최대800개절차적숲기호,지도패널모바일기본접힘,렌더링오프셋은미터단위,카메라근접LOD는Chunk경계거리기준. 기존독립Three.js엔진과공개에셋정책을유지했다.':'실제 조회 고도 513² 고정, 동시 요청 3개와 캐시 16개, 해상도 조회 캐시 3개, 최대 800개 절차적 숲 기호, 모바일 지도 패널 기본 접힘을 선택했다. 렌더링 오프셋은 미터 단위이며, 근접 LOD는 Chunk 경계까지의 거리를 기준으로 한다. 기존 독립 Three.js 엔진과 공개 에셋 정책을 유지했다.',
}.items():text=text.replace(before,after)
(r/'docs/V3_FINAL_REPORT.md').write_text(text,encoding='utf-8')
print('Wrote docs/V3_FINAL_REPORT.md from 24 measured cases')
