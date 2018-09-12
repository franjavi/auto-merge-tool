import re
from sources.git_utils import GitUtils
from input_parameters import InputParameters
import logging
import sys


class Validator(object):
    gitUtils = GitUtils()

    @staticmethod
    def is_value_in_branches(multiline: str, value):
        for line in multiline.splitlines():
            if line.endswith(value):
                return True
        return False

    def validate_input_parameters(self, input_parameters: InputParameters):
        # TA remote is not valid
        if input_parameters.teamFork == "TA":
            print("ERROR: The TA repository (http://X@bitbucket-server/scm/ta) is not allowed",
                  file=sys.stderr)
            input_parameters.teamFork = ""

    # Check that the origin remote is not pointing to TA
    def validate_remotes(self, sources_root, repo, errors):
        output = self.gitUtils.execute_git_command(sources_root, repo, "remote -v")

        for line in output.splitlines():
            pattern = re.compile(r"^origin *.*://([^/]+)/scm/ta/")
            if pattern.match(line):
                errors.append(
                    "ERROR: The TA repository (http://X@bitbucket-server/scm/ta) is not allowed in " + repo)
        return errors

    # TODO validate all the repos are the same as inputParamters.teamFork

    # Validates that the repositories are in a ready state to be able to merge
    # Checks that the branches exists, the temporal branch not, and that is poiting to the right team fork
    def validate_repositories(self, parameters: InputParameters):
        logging.info("Starting the validation of repositories \n" + parameters.__str__())
        repo_output = {}

        for repo in parameters.repositories:
            errors_in_repo = []
            # TODO if repo do not exist create/clone
            # validate the remote is not TA
            self.validate_remotes(parameters.sourcesRoot, repo, errors_in_repo)

            # validate origin/destination branch exists
            # validate temporal branch does not exist already
            self.gitUtils.execute_git_command(parameters.sourcesRoot, repo, "fetch")
            output = self.gitUtils.execute_git_command(parameters.sourcesRoot, repo, "branch -a")

            if not Validator.is_value_in_branches(output, "remotes/origin/" + parameters.baseBranch):
                errors_in_repo.append("ERROR: Base branch " + parameters.baseBranch + " not found in " + repo)
            if not Validator.is_value_in_branches(output, "remotes/origin/" + parameters.mergingBranch):
                errors_in_repo.append("ERROR: Merging branch " + parameters.mergingBranch + " not found in " + repo)
            if Validator.is_value_in_branches(output, parameters.temporalBranch):
                errors_in_repo.append("ERROR: The temporal branch " + parameters.temporalBranch +
                                      " already exists in " + repo)

            if errors_in_repo:
                repo_output[repo] = errors_in_repo
            logging.debug("Repository " + repo + " errors " + errors_in_repo.__str__())

        return repo_output
