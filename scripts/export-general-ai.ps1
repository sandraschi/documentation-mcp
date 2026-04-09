# Export General AI Documentation Stack
# Requires: pandoc (winget install pandoc)

param(
    [ValidateSet("docx", "html", "pdf")]
    [string]$Format = "docx",
    [string]$OutputDir = "$env:USERPROFILE\Desktop\general-ai-export"
)

$ErrorActionPreference = "Stop"
$SourceDir = "D:\Dev\repos\mcp-central-docs\docs\general-ai"

# Check pandoc
if (-not (Get-Command pandoc -ErrorAction SilentlyContinue)) {
    Write-Host "Pandoc not found. Install with: winget install pandoc" -ForegroundColor Red
    exit 1
}

# Add wkhtmltopdf to PATH if needed (for PDF export)
$wkPath = "C:\Program Files\wkhtmltopdf\bin"
if (Test-Path $wkPath) {
    $env:Path = "$wkPath;$env:Path"
}

# Create output directory
New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null

# Define hierarchical document structure
# Format: @{ Part = "Part Title"; Files = @("file1.md", "file2.md") }
$docStructure = @(
    @{
        Part = "Preface"
        Files = @(
            "README.md"
        )
    },
    @{
        Part = "Part I: History & Context"
        Files = @(
            "history/timeline-2025.md"
        )
    },
    @{
        Part = "Part II: The November 2025 Landscape"
        Files = @(
            "models/sota-comparison.md",
            "models/open-source.md",
            "models/agentic-coding.md",
            "models/video-gen.md",
            "models/image-gen.md",
            "models/scientific-computing.md"
        )
    },
    @{
        Part = "Part III: Hardware & Infrastructure"
        Files = @(
            "hardware/nvidia-story.md",
            "hardware/chip-wars.md",
            "hardware/supply-chain.md",
            "hardware/infrastructure.md"
        )
    },
    @{
        Part = "Part IV: Geopolitics & Regulation"
        Files = @(
            "regions/us-china-race.md",
            "regions/regulation-2025.md"
        )
    },
    @{
        Part = "Part V: Philosophy of Mind"
        Files = @(
            "theory/consciousness.md",
            "theory/classical-debates.md"
        )
    },
    @{
        Part = "Part VI: Society & Culture"
        Files = @(
            "society/doomsters-vs-pollyannas.md",
            "society/myths-and-narratives.md",
            "society/silicon-eschatology.md"
        )
    },
    @{
        Part = "Part VII: Doom Scenarios"
        Files = @(
            "doom-scenarios/democratized-destruction.md",
            "doom-scenarios/existential-risk.md",
            "doom-scenarios/endpoints-and-fiction.md"
        )
    },
    @{
        Part = "Part VIII: The Prophets (Science Fiction)"
        Files = @(
            "scifi/README.md",
            "scifi/solaris.md",
            "scifi/neuromancer.md",
            "scifi/snow-crash.md",
            "scifi/diamond-age.md",
            "scifi/fire-upon-the-deep.md",
            "scifi/dragons-egg.md",
            "scifi/accelerando.md"
        )
    }
)

# Build combined markdown with hierarchy
$combinedMd = "$OutputDir\general-ai-combined.md"
$content = @()

# Add document title
$content += "---"
$content += "title: 'General AI Landscape - November 2025'"
$content += "author: 'Compiled Documentation'"
$content += "date: '$(Get-Date -Format "MMMM yyyy")'"
$content += "---"
$content += ""

foreach ($section in $docStructure) {
    $partTitle = $section.Part
    $files = $section.Files
    
    # Add Part header (H1)
    Write-Host "`n=== $partTitle ===" -ForegroundColor Yellow
    $content += ""
    $content += "# $partTitle"
    $content += ""
    
    foreach ($file in $files) {
        $path = Join-Path $SourceDir $file
        if (Test-Path $path) {
            Write-Host "  Adding: $file" -ForegroundColor Cyan
            $fileContent = Get-Content $path -Raw
            
            # Bump headings down one level, but cap at H4 (H5+ look like body text)
            # Part headers = H1, chapter titles = H2, sections = H3, subsections = H4
            # First: flatten anything H4+ to H3 (so it becomes H4 after bump)
            $fileContent = $fileContent -replace '(?m)^#{4,}\s', '### '
            # Then bump: H1->H2, H2->H3, H3->H4
            $fileContent = $fileContent -replace '(?m)^### ', '#### '
            $fileContent = $fileContent -replace '(?m)^## ', '### '
            $fileContent = $fileContent -replace '(?m)^# ', '## '
            
            # Remove ALL internal links for self-contained export
            # 1. Windows absolute paths: [text](C:/path/file.md)
            $fileContent = $fileContent -replace '\[([^\]]+)\]\([A-Za-z]:[^\)]*\.md[^\)]*\)', '**$1**'
            # 2. Markdown file links: [text](./path.md) or [text](path.md#anchor)
            $fileContent = $fileContent -replace '\[([^\]]+)\]\([^\)]*\.md[^\)]*\)', '**$1**'
            # 3. Folder links: [models/](./models/) or [text](./folder/)
            $fileContent = $fileContent -replace '\[([^\]]+)\]\(\./[^\)]+/\)', '**$1**'
            # 4. Wiki-style links: [[text]] -> **text**
            $fileContent = $fileContent -replace '\[\[([^\]]+)\]\]', '**$1**'
            
            # 5. Remove "Documentation Structure" section entirely (useless folder list)
            $fileContent = $fileContent -replace '(?ms)^#{2,4}\s+Documentation Structure.*?(?=^#{1,3}\s+[A-Z]|\z)', ''
            
            $content += $fileContent
            $content += ""
            $content += "---"
            $content += ""
        } else {
            Write-Host "  Skipping (not found): $file" -ForegroundColor DarkYellow
        }
    }
}

$content | Out-File $combinedMd -Encoding utf8

# Generate actual TOC from headings (Pandoc's DOCX TOC is broken)
Write-Host "`nGenerating Table of Contents..." -ForegroundColor Cyan
$mdContent = Get-Content $combinedMd -Raw
$headings = [regex]::Matches($mdContent, '(?m)^(#{1,4})\s+(.+)$')

$toc = @()
$toc += "# Table of Contents"
$toc += ""

foreach ($h in $headings) {
    $level = $h.Groups[1].Value.Length
    $title = $h.Groups[2].Value.Trim()
    # Skip the YAML front matter title and TOC itself
    if ($title -match "^(title:|author:|date:|Table of Contents)") { continue }
    # Create anchor link (GitHub-style slugify)
    $anchor = $title.ToLower() -replace '[^a-z0-9\s-]', '' -replace '\s+', '-'
    $indent = "  " * ($level - 1)
    $toc += "$indent- [$title](#$anchor)"
}

$toc += ""
$toc += "---"
$toc += ""

# Insert TOC after YAML front matter (for HTML/PDF - markdown anchors work)
$yamlEnd = $mdContent.IndexOf("---", $mdContent.IndexOf("---") + 3) + 3
$beforeYaml = $mdContent.Substring(0, $yamlEnd)
$afterYaml = $mdContent.Substring($yamlEnd)
$contentWithToc = $beforeYaml + "`n`n" + ($toc -join "`n") + $afterYaml
$contentWithToc | Out-File $combinedMd -Encoding utf8

# For DOCX: create version without markdown TOC (Pandoc will generate Word TOC)
$combinedMdNoToc = "$OutputDir\general-ai-combined-notoc.md"
$contentNoToc = $beforeYaml + $afterYaml
$contentNoToc | Out-File $combinedMdNoToc -Encoding utf8

# Convert with pandoc
$timestamp = Get-Date -Format "yyyy-MM-dd"
$outputFile = "$OutputDir\General-AI-Landscape-$timestamp.$Format"

Write-Host "`nConverting to $Format..." -ForegroundColor Green

switch ($Format) {
    "docx" {
        # Strategy: Pandoc --toc creates clickable hyperlinks, then we convert
        # field codes to static hyperlinks (keeps clicks, removes popups)
        $fixScript = "$PSScriptRoot\fix-docx-toc.ps1"
        
        # Step 1: Create DOCX with Pandoc's native TOC (creates hyperlinks)
        pandoc $combinedMdNoToc -o $outputFile `
            --toc --toc-depth=3 `
            --metadata title="General AI Landscape - November 2025" `
            --metadata author="Compiled Documentation" `
            -V toc-title="Table of Contents"
        
        # Step 2: Convert TOC fields to static hyperlinks (clickable, no popups)
        if (Test-Path $fixScript) {
            Write-Host "Converting TOC to static hyperlinks..." -ForegroundColor Yellow
            & $fixScript -DocxPath $outputFile
        } else {
            Write-Host "WARNING: fix-docx-toc.ps1 not found - TOC may show popup" -ForegroundColor Yellow
        }
    }
    "html" {
        pandoc $combinedMd -o $outputFile --toc --toc-depth=3 --standalone `
            --embed-resources --standalone `
            --metadata title="General AI Landscape - November 2025" `
            --css="https://cdn.jsdelivr.net/npm/water.css@2/out/dark.min.css" `
            -V toc-title="Table of Contents"
    }
    "pdf" {
        # Use wkhtmltopdf (HTML->PDF) instead of LaTeX - simpler, no package hell
        pandoc $combinedMd -o $outputFile --toc --toc-depth=3 `
            --metadata title="General AI Landscape - November 2025" `
            --metadata author="Compiled Documentation" `
            --pdf-engine=wkhtmltopdf `
            --pdf-engine-opt="--enable-local-file-access" `
            --pdf-engine-opt="--margin-top" --pdf-engine-opt="15mm" `
            --pdf-engine-opt="--margin-bottom" --pdf-engine-opt="15mm" `
            --pdf-engine-opt="--margin-left" --pdf-engine-opt="15mm" `
            --pdf-engine-opt="--margin-right" --pdf-engine-opt="15mm" `
            --pdf-engine-opt="--minimum-font-size" --pdf-engine-opt="18"
    }
}

Write-Host "`nExported to: $outputFile" -ForegroundColor Green
Write-Host "Combined markdown at: $combinedMd" -ForegroundColor Gray

# Open output folder
Start-Process explorer.exe $OutputDir
