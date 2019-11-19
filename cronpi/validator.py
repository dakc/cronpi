import re
from datetime import datetime

CMD_INDEX = 5
MIN_CMD_LENGTH = 2
JOB_TIME_LENGTH = 5
ERR_NO_ARGS_FOUND = "No arguments are passed."
ERR_ARGS_NOT_VALID = "Arguments are not valid."
ERR_COMMAND_FORMAT_NOT_VALID = "command format is not correct."
ERR_IS_OVERWRITE_FORMAT_NOT_VALID = "'overwrite' should be bool either True or False."
ERR_HOUR_FORMAT_NOT_VALID = "hour should be integer between 0 and 23 if no suffix is added else should be between 0 and 12."
ERR_MIN_FORMAT_NOT_VALID = "minute should be integer between 0 and 59."
ERR_DAY_FORMAT_NOT_VALID = "day should be integer between 1 and 31."
ERR_MONTH_FORMAT_NOT_VALID = "month should be either string having single month or list of multiple months."
ERR_WEEKDAY_FORMAT_NOT_VALID = "weekday should be either string having single day or list of multiple days."
ERR_CMD_LENGTH_INVALID = "command string should be more then single letter."
ERR_JOB_TIME_FORMAT_NOT_VALID = "job_time parameter is not a valid format. It should be in 'HH:mm' format."
ERR_JOB_DATE_FORMAT_NOT_VALID = "date is not a valid format. It should be in 'YYYY-MM-DD HH:mm' format.(AM or PM as suffix is optional)"
ERR_JOB_DATE_NOT_VALID_SPAN = "date is not valid. It should be future time."

def validate_command(command, overwrite):
    if not isinstance(command, str):
        raise ValueError(ERR_COMMAND_FORMAT_NOT_VALID)
    if not len(command.strip()) >= MIN_CMD_LENGTH:
        raise ValueError(ERR_CMD_LENGTH_INVALID)
    if not isinstance(overwrite, bool):
        raise ValueError(ERR_IS_OVERWRITE_FORMAT_NOT_VALID)

    # replace the multiple spaces with single
    return ' '.join(command.split()), overwrite

def get_time_once(job_time):
    am_pm = job_time[-2:].lower()
    if am_pm == "am" or am_pm == "pm":
        job_time = job_time[:-2]

    m = re.match(
        "(\d{4})-(\d{1,2})-(\d{1,2})\s+(\d{1,2}):(\d{1,2})", job_time)
    if m is None or not len(m.groups()) == 5:
        raise ValueError(ERR_JOB_DATE_FORMAT_NOT_VALID)

    # check if date is past
    (hr, mn) = get_time("{}:{}{}".format(m.group(4), m.group(5),am_pm))
    job_time_dt = datetime.strptime(job_time, "%Y-%m-%d %H:%M")
    job_time_dt = job_time_dt.replace(hour=hr, minute=mn)
    if job_time_dt < datetime.now():
        raise ValueError(ERR_JOB_DATE_NOT_VALID_SPAN)
    
    return m.group(2), m.group(3), hr, mn

def get_time(job_time):
    am_pm = job_time[-2:].lower()
    if am_pm == "am" or am_pm == "pm":
        job_time = job_time[:-2]

    m = re.match("(\d{1,2}):(\d{1,2})", job_time)
    if m is None:
        raise ValueError(ERR_JOB_TIME_FORMAT_NOT_VALID)

    matches = m.groups()
    if not len(matches) == 2:
        raise ValueError(ERR_JOB_TIME_FORMAT_NOT_VALID)
    hour = minute = ""
    try:
        hour = int(matches[0])
        if am_pm == "pm":
            hour += 12
    except:
        pass
    if not isinstance(hour, int):
        raise ValueError(ERR_HOUR_FORMAT_NOT_VALID)
    if hour < 0 or hour > 23 :
        raise ValueError(ERR_HOUR_FORMAT_NOT_VALID)

    try:
        minute = int(matches[1])
    except:
        pass
    if not isinstance(minute, int):
        raise ValueError(ERR_MIN_FORMAT_NOT_VALID)
    if minute < 0 or minute > 59 :
        raise ValueError(ERR_MIN_FORMAT_NOT_VALID)

    return (hour,minute,)

def get_week_days(target_week):
    def get_week_day_id(day):
        if not isinstance(day, str):
            return None

        if day.lower() == "sun" or day.lower() == "sunday":
            return "0"
        if day.lower() == "mon" or day.lower() == "monday":
            return "1"
        if day.lower() == "tue" or day.lower() == "tuesday":
            return "2"
        if day.lower() == "wed" or day.lower() == "wednesday":
            return "3"
        if day.lower() == "thu" or day.lower() == "thursday":
            return "4"
        if day.lower() == "fri" or day.lower() == "friday":
            return "5"
        if day.lower() == "sat" or day.lower() == "saturday":
            return "6"
        return None

    day_id = ""
    if isinstance(target_week, str):
        day_id = get_week_day_id(target_week)
        if day_id is None:
            raise ValueError(ERR_WEEKDAY_FORMAT_NOT_VALID)

    elif isinstance(target_week, list):
        for d in target_week:
            _day_id = get_week_day_id(d)
            if _day_id is None:
                raise ValueError(ERR_WEEKDAY_FORMAT_NOT_VALID)
            day_id += _day_id + ","

    return day_id.rstrip(",")



def get_month_days(target_day):
    def validate(day):
        if not isinstance(day, int):
            raise ValueError(ERR_DAY_FORMAT_NOT_VALID)
        if day < 1 or day > 31:
            raise ValueError(ERR_DAY_FORMAT_NOT_VALID)
        return True

    if not isinstance(target_day, int) and not isinstance(target_day, list):
        raise ValueError(ERR_DAY_FORMAT_NOT_VALID)

    days = ""
    if isinstance(target_day, int):
        validate(target_day)
        days = target_day
    else:
        for d in target_day:
            validate(d)
            days += str(d) + ","
        days = days.rstrip(",")
    
    return days

def get_months(target_month):
    def get_month_id(month):
        if month.lower() == "jan" or month.lower() == "january":
            return "1"
        if month.lower() == "feb" or month.lower() == "february":
            return "2"
        if month.lower() == "mar" or month.lower() == "march":
            return "3"
        if month.lower() == "apr" or month.lower() == "april":
            return "4"
        if month.lower() == "may":
            return "5"
        if month.lower() == "jun" or month.lower() == "june":
            return "6"
        if month.lower() == "jul" or month.lower() == "july":
            return "7"
        if month.lower() == "aug" or month.lower() == "august":
            return "8"
        if month.lower() == "sep" or month.lower() == "september":
            return "9"
        if month.lower() == "oct" or month.lower() == "october":
            return "10"
        if month.lower() == "nov" or month.lower() == "november":
            return "11"
        if month.lower() == "dec" or month.lower() == "december":
            return "12"
        return None

    month_id = ""
    if isinstance(target_month, str):
        month_id = get_month_id(target_month)
        if month_id is None:
            raise ValueError(ERR_MONTH_FORMAT_NOT_VALID)

    elif isinstance(target_month, list):
        for m in target_month:
            _month_id = get_month_id(m)
            if _month_id is None:
                raise ValueError(ERR_MONTH_FORMAT_NOT_VALID)
            month_id += _month_id + ","

    return month_id.rstrip(",")

def get_time_interval(minute):
    if not isinstance(minute, int):
        raise ValueError(ERR_MIN_FORMAT_NOT_VALID)
    if minute < 1 or minute > 59:
        raise ValueError(ERR_MIN_FORMAT_NOT_VALID)
    
    return str(minute)


def validate_crontab_content(content):
    if not content:
        raise ValueError(ERR_NO_ARGS_FOUND)
    split_command = content.split()
    if len(split_command) <= CMD_INDEX:
        raise ValueError(ERR_COMMAND_FORMAT_NOT_VALID)
    for i in range(CMD_INDEX):
        if split_command[i] == "*":
            continue
        m = re.match("([\d{1,2}|*])([-|/|,])?(\d{1,2})?", split_command[i])
        if (m is None or
            split_command[i].strip() == "*-" or
            split_command[i].strip() == "-*" or
            split_command[i].strip() == "*-*" or
            split_command[i].strip() == "*," or
            split_command[i].strip() == ",*" or
            split_command[i].strip() == "*,*" or
            split_command[i].strip() == "*/" or
            split_command[i].strip() == "/*" or
                split_command[i].strip() == "*/*"):
            raise ValueError(ERR_COMMAND_FORMAT_NOT_VALID)
    if not split_command[CMD_INDEX].strip():
        raise ValueError(ERR_COMMAND_FORMAT_NOT_VALID)