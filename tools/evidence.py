"""Hash source rasters and copy shareable verification evidence into repository docs."""
from pathlib import Path
import hashlib,json,shutil
r=Path(__file__).resolve().parents[1];hashes={}
for folder in ['dem-cache','cover-cache','public/assets/terrain/henan-central','public/data','public/assets/models']:
 for p in sorted((r/folder).rglob('*')):
  if p.is_file():
   digest=hashlib.sha256()
   with p.open('rb') as f:
    for chunk in iter(lambda:f.read(1024*1024),b''):digest.update(chunk)
   hashes[p.relative_to(r).as_posix()]={'bytes':p.stat().st_size,'sha256':digest.hexdigest()}
(r/'verification/source-hashes.json').write_text(json.dumps(hashes,indent=2),encoding='utf-8')
out=r/'docs/verification-v3';out.mkdir(exist_ok=True)
for p in (r/'verification').iterdir():
 if p.is_file() and p.suffix in ['.json','.log','.png'] and not p.name.startswith('ci-browser-'):
  shutil.copy2(p,out/p.name)
print(f'Hashed {len(hashes)} files; copied shareable evidence')
