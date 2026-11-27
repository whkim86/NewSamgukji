"""Read authorized repository Actions state; never print credentials."""
import json,urllib.request,urllib.error,subprocess,pathlib,base64
root=pathlib.Path(__file__).resolve().parents[1]
headers={'Accept':'application/vnd.github+json','User-Agent':'NewSamgukji-verification'}
def get(path):
 url='https://api.github.com/repos/whkim86/NewSamgukji/'+path
 try:
  return json.load(urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=30))
 except urllib.error.HTTPError as e:
  if e.code not in (401,404) or 'Authorization' in headers:raise
  result=subprocess.run(['git','credential','fill'],input='protocol=https\nhost=github.com\n\n',text=True,capture_output=True,check=True)
  credentials=dict(line.split('=',1) for line in result.stdout.splitlines() if '=' in line)
  headers['Authorization']='Basic '+base64.b64encode((credentials['username']+':'+credentials['password']).encode()).decode()
  return json.load(urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=30))
runs=get('actions/runs?branch=codex%2Fv3-stabilization&per_page=3')['workflow_runs']
summary=[]
for run in runs:
 jobs=get(f"actions/runs/{run['id']}/jobs")['jobs']
 summary.append({k:run[k] for k in ['id','name','head_sha','status','conclusion','html_url']})
 summary[-1]['jobs']=[{'name':j['name'],'conclusion':j['conclusion'],'steps':[{'name':s['name'],'status':s['status'],'conclusion':s['conclusion']} for s in j['steps']]} for j in jobs]
(root/'verification/github-actions.json').write_text(json.dumps(summary,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
