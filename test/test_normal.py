import unittest
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

import cronpi
from cronpi import get_job_list

class Testcronpi(unittest.TestCase):
    def test_deploy_daily(self):
        """
        deploy_daily
        """        
        cronpi.run_every_day("ls", isOverwrite=True).on("7:30")
        self.assertEqual(get_job_list()[0], "30 7 * * * ls")

        cronpi.run_every_day("ls", isOverwrite=True).on("7:30pm")
        self.assertEqual(get_job_list()[0], "30 19 * * * ls")

        cronpi.run_every_day("ls", isOverwrite=True).on("17:30")
        self.assertEqual(get_job_list()[0], "30 17 * * * ls")

    def test_deploy_by_weekday(self):
        """
        deploy_by_weekday
        """
        cronpi.run_every_week("ls", isOverwrite=True).on("saturday", time="7:30")
        self.assertEqual(get_job_list()[0], "30 7 * * 6 ls")

        cronpi.run_every_week("ls", isOverwrite=True).on("saturday", time="7:30am")
        self.assertEqual(get_job_list()[0], "30 7 * * 6 ls")

        cronpi.run_every_week("ls", isOverwrite=True).on(["sat", "friday"], time="7:30pm")
        self.assertEqual(get_job_list()[0], "30 19 * * 6,5 ls")

        cronpi.run_every_week("ls", isOverwrite=True).on(["sat", "friday"], time="17:30")
        self.assertEqual(get_job_list()[0], "30 17 * * 6,5 ls")

    def test_deploy_monthly(self):
        """
        deploy_monthly
        """
        cronpi.run_every_month("ls", isOverwrite=True).on(2, time="7:30")
        self.assertEqual(get_job_list()[0], "30 7 2 * * ls")

        cronpi.run_every_month("ls", isOverwrite=True).on(2, time="7:30am")
        self.assertEqual(get_job_list()[0], "30 7 2 * * ls")

        cronpi.run_every_month("ls", isOverwrite=True).on([2, 5], time="7:30pm")
        self.assertEqual(get_job_list()[0], "30 19 2,5 * * ls")

        cronpi.run_every_month("ls", isOverwrite=True).on([2, 5], time="17:30")
        self.assertEqual(get_job_list()[0], "30 17 2,5 * * ls")

    def test_deploy_yearly(self):
        """
        deploy_yearly
        """
        cronpi.run_every_year("ls", isOverwrite=True).on("january", day=2, time="7:30")
        self.assertEqual(get_job_list()[0], "30 7 2 1 * ls")

        cronpi.run_every_year("ls", isOverwrite=True).on("january", day=2, time="7:30am")
        self.assertEqual(get_job_list()[0], "30 7 2 1 * ls")

        cronpi.run_every_year("ls", isOverwrite=True).on(["jan", "july"], day=[2, 5], time="7:30pm")
        self.assertEqual(get_job_list()[0], "30 19 2,5 1,7 * ls")

        cronpi.run_every_year("ls", isOverwrite=True).on(["jan"], day=[2, 5], time="17:30")
        self.assertEqual(get_job_list()[0], "30 17 2,5 1 * ls")

    def test_deploy_by_date(self):
        """
        deploy_by_date
        """
        cronpi.run_by_date("ls", isOverwrite=True).on("2020-10-20 7:30")
        self.assertEqual(get_job_list()[0], "30 7 20 10 * ls")

        cronpi.run_by_date("ls", isOverwrite=True).on("2020-10-20 7:30am")
        self.assertEqual(get_job_list()[0], "30 7 20 10 * ls")

        cronpi.run_by_date("ls", isOverwrite=True).on("2020-10-20 7:30pm")
        self.assertEqual(get_job_list()[0], "30 19 20 10 * ls")

        cronpi.run_by_date("ls", isOverwrite=True).on("2020-10-20 17:30")
        self.assertEqual(get_job_list()[0], "30 17 20 10 * ls")

    def test_deploy_like_crontab(self):
        """
        deploy_by_date
        """
        cronpi.run_custom("* * * * * ls", isOverwrite=True)
        self.assertEqual(get_job_list()[0], "* * * * * ls")

    def test_for_overwrite(self):
        """
        deploy_by_date

        Note: Donot forget to crontab -r
        """
        cron_job = (
            "* * * * * ls",
            "30 * * * * ls",
            "30 7 * * * ls",
        )
        cronpi.run_custom(cron_job[0], isOverwrite=True)
        cronpi.run_custom("30 * * * * ls")
        cronpi.run_every_day("ls").on("7:30am")

        cron_result = get_job_list()
        for itm in cron_result:
            self.assertTrue(itm in cron_job)

        for itm in cron_job:
            self.assertTrue(itm in cron_result)

if __name__ == '__main__':
    unittest.main()