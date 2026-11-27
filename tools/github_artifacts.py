"""Fetch verification evidence, with credentials limited to the GitHub API."""
import pathlib,json,subprocess,base64,urllib.request,urllib.error,zipfile,sys
sys.stdout.reconfigure(encoding='utf-8');root=pathlib.Path(__file__).resolve().parents[1]
run=json.loads((root/'verification/github-actions.json').read_text())[0]
c=subprocess.run(['git','credential','fill'],input='protocol=https\nhost=github.com\n\n',text=True,capture_output=True,check=True);d=dict(s.split('=',1) for s in c.stdout.splitlines() if '=' in s)
headers={'User-Agent':'NewSamgukji-verification','Authorization':'Basic '+base64.b64encode((d['username']+':'+d['password']).encode()).decode()}
base='https://api.github.com/repos/whkim86/NewSamgukji/'
artifacts=json.load(urllib.request.urlopen(urllib.request.Request(base+f"actions/runs/{run['id']}/artifacts",headers=headers),timeout=30))['artifacts']
class NoRedirect(urllib.request.HTTPRedirectHandler):
 def redirect_request(self,*args):return None
for a in artifacts:
 if a['name']!='candidate-verification':continue
 try:
  response=urllib.request.build_opener(NoRedirect).open(urllib.request.Request(base+f"actions/artifacts/{a['id']}/zip",headers=headers),timeout=30)
 except urllib.error.HTTPError as e:
  if e.code!=302:raise
  response=urllib.request.urlopen(e.headers['Location'],timeout=30)
 with response:data=response.read()
 path=root/f"verification/ci-artifact-{run['id']}.zip";path.write_bytes(data)
 with zipfile.ZipFile(path) as z:
  for name in z.namelist():
   if name.endswith('browser.json'):
    text=z.read(name).decode('utf-8-sig');(root/f"verification/ci-browser-{run['id']}.json").write_text(text,encoding='utf-8');print(text)
