from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import Response
from mcp.server.sse import SseServerTransport
from mcp.server import Server
# Local fallback for NotificationOptions if not available in mcp.server
try:
    from mcp.server import NotificationOptions
except ImportError:
    class NotificationOptions:
        def __init__(self, tools_changed=False, resources_changed=False, prompts_changed=False):
            self.tools_changed = tools_changed
            self.resources_changed = resources_changed
            self.prompts_changed = prompts_changed

from mcp.server.models import InitializationOptions
import mcp.types as types
import asyncio
from .server import server

# 4. Initialize SSE transport layer
sse = SseServerTransport("/messages/")

# 5. SSE connection handler
async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await server.run(
            streams[0],
            streams[1],
            server.create_initialization_options(
                notification_options=NotificationOptions(
                    tools_changed=True,
                    resources_changed=True,
                    prompts_changed=False
                )
            )
        )
    return Response()

# 6. Starlette routes
routes = [
    Route("/sse", endpoint=handle_sse, methods=["GET"]),
    Mount("/messages/", app=sse.handle_post_message),
]

# 7. Create Starlette application
starlette_app = Starlette(routes=routes)

# 8. Start (using uvicorn)
if __name__ == "__main__":
    import uvicorn
    # Listen on 0.0.0.0 for Docker and external access
    uvicorn.run(starlette_app, host="0.0.0.0", port=8100) 