# ==============================================================
# run_codellama_4bit_auto.ps1
# ==============================================================
# 1️⃣ Install Ollama (if missing)
# 2️⃣ Install Python + bitsandbytes (if missing)
# 3️⃣ Download & quantise CodeLlama‑34B (code‑instruction) to 4‑bit NF‑4
# 4️⃣ Auto‑remove any old non‑quantised model
# 5️⃣ Auto‑add the new 4‑bit model with the same public name
# 6️⃣ Start an interactive chat
# ==============================================================

# ------------------- Helper functions --------------------------
function Test-Command {
    param([string]$cmd)
    return (Get-Command $cmd -ErrorAction SilentlyContinue) -ne $null
}

# ------------------- 1️⃣ Install Ollama -----------------------
if (-not (Test-Command ollama)) {
    Write-Host "Ollama not found. Installing..." -ForegroundColor Yellow
    $installer = "$env:TEMP\ollama_windows.exe"
    Write-Host "Downloading installer..." -ForegroundColor Cyan
    Invoke-WebRequest -Uri "https://ollama.com/download/ollama_windows.exe" -OutFile $installer
    Write-Host "Running installer..." -ForegroundColor Cyan
    Start-Process -FilePath $installer -ArgumentList "/S" -Wait
    Remove-Item $installer -Force
    # Ensure Ollama is in PATH
    $ollamaPath = "$env:ProgramFiles\ollama"
    if (-not (Test-Command ollama) -and (Test-Path $ollamaPath)) {
        $env:PATH += ";$ollamaPath"
    }
}

# ------------------- 2️⃣ Install Python & bitsandbytes -------
if (-not (Test-Command python)) {
    Write-Host "Python 3.10+ not found. Please install it and add 'python' to PATH." -ForegroundColor Red
    exit 1
}
if (-not (Test-Command pip)) {
    Write-Host "pip not found. Installing via ensurepip..." -ForegroundColor Yellow
    python -m ensurepip --upgrade
}
$bitsandbytesPresent = $false
try { python -c "import bitsandbytes" 2>$null; $bitsandbytesPresent = $true } catch {}
if (-not $bitsandbytesPresent) {
    Write-Host "Installing bitsandbytes (CUDA 12+)..." -ForegroundColor Cyan
    pip install --upgrade bitsandbytes==0.41.2
}

# ------------------- 3️⃣ Quantise the model -------------------
$modelName        = "codellama/CodeLlama-34b-hf"
$quantDir         = ".\codellama-34b-4bit"
$publicName       = "codellama:34b-codeinstruct"   # name used in Ollama

# Clean any previous quantised folder
if (Test-Path $quantDir) {
    Write-Host "Removing old quantised folder $quantDir..." -ForegroundColor Yellow
    Remove-Item -Recurse -Force $quantDir
}
New-Item -ItemType Directory -Path $quantDir | Out-Null

# Python script to perform quantisation
$pyScript = @'
import sys
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

model_name = "codellama/CodeLlama-34b-hf"
output_dir = Path(sys.argv[1])

# 4‑bit NF‑4 config
bnb_cfg = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
)

# Load on GPU (auto‑place)
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_cfg,
    device_map="auto",
    trust_remote_code=True,
)

tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=False)

# Save both
model.save_pretrained(output_dir)
tokenizer.save_pretrained(output_dir)

print(f"✅ 4‑bit model saved to {output_dir}")
'@

# Write & run script
$tempPy = "$env:TEMP\quantise_codellama.py"
Set-Content -Path $tempPy -Value $pyScript -Encoding UTF8
Write-Host "Quantising model - this may take ~30‑60 s (GPU)..." -ForegroundColor Cyan
& python $tempPy $quantDir
Remove-Item $tempPy -Force

# ------------------- 4️⃣ Auto‑remove old non‑quantised model ----------
$existingModels = ollama list --format json | ConvertFrom-Json
$oldExists = ($existingModels | Where-Object { $_.model -eq $publicName }).Count -gt 0

if ($oldExists) {
    Write-Host "Removing existing non‑quantised model `$publicName`..." -ForegroundColor Yellow
    try { ollama rm $publicName -y } catch {
        Write-Host "  ❌  Could not remove - maybe already deleted." -ForegroundColor Red
    }
} else {
    Write-Host "No pre‑existing non‑quantised model found. Skipping deletion." -ForegroundColor Green
}

# ------------------- 5️⃣ Register the 4‑bit model --------------------
Write-Host "Registering 4‑bit model as `$publicName`..." -ForegroundColor Cyan
ollama add $publicName $quantDir

# ------------------- 6️⃣ Interactive session ------------------------
Write-Host "`n🎉 4‑bit CodeLlama ready!  Type `exit` or press Ctrl‑C to quit." -ForegroundColor Green
ollama run $publicName
