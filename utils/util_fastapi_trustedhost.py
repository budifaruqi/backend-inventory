from ipaddress import ip_address
import typing

from fastapi.datastructures import Address
from starlette.datastructures import Headers
from starlette.responses import PlainTextResponse
from starlette.types import ASGIApp, Receive, Scope, Send

from utils.util_logger import msLogger


MS_ENFORCE_DOMAIN_WILDCARD = "Domain wildcard patterns must be like '*.example.com'."


class MsTrustedHostMiddleware:
    def __init__(
        self,
        app: ASGIApp,
        allowed_hosts: typing.Optional[typing.Sequence[str]] = None,
        hostHeaderName: str = "host",
        behindNAT: bool = False,
        proxyIpAddressHeaderName: str | None = None,
        allowLoopbackIp: bool = False,
        allowPrivateIp: bool = False,
        debug: bool = False
    ) -> None:
        self.debug = debug
        if allowed_hosts is None:
            allowed_hosts = ["*"]

        for pattern in allowed_hosts:
            assert "*" not in pattern[1:], MS_ENFORCE_DOMAIN_WILDCARD
            if pattern.startswith("*") and pattern != "*":
                assert pattern.startswith("*."), MS_ENFORCE_DOMAIN_WILDCARD
        self.app = app
        self.allowed_hosts = list(allowed_hosts)
        self.allow_any = "*" in allowed_hosts
        self.hostHeaderName = hostHeaderName
        self.behindNAT = behindNAT
        self.proxyIpAddressHeaderName = proxyIpAddressHeaderName or "x-real-ip"
        self.allowLoopbackIp = allowLoopbackIp
        self.allowPrivateIp = allowPrivateIp

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if self.allow_any or scope["type"] not in (
            "http",
            "websocket",
        ):  # pragma: no cover
            await self.app(scope, receive, send)
            return

        headers = Headers(scope=scope)
        host = headers.get(self.hostHeaderName, "").split(":")[0]
        is_valid_host = False
        for pattern in self.allowed_hosts:
            if host == pattern or (
                pattern.startswith("*") and host.endswith(pattern[1:])
            ):
                is_valid_host = True
                break
            
        if (not is_valid_host) and (self.allowLoopbackIp or self.allowPrivateIp):
            addrs = ""
            if self.behindNAT:
                addrs = headers.get(self.proxyIpAddressHeaderName)
            if (addrs is None) or (len(addrs) == 0):
                try:
                    host_port = scope.get("client")
                    if host_port is not None:
                        addr = Address(*host_port)
                        ip = ip_address(addr.host)
                        if self.allowLoopbackIp:
                            is_valid_host = ip.is_loopback
                        if (not is_valid_host) and (self.allowPrivateIp):
                            is_valid_host = ip.is_private
                except:
                    pass
                
        if is_valid_host:
            await self.app(scope, receive, send)
        else:
            if self.debug:
                msLogger.error(f"Invalid host header, header: {self.hostHeaderName}; value: {host}")
            response = PlainTextResponse("Invalid host header", status_code=400)
            await response(scope, receive, send)
