from cronpi.app import cronpiObj as __cronpiObj

def run_every_day(cmd, isOverwrite=False):
    """
    set a command that runs every day.
    It is of no use if "on" method is not called.

    parameters
    ---------------
    cmd: string
        command to run as cronjob

    isOverwrite: bool
        If True and cmd already exists as cronjob,
        it will overwrite with the new date and time.
        Otherwise, it will insert as new cron job.
        Default value is False.
    """
    __cronpiObj.type = 1
    return __cronpiObj.set_command(cmd,isOverwrite)

def run_every_week(cmd, isOverwrite=False):
    """
    set a command that runs every week.
    It is of no use if "on" method is not called.

    parameters
    ---------------
    cmd: string
        command to run as cronjob

    isOverwrite: bool
        If True and cmd already exists as cronjob,
        it will overwrite with the new date and time.
        Otherwise, it will insert as new cron job.
        Default value is False.
    """
    __cronpiObj.type = 2
    return __cronpiObj.set_command(cmd, isOverwrite)
    
def run_every_month(cmd, isOverwrite=False):
    """
    set a command that runs every month.
    It is of no use if "on" method is not called.

    parameters
    ---------------
    cmd: string
        command to run as cronjob

    isOverwrite: bool
        If True and cmd already exists as cronjob,
        it will overwrite with the new date and time.
        Otherwise, it will insert as new cron job.
        Default value is False.
    """
    __cronpiObj.type = 3
    return __cronpiObj.set_command(cmd, isOverwrite)
    
def run_every_year(cmd, isOverwrite=False):
    """
    set a command that runs every year.
    It is of no use if "on" method is not called.

    parameters
    ---------------
    cmd: string
        command to run as cronjob

    isOverwrite: bool
        If True and cmd already exists as cronjob,
        it will overwrite with the new date and time.
        Otherwise, it will insert as new cron job.
        Default value is False.
    """
    __cronpiObj.type = 4
    return __cronpiObj.set_command(cmd, isOverwrite)
    
def run_by_date(cmd, isOverwrite=False):
    """
    set a command that runs at given date.
    It is of no use if "on" method is not called.

    parameters
    ---------------
    cmd: string
        command to run as cronjob

    isOverwrite: bool
        If True and cmd already exists as cronjob,
        it will overwrite with the new date and time.
        Otherwise, it will insert as new cron job.
        Default value is False.
    """
    __cronpiObj.type = 5
    return __cronpiObj.set_command(cmd, isOverwrite)
    
def run_custom(cmd, isOverwrite=False):
    """
    set a cronjob like "crontab -e" command

    parameters
    ---------------
    cmd: string
        command to run as cronjob

    isOverwrite: bool
        If True and cmd already exists as cronjob,
        it will overwrite with the new date and time.
        Otherwise, it will insert as new cron job.
        Default value is False.
    """
    __cronpiObj.type = 6
    return __cronpiObj.set_command(cmd, isOverwrite).on(None)

def get_job_list():
    """
    get the jobs in crontab for current user

    Return
    ----------
    result: list
        result of "crontab -l" command  as list
    """
    installed_content = __cronpiObj.get_job_list()
    installed_content = installed_content.rstrip("\n")

    return installed_content.split("\n")