# V2.1 streaming checkpoint
- Resident meshes selected by camera X/Z and max(far LOD radius, twice camera Y), 15% retention, maximum 16. Source grid and normals remain resident on CPU; this is local mesh residency, not asynchronous network tile streaming. Mesh creation synchronous; horizon gaps and frame spikes require browser validation.
- Optional `public/data/henan-central-landcover.json`: source `ESA WorldCover 2021`, license string, bounds [west,south,east,north], width, height, classes north-to-south row-major integer ESA class codes (0 missing). Maximum one million cells. No actual raster acquired. License string is metadata, not independent license verification. Forest/wetland affect clicked cost only; cost overlay not refreshed. No water-depth inference. No vegetation rendering yet.
- Original eight GLBs retained. Additional rigid articulated soldier uses separate arm/leg pivots and idle/walk/run clips. Not a rigged GLB; no visual validation.


## V3.0 superseding checkpoint
실제 네트워크 detail tiles와 토지피복을 확보했다. 개별16타일×3해상도, bounded async loader(동시3/캐시16), stale 요청취소, 원거리캐시해제, 저해상도 배경 및 실패대체. CPU query용 격자는 별도 상주한다. 실제 ESA 2021 500×340 축소표본을 표면색/비용/최대800개 절차적 숲기호에 연결했다. 상세 출처와 제한은 V3_DATA_PROVENANCE.md. 위 미확보/미구현 기록은 이전 checkpoint 이력으로 보존한다.
