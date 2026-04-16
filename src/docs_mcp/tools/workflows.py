import logging
from pathlib import Path
from fastmcp import Context, FastMCP
from docs_mcp.utils.formatting import _to_markdown

logger = logging.getLogger("docs_mcp.tools.workflows")

def register_tools(mcp: FastMCP):
    """Register agentic and system orchestration tools."""

    @mcp.tool()
    def start_webapp() -> dict:
        """Start the Documentation MCP webapp fully automatically."""
        import subprocess
        repo_root = Path(__file__).resolve().parent.parent.parent.parent
        start_ps1 = repo_root / "web_sota" / "start.ps1"
        
        if not start_ps1.is_file():
            return {"success": False, "message": f"Startup script not found at {start_ps1}"}

        try:
            # SOTA v14.0 automated startup pattern
            subprocess.Popen(
                ["powershell.exe", "-ExecutionPolicy", "Bypass", "-File", str(start_ps1), "-Automated"],
                creationflags=subprocess.CREATE_NEW_CONSOLE if hasattr(subprocess, "CREATE_NEW_CONSOLE") else 0
            ) # noqa: S603, S607
            
            return {
                "success": True, 
                "message": "Webapp startup sequence initiated in background.",
                "url": "http://localhost:10794"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    @mcp.tool()
    async def agentic_doc_workflow(workflow_prompt: str, ctx: Context) -> dict:
        """Execute autonomous documentation research and report generation workflows."""
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
