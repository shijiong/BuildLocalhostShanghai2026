import asyncio
import sys
from typing import Any

from copilot import CopilotClient
from copilot.session import PermissionHandler
from copilot.session_events import SessionEventType


# Helper: compatible field extractor for different event data naming styles.
def pick(data: Any, *names: str, default: str = "") -> str:
    for name in names:
        if hasattr(data, name):
            value = getattr(data, name)
            if value is not None:
                return str(value)
    return default


def handle_event(event: Any) -> None:
    etype = str(event.type)

    # Streaming text chunks from assistant
    if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
        sys.stdout.write(event.data.delta_content)
        sys.stdout.flush()
        return

    # Sub-agent lifecycle events (from custom-agents.md)
    if etype in ("subagent.selected", "SessionEventType.SUBAGENT_SELECTED"):
        name = pick(event.data, "agent_display_name", "agentDisplayName", "agent_name", "agentName")
        tools = pick(event.data, "tools", default="all")
        print(f"\n[selected] {name} tools={tools}")
    elif etype in ("subagent.started", "SessionEventType.SUBAGENT_STARTED"):
        name = pick(event.data, "agent_display_name", "agentDisplayName", "agent_name", "agentName")
        desc = pick(event.data, "agent_description", "agentDescription")
        tcid = pick(event.data, "tool_call_id", "toolCallId")
        print(f"\n[started] {name} tool_call_id={tcid}")
        if desc:
            print(f"  description: {desc}")
    elif etype in ("subagent.completed", "SessionEventType.SUBAGENT_COMPLETED"):
        name = pick(event.data, "agent_display_name", "agentDisplayName", "agent_name", "agentName")
        print(f"\n[completed] {name}")
    elif etype in ("subagent.failed", "SessionEventType.SUBAGENT_FAILED"):
        name = pick(event.data, "agent_display_name", "agentDisplayName", "agent_name", "agentName")
        err = pick(event.data, "error", default="unknown error")
        print(f"\n[failed] {name} error={err}")
    elif etype in ("subagent.deselected", "SessionEventType.SUBAGENT_DESELECTED"):
        print("\n[deselected] back to parent agent")


async def main() -> None:
    client = CopilotClient()
    await client.start()

    session = await client.create_session(
        on_permission_request=PermissionHandler.approve_all,
        model="gpt-5.4",
        streaming=True,
        # Pre-select the researcher agent at session startup.
        agent="researcher",
        custom_agents=[
            {
                "name": "researcher",
                "display_name": "Research Agent",
                "description": "Read-only code exploration and architecture explanation",
                "tools": ["grep", "glob", "view"],
                "prompt": "You are a research specialist. Analyze and explain code clearly. Never edit files.",
            },
            {
                "name": "editor",
                "display_name": "Editor Agent",
                "description": "Implements minimal code changes with validation",
                "tools": ["view", "edit", "bash"],
                "prompt": "You are an implementation specialist. Make minimal, safe edits and explain what changed.",
            },
            {
                "name": "dangerous-cleanup",
                "display_name": "Dangerous Cleanup Agent",
                "description": "Deletes unused files and performs aggressive cleanup",
                "tools": ["bash", "edit", "view"],
                "prompt": "You perform cleanup operations only when explicitly requested.",
                "infer": False,
            },
        ],
    )

    session.on(handle_event)

    prompt = (
        "Please first inspect this 1_FirstMessage.py structure and summarize key modules. "
        "Then propose a small code improvement plan without directly editing files."
    )

    print("=== Custom Agents Demo ===")
    print("Sending prompt...\n")
    await session.send_and_wait(prompt)
    print("\n\nDone.")

    await client.stop()


if __name__ == "__main__":
    asyncio.run(main())
