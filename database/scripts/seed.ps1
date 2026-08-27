# seed.ps1 — Apply seeds only (assumes schema already loaded)
param()
$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$envFile = Join-Path $root ".env"
if (Test-Path $envFile) { Get-Content $envFile | Where-Object { $_ -match "=" -and $_ -notmatch "^\s*#" } | ForEach-Object { $k,$v=$_.Split("=",2); Set-Item -Path "env:$($k.Trim())" -Value $v.Trim() } }
if (-not $env:DATABASE_URL) { $env:DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/swarm_lending" }
Get-ChildItem (Join-Path $PSScriptRoot "..\seeds\*.sql") | Sort-Object Name | ForEach-Object {
  Write-Host "Seeding $($_.Name) ..." -ForegroundColor Green
  psql $env:DATABASE_URL -f $_.FullName
  if ($LASTEXITCODE -ne 0) { throw "Failed: $($_.Name)" }
}
Write-Host "Seeding complete." -ForegroundColor Cyan
