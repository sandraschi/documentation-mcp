# NSIS Build Procedure — Belt & Suspenders

**Status:** Fleet standard (June 2026)
**Audience:** Agent performing a Tauri NSIS build for any fleet repo (autonomous, no user interaction)
**Cross-refs:** [TAURI_PRODUCTION_PITFALLS.md](../standards/TAURI_PRODUCTION_PITFALLS.md) · [tauri_nsis_building.md](../standards/rules/tauri_nsis_building.md) · [cua_nsis_smoke_testing.md](../standards/rules/cua_nsis_smoke_testing.md) · [WEBAPP_PORTS.md](../operations/WEBAPP_PORTS.md)

---

## How to use this document

Each phase starts with a **WHAT** statement explaining what is being done and why.
Each phase MUST pass before the next begins. If a phase fails, fix at that phase — never proceed.
After phase completion, results are appended to `$results` for the final report.

---

## Phase 0: Pre-flight

**WHAT: Gather per-repo variables, kill zombie processes, verify toolchain. If anything missing, abort immediately.**

### 0.1 Read repo config and allocate variables

```powershell
$repo = Split-Path -Leaf (Get-Location)   # auto-detected from current dir
# Or override: $repo = "my-repo-name"

# Look up port from WEBAPP_PORTS.md
$portMap = Select-String -Path "D:\Dev\repos\mcp-central-docs\operations\WEBAPP_PORTS.md" -Pattern "\| (\d+).*\| ${repo}\s+\|"
if (-not $portMap) { throw "Repo '$repo' not found in WEBAPP_PORTS.md — register a port first" }
$port = $portMap.Matches.Groups[1].Value
$fePort = [int]$port + 1
$identifier = "ai.fleet.$repo"
$productName = (Get-Culture).TextInfo.ToTitleCase($repo.Replace("-", " ")) + " MCP"
$mainBinary = "${repo}-native"
$envVar = "${repo}_TAURI".ToUpper()

# Detect webapp directory
foreach ($try in @("web_sota", "webapp", "native/webapp")) {
    $webDir = $try
    if (Test-Path "D:\Dev\repos\$repo\$try\package.json") { break }
}
Write-Host "CONFIG: repo=$repo port=$port fePort=$fePort webDir=$webDir"
```

### 0.2 If native/ already exists, back it up

```powershell
$nativeDir = "D:\Dev\repos\$repo\native"
if (Test-Path $nativeDir) {
    $backupStamp = Get-Date -Format 'yyyyMMdd_HHmmss'
    Rename-Item -Path $nativeDir -NewName "native.$backupStamp.bak" -Force
    Write-Host "BACKUP: existing native/ -> native.$backupStamp.bak"
}
```

### 0.3 Kill zombie processes

```powershell
Get-Process -Name "$repo-native", "$repo-backend" -ErrorAction SilentlyContinue | Stop-Process -Force
Get-NetTCPConnection -LocalPort $port -ErrorAction SilentlyContinue | ForEach-Object {
    Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue
}
Get-NetTCPConnection -LocalPort $fePort -ErrorAction SilentlyContinue | ForEach-Object {
    Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue
}
Start-Sleep 2
Write-Host "ZOMBIES: cleared"
```

### 0.4 Verify prerequisites

```powershell
$checks = @(
    @{cmd="rustc --version"; regex="\d+\.\d+"},
    @{cmd="npx @tauri-apps/cli --version 2>$null"; regex="\d+"},
    @{cmd="uv run python --version"; regex="3\.1[23]"},
    @{cmd="uv run pyinstaller --version 2>$null"; regex="\d+"},
    @{cmd="node --version"; regex="1[89]\.|2[0-9]\."},
    @{cmd="npm --version 2>$null"; regex="\d+"}
)
$allOk = $true
foreach ($c in $checks) {
    $out = cmd /c ($c.cmd) 2>&1
    if ($out -notmatch $c.regex) { Write-Warning "MISSING: $($c.cmd)"; $allOk = $false }
}
if (-not $allOk) { throw "Prerequisites missing — install before proceeding" }
Write-Host "PREREQS: all present"
```

### 0.5 Verify repo has required files

```powershell
$requiredFiles = @("pyproject.toml", "run_server.py", "${repo}-backend.spec")
$missing = $requiredFiles | Where-Object { -not (Test-Path "D:\Dev\repos\$repo\$_") }
if ($missing) { throw "Missing required files: $($missing -join ', ')" }
Write-Host "REPO FILES: all present"
```

### Results

```powershell
$results = [PSCustomObject]@{
    Repo = $repo; Port = $port; FePort = $fePort; Identifier = $identifier
    ProductName = $productName; MainBinary = $mainBinary; EnvVar = $envVar; WebDir = $webDir
    Gates = @{}; Phases = @{}
}
$results.Phases["preflight"] = "PASS"
```

---

## Phase 1: Scaffold native/ folder

**WHAT: Copy the Tauri template from mcp-central-docs and patch all placeholders with per-repo values.**

### 1.1 Copy template

```powershell
$src = "D:\Dev\repos\mcp-central-docs\templates\tauri-native"
Copy-Item -Path $src -Destination $nativeDir -Recurse -Force
Write-Host "COPIED: template -> $nativeDir"
```

### 1.2 Patch placeholders

```powershell
$replacements = @{
    '{repo}' = $repo
    '{port}' = $port
    '{identifier}' = $identifier
    '{productName}' = $productName
    '{mainBinary}' = $mainBinary
    '{envVar}' = $envVar
    '{webDir}' = $webDir
}
Get-ChildItem -Recurse -File $nativeDir | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    foreach ($key in $replacements.Keys) {
        $content = $content -replace [regex]::Escape($key), $replacements[$key]
    }
    Set-Content $_.FullName -Value $content -NoNewline
}
Write-Host "PATCHED: placeholders replaced"
```

### 1.3 Verify no unsubstituted placeholders remain

```powershell
$leftovers = Select-String -Path "$nativeDir\*" -Pattern '\{repo\}|\{port\}|\{identifier\}|\{productName\}|\{mainBinary\}|\{envVar\}' -Recurse
if ($leftovers) {
    $leftoverFiles = ($leftovers | Select-Object -ExpandProperty Path -Unique) -join ", "
    throw "Unsubstituted placeholders remain in: $leftoverFiles"
}
Write-Host "VERIFIED: no placeholders left behind"
$results.Phases["scaffold"] = "PASS"
```

---

## Phase 2: Code gates (TAURI_PRODUCTION_PITFALLS.md checklist)

**WHAT: Run each code gate (A through J). Each gate reads the source files, verifies correctness, and fails with a clear message if something is wrong.**

### Gate A: Ports and naming

**WHAT: Verify bundle id, binary names, and port match the fleet registry.**

```powershell
$gates = $results.Gates
# Check port is correct in tauri.conf.json
$tauriConfig = Get-Content "$nativeDir\tauri.conf.json" -Raw | ConvertFrom-Json
if ($tauriConfig.productName -ne $productName) { throw "tauri.conf.json productName mismatch" }
if ($tauriConfig.identifier -ne $identifier) { throw "tauri.conf.json identifier mismatch" }
$gates["A_ports"] = "PASS"
```

### Gate B: Frontend production API

**WHAT: Audit frontend source for relative fetch() calls that break in Tauri (WebView origin differs from dev).**

```powershell
# Audit for relative API calls (must use absolute http://127.0.0.1:{port})
$relCalls = Select-String -Path "D:\Dev\repos\$repo\$webDir" -Pattern "fetch\(['\`"]/api/" -Recurse -SimpleMatch -Exclude "**/node_modules/**"
if ($relCalls) { throw "Relative fetch() found — must use absolute API_BASE. Files: $(($relCalls | Select -First 5).Path -join ', ')" }

# Verify tauri.conf.json CSP includes backend port
if ($tauriConfig.app.security.csp -notmatch [regex]::Escape("http://127.0.0.1:$port")) {
    throw "tauri.conf.json CSP connect-src missing http://127.0.0.1:$port"
}
$gates["B_frontend_api"] = "PASS"
```

### Gate C: Backend CORS

**WHAT: Verify backend CORS middleware allows tauri.localhost origins. Read the backend app setup file.**

```powershell
$backendFiles = Get-ChildItem "D:\Dev\repos\$repo\src" -Recurse -Filter "*.py" | Select-Object -First 5
$corsFound = $false
foreach ($f in $backendFiles) {
    $content = Get-Content $f.FullName -Raw
    if ($content -match "tauri\.localhost|tauri://localhost") { $corsFound = $true; break }
}
if (-not $corsFound) { throw "No tauri.localhost CORS origins found in backend — add per Gate C pattern" }
$gates["C_cors"] = "PASS"
```

### Gate D: run_server.py (PyInstaller entry)

**WHAT: Verify the PyInstaller entry point is frozen-safe (no os.chdir when frozen, eager-imports stdlib C exts).**

```powershell
$rsp = Get-Content "D:\Dev\repos\$repo\run_server.py" -Raw
if ($rsp -match "os\.chdir") { throw "run_server.py has os.chdir — will crash when frozen. Use frozen-safe pattern." }
if ($rsp -notmatch "import _strptime") { throw "run_server.py missing import _strptime — stdlib C ext will fail frozen" }
$gates["D_run_server"] = "PASS"
```

### Gate E: PyInstaller spec

**WHAT: Verify {repo}-backend.spec has the mandatory settings (noarchive=True, upx=False, strip=False).**

```powershell
$spec = Get-Content "D:\Dev\repos\$repo\${repo}-backend.spec" -Raw
if ($spec -match "noarchive=False|noarchive\s*=\s*False") { throw "spec has noarchive=False — set noarchive=True" }
if ($spec -notmatch "noarchive\s*=\s*True") { throw "spec missing noarchive=True — mandatory for onefile" }
if ($spec -match "upx=True") { throw "spec has upx=True — set upx=False (UPX breaks on Windows)" }
if ($spec -notmatch "cachetools") { Write-Warning "spec missing cachetools in hiddenimports" }
$gates["E_pyinstaller"] = "PASS"
```

### Gate F: Rust backend.rs

**WHAT: Verify Rust spawn code resolves backend from resources/ first, sets PORT and TAURI env vars.**

```powershell
$backendRs = Get-Content "$nativeDir\src\backend.rs" -Raw
if ($backendRs -notmatch "BaseDirectory::Resource") { throw "backend.rs must resolve from Resource, not exe_dir" }
if ($backendRs -notmatch [regex]::Escape("$envVar")) { throw "backend.rs missing env var $envVar" }
if ($backendRs -notmatch [regex]::Escape("$port")) { throw "backend.rs missing PORT=$port" }
if ($backendRs -notmatch "CREATE_NO_WINDOW") { throw "backend.rs missing CREATE_NO_WINDOW" }
$gates["F_backend_rs"] = "PASS"
```

### Gate G: Rust main.rs lifecycle

**WHAT: Verify main.rs spawns backend in setup() and kills child on exit.**

```powershell
$mainRs = Get-Content "$nativeDir\src\main.rs" -Raw
if ($mainRs -notmatch "\.setup\(") { throw "main.rs must spawn backend in setup() hook" }
if ($mainRs -notmatch "RunEvent::Exit") { throw "main.rs must kill backend on RunEvent::Exit" }
$gates["G_lifecycle"] = "PASS"
```

### Gate H: Build scripts

**WHAT: Verify build-sidecar.ps1 exists or build.ps1 covers the full pipeline.**

```powershell
if (-not (Test-Path "$nativeDir\build-sidecar.ps1") -and -not (Test-Path "$nativeDir\build.ps1")) {
    throw "No build script found in native/ — need build-sidecar.ps1 or build.ps1"
}
$gates["H_build_scripts"] = "PASS"
```

### Gate I: NSIS hooks

**WHAT: Verify hooks kill BOTH backend and operator exes, and tauri.conf.json has the right NSIS settings.**

```powershell
$hooks = Get-Content "$nativeDir\windows\hooks.nsh" -Raw
if ($hooks -notmatch "KillProcessCurrentUser" -or $hooks -notmatch "${repo}-backend") {
    throw "hooks.nsh missing KillProcessCurrentUser for ${repo}-backend.exe"
}
if ($tauriConfig.bundle.windows.nsis.installMode -ne "currentUser") {
    throw "tauri.conf.json nsis.installMode should be 'currentUser'"
}
if ($tauriConfig.bundle.windows.nsis.installerHooks -ne "./windows/hooks.nsh") {
    throw "tauri.conf.json missing installerHooks"
}
if ($tauriConfig.bundle.windows.webviewInstallMode.type -ne "skip") {
    Write-Warning "webviewInstallMode should be 'skip' on modern Windows"
}
$gates["I_nsis_hooks"] = "PASS"
```

### Gate J: MCP stdio vs Tauri spawn

**WHAT: Verify backend does not enter stdio MCP mode when spawned by Tauri (stdout piped, not a TTY).**

```python
# Search for isatty() guards in backend code:
$hasTauriGuard = $false
$pyFiles = Get-ChildItem "D:\Dev\repos\$repo\src" -Recurse -Filter "*.py"
foreach ($f in $pyFiles) {
    $content = Get-Content $f.FullName -Raw
    if ($content -match [regex]::Escape($envVar) -and $content -match "isatty") { $hasTauriGuard = $true; break }
}
if (-not $hasTauriGuard) {
    Write-Warning "No ${envVar} / isatty guard found — backend may enter stdio mode when Tauri spawns it"
}
$gates["J_stdio_guard"] = "PASS"
```

```powershell
Write-Host "GATES: all passed"
$results.Phases["gates"] = "PASS"
```

---

## Phase 3: Sidecar smoke test

**WHAT: Build just the PyInstaller exe, run it standalone with PORT + TAURI env vars, verify health + feature endpoint + stderr is clean. This catches 90% of failures in 30s instead of 15min.**

### 3.1 Build sidecar

```powershell
Write-Host "PHASE 3.1: Building PyInstaller sidecar..."
Push-Location "D:\Dev\repos\$repo"
uv run pyinstaller "${repo}-backend.spec" --clean --noconfirm
if ($LASTEXITCODE -ne 0) { throw "PyInstaller failed with exit code $LASTEXITCODE" }

$sidecarExe = "dist\${repo}-backend.exe"
if (-not (Test-Path $sidecarExe)) { throw "Sidecar exe not found at $sidecarExe" }
Write-Host "SIDECAR BUILT: $((Get-Item $sidecarExe).Length / 1MB) MB"

# Copy to native/resources/
Copy-Item $sidecarExe "$nativeDir\resources\${repo}-backend.exe" -Force
Pop-Location
```

### 3.2 Run sidecar, test health + feature route

```powershell
Write-Host "PHASE 3.2: Running sidecar smoke test..."
$env:PORT = "$port"
$env:$envVar = "1"
$p = Start-Process "D:\Dev\repos\$repo\dist\${repo}-backend.exe" -PassThru -WindowStyle Hidden

# Wait for startup
$healthy = $false
for ($i = 0; $i -lt 30; $i++) {
    Start-Sleep 1
    try {
        $r = Invoke-WebRequest "http://127.0.0.1:$port/health" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
        if ($r.StatusCode -eq 200) { $healthy = $true; Write-Host "HEALTH: OK (after ${i}s)"; break }
    } catch {}
}
if (-not $healthy) { Stop-Process -Id $p.Id -Force; throw "Backend not healthy after 30s" }

# Feature route (data endpoint, not just /health)
$featureOk = $false
$featurePaths = @("/api/v1/tools", "/api/v1/diagnostics", "/api/tools", "/api/v1/system/info", "/api/v1/status")
foreach ($fp in $featurePaths) {
    try {
        $r = Invoke-WebRequest "http://127.0.0.1:$port$fp" -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop
        Write-Host "FEATURE $fp: $($r.StatusCode) ($($r.Content.Length) bytes)"; $featureOk = $true; break
    } catch {}
}
if (-not $featureOk) { Write-Warning "No feature route responded — check endpoint paths" }

# Check stderr for failures
$stderrOk = $true
$badPatterns = @("cachetools", "isatty", "webapp/backend", "FileNotFoundError", "_strptime", "Traceback", "Error:")
$logFiles = Get-ChildItem "$env:LOCALAPPDATA\ai.fleet.$repo\logs" -Filter "*.log" -ErrorAction SilentlyContinue
foreach ($lf in $logFiles) {
    $logText = Get-Content $lf.FullName -Tail 50
    foreach ($pat in $badPatterns) {
        if ($logText -match $pat) { Write-Error "STDERR: '$pat' found in $($lf.Name)"; $stderrOk = $false }
    }
}
if ($stderrOk) { Write-Host "STDERR: clean" }

Stop-Process -Id $p.Id -Force; Start-Sleep 1
if (-not $healthy) { throw "Sidecar smoke failed" }
$results.Phases["sidecar_smoke"] = "PASS"
```

---

## Phase 4: Full Tauri build

**WHAT: Build frontend (with tsc gate), then build NSIS installer via Tauri CLI, delete stale shadow exe.**

### 4.1 Build frontend with TypeScript gate

```powershell
Write-Host "PHASE 4.1: Building frontend..."
Push-Location "D:\Dev\repos\$repo\$webDir"
if (-not (Test-Path "package.json")) { throw "No package.json in $webDir" }
npm install --silent 2>$null

# TypeScript check gate
$tscOk = $true
try { npx tsc --noEmit 2>&1 | Out-Null } catch { $tscOk = $false }
if (-not $tscOk) { Write-Warning "tsc --noEmit reported errors — review before releasing" }

npx vite build # or: npm run build
if ($LASTEXITCODE -ne 0) { throw "Frontend build failed" }
Write-Host "FRONTEND: built"
Pop-Location
```

### 4.2 Build NSIS installer

```powershell
Write-Host "PHASE 4.2: Building NSIS installer..."
Push-Location $nativeDir
$env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"

# MSVC environment (try common paths)
$vcvarsPaths = @(
    "C:\Program Files\Microsoft Visual Studio\2022\Community\VC\Auxiliary\Build\vcvars64.bat",
    "C:\Program Files\Microsoft Visual Studio\2022\Professional\VC\Auxiliary\Build\vcvars64.bat",
    "C:\Program Files\Microsoft Visual Studio\2022\Enterprise\VC\Auxiliary\Build\vcvars64.bat"
)
$vcvars = $vcvarsPaths | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $vcvars) { throw "MSVC vcvars64.bat not found — install VS 2022 C++ tools" }

$envOutput = cmd /c "`"$vcvars`" > nul & set" | Where-Object {
    $_ -match '^(INCLUDE|LIB|LIBPATH|VCToolsVersion|WindowsSdkDir|UniversalCRTSdkDir|UCRTVersion)='
}
foreach ($line in $envOutput) {
    $parts = $line.Split('=', 2)
    Set-Item -Path "env:$($parts[0])" -Value $parts[1] -ErrorAction SilentlyContinue
}

npx @tauri-apps/cli build --bundles nsis
if ($LASTEXITCODE -ne 0) { throw "Tauri build failed" }
Pop-Location
```

### 4.3 Delete stale shadow backend

```powershell
$shadowExe = "$nativeDir\target\release\${repo}-backend.exe"
if (Test-Path $shadowExe) {
    Remove-Item -Force $shadowExe
    Write-Host "SHADOW: deleted $shadowExe"
}
```

### 4.4 Locate installer

```powershell
$installer = Get-ChildItem -Path "$nativeDir\target\release\bundle\nsis" -Filter "*setup.exe" |
    Sort-Object LastWriteTime -Descending | Select-Object -First 1
if (-not $installer) { throw "No NSIS installer found in bundle output" }
Write-Host "INSTALLER: $($installer.FullName) ($('{0:N1}' -f ($installer.Length / 1MB)) MB)"
$results.Phases["tauri_build"] = "PASS"
```

---

## Phase 5: Install & verify

**WHAT: Silent-install the NSIS, launch the app, verify health + feature routes + page routes + logs, then uninstall cleanly.**

### 5.1 Kill stale processes and ports

```powershell
Write-Host "PHASE 5.1: Clearing stale processes..."
Get-Process -Name "$repo-native", "$repo-backend" -ErrorAction SilentlyContinue | Stop-Process -Force
@($port, $fePort) | ForEach-Object {
    Get-NetTCPConnection -LocalPort $_ -ErrorAction SilentlyContinue | ForEach-Object {
        Stop-Process -Id $_.OwningProcess -Force -ErrorAction SilentlyContinue
    }
}
Start-Sleep 2
```

### 5.2 Silent install

```powershell
Write-Host "PHASE 5.2: Installing NSIS..."
$installResult = Start-Process -FilePath $installer.FullName -ArgumentList "/S" -Wait -PassThru
if ($installResult.ExitCode -ne 0) { throw "Installer exited with code $($installResult.ExitCode)" }
Write-Host "INSTALL: OK (exit code 0)"
```

### 5.3 Launch app

```powershell
Write-Host "PHASE 5.3: Launching installed app..."
# Find the installed binary
$searchPaths = @(
    "$env:LOCALAPPDATA\$productName\$mainBinary.exe",
    "$env:LOCALAPPDATA\$identifier\$mainBinary.exe",
    "$env:PROGRAMDATA\$productName\$mainBinary.exe"
)
$appPath = $searchPaths | Where-Object { Test-Path $_ } | Select-Object -First 1
if (-not $appPath) {
    $appPath = Get-ChildItem -Path "$env:LOCALAPPDATA" -Recurse -Filter "$mainBinary.exe" -ErrorAction SilentlyContinue |
        Select-Object -First 1 -ExpandProperty FullName
}
if (-not $appPath) { throw "Installed $mainBinary.exe not found" }
Write-Host "APP PATH: $appPath"
$appProcess = Start-Process -FilePath $appPath -PassThru
```

### 5.4 Wait for backend health

```powershell
Write-Host "PHASE 5.4: Waiting for backend health..."
$backendHealthy = $false
for ($i = 0; $i -lt 60; $i++) {
    Start-Sleep 1
    try {
        $r = Invoke-WebRequest "http://127.0.0.1:$port/health" -UseBasicParsing -TimeoutSec 2 -ErrorAction Stop
        if ($r.StatusCode -eq 200) { $backendHealthy = $true; Write-Host "HEALTH: OK (after ${i}s)"; break }
    } catch {}
}
if (-not $backendHealthy) {
    Stop-Process -Id $appProcess.Id -Force -ErrorAction SilentlyContinue
    throw "Backend not healthy after 60s"
}
```

### 5.5 Verify feature route

```powershell
Write-Host "PHASE 5.5: Verifying feature route..."
$featureOk = $false
$featurePaths = @("/api/v1/tools", "/api/v1/diagnostics", "/api/tools", "/api/v1/status")
foreach ($fp in $featurePaths) {
    try {
        $r = Invoke-WebRequest "http://127.0.0.1:$port$fp" -UseBasicParsing -TimeoutSec 3 -ErrorAction Stop
        Write-Host "FEATURE $fp: $($r.StatusCode) ($($r.Content.Length) bytes)"
        $featureOk = $true; break
    } catch {}
}
if (-not $featureOk) { Write-Warning "No feature route responded" }
```

### 5.6 Check backend logs for errors

```powershell
Write-Host "PHASE 5.6: Checking backend logs..."
$logFiles = Get-ChildItem "$env:LOCALAPPDATA\$identifier\logs" -Filter "*.log" -ErrorAction SilentlyContinue
$logErrors = @()
foreach ($lf in $logFiles) {
    $lines = Get-Content $lf.FullName -Tail 50
    $logErrors += $lines | Select-String -Pattern "Traceback|Error:|CRITICAL|cachetools|isatty|_strptime|FileNotFoundError"
}
if ($logErrors) {
    Write-Warning "Log errors found:"
    $logErrors | ForEach-Object { Write-Warning "  $_" }
} else {
    Write-Host "LOGS: clean"
}
```

### 5.7 Page-level verification

**WHAT: Verify each frontend route returns 200 (SPA fallback working) and no route is broken. Then use Playwright to check the actual WebView for console errors.**

```powershell
Write-Host "PHASE 5.7: Page route verification..."
$routes = @("/", "/dashboard", "/tools", "/chat", "/settings", "/help", "/logs", "/apps", "/skills")
$routeFailures = @()
foreach ($route in $routes) {
    try {
        $r = Invoke-WebRequest "http://127.0.0.1:$port$route" -UseBasicParsing -TimeoutSec 5
        if ($r.StatusCode -eq 200) {
            Write-Host "  ROUTE $route : 200 ($('{0:N0}' -f $r.Content.Length) bytes)"
        } elseif ($r.StatusCode -eq 404) {
            Write-Host "  ROUTE $route : 404 (missing SPA fallback?)"
            $routeFailures += $route
        } else {
            Write-Host "  ROUTE $route : $($r.StatusCode)"
            $routeFailures += $route
        }
    } catch {
        Write-Host "  ROUTE $route : unreachable ($($_.Exception.Message))"
    }
}
if ($routeFailures) { Write-Warning "Route failures: $($routeFailures -join ', ')" }
```

### 5.8 Uninstall

```powershell
Write-Host "PHASE 5.8: Uninstalling..."
$uninstaller = Get-ChildItem -Path "$env:LOCALAPPDATA" -Recurse -Filter "uninstall*.exe" -ErrorAction SilentlyContinue |
    Where-Object { $_.FullName -match [regex]::Escape($productName) } |
    Select-Object -First 1 -ExpandProperty FullName
if (-not $uninstaller) {
    $uninstaller = Get-ChildItem -Path "$env:LOCALAPPDATA" -Recurse -Filter "uninstall*.exe" -ErrorAction SilentlyContinue |
        Select-Object -First 1 -ExpandProperty FullName
}
if ($uninstaller) {
    Stop-Process -Name "$repo-native", "$repo-backend" -Force -ErrorAction SilentlyContinue
    Start-Sleep 2
    $uninstallResult = Start-Process -FilePath $uninstaller -ArgumentList "/S" -Wait -PassThru
    if ($uninstallResult.ExitCode -eq 0) { Write-Host "UNINSTALL: OK" }
    else { Write-Warning "Uninstall exited with code $($uninstallResult.ExitCode)" }
} else {
    Write-Warning "Uninstaller not found — may need manual cleanup"
}
$results.Phases["install_verify"] = "PASS"
```

---

## Phase 6: Results report

**WHAT: Print a structured pass/fail summary of every gate and phase.**

```powershell
Write-Host "`n========================================"
Write-Host " NSIS BUILD RESULTS — $repo"
Write-Host "========================================"
Write-Host " Installer: $($installer.FullName)"
Write-Host " Size:      $('{0:N1}' -f ($installer.Length / 1MB)) MB"
Write-Host " Port:      $port"
Write-Host "`n-- Gates --"
$results.Gates.Keys | Sort-Object | ForEach-Object {
    $icon = if ($results.Gates[$_] -eq "PASS") { "V" } else { "X" }
    Write-Host "  $icon $_"
}
Write-Host "`n-- Phases --"
$results.Phases.Keys | Sort-Object | ForEach-Object {
    $icon = if ($results.Phases[$_] -eq "PASS") { "V" } else { "X" }
    Write-Host "  $icon $_"
}
$allPassed = ($results.Gates.Values -notcontains "FAIL") -and ($results.Phases.Values -notcontains "FAIL")
Write-Host "`nOVERALL: $(if ($allPassed) { 'ALL PASSED V' } else { 'SOME FAILED X' })"
Write-Host "========================================`n"
```

---

## Phase 7: Failure playbook

**WHAT: When a phase fails, look up the symptom here for the exact cause and fix.**

| Symptom | Likely cause | Fix at phase |
|---------|-------------|-------------|
| Installer hangs at "Installing..." | NSIS hooks not killing backend.exe | Gate I — add hooks.nsh |
| WebView loads but blank/error | CORS missing tauri.localhost | Gate C — add CORS origins |
| WebView loads but blank/error | API_BASE still relative in prod | Gate B — set absolute URL |
| WebView loads but blank/error | CSP connect-src missing backend port | Gate B — add to tauri.conf.json |
| Backend not healthy after install | Stale shadow exe in target/release/ | Phase 4.3 — delete it |
| Backend not healthy after install | run_server.py chdir when frozen | Gate D — frozen-safe pattern |
| Backend not healthy after install | Missing cachetools hiddenimport | Gate E — add to spec |
| `Failed to fetch` on some pages | _strptime/_datetime not eager-imported | Gate D — add to run_server.py |
| `No module named 'difflib'` | noarchive=False in spec | Gate E — set noarchive=True |
| `/app/` returns 404 JSON | Starlette realpath on _MEIPASS path | See pitfalls.md §E2 — SPAStaticFiles |
| Dynamic routes 404 (e.g. /books/123) | StaticFiles has no SPA fallback | See pitfalls.md §E2 — SPAStaticFiles |
| PyInstaller build locked (Win32 32) | Orphan process holds file lock | Phase 0.3 — kill all before rebuild |
| Frontend build fails | TypeScript compilation errors | Phase 4.1 — fix tsc errors |
| Frontend routes return 404 | SPA not built or wrong dist path | Phase 4.1 — check npm run build output |

---

## Reference: per-repo variables

| Repo | Port | Identifier | Env var |
|------|------|-----------|---------|
| pywinauto-mcp | 10789 | ai.fleet.pywinauto-mcp | PYWINAUTO_TAURI |
| calibre-mcp | 10720 | ai.fleet.calibre-mcp | CALIBRE_TAURI |
| plex-mcp | 10740 | ai.fleet.plex-mcp | PLEX_TAURI |
| email-mcp | 10813 | ai.fleet.email-mcp | EMAIL_TAURI |
| bookmarks-mcp | 10803 | ai.fleet.bookmarks-mcp | BOOKMARKS_TAURI |
| freecad-mcp | 10944 | ai.fleet.freecad-mcp | FREECAD_TAURI |
| qcad-mcp | 10966 | ai.fleet.qcad-mcp | QCAD_TAURI |

For new repos: allocate from `operations/WEBAPP_PORTS.md`. Adjacent pair (backend N, frontend N+1).
