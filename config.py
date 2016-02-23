import os
from pygithub3 import Github

GH_USERNAME = os.getenv("GH_USERNAME", None)
GH_TOKEN = os.getenv("GH_TOKEN", None)
GH_REPO = os.getenv("GH_REPO", "fifth-guy")
GH_SECRET_TOKEN = os.getenv("GH_SECRET_TOKEN", None)
CIRCLE_TOKEN = os.getenv("CIRCLE_TOKEN", None)

assert GH_USERNAME is not None, "You must set the GH_USERNAME env var"
assert GH_TOKEN is not None, "You must set the GH_TOKEN env var"
assert GH_REPO is not None, "You must set the GH_REPO env var"
assert GH_SECRET_TOKEN is not None, "You must set the GH_SECRET_TOKEN env var"
assert CIRCLE_TOKEN is not None, "You must set the CIRCLE_TOKEN env var"

PROD = os.getenv("PROD", False)

github = Github(user=GH_USERNAME,
                token=GH_TOKEN,
                repo=GH_REPO)


def create_github_webhook(url):
    print "creating webhook"
    hook_data = {
        "name": "web",
        "active": True,
        "config": {
            "content_type": "json",
            "secret": GH_SECRET_TOKEN,
            "insecure_ssl": "1",
            "url": url
        },
        "events": ["issue_comment", ]
    }

    return github.repos.hooks.create(
        data=hook_data,
        user=GH_USERNAME,
        repo=GH_REPO)
