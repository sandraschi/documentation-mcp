# Blender MCP Zed Extension Build Script (Windows)
rustup target add wasm32-wasip1
Write-Host "Building Blender MCP Zed extension..." -ForegroundColor Green
cargo build --release --target wasm32-wasip1

if ($LASTEXITCODE -eq 0) {
    Write-Host "âœ“ Build successful!" -ForegroundColor Green
    Write-Host "Install via: Zed â†’ Extensions â†’ Install Dev Extension" -ForegroundColor Cyan
    Write-Host "Select this directory: $PWD" -ForegroundColor Cyan
} else {
    Write-Host "âœ- Build failed" -ForegroundColor Red
    exit 1
}
