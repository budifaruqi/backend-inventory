

from enum import Enum


class RabbitMqRoutingKeyUserService(str, Enum):
    company_category = "user-company_category"
    company = "user-company"
    account = "user-account"
    account_external = "user-account_external"