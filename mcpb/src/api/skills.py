import json
import logging
from pathlib import Path

from fastapi import APIRouter, HTTPException

logger = logging.getLogger("docs_mcp.api.skills")
router = APIRouter(prefix="/api")

@router.get("/skills")
async def api_skills():
    """List skills exposed by this server."""
    try:
        import frontmatter
        skills_dir = Path(__file__).resolve().parent.parent / "skills"
        if not skills_dir.is_dir():
            return {"skills": []}

        skills = []
        for subdir in sorted(skills_dir.iterdir()):
            if not subdir.is_dir():
                continue
            skill_md = subdir / "SKILL.md"
            if not skill_md.is_file():
                continue
            try:
                with open(skill_md, encoding="utf-8") as f:
                    post = frontmatter.load(f)
                skills.append({
                    "id": subdir.name,
                    "name": post.get("name") or subdir.name,
                    "description": post.get("description") or "",
                    "content": post.content,
                    "uri": f"skill://{subdir.name}/SKILL.md",
                })
            except Exception as e:
                logger.warning("Failed to parse skill %s: %s", subdir.name, e)
        return {"skills": skills}
    except Exception as e:
        logger.error(f"Error listing skills: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/skill_marketplaces")
async def api_skill_marketplaces():
    """Serve curated skill marketplaces."""
    try:
        data_path = Path(__file__).parent.parent / "data" / "skill_marketplaces.json"
        if data_path.exists():
            with open(data_path, encoding="utf-8") as f:
                return json.load(f)
        return {"marketplaces": []}
    except Exception as e:
        logger.error(f"Error in api_skill_marketplaces: {e}")
        raise HTTPException(status_code=500, detail=str(e))
