from enum import Enum


class GlobalConfig(str, Enum):
    partner_auth_rsa = "partner_auth_rsa"
    partner_auth_aes_key = "partner_auth_aes_key"
    partner_auth_additional_key = "partner_auth_additional_key"

    client_auth_rsa = "client_auth_rsa"
    client_auth_aes_key = "client_auth_aes_key"
    client_auth_additional_key = "client_auth_additional_key"