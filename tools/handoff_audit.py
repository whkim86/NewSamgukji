"""Read-only comparison against both the original ZIP and isolated remote checkout."""
import pathlib,zipfile,hashlib,json,subprocess
root=pathlib.Path(__file__).resolve().parents[1]
remote=root.parent/'NewSamgukji_remote_V3'
backup=root.parent/'NewSamgukji_before_V3_20261127.zip'
sha=lambda b:hashlib.sha256(b).hexdigest()
with zipfile.ZipFile(backup) as z:
 baseline={str(pathlib.PurePosixPath(i.filename).relative_to(root.name)):sha(z.read(i)) for i in z.infolist() if not i.is_dir()}
current={str(p.relative_to(root).as_posix()):sha(p.read_bytes()) for p in root.rglob('*') if p.is_file() and not any(x in p.relative_to(root).parts for x in ['node_modules','.tooling','dist','verification','dem-cache','cover-cache','.git'])}
git=['git','-c',f'safe.directory={remote.as_posix()}','-C',str(remote)]
base='767c23712b6e30087896f8e24fa2ba3cd8162d29'
paths=subprocess.check_output(git+['ls-tree','-rz','--name-only',base]).decode().split('\0')
remote_files={p:sha(subprocess.check_output(git+['show',f'{base}:{p}'])) for p in paths if p}
meta='public/assets/terrain/henan-central/metadata.json'
result=dict(backup=str(backup),backup_sha256=sha(backup.read_bytes()),baseline_count=len(baseline),current_count=len(current),remote_count=len(remote_files),baseline_deleted=sorted(set(baseline)-set(current)),baseline_modified=sorted(k for k in baseline if k in current and baseline[k]!=current[k]),baseline_added=sorted(set(current)-set(baseline)),remote_only=sorted(set(remote_files)-set(current)),remote_differences=sorted(k for k in remote_files if k in current and remote_files[k]!=current[k]),dem_preserved=all(current.get(k)==v for k,v in remote_files.items() if k.startswith('public/assets/terrain/') and k.endswith('.f32')),metadata_preserved=json.loads((root/meta).read_text(encoding='utf-8'))==json.loads(subprocess.check_output(git+['show',f'{base}:{meta}'])))
(root/'verification/handoff-audit.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(result,ensure_ascii=False,indent=2))
