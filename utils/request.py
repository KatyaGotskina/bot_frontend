from typing import Any, Dict, Optional

import aiohttp

from bot_frontend.core.config import settings


async def do_request(
    url: str,
    params: Optional[Dict[str, Any]] = None,
    headers: Optional[Dict[str, Any]] = None,
    method: str = 'POST'
) -> Any:
    if not headers:
        headers = {"Content-Type": "application/json"}
    timeout = aiohttp.ClientTimeout(total=3)
    connector = aiohttp.TCPConnector()

    final_exc = None
    async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
        for _ in range(settings.RETRY_COUNT):
            try:
                async with session.request(
                    method,
                    url,
                    json=params,
                    headers=headers,
                ) as response:
                    # response.raise_for_status()
                    try:
                        await response.json()
                    except Exception:
                        pass
                    return response
            except aiohttp.ClientResponseError as exc:
                final_exc = exc

    if final_exc is not None:
        raise final_exc
    raise RuntimeError('Unsupported')
