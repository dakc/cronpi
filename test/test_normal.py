import cronpi
import unittest
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

# commands to be inserted as crontab
cron_cmd = [
    "0 0 * * * echo 10",
    "0 10 * * * echo 11",
    "45 10 * * * echo 12",

    "0 0 1 * * echo 20",
    "0 0 10 * * echo 21",
    "0 17 10 * * echo 22",
    "30 17 10 * * echo 23",

    "0 0 1 1 * echo 30",
    "0 0 1 3 * echo 31",
    "0 0 1 3,4,10 * echo 32",
    "0 0 10 10 * echo 33",
    "0 17 10 10 * echo 34",
    "30 17 10 10 * echo 35",

    "*/30 * * * * echo 40",

    "0 0 * * 0 echo 50",
    "0 0 * * 0,1 echo 51",
    "0 17 * * 0,2,5 echo 52",
    "40 17 * * 5 echo 53",

    "* * * * * echo 60",
    "*/15 * * * * echo 61",
    "0 9,18 * * * echo 62",
    "0 10-18 * * * echo 63",
    "0 */6 * * * echo 64",
    "0 6-18/6 * * * echo 65",
    "0 0,10-18 * * * echo 66",
    "0 21,6-18/6 * * * echo 67"
]
cron_cmd = [x.replace(" ", "") for x in cron_cmd]

class Testcronpi(unittest.TestCase):
    def test_deploy_daily(self):
        """
        deploy_daily(cmd, hour=0, minute=0)
        """        
        # run job at 0:00 (parameters:cmd)
        cronpi.deploy_daily("echo 10")

        # run job daily at 10:00AM (parameters:cmd, hour)
        cronpi.deploy_daily("echo 11", 10)

        # run job daily at 10:45AM (parameters:cmd, hour , min)
        cronpi.deploy_daily("echo 12", 10,45)

    def test_deploy_monthly(self):
        """
        deploy_monthly(cmd, day=1, hour=0, minute=0)
        """
        # run job at 1th of the month at 0:00 (parameters:cmd)
        cronpi.deploy_monthly("echo 20")

        # run job at 10th of the month at 0:00AM (parameters:cmd, month)
        cronpi.deploy_monthly("echo 21", 10)

        # run job at 10th of the month at 5:00PM (parameters:cmd, month, hour)
        cronpi.deploy_monthly("echo 22", 10, 17)

        # run job at 10th of the month at 5:30PM (parameters:cmd, month, hour, min)
        cronpi.deploy_monthly("echo 23", 10, 17, 30)

    def test_deploy_yearly(self):
        """
        deploy_yearly(cmd, month="jan", day=1, hour=0, minute=0)
        """
        # run job at 1st january at 0:00 (parameters:cmd)
        cronpi.deploy_yearly("echo 30")

        # run job at 1st march at 0:00AM (parameters:cmd, month)
        cronpi.deploy_yearly("echo 31", "march")

        # run job at 1st march,april,october at 0:00AM (parameters:cmd, list of months)
        cronpi.deploy_yearly("echo 32", ["march","apr","oct"])

        # run job at 10th october at 0:00AM (parameters:cmd, month, day)
        cronpi.deploy_yearly("echo 33", "oct", 10)

        # run job at 10th october at 5:00PM (parameters:cmd, month, day, hour)
        cronpi.deploy_yearly("echo 34", "oct", 10, 17)

        # run job at 10th october at 5:30PM (parameters:cmd, month, hour. min)
        cronpi.deploy_yearly("echo 35", "oct", 10, 17, 30)

    def test_deploy_minutely(self):
        """
        deploy_minutely(cmd, minute)
        """
        # run job at every 30 minutes (parameters:cmd, minute)
        cronpi.deploy_minutely("echo 40", 30)

    def test_deploy_by_weekday(self):
        """
        deploy_by_weekday(cmd, weekday, hour=0, minute=0)
        """
        # run job at every sunday at 0:00 (parameters:cmd, weekday)
        cronpi.deploy_by_weekday("echo 50", "sun")

        # run job at every sunday and monday at 0:00AM (parameters:cmd, list of weekdays )
        cronpi.deploy_by_weekday("echo 51", ["sun", "monday"])

        # run job at every sunday, tuesday and friday at 5:00PM (parameters:cmd, list of weekdays, hour)
        cronpi.deploy_by_weekday("echo 52", ["sun","tue","fri"], 17)

        # run job at every friday at 5:40PM (parameters:cmd, weekday, hour, minute)
        cronpi.deploy_by_weekday("echo 53", "fri", 17, 40)

    def test_deploy(self):
        # run at every minute
        self.assertTrue(cronpi.deploy("* * * * * echo 60"))
        # run at every 15 minutes
        self.assertTrue(cronpi.deploy("*/15 * * * * echo 61"))
        # run for 9:00 and 18:00
        self.assertTrue(cronpi.deploy("0 9,18 * * * echo 62"))
        # run between 10:00~18:00 every (min@0)
        self.assertTrue(cronpi.deploy("0 10-18 * * * echo 63"))
        # run every 6hours from 0:00
        self.assertTrue(cronpi.deploy("0 */6 * * * echo 64"))
        # run every 6hours from 6:00 to 18:00 (min@0)
        self.assertTrue(cronpi.deploy("0 6-18/6 * * * echo 65"))
        # run at 0:00 and between 10:00~18:00 (min@0)
        self.assertTrue(cronpi.deploy("0 0,10-18 * * * echo 66"))
        # run at 21:00 and every 6 hours between 6:00~18:00 (min@0)
        self.assertTrue(cronpi.deploy("0 21,6-18/6 * * * echo 67"))
    
    def tearDown(self):
        """
        Delete all the crontab added"
        """
        # check if all the cron jobs are inserted or not
        installed_content = cronpi.app._get_installed_content()
        installed_content = installed_content.rstrip("\n")
        for installed_crontab in installed_content.split("\n"):
            t = installed_crontab.replace(" ", "")
            self.assertTrue(t in cron_cmd)

        # delete crontab (change -l to -r)
        cronpi.app._run_shell_cmd("crontab -l")

if __name__ == '__main__':
    unittest.main()