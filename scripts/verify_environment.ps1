# scripts/verify_environment.ps1
Write-Host "=== Sauti ya Mwananchi — Environment Verification ===" -ForegroundColor Cyan
Write-Host ""

$checks = @(
    @{ Name = "Python 3.12+";    Cmd = "python --version" },
    @{ Name = "pip";             Cmd = "pip --version" },
    @{ Name = "Git";             Cmd = "git --version" },
    @{ Name = "Google Cloud CLI";Cmd = "gcloud --version" },
    @{ Name = "Docker";          Cmd = "docker --version" },
    @{ Name = "ngrok";           Cmd = "ngrok --version" }
)

$failed = @()
foreach ($check in $checks) {
    try {
        $output = Invoke-Expression $check.Cmd 2>&1 | Select-Object -First 1
        Write-Host "[PASS] $($check.Name): $output" -ForegroundColor Green
    } catch {
        Write-Host "[FAIL] $($check.Name): NOT FOUND" -ForegroundColor Red
        $failed += $check.Name
    }
}

Write-Host ""
if ($failed.Count -eq 0) {
    Write-Host "All checks passed. Ready for Phase 0." -ForegroundColor Green
} else {
    $msg = "MISSING: " + ($failed -join ", ") + ". Install before proceeding."
    Write-Host $msg -ForegroundColor Red
}
