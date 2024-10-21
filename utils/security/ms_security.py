import random
from secrets import token_bytes
from base64 import standard_b64decode, standard_b64encode, urlsafe_b64decode, urlsafe_b64encode
from uuid import UUID, uuid1
import os

buffer_bytes_types = bytes | bytearray
str_buffer_bytes_types = str | buffer_bytes_types

class MsSecurity:

    letter = "abcdefghijklmnopqrstuvwxyz"
    alphabet = "abcdefghijklmnopqrstuvwxyz0123456789"
    alphabetAny = "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ0123456789"
    number = "0123456789"
    pkce_code_verifier = "aAbBcCdDeEfFgGhHiIjJkKlLmMnNoOpPqQrRsStTuUvVwWxXyYzZ0123456789-._~"

    @staticmethod
    def GenRandomBytes(size: int) -> bytes:
        return token_bytes(size)
    
    @staticmethod
    def GenRandomString(size: int) -> str:
        if size < 1:
            size = 1
        return "".join(random.choice(MsSecurity.alphabet) for _ in range(size))
    
    @staticmethod
    def GenRandomLetter(size: int) -> str:
        if size < 1:
            size = 1
        return "".join(random.choice(MsSecurity.letter) for _ in range(size))
    
    @staticmethod
    def GenRandomAnyString(size: int) -> str:
        if size < 1:
            size = 1
        return "".join(random.choice(MsSecurity.alphabetAny) for _ in range(size))
    
    @staticmethod
    def GenRandomPkceCodeVerifier(size: int = 128) -> str:
        # https://www.rfc-editor.org/rfc/rfc7636#section-4.1
        # minimum 43
        # maksimum 128
        if size < 43:
            size = 43
        elif size > 128:
            size = 128
        return "".join(random.choice(MsSecurity.pkce_code_verifier) for _ in range(size))
    
    @staticmethod
    def GenRandomNumber(size: int) -> str:
        if size < 1:
            size = 1
        return "".join(random.choice(MsSecurity.number) for _ in range(size))

    @staticmethod
    def b64decode_standard(msg: str_buffer_bytes_types) -> bytes:
        """
        msg: str
        """
        # add padding
        if isinstance(msg, str):
            while (len(msg) % 4) != 0:
                msg += "="
        elif isinstance(msg, bytearray):
            while (len(msg) % 4) != 0:
                msg.extend(b"=")
        else:
            if (len(msg) % 4) != 0:
                msg = bytearray(msg)
                while (len(msg) % 4) != 0:
                    msg.extend(b"=")
        return standard_b64decode(msg)

    @staticmethod
    def b64encode_standard(msg: buffer_bytes_types, removePadding: bool = False) -> bytes:
        raw = standard_b64encode(msg)
        if not removePadding:
            return raw
        # remove b64 padding
        b = bytearray(raw)
        while b[len(b)-1] == 61:
            del b[len(b)-1]
        return bytes(b)

    @staticmethod
    def b64decode_url(msg: str_buffer_bytes_types) -> bytes:
        """
        msg: str
        """
        # add padding
        if isinstance(msg, str):
            while (len(msg) % 4) != 0:
                msg += "="
        elif isinstance(msg, bytearray):
            while (len(msg) % 4) != 0:
                msg.extend(b"=")
        else:
            if (len(msg) % 4) != 0:
                msg = bytearray(msg)
                while (len(msg) % 4) != 0:
                    msg.extend(b"=")
        return urlsafe_b64decode(msg)

    @staticmethod
    def b64encode_url(msg: buffer_bytes_types, removePadding: bool = True) -> bytes:
        raw = urlsafe_b64encode(msg)
        if not removePadding:
            return raw
        b = bytearray(raw)
        # remove b64 padding
        while b[len(b)-1] == 61:
            del b[len(b)-1]
        return bytes(b)
        
    @staticmethod
    def UUID1SafeGenRandom() -> UUID:
        u = uuid1()
        return UUID(
            fields=(
                u.time_low,
                u.time_mid,
                u.time_hi_version,
                u.clock_seq_hi_variant,
                u.clock_seq_low, 
                int.from_bytes(bytes=os.urandom(6), byteorder='big')
            ),
            version=u.version,
            is_safe=u.is_safe
            )
    
    @staticmethod
    def rotlbyte(val: int, rot: int):
        return (((val << rot) | (val >> (8 - rot))) & 0xff)

    @staticmethod
    def rotrbyte(val: int, rot: int):
        return (((val >> rot) | (val << (8 - rot))) & 0xff)

    @staticmethod
    def bytesrotl(b: bytearray, rot: int) -> bytearray:
        ret = b.copy()
        rot &= 0xff
        for t in range(len(b)):
            ret[t] = MsSecurity.rotlbyte(ret[t], rot)
        return ret

    @staticmethod
    def bytesrotr(b: bytearray, rot: int) -> bytearray:
        ret = b.copy()
        rot &= 0xff
        for t in range(len(b)):
            ret[t] = MsSecurity.rotrbyte(ret[t], rot)
        return ret
