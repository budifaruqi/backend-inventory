from cryptography.hazmat.primitives import hashes, hmac
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

class MsHash:

    @staticmethod
    def hash_md5(msg: bytes) -> bytes:
        h = hashes.Hash(hashes.MD5())
        h.update(msg)
        return h.finalize()

    @staticmethod
    def hash_sha1(msg: bytes) -> bytes:
        h = hashes.Hash(hashes.SHA1())
        h.update(msg)
        return h.finalize()
    
    @staticmethod
    def hash_sha256(msg: bytes) -> bytes:
        h = hashes.Hash(hashes.SHA256())
        h.update(msg)
        return h.finalize()
    
    @staticmethod
    def hash_sha512(msg: bytes) -> bytes:
        h = hashes.Hash(hashes.SHA512())
        h.update(msg)
        return h.finalize()
    
    # ========================================================================

    @staticmethod
    def create_hash_md5() -> hashes.Hash:
        return hashes.Hash(hashes.MD5())

    @staticmethod
    def create_hash_sha1() -> hashes.Hash:
        return hashes.Hash(hashes.SHA1())

    @staticmethod
    def create_hash_sha256() -> hashes.Hash:
        return hashes.Hash(hashes.SHA256())
    
    @staticmethod
    def create_hash_sha512() -> hashes.Hash:
        return hashes.Hash(hashes.SHA512())
    
    # ========================================================================

    @staticmethod
    def create_hmac_md5(key: bytes) -> hmac.HMAC:
        return hmac.HMAC(key, hashes.MD5())

    @staticmethod
    def create_hmac_sha1(key: bytes) -> hmac.HMAC:
        return hmac.HMAC(key, hashes.SHA1())

    @staticmethod
    def create_hmac_sha256(key: bytes) -> hmac.HMAC:
        return hmac.HMAC(key, hashes.SHA256())
    
    @staticmethod
    def create_hmac_sha512(key: bytes) -> hmac.HMAC:
        return hmac.HMAC(key, hashes.SHA512())
    
    # ========================================================================

    @staticmethod
    def hmac_md5(key: bytes, msg: bytes) -> bytes:
        h = hmac.HMAC(key, hashes.MD5())
        h.update(msg)
        return h.finalize()

    @staticmethod
    def hmac_md5_verify(key: bytes, msg: bytes, signature: bytes) -> bool:
        h = hmac.HMAC(key, hashes.MD5())
        h.update(msg)
        try:
            h.verify(signature)
            return True
        except:
            return False
        
    # ========================================================================

    @staticmethod
    def hmac_sha1(key: bytes, msg: bytes) -> bytes:
        h = hmac.HMAC(key, hashes.SHA1())
        h.update(msg)
        return h.finalize()

    @staticmethod
    def hmac_sha1_verify(key: bytes, msg: bytes, signature: bytes) -> bool:
        h = hmac.HMAC(key, hashes.SHA1())
        h.update(msg)
        try:
            h.verify(signature)
            return True
        except:
            return False
        
    # ========================================================================

    @staticmethod
    def hmac_sha256(key: bytes, msg: bytes) -> bytes:
        h = hmac.HMAC(key, hashes.SHA256())
        h.update(msg)
        return h.finalize()

    @staticmethod
    def hmac_sha256_verify(key: bytes, msg: bytes, signature: bytes) -> bool:
        h = hmac.HMAC(key, hashes.SHA256())
        h.update(msg)
        try:
            h.verify(signature)
            return True
        except:
            return False

    # ========================================================================

    @staticmethod
    def hmac_sha512(key: bytes, msg: bytes) -> bytes:
        h = hmac.HMAC(key, hashes.SHA512())
        h.update(msg)
        return h.finalize()

    @staticmethod
    def hmac_sha512_verify(key: bytes, msg: bytes, signature: bytes) -> bool:
        h = hmac.HMAC(key, hashes.SHA512())
        h.update(msg)
        try:
            h.verify(signature)
            return True
        except:
            return False

    # ========================================================================
    
    @staticmethod
    def Derive_PBKDF2HMAC(
        secret: bytes,
        salt: bytes,
        iterations: int
    ) -> bytes:
        h = hashes.SHA256()
        kdf = PBKDF2HMAC(
            h,
            h.digest_size,
            salt,
            iterations,
        )
        return kdf.derive(secret)

    @staticmethod
    def Verify_PBKDF2HMAC(
        msg: bytes,
        salt: bytes,
        iterations: int,
        signature: bytes
    ) -> bool:
        h = hashes.SHA256()
        kdf = PBKDF2HMAC(
            h,
            h.digest_size,
            salt,
            iterations,
        )
        try:
            kdf.verify(msg, signature)
            return True
        except:
            return False
        
    # ========================================================================
    