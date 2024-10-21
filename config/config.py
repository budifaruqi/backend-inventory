# https://docs.pydantic.dev/latest/concepts/pydantic_settings

from base64 import standard_b64decode
from typing import Any, List, Tuple, Type
from pydantic import BaseModel, Field, field_serializer
from pydantic_settings import BaseSettings, JsonConfigSettingsSource, PydanticBaseSettingsSource, SettingsConfigDict, YamlConfigSettingsSource

from models.shared.modelEnvironment import MsEnvironment
from models.shared.modelMongodbAuthMechanism import MongodbAuthMechanism

class SettingFastApi(BaseModel):
    project_name: str
    debug: bool
    version: str
    description: str
    root_path: str
    openapi_path: str | None = None
    docs_path: str | None = None
    redoc_path: str | None = None

class SettingProject(BaseModel):
    serviceName: str
    environment: MsEnvironment
    dev_mode: bool
    use_localdb: bool
    logging_use_colors: bool

class SettingMongoDb(BaseModel):
    database_name: str
    username: str | None = None
    password: str | None = None
    host: str
    port: int | None = None
    authMechanism: MongodbAuthMechanism | None = None
    directConnection: bool | None = None
    replica_set_name: str | None = None

    localdb_database_name: str
    localdb_username: str | None = None
    localdb_password: str | None = None
    localdb_host: str
    localdb_port: int | None = None
    localdb_authMechanism: MongodbAuthMechanism | None = None
    localdb_directConnection: bool | None = None
    localdb_replica_set_name: str | None = None

# -------------------------------------------------------

class SettingApm(BaseModel):
    server: str | None
    prefix: str | None

# -------------------------------------------------------

class SettingRabbitMq(BaseModel):
    username: str
    password: str
    host: str
    port: int
    virtual_host: str
    prefetch_count: int
    reconnectDelaySec: int
    exchangeName: str
    queueName: str

# -------------------------------------------------------

class SettingHttpClientTimeout(BaseModel):
    connect: float | None = None
    read: float | None = None
    write: float | None = None
    pool: float | None = None

class SettingHttpClientLimit(BaseModel):
    max_connections: int | None = None
    max_keepalive_connections: int | None = None
    keepalive_expiry: float | None = None

class SettingHttpClient(BaseModel):
    timeout: SettingHttpClientTimeout
    limit: SettingHttpClientLimit
    trust_env: bool = False
    http2: bool = False
    user_agent: str | None = None

class SettingsConfig(BaseModel):
    installation: bool
    timezone: str
    behindNAT: bool
    proxyIpAddressHeaderName: str
    proxyHostHeaderName: str | None = "host"
    allow_origins: List[str]
    allowed_hosts: List[str]

class SettingServices(BaseModel):
    authService: str

class SettingConst(BaseModel):
    dbSecurityKeyStr: str = "bbtx81WhxprxC/Fvlm+VRqz7c32dSiqOx15egfKP7IM="
    dbSecurityKey: bytes | None = None
    dbSecurityIvStr: str = "9GClnVaRqPGt5i68HuP78g=="
    dbSecurityIv: bytes | None = None

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

        self.dbSecurityKey = standard_b64decode(self.dbSecurityKeyStr)
        self.dbSecurityIv = standard_b64decode(self.dbSecurityIvStr)

    @field_serializer('dbSecurityKey', 'dbSecurityIv', when_used='json')
    def dump_bytes(self, v: bytes | None):
        if v is not None:
            return v.hex(" ", bytes_per_sep=0)
        else:
            return None

class SettingsModel(BaseSettings):
    fastapi: SettingFastApi
    project: SettingProject
    mongodb: SettingMongoDb
    apm: SettingApm
    rabbitmq: SettingRabbitMq
    httpClient: SettingHttpClient
    config: SettingsConfig

    services: SettingServices
    const: SettingConst = Field(
        default={}
    )
    
    apiKey: str | None = None
    apiUsername: str | None = None

    model_config = SettingsConfigDict(
        extra='allow',
        # env_prefix='microservice_',
        secrets_dir="./env",
        env_file=("./env/.env", "./env/.env.setting"), env_file_encoding="utf-8",
        json_file="./env/setting.json", json_file_encoding="utf-8",
        yaml_file="./env/setting.yml", yaml_file_encoding="utf-8"
    )

    def __init__(self, **data: Any) -> None:
        super().__init__(**data)

        self.const = SettingConst(**{})
        
    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            # highest priority
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
            JsonConfigSettingsSource(settings_cls),
            YamlConfigSettingsSource(settings_cls),
            # lower priority
        )

settings = SettingsModel()

