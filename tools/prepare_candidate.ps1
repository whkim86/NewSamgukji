$ErrorActionPreference = 'Stop'
$sourceRoot = Split-Path -Parent $PSScriptRoot
$candidateRoot = Join-Path (Split-Path -Parent $sourceRoot) 'NewSamgukji_remote_V3'
$workspaceRoot = [IO.Path]::GetFullPath((Split-Path -Parent $sourceRoot))
if (-not ([IO.Path]::GetFullPath($candidateRoot).StartsWith($workspaceRoot + [IO.Path]::DirectorySeparatorChar))) { throw 'Candidate path outside workspace' }
if (-not (Test-Path -LiteralPath (Join-Path $candidateRoot '.git'))) { throw 'Missing isolated repository clone' }
foreach ($name in @('.github','docs','preview','public','screenshots','src','tests','tools','.gitignore','AGENTS.md','index.html','package.json','package-lock.json','README.md','START.bat','vite.config.js')) {
    $item = Join-Path $sourceRoot $name
    if (Test-Path -LiteralPath $item -PathType Container) {
        $destination = Join-Path $candidateRoot $name
        New-Item -ItemType Directory -Path $destination -Force | Out-Null
        Get-ChildItem -LiteralPath $item -Force | Copy-Item -Destination $destination -Recurse -Force
    } elseif (Test-Path -LiteralPath $item -PathType Leaf) {
        Copy-Item -LiteralPath $item -Destination (Join-Path $candidateRoot $name) -Force
    }
}
Write-Output "Candidate copied without deletion: $candidateRoot"
