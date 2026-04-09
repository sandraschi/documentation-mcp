<#
.SYNOPSIS
    Emoji Bash - Find and replace illegal emojis in CODE files (not markdown)

.PARAMETER Fix
    Replace illegal emojis with text equivalents (default: report only)

.PARAMETER Path
    Directory to scan (default: current directory)

.EXAMPLE
    .\emoji-bash.ps1           # Report only
    .\emoji-bash.ps1 -Fix      # Replace emojis with text equivalents
#>

param(
    [switch]$Fix,
    [string]$Path = "."
)

# Allowed emojis (from cursor rules) - these render safely everywhere
$Allowed = '✅❌⚠️✓✗📚📁📋📦📊📄🎯🚀💡🔗🔧⚙️🛠️🧪🏗️💻✨🎉🎵▶◀▲▼→←↑↓💪🤖🌐💬🔒🔑'

# Replacement table: illegal emoji -> meaningful text
# NOTE: This file excludes itself from scanning to preserve this table!
$ReplacementTable = @{
    # Search/View
    '🔍' = '[search]'
    '👁' = '[view]'
    '👀' = '[look]'
    
    # Status indicators
    '🔴' = '[red]'
    '🟡' = '[yellow]'
    '🟢' = '[green]'
    '🔵' = '[blue]'
    '⚪' = '[white]'
    '⚫' = '[black]'
    '🟠' = '[orange]'
    '🟣' = '[purple]'
    
    # Alerts/Warnings
    '🚨' = '[alert]'
    '🚫' = '[prohibited]'
    '⛔' = '[stop]'
    '🛑' = '[stop]'
    '⚡' = '[fast]'
    '💥' = '[impact]'
    
    # Actions
    '🔄' = '[sync]'
    '🔃' = '[refresh]'
    '➕' = '[add]'
    '➖' = '[remove]'
    '✏️' = '[edit]'
    '📝' = '[note]'
    '💾' = '[save]'
    '🗑' = '[delete]'
    '📤' = '[upload]'
    '📥' = '[download]'
    
    # Development
    '🐛' = '[bug]'
    '🐍' = '[python]'
    '🦀' = '[rust]'
    '☕' = '[java]'
    '💎' = '[ruby]'
    '🔨' = '[build]'
    '🔩' = '[config]'
    '🧠' = '[ai]'
    '🤝' = '[handshake]'
    '🔥' = '[hot]'
    '💰' = '[money]'
    '📈' = '[up]'
    '📉' = '[down]'
    '📖' = '[docs]'
    '🆕' = '[new]'
    '🆚' = '[vs]'
    
    # Objects
    '🎮' = '[game]'
    '🎨' = '[design]'
    '🎥' = '[video]'
    '🎹' = '[music]'
    '🎲' = '[random]'
    '🖼' = '[image]'
    '📱' = '[mobile]'
    '📞' = '[call]'
    '📢' = '[announce]'
    '🕐' = '[time]'
    '🗺' = '[map]'
    '🛡' = '[shield]'
    '🔮' = '[predict]'
    
    # Achievement
    '🏆' = '[trophy]'
    '🏅' = '[medal]'
    '🌟' = '[star]'
    '⭐' = '[star]'
    '🎓' = '[graduate]'
    
    # DJ/Audio
    '🎧' = '[headphones]'
    '🎛' = '[mixer]'
    '🎚' = '[fader]'
    '🎶' = '[music]'
    '🎙' = '[mic]'
    '📀' = '[disc]'
    '🔊' = '[speaker]'
    '🖥' = '[screen]'
    '⏹' = '[stop]'
    '⏸' = '[pause]'
    '⏺' = '[record]'
    '⏭' = '[skip]'
    '⏱' = '[timer]'
    '🇦' = ''  # Flag component (remove)
    '🇹' = ''  # Flag component (remove)
    
    # Misc
    '👶' = '[baby]'
    '😄' = '[smile]'
    '🎭' = '[theater]'
    '🍕' = '[pizza]'
    '🍺' = '[beer]'
    '🛁' = '[bath]'
    '☀' = '[sun]'
    '🔤' = '[text]'
    '🔓' = '[unlock]'
    '🧹' = '[clean]'
    '📏' = '[measure]'
}

Write-Host "`n🔍 EMOJI BASH - Encoding Safety Scanner" -ForegroundColor Cyan
Write-Host "=" * 50
Write-Host "Mode: $(if ($Fix) { 'FIX (replace with text)' } else { 'REPORT ONLY' })" -ForegroundColor $(if ($Fix) { 'Yellow' } else { 'Cyan' })
Write-Host ""

$TotalIssues = 0
$FilesFixed = 0
$UnknownEmojis = @{}

# Scan CODE files only (not markdown - browsers render all emojis fine)
# Exclude self to avoid destroying the replacement table!
$Files = Get-ChildItem -Path $Path -Include @("*.ps1", "*.py", "*.sh", "*.bat", "*.cmd") -Recurse -ErrorAction SilentlyContinue | 
    Where-Object { 
        $_.FullName -notmatch '[\\/](\.git|node_modules|__pycache__|\.venv|backups)[\\/]' -and
        $_.Name -ne 'emoji-bash.ps1'
    }

foreach ($File in $Files) {
    $Content = Get-Content $File.FullName -Raw -ErrorAction SilentlyContinue
    if (-not $Content) { continue }
    
    $OriginalContent = $Content
    $FileIssues = @()
    
    # Find emoji-like characters
    $Matches = [regex]::Matches($Content, '[\uD83C-\uDBFF][\uDC00-\uDFFF]|[\u2600-\u27BF]|[\u2300-\u23FF]')
    
    foreach ($Match in $Matches) {
        $E = $Match.Value
        if ($Allowed -notmatch [regex]::Escape($E)) {
            $FileIssues += $E
            
            if ($Fix) {
                # Look up replacement or use generic
                if ($ReplacementTable.ContainsKey($E)) {
                    $Replacement = $ReplacementTable[$E]
                } else {
                    $Replacement = '[?]'
                    # Track unknown emojis
                    if (-not $UnknownEmojis.ContainsKey($E)) {
                        $UnknownEmojis[$E] = 0
                    }
                    $UnknownEmojis[$E]++
                }
                $Content = $Content.Replace($E, $Replacement)
            }
        }
    }
    
    if ($FileIssues.Count -gt 0) {
        $RelPath = $File.FullName.Replace((Resolve-Path $Path).Path, '').TrimStart('\', '/')
        $UniqueIssues = $FileIssues | Sort-Object -Unique
        Write-Host "❌ $RelPath" -ForegroundColor Red
        Write-Host "   Illegal: $($UniqueIssues -join ' ') ($($FileIssues.Count) total)" -ForegroundColor DarkGray
        $TotalIssues += $FileIssues.Count
        
        if ($Fix -and ($Content -ne $OriginalContent)) {
            Set-Content -Path $File.FullName -Value $Content -NoNewline -Encoding UTF8
            Write-Host "   ✅ Fixed!" -ForegroundColor Green
            $FilesFixed++
        }
    }
}

# Summary
Write-Host ""
Write-Host "=" * 50
Write-Host "📊 SUMMARY" -ForegroundColor Cyan
Write-Host "   Illegal emojis found: $TotalIssues" -ForegroundColor $(if ($TotalIssues -gt 0) { 'Red' } else { 'Green' })

if ($Fix -and $FilesFixed -gt 0) {
    Write-Host "   Files modified:       $FilesFixed" -ForegroundColor Yellow
}

if ($UnknownEmojis.Count -gt 0) {
    Write-Host ""
    Write-Host "⚠️ UNKNOWN EMOJIS (replaced with [?]):" -ForegroundColor Yellow
    Write-Host "   Add these to ReplacementTable in script:" -ForegroundColor DarkGray
    foreach ($E in $UnknownEmojis.Keys) {
        $CodePoint = [int][char]$E[0]
        if ($E.Length -gt 1) {
            $CodePoint = "surrogate"
        }
        Write-Host "   '$E' = '[???]'  # $($UnknownEmojis[$E]) occurrences"
    }
}

if ($TotalIssues -eq 0) {
    Write-Host ""
    Write-Host "✅ All clear! No illegal emojis." -ForegroundColor Green
} elseif (-not $Fix) {
    Write-Host ""
    Write-Host "To fix, run:" -ForegroundColor Yellow
    Write-Host "   .\emoji-bash.ps1 -Fix" -ForegroundColor Cyan
}

Write-Host ""

# Show replacement table summary
if ($Fix) {
    Write-Host "Replacement examples:" -ForegroundColor DarkGray
    Write-Host "   🔍→[search]  🔴→[red]  🚨→[alert]  📝→[note]  🐛→[bug]" -ForegroundColor DarkGray
}
