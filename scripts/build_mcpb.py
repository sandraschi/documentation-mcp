#!/usr/bin/env python3
"""
Build MCPB package for docs-mcp server
"""

import zipfile
from pathlib import Path


def build_mcpb_package():
    """Build MCPB package for docs-mcp"""

    # Paths
    repo_root = Path(__file__).parent.parent
    dist_dir = repo_root / "dist"
    src_dir = repo_root / "src"

    # Create dist directory
    dist_dir.mkdir(exist_ok=True)

    # Package info
    package_name = "docs-mcp"
    version = "1.0.0"
    package_file = dist_dir / f"{package_name}-{version}.mcpb"

    print(f"Building MCPB package: {package_file}")

    # Create ZIP archive
    with zipfile.ZipFile(package_file, "w", zipfile.ZIP_DEFLATED) as zipf:
        # Add manifest.json
        manifest_path = repo_root / "manifest.json"
        if manifest_path.exists():
            zipf.write(manifest_path, "manifest.json")
            print("✓ Added manifest.json")

        # Add source files
        docs_mcp_dir = src_dir / "docs_mcp"
        if docs_mcp_dir.exists():
            for file_path in docs_mcp_dir.rglob("*"):
                if file_path.is_file():
                    arcname = str(file_path.relative_to(src_dir))
                    zipf.write(file_path, arcname)
            print("✓ Added docs_mcp source files")

        # Add pyproject.toml
        pyproject_path = repo_root / "pyproject.toml"
        if pyproject_path.exists():
            zipf.write(pyproject_path, "pyproject.toml")
            print("✓ Added pyproject.toml")

        # Add README
        readme_path = repo_root / "README_DOCS_MCP.md"
        if readme_path.exists():
            zipf.write(readme_path, "README.md")
            print("✓ Added README.md")

    print(f"✅ MCPB package built successfully: {package_file}")
    print(f"📦 Size: {package_file.stat().st_size / 1024:.1f} KB")

    return package_file


if __name__ == "__main__":
    build_mcpb_package()
