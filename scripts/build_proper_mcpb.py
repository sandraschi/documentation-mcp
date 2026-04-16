#!/usr/bin/env python3
"""
Build proper MCPB package for docs-mcp server according to MCPB standards
"""

import shutil
import zipfile
from pathlib import Path


def build_proper_mcpb_package():
    """Build MCPB package following MCPB standards - NO dependencies, extensive prompts"""

    # Paths
    repo_root = Path(__file__).parent.parent
    dist_dir = repo_root / "dist"
    src_dir = repo_root / "src"
    assets_dir = repo_root / "assets"

    # Create clean build directory
    build_dir = dist_dir / "build"
    if build_dir.exists():
        shutil.rmtree(build_dir)
    build_dir.mkdir(parents=True)

    # Package info
    package_name = "docs-mcp"
    version = "1.0.0"
    package_file = dist_dir / f"{package_name}-{version}.mcpb"

    print(f"Building proper MCPB package: {package_file}")

    # Create proper MCPB structure
    mcp_server_dir = build_dir / "docs-mcp"
    mcp_server_dir.mkdir()

    # Copy manifest.json (proper MCPB format)
    manifest_src = repo_root / "manifest.json"
    manifest_dst = mcp_server_dir / "manifest.json"
    if manifest_src.exists():
        shutil.copy2(manifest_src, manifest_dst)
        print("✓ Added manifest.json")

    # Copy assets directory (prompts are REQUIRED)
    if assets_dir.exists():
        assets_dst = mcp_server_dir / "assets"
        shutil.copytree(assets_dir, assets_dst)
        print("✓ Added assets/ directory with extensive prompts")

    # Copy source code ONLY (no dependencies)
    docs_mcp_src = src_dir / "docs_mcp"
    if docs_mcp_src.exists():
        src_dst = mcp_server_dir / "src" / "docs_mcp"
        src_dst.parent.mkdir(parents=True)
        shutil.copytree(docs_mcp_src, src_dst)
        print("✓ Added source code (no dependencies)")

    # Copy README.md
    readme_src = repo_root / "README_DOCS_MCP.md"
    readme_dst = mcp_server_dir / "README.md"
    if readme_src.exists():
        shutil.copy2(readme_src, readme_dst)
        print("✓ Added README.md")

    # Verify required files
    required_files = [
        "manifest.json",
        "assets/prompts/system.md",
        "assets/prompts/user.md",
        "assets/prompts/examples.json",
        "src/docs_mcp/server.py",
        "README.md",
    ]

    missing_files = []
    for file_path in required_files:
        full_path = mcp_server_dir / file_path
        if not full_path.exists():
            missing_files.append(file_path)

    if missing_files:
        print(f"❌ Missing required files: {missing_files}")
        return None

    # Create ZIP archive
    with zipfile.ZipFile(package_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        # Add all files in build directory
        for file_path in mcp_server_dir.rglob("*"):
            if file_path.is_file():
                arcname = str(file_path.relative_to(build_dir))
                zipf.write(file_path, arcname)

    # Calculate sizes
    package_size = package_file.stat().st_size
    prompt_size = sum(f.stat().st_size for f in (mcp_server_dir / "assets" / "prompts").rglob("*") if f.is_file())

    print(f"✅ MCPB package built successfully: {package_file}")
    print(f"📦 Total Size: {package_size / 1024:.1f} KB")
    print(f"📝 Prompts Size: {prompt_size / 1024:.1f} KB")
    print(f"📁 Files: {len(list(mcp_server_dir.rglob('*')))}")

    # Verify package structure
    print("\n🔍 Package Structure:")
    for root, _dirs, files in os.walk(mcp_server_dir):
        level = root.replace(str(mcp_server_dir), "").count(os.sep)
        indent = " " * 2 * level
        print(f"{indent}{os.path.basename(root)}/")
        subindent = " " * 2 * (level + 1)
        for file in files:
            print(f"{subindent}{file}")

    # Cleanup build directory
    shutil.rmtree(build_dir)

    return package_file


if __name__ == "__main__":
    import os

    build_proper_mcpb_package()
