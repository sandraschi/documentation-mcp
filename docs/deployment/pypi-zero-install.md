# PyPI Zero-Install & Industrial Releases (OIDC)

**Status:** SOTA v14.0 Component  
**Substrate:** PyPI.org (Public)  
**Standard:** MIT License

To achieve universal, IDE-agnostic **Zero-Install** capabilities for the fleet, we utilize PyPI as the primary distribution layer. This replaces the limiting, desktop-only `.mcpb` standard with a globally cached, versioned architecture.

## 1. Zero-Friction Consumption

Users (and agents) can invoke any core fleet server without local cloning:

```powershell
# Global run (Zero-Install)
uvx schi-mcp-advanced-memory --serve
```

## 2. Trusted Publishing (OIDC Flow)

We eliminate risk from static API tokens by using **OpenID Connect (OIDC)** Handshakes. This is a "Materialist" security model: identity is verified via the repository provenance, not a stored secret.

### Phase 1: PyPI Setup (One-time per Repo)
1. Log in to your PyPI account.
2. Navigate to **Account Settings** > **Publishing**.
3. Under **Add a new pending publisher**, select **GitHub**.
4. **Identity Configuration**:
   - **Owner**: `sandraschi`
   - **Repository Name**: `[repo-name]`
   - **Workflow Name**: `industrial-launch.yml`
   - **Environment Name**: `release`

### Phase 2: GitHub Action (`industrial-launch.yml`)
The workflow must have the `id-token: write` permission to request the OIDC token from GitHub's identity provider.

```yaml
permissions:
  id-token: write      # For PyPI Handshake
  contents: write      # For GitHub Release Artifacts
```

## 3. Industrial Release Standard

Professionalization requires that every release be documented and preserved. Our unified launch workflow produces:
1.  **PyPI Wheel**: High-speed, cached distribution.
2.  **GitHub Release**: Formal versioned record of the fleet state.
3.  **Artifacts**: `.whl`, `.tar.gz`, and `.mcpb` (Claude Desktop legacy).
4.  **Changelog**: Automatically generated from conventional commits or PR merges.

---
*Last Updated: April 2026*
*Standard maintained by the Antigravity SOTA Fleet.*
