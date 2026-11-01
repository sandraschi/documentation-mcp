# Live Studio Plan (summary)

**Canonical doc:** [libreoffice-mcp/docs/LIVE_STUDIO_PLAN.md](https://github.com/sandraschi/libreoffice-mcp/blob/main/docs/LIVE_STUDIO_PLAN.md) in the repo.

Live Studio is the webapp hub at `/studio` for live LibreOffice workflows: bridge status, links to Live Write/Calc, and open-in-app for Writer/Calc/Impress.

## Phases

| Phase | Focus |
|-------|--------|
| **A (now)** | `/studio` hub, `/api/studio/session`, `open-in-app`, session bar, recent outputs |
| **B** | Impress launch + outline→slides headless; open in Impress GUI |
| **C** | Persistent session bar across pages; "reveal in LO" from Output |
| **D** | Impress live bridge (.oxt) if GUI-only is not enough |
| **E** | Fleet coworker hooks (email PDF attach, etc.) |

See the repo doc for API shapes, file layout, and acceptance criteria.
