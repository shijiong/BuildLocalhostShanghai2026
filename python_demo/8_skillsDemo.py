import asyncio
from pathlib import Path

from copilot import CopilotClient
from copilot.session import PermissionHandler


def ensure_demo_skills(root: Path) -> None:
    """Create minimal local skills used by this demo."""
    skills = {
        "security-scan": """---
name: security-scan
description: Security review checklist for web/backend code
---

# Security Scan

When answering:
1. Check input validation and output encoding risks.
2. Check secret leakage risks.
3. Check permission and auth boundary risks.
4. Propose concise, actionable mitigations.
""",
        "python-style": """---
name: python-style
description: Python code quality and maintainability checklist
---

# Python Style

When answering:
1. Prefer clear naming and small functions.
2. Highlight error handling and resource cleanup.
3. Recommend minimal, testable changes.
""",
        "experimental-feature": """---
name: experimental-feature
description: Intentionally disabled in this demo
---

# Experimental Feature

This skill should be disabled by `disabled_skills`.
""",
    }

    root.mkdir(parents=True, exist_ok=True)
    for skill_name, content in skills.items():
        skill_dir = root / skill_name
        skill_dir.mkdir(parents=True, exist_ok=True)
        (skill_dir / "SKILL.md").write_text(content, encoding="utf-8")


async def main() -> None:
    project_root = Path(__file__).resolve().parent
    skills_root = project_root / "demo_skills"
    ensure_demo_skills(skills_root)

    client = CopilotClient()
    await client.start()

    try:
        session = await client.create_session(
            on_permission_request=PermissionHandler.approve_all,
            model="gpt-5.4",
            skill_directories=[str(skills_root)],
            disabled_skills=["experimental-feature"],
            custom_agents=[
                {
                    "name": "security-auditor",
                    "display_name": "Security Auditor",
                    "description": "Security-focused reviewer for Python/FastAPI services",
                    "prompt": "You are a security auditor. Focus on practical risks and fixes.",
                    "skills": ["security-scan"],
                },
                {
                    "name": "python-reviewer",
                    "display_name": "Python Reviewer",
                    "description": "Python code quality reviewer",
                    "prompt": "You are a Python reviewer. Keep suggestions minimal and testable.",
                    "skills": ["python-style"],
                },
            ],
            agent="security-auditor",
        )

        prompt = (
            "Review this FastAPI snippet and provide top 3 security issues plus fixes:\n"
            "\n"
            "from fastapi import FastAPI, Request\n"
            "app = FastAPI()\n"
            "@app.post('/login')\n"
            "async def login(req: Request):\n"
            "    data = await req.json()\n"
            "    print(data)\n"
            "    return {'ok': True}\n"
        )

        response = await session.send_and_wait(prompt)

        print("=== Skills Demo ===")
        print(f"Skills directory: {skills_root}")
        print("Disabled skills: ['experimental-feature']")
        print("Preselected agent: security-auditor (skills=['security-scan'])")
        print("\nAssistant Response:\n")
        print(response.data.content)
    finally:
        await client.stop()


if __name__ == "__main__":
    asyncio.run(main())
