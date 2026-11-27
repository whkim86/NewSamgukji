$ErrorActionPreference = 'Stop'
$sourceRoot = [IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot))
$workspaceRoot = [IO.Path]::GetFullPath((Split-Path -Parent $sourceRoot))
$candidateRoot = Join-Path $workspaceRoot 'NewSamgukji_remote_V3'
$historyRoot = Join-Path $sourceRoot 'verification\development-scripts'
New-Item -ItemType Directory -Path $historyRoot -Force | Out-Null
foreach ($name in @('stabilize_v3.py','finish_v3.py','refine_v3.py','correct_surface_v3.py','record_v3.py')) {
    $fromPath = [IO.Path]::GetFullPath((Join-Path $sourceRoot ('tools\' + $name)))
    $copyPath = [IO.Path]::GetFullPath((Join-Path $candidateRoot ('tools\' + $name)))
    if (-not $fromPath.StartsWith($workspaceRoot + '\') -or -not $copyPath.StartsWith($workspaceRoot + '\')) { throw 'Outside workspace' }
    if (Test-Path -LiteralPath $fromPath) { Move-Item -LiteralPath $fromPath -Destination (Join-Path $historyRoot $name) -Force }
    if (Test-Path -LiteralPath $copyPath) { Remove-Item -LiteralPath $copyPath }
}
