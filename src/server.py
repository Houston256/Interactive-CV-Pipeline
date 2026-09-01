from collections.abc import Awaitable, Callable
from typing import Any

import streamlit as st
from starlette.middleware import Middleware
from starlette.responses import PlainTextResponse


SECURITY_HEADERS = (
    (b'x-content-type-options', b'nosniff'),
    (b'x-frame-options', b'SAMEORIGIN'),
    (b'referrer-policy', b'same-origin'),
    (b'permissions-policy', b'camera=(), geolocation=(), microphone=()'),
)


class SecurityMiddleware:
    def __init__(self, app: Callable[..., Awaitable[None]]):
        self.app = app

    async def __call__(self, scope: dict[str, Any], receive: Callable, send: Callable):
        if scope['type'] == 'http' and scope.get('path') == '/_stcore/metrics':
            await PlainTextResponse('Not Found', status_code=404)(scope, receive, send)
            return

        async def send_with_security_headers(message: dict[str, Any]):
            if message['type'] == 'http.response.start':
                headers = list(message.get('headers', []))
                existing = {name.lower() for name, _ in headers}
                headers.extend(header for header in SECURITY_HEADERS if header[0] not in existing)
                message = {**message, 'headers': headers}
            await send(message)

        await self.app(scope, receive, send_with_security_headers)


if __name__ == '__main__':
    app = st.App('main.py', middleware=[Middleware(SecurityMiddleware)])
    # Required inside Docker; Compose publishes it only on host loopback.
    app.run(config={'server.address': '0.0.0.0', 'server.port': 8501})  # nosec B104
