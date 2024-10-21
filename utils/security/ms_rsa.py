from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization
from utils.util_http_exception import MsHTTPBadRequestException


class MsRsa:

    @staticmethod
    def GenerateRsa(keyStrength: int, public_exponent: int = 65537) -> tuple[bytes, bytes]:
        """
        return: privateKey, publicKey
        """
        
        if keyStrength < 512:
            raise MsHTTPBadRequestException(
                type="INVALID_RSA_KEY_STRENGTH",
                message="Unsupported RSA key, the key size must be greater than or equal to 512 bits"
            )
        if keyStrength > 16384:
            raise MsHTTPBadRequestException(
                type="INVALID_RSA_KEY_STRENGTH",
                message="Unsupported RSA key, the key size must be less than or equal to 16384 bits"
            )
        if keyStrength % 64 != 0:
            raise MsHTTPBadRequestException(
                type="INVALID_RSA_KEY_STRENGTH",
                message="Unsupported RSA key, the key size must a multiple of 64"
            )
        privateKeyObj = rsa.generate_private_key(
            public_exponent=public_exponent,
            key_size=keyStrength
        )

        privateKey = privateKeyObj.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )

        publicKey = privateKeyObj.public_key().public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.PKCS1
        )

        return privateKey, publicKey