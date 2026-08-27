# reset.ps1 — Drop and recreate public schema (destructive)
param()
$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$envFile = Join-Path $root ".env"
if (Test-Path $envFile) { Get-Content $envFile | Where-Object { $_ -match "=" -and $_ -notmatch "^\s*#" } | ForEach-Object { $k,$v=$_.Split("=",2); Set-Item -Path "env:$($k.Trim())" -Value $v.Trim() } }
if (-not $env:DATABASE_URL) { $env:DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/swarm_lending" }
Write-Host "Resetting database (DROP SCHEMA public CASCADE) ..." -ForegroundColor Yellow
psql $env:DATABASE_URL -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public; GRANT ALL ON SCHEMA public TO postgres; GRANT ALL ON SCHEMA public TO public;"
Write-Host "Reset done. Run setup.ps1 or seed.ps1 next." -ForegroundColor Cyan
