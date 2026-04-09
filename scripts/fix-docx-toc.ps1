# Fix DOCX TOC - Convert to clickable static hyperlinks
# The hyperlinks have SubAddress (bookmark) but empty TextToDisplay
# We need to get the text from Range.Text instead

param(
    [Parameter(Mandatory=$true)]
    [string]$DocxPath
)

$ErrorActionPreference = "Stop"

$DocxPath = (Resolve-Path $DocxPath).Path
Write-Host "Processing: $DocxPath" -ForegroundColor Cyan

$word = New-Object -ComObject Word.Application
$word.Visible = $false
$word.DisplayAlerts = 0

try {
    $doc = $word.Documents.Open($DocxPath, $false, $false, $false)
    
    if ($doc.TablesOfContents.Count -gt 0) {
        Write-Host "Found TOC" -ForegroundColor Yellow
        
        $toc = $doc.TablesOfContents.Item(1)
        $toc.Update()
        
        $tocStart = $toc.Range.Start
        $tocEnd = $toc.Range.End
        
        # Collect hyperlinks - use Range.Text instead of TextToDisplay
        $linkMap = @{}
        $allLinks = @($doc.Hyperlinks)
        
        foreach ($h in $allLinks) {
            $bookmark = $h.SubAddress
            if ($bookmark -and $bookmark -match "^_Toc") {
                # Get text from the range itself
                $text = $h.Range.Text.Trim()
                # Remove page numbers and tabs
                $text = $text -replace '\t.*$', ''
                $text = $text.Trim()
                if ($text) {
                    $linkMap[$text] = $bookmark
                }
            }
        }
        
        Write-Host "Found $($linkMap.Count) TOC entries" -ForegroundColor Green
        
        if ($linkMap.Count -gt 0) {
            # Show some examples
            $examples = $linkMap.GetEnumerator() | Select-Object -First 3
            foreach ($ex in $examples) {
                Write-Host "  '$($ex.Key)' -> $($ex.Value)" -ForegroundColor DarkGray
            }
            
            # Unlink TOC fields (converts to static text)
            $toc.Range.Fields.Unlink()
            
            # Re-add hyperlinks by finding text in TOC area
            $restored = 0
            
            foreach ($entry in $linkMap.GetEnumerator()) {
                # Create fresh search range for each search
                $searchRange = $doc.Range($tocStart, $tocEnd)
                $searchRange.Find.ClearFormatting()
                
                $found = $searchRange.Find.Execute(
                    $entry.Key,  # FindText
                    $false,      # MatchCase
                    $true,       # MatchWholeWord
                    $false,      # MatchWildcards
                    $false,      # MatchSoundsLike
                    $false,      # MatchAllWordForms
                    $true,       # Forward
                    1,           # Wrap (wdFindStop)
                    $false,      # Format
                    "",          # ReplaceWith
                    0            # Replace (wdReplaceNone)
                )
                
                if ($found) {
                    try {
                        $doc.Hyperlinks.Add($searchRange, "", $entry.Value) | Out-Null
                        $restored++
                    } catch {
                        Write-Host "  Failed: $($entry.Key)" -ForegroundColor DarkYellow
                    }
                }
            }
            
            Write-Host "Restored $restored / $($linkMap.Count) hyperlinks" -ForegroundColor Green
        } else {
            Write-Host "No TOC links found" -ForegroundColor Yellow
            $toc.Range.Fields.Unlink()
        }
        
        $doc.Save()
        Write-Host "SUCCESS!" -ForegroundColor Green
    } else {
        Write-Host "No TOC found" -ForegroundColor Yellow
    }
}
catch {
    Write-Host "ERROR: $($_.Exception.Message)" -ForegroundColor Red
    throw
}
finally {
    if ($doc) { 
        $doc.Close($false) 
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($doc) | Out-Null
    }
    if ($word) { 
        $word.Quit() 
        [System.Runtime.InteropServices.Marshal]::ReleaseComObject($word) | Out-Null
    }
    [GC]::Collect()
    [GC]::WaitForPendingFinalizers()
}
