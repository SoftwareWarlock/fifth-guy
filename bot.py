from config import github, GH_USERNAME, GH_REPO

def issue_comment_created(issue_comment):
    comment_body = issue_comment["comment"]["body"]
    if comment_body.lower() == "lgtm":
        # trigger circle ci build

        issue_number = issue_comment["issue"]["number"]
        issue_comment_id = issue_comment["comment"]["id"]
        github.issues.comments.create(
            number=issue_number,
	    message="Running e2e test",
            user=GH_USERNAME,
            repo=GH_REPO)
