from datetime import datetime, timedelta, timezone
import calendar

import pytz
from config.config import settings
from models.shared.modelDataType import ObjectId


class SampleModel:

    objectId_str_0 = "000000000000000000000000"
    objectId_str_1 = "000000000000000000000001"
    objectId_str_2 = "000000000000000000000002"
    objectId_str_3 = "000000000000000000000003"
    objectId_str_4 = "000000000000000000000004"
    objectId_str_5 = "000000000000000000000005"
    objectId_str_6 = "000000000000000000000006"
    objectId_str_7 = "000000000000000000000007"
    objectId_str_8 = "000000000000000000000008"
    objectId_str_9 = "000000000000000000000009"

    objectId_str_A = "00000000000000000000000A"
    objectId_str_B = "00000000000000000000000B"
    objectId_str_C = "00000000000000000000000C"
    objectId_str_D = "00000000000000000000000D"
    objectId_str_E = "00000000000000000000000E"
    objectId_str_F = "00000000000000000000000F"
    
    objectId_str_AA = "AAAAAAAAAAAAAAAAAAAAAAAA"
    objectId_str_BB = "BBBBBBBBBBBBBBBBBBBBBBBB"
    objectId_str_CC = "CCCCCCCCCCCCCCCCCCCCCCCC"
    objectId_str_DD = "DDDDDDDDDDDDDDDDDDDDDDDD"
    objectId_str_EE = "EEEEEEEEEEEEEEEEEEEEEEEE"
    objectId_str_FF = "FFFFFFFFFFFFFFFFFFFFFFFF"
    # -----------------------------------------------
    objectId_0 = ObjectId(objectId_str_0)
    objectId_1 = ObjectId(objectId_str_1)
    objectId_2 = ObjectId(objectId_str_2)
    objectId_3 = ObjectId(objectId_str_3)
    objectId_4 = ObjectId(objectId_str_4)
    objectId_5 = ObjectId(objectId_str_5)
    objectId_6 = ObjectId(objectId_str_6)
    objectId_7 = ObjectId(objectId_str_7)
    objectId_8 = ObjectId(objectId_str_8)
    objectId_9 = ObjectId(objectId_str_9)

    objectId_A = ObjectId(objectId_str_A)
    objectId_B = ObjectId(objectId_str_B)
    objectId_C = ObjectId(objectId_str_C)
    objectId_D = ObjectId(objectId_str_D)
    objectId_E = ObjectId(objectId_str_E)
    objectId_F = ObjectId(objectId_str_F)
    
    objectId_AA = ObjectId(objectId_str_AA)
    objectId_BB = ObjectId(objectId_str_BB)
    objectId_CC = ObjectId(objectId_str_CC)
    objectId_DD = ObjectId(objectId_str_DD)
    objectId_EE = ObjectId(objectId_str_EE)
    objectId_FF = ObjectId(objectId_str_FF)

    datetime_now_local = datetime.now().replace(microsecond=0)
    datetime_now_local_second0 = datetime_now_local.replace(second=0)
    datetime_now_local_minute0 = datetime_now_local_second0.replace(minute=0)
    datetime_now_local_hour0 = datetime_now_local_minute0.replace(hour=0)

    datetime_now_utc = datetime.now(timezone.utc).replace(microsecond=0)
    datetime_now_utc_second0 = datetime_now_utc.replace(second=0)
    datetime_now_utc_minute0 = datetime_now_utc_second0.replace(minute=0)
    datetime_now_utc_hour0 = datetime_now_utc_minute0.replace(hour=0)

    datetime_now_utc_2 = datetime_now_utc + timedelta(days=2)
    datetime_now_utc_2_second0 = datetime_now_utc_second0 + timedelta(days=2)
    datetime_now_utc_2_minute0 = datetime_now_utc_minute0 + timedelta(days=2)
    datetime_now_utc_2_hour0 = datetime_now_utc_hour0 + timedelta(days=2)

    date_now_local = datetime_now_local.date()
    date_now_local_day_1 = date_now_local.replace(day=1)
    date_now_local_2 = date_now_local + timedelta(days=2)
    date_now_local_5 = date_now_local + timedelta(days=5)
    date_now_local_yesterday = date_now_local - timedelta(days=1)

    date_now_utc = datetime_now_utc.date()
    date_now_utc_day_1 = date_now_utc.replace(day=1)
    date_now_utc_2 = date_now_utc + timedelta(days=2)
    date_now_utc_5 = date_now_utc + timedelta(days=5)

    time_now_utc = datetime_now_utc.time()
    time_now_utc_2 = (datetime_now_utc + timedelta(hours=2)).time()
    time_now_utc_5 = (datetime_now_utc + timedelta(hours=5)).time()

    time_now_utc_second0 = datetime_now_utc.replace(second=0).time()
    time_now_utc_second0_2 = (datetime_now_utc + timedelta(hours=2)).replace(second=0).time()
    time_now_utc_second0_5 = (datetime_now_utc + timedelta(hours=5)).replace(second=0).time()

    currentUtcYear = date_now_utc.year
    currentUtcMonth = date_now_utc.month
    currentUtcDay = date_now_utc.day

    currentLocalYear = date_now_local.year
    currentLocalMonth = date_now_local.month
    currentLocalDay = date_now_local.day

    currentUtcWeekday, currentUtcMonthRangeLastDay = calendar.monthrange(currentUtcYear, currentUtcMonth)
    currentLocalWeekday, currentLocalMonthRangeLastDay = calendar.monthrange(currentLocalYear, currentLocalMonth)

    date_utc_last = datetime_now_utc.date().replace(day=currentUtcMonthRangeLastDay)
    datetime_utc_last_max = datetime.combine(date_utc_last, datetime.max.time())
    datetime_utc_last_min = datetime.combine(date_utc_last, datetime.min.time())

    date_local_last = datetime_now_local.date().replace(day=currentLocalMonthRangeLastDay)
    datetime_local_last_max = datetime.combine(date_local_last, datetime.max.time())
    datetime_local_last_min = datetime.combine(date_local_last, datetime.min.time())

    zone = pytz.timezone(settings.config.timezone)
    datetime_now_timezone = zone.localize(datetime_now_utc.replace(tzinfo=None))
    datetime_timezone_last_max = zone.localize(datetime_utc_last_max)
    datetime_timezone_last_min = zone.localize(datetime_utc_last_min)