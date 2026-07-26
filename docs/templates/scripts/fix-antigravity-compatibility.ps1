# Fix Antigravity IDE Compatibility for All Python MCP Servers
# Applies the binary mode stdio fix to prevent "invalid trailing data" errors

param(
    [string]$ReposPath = "D:\Dev\repos",
    [switch]$DryRun
)

$ErrorActionPreference = "Stop"

Write-Host "🔧 Antigravity IDE Compatibility Fix" -ForegroundColor Cyan
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host ""

if ($DryRun) {
    Write-Host "🔍 DRY RUN MODE - No files will be modified" -ForegroundColor Yellow
    Write-Host ""
}

# Pattern to find MCP server entry points
$patterns = @(
    "**/mcp/server.py",
    "**/mcp/__main__.py",
    "**/mcp_instance.py",
    "**/server.py"
)

# Fix code to inject
$fixCode = @"
# CRITICAL: Set stdio to binary mode on Windows for Antigravity IDE compatibility
# Antigravity IDE is strict about JSON-RPC protocol and interprets trailing \r as "invalid trailing data"
# Binary mode prevents Python from automatically converting line endings
if os.name == 'nt':  # Windows
    try:
        import msvcrt
        # Set stdin/stdout to binary mode to prevent line ending conversion
        # This fixes "invalid trailing data" errors with Antigravity IDE
        msvcrt.setmode(sys.stdin.fileno(), os.O_BINARY)
        msvcrt.setmode(sys.stdout.fileno(), os.O_BINARY)
    except (ImportError, OSError):
        # If msvcrt is not available or setting fails, continue without it
        # This might happen in some environments, but it's not critical
        pass
"@

$fixedCount = 0
$skippedCount = 0
$errorCount = 0

# Find all Python MCP server files
$files = Get-ChildItem -Path $ReposPath -Include $patterns -Recurse -File | 
    Where-Object { 
        $_.FullName -notmatch "node_modules|\.venv|venv|__pycache__|\.git|dist|build" -and
        $_.Extension -eq ".py"
    }

Write-Host "Found $($files.Count) potential MCP server files" -ForegroundColor Green
Write-Host ""

foreach ($file in $files) {
    $relativePath = $file.FullName.Replace($ReposPath + "\", "")
    Write-Host "Processing: $relativePath" -ForegroundColor Gray
    
    try {
        $content = Get-Content $file.FullName -Raw -Encoding UTF8
        
        # Skip if already has the fix
        if ($content -match "msvcrt\.setmode") {
            Write-Host "  ⏭️  Already fixed, skipping" -ForegroundColor Yellow
            $skippedCount++
            continue
        }
        
        # Check if it's actually an MCP server file
        if ($content -notmatch "(FastMCP|mcp\.tool|server\.run|@mcp\.tool)") {
            Write-Host "  ⏭️  Not an MCP server file, skipping" -ForegroundColor Yellow
            $skippedCount++
            continue
        }
        
        # Find the insertion point (after imports, before other code)
        $lines = $content -split "`n"
        $insertIndex = -1
        
        # Look for the right place to insert (after sys/os imports, before other code)
        for ($i = 0; $i -lt [Math]::Min(30, $lines.Length); $i++) {
            $line = $lines[$i]
            
            # Check if we've imported sys and os
            if ($line -match "^\s*import\s+(sys|os)\s*$" -or $line -match "^\s*from\s+(sys|os)\s+import") {
                # Look for the next non-import, non-comment line
                for ($j = $i + 1; $j -lt [Math]::Min($i + 10, $lines.Length); $j++) {
                    $nextLine = $lines[$j].Trim()
                    if ($nextLine -and $nextLine -notmatch "^(import|from|#|$)") {
                        $insertIndex = $j
                        break
                    }
                }
                if ($insertIndex -ge 0) {
                    break
                }
            }
        }
        
        if ($insertIndex -lt 0) {
            # Fallback: insert after first 5 lines
            $insertIndex = 5
        }
        
        if (-not $DryRun) {
            # Insert the fix code
            $newLines = @()
            $newLines += $lines[0..($insertIndex - 1)]
            $newLines += ""
            $newLines += $fixCode -split "`n"
            $newLines += ""
            $newLines += $lines[$insertIndex..($lines.Length - 1)]
            
            $newContent = $newLines -join "`n"
            Set-Content -Path $file.FullName -Value $newContent -Encoding UTF8 -NoNewline
            Write-Host "  ✅ Fixed!" -ForegroundColor Green
        } else {
            Write-Host "  🔍 Would fix (dry run)" -ForegroundColor Cyan
        }
        
        $fixedCount++
        
    } catch {
        Write-Host "  ❌ Error: $_" -ForegroundColor Red
        $errorCount++
    }
}

Write-Host ""
Write-Host "=====================================" -ForegroundColor Cyan
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "  Fixed: $fixedCount" -ForegroundColor Green
Write-Host "  Skipped: $skippedCount" -ForegroundColor Yellow
Write-Host "  Errors: $errorCount" -ForegroundColor $(if ($errorCount -gt 0) { "Red" } else { "Green" })
Write-Host ""

if ($DryRun) {
    Write-Host "Run without -DryRun to apply fixes" -ForegroundColor Yellow
} else {
    Write-Host "✅ Fix applied! Restart Antigravity IDE to test." -ForegroundColor Green
}

