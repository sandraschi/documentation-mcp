# MCP Project Assessment Script

# Function to get file modification date
function Get-FileDate {
    param($FilePath)
    if (Test-Path $FilePath) {
        return (Get-Item $FilePath).LastWriteTime
    }
    return $null
}

# Function to assess a project
function Assess-Project {
    param($ProjectName, $ProjectPath, $Category)
    
    $assessment = @{
        Name                 = $ProjectName
        Category             = $Category
        Status               = "Unknown"
        DevStatus            = "Unknown"
        RuntStatus           = "Unknown"
        StandardsCompliance  = @()
        ImportantTODOs       = @()
        Description          = ""
        LastModified         = $null
        HasGit               = $false
        HasProperStructure   = $false
        HasPackaging         = $false
        HasCI                = $false
        HasMonitoring        = $false
        FastMCPVersion       = "Unknown"
        DocumentationQuality = "Unknown"
    }
    
    # Check if it's a git repository
    if (Test-Path "$ProjectPath\.git") {
        $assessment.HasGit = $true
    }
    
    # Check README modification date
    $readmePath = "$ProjectPath\README.md"
    if (Test-Path $readmePath) {
        $assessment.LastModified = Get-FileDate $readmePath
        $assessment.DocumentationQuality = "Has README"
        
        # Check if README is old (before July 2025)
        if ($assessment.LastModified -lt [DateTime]"2025-07-01") {
            $assessment.RuntStatus = "RUNT - Old documentation"
        }
    }
    else {
        $assessment.RuntStatus = "RUNT - No README"
        $assessment.DocumentationQuality = "No README"
    }
    
    # Check project structure
    $hasSrc = Test-Path "$ProjectPath\src"
    $hasTests = Test-Path "$ProjectPath\tests"
    $hasPyProject = Test-Path "$ProjectPath\pyproject.toml"
    $hasRequirements = Test-Path "$ProjectPath\requirements.txt"
    
    if ($hasSrc -and $hasTests -and ($hasPyProject -or $hasRequirements)) {
        $assessment.HasProperStructure = $true
        $assessment.StandardsCompliance += "Proper project structure"
    }
    else {
        $assessment.RuntStatus = "RUNT - Poor project structure"
    }
    
    # Check for MCPB packaging
    $hasManifest = Test-Path "$ProjectPath\manifest.json"
    if ($hasManifest) {
        $assessment.HasPackaging = $true
        $assessment.StandardsCompliance += "MCPB packaging"
    }
    else {
        $assessment.RuntStatus = "RUNT - No MCPB packaging"
    }
    
    # Check for CI/CD
    $hasCI = Test-Path "$ProjectPath\.github\workflows"
    if ($hasCI) {
        $assessment.HasCI = $true
        $assessment.StandardsCompliance += "CI/CD pipeline"
    }
    
    # Check for monitoring
    $hasMonitoring = (Test-Path "$ProjectPath\monitoring") -or (Test-Path "$ProjectPath\docker-compose.yml")
    if ($hasMonitoring) {
        $assessment.HasMonitoring = $true
        $assessment.StandardsCompliance += "Monitoring stack"
    }
    
    # Determine overall status
    if ($assessment.RuntStatus -eq "Unknown") {
        if ($assessment.HasGit -and $assessment.HasProperStructure -and $assessment.HasPackaging) {
            $assessment.Status = "Production Ready"
            $assessment.DevStatus = "Complete"
        }
        elseif ($assessment.HasGit -and $assessment.HasProperStructure) {
            $assessment.Status = "Development"
            $assessment.DevStatus = "In Progress"
        }
        else {
            $assessment.Status = "Early Stage"
            $assessment.DevStatus = "Basic"
        }
    }
    else {
        $assessment.Status = "Runt"
        $assessment.DevStatus = "Needs Major Work"
    }
    
    return $assessment
}

# Main assessment
$reposPath = "D:\Dev\repos"
$mcpCentralDocsPath = "D:\Dev\repos\mcp-central-docs"

$assessments = @()

# Get all directories in repos root
$allDirs = Get-ChildItem $reposPath -Directory

foreach ($dir in $allDirs) {
    # Skip non-project directories if needed (e.g., .vscode, etc. if they exist at root, though usually they are hidden)
    if ($dir.Name.StartsWith(".")) { continue }
    
    # Skip mcp-central-docs itself to avoid circular refs or keep it if desired
    # Keeping it is fine as it's a project too
    
    $originalPath = $dir.FullName
    
    # Determine category based on name
    if ($dir.Name -match "mcp") {
        $category = "MCP Server"
    }
    else {
        $category = "Other Project"
    }
    
    Write-Host "Assessing $($dir.Name)..."
    $assessment = Assess-Project -ProjectName $dir.Name -ProjectPath $originalPath -Category $category
    $assessments += $assessment
}

# Generate assessment report
$reportPath = "D:\Dev\repos\mcp-central-docs\PROJECT_ASSESSMENT_REPORT.md"
$report = @"
# Project Assessment Report

**Generated:** $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")  
**Total Projects:** $($assessments.Count)

---

## 📊 **Summary Statistics**

### **By Status**
"@

# Count by status
$statusCounts = $assessments | Group-Object Status | Sort-Object Count -Descending
foreach ($group in $statusCounts) {
    $report += "`n- **$($group.Name)**: $($group.Count) projects"
}

$report += @"

### **By Category**
"@

# Count by category
$categoryCounts = $assessments | Group-Object Category | Sort-Object Count -Descending
foreach ($group in $categoryCounts) {
    $report += "`n- **$($group.Name)**: $($group.Count) projects"
}

$report += @"

### **Standards Compliance**
"@

# Count standards compliance
$standardsCounts = $assessments | ForEach-Object { $_.StandardsCompliance } | Group-Object | Sort-Object Count -Descending
foreach ($group in $standardsCounts) {
    $report += "`n- **$($group.Name)**: $($group.Count) projects"
}

$report += @"

---

## 🔍 **Detailed Assessments**

### **🟢 Production Ready Projects**
"@

$productionProjects = $assessments | Where-Object { $_.Status -eq "Production Ready" }
foreach ($project in $productionProjects) {
    $report += @"

#### **$($project.Name)**
- **Category**: $($project.Category)
- **Status**: $($project.Status)
- **Development Status**: $($project.DevStatus)
- **Standards Compliance**: $($project.StandardsCompliance -join ", ")
- **Last Modified**: $($project.LastModified)
- **Has Git**: $($project.HasGit)
- **Has Proper Structure**: $($project.HasProperStructure)
- **Has Packaging**: $($project.HasPackaging)
- **Has CI/CD**: $($project.HasCI)
- **Has Monitoring**: $($project.HasMonitoring)
"@
}

$report += @"

### **🟡 Development Projects**
"@

$developmentProjects = $assessments | Where-Object { $_.Status -eq "Development" }
foreach ($project in $developmentProjects) {
    $report += @"

#### **$($project.Name)**
- **Category**: $($project.Category)
- **Status**: $($project.Status)
- **Development Status**: $($project.DevStatus)
- **Standards Compliance**: $($project.StandardsCompliance -join ", ")
- **Last Modified**: $($project.LastModified)
- **Has Git**: $($project.HasGit)
- **Has Proper Structure**: $($project.HasProperStructure)
- **Has Packaging**: $($project.HasPackaging)
- **Has CI/CD**: $($project.HasCI)
- **Has Monitoring**: $($project.HasMonitoring)
"@
}

$report += @"

### **🔴 Runt Projects (Need Major Work)**
"@

$runtProjects = $assessments | Where-Object { $_.Status -eq "Runt" }
foreach ($project in $runtProjects) {
    $report += @"

#### **$($project.Name)**
- **Category**: $($project.Category)
- **Status**: $($project.Status)
- **Development Status**: $($project.DevStatus)
- **Runt Status**: $($project.RuntStatus)
- **Standards Compliance**: $($project.StandardsCompliance -join ", ")
- **Last Modified**: $($project.LastModified)
- **Has Git**: $($project.HasGit)
- **Has Proper Structure**: $($project.HasProperStructure)
- **Has Packaging**: $($project.HasPackaging)
- **Has CI/CD**: $($project.HasCI)
- **Has Monitoring**: $($project.HasMonitoring)
"@
}

$report += @"

### **🟠 Early Stage Projects**
"@

$earlyStageProjects = $assessments | Where-Object { $_.Status -eq "Early Stage" }
foreach ($project in $earlyStageProjects) {
    $report += @"

#### **$($project.Name)**
- **Category**: $($project.Category)
- **Status**: $($project.Status)
- **Development Status**: $($project.DevStatus)
- **Standards Compliance**: $($project.StandardsCompliance -join ", ")
- **Last Modified**: $($project.LastModified)
- **Has Git**: $($project.HasGit)
- **Has Proper Structure**: $($project.HasProperStructure)
- **Has Packaging**: $($project.HasPackaging)
- **Has CI/CD**: $($project.HasCI)
- **Has Monitoring**: $($project.HasMonitoring)
"@
}

$report += @"

---

## 📋 **Action Items**

### **Priority 1: Fix Runt Projects**
"@

foreach ($project in $runtProjects) {
    $report += @"

#### **$($project.Name)**
- **Issues**: $($project.RuntStatus)
- **Action**: Major refactoring needed
- **Standards**: Implement proper project structure, MCPB packaging, CI/CD
"@
}

$report += @"

### **Priority 2: Complete Development Projects**
"@

foreach ($project in $developmentProjects) {
    $report += @"

#### **$($project.Name)**
- **Status**: Development in progress
- **Action**: Complete packaging and CI/CD setup
"@
}

$report += @"

### **Priority 3: Enhance Early Stage Projects**
"@

foreach ($project in $earlyStageProjects) {
    $report += @"

#### **$($project.Name)**
- **Status**: Early stage
- **Action**: Implement proper structure and standards
"@
}

$report += @"

---

## 🎯 **Recommendations**

1. **Focus on Runt Projects**: These need immediate attention and major work
2. **Complete Development Projects**: Finish packaging and CI/CD setup
3. **Enhance Early Stage Projects**: Implement proper structure and standards
4. **Maintain Production Projects**: Keep them up to date with latest standards

---

*Report generated on $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")*
"@

$report | Out-File -FilePath $reportPath -Encoding UTF8
Write-Host "Assessment report generated: $reportPath"

# Also create individual assessment files for each project
foreach ($assessment in $assessments) {
    $assessmentPath = "D:\Dev\repos\$($assessment.Name)\ASSESSMENT.md"
    $individualReport = @"
# $($assessment.Name) - Project Assessment

**Category**: $($assessment.Category)  
**Assessment Date**: $(Get-Date -Format "yyyy-MM-dd")  
**Status**: $($assessment.Status)

---

## 📊 **Assessment Summary**

| Metric | Value |
|--------|-------|
| **Status** | $($assessment.Status) |
| **Development Status** | $($assessment.DevStatus) |
| **Runt Status** | $($assessment.RuntStatus) |
| **Last Modified** | $($assessment.LastModified) |
| **Has Git Repository** | $($assessment.HasGit) |
| **Has Proper Structure** | $($assessment.HasProperStructure) |
| **Has MCPB Packaging** | $($assessment.HasPackaging) |
| **Has CI/CD Pipeline** | $($assessment.HasCI) |
| **Has Monitoring Stack** | $($assessment.HasMonitoring) |

---

## 🎯 **Standards Compliance**

"@

    if ($assessment.StandardsCompliance.Count -gt 0) {
        foreach ($standard in $assessment.StandardsCompliance) {
            $individualReport += "`n- ✅ $standard"
        }
    }
    else {
        $individualReport += "`n- ❌ No standards compliance detected"
    }

    $individualReport += @"

---

## 📋 **Important TODOs**

"@

    if ($assessment.RuntStatus -ne "Unknown") {
        $individualReport += "`n- 🔴 **CRITICAL**: $($assessment.RuntStatus)"
    }

    if (-not $assessment.HasGit) {
        $individualReport += "`n- 🔴 **CRITICAL**: Initialize Git repository"
    }

    if (-not $assessment.HasProperStructure) {
        $individualReport += "`n- 🔴 **CRITICAL**: Implement proper project structure (src/, tests/, pyproject.toml)"
    }

    if (-not $assessment.HasPackaging) {
        $individualReport += "`n- 🔴 **CRITICAL**: Implement MCPB packaging (manifest.json)"
    }

    if (-not $assessment.HasCI) {
        $individualReport += "`n- 🟡 **IMPORTANT**: Set up CI/CD pipeline"
    }

    if (-not $assessment.HasMonitoring) {
        $individualReport += "`n- 🟡 **IMPORTANT**: Implement monitoring stack"
    }

    $individualReport += @"

---

## 🚀 **Next Steps**

"@

    if ($assessment.Status -eq "Runt") {
        $individualReport += @"

### **Major Refactoring Required**
1. **Initialize Git repository** if missing
2. **Implement proper project structure**
3. **Set up MCPB packaging**
4. **Create CI/CD pipeline**
5. **Update documentation**
6. **Implement monitoring stack**
"@
    }
    elseif ($assessment.Status -eq "Development") {
        $individualReport += @"

### **Complete Development**
1. **Finish MCPB packaging**
2. **Set up CI/CD pipeline**
3. **Implement monitoring stack**
4. **Complete documentation**
"@
    }
    elseif ($assessment.Status -eq "Early Stage") {
        $individualReport += @"

### **Enhance Early Stage**
1. **Implement proper project structure**
2. **Set up MCPB packaging**
3. **Create CI/CD pipeline**
4. **Add monitoring stack**
"@
    }
    else {
        $individualReport += @"

### **Maintain Production**
1. **Keep up to date with latest standards**
2. **Regular maintenance and updates**
3. **Monitor for improvements**
"@
    }

    $individualReport += @"

---

## 📚 **References**

- [MCP Central Documentation Standards](../STANDARDS.md)
- [FastMCP 2.12 Migration Guide](../FASTMCP_2.12_MIGRATION.md)
- [MCPB Packaging Standards](../MCPB_PACKAGING_STANDARDS.md)
- [Monitoring Standards](../monitoring/README.md)

---

*Assessment generated on $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")*
"@

    $individualReport | Out-File -FilePath $assessmentPath -Encoding UTF8
}

Write-Host "Individual assessment files created for each project"
Write-Host "Assessment completed!"
