from ipaddress import ip_address
from fastapi import Request as FastApiRequest
from models.shared.modelDataType import ObjectId
from utils.util_logger import msLogger


class OtherUtil:

    SecondMenit = 60
    SecondJam = SecondMenit * 60
    Secondhari = SecondJam * 24

    @staticmethod
    def PrettySecond(second: int) -> str:
        if second <= 0:
            s = "0 detik"
            i = 0
        elif second < OtherUtil.SecondMenit:
            s = f"{second} detik"
            i = 0
        elif second < OtherUtil.SecondJam:
            s = f"{int(second // OtherUtil.SecondMenit)} menit"
            i = second % OtherUtil.SecondMenit
        elif second < OtherUtil.Secondhari:
            s = f"{int(second // OtherUtil.SecondJam)} jam"
            i = second % OtherUtil.SecondJam
        else:
            s = f"{int(second // OtherUtil.Secondhari)} hari"
            i = second % OtherUtil.Secondhari

        if i > 0:
            return s + ", " + OtherUtil.PrettySecond(i)
        else:
            return s
        
    @staticmethod
    def PrettyMinute(minute: int) -> str:
        return OtherUtil.PrettySecond(minute * OtherUtil.SecondMenit)
    
    @staticmethod
    def PrettyHour(hour: int) -> str:
        return OtherUtil.PrettySecond(hour * OtherUtil.SecondJam)
    
    @staticmethod
    def IncString(string: str | None) -> str | None:
        if string is None:
            return "A"
        string = string.strip()
        if string == "":
            return "A"
        if not string.isalpha():
            return None
        b = bytearray(string.encode(encoding="ascii"))
        for i in range(len(b), 0, -1):
            s = b[i-1]
            if s == 90: # Z
                b[i-1] = 65 # A
                if i == 1:
                    return "A" + b.decode(encoding="ascii")
            else:
                b[i-1] = s + 1
                return b.decode(encoding="ascii")

    @staticmethod
    def IntToStrLeadingZero(value: int, digit: int) -> str:
        if digit < 1:
            digit = 1
        fmt = "{:0" + str(digit) + "d}"
        return fmt.format(value)

    @staticmethod
    def PrettyObjectId(_id: ObjectId) -> str:
        idStr = str(_id)
        ret = ""
        for x in range(6):
            ret += idStr[x * 4: (x * 4) + 4]
            if x < 5:
                ret += "-"
        return ret
    
    @staticmethod
    def GetIpAddress(request: FastApiRequest, behindNAT: bool = False, proxyIpAddressHeaderName: str | None = None) -> str | None:
        try:
            addrs = ""
            if behindNAT and (proxyIpAddressHeaderName is not None):
                addrs = request.headers.get(proxyIpAddressHeaderName)
            if (addrs is None) or (len(addrs) == 0):
                addr = request.client
                if addr is not None:
                    addrs = addr.host

            if (addrs is not None) and (len(addrs) > 0):
                ip = ip_address(addrs)
                return str(ip)
        except Exception as err:
            msLogger.error(f"Error reading IP Address. {str(err)}")

        return None