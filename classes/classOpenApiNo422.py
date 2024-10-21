from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi


class OpenApiNo422:
    def __init__(self, _app: FastAPI) -> None:
        self._app = _app
        self._app.openapi = self.custom_openapi_no_422

    def custom_openapi_no_422(self):
        if not self._app.openapi_schema:
            self._app.openapi_schema = get_openapi(
                title=self._app.title,
                version=self._app.version,
                openapi_version=self._app.openapi_version,
                summary=self._app.summary,
                description=self._app.description,
                routes=self._app.routes,
                tags=self._app.openapi_tags,
                servers=self._app.servers,
                terms_of_service=self._app.terms_of_service,
                contact=self._app.contact,
                license_info=self._app.license_info,
                separate_input_output_schemas=self._app.separate_input_output_schemas
            )
            for _, method_item in self._app.openapi_schema.get('paths').items(): # type: ignore
                for _, param in method_item.items():
                    responses = param.get('responses')
                    # remove 422 response, also can remove other status code
                    if '422' in responses:
                        del responses['422']
        return self._app.openapi_schema