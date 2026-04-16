# Apple Development Project

iOS/iPadOS/macOS app development using Cursor IDE with Xcode 26.1 integration, focusing on Apple Intelligence applications.

## Project Overview

This project is set up for developing Apple Intelligence-powered applications across iOS, iPadOS, and macOS platforms using:
- **Cursor IDE** - Primary development environment with AI assistance
- **Xcode 26.1** - Final build, debugging, and release tool
- **Swift** - Primary programming language
- **Apple Intelligence APIs** - Foundation Models, Writing Tools, App Intents

## Developer Setup

### Hardware
- **M1 MacBook** - Apple Silicon (Apple Intelligence compatible)
- **M4 MacBook** - Latest Apple Silicon (full Apple Intelligence support)
- **Apple Developer Account** - $99/year membership (active)

### Advantages
- **Apple Intelligence Support** - Both M1 and M4 support Apple Intelligence features
- **Native Performance** - Apple Silicon optimized development
- **Test Coverage** - Can test on both M1 and M4 architectures
- **App Store Distribution** - Developer account enables App Store publishing

## Quick Start

### 🚀 Setup Checklists

- **📋 Complete Checklist:** See [`SETUP_CHECKLIST.md`](SETUP_CHECKLIST.md) for detailed step-by-step setup instructions
- **⚡ Quick Start:** See [`SETUP_QUICK_START.md`](SETUP_QUICK_START.md) for fast-track setup guide

### Prerequisites

1. **macOS** (required for Apple development) ✅ M1 & M4 MacBooks
2. **Xcode 26.1** - Install from Mac App Store
3. **Cursor IDE** - Download from [cursor.com](https://cursor.com)
4. **Homebrew** - Package manager for macOS
5. **Apple Developer Account** ✅ Active ($99/year)
6. **Git** - Version control (standard for Apple development)

### Initial Setup

```bash
# Install Homebrew (if not already installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install essential development tools
brew install xcode-build-server xcbeautify swiftformat

# Install Cursor extensions:
# 1. Swift Language Support
# 2. Sweetpad (Xcode integration)
```

**📝 For complete setup instructions, see [`SETUP_CHECKLIST.md`](SETUP_CHECKLIST.md)**

### Project Structure

```
apple-test/
├── docs/                    # Documentation
│   ├── setup-guide.md      # Detailed setup instructions
│   ├── workflow.md          # Development workflow
│   ├── apple-intelligence.md # Apple Intelligence integration
│   └── tools.md            # Development tools reference
├── src/                     # Source code (to be created)
├── tests/                   # Test files (to be created)
├── buildServer.json         # Sweetpad configuration (generated)
├── .gitignore              # Git ignore rules
└── README.md               # This file
```

## Version Control

**Git/GitHub is standard** for Apple development. There's no special Apple version control system.

- **Git** - Built into Xcode, also available via command line
- **GitHub** - Most common hosting platform for Apple projects
- **Xcode Integration** - Xcode has built-in Git support
- **Alternatives** - Mercurial and Subversion exist but are rarely used

**Recommended Setup:**
```bash
# Initialize Git repository
git init

# Configure Git (if not already done)
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"

# Add remote (GitHub, GitLab, etc.)
git remote add origin https://github.com/yourusername/yourrepo.git
```

## Development Workflow

1. **Primary Development** - Use Cursor IDE
   - Write code with AI assistance
   - Use Sweetpad for building/testing
   - Leverage Swift Language Support for completion
   - Commit changes to Git

2. **Finalization** - Use Xcode
   - Open project in Xcode for advanced debugging
   - Build for release
   - Archive and distribute via App Store Connect

3. **Synchronization** - Keep Cursor and Xcode in sync
   - Files added in Cursor may need manual addition to Xcode
   - Use XcodeGen for automated project generation (optional)
   - Use Git for version control across both environments

## Mac Requirements

**Do you need Mac running all the time?**
- ❌ **No** - Code on Windows (Cursor), build on Mac when needed
- ✅ **Simulator testing** - iOS Simulator included with Xcode (no physical device needed)
- ✅ **Mac only needed** - When building/testing, not when coding

See `docs/mac-requirements.md` for complete details.

## Documentation

See the `docs/` folder for detailed guides:
- **setup-guide.md** - Complete environment setup
- **workflow.md** - Development workflow patterns
- **apple-intelligence.md** - Apple Intelligence integration guide
- **tools.md** - Development tools reference
- **version-control.md** - Git/GitHub setup and workflow
- **publishing-guide.md** - App Store vs EU alternative stores publishing
- **project-ideas.md** - AI project ideas and opportunities
- **mac-requirements.md** - Mac requirements and simulator testing

## Apple Intelligence Features

This project focuses on integrating:
- **Foundation Models Framework** - On-device AI capabilities
- **Writing Tools** - Text rewriting, proofreading, summarization
- **Image Playground API** - Context-aware image generation
- **App Intents** - Siri, Spotlight, Widget integration

## Resources

- [Apple Developer - Apple Intelligence](https://developer.apple.com/apple-intelligence/)
- [Cursor Swift Guide](https://docs.cursor.com/en/guides/languages/swift)
- [Foundation Models Framework Documentation](https://developer.apple.com/documentation/foundationmodels)
- [App Intents Documentation](https://developer.apple.com/documentation/appintents)

## Notes

- Comprehensive research and patterns stored in Advanced Memory
- See `development/apple/` folder in Advanced Memory for detailed guides
- Regular updates as Apple Intelligence evolves

## License

[Add your license here]

