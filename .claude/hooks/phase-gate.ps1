# PreToolUse hook: enforces the phase-approval gate before a Write/Edit to a docs/*.md phase
# artifact, and before `gh pr create`. Reads the tool-call JSON from stdin (Claude Code's
# PreToolUse hook contract). Exit 0 = allow. Exit 2 = block (stderr is surfaced to Claude/user).

$ErrorActionPreference = "Stop"

$raw = [Console]::In.ReadToEnd()
if ([string]::IsNullOrWhiteSpace($raw)) { exit 0 }

try {
    $data = $raw | ConvertFrom-Json
} catch {
    exit 0
}

$toolName = $data.tool_name
$toolInput = $data.tool_input

$statusPath = Join-Path (Get-Location) "docs\pipeline-status.json"
if (-not (Test-Path $statusPath)) { exit 0 }
$status = Get-Content $statusPath -Raw | ConvertFrom-Json

function Get-Decision([int]$phaseNum) {
    $phase = $status.phases | Where-Object { $_.n -eq $phaseNum }
    if ($null -eq $phase) { return $null }
    return $phase.decision
}

function Block([string]$message) {
    [Console]::Error.WriteLine($message)
    exit 2
}

# Map a docs/*.md artifact (or the coding-standards file written alongside architecture.md) to
# the phase that owns it and the phase that must already be APPROVED before it may be written.
$artifactGate = @{
    "docs/architecture.md"             = 1
    ".claude/instructions/coding.md"   = 1
    "docs/design-review.md"            = 2
    "docs/impl-plan.md"                = 3
    "docs/review-notes.md"             = 5
    "docs/verification-report.md"      = 6
}

if ($toolName -eq "Write" -or $toolName -eq "Edit") {
    $filePath = $toolInput.file_path
    if ($null -ne $filePath) {
        $normalized = ($filePath -replace '\\', '/')
        foreach ($artifact in $artifactGate.Keys) {
            if ($normalized -like "*$artifact") {
                $requiredPhase = $artifactGate[$artifact]
                $decision = Get-Decision $requiredPhase
                if ($decision -ne "APPROVED") {
                    Block "Blocked: phase $requiredPhase must be APPROVED (run /approve-phase $requiredPhase APPROVED) before writing $artifact."
                }
            }
        }
    }
}

if ($toolName -eq "Bash") {
    $command = $toolInput.command
    if ($null -ne $command -and $command -match "gh\s+pr\s+create") {
        $decision = Get-Decision 7
        if ($decision -ne "APPROVED") {
            Block "Blocked: phase 7 (verify) must be APPROVED (run /approve-phase 7 APPROVED) before creating a PR."
        }
    }
}

exit 0
