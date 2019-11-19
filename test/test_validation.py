import unittest
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

import cronpi

class Testcronpi(unittest.TestCase):
    def test_deploy_daily(self):
        """
        deploy_daily
        cronpi.run_every_day("ls", isOverwrite=True).on("7:30pm")
        """
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_CMD_LENGTH_INVALID):
            cronpi.run_every_day("a", isOverwrite=True).on("")
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_JOB_TIME_FORMAT_NOT_VALID):
            cronpi.run_every_day("ls", isOverwrite=True).on("")
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_JOB_TIME_FORMAT_NOT_VALID):
            cronpi.run_every_day("ls", isOverwrite=True).on("adsf")
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_HOUR_FORMAT_NOT_VALID):
            cronpi.run_every_day("ls", isOverwrite=True).on("25:30")
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_HOUR_FORMAT_NOT_VALID):
            cronpi.run_every_day("ls", isOverwrite=True).on("13:30pm")
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_MIN_FORMAT_NOT_VALID):
            cronpi.run_every_day("ls", isOverwrite=True).on("2:60")

    def test_deploy_by_weekday(self):
        """
        deploy_weekly
        cronpi.run_every_week("ls", isOverwrite=True).on(["sat", "friday"], time="7:30pm")
        """
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_WEEKDAY_FORMAT_NOT_VALID):
            cronpi.run_every_week("ls", isOverwrite=True).on("satu", time="7:30pm")
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_WEEKDAY_FORMAT_NOT_VALID):
            cronpi.run_every_week("ls", isOverwrite=True).on(["sat", 23], time="7:30pm")
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_HOUR_FORMAT_NOT_VALID):
            cronpi.run_every_week("ls", isOverwrite=True).on(["sat", "fri"], time="17:30pm")

    def test_deploy_monthly(self):
        """
        deploy_monthly
        cronpi.run_every_month("ls", isOverwrite=True).on(2, time="7:30")
        """
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_DAY_FORMAT_NOT_VALID):
            cronpi.run_every_month("ls", isOverwrite=True).on("satu", time="7:30pm")
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_DAY_FORMAT_NOT_VALID):
            cronpi.run_every_month("ls", isOverwrite=True).on(["sat", 23], time="7:30pm")
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_DAY_FORMAT_NOT_VALID):
            cronpi.run_every_month("ls", isOverwrite=True).on([5,40], time="7:30pm")
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_HOUR_FORMAT_NOT_VALID):
            cronpi.run_every_month("ls", isOverwrite=True).on([5,10], time="17:30pm")

    def test_deploy_yearly(self):
        """
        deploy_yearly
        cronpi.run_every_year("ls", isOverwrite=True).on(["jan", "july"], day=[2, 5], time="7:30pm")
        """
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_MONTH_FORMAT_NOT_VALID):
            cronpi.run_every_year("ls", isOverwrite=True).on("satu", day=2, time="7:30pm")
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_DAY_FORMAT_NOT_VALID):
            cronpi.run_every_year("ls", isOverwrite=True).on("jan", time="7:30pm")

    def test_deploy_by_date(self):
        """
        deploy_by_date
        cronpi.run_by_date("ls", isOverwrite=True).on("2020-10-20 7:30")
        """
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_JOB_DATE_NOT_VALID_SPAN):
            cronpi.run_by_date("ls", isOverwrite=True).on("2018-10-20 7:30")

    def test_deploy_like_crontab(self):
        """
        deploy_by_date
        cronpi.run_custom("* * * * * ls", isOverwrite=True)
        """
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_COMMAND_FORMAT_NOT_VALID):
            cronpi.run_custom("* * * *  ls", isOverwrite=True)


if __name__ == '__main__':
    unittest.main()