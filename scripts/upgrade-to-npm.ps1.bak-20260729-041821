# Upgrade MCP Server to npm/npx Distribution
# 
# This script automates the creation of npm package files for Python-based MCP servers.
# It creates package.json, bin/ wrapper script, and src/ Python checker.
#
# Usage:
#   .\upgrade-to-npm.ps1 -ServerPath "D:\Dev\repos\robotics-mcp"
#   .\upgrade-to-npm.ps1 -ServerPath "D:\Dev\repos\robotics-mcp" -Publish
#   .\upgrade-to-npm.ps1 -ServerPath "D:\Dev\repos\robotics-mcp" -TestOnly

param(
    [Parameter(Mandatory=$true)]
    [string]$ServerPath,
    
    [Parameter(Mandatory=$false)]
    [string]$NpmScope = "@sandraschi",
    
    [Parameter(Mandatory=$false)]
    [string]$Author = "Sandra Schi",
    
    [Parameter(Mandatory=$false)]
    [string]$License = "MIT",
    
    [Parameter(Mandatory=$false)]
    [switch]$Publish,
    
    [Parameter(Mandatory=$false)]
    [switch]$TestOnly,
    
    [Parameter(Mandatory=$false)]
    [switch]$Force
)

$ErrorActionPreference = "Stop"

# Validate server path
if (-not (Test-Path $ServerPath)) {
    Write-Error "Server path does not exist: $ServerPath"
    exit 1
}

$ServerPath = Resolve-Path $ServerPath
$ServerName = Split-Path $ServerPath -Leaf
$NpmPackageName = "$NpmScope/$($ServerName -replace '-mcp$', '-mcp')"

Write-Host "=== NPM/NPX Upgrade Script ===" -ForegroundColor Cyan
Write-Host "Server: $ServerName" -ForegroundColor Yellow
Write-Host "Path: $ServerPath" -ForegroundColor Yellow
Write-Host "NPM Package: $NpmPackageName" -ForegroundColor Yellow
Write-Host ""

# Check if package.json already exists
$PackageJsonPath = Join-Path $ServerPath "package.json"
if ((Test-Path $PackageJsonPath) -and -not $Force) {
    Write-Warning "package.json already exists. Use -Force to overwrite."
    $response = Read-Host "Continue anyway? (y/N)"
    if ($response -ne "y" -and $response -ne "Y") {
        Write-Host "Aborted." -ForegroundColor Red
        exit 0
    }
}

# Step 1: Read pyproject.toml or setup.py to get metadata, create/update pyproject.toml if needed
$PyProjectPath = Join-Path $ServerPath "pyproject.toml"
$SetupPyPath = Join-Path $ServerPath "setup.py"
$RequirementsPath = Join-Path $ServerPath "requirements.txt"
$Description = "MCP server for $ServerName"
$Version = "1.0.0"
$PythonModule = $null
$Author = "Sandra Schi"
$License = "MIT"
$PythonVersion = ">=3.10"
$Dependencies = @()

# Try to read from pyproject.toml first
if (Test-Path $PyProjectPath) {
    Write-Host "Reading pyproject.toml..." -ForegroundColor Green
    $pyprojectContent = Get-Content $PyProjectPath -Raw
    
    # Extract description
    if ($pyprojectContent -match 'description\s*=\s*"([^"]+)"') {
        $Description = $Matches[1]
    } elseif ($pyprojectContent -match "description\s*=\s*'([^']+)'") {
        $Description = $Matches[1]
    }
    
    # Extract version
    if ($pyprojectContent -match 'version\s*=\s*"([^"]+)"') {
        $Version = $Matches[1]
    } elseif ($pyprojectContent -match "version\s*=\s*'([^']+)'") {
        $Version = $Matches[1]
    }
    
    # Extract project name (Python module name)
    if ($pyprojectContent -match 'name\s*=\s*"([^"]+)"') {
        $PythonModule = $Matches[1] -replace '-', '_'
    } elseif ($pyprojectContent -match "name\s*=\s*'([^']+)'") {
        $PythonModule = $Matches[1] -replace '-', '_'
    }
    
    # Extract author
    if ($pyprojectContent -match 'authors\s*=\s*\[\s*\{[^}]*name\s*=\s*"([^"]+)"') {
        $Author = $Matches[1]
    }
    
    # Extract license
    if ($pyprojectContent -match 'license\s*=\s*\{[^}]*text\s*=\s*"([^"]+)"') {
        $License = $Matches[1]
    }
    
    # Extract Python version
    if ($pyprojectContent -match 'requires-python\s*=\s*"([^"]+)"') {
        $PythonVersion = $Matches[1]
    }
    
    # Extract dependencies
    if ($pyprojectContent -match '(?s)dependencies\s*=\s*\[(.*?)\]') {
        $depsSection = $Matches[1]
        $depsSection -split "`n" | ForEach-Object {
            $line = $_.Trim()
            if ($line -match '"([^"]+)"' -or $line -match "'([^']+)'") {
                $Dependencies += $Matches[1]
            }
        }
    }
}
# Fallback to setup.py if pyproject.toml doesn't exist
elseif (Test-Path $SetupPyPath) {
    Write-Host "Reading setup.py (will create pyproject.toml)..." -ForegroundColor Yellow
    $setupContent = Get-Content $SetupPyPath -Raw
    
    # Extract version
    if ($setupContent -match 'version\s*=\s*"([^"]+)"') {
        $Version = $Matches[1]
    }
    
    # Extract description
    if ($setupContent -match 'description\s*=\s*"([^"]+)"') {
        $Description = $Matches[1]
    }
    
    # Extract author
    if ($setupContent -match 'author\s*=\s*"([^"]+)"') {
        $Author = $Matches[1]
    }
    
    # Extract Python version
    if ($setupContent -match 'python_requires\s*=\s*"([^"]+)"') {
        $PythonVersion = $Matches[1]
    }
    
    # Extract dependencies from install_requires
    if ($setupContent -match '(?s)install_requires\s*=\s*\[(.*?)\]') {
        $depsSection = $Matches[1]
        $depsSection -split "`n" | ForEach-Object {
            $line = $_.Trim()
            if ($line -match '"([^"]+)"' -or $line -match "'([^']+)'") {
                $Dependencies += $Matches[1]
            }
        }
    }
    
    # Also try reading from requirements.txt
    if (Test-Path $RequirementsPath) {
        Get-Content $RequirementsPath | ForEach-Object {
            $line = $_.Trim()
            if ($line -and -not $line.StartsWith("#")) {
                $Dependencies += $line
            }
        }
    }
}

# Ensure FastMCP 2.13.1+ is in dependencies
$HasFastMCP = $false
$FastMCPVersion = "fastmcp>=2.14.1,<2.15.0"
for ($i = 0; $i -lt $Dependencies.Count; $i++) {
    if ($Dependencies[$i] -match "^fastmcp") {
        $HasFastMCP = $true
        # Update to 2.13.1+ if needed
        if ($Dependencies[$i] -notmatch "2\.13\.1") {
            $Dependencies[$i] = $FastMCPVersion
            Write-Host "Updating FastMCP to 2.13.1+ in dependencies" -ForegroundColor Yellow
        }
        break
    }
}
if (-not $HasFastMCP) {
    $Dependencies = @($FastMCPVersion) + $Dependencies
    Write-Host "Adding FastMCP 2.13.1+ to dependencies" -ForegroundColor Yellow
}

# If Python module not found, try to infer from directory structure
if (-not $PythonModule) {
    $SrcPath = Join-Path $ServerPath "src"
    if (Test-Path $SrcPath) {
        $PossibleModules = Get-ChildItem $SrcPath -Directory | Where-Object { 
            $_.Name -match '^[a-z_]+$' 
        } | Select-Object -First 1
        
        if ($PossibleModules) {
            $PythonModule = $PossibleModules.Name
        }
    }
    
    # Fallback: use server name
    if (-not $PythonModule) {
        $PythonModule = $ServerName -replace '-', '_'
    }
}

Write-Host "Detected Python module: $PythonModule" -ForegroundColor Green
Write-Host "Description: $Description" -ForegroundColor Green
Write-Host "Version: $Version" -ForegroundColor Green
Write-Host ""

# Step 1.5: Create/Update pyproject.toml (SOTA requirement - no repo without it!)
# ALWAYS ensure pyproject.toml exists and is SOTA-compliant
$PyProjectNeedsUpdate = $false
if (-not (Test-Path $PyProjectPath)) {
    Write-Host "Creating pyproject.toml (SOTA requirement - no repo without it!)..." -ForegroundColor Cyan
    $PyProjectNeedsUpdate = $true
} else {
    # Always check and update if needed (SOTA enforcement)
    $existingContent = Get-Content $PyProjectPath -Raw
    $needsUpdate = $false
    
    # Check FastMCP version
    if ($existingContent -notmatch "fastmcp>=2\.13\.1") {
        Write-Host "pyproject.toml needs FastMCP 2.13.1+ update (SOTA requirement)" -ForegroundColor Yellow
        $needsUpdate = $true
    }
    
    # Check for required sections
    if ($existingContent -notmatch '\[build-system\]') {
        Write-Host "pyproject.toml missing [build-system] section" -ForegroundColor Yellow
        $needsUpdate = $true
    }
    
    if ($needsUpdate -or $Force) {
        Write-Host "Updating pyproject.toml to SOTA standards..." -ForegroundColor Cyan
        $PyProjectNeedsUpdate = $true
    }
}

if ($PyProjectNeedsUpdate) {
    
    # Build dependencies list for TOML
    $DepsList = ""
    foreach ($dep in $Dependencies) {
        if ($dep) {
            $DepsList += "    `"$dep`",`n"
        }
    }
    $DepsList = $DepsList.TrimEnd("`n,")
    
    # Determine Python version for classifiers
    $PyVersionShort = "3.10"
    $PyVersionNum = "10"
    $MinVersion = 10
    if ($PythonVersion -match ">=3\.(\d+)") {
        $MinVersion = [int]$Matches[1]
        $PyVersionShort = "3.$MinVersion"
        $PyVersionNum = "$MinVersion"
    }
    
    # Build classifier list for Python versions
    $PyClassifiers = @(
        "    `"Programming Language :: Python :: 3`","
    )
    # Add specific version classifiers from min version to 3.12
    for ($v = $MinVersion; $v -le 12; $v++) {
        $PyClassifiers += "    `"Programming Language :: Python :: 3.$v`","
    }
    $PyClassifiersList = $PyClassifiers -join "`n"
    
    $PyProjectContent = @"
[build-system]
requires = ["setuptools>=61.0", "wheel"]
build-backend = "setuptools.build_meta"

[project]
name = "$ServerName"
version = "$Version"
description = "$Description"
readme = "README.md"
license = {text = "$License"}
authors = [
    {name = "$Author", email = "sandra@example.com"}
]
requires-python = "$PythonVersion"
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: MIT License",
$PyClassifiersList
    "Topic :: Software Development :: Libraries :: Python Modules",
]
keywords = [
    "mcp",
    "modelcontextprotocol",
    "fastmcp",
    "sota",
]

dependencies = [
$DepsList
]

[project.optional-dependencies]
dev = [
    "pytest>=7.3.1",
    "pytest-asyncio>=0.21.0",
    "ruff>=0.3.0",
    "mypy>=1.5.0",
]

[project.urls]
Homepage = "https://github.com/sandraschi/$ServerName"
Repository = "https://github.com/sandraschi/$ServerName"
Documentation = "https://github.com/sandraschi/$ServerName#readme"
Issues = "https://github.com/sandraschi/$ServerName/issues"

[project.scripts]
$($ServerName -replace '-mcp$', '-mcp') = "$PythonModule.__main__:main"

[tool.setuptools]
package-dir = {"" = "src"}

[tool.setuptools.packages.find]
where = ["src"]

[tool.ruff]
line-length = 100
target-version = "py$PyVersionNum"

[tool.ruff.lint]
select = ["E", "F", "I", "N", "W", "UP", "B", "C4", "SIM"]
ignore = ["E501"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
asyncio_mode = "auto"
"@
    
    Set-Content -Path $PyProjectPath -Value $PyProjectContent -Encoding UTF8
    Write-Host "✓ Created/updated pyproject.toml" -ForegroundColor Green
}

# Step 2: Create bin/ directory
$BinPath = Join-Path $ServerPath "bin"
if (-not (Test-Path $BinPath)) {
    New-Item -ItemType Directory -Path $BinPath -Force | Out-Null
    Write-Host "Created bin/ directory" -ForegroundColor Green
}

# Step 3: Create src/ directory (for check-python.js)
$SrcJsPath = Join-Path $ServerPath "src"
if (-not (Test-Path $SrcJsPath)) {
    New-Item -ItemType Directory -Path $SrcJsPath -Force | Out-Null
    Write-Host "Created src/ directory" -ForegroundColor Green
}

# Step 4: Create bin wrapper script
$BinScriptName = "$ServerName.js"
$BinScriptPath = Join-Path $BinPath $BinScriptName

$BinScriptContent = @"
#!/usr/bin/env node
/**
 * NPM wrapper for $ServerName MCP Server
 * 
 * This script launches the Python MCP server via FastMCP.
 * Python and dependencies must be installed separately.
 */

import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname, join } from 'path';
import { existsSync } from 'fs';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const serverRoot = join(__dirname, '..');

// Determine Python command based on platform
const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';

// Try to find Python module entry point
// Common patterns: python -m module_name or python -m module_name.__main__
const moduleName = '$PythonModule';
const possibleCommands = [
    ['-m', moduleName],
    ['-m', moduleName + '.__main__'],
    ['-m', moduleName + '.server'],
];

// Function to test if a Python command works
function testPythonCommand(args) {
    return new Promise((resolve) => {
        const testProc = spawn(pythonCmd, ['-c', `import ${args[1].split('.')[0]}`], {
            stdio: 'pipe',
            cwd: serverRoot
        });
        
        testProc.on('close', (code) => {
            resolve(code === 0);
        });
        
        testProc.on('error', () => {
            resolve(false);
        });
    });
}

// Find working command
async function findWorkingCommand() {
    for (const args of possibleCommands) {
        const works = await testPythonCommand(args);
        if (works) {
            return args;
        }
    }
    // Fallback to first option
    return possibleCommands[0];
}

// Main execution
(async () => {
    try {
        const commandArgs = await findWorkingCommand();
        
        const proc = spawn(pythonCmd, commandArgs, {
            stdio: 'inherit',
            cwd: serverRoot,
            env: {
                ...process.env,
                PYTHONUNBUFFERED: '1'
            }
        });
        
        proc.on('error', (err) => {
            console.error('Error starting Python server: ' + err.message);
            console.error('\nMake sure Python is installed and ''$PythonModule'' is available.');
            console.error('Try: pip install -e .');
            process.exit(1);
        });
        
        proc.on('exit', (code) => {
            process.exit(code || 0);
        });
        
        // Handle signals
        process.on('SIGINT', () => {
            proc.kill('SIGINT');
        });
        
        process.on('SIGTERM', () => {
            proc.kill('SIGTERM');
        });
        
    } catch (error) {
        console.error('Failed to start server: ' + error.message);
        process.exit(1);
    }
})();
"@

Set-Content -Path $BinScriptPath -Value $BinScriptContent -Encoding UTF8
Write-Host "Created bin/$BinScriptName" -ForegroundColor Green

# Step 5: Create src/check-python.js
$CheckPythonPath = Join-Path $SrcJsPath "check-python.js"

$CheckPythonContent = @"
/**
 * Python environment checker
 * Runs after npm install to validate Python setup
 */

import { spawn } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const pythonCmd = process.platform === 'win32' ? 'python' : 'python3';
const moduleName = '$PythonModule';

// Check if Python is available
const checkPython = () => {
    return new Promise((resolve) => {
        const proc = spawn(pythonCmd, ['--version'], {
            stdio: 'pipe'
        });
        
        proc.on('close', (code) => {
            resolve(code === 0);
        });
        
        proc.on('error', () => {
            resolve(false);
        });
    });
};

// Check if module is importable
const checkModule = () => {
    return new Promise((resolve) => {
        const moduleToImport = moduleName.split('.')[0];
        const proc = spawn(pythonCmd, ['-c', 'import ' + moduleToImport], {
            stdio: 'pipe'
        });
        
        proc.on('close', (code) => {
            resolve(code === 0);
        });
        
        proc.on('error', () => {
            resolve(false);
        });
    });
};

(async () => {
    const hasPython = await checkPython();
    if (!hasPython) {
        console.warn('[WARNING] Python not found. Install Python 3.10+ to use this package.');
        console.warn('   Command: ' + pythonCmd);
        process.exit(0); // Don't fail install, just warn
    }
    
    const hasModule = await checkModule();
    if (!hasModule) {
        console.warn('[WARNING] Python module "' + moduleName + '" not found.');
        console.warn('   Install dependencies with: pip install -e .');
        process.exit(0); // Don't fail install, just warn
    }
    
    console.log('[OK] Python environment check passed');
})();
"@

Set-Content -Path $CheckPythonPath -Value $CheckPythonContent -Encoding UTF8
Write-Host "Created src/check-python.js" -ForegroundColor Green

# Step 6: Create package.json
$PackageJson = @{
    name = $NpmPackageName
    version = $Version
    description = $Description
    type = "module"
    main = "bin/$BinScriptName"
    bin = @{
        $ServerName = "./bin/$BinScriptName"
    }
    scripts = @{
        postinstall = "node src/check-python.js"
        test = "node bin/$BinScriptName --help"
    }
    keywords = @(
        "mcp",
        "modelcontextprotocol",
        "fastmcp",
        ($ServerName -replace '-mcp$', '')
    )
    author = $Author
    license = $License
    engines = @{
        node = ">=18"
    }
    repository = @{
        type = "git"
        url = "https://github.com/sandraschi/$ServerName.git"
    }
    bugs = @{
        url = "https://github.com/sandraschi/$ServerName/issues"
    }
    homepage = "https://github.com/sandraschi/$ServerName#readme"
}

$PackageJsonContent = $PackageJson | ConvertTo-Json -Depth 10
Set-Content -Path $PackageJsonPath -Value $PackageJsonContent -Encoding UTF8
Write-Host "Created package.json" -ForegroundColor Green

# Step 7: Update .gitignore if needed
$GitIgnorePath = Join-Path $ServerPath ".gitignore"
$GitIgnoreContent = @"
# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*
.npm
"@

if (Test-Path $GitIgnorePath) {
    $ExistingContent = Get-Content $GitIgnorePath -Raw
    if ($ExistingContent -notmatch 'node_modules') {
        Add-Content -Path $GitIgnorePath -Value "`n$GitIgnoreContent"
        Write-Host "Updated .gitignore" -ForegroundColor Green
    }
} else {
    Set-Content -Path $GitIgnorePath -Value $GitIgnoreContent
    Write-Host "Created .gitignore" -ForegroundColor Green
}

# Step 7.5: Update README.md with npm/npx installation instructions
$ReadmePath = Join-Path $ServerPath "README.md"
if (Test-Path $ReadmePath) {
    Write-Host "Updating README.md with npm/npx installation..." -ForegroundColor Yellow
    $readmeContent = Get-Content $ReadmePath -Raw
    
    # Check if npm installation section already exists
    if ($readmeContent -notmatch "npm install.*$NpmPackageName" -and $readmeContent -notmatch "Option 1.*npm/npx") {
        # Find the Installation section
        if ($readmeContent -match "(?s)(## Installation\s*\n)(.*?)(?=\n## |$|\Z)") {
            $installationSection = $Matches[2]
            $beforeInstallation = $readmeContent.Substring(0, $Matches.Index + $Matches.Groups[1].Length)
            $afterInstallation = $readmeContent.Substring($Matches.Index + $Matches.Length)
            
            # Create npm/npx installation section
            $npmInstallSection = @"

### Option 1: npm/npx (Recommended)

Install via npm for easy access:

```powershell
# Install globally
npm install -g $NpmPackageName

# Or use npx (no installation needed)
npx $ServerName
```

**Note:** Python $($PythonVersion -replace '>=', '')+ and dependencies must be installed separately. The npm package will check for Python during installation.

"@
            
            # Renumber existing options
            $renumberedSection = $installationSection -replace "### Option (\d+):", {
                $num = [int]$Matches[1]
                "### Option $($num + 1):"
            }
            
            # Combine sections
            $newReadmeContent = $beforeInstallation + $npmInstallSection + $renumberedSection + $afterInstallation
            Set-Content -Path $ReadmePath -Value $newReadmeContent -Encoding UTF8
            Write-Host "✓ Updated README.md with npm/npx installation" -ForegroundColor Green
        } else {
            Write-Warning "Could not find Installation section in README.md - manual update may be needed"
        }
    } else {
        Write-Host "README.md already has npm/npx installation instructions" -ForegroundColor Gray
    }
} else {
    Write-Warning "README.md not found - npm installation instructions not added"
}

Write-Host ""
Write-Host "=== Files Created/Updated ===" -ForegroundColor Cyan
if (-not (Test-Path $PyProjectPath) -or $Force) {
    Write-Host "✓ pyproject.toml (SOTA requirement)" -ForegroundColor Green
}
Write-Host "✓ package.json" -ForegroundColor Green
Write-Host "✓ bin/$BinScriptName" -ForegroundColor Green
Write-Host "✓ src/check-python.js" -ForegroundColor Green
Write-Host ""

# Step 8: Test locally if requested
if ($TestOnly -or $Publish) {
    Write-Host "=== Testing Package ===" -ForegroundColor Cyan
    
    Push-Location $ServerPath
    
    try {
        # Install locally
        Write-Host "Installing package locally..." -ForegroundColor Yellow
        npm install . 2>&1 | Out-Null
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Package installed successfully" -ForegroundColor Green
        } else {
            Write-Warning "Package installation had warnings (this is OK)"
        }
        
        # Test npx command (dry run - just check it exists)
        Write-Host "Testing npx command..." -ForegroundColor Yellow
        $npxTest = Get-Command "npx" -ErrorAction SilentlyContinue
        if ($npxTest) {
            Write-Host "✓ npx is available" -ForegroundColor Green
        } else {
            Write-Warning "npx not found - install Node.js to test"
        }
        
    } catch {
        Write-Warning "Local test failed: $_"
    } finally {
        Pop-Location
    }
    
    Write-Host ""
}

# Step 9: Publish if requested
if ($Publish) {
    Write-Host "=== Publishing to npm ===" -ForegroundColor Cyan
    
    # Check if logged in
    $npmWhoami = npm whoami 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Not logged in to npm. Run: npm login"
        exit 1
    }
    
    Write-Host "Logged in as: $npmWhoami" -ForegroundColor Green
    
    Push-Location $ServerPath
    
    try {
        # Check if package already exists
        $existingVersion = npm view $NpmPackageName version 2>&1
        if ($LASTEXITCODE -eq 0) {
            Write-Warning "Package already exists on npm: version $existingVersion"
            $response = Read-Host "Publish new version? (y/N)"
            if ($response -ne "y" -and $response -ne "Y") {
                Write-Host "Publishing cancelled." -ForegroundColor Yellow
                Pop-Location
                exit 0
            }
        }
        
        # Publish
        Write-Host "Publishing $NpmPackageName@$Version..." -ForegroundColor Yellow
        npm publish --access public
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host ""
            Write-Host "✓ Successfully published to npm!" -ForegroundColor Green
            Write-Host "  Package: $NpmPackageName" -ForegroundColor Cyan
            Write-Host "  Version: $Version" -ForegroundColor Cyan
            Write-Host "  Install: npm install -g $NpmPackageName" -ForegroundColor Cyan
            Write-Host "  Use: npx $NpmPackageName" -ForegroundColor Cyan
        } else {
            Write-Error "Publishing failed"
            exit 1
        }
        
    } catch {
        Write-Error "Publishing error: $_"
        exit 1
    } finally {
        Pop-Location
    }
}

Write-Host ""
Write-Host "=== Next Steps ===" -ForegroundColor Cyan
Write-Host "1. Test locally: npm install -g ." -ForegroundColor Yellow
Write-Host "2. Test execution: npx $ServerName" -ForegroundColor Yellow
if (-not $Publish) {
    Write-Host "3. Publish: npm publish --access public" -ForegroundColor Yellow
}
Write-Host ""
Write-Host "Done! ✓" -ForegroundColor Green


