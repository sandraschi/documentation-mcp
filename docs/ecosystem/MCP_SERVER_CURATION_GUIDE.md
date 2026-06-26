# MCP Server Curation Guide

## Overview

You have **58 auto-discovered MCP servers** in your workspace. This guide helps you curate them into a **high-quality showcase monorepo** by applying quality standards and inclusion criteria.

## Quick Curation Process

### Step 1: Get Server Inventory
```bash
# Run the analysis script to see all discovered servers
cd myhomeserver
python analyze_mcp_servers.py

# This shows you the breakdown by category
```

### Step 2: Apply Quality Filters

#### Filter 1: Remove Stub/Trivial Servers
**Reject if:**
- Only 1-2 tools with minimal functionality
- Contains extensive TODO comments
- Appears to be just a template or placeholder
- No real integration with actual systems

**Example Rejects:**
- `hello-world-mcp` (just returns "Hello World")
- `template-mcp` (unmodified scaffold)
- `experimental-mcp` (proof-of-concept only)

#### Filter 2: Remove Incomplete Implementations
**Reject if:**
- Core functionality is missing or broken
- No error handling or edge cases covered
- Dependencies are missing or broken
- Server crashes on basic operations

#### Filter 3: Remove Duplicates
**Reject if:**
- Provides same functionality as existing server
- Redundant capabilities (e.g., 5th weather server)
- Overlapping tools with better implementations

#### Filter 4: Check Maturity
**Reject if:**
- Less than 1 week old (too new/unstable)
- No commits in 3+ months (unmaintained)
- Breaking changes in recent commits
- Still in heavy development phase

### Step 3: Categorize Accepted Servers

#### Tier 1: Showcase Servers (Premium)
**Criteria:**
- Production-ready with comprehensive testing
- Extensive documentation and examples
- Active maintenance (< 1 month since last commit)
- Real-world utility with meaningful tools
- Passes all quality gates

**Target: 20-25 servers**
```
✅ devices-mcp      (Smart Home - Your proven camera integration)
✅ ring-mcp            (Security - Your working Ring cameras)
✅ blender-mcp         (Creative - Mature 3D software)
✅ docker-mcp          (DevOps - Essential container management)
✅ plex-mcp            (Media - Production media server)
✅ home-assistant-mcp  (Smart Home - Your Nest integration)
✅ netatmo-weather-mcp (Weather - Your weather station)
```

#### Tier 2: Community Servers (Standard)
**Criteria:**
- Functional but may need minor improvements
- Basic documentation and testing
- Reasonable maintenance activity
- Useful but not showcase-quality

**Target: 15-20 servers**
```
⚠️  gimp-mcp           (Creative - Good but basic)
⚠️  git-mcp            (Development - Functional but simple)
⚠️  some-weather-mcp   (Weather - Works but duplicate)
```

#### Tier 3: Experimental (Separate Repo)
**Move to experimental repository:**
```
❌ experimental-ai-mcp  (Too incomplete)
❌ stub-server-mcp      (Just placeholder code)
❌ duplicate-weather-mcp (5th weather server)
❌ unmaintained-mcp     (No commits in 6 months)
```

## Your Expected Results

From your **58 discovered servers**, you should expect:

- **✅ Include: 30-40 servers** (52-69% acceptance rate)
- **⚠️ Improve: 10-15 servers** (need work before inclusion)
- **❌ Exclude: 10-15 servers** (not suitable for curated repo)

## Practical Curation Script

```python
#!/usr/bin/env python3
"""
Server Curation Script - Evaluate discovered MCP servers for inclusion
"""

import os
import json
import subprocess
from pathlib import Path

def curate_servers():
    """Curate discovered MCP servers for monorepo inclusion"""

    # Load your discovered servers (from your analyze_mcp_servers.py output)
    discovered_servers = get_discovered_servers()

    curated = {
        "tier_1_showcase": [],
        "tier_2_community": [],
        "tier_3_experimental": [],
        "rejected": []
    }

    for server in discovered_servers:
        assessment = assess_server_quality(server)

        if assessment["score"] >= 8:
            curated["tier_1_showcase"].append(server)
        elif assessment["score"] >= 6:
            curated["tier_2_community"].append(server)
        elif assessment["score"] >= 4:
            curated["tier_3_experimental"].append(server)
        else:
            curated["rejected"].append(server)

    print(f"Curation Results:")
    print(f"Tier 1 (Showcase): {len(curated['tier_1_showcase'])} servers")
    print(f"Tier 2 (Community): {len(curated['tier_2_community'])} servers")
    print(f"Tier 3 (Experimental): {len(curated['tier_3_experimental'])} servers")
    print(f"Rejected: {len(curated['rejected'])} servers")

    return curated

def assess_server_quality(server):
    """Assess server quality with scoring system"""
    score = 0
    reasons = []

    # Check code quality
    if has_tests(server): score += 2
    if has_docs(server): score += 2
    if passes_lint(server): score += 1

    # Check functionality
    tool_count = get_tool_count(server)
    if tool_count >= 5: score += 2
    elif tool_count >= 3: score += 1

    # Check maintenance
    if is_recently_updated(server): score += 1
    if has_active_maintainer(server): score += 1

    # Check uniqueness
    if not is_duplicate(server): score += 1

    return {"score": score, "reasons": reasons}

if __name__ == "__main__":
    results = curate_servers()

    # Save curation results
    with open("server_curation_results.json", "w") as f:
        json.dump(results, f, indent=2)

    print("Curation complete! Check server_curation_results.json")
```

## Implementation Checklist

### Week 1: Assessment
- [ ] Run analysis on all 58 discovered servers
- [ ] Apply quality criteria to each server
- [ ] Document assessment results
- [ ] Create initial inclusion/exclusion lists

### Week 2: Curation
- [ ] Review borderline cases with team
- [ ] Finalize tier assignments
- [ ] Plan improvement roadmap for Tier 2 servers
- [ ] Set up experimental repository for Tier 3

### Week 3: Implementation
- [ ] Create showcase monorepo structure
- [ ] Move curated servers to appropriate locations
- [ ] Set up CI/CD for included servers
- [ ] Update documentation and README

### Week 4: Launch
- [ ] Test monorepo functionality
- [ ] Create interoperability demos
- [ ] Publish initial release
- [ ] Announce to MCP community

## Quality Metrics

### Inclusion Rate Goals
- **Overall Acceptance**: 50-70% of discovered servers
- **Tier 1 Ratio**: 30-40% of accepted servers
- **Tier 2 Ratio**: 40-50% of accepted servers
- **Tier 3 Ratio**: 20-30% of accepted servers

### Quality Benchmarks
- **Average Tool Count**: > 3 tools per server
- **Test Coverage**: > 70% for Tier 1 servers
- **Documentation Score**: > 80% completeness
- **Maintenance Activity**: < 30 days since last commit

## Maintenance Strategy

### Ongoing Curation
- **Monthly Reviews**: Assess new server submissions
- **Quarterly Audits**: Re-evaluate existing servers
- **Community Feedback**: Incorporate user reports
- **Quality Improvements**: Help Tier 2 servers reach Tier 1

### Server Lifecycle
- **New Servers**: 30-day evaluation period
- **Tier Promotions**: Based on quality improvements
- **Deprecation**: Clear process for unmaintained servers
- **Archival**: Move inactive servers to separate repository

This curation process ensures your MCP monorepo maintains high quality while maximizing the value of your 58 discovered servers!
