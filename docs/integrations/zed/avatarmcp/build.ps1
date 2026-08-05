# AvatarMCP Zed Extension Build Script (Windows)
rustup target add wasm32-wasip1
Write-Host \"Building AvatarMCP Zed extension...\" -ForegroundColor Green
cargo build --release --target wasm32-wasip1

if ($LASTEXITCODE -eq 0) {
    Write-Host \"OK Build successful!\" -ForegroundColor Green
    Write-Host \"Install via: Zed → Extensions → Install Dev Extension\" -ForegroundColor Cyan
    Write-Host \"Select this directory: $PWD\" -ForegroundColor Cyan
} else {
    Write-Host \"✗ Build failed\" -ForegroundColor Red
    exit 1
}
