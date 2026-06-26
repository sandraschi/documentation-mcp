# SOTA CLI Tooling Integration

This document outlines the standard CLI toolset integrated into the MCP development environment. These tools are selected for their performance, reliability, and "force multiplier" effect on agentic development workflows.

## Core Infrastructure

### [uv](https://github.com/astral-sh/uv)
- **Description**: Extremely fast Python package and project manager, written in Rust.
- **Role**: Primary dependency manager. Used for scaffolding libraries and managing virtual environments with zero overhead.

### [gh (GitHub CLI)](https://github.com/cli/cli)
- **Description**: The official command-line interface for GitHub.
- **Role**: Orchestrates repository lifecycle, CI/CD monitoring, and issue/PR management directly from the terminal.

## Search & Discovery

### [ripgrep (rg)](https://github.com/BurntSushi/ripgrep)
- **Description**: A line-oriented search tool that recursively searches the current directory for a regex pattern.
- **Role**: High-speed workspace auditing. Essential for finding patterns across thousands of files without delay.

### [fd](https://github.com/sharkdp/fd)
- **Description**: A simple, fast, and user-friendly alternative to `find`.
- **Role**: Used for rapid file discovery and path matching. Superior performance in deep directory trees.

### [fzf](https://github.com/junegunn/fzf)
- **Description**: A general-purpose command-line fuzzy finder.
- **Role**: Interactive path selection and fuzzy search integration for terminal workflows.

## Inspection & Processing

### [jq](https://github.com/jqlang/jq)
- **Description**: Lightweight and flexible command-line JSON processor.
- **Role**: Mandatory for filtering and transforming JSON outputs from MCP tools and APIs.

### [bat](https://github.com/sharkdp/bat)
- **Description**: A `cat` clone with wings (syntax highlighting and Git integration).
- **Role**: Code preview and inspection. Provides immediate visual clarity when reviewing file contents in the terminal.

### [tokei](https://github.com/XAMPPRocky/tokei)
- **Description**: A program that displays statistics about your code (LOC, language breakdown).
- **Role**: Workspace auditing and project scale assessment.

## Visualization

### [delta](https://github.com/dandavison/delta)
- **Description**: A syntax-highlighting pager for git, diff, and grep output.
- **Role**: Human-readable diffing and code comparison.

### [eza](https://github.com/eza-community/eza)
- **Description**: A modern, maintained replacement for `ls`.
- **Role**: Visual directory exploration with Git integration and enhanced metadata display.

---
**Standard Installation (Windows)**:
```powershell
winget install sharkdp.fd jqlang.jq sharkdp.bat dandavison.delta junegunn.fzf XAMPPRocky.tokei eza-community.eza BurntSushi.ripgrep.MSVC
```
