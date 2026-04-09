# Allowed Emoji Test Script
# Tests rendering of all permitted emojis per cursor rules

Write-Host "`n=== ALLOWED EMOJI TEST ===" -ForegroundColor Cyan
Write-Host "If any emoji shows as boxes/?, terminal font needs updating`n"

Write-Host "STATUS:" -ForegroundColor Yellow
Write-Host "  ✅ Check (success)    ❌ Cross (failure)    ⚠️ Warning"
Write-Host "  ✓ Light check        ✗ Light cross"

Write-Host "`nDOCUMENTS:" -ForegroundColor Yellow  
Write-Host "  📚 Books    📁 Folder    📋 Clipboard    📦 Package    📊 Chart    📄 Document"

Write-Host "`nACTIONS:" -ForegroundColor Yellow
Write-Host "  🎯 Target    🚀 Rocket    💡 Lightbulb    🔗 Link    🔧 Wrench    ⚙️ Gear"

Write-Host "`nDEVELOPMENT:" -ForegroundColor Yellow
Write-Host "  🛠️ Tools    🧪 Test tube    🏗️ Construction    💻 Laptop"

Write-Host "`nCELEBRATION:" -ForegroundColor Yellow
Write-Host "  ✨ Sparkles    🎉 Party    🎵 Music"

Write-Host "`nARROWS:" -ForegroundColor Yellow
Write-Host "  ▶ Play    ◀ Back    ▲ Up    ▼ Down"
Write-Host "  → Right   ← Left    ↑ Up    ↓ Down"

Write-Host "`nOTHER:" -ForegroundColor Yellow
Write-Host "  💪 Strength    🤖 Robot    🌐 Globe    💬 Speech    🔒 Lock    🔑 Key"

Write-Host "`n=== TEST COMPLETE ===" -ForegroundColor Green
Write-Host "All above emojis are ALLOWED in code/scripts/docs"
Write-Host "Any OTHER emoji is FORBIDDEN`n" -ForegroundColor Red

