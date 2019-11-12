import re
from datetime import datetime
from cronpi import cron, validator

class App:
    def __init__(self):
        self.__cmd = ""
        self.__overwrite = False
        self.type = 0

    def set_command(self, command, overwrite):
        self.__cmd, self.__overwrite = validator.validate_command(
            command, overwrite)
        return self

    def deploy_daily(self, job_time):
        dt = validator.get_time(job_time)
        crontab_command = "{} {} * * * {}".format(
            dt[1], dt[0], self.__cmd)
        return cron.deploy(crontab_command, self.__overwrite)

    def deploy_by_weekday(self, job_time, target_day):
        dt = validator.get_time(job_time)
        weekdays = validator.get_week_days(target_day)

        crontab_command = "{} {} * * {} {}".format(
            dt[1], dt[0], weekdays, self.__cmd)
        return cron.deploy(crontab_command, self.__overwrite)

    def deploy_by_month_day(self, job_time, target_day):
        dt = validator.get_time(job_time)
        days = validator.get_month_days(target_day)

        crontab_command = "{} {} {} * * {}".format(
            dt[1], dt[0], days, self.__cmd)
        return cron.deploy(crontab_command, self.__overwrite)

    def deploy_by_month_name(self, job_time, target_day, target_month):
        dt = validator.get_time(job_time)
        days = validator.get_month_days(target_day)
        months = validator.get_months(target_month)
        crontab_command = "{} {} {} {} * {}".format(
            dt[1], dt[0], days, months, self.__cmd)
        return cron.deploy(crontab_command, self.__overwrite)

    def deploy_by_date(self, job_time):
        month, day, hour, minute = validator.get_time_once(job_time)
        crontab_command = "{} {} {} {} * {}".format(
            minute, hour, day, month, self.__cmd)
        return cron.deploy(crontab_command, self.__overwrite)

    def deploy_like_crontab_command(self):
        return cron.deploy(self.__cmd, self.__overwrite)

    def on(self, arg, **kwargs):
        """
        Time to deploy the cronjob.
        """
        if self.type == 1:
            return self.deploy_daily(arg)

        if self.type == 2:
            return self.deploy_by_weekday(kwargs.get("time", ""), arg)

        if self.type == 3:
            return self.deploy_by_month_day(kwargs.get("time", ""), arg)

        if self.type == 4:
            return self.deploy_by_month_name(kwargs.get("time", ""), kwargs.get("day", ""), arg)

        if self.type == 5:
            return self.deploy_by_date(arg)

        if self.type == 6:
            return self.deploy_like_crontab_command()

    def get_job_list(self):
        """
        get the cron job list of current user
        """
        return cron._get_installed_content()


cronpiObj = App()