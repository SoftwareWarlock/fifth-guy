from config import github, GH_USERNAME, GH_REPO

def pull_request_comment_created(pull_request_comment):
    comment_body = pull_request_comment["comment"]["body"]
    if comment_body.lower() == "lgtm":
        # trigger circle ci build

        pull_request_number = pull_request_comment["pull_request"]["number"]
        pull_request_comment_id = pull_request_comment["comment"]["id"]
        comment_data = {
            "body": "Running e2e tests",
            "in_reply_to": pull_request_comment_id
        }
        github.pull_requests.comments.create(
            number=pull_request_number,
            data=comment_data,
            user=GH_USERNAME,
            repo=GH_REPO)
