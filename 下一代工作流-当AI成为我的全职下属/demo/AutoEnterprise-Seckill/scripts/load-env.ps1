param(
    [string]$Path = ".env"
)

if (-not (Test-Path -LiteralPath $Path)) {
    throw "Environment file not found: $Path"
}

Get-Content -LiteralPath $Path | ForEach-Object {
    $line = $_.Trim()
    if (-not $line -or $line.StartsWith("#") -or -not $line.Contains("=")) {
        return
    }

    $name, $value = $line -split "=", 2
    $name = $name.Trim()
    $value = $value.Trim().Trim('"').Trim("'")

    if ($name) {
        Set-Item -Path "Env:$name" -Value $value
    }
}
