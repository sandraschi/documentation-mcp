# Allowed Emoji Test Script
# Tests rendering of all permitted emojis per cursor rules

Write-Host "`n=== ALLOWED EMOJI TEST ===" -ForegroundColor Cyan
Write-Host "If any emoji shows as boxes/?, terminal font needs updating`n"

Write-Host "STATUS:" -ForegroundColor Yellow
Write-Host "  âœ... Check (success)    âŒ Cross (failure)    âš ï¸ Warning"
Write-Host "  âœ" Light check        âœ- Light cross"

Write-Host "`nDOCUMENTS:" -ForegroundColor Yellow  
Write-Host "  ðŸ"š Books    ðŸ" Folder    ðŸ"‹ Clipboard    ðŸ"¦ Package    ðŸ"Š Chart    ðŸ"„ Document"

Write-Host "`nACTIONS:" -ForegroundColor Yellow
Write-Host "  ðŸŽ¯ Target    ðŸš€ Rocket    ðŸ'¡ Lightbulb    ðŸ"- Link    ðŸ"§ Wrench    âš™ï¸ Gear"

Write-Host "`nDEVELOPMENT:" -ForegroundColor Yellow
Write-Host "  ðŸ› ï¸ Tools    ðŸ§ª Test tube    ðŸ-ï¸ Construction    ðŸ'» Laptop"

Write-Host "`nCELEBRATION:" -ForegroundColor Yellow
Write-Host "  âœ¨ Sparkles    ðŸŽ‰ Party    ðŸŽµ Music"

Write-Host "`nARROWS:" -ForegroundColor Yellow
Write-Host "  â-¶ Play    â-€ Back    â-² Up    â-¼ Down"
Write-Host "  â†' Right   â† Left    â†' Up    â†" Down"

Write-Host "`nOTHER:" -ForegroundColor Yellow
Write-Host "  ðŸ'ª Strength    ðŸ¤- Robot    ðŸŒ Globe    ðŸ'¬ Speech    ðŸ"' Lock    ðŸ"' Key"

Write-Host "`n=== TEST COMPLETE ===" -ForegroundColor Green
Write-Host "All above emojis are ALLOWED in code/scripts/docs"
Write-Host "Any OTHER emoji is FORBIDDEN`n" -ForegroundColor Red

