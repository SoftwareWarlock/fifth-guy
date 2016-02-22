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
	pull_request_number = pull_request_user.split("/")[-1]
    	pull_request = github.pull_requests.get(
	    number=pull_request_number,
	    user=GH_USERNAME,
	    repo=GH_REPO)
	branch = pull_request["head"]["ref"]
	print branch
	circle_url = get_circle_url(branch, CIRCLE_TOKEN)
	circle_response = requests.post(circle_url)

	if circle_response.status == 201:
	    issue_number = issue_comment["issue"]["number"]
	    issue_comment_id = issue_comment["comment"]["id"]
	    github.issues.comments.create(
	        number=issue_number,
	        message="Running e2e test",
	        user=GH_USERNAME,
	        repo=GH_REPO)
