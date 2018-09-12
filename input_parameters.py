import os

class InputParameters(object):

    # ====== Manual editable variables ==============
    # REQUIRED: Comment out the repos to ignore
    repositories = [
        "repoA",
        "repoB"
    ]
    # REQUIRED: The branch from wich the temporal branch will be created
    baseBranch = "feature/branchName"
    # REQUIRED: The branch to pull over the base one
    mergingBranch = "franjavi/testAutoMerge"
    # REQUIRED: The JIRA ticket number: CP-XXXX
    jiraTicket = "CP-XXXXXX"
    # REQUIRED: The team fork bitbucket project ID. For example TEST, what you can get from
    # http://bitbucketServer/projects/TEST/
    # TODO get default from trucare
    teamFork = "TEST"
    # REQUIRED: A name following the conventions: nickname/CP-XXXXX
    # TODO create branch name from ticket number. For now is REQUIRED field
    temporalBranch = "aTempBranch"
    # OPTIONAL: The nicknames of the users to add as reviewers to the pull request
    reviewersNicknames = ["aUser"]
    # OPTIONAL: Code root, at the level where the main repo is. If not set the tool should be at the same level manually using this field
    sourcesRoot = ""
    # ====================================

    # ===== NOT Manual editable variables ==============
    # Fill these ones only by argument for security reasons
    # These credentials are the bitbucket credentials in order to create the pull requests
    user = ""
    password = ""
    # "http://server:port"
    server = "bitbucketServer" 
    # The main bitbucket project ID. For example TA, what you can get from http://bitbucketServer/projects/TA/
    mainFork = "TA"
    # ====================================

    def __init__(self):
        # Sets the same level directory by default, so the tool can be set at the same level and no need to specify
        # the sourcesRoot field
        if not self.sourcesRoot:
            parent_directory = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
            self.sourcesRoot = parent_directory + os.path.sep

        if not self.temporalBranch and self.user and self.teamFork and self.jiraTicket:
            self.temporalBranch = self.user + "/" + self.teamFork + "/" + self.jiraTicket

    def __str__(self):
        rep = "sourcesRoot: " + self.sourcesRoot + "\n"
        rep += "baseBranch: " + self.baseBranch + "\n"
        rep += "mergingBranch: " + self.mergingBranch + "\n"
        rep += "temporalBranch: " + self.temporalBranch + "\n"
        rep += "teamFork: " + self.teamFork + "\n"
        rep += "user: " + self.user + "\n"
        rep += "repositories: " + str(self.repositories)
        return rep
