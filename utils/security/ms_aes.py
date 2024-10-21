from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

class MsAES:

    @staticmethod
    def AesGcmEncrypt(
        key: bytes,
        iv: bytes, # gcm 96-bit IV
        plaintext: bytes,
        associated_data: bytes
    ):
        encryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv)
        ).encryptor()
        encryptor.authenticate_additional_data(associated_data)
        ciphertext = encryptor.update(plaintext) + encryptor.finalize()
        return ciphertext, encryptor.tag

    @staticmethod
    def AesGcmDecrypt(
        key: bytes,
        associated_data: bytes,
        iv: bytes, # gcm 96-bit IV
        ciphertext: bytes,
        tag: bytes | None
    ):
        decryptor = Cipher(
            algorithms.AES(key),
            modes.GCM(iv, tag)
        ).decryptor()
        decryptor.authenticate_additional_data(associated_data)
        return decryptor.update(ciphertext) + decryptor.finalize()

    # ========================================================================
    
    @staticmethod
    def Aes256CbcEncrypt(
        key: bytes, # 256-bit key
        iv: bytes, # 128-bit IV
        plaintext: bytes
    ) -> bytes:
        """
        AES-256-CBC PADDING-PKCS7
        """
        
        cipher = Cipher(
            algorithms.AES256(key),
            modes.CBC(iv)
        )
        encryptor = cipher.encryptor()
        plaintextLen = len(plaintext)
        offset = 0
        ciphertext = b""
        while offset < plaintextLen:
            buf = plaintext[offset:offset + 16]
            offset += 16
            if (len(buf) < 16) or (offset == plaintextLen):
                padder = padding.PKCS7(128).padder()
                padded_data = padder.update(buf) + padder.finalize()
                ciphertext += encryptor.update(padded_data)
            else:
                ciphertext += encryptor.update(buf)
        
        ciphertext += encryptor.finalize()

        return ciphertext

    @staticmethod
    def Aes256CbcDecrypt(
        key: bytes, # 256-bit key
        iv: bytes, # 128-bit IV
        ciphertext: bytes
    ) -> bytes:
        """
        AES-256-CBC PADDING-PKCS7
        """

        cipher = Cipher(
            algorithms.AES256(key),
            modes.CBC(iv)
        )
        decryptor = cipher.decryptor()
        plaintextPadded = decryptor.update(ciphertext) + decryptor.finalize()
        unpadder = padding.PKCS7(128).unpadder()
        plaintext = unpadder.update(plaintextPadded)
        plaintext += unpadder.finalize()
        
        return plaintext
    # ========================================================================
    