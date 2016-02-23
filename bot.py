from config import github, GH_USERNAME, GH_REPO, CIRCLE_TOKEN, GH_TOKEN
import requests


def get_circle_url(branch, token):
    return "https://circleci.com/api/v1/project/twoguysapp/pmcloud/tree/{branch}?circle-token={token}".format(
        branch=branch,
        token=token)


def get_github_merge_url(user, repo):
    return "https://api.github.com/repos/{user}/{repo}/merges"


def trigger_circle_ci_build(branch):
    circle_url = get_circle_url(branch, CIRCLE_TOKEN)
    circle_body = {
        "build_parameters": {
            "RUN_E2E_TESTS": True
        }
    }
    return requests.post(circle_url, json=circle_body)


def merge_master_into_branch(branch):
    merge_data = {
        "base": branch,
        "head": "master",
        "commit_message": "Merged master into " + branch
    }
    headers = {
        "Authorization": "Token %s" % GH_TOKEN
    }
    return requests.post(
        get_github_merge_url(GH_USERNAME, GH_REPO),
        json=merge_data,
        headers=headers)


def create_issue_comment(issue_comment, message):
    issue_number = issue_comment["issue"]["number"]
    issue_comment_id = issue_comment["comment"]["id"]
    github.issues.comments.create(
        number=issue_number,
        message=message,
        user=GH_USERNAME,
        repo=GH_REPO)


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

        if pull_request.mergeable:
            merge_response = merge_master_into_branch(branch)
            if merge_response.status == 409:
                create_issue_comment(issue_comment, "Automatic merge of master failed with conflicts")
            else if merge_response.status in [200, 204]:
                circle_response = trigger_circle_ci_build(branch)
                if circle_response.status == 201:
                    create_issue_comment(issue_comment, "Running e2e tests")
                else:
                    create_issue_comment(issue_comment, "Failed to run e2e tests")
            else:
                create_issue_comment(issue_comment, merge_response.json().get("message", "Unknown error occured"))
        else:
            create_issue_comment(issue_comment, "Look, you're gonna have to fix these merge conflicts before I can even do anything.")
