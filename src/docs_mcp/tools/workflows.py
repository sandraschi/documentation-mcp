import logging
from pathlib import Path

from fastmcp import Context, FastMCP

from docs_mcp.utils.formatting import _to_markdown

logger = logging.getLogger("docs_mcp.tools.workflows")

_MUTATING = {}


def register_tools(mcp: FastMCP):
    """Register agentic and system orchestration tools."""

    @mcp.tool(annotations=_MUTATING, version="1.0.1")
    def start_webapp() -> dict:
        """Start the Documentation MCP webapp fully automatically.

        Launches the web_sota/start.ps1 script in -Automated mode,
        which starts the backend, frontend, and opens a browser.

        ## Return Format
        {"success": bool, "message": str, "url": str}

        ## Examples
        - start_webapp()
        """
        import subprocess
        repo_root = Path(__file__).resolve().parent.parent.parent.parent
        start_ps1 = repo_root / "web_sota" / "start.ps1"

        if not start_ps1.is_file():
            return {"success": False, "message": f"Startup script not found at {start_ps1}"}

        try:
            subprocess.Popen(
                ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", str(start_ps1), "-Automated"],
                creationflags=subprocess.CREATE_NEW_CONSOLE if hasattr(subprocess, "CREATE_NEW_CONSOLE") else 0,
            )

            return {
                "success": True,
                "message": "Webapp startup sequence initiated in background.",
                "url": "http://localhost:11032",
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool(annotations=_MUTATING, version="1.0.1")
    async def agentic_doc_workflow(workflow_prompt: str, ctx: Context) -> dict:
        """Execute autonomous documentation research and report generation workflows.

        Uses MCP sampling (ctx.sample) to synthesize a research report from the
        documentation index. Requires client sampling support.

        ## Return Format
        {"success": bool, "operation": "agentic_doc_workflow", "message": str,
         "data": {"report": str}}

        ## Examples
        - agentic_doc_workflow(workflow_prompt="Research all FastMCP 3.2+ tool registration standards and summarize")
        """
        system_prompt = (
            "You are an autonomous documentation researcher. Your goal is to use the "
            "available search_docs and ask_docs tools to fulfill the user's research request."
        )

        try:
            ctx.report_progress("Analyzing workflow requirements...", 10)
            response = await ctx.sample(
                messages=[workflow_prompt],
                system_prompt=system_prompt,
                max_tokens=2000,
            )
            ctx.report_progress("Finalizing research report...", 90)

            res = {
                "success": True,
                "operation": "agentic_doc_workflow",
                "message": "Autonomous research workflow complete.",
                "data": {"report": response.text},
            }
            return {"result": _to_markdown(res, "agentic_doc_workflow")}
        except Exception as e:
            return {"success": False, "error": str(e)}
