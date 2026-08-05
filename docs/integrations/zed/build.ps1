# Advanced Memory MCP Zed Extension Build Script (Windows)
rustup target add wasm32-wasip1
Write-Host \ Building Advanced Memory MCP Zed extension...\ -ForegroundColor Green
cargo build --release --target wasm32-wasip1

if ( -eq 0) {
    Write-Host \OK Build successful!\ -ForegroundColor Green
    Write-Host \Install via: Zed → Extensions → Install Dev Extension\ -ForegroundColor Cyan
    Write-Host \Select this directory: D:\Dev\repos\mcp-central-docs\integrations\zed\ -ForegroundColor Cyan
} else {
    Write-Host \✗ Build failed\ -ForegroundColor Red
    exit 1
}
