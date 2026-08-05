# CPU full doc reindex - venv python (not uv run while GPU mode active).
$ErrorActionPreference = "Stop"
$RepoRoot = Split-Path $PSScriptRoot -Parent
Set-Location $RepoRoot
$py = & (Join-Path $PSScriptRoot "rag-python.ps1")
& $py scripts/rag_reindex.py
exit $LASTEXITCODE
