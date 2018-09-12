import requests
import json
import logging
from input_parameters import InputParameters

# ======= Constant declaration =======
decodeFormat = "utf-8"
# ====================================


class PullRequestCreator(object):

    def create_json_request(self, parameters: InputParameters, repo):
        if repo.startswith("api/"):
            repo = repo[4:]

        reviewers_array = []
        for reviewer in parameters.reviewersNicknames:
            reviewers_array.append({
                "user": {
                    "name": reviewer
                }
            })

        output_json = {
            "title": "Merge from " + parameters.mergingBranch + " to " + parameters.baseBranch,
            "description": parameters.jiraTicket + " Merge from " + parameters.mergingBranch + " to " + parameters.baseBranch,
            "state": "OPEN",
            "open": True,
            "closed": False,
            "locked": False,
            "fromRef": {
                "id": "refs/heads/" + parameters.temporalBranch,
                "repository": {
                    "slug": repo,
                    "name": None,
                    "project": {
                        "key": parameters.teamFork
                    }
                }
            },
            "toRef": {
                "id": "refs/heads/" + parameters.baseBranch,
                "repository": {
                    "slug": repo,
                    "name": None,
                    "project": {
                        "key": parameters.mainFork
                    }
                }
            },
            "reviewers": reviewers_array
        }
        return output_json

    def create_pull_request(self, input_parameters: InputParameters, repo):
        if not input_parameters.user or not input_parameters.password:
            return "ERROR: The user and password needs to be provided in order to create the pull requests"
        else:
            logging.info("Creating pull request for " + repo)

            json_request = self.create_json_request(input_parameters, repo)

            url = input_parameters.server + "/rest/api/1.0/projects/" + input_parameters.mainFork + "/repos/" + repo + "/pull-requests"

            r = requests.post(url, json=json_request, auth=(input_parameters.user, input_parameters.password))
            if r.status_code != 200 and r.status_code != 201:
                return r.text
            else:
                logging.info("Pull request created for " + repo)
                # TODO return pull request link
                pr_url = json.loads(r.text)["links"]["self"][0]["href"]
                return pr_url
