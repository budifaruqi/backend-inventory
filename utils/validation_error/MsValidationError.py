
from typing import Any
from utils.validation_error.MsValidationErrorType import ValidationErrorLocation, ValidationErrorMessage, ValidationErrorType
from models.shared.modelDataType import ObjectId


def FastApiParseError(error: dict[str, Any]) -> dict[str, Any] | None:
    typeError = error.get("type")
    if (typeError is None) or (not isinstance(typeError, str)):
        return None
    loc: tuple[str | Any,] | None = error.get("loc")
    if (loc is None):
        return None
    loc0 = loc[0]
    if not isinstance(loc0, str):
       return None
    try:
        _ = ValidationErrorLocation(loc0)
    except:
        return None
    lengthLoc = len(loc)
    if lengthLoc < 1:
        return None
    # remove first index
    listLoc = list[str | Any](loc)
    listLoc.pop(0)
    locPydantic = tuple(listLoc)
    msgError = error.get("msg")
    if (msgError is None) or (not isinstance(msgError, str)):
        msgError = None
    ctx = error.get("ctx")

    return PydanticParseError(
        typeError,
        locPydantic,
        ctx,
        msgError
    )

def PydanticParseError(
    typeError: str,
    loc: tuple[str | Any, ...],
    ctx: dict[str, Any] | Any | None,
    msg: str | None
) -> dict[str, Any]:
    lengthLoc = len(loc)
    locStr: str | None = None
    fieldStr: str | None = None

    # get fieldStr
    locIndex = lengthLoc
    while locIndex > 0:
        s = loc[locIndex - 1]
        if (s is None):
            locIndex -= 1
        elif isinstance(s, str):
            fieldStr = s
            break
        else:
            locIndex -= 1

    # get locStr
    for i in range(lengthLoc):
        s = loc[i]
        if isinstance(s, str):
            if locStr is None:
                locStr = s
            else:
                locStr += ", " + s
        elif isinstance(s, int):
            if locStr is None:
                locStr = "indek ke " + str(s)
            else:
                locStr += ", " + "indek ke " + str(s)
    if locStr is None:
        locStr = "input"

    if (ctx is not None) and (isinstance(ctx, dict)):
        respCtx: Any = ctx
    else:
        respCtx = None
    # ----------------------------------------------------------
    if typeError == "bool_parsing":
        # This error is raised when the input value is a string that is not valid for coercion to a boolean
        t: str = ValidationErrorType.VALIDATION_ERROR_BOOL_PARSING.value
        m: str = ValidationErrorMessage.BOOL_PARSING_F.value.format(fieldName=locStr)
    elif typeError == "bool_type":
        # This error is raised when the input value's type is not valid for a `bool` field
        t: str = ValidationErrorType.VALIDATION_ERROR_BOOL_TYPE.value
        m: str = ValidationErrorMessage.BOOL_TYPE_F.value.format(fieldName=locStr)
    # ----------------------------------------------------------
    elif typeError == "bytes_too_long":
        # This error is raised when the length of a `bytes` value is greater than the field's `max_length` constraint
        t: str = ValidationErrorType.VALIDATION_ERROR_BYTES_TOO_LONG.value
        m: str = ValidationErrorMessage.BYTES_TOO_LONG_F.value.format(fieldName=locStr)
        if (ctx is not None) and (isinstance(ctx, dict)):
            max_length = ctx.get("max_length")
            if (max_length is not None) and (isinstance(max_length, int)):
                m += f", maksimal {max_length} bytes"
    elif typeError == "bytes_too_short":
        # This error is raised when the length of a `bytes` value is less than the field's `min_length` constraint
        t: str = ValidationErrorType.VALIDATION_ERROR_BYTES_TOO_SHORT.value
        m: str = ValidationErrorMessage.BYTES_TOO_SHORT_F.value.format(fieldName=locStr)
        if (ctx is not None) and (isinstance(ctx, dict)):
            min_length = ctx.get("min_length")
            if (min_length is not None) and (isinstance(min_length, int)):
                m += f", minimal {min_length} bytes"
    elif typeError == "bytes_type":
        # This error is raised when the input value's type is not valid for a `bytes` field
        t: str = ValidationErrorType.VALIDATION_ERROR_BYTES_TYPE.value
        m: str = ValidationErrorMessage.BYTES_TYPE_F.value.format(fieldName=locStr)
    # ----------------------------------------------------------
    elif typeError == "date_from_datetime_inexact":
        # This error is raised when the input `datetime` value provided for a `date` field has a nonzero time component.
        # For a timestamp to parse into a field of type `date`, the time components must all be zero
        t = ValidationErrorType.VALIDATION_ERROR_DATE_FROM_DATETIME_INEXACT.value
        m = ValidationErrorMessage.DATE_FROM_DATETIME_INEXACT_F.value.format(fieldName=locStr)
    elif typeError == "date_from_datetime_parsing":
        # This error is raised when the input value is a string that cannot be parsed for a `date` field
        t: str = ValidationErrorType.VALIDATION_ERROR_DATE_FROM_DATETIME_PARSING.value
        m: str = ValidationErrorMessage.DATE_FROM_DATETIME_PARSING_F.value.format(fieldName=locStr)
    elif typeError == "date_future":
        # This error is raised when the input value provided for a `FutureDate` field is not in the future
        t: str = ValidationErrorType.VALIDATION_ERROR_DATE_FUTURE.value
        m: str = ValidationErrorMessage.DATE_FUTURE_F.value.format(fieldName=locStr)
    elif typeError == "date_parsing":
        # This error is raised when validating JSON where the input value is string that cannot be parsed for a `date` field
        t: str = ValidationErrorType.VALIDATION_ERROR_DATE_PARSING.value
        m: str = ValidationErrorMessage.DATE_PARSING_F.value.format(fieldName=locStr)
    elif typeError == "date_past":
        # This error is raised when the value provided for a `PastDate` field is not in the past
        t: str = ValidationErrorType.VALIDATION_ERROR_DATE_PAST.value
        m: str = ValidationErrorMessage.DATE_PAST_F.value.format(fieldName=locStr)
    elif typeError == "date_type":
        # This error is raised when the input value's type is not valid for a `date` field
        t: str = ValidationErrorType.VALIDATION_ERROR_DATE_TYPE.value
        m: str = ValidationErrorMessage.DATE_TYPE_F.value.format(fieldName=locStr)
    # ----------------------------------------------------------
    elif typeError == "datetime_from_date_parsing":
        # This error is raised when the input value is a string that cannot be parsed for a `datetime` field
        t: str = ValidationErrorType.VALIDATION_ERROR_DATETIME_FROM_DATE_PARSING.value
        m: str = ValidationErrorMessage.DATETIME_FROM_DATE_PARSING_F.value.format(fieldName=locStr)
    elif typeError == "datetime_future":
        # This error is raised when the value provided for a `FutureDatetime` field is not in the future
        t: str = ValidationErrorType.VALIDATION_ERROR_DATETIME_FUTURE.value
        m: str = ValidationErrorMessage.DATETIME_FUTURE_F.value.format(fieldName=locStr)
    elif typeError == "datetime_object_invalid":
        # This error is raised when something about the `datetime` object is not valid
        t: str = ValidationErrorType.VALIDATION_ERROR_DATETIME_OBJECT_INVALID.value
        m: str = ValidationErrorMessage.DATETIME_OBJECT_INVALID_F.value.format(fieldName=locStr)
    elif typeError == "datetime_parsing":
        # This error is raised when the value is a string that cannot be parsed for a `datetime` field
        t: str = ValidationErrorType.VALIDATION_ERROR_DATETIME_PARSING.value
        m: str = ValidationErrorMessage.DATETIME_PARSING_F.value.format(fieldName=locStr)
    elif typeError == "datetime_past":
        # This error is raised when the value provided for a `PastDatetime` field is not in the past
        t: str = ValidationErrorType.VALIDATION_ERROR_DATETIME_PAST.value
        m: str = ValidationErrorMessage.DATETIME_PAST_F.value.format(fieldName=locStr)
    elif typeError == "datetime_type":
        # This error is raised when the input value's type is not valid for a `datetime` field
        t: str = ValidationErrorType.VALIDATION_ERROR_DATETIME_TYPE.value
        m: str = ValidationErrorMessage.DATETIME_TYPE_F.value.format(fieldName=locStr)
    # ----------------------------------------------------------
    elif typeError == "decimal_max_digits":
        # This error is raised when the value provided for a `Decimal` has too many digits
        t: str = ValidationErrorType.VALIDATION_ERROR_DECIMAL_MAX_DIGITS.value
        m: str = ValidationErrorMessage.DECIMAL_MAX_DIGITS_F.value.format(fieldName=locStr)
        if (ctx is not None) and (isinstance(ctx, dict)):
            max_digits = ctx.get("max_digits")
            if (max_digits is not None) and (isinstance(max_digits, int)):
                m += f", maksimal {max_digits} digit"
    elif typeError == "decimal_max_places":
        # This error is raised when the value provided for a `Decimal` has too many digits after the decimal point
        t: str = ValidationErrorType.VALIDATION_ERROR_DECIMAL_MAX_PLACES.value
        m: str = ValidationErrorMessage.DECIMAL_MAX_PLACES_F.value.format(fieldName=locStr)
        if (ctx is not None) and (isinstance(ctx, dict)):
            decimal_places = ctx.get("decimal_places")
            if (decimal_places is not None) and (isinstance(decimal_places, int)):
                m += f", maksimal {decimal_places} digit"
    elif typeError == "decimal_parsing":
        # This error is raised when the value provided for a `Decimal` could not be parsed as a decimal number
        t: str = ValidationErrorType.VALIDATION_ERROR_DECIMAL_PARSING.value
        m: str = ValidationErrorMessage.DECIMAL_PARSING_F.value.format(fieldName=locStr)
    elif typeError == "decimal_type":
        # This error is raised when the value provided for a `Decimal` is of the wrong type
        t: str = ValidationErrorType.VALIDATION_ERROR_DECIMAL_TYPE.value
        m: str = ValidationErrorMessage.DECIMAL_TYPE_F.value.format(fieldName=locStr)
    elif typeError == "decimal_whole_digits":
        # This error is raised when the value provided for a `Decimal` has more digits before the decimal point than `max_digits` - `decimal_places` (as long as both are specified)
        t: str = ValidationErrorType.VALIDATION_ERROR_DECIMAL_WHOLE_DIGITS.value
        m: str = ValidationErrorMessage.DECIMAL_WHOLE_DIGITS_F.value.format(fieldName=locStr)
        if (ctx is not None) and (isinstance(ctx, dict)):
            whole_digits = ctx.get("whole_digits")
            if (whole_digits is not None) and (isinstance(whole_digits, int)):
                m += f", maksimal keseluruhan jumlah digit adalah {whole_digits} digit"
    # ----------------------------------------------------------
    elif typeError == "dict_type":
        # This error is raised when the input value's type is not `dict` for a `dict` field
        t: str = ValidationErrorType.VALIDATION_ERROR_DICT_TYPE.value
        m: str = ValidationErrorMessage.DICT_TYPE_F.value.format(fieldName=locStr)
    elif typeError == "enum":
        # This error is raised when the input value does not exist in an `enum` field members
        t: str = ValidationErrorType.VALIDATION_ERROR_ENUM.value
        m: str = ValidationErrorMessage.ENUM_MEMBER_F.value.format(fieldName=locStr)
        if (ctx is not None) and (isinstance(ctx, dict)):
            expected = ctx.get("expected")
            if (expected is not None) and (isinstance(expected, str)):
                expected = expected.replace("' or '", "' atau '")
                m += f", yaitu {expected}"
    elif typeError == "extra_forbidden":
        # This error is raised when the input value contains extra fields, but `model_config['extra'] == 'forbid'`
        t: str = ValidationErrorType.VALIDATION_ERROR_EXTRA_FORBIDDEN.value
        m: str = ValidationErrorMessage.EXTRA_FORBIDDEN_F.value.format(fieldName=locStr)
    # ----------------------------------------------------------
    elif typeError == "finite_number":
        # This error is raised when the value is infinite, or too large to be represented as a 64-bit floating point number during validation
        t: str = ValidationErrorType.VALIDATION_ERROR_FINITE_NUMBER.value
        m: str = ValidationErrorMessage.FINITE_NUMBER_F.value.format(fieldName=locStr)
    elif typeError == "float_parsing":
        # This error is raised when the value is a string that can't be parsed as a `float`
        t: str = ValidationErrorType.VALIDATION_ERROR_FLOAT_PARSING.value
        m: str = ValidationErrorMessage.FLOAT_PARSING_F.value.format(fieldName=locStr)
    elif typeError == "float_type":
        # This error is raised when the input value's type is not valid for a `float` field
        t: str = ValidationErrorType.VALIDATION_ERROR_FLOAT_TYPE.value
        m: str = ValidationErrorMessage.FLOAT_TYPE_F.value.format(fieldName=locStr)
    # ----------------------------------------------------------
    elif typeError == "get_attribute_error":
        # This error is raised when `model_config['from_attributes'] == True` and an error is raised while reading the attributes
        t: str = ValidationErrorType.VALIDATION_ERROR_GET_ATTRIBUTE_ERROR.value
        
        m: str = ValidationErrorMessage.GET_ATTRIBUTE_ERROR_F.value.format(fieldName=locStr)
    # ----------------------------------------------------------
    elif typeError == "greater_than":
        # This error is raised when the value is not greater than the field's `gt` constraint
        t: str = ValidationErrorType.VALIDATION_ERROR_GREATER_THAN.value
        gtValue = "tidak diketahui"
        if (ctx is not None) and (isinstance(ctx, dict)):
            gt = ctx.get("gt")
            if (gt is not None) and (isinstance(gt, int)):
                gtValue = gt
        m: str = ValidationErrorMessage.GREATER_THAN_F.value.format(fieldName=locStr, gt=gtValue)
    elif typeError == "greater_than_equal":
        # This error is raised when the value is not greater than or equal to the field's `ge` constraint
        t: str = ValidationErrorType.VALIDATION_ERROR_GREATER_THAN_EQUAL.value
        geValue = "tidak diketahui"
        if (ctx is not None) and (isinstance(ctx, dict)):
            ge = ctx.get("ge")
            if (ge is not None) and (isinstance(ge, int)):
                geValue = ge
        m: str = ValidationErrorMessage.GREATER_THAN_EQUAL_F.value.format(fieldName=locStr, ge=geValue)
    # ----------------------------------------------------------
    elif typeError == "int_from_float":
        # This error is raised when you provide a `float` value for an `int` field
        t: str = ValidationErrorType.VALIDATION_ERROR_INT_FROM_FLOAT.value
        m: str = ValidationErrorMessage.INT_FROM_FLOAT_F.value.format(fieldName=locStr)
    elif typeError == "int_parsing":
        # This error is raised when the value can't be parsed as `int`
        t: str = ValidationErrorType.VALIDATION_ERROR_INT_PARSING.value
        m: str = ValidationErrorMessage.INT_PARSING_F.value.format(fieldName=locStr)
    elif typeError == "int_parsing_size":
        # This error is raised when attempting to parse a python or JSON value from a string outside the maximum range that Python
        # `str` to `int` parsing permits
        t = ValidationErrorType.VALIDATION_ERROR_INT_PARSING_SIZE.value
        m = ValidationErrorMessage.INT_PARSING_SIZE_F.value.format(fieldName=locStr)
    elif typeError == "int_type":
        # This error is raised when the input value's type is not valid for an `int` field
        t = ValidationErrorType.VALIDATION_ERROR_INT_TYPE.value
        m = ValidationErrorMessage.INT_TYPE_F.value.format(fieldName=locStr)
    # ----------------------------------------------------------
    elif typeError == "invalid_key":
        # This error is raised when attempting to validate a `dict` that has a key that is not an instance of `str`
        t: str = ValidationErrorType.VALIDATION_ERROR_INVALID_KEY.value
        m: str = ValidationErrorMessage.INVALID_KEY.value
    # ----------------------------------------------------------
    elif typeError == "is_instance_of":
        # This error is raised when the input value is not an instance of the expected type
        t: str = ValidationErrorType.VALIDATION_ERROR_IS_INSTANCE_OF.value
        className = "tidak diketahui"
        if (ctx is not None) and (isinstance(ctx, dict)):
            className = ctx.get("class")
            if (className is not None) and (isinstance(className, str)):
                className = className
        m: str = ValidationErrorMessage.IS_INSTANCE_OF.value.format(fieldName=locStr, className=className)
    elif typeError == "is_subclass_of":
        # This error is raised when the input value is not a subclass of the expected type
        t: str = ValidationErrorType.VALIDATION_ERROR_IS_SUBCLASS_OF.value
        className = "tidak diketahui"
        if (ctx is not None) and (isinstance(ctx, dict)):
            className = ctx.get("class")
            if (className is not None) and (isinstance(className, str)):
                className = className
        m: str = ValidationErrorMessage.IS_SUBCLASS_OF.value.format(fieldName=locStr, className=className)
    # ----------------------------------------------------------
    elif typeError == "json_invalid":
        # This error is raised when the input value is not a valid JSON string
        t: str = ValidationErrorType.VALIDATION_ERROR_JSON_INVALID.value
        m: str = ValidationErrorMessage.JSON_INVALID.value
        m += " bagian " + locStr
    elif typeError == "json_type":
        # This error is raised when the input value is of a type that cannot be parsed as JSON
        t: str = ValidationErrorType.VALIDATION_ERROR_JSON_TYPE.value
        m: str = ValidationErrorMessage.JSON_TYPE_F.value.format(fieldName=locStr)
    # ----------------------------------------------------------
    elif typeError == "less_than":
        # This error is raised when the input value is not less than the field's `lt` constraint
        t: str = ValidationErrorType.VALIDATION_ERROR_LESS_THAN.value
        ltValue = "tidak diketahui"
        if (ctx is not None) and (isinstance(ctx, dict)):
            lt = ctx.get("lt")
            if (lt is not None) and (isinstance(lt, int)):
                ltValue = lt
        m: str = ValidationErrorMessage.LESS_THAN_F.value.format(fieldName=locStr, lt=ltValue)
    elif typeError == "less_than_equal":
        # This error is raised when the input value is not less than or equal to the field's `le` constraint
        t: str = ValidationErrorType.VALIDATION_ERROR_LESS_THAN_EQUAL.value
        leValue = "tidak diketahui"
        if (ctx is not None) and (isinstance(ctx, dict)):
            le = ctx.get("le")
            if (le is not None) and (isinstance(le, int)):
                leValue = le
        m: str = ValidationErrorMessage.LESS_THAN_EQUAL_F.value.format(fieldName=locStr, le=leValue)
    # ----------------------------------------------------------
    elif typeError == "list_type":
        # This error is raised when the input value's type is not valid for a `list` field
        t: str = ValidationErrorType.VALIDATION_ERROR_LIST_TYPE.value
        m: str = ValidationErrorMessage.LIST_TYPE_F.value.format(fieldName=locStr)
    elif typeError == "literal_error":
        # This error is raised when the input value is not one of the expected literal values
        t: str = ValidationErrorType.VALIDATION_ERROR_LITERAL_ERROR.value
        m: str = ValidationErrorMessage.LITERAL_ERROR_F.value.format(fieldName=locStr)
        if (ctx is not None) and (isinstance(ctx, dict)):
            expected = ctx.get("expected")
            if (expected is not None) and (isinstance(expected, str)):
                expected = expected.replace("' or '", "' atau '")
                m += f", nilai yang diperbolehkan yaitu {expected}"
    elif typeError == "missing":
        # This error is raised when there are required fields missing from the input value
        t: str = ValidationErrorType.VALIDATION_ERROR_MISSING.value
        m: str = ValidationErrorMessage.MISSING_F.value.format(fieldName=locStr)
    elif typeError == "model_attributes_type":
        # This error is raised when the input value is not a valid dictionary, model instance, or instance that fields can be extracted from
        t = ValidationErrorType.VALIDATION_ERROR_MODEL_ATTRIBUTES_TYPE.value
        m = ValidationErrorMessage.MODEL_ATTRIBUTES_TYPE_F.value.format(fieldName=locStr)
    elif typeError == "model_type":
        # This error is raised when the input to a model is not an instance of the model or dict
        t: str = ValidationErrorType.VALIDATION_ERROR_MODEL_TYPE.value
        m: str = ValidationErrorMessage.MODEL_TYPE_F.value
        if (ctx is not None) and (isinstance(ctx, dict)):
            class_name = ctx.get("class_name")
            if (class_name is not None) and (isinstance(class_name, str)):
                m += " atau class dari " + class_name
    elif typeError == "multiple_of":
        # This error is raised when the input is not a multiple of a field's `multiple_of` constraint
        t: str = ValidationErrorType.VALIDATION_ERROR_MULTIPLE_OF.value
        multiple_ofValue = "tidak diketahui"
        if (ctx is not None) and (isinstance(ctx, dict)):
            multiple_of = ctx.get("multiple_of")
            if (multiple_of is not None) and (isinstance(multiple_of, int)):
                multiple_ofValue = multiple_of
        m: str = ValidationErrorMessage.MULTIPLE_OF_F.value.format(fieldName=locStr, multiple_of=multiple_ofValue)
    elif typeError == "no_such_attribute":
        # is error is raised when `validate_assignment=True` in the config, and you attempt to assign a value to an attribute
        # that is not an existing field
        t: str = ValidationErrorType.VALIDATION_ERROR_NO_SUCH_ATTRIBUTE.value
        m: str = ValidationErrorMessage.NO_SUCH_ATTRIBUTE_F.value.format(fieldName=locStr)
    elif typeError == "none_required":
        # This error is raised when the input value is not `None` for a field that requires `None`
        t: str = ValidationErrorType.VALIDATION_ERROR_NONE_REQUIRED.value
        m: str = ValidationErrorMessage.NONE_REQUIRED_F.value.format(fieldName=locStr)
    elif typeError == "set_type":
        # This error is raised when the value type is not valid for a `set` field
        t: str = ValidationErrorType.VALIDATION_ERROR_SET_TYPE.value
        m: str = ValidationErrorMessage.SET_TYPE_F.value.format(fieldName=locStr)
    # ----------------------------------------------------------
    elif typeError == "string_pattern_mismatch":
        # This error is raised when the input value doesn't match the field's `pattern` constraint
        t: str = ValidationErrorType.VALIDATION_ERROR_STRING_PATTERN_MISMATCH.value
        m: str = ValidationErrorMessage.STRING_PATTERN_MISMATCH_F.value.format(fieldName=locStr)
    elif typeError == "string_sub_type":
        # This error is raised when the value is an instance of a strict subtype of `str` when the field is strict
        t: str = ValidationErrorType.VALIDATION_ERROR_STRING_SUB_TYPE.value
        m: str = ValidationErrorMessage.STRING_SUB_TYPE_F.value.format(fieldName=locStr)
    elif typeError == "string_too_long":
        # This error is raised when the input value is a string whose length is greater than the field's `max_length` constraint
        t: str = ValidationErrorType.VALIDATION_ERROR_STRING_TOO_LONG.value
        max_length_value = "tidak diketahui"
        if (ctx is not None) and (isinstance(ctx, dict)):
            max_length = ctx.get("max_length")
            if (max_length is not None) and (isinstance(max_length, int)):
                max_length_value = max_length
        m: str = ValidationErrorMessage.STRING_TOO_LONG_F.value.format(fieldName=locStr, max_length=max_length_value)
    elif typeError == "string_too_short":
        # This error is raised when the input value is a string whose length is less than the field's `min_length` constraint
        t: str = ValidationErrorType.VALIDATION_ERROR_STRING_TOO_SHORT.value
        min_length_value = "tidak diketahui"
        if (ctx is not None) and (isinstance(ctx, dict)):
            min_length = ctx.get("min_length")
            if (min_length is not None) and (isinstance(min_length, int)):
                min_length_value = min_length
        m: str = ValidationErrorMessage.STRING_TOO_SHORT_F.value.format(fieldName=locStr, min_length=min_length_value)
    elif typeError == "string_type":
        # This error is raised when the input value's type is not valid for a `str` field
        t: str = ValidationErrorType.VALIDATION_ERROR_STRING_TYPE.value
        m: str = ValidationErrorMessage.STRING_TYPE_F.value.format(fieldName=locStr)
    elif typeError == "string_unicode":
        # This error is raised when the value cannot be parsed as a Unicode string
        t: str = ValidationErrorType.VALIDATION_ERROR_STRING_UNICODE.value
        m = ValidationErrorMessage.STRING_UNICODE_F.value.format(fieldName=locStr)
    # ----------------------------------------------------------
    elif typeError == "time_delta_parsing":
        # This error is raised when the input value is a string that cannot be parsed for a `timedelta` field
        t: str = ValidationErrorType.VALIDATION_ERROR_TIME_DELTA_PARSING.value
        m: str = ValidationErrorMessage.TIME_DELTA_PARSING_F.value.format(fieldName=locStr)
    elif typeError == "time_delta_type":
        # This error is raised when the input value's type is not valid for a `timedelta` field
        t: str = ValidationErrorType.VALIDATION_ERROR_TIME_DELTA_TYPE.value
        m: str = ValidationErrorMessage.TIME_DELTA_TYPE_F.value.format(fieldName=locStr)
    # ----------------------------------------------------------
    elif typeError == "time_parsing":
        # This error is raised when the input value is a string that cannot be parsed for a `time` field
        t: str = ValidationErrorType.VALIDATION_ERROR_TIME_PARSING.value
        m = ValidationErrorMessage.TIME_PARSING_F.value.format(fieldName=locStr)
    elif typeError == "time_type":
        # This error is raised when the value type is not valid for a `time` field
        t: str = ValidationErrorType.VALIDATION_ERROR_TIME_TYPE.value
        m: str = ValidationErrorMessage.TIME_TYPE_F.value.format(fieldName=locStr)
    # ----------------------------------------------------------
    elif typeError == "timezone_aware":
        # This error is raised when the `datetime` value provided for a timezone-aware `datetime` field
        # doesn't have timezone information
        t: str = ValidationErrorType.VALIDATION_ERROR_TIMEZONE_AWARE.value
        m: str = ValidationErrorMessage.TIMEZONE_AWARE_F.value.format(fieldName=locStr)
    elif typeError == "timezone_naive":
        # This error is raised when the `datetime` value provided for a timezone-naive `datetime` field
        # has timezone info
        t = ValidationErrorType.VALIDATION_ERROR_TIMEZONE_NAIVE.value
        m = ValidationErrorMessage.TIMEZONE_NAIVE_F.value.format(fieldName=locStr)
    # ----------------------------------------------------------
    elif typeError == "too_long":
        # This error is raised when the input value's length is greater than the field's `max_length` constraint
        t = ValidationErrorType.VALIDATION_ERROR_TOO_LONG.value
        max_length_value = "tidak diketahui"
        if (ctx is not None) and (isinstance(ctx, dict)):
            max_length = ctx.get("max_length")
            if (max_length is not None) and (isinstance(max_length, int)):
                max_length_value = max_length
        m = ValidationErrorMessage.TOO_LONG_F.value.format(fieldName=locStr, max_length=max_length_value)
    elif typeError == "too_short":
        # This error is raised when the value length is less than the field's `min_length` constraint
        t: str = ValidationErrorType.VALIDATION_ERROR_TOO_SHORT.value
        min_length_value = "tidak diketahui"
        if (ctx is not None) and (isinstance(ctx, dict)):
            min_length = ctx.get("min_length")
            if (min_length is not None) and (isinstance(min_length, int)):
                min_length_value = min_length
        m: str = ValidationErrorMessage.TOO_SHORT_F.value.format(fieldName=locStr, min_length=min_length_value)
    # ----------------------------------------------------------
    elif typeError == "tuple_type":
        # This error is raised when the value length is less than the field's `min_length` constraint
        t: str = ValidationErrorType.VALIDATION_ERROR_TUPLE_TYPE.value
        m: str = ValidationErrorMessage.TUPLE_TYPE_F.value.format(fieldName=locStr)
    # ----------------------------------------------------------
    elif typeError == "union_tag_invalid":
        # This error is raised when the input's discriminator is not one of the expected values
        t: str = ValidationErrorType.VALIDATION_ERROR_UNION_TAG_INVALID.value
        discriminator_value = "tidak diketahui"
        expected_tags_value: str| None = None
        if (ctx is not None) and (isinstance(ctx, dict)):
            discriminator = ctx.get("discriminator")
            expected_tags = ctx.get("expected_tags")
            if (discriminator is not None) and (isinstance(discriminator, str)):
                discriminator_value = discriminator
            if (expected_tags is not None) and (isinstance(expected_tags, str)):
                expected_tags_value = expected_tags
        m: str = ValidationErrorMessage.UNION_TAG_INVALID_F.value.format(discriminator=discriminator_value, fieldName=locStr)
        if expected_tags_value is not None:
            m += ", nilai yang diharapkan adalah " + expected_tags_value
    elif typeError == "union_tag_not_found":
        # This error is raised when it is not possible to extract a discriminator value from the input
        t: str = ValidationErrorType.VALIDATION_ERROR_UNION_TAG_NOT_FOUND.value
        discriminator_value = "tidak diketahui"
        expected_tags_value: str| None = None
        if (ctx is not None) and (isinstance(ctx, dict)):
            discriminator = ctx.get("discriminator")
            if (discriminator is not None) and (isinstance(discriminator, str)):
                discriminator_value = discriminator
        m: str = ValidationErrorMessage.UNION_TAG_NOT_FOUND_F.value.format(discriminator=discriminator_value, fieldName=locStr)
    # ----------------------------------------------------------
    elif typeError == "url_parsing":
        # This error is raised when the input value cannot be parsed as a URL
        t: str = ValidationErrorType.VALIDATION_ERROR_URL_PARSING.value
        m: str = ValidationErrorMessage.URL_PARSING_F.value.format(fieldName=locStr)
    elif typeError == "url_scheme":
        # This error is raised when the URL scheme is not valid for the URL type of the field
        t = ValidationErrorType.VALIDATION_ERROR_URL_SCHEME.value
        m = ValidationErrorMessage.URL_SCHEME_F.value.format(fieldName=locStr)
        if (ctx is not None) and (isinstance(ctx, dict)):
            expected_schemes = ctx.get("expected_schemes")
            if (expected_schemes is not None) and (isinstance(expected_schemes, str)):
                expected_schemes = expected_schemes.replace("' or '", "' atau '")
                m += f", sekema yang diperbolehkan yaitu {expected_schemes}"
    elif typeError == "url_syntax_violation":
        # This error is raised when the URL syntax is not valid
        t: str = ValidationErrorType.VALIDATION_ERROR_URL_SYNTAX_VIOLATION.value
        m: str = ValidationErrorMessage.URL_SYNTAX_VIOLATION_F.value.format(fieldName=locStr)
    elif typeError == "url_too_long":
        # This error is raised when the URL length is greater than 2083
        t: str = ValidationErrorType.VALIDATION_ERROR_URL_TOO_LONG.value
        m: str = ValidationErrorMessage.URL_TOO_LONG_F.value.format(fieldName=locStr)
        if (ctx is not None) and (isinstance(ctx, dict)):
            max_length = ctx.get("max_length")
            if (max_length is not None) and (isinstance(max_length, int)):
                m += f", maksimal {max_length} karakter"
    elif typeError == "url_type":
        # This error is raised when the input value's type is not valid for a URL field
        t: str = ValidationErrorType.VALIDATION_ERROR_URL_TYPE.value
        m: str = ValidationErrorMessage.URL_TYPE_F.value.format(fieldName=locStr)
    # ----------------------------------------------------------
    elif typeError == "uuid_parsing":
        # This error is raised when the input value's type is not valid for a UUID field
        t = ValidationErrorType.VALIDATION_ERROR_UUID_PARSING.value
        m = ValidationErrorMessage.UUID_PARSING_F.value.format(fieldName=locStr)
    elif typeError == "uuid_type":
        # This error is raised when the input value's type is not valid instance for a UUID field (str, bytes or UUID)
        t = ValidationErrorType.VALIDATION_ERROR_UUID_TYPE.value
        m = ValidationErrorMessage.UUID_TYPE_F.value.format(fieldName=locStr)
    elif typeError == "uuid_version":
        # This error is raised when the input value's type is not match UUID version
        t: str = ValidationErrorType.VALIDATION_ERROR_UUID_VERSION.value
        expected_version_value = "tidak diketahui"
        if (ctx is not None) and (isinstance(ctx, dict)):
            expected_version = ctx.get("expected_version")
            if (expected_version is not None) and (isinstance(expected_version, int)):
                expected_version_value = expected_version
        m: str = ValidationErrorMessage.UUID_VERSION_F.value.format(fieldName=locStr, expected_version=expected_version_value)
    # ----------------------------------------------------------
    elif typeError == "value_error":
        # This error is raised when a `ValueError` is raised during validation
        if msg is not None:
            if msg == "value is not a valid phone number":
                # pydantic extra type PhoneNumber
                t: str = ValidationErrorType.VALIDATION_ERROR_INVALID_PHONE_NUMBER.value
                m: str = ValidationErrorMessage.INVALID_PHONE_NUMBER_F.value.format(fieldName=locStr)
            elif msg.startswith("value is not a valid email address:"):
                # pydantic EmailStr
                t: str = ValidationErrorType.VALIDATION_ERROR_INVALID_EMAIL_ADDRESS.value
                m: str = ValidationErrorMessage.INVALID_EMAIL_ADDRESS_F.value.format(fieldName=locStr)
            else:
                t: str = ValidationErrorType.VALIDATION_ERROR_VALUE_ERROR.value
                m: str = ValidationErrorMessage.VALUE_ERROR_F.value.format(fieldName=locStr)
        else:
            t: str = ValidationErrorType.VALIDATION_ERROR_VALUE_ERROR.value
            m: str = ValidationErrorMessage.VALUE_ERROR_F.value.format(fieldName=locStr)
    # ----------------------------------------------------------
    elif typeError == ObjectId.invalid_object_id:
        t: str = ValidationErrorType.VALIDATION_ERROR_INVALID_OBJECT_ID.value
        m: str = ValidationErrorMessage.INVALID_OBJECT_ID_F.value.format(fieldName=locStr)
    # ----------------------------------------------------------
    elif typeError == "ip_any_address":
        # IPvAnyAddress
        t: str = ValidationErrorType.VALIDATION_ERROR_INVALID_IP_ANY_ADDRESS.value
        m: str = ValidationErrorMessage.INVALID_IP_ANY_ADDRESS_F.value.format(fieldName=locStr)
    elif typeError == "ip_v4_address":
        # IPv4Address
        t = ValidationErrorType.VALIDATION_ERROR_INVALID_IP_V4_ADDRESS.value
        m = ValidationErrorMessage.INVALID_IP_V4_ADDRESS_F.value.format(fieldName=locStr)
    elif typeError == "ip_v6_address":
        # IPv6Address
        t: str = ValidationErrorType.VALIDATION_ERROR_INVALID_IP_V6_ADDRESS.value
        m: str = ValidationErrorMessage.INVALID_IP_V6_ADDRESS_F.value.format(fieldName=locStr)
    else:
        t: str = "VALIDATION_ERROR_" + typeError.upper()
        if (msg is not None):
            m: str = msg
        else:
            m: str = ValidationErrorMessage.UNKNOWN_ERROR.value
    # ----------------------------------------------------------
    # ----------------------------------------------------------
    if fieldStr is None:
        fieldStr = locStr
    if respCtx is not None:
        return {
            "type": t,
            "message": m,
            "loc": loc,
            "field": fieldStr,
            "msg": msg,
            "ctx": respCtx
        }
    else:
        return {
            "type": t,
            "message": m,
            "loc": loc,
            "field": fieldStr,
            "msg": msg
        }
