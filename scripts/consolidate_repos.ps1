$ErrorActionPreference = "Stop"

$projectsPath = "d:/Dev/repos/mcp-central-docs/projects"
$reposPath = "d:/Dev/repos/mcp-central-docs/repos"

# 1. Process mcp-servers
$mcpServersPath = Join-Path $projectsPath "mcp-servers"
if (Test-Path $mcpServersPath) {
    $servers = Get-ChildItem -Path $mcpServersPath -Directory
    foreach ($server in $servers) {
        $serverName = $server.Name
        $destPath = Join-Path $reposPath $serverName
        
        if (Test-Path $destPath) {
            Write-Host "Merging $serverName..."
            
            # Move ASSESSMENT.md
            $assessmentSrc = Join-Path $server.FullName "ASSESSMENT.md"
            if (Test-Path $assessmentSrc) {
                Move-Item -Path $assessmentSrc -Destination (Join-Path $destPath "AUTOMATED_ASSESSMENT.md") -Force
            }
            
            # Move CHANGELOG.md if it doesn't exist in dest or rename
            $changelogSrc = Join-Path $server.FullName "CHANGELOG.md"
            if (Test-Path $changelogSrc) {
                if (Test-Path (Join-Path $destPath "CHANGELOG.md")) {
                    Move-Item -Path $changelogSrc -Destination (Join-Path $destPath "CHANGELOG_SNAPSHOT.md") -Force
                } else {
                    Move-Item -Path $changelogSrc -Destination $destPath -Force
                }
            }
            
            # Move README.md if it doesn't exist in dest or rename
            $readmeSrc = Join-Path $server.FullName "README.md"
            if (Test-Path $readmeSrc) {
                if (Test-Path (Join-Path $destPath "README.md")) {
                    Move-Item -Path $readmeSrc -Destination (Join-Path $destPath "README_SNAPSHOT.md") -Force
                } else {
                    Move-Item -Path $readmeSrc -Destination $destPath -Force
                }
            }
            
            # Remove the source directory if empty (or force remove remaining files if any unimportant ones left? No, let's be safe)
            # Actually, we should probably move any other files too?
            # Let's move any other files that don't exist in destination
            Get-ChildItem -Path $server.FullName | Where-Object { $_.Name -notin @("ASSESSMENT.md", "CHANGELOG.md", "README.md") } | ForEach-Object {
                $itemDest = Join-Path $destPath $_.Name
                if (-not (Test-Path $itemDest)) {
                    Move-Item -Path $_.FullName -Destination $destPath -Force
                } else {
                    Write-Warning "Skipping duplicate file: $($_.Name) in $serverName"
                }
            }
            
            Remove-Item -Path $server.FullName -Recurse -Force
        } else {
            Write-Host "Moving $serverName to repos..."
            Move-Item -Path $server.FullName -Destination $reposPath -Force
            
            # Rename ASSESSMENT.md to AUTOMATED_ASSESSMENT.md in the new location
            $newAssessmentPath = Join-Path $destPath "ASSESSMENT.md"
            if (Test-Path $newAssessmentPath) {
                Rename-Item -Path $newAssessmentPath -NewName "AUTOMATED_ASSESSMENT.md"
            }
        }
    }
}

# 2. Process other directories
$otherDirs = @("myai", "veogen", "other-projects")
foreach ($dirName in $otherDirs) {
    $srcDir = Join-Path $projectsPath $dirName
    if (Test-Path $srcDir) {
        $destDir = Join-Path $reposPath $dirName
        if (-not (Test-Path $destDir)) {
            Write-Host "Moving $dirName to repos..."
            Move-Item -Path $srcDir -Destination $reposPath -Force
        } else {
            Write-Warning "Destination $dirName already exists in repos. Manual intervention might be needed."
        }
    }
}

# 3. Cleanup
if ((Get-ChildItem -Path $projectsPath).Count -eq 1) { # Only mcp-servers folder left (which should be empty)
    Remove-Item -Path $projectsPath -Recurse -Force
    Write-Host "Projects directory removed."
} else {
    Write-Warning "Projects directory not empty. Please check manually."
    Get-ChildItem -Path $projectsPath
}
