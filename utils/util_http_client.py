from httpx import AsyncClient, Response
from classes.classHttpClient import MsHttpAsyncClient
from config.config import settings

def IsJsonResponse(response: Response) -> bool:
    headersContentType = response.headers.get_list("content-type", True)
    isJsonResponse = len(headersContentType) > 0
    if isJsonResponse:
        isJsonResponse = False
        for contentType in headersContentType:
            if contentType.lower().find("application/json") >= 0:
                isJsonResponse = True
                break

    return isJsonResponse

__msHttpClientInstance = None
def HttpClientDefault() -> AsyncClient:
    global __msHttpClientInstance
    if __msHttpClientInstance is None:
        conf_trust_env = settings.httpClient.trust_env
        if not conf_trust_env:
            trust_env = False
        else:
            trust_env = conf_trust_env

        conf_http2 = settings.httpClient.http2
        if not conf_http2:
            use_http2 = False
        else:
            use_http2 = conf_http2

        __msHttpClientInstance = MsHttpAsyncClient(
            connect=settings.httpClient.timeout.connect,
            read=settings.httpClient.timeout.read,
            write=settings.httpClient.timeout.write,
            pool=settings.httpClient.timeout.pool,
            user_agent=settings.httpClient.user_agent,
            max_connections=settings.httpClient.limit.max_connections,
            max_keepalive_connections=settings.httpClient.limit.max_keepalive_connections,
            keepalive_expiry=settings.httpClient.limit.keepalive_expiry,
            trust_env=trust_env,
            http2=use_http2
        )
    return __msHttpClientInstance.client