import asyncio
import os
from copilot import CopilotClient
from copilot.session import PermissionHandler

async def main():
    client = CopilotClient()
    await client.start()

    session = await client.create_session(on_permission_request=PermissionHandler.approve_all, model="qwen3:8b",provider={
        "type": "openai",
        "base_url": "http://192.168.0.117:11434/v1",  # Ollama endpoint
    })
    response = await session.send_and_wait("What is 2 + 2?")
    print(response.data.content)

    await client.stop()

asyncio.run(main())