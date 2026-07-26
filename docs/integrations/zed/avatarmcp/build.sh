#!/bin/bash
rustup target add wasm32-wasip1
echo \"Building AvatarMCP Zed extension...\"
cargo build --release --target wasm32-wasip1

if [ $? -eq 0 ]; then
    echo \"✓ Build successful!\"
    echo \"Install via: Zed → Extensions → Install Dev Extension\"
    echo \"Select this directory: $(pwd)\"
else
    echo \"✗ Build failed\"
    exit 1
fi
