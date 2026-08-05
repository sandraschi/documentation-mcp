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
$Allowed = 'âœ...âŒâš ï¸âœ"âœ-ðŸ"šðŸ"ðŸ"‹ðŸ"¦ðŸ"ŠðŸ"„ðŸŽ¯ðŸš€ðŸ'¡ðŸ"-ðŸ"§âš™ï¸ðŸ› ï¸ðŸ§ªðŸ-ï¸ðŸ'»âœ¨ðŸŽ‰ðŸŽµâ-¶â-€â-²â-¼â†'â†â†'â†"ðŸ'ªðŸ¤-ðŸŒðŸ'¬ðŸ"'ðŸ"''

# Replacement table: illegal emoji -> meaningful text
# NOTE: This file excludes itself from scanning to preserve this table!
$ReplacementTable = @{
    # Search/View
    'ðŸ"' = '[search]'
    'ðŸ'' = '[view]'
    'ðŸ'€' = '[look]'
    
    # Status indicators
    'ðŸ"´' = '[red]'
    'ðŸŸ¡' = '[yellow]'
    'ðŸŸ¢' = '[green]'
    'ðŸ"µ' = '[blue]'
    'âšª' = '[white]'
    'âš«' = '[black]'
    'ðŸŸ ' = '[orange]'
    'ðŸŸ£' = '[purple]'
    
    # Alerts/Warnings
    'ðŸš¨' = '[alert]'
    'ðŸš«' = '[prohibited]'
    'â›"' = '[stop]'
    'ðŸ›'' = '[stop]'
    'âš¡' = '[fast]'
    'ðŸ'¥' = '[impact]'
    
    # Actions
    'ðŸ"„' = '[sync]'
    'ðŸ"ƒ' = '[refresh]'
    'âž•' = '[add]'
    'âž-' = '[remove]'
    'âœï¸' = '[edit]'
    'ðŸ"' = '[note]'
    'ðŸ'¾' = '[save]'
    'ðŸ-'' = '[delete]'
    'ðŸ"¤' = '[upload]'
    'ðŸ"¥' = '[download]'
    
    # Development
    'ðŸ›' = '[bug]'
    'ðŸ' = '[python]'
    'ðŸ¦€' = '[rust]'
    'â˜•' = '[java]'
    'ðŸ'Ž' = '[ruby]'
    'ðŸ"¨' = '[build]'
    'ðŸ"©' = '[config]'
    'ðŸ§ ' = '[ai]'
    'ðŸ¤' = '[handshake]'
    'ðŸ"¥' = '[hot]'
    'ðŸ'°' = '[money]'
    'ðŸ"ˆ' = '[up]'
    'ðŸ"‰' = '[down]'
    'ðŸ"-' = '[docs]'
    'ðŸ†•' = '[new]'
    'ðŸ†š' = '[vs]'
    
    # Objects
    'ðŸŽ®' = '[game]'
    'ðŸŽ¨' = '[design]'
    'ðŸŽ¥' = '[video]'
    'ðŸŽ¹' = '[music]'
    'ðŸŽ²' = '[random]'
    'ðŸ-¼' = '[image]'
    'ðŸ"±' = '[mobile]'
    'ðŸ"ž' = '[call]'
    'ðŸ"¢' = '[announce]'
    'ðŸ•' = '[time]'
    'ðŸ-º' = '[map]'
    'ðŸ›¡' = '[shield]'
    'ðŸ"®' = '[predict]'
    
    # Achievement
    'ðŸ†' = '[trophy]'
    'ðŸ...' = '[medal]'
    'ðŸŒŸ' = '[star]'
    'â­' = '[star]'
    'ðŸŽ"' = '[graduate]'
    
    # DJ/Audio
    'ðŸŽ§' = '[headphones]'
    'ðŸŽ›' = '[mixer]'
    'ðŸŽš' = '[fader]'
    'ðŸŽ¶' = '[music]'
    'ðŸŽ™' = '[mic]'
    'ðŸ"€' = '[disc]'
    'ðŸ"Š' = '[speaker]'
    'ðŸ-¥' = '[screen]'
    'â¹' = '[stop]'
    'â¸' = '[pause]'
    'âº' = '[record]'
    'â­' = '[skip]'
    'â±' = '[timer]'
    'ðŸ‡¦' = ''  # Flag component (remove)
    'ðŸ‡¹' = ''  # Flag component (remove)
    
    # Misc
    'ðŸ'¶' = '[baby]'
    'ðŸ˜„' = '[smile]'
    'ðŸŽ­' = '[theater]'
    'ðŸ•' = '[pizza]'
    'ðŸº' = '[beer]'
    'ðŸ›' = '[bath]'
    'â˜€' = '[sun]'
    'ðŸ"¤' = '[text]'
    'ðŸ""' = '[unlock]'
    'ðŸ§¹' = '[clean]'
    'ðŸ"' = '[measure]'
}

Write-Host "`nðŸ" EMOJI BASH - Encoding Safety Scanner" -ForegroundColor Cyan
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
        Write-Host "âŒ $RelPath" -ForegroundColor Red
        Write-Host "   Illegal: $($UniqueIssues -join ' ') ($($FileIssues.Count) total)" -ForegroundColor DarkGray
        $TotalIssues += $FileIssues.Count
        
        if ($Fix -and ($Content -ne $OriginalContent)) {
            Set-Content -Path $File.FullName -Value $Content -NoNewline -Encoding UTF8
            Write-Host "   âœ... Fixed!" -ForegroundColor Green
            $FilesFixed++
        }
    }
}

# Summary
Write-Host ""
Write-Host "=" * 50
Write-Host "ðŸ"Š SUMMARY" -ForegroundColor Cyan
Write-Host "   Illegal emojis found: $TotalIssues" -ForegroundColor $(if ($TotalIssues -gt 0) { 'Red' } else { 'Green' })

if ($Fix -and $FilesFixed -gt 0) {
    Write-Host "   Files modified:       $FilesFixed" -ForegroundColor Yellow
}

if ($UnknownEmojis.Count -gt 0) {
    Write-Host ""
    Write-Host "âš ï¸ UNKNOWN EMOJIS (replaced with [?]):" -ForegroundColor Yellow
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
    Write-Host "âœ... All clear! No illegal emojis." -ForegroundColor Green
} elseif (-not $Fix) {
    Write-Host ""
    Write-Host "To fix, run:" -ForegroundColor Yellow
    Write-Host "   .\emoji-bash.ps1 -Fix" -ForegroundColor Cyan
}

Write-Host ""

# Show replacement table summary
if ($Fix) {
    Write-Host "Replacement examples:" -ForegroundColor DarkGray
    Write-Host "   ðŸ"â†'[search]  ðŸ"´â†'[red]  ðŸš¨â†'[alert]  ðŸ"â†'[note]  ðŸ›â†'[bug]" -ForegroundColor DarkGray
}
