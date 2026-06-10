from copilot import CopilotClient, PermissionHandler
from copilot.session import PermissionHandler
from copilot.session_events import SessionEventType
import asyncio
import base64
import sys

async def main():
    client = CopilotClient()
    await client.start()

    session = await client.create_session(on_permission_request=PermissionHandler.approve_all, model="gpt-5.4", streaming=True)

    with open('demo.jpg', 'rb') as image_file:
        image_data = image_file.read()

    base64_image_data = base64.b64encode(image_data).decode('utf-8')

    # Listen for response chunks
    def handle_event(event):
        if event.type == SessionEventType.ASSISTANT_MESSAGE_DELTA:
            sys.stdout.write(event.data.delta_content)
            sys.stdout.flush()
        if event.type == SessionEventType.SESSION_IDLE:
            print()  # New line when done

    session.on(handle_event)

    await session.send_and_wait(
        "Describe what you see in this image",
        attachments=[
            {
                "type": "blob",
                "data": base64_image_data,
                "mimeType": "image/jpeg",
                "displayName": "demo.jpg",
            },
        ],
    )

    await client.stop()

asyncio.run(main())