"""Download Actions logs with credentials limited to api.github.com."""
import json,subprocess,base64,urllib.request,urllib.error,pathlib,zipfile,re
root=pathlib.Path(__file__).resolve().parents[1]
run=json.loads((root/'verification/github-actions.json').read_text())[0]
c=subprocess.run(['git','credential','fill'],input='protocol=https\nhost=github.com\n\n',text=True,capture_output=True,check=True)
d=dict(s.split('=',1) for s in c.stdout.splitlines() if '=' in s)
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args):return None
request=urllib.request.Request(f"https://api.github.com/repos/whkim86/NewSamgukji/actions/runs/{run['id']}/logs",headers={'User-Agent':'NewSamgukji-verification','Authorization':'Basic '+base64.b64encode((d['username']+':'+d['password']).encode()).decode()})
try:
 with urllib.request.build_opener(NoRedirect).open(request,timeout=30) as response:data=response.read()
except urllib.error.HTTPError as e:
 if e.code!=302:raise
 with urllib.request.urlopen(e.headers['Location'],timeout=30) as response:data=response.read()
p=root/f"verification/ci-{run['id']}.zip";p.write_bytes(data)
with zipfile.ZipFile(p) as z:
 for name in z.namelist():
  if 'Browser tools' in name:
   lines=z.read(name).decode('utf-8',errors='replace').splitlines();print('\n'.join(lines[-55:]))
