# Export General AI Documentation for Amazon KDP
# Creates PDF formatted for 6x9" trim size
# Requires: pandoc, wkhtmltopdf

param(
    [ValidateSet("pdf", "epub")]
    [string]$Format = "pdf",
    [string]$OutputDir = "$env:USERPROFILE\Desktop\general-ai-amazon"
)

$ErrorActionPreference = "Stop"
$SourceDir = "D:\Dev\repos\mcp-central-docs\docs\general-ai"

# Check pandoc
if (-not (Get-Command pandoc -ErrorAction SilentlyContinue)) {
    Write-Host "Pandoc not found. Install with: winget install pandoc" -ForegroundColor Red
    exit 1
}

# Add wkhtmltopdf to PATH if needed
$wkPath = "C:\Program Files\wkhtmltopdf\bin"
if (Test-Path $wkPath) {
    $env:Path = "$wkPath;$env:Path"
}

# Create output directory
New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null

# Amazon KDP document structure
$docStructure = @(
    @{
        Part = ""  # No part header for front matter
        Files = @(
            "amazon/FRONT_MATTER.md"
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
            "models/image-gen.md"
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
    },
    @{
        Part = ""  # No part header for back matter
        Files = @(
            "amazon/BIBLIOGRAPHY.md",
            "amazon/BACK_MATTER.md"
        )
    }
)

# Build combined markdown
$combinedMd = "$OutputDir\amazon-combined.md"
$content = @()

# YAML metadata for book
$content += "---"
$content += "title: 'The AI Landscape: A November 2025 Snapshot'"
$content += "subtitle: 'From Turing to Gemini, from GPUs to Galaxies'"
$content += "author: 'Sandra Schi'"
$content += "date: 'November 2025'"
$content += "lang: en-US"
$content += "---"
$content += ""

foreach ($section in $docStructure) {
    $partTitle = $section.Part
    $files = $section.Files
    
    # Add Part header only if not empty
    if ($partTitle) {
        Write-Host "`n=== $partTitle ===" -ForegroundColor Yellow
        $content += ""
        $content += "# $partTitle"
        $content += ""
    }
    
    foreach ($file in $files) {
        $path = Join-Path $SourceDir $file
        if (Test-Path $path) {
            Write-Host "  Adding: $file" -ForegroundColor Cyan
            $fileContent = Get-Content $path -Raw
            
            # Bump headings (except front/back matter), cap at H4
            if ($partTitle) {
                # Flatten H4+ to H3 first (so it becomes H4 after bump)
                $fileContent = $fileContent -replace '(?m)^#{4,}\s', '### '
                # Then bump: H1->H2, H2->H3, H3->H4
                $fileContent = $fileContent -replace '(?m)^### ', '#### '
                $fileContent = $fileContent -replace '(?m)^## ', '### '
                $fileContent = $fileContent -replace '(?m)^# ', '## '
            }
            
            # Remove ALL .md links for self-contained export
            # Handles: ./path.md, ../path.md, path.md, path.md#section, /path.md
            $fileContent = $fileContent -replace '\[([^\]]+)\]\([^\)]*\.md[^\)]*\)', '**$1**'
            
            # Also handle wiki-style links [[text]] -> **text**
            $fileContent = $fileContent -replace '\[\[([^\]]+)\]\]', '**$1**'
            
            # Remove external image links (KDP doesn't like external URLs)
            $fileContent = $fileContent -replace '!\[([^\]]*)\]\(https?://[^\)]+\)', ''
            
            $content += $fileContent
            $content += ""
            $content += ""
        } else {
            Write-Host "  Skipping (not found): $file" -ForegroundColor DarkYellow
        }
    }
}

$content | Out-File $combinedMd -Encoding utf8

# Convert
$timestamp = Get-Date -Format "yyyy-MM-dd"

Write-Host "`nConverting to $Format..." -ForegroundColor Green

switch ($Format) {
    "pdf" {
        $outputFile = "$OutputDir\AI-Landscape-November-2025-KDP.$Format"
        # KDP-optimized PDF: 6x9 trim (152x229mm), larger inside margin for binding
        pandoc $combinedMd -o $outputFile --toc --toc-depth=2 `
            --metadata title="The AI Landscape: A November 2025 Snapshot" `
            --metadata author="Sandra Schi" `
            --pdf-engine=wkhtmltopdf `
            --pdf-engine-opt="--enable-local-file-access" `
            --pdf-engine-opt="--page-width" --pdf-engine-opt="152" `
            --pdf-engine-opt="--page-height" --pdf-engine-opt="229" `
            --pdf-engine-opt="--margin-top" --pdf-engine-opt="20" `
            --pdf-engine-opt="--margin-bottom" --pdf-engine-opt="20" `
            --pdf-engine-opt="--margin-left" --pdf-engine-opt="22" `
            --pdf-engine-opt="--margin-right" --pdf-engine-opt="15" `
            --pdf-engine-opt="--minimum-font-size" --pdf-engine-opt="16"
    }
    "epub" {
        $outputFile = "$OutputDir\AI-Landscape-November-2025-KDP.$Format"
        # EPUB for Kindle
        pandoc $combinedMd -o $outputFile --toc --toc-depth=2 `
            --metadata title="The AI Landscape: A November 2025 Snapshot" `
            --metadata author="Sandra Schi" `
            --epub-chapter-level=1
    }
}

Write-Host "`nExported to: $outputFile" -ForegroundColor Green
Write-Host "Combined markdown at: $combinedMd" -ForegroundColor Gray

# Open output folder
Start-Process explorer.exe $OutputDir

