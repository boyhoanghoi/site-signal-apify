param([int]$Port = 8765)
$projectPath = Split-Path -Parent $PSScriptRoot
$pythonPath = Join-Path $projectPath '.venv\Scripts\python.exe'
if (-not (Test-Path -LiteralPath $pythonPath)) { $pythonPath = 'python' }
& $pythonPath -m http.server $Port --bind 127.0.0.1 --directory (Join-Path $projectPath 'dist')
