import re

CMD_INDEX = 5
MIN_CMD_LENGTH = 2
ERR_NO_ARGS_FOUND = "No arguments are passed."
ERR_ARGS_NOT_VALID = "Arguments are not valid."
ERR_COMMAND_FORMAT_NOT_VALID = "command format is not correct."
ERR_HOUR_FORMAT_NOT_VALID = "hour should be integer between 0 and 23."
ERR_MIN_FORMAT_NOT_VALID = "minute should be integer between 0 and 59."
ERR_DAY_FORMAT_NOT_VALID = "day should be integer between 1 and 31."
ERR_MONTH_FORMAT_NOT_VALID = "month should be either string having single month or list of multiple months."
ERR_WEEKDAY_FORMAT_NOT_VALID = "weekday should be either string having single day or list of multiple days."
ERR_CMD_LENGTH_INVALID = "command string should be more then single letter."


def validate_command_string(func):
    def wrapper(*args):
        if not len(args):
            raise ValueError(ERR_NO_ARGS_FOUND)
        cmd = args[0]
        if not isinstance(cmd, str):
            raise ValueError(ERR_COMMAND_FORMAT_NOT_VALID)
        if not len(cmd.strip()) >= MIN_CMD_LENGTH:
            raise ValueError(ERR_CMD_LENGTH_INVALID)

        func(*args)
    return wrapper


def validate_hour(hour):
    if not isinstance(hour, int):
        raise ValueError(ERR_HOUR_FORMAT_NOT_VALID)
    if hour < 0 or hour > 23:
        raise ValueError(ERR_HOUR_FORMAT_NOT_VALID)


def validate_minute(minute):
    if not isinstance(minute, int):
        raise ValueError(ERR_MIN_FORMAT_NOT_VALID)
    if minute < 0 or minute > 59:
        raise ValueError(ERR_MIN_FORMAT_NOT_VALID)


def validate_day(day):
    if not isinstance(day, int):
        raise ValueError(ERR_DAY_FORMAT_NOT_VALID)
    if day < 1 or day > 31:
        raise ValueError(ERR_DAY_FORMAT_NOT_VALID)


def validate_month(month):
    def is_name_correct(m):
        list_month = ['january', 'february', 'march', 'april', 'may', 'june',
                      'july', 'august', 'september', 'october', 'november', 'december']
        if m.lower() in list_month:
            return True
        list_month = ['jan', 'feb', 'mar', 'apr', 'may',
                      'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
        if m.lower() in list_month:
            return True

        return False

    if not isinstance(month, str) and not isinstance(month, list):
        raise ValueError(ERR_MONTH_FORMAT_NOT_VALID)
    if isinstance(month, str):
        if not is_name_correct(month):
            raise ValueError(ERR_MONTH_FORMAT_NOT_VALID)
    else:
        for m in month:
            if not is_name_correct(m):
                raise ValueError(ERR_MONTH_FORMAT_NOT_VALID)


def validate_weekday(weekday):
    def is_name_correct(d):
        list_day = ['sunday', 'monday', 'tuesday',
                    'wednesday', 'thursday', 'friday', 'saturday']
        if d.lower() in list_day:
            return True
        list_day = ['sun', 'mon', 'tue', 'wed', 'thu', 'fri', 'sat']
        if d.lower() in list_day:
            return True

        return False

    if not isinstance(weekday, str) and not isinstance(weekday, list):
        raise ValueError(ERR_WEEKDAY_FORMAT_NOT_VALID)
    if isinstance(weekday, str):
        if not is_name_correct(weekday):
            raise ValueError(ERR_WEEKDAY_FORMAT_NOT_VALID)
    else:
        for d in weekday:
            if not is_name_correct(d):
                raise ValueError(ERR_WEEKDAY_FORMAT_NOT_VALID)


def validate_daily(hour, minute):
    validate_hour(hour)
    validate_minute(minute)


def validate_monthly(day, hour, minute):
    validate_day(day)
    validate_hour(hour)
    validate_minute(minute)


def validate_yearly(month, day, hour, minute):
    validate_month(month)
    validate_day(day)
    validate_hour(hour)
    validate_minute(minute)


def validate_minutely(minute):
    if not isinstance(minute, int):
        raise ValueError(ERR_MIN_FORMAT_NOT_VALID)
    if minute < 1 or minute > 59:
        raise ValueError(ERR_MIN_FORMAT_NOT_VALID)


def validate_by_weekday(weekday, hour, minute):
    validate_weekday(weekday)
    validate_hour(hour)
    validate_minute(minute)


def validate_deploy(content):
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