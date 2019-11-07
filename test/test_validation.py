import unittest
from pathlib import Path
import sys
sys.path.append(str(Path(__file__).parent.parent))

import cronpi

class Testcronpi(unittest.TestCase):
    def test_deploy_daily(self):
        """
        deploy_daily(cmd, hour=0, minute=0)
        """
        # test for calling with empty command
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_CMD_LENGTH_INVALID):
            cronpi.deploy_daily("")

        # test for passing invalid command
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_COMMAND_FORMAT_NOT_VALID):
            cronpi.deploy_daily(1)

        # test for passing invalid hour
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_HOUR_FORMAT_NOT_VALID):
            cronpi.deploy_daily("ls -al /df", "")

        # test for passing invalid minute
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_MIN_FORMAT_NOT_VALID):
            cronpi.deploy_daily("ls -al /df", 5, "nj")

    def test_deploy_monthly(self):
        """
        deploy_monthly(cmd, day=1, hour=0, minute=0)
        """
        # test for calling with empty command
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_CMD_LENGTH_INVALID):
            cronpi.deploy_daily("")

        # test for passing invalid command
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_COMMAND_FORMAT_NOT_VALID):
            cronpi.deploy_monthly(1)

        # test for passing invalid day
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_DAY_FORMAT_NOT_VALID):
            cronpi.deploy_monthly("ls -al /df", "")

        # test for passing invalid hour
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_HOUR_FORMAT_NOT_VALID):
            cronpi.deploy_monthly("ls -al /df", 5, "")

        # test for passing invalid minute
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_MIN_FORMAT_NOT_VALID):
            cronpi.deploy_monthly("ls -al /df", 5, 10, "nj")

        
    def test_deploy_yearly(self):
        """
        deploy_yearly(cmd, month="jan", day=1, hour=0, minute=0)
        """
        # test for calling with empty command
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_CMD_LENGTH_INVALID):
            cronpi.deploy_daily("")

        # test for passing invalid command
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_COMMAND_FORMAT_NOT_VALID):
            cronpi.deploy_yearly(1)

        # test for passing invalid month
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_MONTH_FORMAT_NOT_VALID):
            cronpi.deploy_yearly("ls -al /df", "")
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_MONTH_FORMAT_NOT_VALID):
            cronpi.deploy_yearly("ls -al /df", "jsdf")
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_MONTH_FORMAT_NOT_VALID):
            cronpi.deploy_yearly("ls -al /df", ["jan", "febsd"])

        # test for passing invalid day
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_DAY_FORMAT_NOT_VALID):
            cronpi.deploy_yearly("ls -al /df", "jan", "")

        # test for passing invalid hour
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_HOUR_FORMAT_NOT_VALID):
            cronpi.deploy_yearly("ls -al /df", "jan", 2, "")

        # test for passing invalid minute
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_MIN_FORMAT_NOT_VALID):
            cronpi.deploy_yearly("ls -al /df", "jan", 2, 4, "")

    def test_deploy_minutely(self):
        """
        deploy_minutely(cmd, minute)
        """
            # test for calling with empty command
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_CMD_LENGTH_INVALID):
            cronpi.deploy_daily("", "")

        # test for passing invalid minute
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_MIN_FORMAT_NOT_VALID):
            cronpi.deploy_minutely("ls -al /df", "")
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_MIN_FORMAT_NOT_VALID):
            cronpi.deploy_minutely("ls -al /df", "nj")

    def test_deploy_by_weekday(self):
        """
        deploy_by_weekday(cmd, weekday, hour=0, minute=0)
        """
        # test for calling with empty command
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_CMD_LENGTH_INVALID):
            cronpi.deploy_daily("", "")

        # test for passing invalid command
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_COMMAND_FORMAT_NOT_VALID):
            cronpi.deploy_by_weekday(1, "")

        # test for passing invalid weekdayday
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_WEEKDAY_FORMAT_NOT_VALID):
            cronpi.deploy_by_weekday("ls -al /df", "")
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_WEEKDAY_FORMAT_NOT_VALID):
            cronpi.deploy_by_weekday("ls -al /df", "sanday")
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_WEEKDAY_FORMAT_NOT_VALID):
            cronpi.deploy_by_weekday("ls -al /df", ["sunday", "manday"])

        # test for passing invalid hour
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_HOUR_FORMAT_NOT_VALID):
            cronpi.deploy_by_weekday("ls -al /df", "sun", "")

        # test for passing invalid minute
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_MIN_FORMAT_NOT_VALID):
            cronpi.deploy_by_weekday("ls -al /df", "sun", 10, "nj")

    def test_deploy(self):
        # deploy(content)
        """
        deploy(content)
        content = * * * * * command
        """
        # test for passing invalid command
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_COMMAND_FORMAT_NOT_VALID):
            cronpi.deploy("* * * ")
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_COMMAND_FORMAT_NOT_VALID):
            cronpi.deploy("* * * * *  ")
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_COMMAND_FORMAT_NOT_VALID):
            cronpi.deploy("ac * * * * ls")
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_COMMAND_FORMAT_NOT_VALID):
            cronpi.deploy("* ac * * * ls")
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_COMMAND_FORMAT_NOT_VALID):
            cronpi.deploy("* * * ac * ls")
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_COMMAND_FORMAT_NOT_VALID):
            cronpi.deploy("* * * * ac ls")
        with self.assertRaisesRegex(ValueError, cronpi.validator.ERR_COMMAND_FORMAT_NOT_VALID):
            cronpi.deploy("* * *-* * * ls")

if __name__ == '__main__':
    unittest.main()