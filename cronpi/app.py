import os
import subprocess

from cronpi import validator

@validator.validate_command_string
def deploy_daily(cmd, hour=0, minute=0):
    """
    Install crontab running daily into a system if it's not installed.
    If the cron with same command exists, then it will update that.
    Raises value error if the content is not in correct format.

    Parameters
    ----------
    cmd: string
        command to execute as cron
    hour: int
        Time representing Hour(0~23) to run the job.
        It is Optional. 
        If not set Job will be set to defalut value 0.
    minute: int
        Time representing Minute(0~59) to run the job.
        It is Optional. 
        If not set Job will be set to defalut value 0.

    Usage
    ----------
    1. Run daily at 0:00
    cronpi.deploy_daily("ls -al /opt")

    2. Run daily at 5AM
    cronpi.deploy_daily("ls -al /opt", 5)

    3. Run daily at 10PM
    cronpi.deploy_daily("ls -al /opt", 22)

    4. Run daily at 10:30PM
    cronpi.deploy_daily("ls -al /opt", 22, 30)    
    """
    # validation
    validator.validate_daily(hour, minute)

    crontab_cmd = "{} {} * * * {}".format(minute, hour, cmd)
    deploy(crontab_cmd)


@validator.validate_command_string
def deploy_monthly(cmd, day=1, hour=0, minute=0):
    """
    Install crontab running monthly into a system if it's not installed.
    If the cron with same command exists, then it will update that.
    Raises value error if the content is not in correct format.

    Parameters
    ----------
    cmd: string
        command to execute as cron
    day: int
        Day of month(1~31) to run the job.It is Optional. 
        If not set Job will be set to defalut value 1.
    hour: int
        Time representing Hour(0~23) to run the job.
        It is Optional. 
        If not set Job will be set to defalut value 0.
    minute: int
        Time representing Minute(0~59) to run the job.
        It is Optional. 
        If not set Job will be set to defalut value 0.

    Usage
    ----------
    1. Run at every 1st day of month at 0:00
    cronpi.deploy_monthly("ls -al /opt")

    2. Run at every 20th of the month at 0:00
    cronpi.deploy_monthly("ls -al /opt", 20)

    3. Run at every 5th of the month at 2PM
    cronpi.deploy_monthly("ls -al /opt", 5, 14)

    4. Run at every 5th of the month at 2:30PM
    cronpi.deploy_monthly("ls -al /opt", 5, 14, 30)
    """
    # validation
    validator.validate_monthly(day, hour, minute)

    crontab_cmd = "{} {} {} * * {}".format(minute, hour, day, cmd)
    deploy(crontab_cmd)


@validator.validate_command_string
def deploy_yearly(cmd, month="jan", day=1, hour=0, minute=0):
    """
    Install crontab running yearly into a system if it's not installed.
    If the cron with same command exists, then it will update that.
    Raises value error if the content is not in correct format.

    Parameters
    ----------
    cmd: string
        command to execute as cron
    month: string or list
        Month of a year to run the job.
        It can be either fullname or first THREE letters.
        (eg, jan,January,FEB,..)
        It can be either a single month as a string or a list of months.
        (eg, sun or [jan,FEB,juNe])
        If not set Job will be set to defalut value to January.
    day: int
        Day of month(1~31) to run the job.It is Optional. 
        If not set Job will be set to defalut value 1.
    hour: int
        Time representing Hour(0~23) to run the job.
        It is Optional. 
        If not set Job will be set to defalut value 0.
    minute: int
        Time representing Minute(0~59) to run the job.
        It is Optional. 
        If not set Job will be set to defalut value 0.

    Usage
    ----------
    1. Run at every 1st January at 0:00
    cronpi.deploy_yearly("ls -al /opt", "january")

    2. Run at every 1st January and 1st october  at 0:00 
    cronpi.deploy_yearly("ls -al /opt", ["jan","oct"])

    3. Run at every 5th January at 2PM
    cronpi.deploy_yearly("ls -al /opt", "january", 5, 14)

    4. Run at every 5th January at 2:30AM
    cronpi.deploy_yearly("ls -al /opt", "january", 5, 2, 30)
    """
    # validation
    validator.validate_yearly(month, day, hour, minute)

    crontab_cmd = _get_month_cmd(cmd, month, day, hour, minute)
    deploy(crontab_cmd)


@validator.validate_command_string
def deploy_minutely(cmd, minute):
    """
    Install crontab running minutely into a system if it's not installed.
    If the cron with same command exists, then it will update that.
    Raises value error if the content is not in correct format.

    Parameters
    ----------
    cmd: string
        command to execute as cron
    minute: int
        Time interval in minutes to repeat the command

    Usage
    ----------
    1. Run at every 15minutes
    cronpi.deploy_minutely("ls -al /opt", 15)
    """
    # validation
    validator.validate_minutely(minute)

    crontab_cmd = "*/{} * * * * {}".format(minute, cmd)
    deploy(crontab_cmd)


@validator.validate_command_string
def deploy_by_weekday(cmd, weekday, hour=0, minute=0):
    """
    Install crontab by weekday into a system if it's not installed.
    If the cron with same command exists, then it will update that.
    Raises value error if the content is not in correct format.

    Parameters
    ----------
    cmd: string
        command to execute as cron
    weekday: string or list
        name of a day in week.
        It can be either fullname or first THREE letters.
        (eg, sun,Monday,SAT,..)
        It can be either a single day as a string or a list of day.
        (eg, sun or [mon,tue])
    hour: int
        Time representing Hour(0~23) to run the job.
        It is Optional. 
        If not set Job will be set to defalut value 0.
    minute: int
        Time representing Minute(0~59) to run the job.
        It is Optional. 
        If not set Job will be set to defalut value 0.

    Usage
    ----------
    1. Run at every saturday at 0:00AM
    cronpi.deploy_by_weekday("ls -al /opt", "saturday")

    2. Run at every saturday and sunday  at 0:00 
    cronpi.deploy_by_weekday("ls -al /opt", ["sat","sun"])

    3. Run at every saturday at 5PM
    cronpi.deploy_by_weekday("ls -al /opt", "SAT", 17)

    4. Run at every saturday at 5:30PM
    cronpi.deploy_by_weekday("ls -al /opt", "SAT", 17, 30)
    """
    # validation
    validator.validate_by_weekday(weekday, hour, minute)

    crontab_cmd = _get_week_cmd(cmd, weekday, hour, minute)
    deploy(crontab_cmd)


def deploy(content):
    """
    Install crontab into a system if it's not installed.
    If the cron with same command exists, then it will update that.
    Raises value error if the content is not in correct format.

    Parameters
    ----------
    content: string
        single crontab content

    Usage
    ----------
    1. Run at every minutes
    cronpi.deploy("* * * * * ls -al /opt")
    """
    # validation
    validator.validate_deploy(content)

    # update crontab
    new_content = _get_updated_content(content)
    if new_content is not None:
        retcode, err, out = _run_shell_cmd("crontab", new_content)
        if retcode != 0:
            raise ValueError(
                "failed to install crontab, check if crontab is valid ; out={} ; err={}".format(out, err))
    return True


def _get_command_from_cron(content):
    """
    Get the command part from crontab content

    Parameters
    ----------
    content: string
        single crontab content
    
    Returns
    ----------
    cmd: string
        command part of the crontab
    """
    cmd = ""
    split_command = content.split()
    if len(split_command) >= validator.CMD_INDEX:
        for i in range(validator.CMD_INDEX, len(split_command)):
            cmd += split_command[i].strip()
    return cmd


def _get_updated_content(content):
    """
    Get the content of crontab after updating the command got recently

    Parameters
    ----------
    content: string
        crontab content got recently
    
    Returns
    ----------
    new_content: string
        crontab content after update
    """
    new_content = ""
    is_command_exists = False
    cmd = _get_command_from_cron(content)
    installed_content = _get_installed_content()
    installed_content = installed_content.rstrip("\n")
    for installed_crontab in installed_content.split("\n"):
        if _get_command_from_cron(installed_crontab) == cmd:
            installed_crontab = content
            is_command_exists = True
        new_content += "\n%s" % installed_crontab

    if not is_command_exists:
        new_content += "\n%s" % content

    return new_content.strip() + "\n"


def _get_installed_content():
    """
    get the current installed crontab.

    Returns
    ----------
    installed_content: string
        crontab content multiline
    """
    retcode, err, installed_content = _run_shell_cmd("crontab -l")
    if retcode != 0 and b'no crontab for' not in err:
        raise OSError("crontab not supported in your system")
    return installed_content.decode("utf-8")


def _run_shell_cmd(cmd, input=None):
    """
    run shell command and return the a tuple of the cmd's return code, std
    error and std out.
    WARN: DO NOT RUN COMMANDS THAT NEED TO INTERACT WITH STDIN WITHOUT SPECIFY
    INPUT, (eg cat), IT WILL NEVER TERMINATE.

    Parameters
    ----------
    cmd: string
        command to run
    input: string
        arguments for given command

    Returns
    ----------
    returncode: int
        code returned by subprocess
    stderrdata: strings if streams were opened in text mode; otherwise, bytes
        data from stderr
    stdoutdata: strings if streams were opened in text mode; otherwise, bytes
        data from stdout
    """
    if not hasattr(os, "setsid"):
        raise OSError("crontab not supported in your system")

    if input is not None:
        p = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             close_fds=True, preexec_fn=os.setsid)
        input = input.encode()
    else:
        p = subprocess.Popen(cmd, shell=True,
                             stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                             close_fds=True, preexec_fn=os.setsid)

    stdoutdata, stderrdata = p.communicate(input)
    return p.returncode, stderrdata, stdoutdata


def _get_week_cmd(cmd, weekday, hour, minute):
    """
    Get the crontab command for single job that runs weekly.

    Parameters
    ----------
    cmd: string
        command to execute as cron
    weekday: string or list
        name of a day in week.
        It can be either fullname or first THREE letters.
        (eg, sun,Monday,SAT,..)
        It can be either a single day as a string or a list of day.
        (eg, sun or [mon,tue])
    hour: int
        0~23
    minute: int
        0~59

    Returns
    ----------
    cronjob: string
        crontab command for single job
    """
    day_id = ""
    if isinstance(weekday, str):
        day_id = _get_day_id(weekday)

    elif isinstance(weekday, list):
        for day in weekday:
            _day_id = _get_day_id(day)
            if day_id is not None:
                day_id += _day_id + ","
    return "{} {} * * {} {}".format(minute, hour, day_id.rstrip(","), cmd)


def _get_day_id(day):
    """
    Get the integer for a given weekday (0~6)

    Parameters
    ----------
    day: string
        It can be either fullname or first THREE letters of a weekday

    Returns
    ----------
    day id: string
        id of weekday as string
    """
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


def _get_month_cmd(cmd, month, day, hour, minute):
    """
    Get the crontab command for single job that runs weekly.

    Parameters
    ----------
    cmd: string
        command to execute as cron
    month: string or list
        name of a month in a year.
        It can be either fullname or first THREE letters.
        (eg, jan,January,FEB,..)
        It can be either a single month as a string or a list of months.
        (eg, sun or [jan,FEB,juNe])
    day: int
        1~31
    hour: int
        0~23
    minute: int
        0~59

    Returns
    ----------
    cronjob: string
        crontab command for single job
    """
    month_id = ""
    if isinstance(month, str):
        month_id = _get_month_id(month)

    elif isinstance(month, list):
        for m in month:
            _month_id = _get_month_id(m)
            if month_id is not None:
                month_id += _month_id + ","
    return "{} {} {} {} * {}".format(minute, hour, day, month_id.rstrip(","), cmd)


def _get_month_id(month):
    """
    Get the integer for a given month (1~12)

    Parameters
    ----------
    month: string
        It can be either fullname or first THREE letters of a month

    Returns
    ----------
    day id: string
        id of month as string from 1~12
    """
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
