from enum import Enum

class ValidationErrorLocation(str, Enum):
    body = "body"
    query = "query"
    header = "header"
    path = "path"
    cookie = "cookie"

class ValidationErrorType(str, Enum):

    VALIDATION_ERROR_BOOL_PARSING = "VALIDATION_ERROR_BOOL_PARSING"
    VALIDATION_ERROR_BOOL_TYPE = "VALIDATION_ERROR_BOOL_TYPE"
    VALIDATION_ERROR_BYTES_TOO_LONG = "VALIDATION_ERROR_BYTES_TOO_LONG"
    VALIDATION_ERROR_BYTES_TOO_SHORT = "VALIDATION_ERROR_BYTES_TOO_SHORT"
    VALIDATION_ERROR_BYTES_TYPE = "VALIDATION_ERROR_BYTES_TYPE"

    VALIDATION_ERROR_DATE_FROM_DATETIME_INEXACT = "VALIDATION_ERROR_DATE_FROM_DATETIME_INEXACT"
    VALIDATION_ERROR_DATE_FROM_DATETIME_PARSING = "VALIDATION_ERROR_DATE_FROM_DATETIME_PARSING"
    VALIDATION_ERROR_DATE_FUTURE = "VALIDATION_ERROR_DATE_FUTURE"
    VALIDATION_ERROR_DATE_PARSING = "VALIDATION_ERROR_DATE_PARSING"
    VALIDATION_ERROR_DATE_PAST = "VALIDATION_ERROR_DATE_PAST"
    VALIDATION_ERROR_DATE_TYPE = "VALIDATION_ERROR_DATE_TYPE"

    VALIDATION_ERROR_DATETIME_FROM_DATE_PARSING = "VALIDATION_ERROR_DATETIME_FROM_DATE_PARSING"
    VALIDATION_ERROR_DATETIME_FUTURE = "VALIDATION_ERROR_DATETIME_FUTURE"
    VALIDATION_ERROR_DATETIME_OBJECT_INVALID = "VALIDATION_ERROR_DATETIME_OBJECT_INVALID"
    VALIDATION_ERROR_DATETIME_PARSING = "VALIDATION_ERROR_DATETIME_PARSING"
    VALIDATION_ERROR_DATETIME_PAST = "VALIDATION_ERROR_DATETIME_PAST"
    VALIDATION_ERROR_DATETIME_TYPE = "VALIDATION_ERROR_DATETIME_TYPE"

    VALIDATION_ERROR_DECIMAL_MAX_DIGITS = "VALIDATION_ERROR_DECIMAL_MAX_DIGITS"
    VALIDATION_ERROR_DECIMAL_MAX_PLACES = "VALIDATION_ERROR_DECIMAL_MAX_PLACES"
    VALIDATION_ERROR_DECIMAL_PARSING = "VALIDATION_ERROR_DECIMAL_PARSING"
    VALIDATION_ERROR_DECIMAL_TYPE = "VALIDATION_ERROR_DECIMAL_TYPE"
    VALIDATION_ERROR_DECIMAL_WHOLE_DIGITS = "VALIDATION_ERROR_DECIMAL_WHOLE_DIGITS"

    VALIDATION_ERROR_DICT_TYPE = "VALIDATION_ERROR_DICT_TYPE"
    VALIDATION_ERROR_ENUM = "VALIDATION_ERROR_ENUM"
    VALIDATION_ERROR_EXTRA_FORBIDDEN = "VALIDATION_ERROR_EXTRA_FORBIDDEN"

    VALIDATION_ERROR_FINITE_NUMBER = "VALIDATION_ERROR_FINITE_NUMBER"
    VALIDATION_ERROR_FLOAT_PARSING = "VALIDATION_ERROR_FLOAT_PARSING"
    VALIDATION_ERROR_FLOAT_TYPE = "VALIDATION_ERROR_FLOAT_TYPE"

    VALIDATION_ERROR_GET_ATTRIBUTE_ERROR = "VALIDATION_ERROR_GET_ATTRIBUTE_ERROR"

    VALIDATION_ERROR_GREATER_THAN = "VALIDATION_ERROR_GREATER_THAN"
    VALIDATION_ERROR_GREATER_THAN_EQUAL = "VALIDATION_ERROR_GREATER_THAN_EQUAL"

    VALIDATION_ERROR_INT_FROM_FLOAT = "VALIDATION_ERROR_INT_FROM_FLOAT"
    VALIDATION_ERROR_INT_PARSING = "VALIDATION_ERROR_INT_PARSING"
    VALIDATION_ERROR_INT_PARSING_SIZE = "VALIDATION_ERROR_INT_PARSING_SIZE"
    VALIDATION_ERROR_INT_TYPE = "VALIDATION_ERROR_INT_TYPE"

    VALIDATION_ERROR_INVALID_KEY = "VALIDATION_ERROR_INVALID_KEY"
    VALIDATION_ERROR_IS_INSTANCE_OF = "VALIDATION_ERROR_IS_INSTANCE_OF"
    VALIDATION_ERROR_IS_SUBCLASS_OF = "VALIDATION_ERROR_IS_SUBCLASS_OF"

    VALIDATION_ERROR_JSON_INVALID = "VALIDATION_ERROR_JSON_INVALID"
    VALIDATION_ERROR_JSON_TYPE = "VALIDATION_ERROR_JSON_TYPE"

    VALIDATION_ERROR_LESS_THAN = "VALIDATION_ERROR_LESS_THAN"
    VALIDATION_ERROR_LESS_THAN_EQUAL = "VALIDATION_ERROR_LESS_THAN_EQUAL"

    VALIDATION_ERROR_LIST_TYPE = "VALIDATION_ERROR_LIST_TYPE"
    VALIDATION_ERROR_LITERAL_ERROR = "VALIDATION_ERROR_LITERAL_ERROR"
    VALIDATION_ERROR_MISSING = "VALIDATION_ERROR_MISSING"
    VALIDATION_ERROR_MODEL_ATTRIBUTES_TYPE = "VALIDATION_ERROR_MODEL_ATTRIBUTES_TYPE"
    VALIDATION_ERROR_MODEL_TYPE = "VALIDATION_ERROR_MODEL_TYPE"
    VALIDATION_ERROR_MULTIPLE_OF = "VALIDATION_ERROR_MULTIPLE_OF"
    VALIDATION_ERROR_NO_SUCH_ATTRIBUTE = "VALIDATION_ERROR_NO_SUCH_ATTRIBUTE"
    VALIDATION_ERROR_NONE_REQUIRED = "VALIDATION_ERROR_NONE_REQUIRED"
    VALIDATION_ERROR_SET_TYPE = "VALIDATION_ERROR_SET_TYPE"

    VALIDATION_ERROR_STRING_PATTERN_MISMATCH = "VALIDATION_ERROR_STRING_PATTERN_MISMATCH"
    VALIDATION_ERROR_STRING_SUB_TYPE = "VALIDATION_ERROR_STRING_SUB_TYPE"
    VALIDATION_ERROR_STRING_TOO_LONG = "VALIDATION_ERROR_STRING_TOO_LONG"
    VALIDATION_ERROR_STRING_TOO_SHORT = "VALIDATION_ERROR_STRING_TOO_SHORT"
    VALIDATION_ERROR_STRING_TYPE = "VALIDATION_ERROR_STRING_TYPE"
    VALIDATION_ERROR_STRING_UNICODE = "VALIDATION_ERROR_STRING_UNICODE"

    VALIDATION_ERROR_TIME_DELTA_PARSING = "VALIDATION_ERROR_TIME_DELTA_PARSING"
    VALIDATION_ERROR_TIME_DELTA_TYPE = "VALIDATION_ERROR_TIME_DELTA_TYPE"
    VALIDATION_ERROR_TIME_PARSING = "VALIDATION_ERROR_TIME_PARSING"
    VALIDATION_ERROR_TIME_TYPE = "VALIDATION_ERROR_TIME_TYPE"
    VALIDATION_ERROR_TIMEZONE_AWARE = "VALIDATION_ERROR_TIMEZONE_AWARE"
    VALIDATION_ERROR_TIMEZONE_NAIVE = "VALIDATION_ERROR_TIMEZONE_NAIVE"

    VALIDATION_ERROR_TOO_LONG = "VALIDATION_ERROR_TOO_LONG"
    VALIDATION_ERROR_TOO_SHORT = "VALIDATION_ERROR_TOO_SHORT"

    VALIDATION_ERROR_TUPLE_TYPE = "VALIDATION_ERROR_TUPLE_TYPE"

    VALIDATION_ERROR_UNION_TAG_INVALID = "VALIDATION_ERROR_UNION_TAG_INVALID"
    VALIDATION_ERROR_UNION_TAG_NOT_FOUND = "VALIDATION_ERROR_UNION_TAG_NOT_FOUND"

    VALIDATION_ERROR_URL_PARSING = "VALIDATION_ERROR_URL_PARSING"
    VALIDATION_ERROR_URL_SCHEME = "VALIDATION_ERROR_URL_SCHEME"
    VALIDATION_ERROR_URL_SYNTAX_VIOLATION = "VALIDATION_ERROR_URL_SYNTAX_VIOLATION"
    VALIDATION_ERROR_URL_TOO_LONG = "VALIDATION_ERROR_URL_TOO_LONG"
    VALIDATION_ERROR_URL_TYPE = "VALIDATION_ERROR_URL_TYPE"

    VALIDATION_ERROR_UUID_PARSING = "VALIDATION_ERROR_UUID_PARSING"
    VALIDATION_ERROR_UUID_TYPE = "VALIDATION_ERROR_UUID_TYPE"
    VALIDATION_ERROR_UUID_VERSION = "VALIDATION_ERROR_UUID_VERSION"

    VALIDATION_ERROR_VALUE_ERROR = "VALIDATION_ERROR_VALUE_ERROR"
    #
    VALIDATION_ERROR_UNKNOWN_ERROR = "VALIDATION_ERROR_UNKNOWN_ERROR"
    #
    VALIDATION_ERROR_INVALID_OBJECT_ID = "INVALID_OBJECT_ID"
    VALIDATION_ERROR_INVALID_PHONE_NUMBER = "VALIDATION_ERROR_INVALID_PHONE_NUMBER"
    VALIDATION_ERROR_INVALID_EMAIL_ADDRESS = "VALIDATION_ERROR_INVALID_EMAIL_ADDRESS"
    VALIDATION_ERROR_INVALID_IP_ANY_ADDRESS = "VALIDATION_ERROR_INVALID_IP_ANY_ADDRESS"
    VALIDATION_ERROR_INVALID_IP_V4_ADDRESS = "VALIDATION_ERROR_INVALID_IP_V4_ADDRESS"
    VALIDATION_ERROR_INVALID_IP_V6_ADDRESS = "VALIDATION_ERROR_INVALID_IP_V6_ADDRESS"

class ValidationErrorMessage(str, Enum):

    BOOL_PARSING_F = "Gagal menguraikan bagian '{fieldName}' (harus dalam bentuk format boolean)"
    BOOL_TYPE_F = "Nilai bagian '{fieldName}' harus bertipe boolean"

    BYTES_TOO_LONG_F = "Jumlah bytes pada bagian '{fieldName}' terlalu panjang"
    BYTES_TOO_SHORT_F = "Jumlah bytes pada bagian '{fieldName}' terlalu pendek"
    BYTES_TYPE_F = "Nilai bagian '{fieldName}' harus bertipe bytes"

    DATE_FROM_DATETIME_INEXACT_F = "Gagal menguraikan bagian '{fieldName}' (harus dalam bentuk format tanggal atau tanggal dengan waktu bernilai 0)"
    DATE_FROM_DATETIME_PARSING_F = "Gagal menguraikan bagian '{fieldName}' (harus dalam bentuk format tanggal)"
    DATE_FUTURE_F = "Tanggal bagian '{fieldName}' harus lebih besar dari hari ini"
    DATE_PARSING_F = "Gagal menguraikan bagian '{fieldName}' (harus dalam bentuk format tanggal)"
    DATE_PAST_F = "Tanggal bagian '{fieldName}' harus lebih kecil dari hari ini"
    DATE_TYPE_F = "Nilai bagian '{fieldName}' harus bertipe tanggal"

    DATETIME_FROM_DATE_PARSING_F = "Gagal menguraikan bagian '{fieldName}' (harus dalam bentuk format tanggal dan waktu)"
    DATETIME_FUTURE_F = "Tanggal dan waktu bagian '{fieldName}' harus lebih besar dari tanggal dan waktu saat ini"
    DATETIME_OBJECT_INVALID_F = "Bagian '{fieldName}' harus bertipe obyek tanggal dan waktu"
    DATETIME_PARSING_F = "Gagal menguraikan bagian '{fieldName}' (harus dalam bentuk format tanggal dan waktu)"
    DATETIME_PAST_F = "Tanggal dan waktu bagian '{fieldName}' harus lebih kecil dari tanggal dan waktu saat ini"
    DATETIME_TYPE_F = "Nilai bagian '{fieldName}' harus bertipe tanggal dan waktu"

    DECIMAL_MAX_DIGITS_F = "Jumlah digit bagian '{fieldName}' terlalu panjang"
    DECIMAL_MAX_PLACES_F = "Jumlah digit setelah koma bagian '{fieldName}' terlalu panjang"
    DECIMAL_PARSING_F = "Gagal menguraikan bagian '{fieldName}' (harus dalam bentuk format desimal)"
    DECIMAL_TYPE_F = "Nilai bagian '{fieldName}' harus bertipe desimal"
    DECIMAL_WHOLE_DIGITS_F = "Jumlah keseluruhan jumlah digit bagian '{fieldName}' terlalu panjang"

    DICT_TYPE_F = "Nilai bagian '{fieldName}' harus bertipe obyek"
    ENUM_MEMBER_F = "Nilai bagian '{fieldName}' harus bernilai sesuai dengan nilai yang diperbolehkan"
    EXTRA_FORBIDDEN_F = "Penambahan data tidak diizinkan"

    FINITE_NUMBER_F = "Nilai bagian '{fieldName}' terlalu besar atau diluar batas jangkauan (infinite)"
    FLOAT_PARSING_F = "Gagal menguraikan bagian '{fieldName}' (harus dalam bentuk format desimal atau float)"
    FLOAT_TYPE_F = "Nilai bagian '{fieldName}' harus bertipe desimal atau float"

    GET_ATTRIBUTE_ERROR_F = "Nilai atribut bagian '{fieldName}' tidak sesuai format"

    GREATER_THAN_F = "Nilai bagian '{fieldName}' harus lebih besar dari {gt}"
    GREATER_THAN_EQUAL_F = "Nilai bagian '{fieldName}' harus lebih besar atau sama dengan {ge}"

    INT_FROM_FLOAT_F = "Nilai bagian '{fieldName}' harus bertipe angka, bukan desimal atau float"
    INT_PARSING_F = "Gagal menguraikan nilai angka bagian '{fieldName}' (harus dalam bentuk format angka)"
    INT_PARSING_SIZE_F = "Nilai angka bagian '{fieldName}' diluar jangkauan atau tidak sesuai format angka"
    INT_TYPE_F = "Nilai bagian '{fieldName}' harus bertipe angka"

    INVALID_KEY = "Kunci obyek harus dalam bentuk format teks"
    IS_INSTANCE_OF = "Nilai bagian '{fieldName}' harus berupa obyek dengan class '{className}'"
    IS_SUBCLASS_OF = "Nilai bagian '{fieldName}' harus berupa obyek turunan dari class '{className}'"

    JSON_INVALID = "Gagal menguraikan data json"
    JSON_TYPE_F = "Nilai bagian '{fieldName}' harus bertipe obyek json"

    LESS_THAN_F = "Nilai bagian '{fieldName}' harus lebih kecil dari {lt}"
    LESS_THAN_EQUAL_F = "Nilai bagian '{fieldName}' harus lebih kecil atau sama dengan {le}"

    LIST_TYPE_F = "Nilai bagian '{fieldName}' harus bertipe larik"
    LITERAL_ERROR_F = "Nilai bagian '{fieldName}' harus sesuai ketentuan"
    MISSING_F = "Bagian '{fieldName}' harus diisi"
    MODEL_ATTRIBUTES_TYPE_F = "Atribut bagian '{fieldName}' harus sesuai dengan ketentuan obyek tersebut"
    MODEL_TYPE_F = "Input harus sesuai dengan ketentuan obyek tersebut"
    MULTIPLE_OF_F = "Nilai bagian '{fieldName}' harus kelipatan dari {multiple_of}"
    NO_SUCH_ATTRIBUTE_F = "Obyek tidak mempunyai atribut '{fieldName}'"
    NONE_REQUIRED_F = "Nilai '{fieldName}' harus bernilai null"
    SET_TYPE_F = "Bagian larik '{fieldName}' tidak sesuai ketentuan"

    STRING_PATTERN_MISMATCH_F = "Nilai bagian '{fieldName}' tidak sesuai dengan ketentuan pola"
    STRING_SUB_TYPE_F = "Nilai bagian '{fieldName}' harus berbentuk teks"
    STRING_TOO_LONG_F = "Jumlah karakter bagian '{fieldName}' terlalu panjang, maksimal {max_length} karakter"
    STRING_TOO_SHORT_F = "Jumlah karakter bagian '{fieldName}' terlalu pendek, minimal {min_length} karakter"
    STRING_TYPE_F = "Bagian '{fieldName}' harus berupa teks"
    STRING_UNICODE_F = "Gagal menguraikan karakter unicode pada bagian '{fieldName}'"

    TIME_DELTA_PARSING_F = "Gagal menguraikan tipe rentang waktu pada bagian '{fieldName}'"
    TIME_DELTA_TYPE_F = "Bagian '{fieldName}' tidak boleh kosong dan harus bertipe rentang waktu"
    
    TIME_PARSING_F = "Gagal menguraikan tipe waktu pada bagian '{fieldName}'"
    TIME_TYPE_F = "Bagian '{fieldName}' tidak boleh kosong dan harus bertipe waktu"
    
    TIMEZONE_AWARE_F = "Nilai tanggal dan waktu pada bagian '{fieldName}' harus menyertakan informasi zona waktu"
    TIMEZONE_NAIVE_F = "Nilai tanggal dan waktu pada bagian '{fieldName}' tidak boleh menyertakan informasi zona waktu"

    TOO_LONG_F = "Jumlah larik bagian '{fieldName}' terlalu banyak, maksimal berjumlah {max_length}"
    TOO_SHORT_F = "Jumlah larik bagian '{fieldName}' terlalu sedikit, minimal berjumlah {min_length}"

    TUPLE_TYPE_F = "Bagian '{fieldName}' tidak sesuai dengan format"

    UNION_TAG_INVALID_F = "Informasi penanda '{discriminator}' pada bagian '{fieldName}' salah"
    UNION_TAG_NOT_FOUND_F = "Informasi penanda '{discriminator}' pada bagian '{fieldName}' tidak ditemukan"

    URL_PARSING_F = "Gagal menguraikan url pada bagian '{fieldName}'"
    URL_SCHEME_F = "Sekema url pada bagian '{fieldName}' tidak sesuai ketentuan"
    URL_SYNTAX_VIOLATION_F = "Sintak url pada bagian '{fieldName}' menyalahi aturan"
    URL_TOO_LONG_F = "Panjang karakter url pada bagian '{fieldName}' terlalu panjang"
    URL_TYPE_F = "Bagian '{fieldName}' harus bertipe url"

    UUID_PARSING_F = "Gagal menguraikan UUID pada bagian '{fieldName}'"
    UUID_TYPE_F = "Bagian '{fieldName}' harus bertipe UUID"
    UUID_VERSION_F = "Versi UUID pada bagian '{fieldName}' tidak sesuai dengan versi UUID yang diharapkan, yaitu versi {expected_version}"

    VALUE_ERROR_F = "Terjadi kesalahan pembacaan data bagian '{fieldName}'"

    UNKNOWN_ERROR = "Informasi kesalahan data tidak tersedia"

    INVALID_OBJECT_ID_F = "Bagian '{fieldName}' harus bertipe object id"
    INVALID_PHONE_NUMBER_F = "Nomor telepon bagian '{fieldName}' tidak sesuai format yang berlaku"
    INVALID_EMAIL_ADDRESS_F = "Alamat email address bagian '{fieldName}' tidak sesuai ketentuan"
    INVALID_IP_ANY_ADDRESS_F = "Bagian '{fieldName}' harus berupa alamat IP dengan format IPv4 atau IPv6"
    INVALID_IP_V4_ADDRESS_F = "Bagian '{fieldName}' harus berupa alamat IP dengan format IPv4"
    INVALID_IP_V6_ADDRESS_F = "Bagian '{fieldName}' harus berupa alamat IP dengan format IPv6"