$ErrorActionPreference = "Continue"

$checks = @(
  @{ Name = "Java"; Command = "java"; Args = @("-version"); MinimumMajor = 17 },
  @{ Name = "Maven"; Command = "mvn"; Args = @("-version"); MinimumMajor = $null },
  @{ Name = "Node.js"; Command = "node"; Args = @("--version"); MinimumMajor = 18 },
  @{ Name = "npm"; Command = "npm"; Args = @("--version"); MinimumMajor = 9 },
  @{ Name = "Python"; Command = "python"; Args = @("--version"); MinimumMajor = 3 }
)

Write-Host "CampusHub Testing Lab local environment check"
Write-Host ""

$missing = @()
$warnings = @()
foreach ($check in $checks) {
  $cmd = Get-Command $check.Command -ErrorAction SilentlyContinue
  if ($null -eq $cmd) {
    Write-Host "[MISSING] $($check.Name): command not found ($($check.Command))"
    $missing += $check.Name
    continue
  }

  $output = & $check.Command @($check.Args) 2>&1 | Select-Object -First 1
  $versionMatch = [regex]::Match([string]$output, "v?`"?(\d+)")
  if ($null -ne $check.MinimumMajor -and $versionMatch.Success -and [int]$versionMatch.Groups[1].Value -lt [int]$check.MinimumMajor) {
    Write-Host "[WARN] $($check.Name): $output (recommended >= $($check.MinimumMajor))"
    $warnings += $check.Name
  } else {
    Write-Host "[OK] $($check.Name): $output"
  }
}

Write-Host ""
if ($missing.Count -gt 0) {
  Write-Host "Missing tools: $($missing -join ', ')"
  Write-Host "Install the missing tools first, then run this script again."
  exit 1
}

if ($warnings.Count -gt 0) {
  Write-Host "Warnings: $($warnings -join ', ')"
  Write-Host "These tools are available, but the project recommends newer versions."
  Write-Host ""
}

Write-Host "Next steps:"
Write-Host "1. cd backend; mvn spring-boot:run"
Write-Host "2. cd frontend; npm install; npm run dev"
Write-Host "3. Open http://localhost:5173 and log in with student01 / campus123"
