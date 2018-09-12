from sources.git_utils import GitUtils
from sources.pull_request_caller import *
import logging
from subprocess import CalledProcessError

# ======= Constant declaration =======
decodeFormat = "utf-8"
# ======= Dependencies declaration =======
gitUtils = GitUtils()


def pre_merge_phase(input_parameters: InputParameters, repo, repo_output):
    try:
        # TODO consider to do reset --hard, or check stage is clean
        gitUtils.execute_git_command(input_parameters.sourcesRoot, repo, "reset --hard ")
        gitUtils.execute_git_command(input_parameters.sourcesRoot, repo, "checkout " + input_parameters.baseBranch)
        gitUtils.execute_git_command(input_parameters.sourcesRoot, repo, "pull")

        logging.debug("Merging on " + repo + ". Switching to temporal branch " + input_parameters.temporalBranch)
        gitUtils.execute_git_command(input_parameters.sourcesRoot, repo, "checkout -b " + input_parameters.temporalBranch)
    except CalledProcessError as exc:
        output_string = exc.output.decode(decodeFormat)
        logging.debug(output_string)
        repo_output.append("ERROR: Error executing: " + exc.cmd + " ; " + output_string)


def merge_phase(input_parameters: InputParameters, repo, repo_output):
    try:
        if not repo_output:
            logging.info("Merging on " + repo + ". Merging from " + input_parameters.mergingBranch)
            output = gitUtils.execute_git_command(input_parameters.sourcesRoot, repo,
                                                "pull origin " + input_parameters.mergingBranch)
            logging.debug(output)
    except CalledProcessError as exc:
        output_string = exc.output.decode(decodeFormat)
        logging.debug(output_string)
        if "CONFLICT" in output_string:
            repo_output.append("CONFLICTS: The repository " + repo +
                               " has conflicts that will need to be resolved manually")
        else:
            repo_output.append("ERROR: Error executing: " + exc.cmd + " ; " + output_string)


def after_merge_phase(input_parameters: InputParameters, repo, repo_output):
    try:
        if not repo_output:
            gitUtils.execute_git_command(input_parameters.sourcesRoot, repo, " push --set-upstream origin " +
                                         input_parameters.temporalBranch)
    except CalledProcessError as exc:
        output_string = exc.output.decode(decodeFormat)
        logging.debug(output_string)
        repo_output.append("ERROR: Error executing: " + exc.cmd + " ; " + output_string)


def merge_branch(input_parameters: InputParameters, repo):
    pull_request_creator = PullRequestCreator()
    repo_output = []

    logging.info("Starting merging on " + repo)
    pre_merge_phase(input_parameters, repo, repo_output)
    merge_phase(input_parameters, repo, repo_output)
    after_merge_phase(input_parameters, repo, repo_output)
    if not repo_output:
        if not input_parameters.user or not input_parameters.password:
            repo_output.append(
                "The branch was pushed, but the user and password needs to be provided in order to create the pull "
                "requests")
        else:
            # TODO show the pull requests in the result
            pull_request_output = pull_request_creator.create_pull_request(input_parameters, repo)
            if pull_request_output:
                repo_output.append(pull_request_output)

    logging.info("Finished merging on " + repo + "; errors: " + str(repo_output))

    return repo_output
