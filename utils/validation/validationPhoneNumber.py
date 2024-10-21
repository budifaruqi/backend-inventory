from phonenumbers import parse as phonenumbers_parse, phonenumberutil, country_code_for_valid_region

from utils.util_http_exception import MsHTTPBadRequestException
from utils.util_http_response import MsHTTPExceptionMessage, MsHTTPExceptionType
from utils.validation.validationPhoneNumberConst import DEFAULT_PHONE_REGION, MAX_PHONE_LENGTH, MIN_PHONE_LENGTH

class ValidatePhoneNumberResult:
    
    def __init__(self, country_code: int, national_number: int) -> None:
        self.national_number = national_number
        self.country_code = country_code

    def Validate(self, phoneRef: str) -> str:
        national_number_str = str(self.national_number)
        l = len(national_number_str)
        if (l >= MIN_PHONE_LENGTH) and (l <= MAX_PHONE_LENGTH):
            if self.country_code is not None:
                if self.country_code == 62:

                    stripPhone = ""
                    for i in range(len(phoneRef)):
                        s = phoneRef[i]
                        if (s == "+") or s.isnumeric():
                            stripPhone += s
                            
                    # print("strip 2: " + national_number_str[2:] + " " + stripPhone[2:])
                    if (stripPhone[0] == "0") and (stripPhone[1:] == national_number_str):
                        # 081226526666
                        # (0298)123456
                        # (0298) 123456
                        # (0298)-123456
                        # 0298-123456
                        ret62 = "0" + national_number_str
                    elif (stripPhone[:2] == "62") and (stripPhone[2:] == national_number_str):
                        # 6281226526666
                        # print("mode 2")
                        ret62 = "0" + national_number_str

                    elif (stripPhone[:2] == "62") and (stripPhone[2:] == national_number_str[2:]):
                        # 6281226526666
                        # print("mode 3")
                        ret62 = "0" + national_number_str[2:]

                    elif (stripPhone[:3] == "+62") and (stripPhone[3:] == national_number_str):
                        # +6281226526666
                        ret62 = "0" + national_number_str
                    elif (stripPhone[:3] == "620") and (stripPhone[3:] == national_number_str):
                        # none of mobile prefix leading zero
                        # 62081226526666
                        ret62 = "0" + national_number_str
                    elif (stripPhone[:4] == "+620") and (stripPhone[4:] == national_number_str):
                        # none of mobile prefix leading zero
                        # +62081226526666
                        ret62 = "0" + national_number_str
                    else:
                        if (stripPhone[0] != "+") and (stripPhone[0] != "0"):
                            # trying to test phone number with country code without + sign
                            # e.g: 44123456789
                            for regionCode in phonenumberutil.SUPPORTED_REGIONS:
                                countryCode = country_code_for_valid_region(regionCode)
                                strCountryCode = str(countryCode)
                                if strCountryCode[0] != stripPhone[0]:
                                    continue
                                if not stripPhone.startswith(strCountryCode):
                                    continue
                                try:
                                    testNumber = phonenumbers_parse("+" + stripPhone, regionCode, _check_region=True)
                                    self.country_code = testNumber.country_code
                                    self.national_number = testNumber.national_number
                                    national_number_str = str(self.national_number)
                                except:
                                    pass
                                break
                        return "+" + str(self.country_code) + national_number_str
                    
                    # validate phone length leading zero
                    if len(ret62) > MAX_PHONE_LENGTH:
                        raise MsHTTPBadRequestException(
                            type=MsHTTPExceptionType.INVALID_PHONE_NUMBER,
                            message=MsHTTPExceptionMessage.INVALID_PHONE_NUMBER
                        )
                    return ret62
                else:
                    return "+" + str(self.country_code) + national_number_str
            else:
                return national_number_str
        else:
            raise MsHTTPBadRequestException(
                type=MsHTTPExceptionType.INVALID_PHONE_NUMBER,
                message=MsHTTPExceptionMessage.INVALID_PHONE_NUMBER
            )
    
def ValidatePhoneNumberEx(phone_number: str | None) -> ValidatePhoneNumberResult:
    """
    Function to validate phone number

    Convert only +62 leading zero +628123456 >> 08123456
    ref: https://en.wikipedia.org/wiki/List_of_country_calling_codes
    """

    if (phone_number is None) or (len(phone_number) == 0):
        raise MsHTTPBadRequestException(
            type=MsHTTPExceptionType.EMPTY_PHONE_NUMBER,
            message=MsHTTPExceptionMessage.EMPTY_PHONE_NUMBER
        )
    
    phone_number = phone_number.strip()
    if (len(phone_number) == 0):
        raise MsHTTPBadRequestException(
            type=MsHTTPExceptionType.EMPTY_PHONE_NUMBER,
            message=MsHTTPExceptionMessage.EMPTY_PHONE_NUMBER
        )
    
    # no country code start with +0 LOL
    if phone_number.startswith("+0"):
        phone_number = phone_number.replace("+0", "0").strip()
        if (len(phone_number) == 0):
            raise MsHTTPBadRequestException(
                type=MsHTTPExceptionType.EMPTY_PHONE_NUMBER,
                message=MsHTTPExceptionMessage.EMPTY_PHONE_NUMBER
            )
    
    try:
        my_number = phonenumbers_parse(phone_number, DEFAULT_PHONE_REGION, _check_region=True)
    except:
        try:
            my_number = phonenumbers_parse(phone_number, None)
        except:
            raise MsHTTPBadRequestException(
                type=MsHTTPExceptionType.UNSUPPORTED_PHONE_NUMBER,
                message="Kode negara nomor telepon tidak didukung",
                additionalData={
                    "phone": phone_number
                }
            )
    
    if my_number.national_number is None:
        raise MsHTTPBadRequestException(
            type=MsHTTPExceptionType.INVALID_PHONE_NUMBER,
            message=MsHTTPExceptionMessage.INVALID_PHONE_NUMBER.value + ". Nomor wilayah kosong"
        )
    if my_number.country_code is None:
        raise MsHTTPBadRequestException(
            type=MsHTTPExceptionType.INVALID_PHONE_NUMBER,
            message=MsHTTPExceptionMessage.INVALID_PHONE_NUMBER.value + ". Nomor kode negara kosong"
        )
    return ValidatePhoneNumberResult(
        country_code=my_number.country_code,
        national_number=my_number.national_number
    )
    
def ValidatePhoneNumber(phone_number: str) -> str:
    """
    Function to validate phone number

    Convert only +62 leading zero +628123456 >> 08123456
    ref: https://en.wikipedia.org/wiki/List_of_country_calling_codes
    """

    phone_number = phone_number.strip()
    val = ValidatePhoneNumberEx(phone_number)
    return val.Validate(phone_number)
