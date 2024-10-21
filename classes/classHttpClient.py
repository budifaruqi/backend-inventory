from httpx import AsyncClient
from httpx import Limits as HttpxLimit
from httpx import Timeout as HttpxTimeout
from httpx._config import DEFAULT_LIMITS as HttpxLimitsDefault
from httpx._config import DEFAULT_TIMEOUT_CONFIG as HttpxTimeoutDefault

class MsHttpAsyncClient:

    def __init__(
        self,
        connect: float | None = None,
        read: float | None = None,
        write: float | None = None,
        pool: float | None = None,
        user_agent: str | None = None,
        max_connections: int | None = None,
        max_keepalive_connections: int | None = None,
        keepalive_expiry: float | None = None,
        trust_env: bool = False,
        http2: bool = False
    ) -> None:
        self.client = AsyncClient(
            timeout=HttpxTimeout(
                connect=HttpxTimeoutDefault.connect if connect is None else connect,
                read=HttpxTimeoutDefault.read if read is None else read,
                write=HttpxTimeoutDefault.write if write is None else write,
                pool=HttpxTimeoutDefault.pool if pool is None else pool
            ),
            follow_redirects=False,
            auth=None,
            headers={b"User-Agent": user_agent.encode(encoding="ascii") if user_agent is not None else b"MSHttpClient"},
            limits=HttpxLimit(
                max_connections=HttpxLimitsDefault.max_connections if max_connections is None else max_connections,
                max_keepalive_connections=HttpxLimitsDefault.max_keepalive_connections if max_keepalive_connections is None else max_keepalive_connections,
                keepalive_expiry=HttpxLimitsDefault.keepalive_expiry if keepalive_expiry is None else keepalive_expiry
            ),
            trust_env=trust_env,
            http2=http2
        )
