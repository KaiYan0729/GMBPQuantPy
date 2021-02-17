import pandas as pd
from datetime import datetime, timedelta
import pytz


def datetime_to_dateid(date):
    """
    >>> import gmbp_quant.common.utils.datetime_utils as dtu
    >>> dtu.datetime_to_dateid(datetime(2019, 9, 25))
    20190925
    >>> adt_utc = datetime(2020, 8, 7, 2, 0, 0, tzinfo=pytz.UTC)
    >>> adt_ny = adt_utc.astimezone(pytz.timezone('America/New_York'))
    >>> dtu.datetime_to_dateid(adt_utc)
    20200807
    >>> dtu.datetime_to_dateid(adt_ny)
    20200806
    """
    return int(date.strftime('%Y%m%d %Z')[:8])
#


def dateid_to_datetime(dateid, timezone=None):
    """
    >>> import gmbp_quant.common.utils.datetime_utils as dtu
    >>> dtu.dateid_to_datetime(dateid=20190925)
    datetime.datetime(2019, 9, 25, 0, 0)
    """
    dt = datetime.strptime(str(dateid), '%Y%m%d')
    if timezone is not None:
        dt = dt.replace(tzinfo=pytz.timezone(timezone))
    #

    return dt
#


def dateid_to_datestr(dateid, sep='-'):
    """
    >>> import gmbp_quant.common.utils.datetime_utils as dtu
    >>> dtu.dateid_to_datestr(dateid=20190925)
    '2019-09-25'
    >>> dtu.dateid_to_datestr(dateid=20191013, sep='/')
    '2019/10/13'
    """
    date = str(dateid)
    return f'{date[:4]}{sep}{date[4:6]}{sep}{date[6:]}'
#


def today(timezone=None):
    today = datetime.now() if timezone is None else datetime.now(pytz.timezone(timezone))
    return datetime_to_dateid(date=today)
#


def is_weekday(date):
    """
    >>> import gmbp_quant.common.utils.datetime_utils as dtu
    >>> dtu.is_weekday(20200511)
    True
    """
    if isinstance(date, int):
        date = dateid_to_datetime(dateid=date)
    elif not isinstance(date, datetime):
        raise Exception(f'type(date)={type(date)} is not supported [int|datetime] !')
    #
    return date.weekday() not in [5, 6]
#


def get_biz_dateids(start_dateid, end_dateid):
    """
    >>> import gmbp_quant.common.utils.datetime_utils as dtu
    >>> dtu.get_biz_dateids(start_dateid=20200910, end_dateid=20200917)
    [20200910, 20200911, 20200914, 20200915, 20200916, 20200917]
    """
    bdates = pd.bdate_range(dateid_to_datestr(dateid=start_dateid, sep='-'),
                            dateid_to_datestr(dateid=end_dateid, sep='-')).strftime('%Y%m%d')
    return [int(date) for date in bdates]
#


def next_biz_dateid(dateid):
    one_day = timedelta(days=1)
    next_day = dateid_to_datetime(dateid) + one_day
    while not is_weekday(date=next_day):
        next_day += one_day
    #
    return datetime_to_dateid(next_day)
#


def parse_datetime(dt, format=None, timezone=None, ret_as_timestamp=False):
    if isinstance(dt, int):
        dt = str(dt)
    #
    if (isinstance(dt, datetime) and not ret_as_timestamp) or \
            (isinstance(dt, pd.Timestamp) and ret_as_timestamp):
        return dt
    #

    try:
        dt = pd.Timestamp(dt)
        if timezone is not None:
            dt = dt.tz_localize(timezone)
        #
    except Exception:
        pass
    #

    if isinstance(dt, pd.Timestamp):
        return (dt if ret_as_timestamp else dt.to_pydatetime())
    #
    if isinstance(dt, str):
        dt = pd.to_datetime(dt, format=format)
        if timezone is not None:
            dt = dt.tz_localize(timezone)
        #
        return (dt if ret_as_timestamp else dt.to_pydatetime())
    #
    raise Exception(f'type(dt)={type(dt)} is not supported [dateid|str|datetime|pd.Timestamp|np.datetime64] !')
#
