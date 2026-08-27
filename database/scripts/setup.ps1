# setup.ps1 — Create database (if needed), apply schema, load seeds
# Usage:  .\database\scripts\setup.ps1
# Requires: psql on PATH, .env or $env:DATABASE_URL
param()
$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$envFile = Join-Path $root ".env"
if (Test-Path $envFile) { Get-Content $envFile | Where-Object { $_ -match "=" -and $_ -notmatch "^\s*#" } | ForEach-Object { $k,$v=$_.Split("=",2); Set-Item -Path "env:$($k.Trim())" -Value $v.Trim() } }
if (-not $env:DATABASE_URL) { $env:DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/swarm_lending" }
Write-Host "DATABASE_URL=$env:DATABASE_URL" -ForegroundColor Cyan

# Try create DB (ignore if exists)
try { psql $env:DATABASE_URL -c "SELECT 1" 2>&1 | Out-Null } catch {}
if ($LASTEXITCODE -ne 0) {
  $base = $env:DATABASE_URL -replace "/[^/]*$","/postgres"
  Write-Host "Creating database swarm_lending..." -ForegroundColor Yellow
  psql $base -c "CREATE DATABASE swarm_lending;" 2>&1 | Write-Host
}

$schemaOrder = @("001_extensions.sql","002_types.sql","003_tables.sql","004_relationships.sql","005_indexes.sql","006_constraints.sql","007_views.sql")
foreach ($f in $schemaOrder) {
  $path = Join-Path $PSScriptRoot "..\schema\$f"
  Write-Host "Applying schema/$f ..." -ForegroundColor Green
  psql $env:DATABASE_URL -f $path
  if ($LASTEXITCODE -ne 0) { throw "Failed: $f" }
}
Get-ChildItem (Join-Path $PSScriptRoot "..\seeds\*.sql") | Sort-Object Name | ForEach-Object {
  Write-Host "Seeding $($_.Name) ..." -ForegroundColor Green
  psql $env:DATABASE_URL -f $_.FullName
  if ($LASTEXITCODE -ne 0) { throw "Failed: $($_.Name)" }
}
Write-Host "Setup complete." -ForegroundColor Cyan
