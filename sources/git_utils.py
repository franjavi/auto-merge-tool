from subprocess import call
from subprocess import check_output
from subprocess import Popen
from subprocess import CalledProcessError, DEVNULL
import sys
import subprocess
import logging


class GitUtils(object):

    # ======= Constant declaration =======
    decodeFormat = "utf-8"
    subprocessNewShell = True
    # ====================================

    def execute_git_command_asynch(self, sources_root, repo, command):
        path = sources_root + repo
        logging.debug("Calling git: " + command + " ; on : " + path)
        # for the path use cwd Popen parameter or -C git paramenter
        p = Popen("git " + command, stdin=subprocess.PIPE, stderr=subprocess.STDOUT, shell=self.subprocessNewShell,
                  bufsize=4096, cwd=path)
        p.communicate()
        if p.returncode != 0:
            raise CalledProcessError(returncode=-1, cmd="", output=None)

    def execute_git_command(self, sources_root, repo, command):
        path = sources_root + repo
        logging.debug("Calling git: " + command + " ; on : " + path)
        try:
            # for the path use cwd Popen parameter or -C git paramenter
            cmd_output = check_output("git " + command, stderr=subprocess.STDOUT, shell=self.subprocessNewShell, cwd=path).decode(
                self.decodeFormat)
            logging.debug("Result of git: " + command + " ; on : " + path + " ; output: :" + cmd_output)
            return cmd_output
        except CalledProcessError as exc:
            if exc.output is not None:
                logging.debug(exc.output.decode(self.decodeFormat))
            raise exc
