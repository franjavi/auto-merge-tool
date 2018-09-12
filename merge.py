import logging
import getpass
from sources.validation import Validator
from sources.merge_processor import *
import sys

# ====== Manual variables ==============
logging.basicConfig(level=logging.INFO)
# ====================================
# ======= Constant declaration =======
possibleArguments = """   [-user=] the bitbucket user. If not provided the pull requests will not be created and the git calls will only work if using wincred
   [-password=] the bitbucket password. Use together with -user
   [-help] show help
"""
helpMessage = """This script helps to merge repositories.
It creates the temporal branches, and merges from the merging branch to the base branch.
Valid arguments:"""
# ====================================


def process_merge(parameters: InputParameters):
    validator = Validator()
    # TODO get parameters or populate here. Optional put the variables in another file
    # for arg in sys.argv[1:]:
    # TODO get origin and destination branch
    # TODO get temporal branch name
    # TODO get list of repos
    # TODO get team fork url
    # TODO validate we have all variables populated
    validator.validate_input_parameters(parameters)

    repo_output = validator.validate_repositories(parameters)

    # Discard the repositories with errors
    wrong_repos = list(repo_output.keys())
    logging.debug("Repositories with errors " + str(wrong_repos))
    ready_repos = list(filter(lambda r: r not in wrong_repos, parameters.repositories))
    logging.info("Repositories to merge " + str(ready_repos))
    for repo in ready_repos:
        output = merge_branch(parameters, repo)
        # Set to the error list merge branch issues, like conflicts, etc.
        repo_output[repo] = output

    return repo_output


def separate_argument(argument):
    return argument.split("=")[1].strip()


# Gets the arguments and sets them to InputParametes
def get_arguments():
    input_parameters = InputParameters()

    for arg in sys.argv[1:]:
        if arg.startswith("-user="):
            input_parameters.user = separate_argument(arg)
        elif arg.startswith("-password="):
            input_parameters.password = separate_argument(arg)
        elif arg == "help" or arg == "-help":
            print(helpMessage)
            print(possibleArguments)
            exit()
        else:
            print("INVALID ARGUMENT. Use:")
            print(possibleArguments)
            exit(-1)

    # Get the password from input if is not provided by arguments
    if input_parameters.user and not input_parameters.password:
        input_parameters.password = getpass.getpass("Provide Bitbucket password for the user:")

    return input_parameters


def main():
    logging.info("Starting process")

    input_parameters = get_arguments()

    try:
        repo_output = process_merge(input_parameters)

        print("\nRepositories output: ")
        for key, value in repo_output.items():
            print(key, ": ", value)
        print()
    except CalledProcessError as exc:
        if exc.output is not None:
            logging.error(exc.output.decode(GitUtils.decodeFormat))
        else:
            logging.error("Unexpected error executing git")

    logging.info("Finished process")


# ======= Starting logic point =======
# Execute main as starting point
if __name__ == "__main__":
    main()
