# sync-project-docs.ps1
# SOTA 2026 Documentation Centralization Script
# Centralizes README, PRD, CHANGELOG, and Config files from the repository fleet.

$RepoRoot = "D:\Dev\repos"
$TargetRoot = "D:\Dev\repos\mcp-central-docs\projects"

if (-not (Test-Path $TargetRoot)) {
    New-Item -ItemType Directory -Path $TargetRoot -Force
}

$Repos = Get-ChildItem -Path $RepoRoot -Directory

foreach ($Repo in $Repos) {
    if ($Repo.Name -eq "mcp-central-docs") { continue }
    
    $ProjectName = $Repo.Name
    $ProjectPath = $Repo.FullName
    $ProjectTarget = Join-Path $TargetRoot $ProjectName
    
    Write-Host "Processing Project: $ProjectName..." -ForegroundColor Cyan
    
    if (-not (Test-Path $ProjectTarget)) {
        New-Item -ItemType Directory -Path $ProjectTarget -Force
    }
    
    # 1. Copy Key Documentation
    # Kept in sync with mcp-central-docs/standards/PROJECT_PAGE_STANDARD.md's
    # "Required Layers" table and standards/README_STRUCTURE.md's required
    # file list. If you add a required repo file to either standard, add it
    # here too -- these two docs drifted apart once already (STATUS.md,
    # INSTALL.md, and the four docs/*.md files existed as a requirement for
    # weeks before this script knew to sync them), which is exactly the kind
    # of gap PROJECT_PAGE_STANDARD.md exists to prevent.
    $DocsToSync = @(
        "README.md",
        "PRD.md",
        "docs\PRD.md",
        "CHANGELOG.md",
        "STATUS.md",
        "INSTALL.md",
        "docs\TOOLS.md",
        "docs\CONFIGURATION.md",
        "docs\DEVELOPMENT.md",
        "docs\TROUBLESHOOTING.md",
        "llm.txt",
        "llms.txt",
        "pyproject.toml",
        "config.yaml",
        "config.json"
    )
    
    foreach ($Doc in $DocsToSync) {
        $SourceFile = Join-Path $ProjectPath $Doc
        if (Test-Path $SourceFile) {
            $TargetFile = Join-Path $ProjectTarget ($Doc -replace '\\', '_')
            Copy-Item -Path $SourceFile -Destination $TargetFile -Force
            Write-Host "  Synced: $Doc" -ForegroundColor Green
        }
    }
    
    # 2. Extract GitHub URL
    $GithubUrl = "N/A"
    $GitConfig = Join-Path $ProjectPath ".git\config"
    if (Test-Path $GitConfig) {
        $ConfigContent = Get-Content $GitConfig
        $UrlMatch = $ConfigContent | Select-String -Pattern 'url = (https://github.com/.*)'
        if ($UrlMatch) {
            $GithubUrl = $UrlMatch.Matches.Groups[1].Value.Trim()
        }
    }
    
    # 3. Generate Metadata JSON
    $Metadata = @{
        "id"         = $ProjectName
        "path"       = $ProjectPath
        "github_url" = $GithubUrl
        "last_sync"  = (Get-Date).ToString("yyyy-MM-dd HH:mm:ss")
    }
    
    $Metadata | ConvertTo-Json | Out-File (Join-Path $ProjectTarget "metadata_sync.json") -Encoding utf8
}

Write-Host "Documentation Synchronization Complete." -ForegroundColor Green
