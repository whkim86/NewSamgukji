# V3 실제 데이터 취득 및 검증 (2026-11-27 KST)

기존 DEM은 원격 커밋 `767c23712b6e30087896f8e24fa2ba3cd8162d29`에서 복사했다. 기존 메타데이터와 129/257/513 f32는 변경하지 않았다. SHA-256 및 실제 최소·최대·평균은 `verification/data-audit.json`에 기록한다. 48개 파생 타일은 원래 격자의 겹치는 경계 정점을 그대로 포함하며 모든 표본의 원본 일치와 SHA-256을 검사한다.

Copernicus 원본 9개 COG는 `dem-cache/`에 별도로 보관한다. `validate_dem.py`는 북→남, 서→동 방향의 격자와 원본 최근접 화소를 비교한다. 이는 빌리니어 다운샘플 결과와 최근접 화소의 차이로, 데이터의 지표면 실측 오차를 뜻하지 않는다. 513² 격자의 최근접 원본 대비 MAE 5.318m, RMSE 11.186m. 257²는 MAE 8.398m, 129²는 12.789m. 뒤집힌 방향의 MAE는 각각 약 142m/279m로 정상 방향보다 크다. 대표 5개 마커의 인접 격자 고도 및 비교 좌표는 `verification/dem-validation.json`에 보존한다. 마커는 현대 지명 근사 위치이며 역사 위치 확정 자료가 아니다.

각 해상도는 서로 다른 면적 리샘플링 결과이다. 513²와 공유 좌표에서 129²는 최대 248.778m, 257²는 117.678m 차이가 있다. 표시 해상도와 독립된 고도·경사·이동비용 조회에는 513²를 기준으로 사용한다. 시각 표면은 선택 해상도와 고도 배율을 따르므로 실제 조회 고도와 시각 표면 높이가 같다는 의미가 아니다.

수계는 Natural Earth 1:10m rivers/lake centerlines 3개 선, 도로는 203개 선을 시험 경계로 잘랐다. 황하를 포함한 현대 개략 수계이며 소하천·지역 도로의 완전한 목록이 아니다. UTF-8을 명시하여 Windows CP949 디코딩 오류를 수정했다.

ESA WorldCover 2021 v200 원본 N33E111, N33E114 COG를 확보하고 시험 경계를 500×340 셀로 최근접 표본화했다. 출력 간격은 0.005도이며 원본 10m 해상도 출력이 아니다. 북→남 행, 서→동 열. 170,000개 셀은 숲 29,846, 초지 13,573, 농경지 103,891, 시가지 19,693, 나지 497, 수역 2,500이다. 습지 셀은 이 축소 표본에서 검출되지 않았다. 습지를 만들어 넣지 않는다. 수역 분류로 수심이나 통행 가능성을 추론하지 않는다.

토지피복 색상은 실측 분류에 따른 표시이고, 최대 800개 나무 기호는 숲 셀에 결정적으로 선택한 절차적 기호이다. 실제 개별 나무 좌표·밀도·수종 자료가 아니다. 실제 고대 식생이나 삼국시대 지리 복원 자료가 아니다.

출처 및 이용조건:

- [Copernicus AWS 데이터](https://registry.opendata.aws/copernicus-dem/) 및 [공식 라이선스·출처 표기](https://dataspace.copernicus.eu/explore-data/data-collections/copernicus-contributing-missions/collections-description/COP-DEM): 공개 GLO-90 이용, 가공물 출처 표기를 앱에 유지. 현대 DSM이며 건물·식생을 포함한다.
- [Natural Earth 이용조건](https://www.naturalearthdata.com/about/terms-of-use/): public domain, 수정·재배포 허용.
- [ESA 데이터 및 라이선스](https://esa-worldcover.org/en/data-access): CC BY 4.0, [2021 데이터 DOI](https://doi.org/10.5281/zenodo.7254221). 앱과 JSON에 출처 표기를 포함했다.

원본 COG와 개발용 Python 패키지는 Git에 넣지 않는다. 파생 f32/GeoJSON/토지피복 JSON 및 원본 URL·해시는 포함한다. 원본·파생 파일의 전체 체크섬 목록은 `verification/source-hashes.json`에 기록한다.
