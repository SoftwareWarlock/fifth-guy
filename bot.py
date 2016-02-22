from config import github, GH_USERNAME, GH_REPO, CIRCLE_TOKEN
import requests


def get_circle_url(branch, token):
    return "https://circleci.com/api/v1/project/twoguysapp/pmcloud/tree/{branch}?circle-token={token}".format(
        branch=branch,
	token=token)


def issue_comment_created(issue_comment):
    comment_body = issue_comment["comment"]["body"]
    if comment_body.lower() == "lgtm":
        pull_request_url = issue_comment["issue"]["pull_request"]["url"]
	pull_request_number = pull_request_url.split("/")[-1]
    	pull_request = github.pull_requests.get(
	    number=pull_request_number,
	    user=GH_USERNAME,
	    repo=GH_REPO)
	branch = pull_request.head["ref"]
	circle_url = get_circle_url(branch, CIRCLE_TOKEN)
	circle_body = {
	    "build_parameters": {
	    	"RUN_E2E_TESTS": True
	    }
	}
	circle_response = requests.post(circle_url, data=circle_body)

        issue_number = issue_comment["issue"]["number"]
        issue_comment_id = issue_comment["comment"]["id"]
        github.issues.comments.create(
	    number=issue_number,
	    message="Running e2e tests",
	    user=GH_USERNAME,
	    repo=GH_REPO)
