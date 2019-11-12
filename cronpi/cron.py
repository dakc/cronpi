import os
import subprocess

from cronpi.validator import validate_crontab_content

CMD_INDEX = 5

def deploy(content, isOverwrite):
    """
    Install crontab into a system if it's not installed.
    If the cron with same command exists, then it will update that.
    Raises value error if the content is not in correct format.

    Parameters
    ----------
    content: string
        single crontab content

    isOverwrite: bool
        If True and cmd already exists as cronjob,
        it will overwrite with the new date and time.
        Otherwise, it will insert as new cron job.
        Default value is False.

    Usage
    ----------
    1. Run at every minutes (always inserts new job)
    cronpi.deploy("* * * * * ls -al /opt")

    2. Run at every minutes ( if not found, inserts as new job else updates.)
    cronpi.deploy("* * * * * ls -al /opt", isOverwrite=True)
    """
    # validate conntent
    validate_crontab_content(content)
    # update crontab
    new_content = _get_updated_content(content, isOverwrite)
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
    if len(split_command) >= CMD_INDEX:
        for i in range(CMD_INDEX, len(split_command)):
            cmd += split_command[i].strip()
    return cmd


def _get_updated_content(content, isOverwrite):
    """
    Get the content of crontab after updating the command got recently

    Parameters
    ----------
    content: string
        crontab content got recently

    isOverwrite: bool
        If True and cmd already exists as cronjob,
        it will overwrite with the new date and time.
        Otherwise, it will insert as new cron job.
        Default value is False.

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
        if isOverwrite and _get_command_from_cron(installed_crontab) == cmd:
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