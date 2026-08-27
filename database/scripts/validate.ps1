# validate.ps1 — Verify 31 tables, relationships, seed counts
param()
$ErrorActionPreference = "Stop"
$root = Resolve-Path (Join-Path $PSScriptRoot "..\..")
$envFile = Join-Path $root ".env"
if (Test-Path $envFile) { Get-Content $envFile | Where-Object { $_ -match "=" -and $_ -notmatch "^\s*#" } | ForEach-Object { $k,$v=$_.Split("=",2); Set-Item -Path "env:$($k.Trim())" -Value $v.Trim() } }
if (-not $env:DATABASE_URL) { $env:DATABASE_URL = "postgresql://postgres:postgres@localhost:5432/swarm_lending" }

function q($sql){ psql $env:DATABASE_URL -t -A -c $sql }

Write-Host "`n=== Table count ===" -ForegroundColor Cyan
q "SELECT count(*) FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE';"

Write-Host "`n=== All tables ===" -ForegroundColor Cyan
q "SELECT table_name FROM information_schema.tables WHERE table_schema='public' AND table_type='BASE TABLE' ORDER BY table_name;"

Write-Host "`n=== Row counts ===" -ForegroundColor Cyan
$tables = @("customers","mobile_numbers","addresses","bank_accounts","devices","ip_addresses","dealers","loan_applications","loans","guarantors","payments","locations","application_events","entity_relationships","fraud_signals","risk_scores","fraud_clusters","fraud_cluster_members","fraud_alerts","investigations","investigation_actions","model_versions","predictions","audit_logs","customer_mobile_links","customer_address_links","customer_bank_links","customer_device_links","dealer_customer_links","loan_guarantors","repayment_behaviour")
foreach($t in $tables){ $c=q "SELECT count(*) FROM $t;"; Write-Host ("{0,-28} {1}" -f $t,$c) }

Write-Host "`n=== Cluster F-1001 check ===" -ForegroundColor Cyan
q "SELECT cluster_ref, member_count, cluster_status, risk_score FROM fraud_clusters WHERE cluster_ref='F-1001';"
q "SELECT fcm.entity_type, count(*) FROM fraud_cluster_members fcm JOIN fraud_clusters fc ON fc.cluster_id=fcm.cluster_id WHERE fc.cluster_ref='F-1001' GROUP BY fcm.entity_type ORDER BY fcm.entity_type;"

Write-Host "`n=== Views ===" -ForegroundColor Cyan
q "SELECT table_name FROM information_schema.views WHERE table_schema='public' ORDER BY table_name;"

Write-Host "`n=== Integrity: invalid FK sample (should be 0) ===" -ForegroundColor Cyan
q "SELECT count(*) AS orphan_apps FROM loan_applications la LEFT JOIN customers c ON c.customer_id=la.customer_id WHERE c.customer_id IS NULL;"
q "SELECT count(*) AS orphan_payments FROM payments p LEFT JOIN loans l ON l.loan_id=p.loan_id WHERE l.loan_id IS NULL;"

Write-Host "`nValidation done." -ForegroundColor Cyan
