# reflect-yourself installer for Cursor (Windows PowerShell)
# Installs to ~/.cursor/skills/ for global availability

$ErrorActionPreference = "Stop"

$RepoUrl = "https://raw.githubusercontent.com/maorfsdev/reflect-yourself/main"
$Dest = "$env:USERPROFILE\.cursor\skills\reflect-yourself"

Write-Host ""
Write-Host "reflect-yourself installer" -ForegroundColor Cyan
Write-Host "==========================" -ForegroundColor Cyan
Write-Host ""

# Check if running from local clone or remote
$ScriptDir = if ($MyInvocation.MyCommand.Path) { Split-Path -Parent $MyInvocation.MyCommand.Path } else { $null }

# Create destination directories
New-Item -ItemType Directory -Force -Path "$Dest\commands" | Out-Null
New-Item -ItemType Directory -Force -Path "$Dest\rules" | Out-Null

if ($ScriptDir -and (Test-Path "$ScriptDir\SKILL.md")) {
    # Local install - copy from cloned repo
    Write-Host "Installing from local files..."
    Copy-Item "$ScriptDir\SKILL.md" "$Dest\" -Force
    Copy-Item "$ScriptDir\commands\*" "$Dest\commands\" -Force
    Copy-Item "$ScriptDir\rules\*" "$Dest\rules\" -Force
} else {
    # Remote install - download from GitHub
    Write-Host "Downloading from GitHub..."
    Invoke-WebRequest -Uri "$RepoUrl/SKILL.md" -OutFile "$Dest\SKILL.md"
    Invoke-WebRequest -Uri "$RepoUrl/commands/reflect-yourself.md" -OutFile "$Dest\commands\reflect-yourself.md"
    Invoke-WebRequest -Uri "$RepoUrl/commands/reflect-yourself-skills.md" -OutFile "$Dest\commands\reflect-yourself-skills.md"
    Invoke-WebRequest -Uri "$RepoUrl/commands/reflect-yourself-queue.md" -OutFile "$Dest\commands\reflect-yourself-queue.md"
    Invoke-WebRequest -Uri "$RepoUrl/commands/reflect-yourself-skip.md" -OutFile "$Dest\commands\reflect-yourself-skip.md"
    Invoke-WebRequest -Uri "$RepoUrl/rules/session-reflect.mdc" -OutFile "$Dest\rules\session-reflect.mdc"
}

# Create empty queue file if it doesn't exist
$QueueFile = "$env:USERPROFILE\.cursor\reflect-queue.json"
if (-not (Test-Path $QueueFile)) {
    '{"version": 1, "learnings": []}' | Out-File -FilePath $QueueFile -Encoding utf8
    Write-Host "Created queue file at $QueueFile"
}

Write-Host ""
Write-Host "Installed to $Dest" -ForegroundColor Green
Write-Host ""
Write-Host "The skill is now available in ALL your Cursor projects."
Write-Host ""
Write-Host "Commands:" -ForegroundColor Yellow
Write-Host "  /reflect-yourself        - Capture learnings from session"
Write-Host "  /reflect-yourself-skills - Discover skill patterns"
Write-Host "  /reflect-yourself-queue  - View pending learnings"
Write-Host "  /reflect-yourself-skip   - Clear the queue"
Write-Host ""
Write-Host "Run /reflect-yourself at the end of your sessions!"
Write-Host ""
