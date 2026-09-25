# PreToolUse hook: blocks `git commit` if the staged diff contains a likely secret. This is a
# backstop, not a substitute for care — see CLAUDE.md's Security section. Reads the tool-call
# JSON from stdin. Exit 0 = allow. Exit 2 = block (stderr surfaced to Claude/user).

$ErrorActionPreference = "Stop"

$raw = [Console]::In.ReadToEnd()
if ([string]::IsNullOrWhiteSpace($raw)) { exit 0 }

try {
    $data = $raw | ConvertFrom-Json
} catch {
    exit 0
}

if ($data.tool_name -ne "Bash") { exit 0 }
$command = $data.tool_input.command
if ($null -eq $command -or $command -notmatch "git\s+commit") { exit 0 }

$diff = git diff --cached 2>$null
if ([string]::IsNullOrWhiteSpace($diff)) { exit 0 }

$patterns = @(
    "AKIA[0-9A-Z]{16}",
    "-----BEGIN [A-Z ]*PRIVATE KEY-----",
    "(?i)api[_-]?key\s*=\s*['""][A-Za-z0-9_\-]{16,}['""]",
    "(?i)secret[_-]?key\s*=\s*['""][A-Za-z0-9_\-/+]{16,}['""]",
    "(?i)password\s*=\s*['""][^'""]{8,}['""]",
    "gh[pousr]_[A-Za-z0-9]{20,}",
    "xox[baprs]-[A-Za-z0-9-]{10,}"
)

foreach ($pattern in $patterns) {
    if ($diff -match $pattern) {
        [Console]::Error.WriteLine("Blocked: staged diff matches a likely secret pattern ($pattern). Remove it and use an environment variable instead (see CLAUDE.md Security section).")
        exit 2
    }
}

exit 0
