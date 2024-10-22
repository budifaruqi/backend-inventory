from enum import Enum, IntEnum

class MsHTTPExceptionType(str, Enum):

    # 400
    BAD_REQUEST = "BAD_REQUEST"
    EMPTY_FIELD = "EMPTY_FIELD"
    INVALID_FIELD = "INVALID_FIELD"
    
    INVALID_DATE_RANGE = "INVALID_DATE_RANGE"
    INVALID_DATETIME_RANGE = "INVALID_DATETIME_RANGE"
    INVALID_TIME_RANGE = "INVALID_TIME_RANGE"

    INVALID_MIN_DATE_RANGE = "INVALID_MIN_SEARCH_DATE_RANGE"
    INVALID_MIN_DATETIME_RANGE = "INVALID_MIN_DATETIME_RANGE"
    INVALID_MIN_TIME_RANGE = "INVALID_MIN_TIME_RANGE"

    UNSUPPORTED_TIMEZONE = "UNSUPPORTED_TIMEZONE"
    NON_ASCII_CHARACTER = "NON_ASCII_CHARACTER"
    FEATURE_DISABLED = "DISABLED"

    INVALID_PHONE_NUMBER = "INVALID_PHONE_NUMBER"
    UNSUPPORTED_PHONE_NUMBER = "UNSUPPORTED_PHONE_NUMBER"
    EMPTY_PHONE_NUMBER = "EMPTY_PHONE_NUMBER"
    PHONE_NUMBER_TOO_SHORT = "PHONE_NUMBER_TOO_SHORT"
    
    INVALID_EMAIL_ADDRESS = "INVALID_EMAIL_ADDRESS"
    EMPTY_EMAIL_ADDRESS = "EMPTY_EMAIL_ADDRESS"
    EMAIL_ADDRESS_TOO_LONG = "EMAIL_ADDRESS_TOO_LONG"
    # place other error 400 here
    
    # 401
    UNAUTHORIZED = "UNAUTHORIZED"
    AUTHENTICATION_FAILED = "AUTHENTICATION_FAILED"

    # 403
    FORBIDDEN = "FORBIDDEN"
    ACCESS_FORBIDDEN = "ACCESS_FORBIDDEN"
    NOT_AUTHENTICATED = "NOT_AUTHENTICATED"
    INVALID_AUTHENTICATION_CREDENTIALS = "INVALID_AUTHENTICATION_CREDENTIALS"
    
    # place other error 403 here
    CREDENTIAL_LOCATION_COMPANY_FORBIDDEN = "CREDENTIAL_LOCATION_COMPANY_FORBIDDEN"
    CREDENTIAL_LOCATION_SYSTEM_FORBIDDEN = "CREDENTIAL_LOCATION_SYSTEM_FORBIDDEN"
    
    # 404
    NOT_FOUND = "NOT_FOUND"
    PAGE_NOT_FOUND = "PAGE_NOT_FOUND"
    MASTER_DATA_NOT_EXIST = "MASTER_DATA_NOT_EXIST"
    # place other error 404 here
    
    # 409
    CONFLICT = "CONFLICT"
    ALREADY_EXISTS = "ALREADY_EXISTS"
    MASTER_DATA_NAME_ALREADY_EXISTS = "MASTER_DATA_NAME_ALREADY_EXISTS"
    LEAD_NAME_ALREADY_EXISTS = "LEAD_NAME_ALREADY_EXISTS"
    LEAD_TAG_NAME_ALREADY_EXISTS = "LEAD_TAG_NAME_ALREADY_EXISTS"
    PARTNER_NAME_ALREADY_EXISTS = "PARTNER_NAME_ALREADY_EXISTS"
    UOM_CATEGORY_NAME_ALREADY_EXISTS = "UOM_CATEGORY_NAME_ALREADY_EXISTS"
    UOM_NAME_ALREADY_EXISTS = "UOM_NAME_ALREADY_EXISTS"
    GENERIC_MATERIAL_CATEGORY_NAME_ALREADY_EXISTS = "GENERIC_MATERIAL_CATEGORY_NAME_ALREADY_EXISTS"
    GENERIC_MATERIAL_NAME_ALREADY_EXISTS = "GENERIC_MATERIAL_NAME_ALREADY_EXISTS"






    # 413
    REQUEST_ENTITY_TOO_LARGE = "REQUEST_ENTITY_TOO_LARGE"
    FILE_TOO_LARGE = "FILE_TOO_LARGE"
    IMAGE_DIMENSION_TOO_LARGE = "IMAGE_DIMENSION_TOO_LARGE"
    IMAGE_WIDTH_TOO_LARGE = "IMAGE_WIDTH_TOO_LARGE"
    IMAGE_HEIGHT_TOO_LARGE = "IMAGE_HEIGHT_TOO_LARGE"

    #415
    UNSUPPORTED_MEDIA_TYPE = "UNSUPPORTED_MEDIA_TYPE"
    UNKNOWN_FILE_EXTENSION = "UNKNOWN_FILE_EXTENSION"
    INVALID_IMAGE_DIMENSION = "INVALID_IMAGE_DIMENSION"
    UNKNOWN_IMAGE_FORMAT = "UNKNOWN_IMAGE_FORMAT"
    UNKNOWN_SVG_FORMAT = "UNKNOWN_SVG_FORMAT"
    EMPTY_FILE = "EMPTY_FILE"
    UNSUPPORTED_FILE = "UNSUPPORTED_FILE"

    # 422
    UNPROCESSABLE_ENTITY = "UNPROCESSABLE_ENTITY"
    VALIDATION_ERROR = "VALIDATION_ERROR"

    INVALID_PATH = "INVALID_PATH"

    # 429
    TOO_MANY_REQUESTS = "TOO_MANY_REQUESTS"

    # 500
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    EXTERNAL_SERVER_ERROR = "EXTERNAL_SERVER_ERROR" # error from external service
    UNSUPPORTED_AUTHENTICATION_REQUEST = "UNSUPPORTED_AUTHENTICATION_REQUEST"
    EXTERNAL_SERVER_ERROR_CONNECTION_TIMEOUT = "EXTERNAL_SERVER_ERROR_CONNECTION_TIMEOUT" # error from external service
    UNSUPPORTED_FEATURE = "UNSUPPORTED_FEATURE"
    FAILED_CREATE_DIRECTORY = "FAILED_CREATE_DIRECTORY"
    FAILED_SAVE_FILE = "FAILED_SAVE_FILE"
    UNHANDLED_SYSTEM = "UNHANDLED_SYSTEM"
    FAILED_CREATE_PASSWORD = "FAILED_CREATE_PASSWORD"
    UNSUPPORTED_SESSION = "UNSUPPORTED_SESSION"
    FAILED_UPLOAD_IMAGE = "FAILED_UPLOAD_IMAGE"
    FAILED_SEND_EMAIL = "FAILED_SEND_EMAIL"
    SECURITY_KEY_NOT_AVAILABLE = "SECURITY_KEY_NOT_AVAILABLE"
    INVALID_RSA_PRIVATE_KEY = "INVALID_RSA_PRIVATE_KEY"
    INVALID_RSA_PUBLIC_KEY = "INVALID_RSA_PUBLIC_KEY"
    NOT_RSA_PRIVATE_KEY = "NOT_RSA_PRIVATE_KEY"
    NOT_RSA_PUBLIC_KEY = "NOT_RSA_PUBLIC_KEY"
    FAILED_CREATE_TOKEN = "FAILED_CREATE_TOKEN"
    FAILED_ENCRYPT_TOKEN = "FAILED_ENCRYPT_TOKEN"
    # place other error 500 here
    SECURITY_CREDENTIAL_NOT_AVAILABLE = "SECURITY_CREDENTIAL_NOT_AVAILABLE"
    UNSUPPORTED_SIGNATURE_ALGORITHM = "UNSUPPORTED_SIGNATURE_ALGORITHM"

    EXTERNAL_SERVER_ERROR_AUTH_SERVICE = "EXTERNAL_SERVER_ERROR_AUTH_SERVICE"
    EXTERNAL_SERVER_ERROR_AUTH_SERVICE_INVALID_SUCCESS_RESPONSE = "EXTERNAL_SERVER_ERROR_AUTH_SERVICE_INVALID_SUCCESS_RESPONSE"
    EXTERNAL_SERVER_ERROR_AUTH_SERVICE_INVALID_FAILED_RESPONSE = "EXTERNAL_SERVER_ERROR_AUTH_SERVICE_INVALID_FAILED_RESPONSE"

    # 501
    NOT_IMPLEMENTED = "NOT_IMPLEMENTED"

    # 503
    SERVICE_UNAVAILABLE = "SERVICE_UNAVAILABLE"
    #
    AUTH_SERVICE_UNAVAILABLE = "AUTH_SERVICE_UNAVAILABLE"
    
    # 504
    GATEWAY_TIMEOUT = "GATEWAY_TIMEOUT"
    
class MsHTTPExceptionMessage(str, Enum):
    # 200
    
    # 400
    BAD_REQUEST = "Bad request"
    EMPTY_FIELD_F = "Bagian {fieldName} belum diisi"
    INVALID_FIELD_F = "Isi bagian {fieldName} salah"

    INVALID_DATE_RANGE = "Rentang tanggal salah"
    INVALID_DATE_RANGE_F = "Rentang tanggal salah, antara {dateStart} dan {dateFinish}"
    INVALID_DATETIME_RANGE = "Rentang tanggal dan waktu salah"
    INVALID_DATETIME_RANGE_F = "Rentang tanggal dan waktu salah, antara {datetimeStart} dan {datetimeFinish}"
    INVALID_TIME_RANGE = "Rentang waktu salah"
    INVALID_TIME_RANGE_F = "Rentang waktu salah, antara jam {timeStart} sampai {timeFinish}"

    INVALID_MIN_DATE_RANGE_F = "Minimum rentang tanggal tidak boleh lebih kecil dari {minDate}"
    INVALID_MIN_DATETIME_RANGE_F = "Minimum rentang tanggal dan waktu tidak boleh lebih kecil dari {minDatetime}"
    INVALID_MIN_TIME_RANGE_F = "Minimum rentang waktu tidak boleh lebih kecil dari {minTime}"

    UNSUPPORTED_TIMEZONE_F = "Zona waktu {timeZone} tidak didukung"
    NON_ASCII_CHARACTER = "Teks harus berupa karakter ASCII"
    NON_ASCII_CHARACTER_F = "Bagian {fieldName} harus berupa karakter ASCII"
    FEATURE_DISABLED_F = "Fitur {featureName} tidak tersedia"

    INVALID_PHONE_NUMBER = "Format nomor telepon salah"
    UNSUPPORTED_PHONE_NUMBER = "Format nomor telepon tidak didukung"
    EMPTY_PHONE_NUMBER = "Nomor telepon belum diisi"
    PHONE_NUMBER_TOO_SHORT = "Panjang nomor telepon terlalu pendek"

    INVALID_EMAIL_ADDRESS = "Alamat email tidak sesuai format"
    EMPTY_EMAIL_ADDRESS = "Alamat email belum diisi"
    EMAIL_ADDRESS_TOO_LONG_F = "Alamat email terlalu panjang, maksimal {maxEmail} karakter"
    # place other error 400 here

    # 401
    UNAUTHORIZED = "Tidak sah"
    NOT_AUTHENTICATED = "Tidak diautentikasi"
    AUTHENTICATION_FAILED = "Autentikasi gagal. Sesi telah kadaluarsa atau tidak sah"
    INVALID_AUTHENTICATION_CREDENTIALS = "Kredensial autentikasi tidak sah"
    # place other error 401 here

    # 403
    FORBIDDEN = "Forbidden"
    EMPTY_CREDENTIAL = "Permintaan masuk tidak dapat diproses, kredensial belum diisi"
    ROLE_REQUIRED = "Anda tidak mempunyai peran hak akses untuk mengakses informasi ini"
    PERMISSION_REQUIRED = "Anda tidak mempunyai izin hak akses untuk mengakses informasi ini"
    UNAUTHORIZED_ROLE = "Peran hak akses yang anda gunakan tidak diperuntukkan untuk mengakses informasi ini"
    UNAUTHORIZED_PERMISSION = "Izin hak akses yang anda gunakan tidak diperuntukkan untuk mengakses informasi ini"
    UNAUTHORIZED_ROLE_OR_PERMISSION = "Peran atau izin hak akses yang anda gunakan tidak diperuntukkan untuk mengakses informasi ini"
    # place other error 403 here
    CREDENTIAL_LOCATION_COMPANY_FORBIDDEN = "Kredensial lokasi perusahaan tidak diperkenankan mengakses informasi ini"
    CREDENTIAL_LOCATION_SYSTEM_FORBIDDEN = "Kredensial lokasi sistem tidak diperkenankan mengakses informasi ini"

    # 404
    NOT_FOUND = "Tidak ditemukan"
    PAGE_NOT_FOUND = "Halaman yang anda coba akses tidak tersedia"
    MASTER_DATA_NOT_FOUND = "Master Data tidak ditemukan"
    MASTER_DATA_FOLLOWER_NOT_FOUND = "Master Data Follower tidak ditemukan"
    STATUS_NOT_MATCH = "Status tidak sesuai"
    LEAD_TAG_NOT_FOUND = "Lead Tag tidak ditemukan"
    PARTNER_NOT_FOUND = "Partner tidak ditemukan"
    UOM_CATEGORY_NOT_FOUND = "Kategori Unit Of Measure tidak ditemukan"
    UOM_NOT_FOUND = "Unit Of Measure tidak ditemukan"
    GENERIC_MATERIAL_CATEGORY_NOT_FOUND = "Kategori Generic Material tidak ditemukan"
    GENERIC_MATERIAL_NOT_FOUND = "Generic Material tidak ditemukan"


    # place other error 404 here
    
    # 409
    CONFLICT = "Conflict"
    ALREADY_EXISTS_F = "{field_title} sudah ada"
    MASTER_DATA_NAME_ALREADY_EXISTS_F = "Nama Master Data \"{name}\" sudah terdaftar"
    LEAD_TAG_NAME_ALREADY_EXISTS_F = "Nama Lead Tag \"{name}\" sudah terdaftar"
    LEAD_NAME_ALREADY_EXISTS_F = "Nama Lead \"{name}\" sudah terdaftar"
    PARTNER_NAME_ALREADY_EXISTS_F = "Nama Partner \"{name}\" sudah terdaftar"
    MASTER_DATA_FOLLOWER_ALREADY_EXIST = "Master Data Follower sudah ada"
    UOM_CATEGORY_NAME_ALREADY_EXISTS_F = "Nama Kategori Unit of Measure \"{name}\" sudah terdaftar"
    UOM_NAME_ALREADY_EXISTS_F = "Nama Unit of Measure \"{name}\" sudah terdaftar"
    GENERIC_MATERIAL_CATEGORY_NAME_ALREADY_EXISTS_F = "Nama Kategori Generic Material \"{name}\" sudah terdaftar"
    GENERIC_MATERIAL_NAME_ALREADY_EXISTS_F = "Nama Generic Material \"{name}\" sudah terdaftar"



    # place other error 409 here
    
    # 413
    REQUEST_ENTITY_TOO_LARGE = "Request entity too large"
    FILE_TOO_LARGE = "Ukuran berkas terlalu besar"
    FILE_TOO_LARGE_F = "Ukuran berkas terlalu besar, maksimal {maxSize}"
    IMAGE_FILE_TOO_LARGE_F = "Ukuran berkas gambar terlalu besar, maksimal {maxSize}"
    IMAGE_WIDTH_TOO_LARGE = "Ukuran lebar dimensi gambar terlalu besar"
    IMAGE_WIDTH_TOO_LARGE_F = "Ukuran lebar dimensi gambar terlalu besar ({img_w} px). Maksimal {maxWidth} px"
    IMAGE_HEIGHT_TOO_LARGE = "Ukuran tinggi dimensi gambar terlalu besar"
    IMAGE_HEIGHT_TOO_LARGE_F = "Ukuran tinggi dimensi gambar terlalu besar ({img_h} px). Maksimal {maxHeight} px"
    # place other error 413 here

    # 415
    UNSUPPORTED_MEDIA_TYPE = "Jenis berkas tidak didukung"
    UNKNOWN_FILE_EXTENSION = "Ekstensi berkas tidak diketahui"
    UNSUPPORTED_FILE = "Berkas tidak didukung"
    UNKNOWN_IMAGE_FORMAT = "Format gambar tidak diketahui"
    UNKNOWN_SVG_FORMAT = "Format gambar svg tidak diketahui"
    EMPTY_FILE = "Berkas tidak ada isinya (kosong)"
    EMPTY_IMAGE_FILE = "Berkas gambar tidak ada isinya (kosong)"
    UNSUPPORTED_MEDIA_TYPE_IMAGE = "Format berkas gambar tidak didukung"
    INVALID_IMAGE_DIMENSION = "Ukuran dimensi gambar tidak sesuai"
    # place other error 415 here

    # 422
    UNPROCESSABLE_ENTITY = "Invalid request entity"
    # place other error 422 here

    # 429
    TOO_MANY_REQUESTS = "Terlalu banyak permintaan yang diproses"
    # place other error 429 here

    # 500
    INTERNAL_SERVER_ERROR = "Terjadi kesalahan pada internal server"
    EXTERNAL_SERVER_ERROR = "Terjadi kesalahan pada eksternal server"
    UNSUPPORTED_AUTHENTICATION_REQUEST = "Permintaan autentikasi tidak didukung"
    UNSUPPORTED_FEATURE = "Fitur belum tersedia"
    FAILED_CREATE_DIRECTORY = "Gagal membuat directori"
    FAILED_SAVE_FILE = "Gagal menyimpan berkas"
    UNHANDLED_SYSTEM = "Sistem tidak menangani proses ini"
    FAILED_CREATE_PASSWORD = "Gagal menyandikan kata sandi"
    UNSUPPORTED_SESSION = "Sesi tidak mendukung"
    FAILED_UPLOAD_IMAGE = "Gagal mengunggah gambar"
    FAILED_SEND_EMAIL = "Gagal mengirim surel"
    SECURITY_KEY_NOT_AVAILABLE = "Sandi keamanan sistem tidak tersedia"
    FAILED_CREATE_TOKEN = "Gagal membuat token"
    FAILED_ENCRYPT_TOKEN = "Gagal menyandikan token"
    # place other error 500 here
    INVALID_RSA_PUBLIC_KEY = "Kunci publik RSA yang terpasang tidak sesuai"
    INVALID_RSA_PRIVATE_KEY = "Kunci pribadi RSA yang terpasang tidak sesuai"
    NOT_RSA_PRIVATE_KEY = "Kunci pribadi yang dimuat, bukan berjenis kunci pribadi RSA"
    NOT_RSA_PUBLIC_KEY = "Kunci publik yang dimuat, bukan berjenis kunci publik RSA"
    UNSUPPORTED_SIGNATURE_ALGORITHM = "Tanda tangan digital tidak didukung"

class MsHTTPStatusCode(IntEnum):
    RESPONSE_VALIDATION_ERROR = 522, 'Unprocessable Response Entity', 'Server failed to validate response'
    VALIDATION_ERROR = 523, 'Validation Error', 'Server failed to validate model validation'
    VALIDATION_ERROR_INPUT_IS_COROUTINE = 524, 'Input is coroutine', 'Server failed to validate coroutine'
    # database
    DATABASE_ERROR = 540, 'Database Error', 'General database error'
    DATABASE_CONNECTION_TIMEOUT = 541, 'Database Connection Timeout', 'Connection to database server timeout'
    OPERATION_DATABASE_ERROR = 542, 'Operation Database Error', 'Database operation fail'

    def __init__(self, _value: int, phrase: str = "", description: str = "") -> None:
        super().__init__()
        self._value_ = _value
        self._phrase = phrase
        self._description = description
        
    def __new__(cls, value: int, phrase: str = "", description: str = ""):
        obj = int.__new__(cls, value)
        obj._value_ = value

        obj._phrase = phrase
        obj._description = description
        return obj

    @property
    def phrase(self) -> str:
        return self._phrase

    @property
    def description(self) -> str:
        return self._description