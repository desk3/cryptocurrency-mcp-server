from starlette.applications import Starlette
from starlette.routing import Route, Mount
from starlette.responses import Response
from mcp.server.sse import SseServerTransport
from src.desk3_service.server import server

# 1. Initialize SSE transport layer
sse = SseServerTransport("/messages/")

# 2. SSE connection handler
async def handle_sse(request):
    async with sse.connect_sse(request.scope, request.receive, request._send) as streams:
        await server.run(
            streams[0],
            streams[1],
            server.create_initialization_options()
        )
    return Response()

# 3. Starlette routes
routes = [
    Route("/sse", endpoint=handle_sse, methods=["GET"]),
    Mount("/messages/", app=sse.handle_post_message),
]

# 4. Create Starlette application
starlette_app = Starlette(routes=routes)

# 5. Start (using uvicorn)
if __name__ == "__main__":
    import uvicorn
    # Listen on 0.0.0.0 for Docker and external access
    uvicorn.run(starlette_app, host="0.0.0.0", port=8100) 