from config import GH_SECRET_TOKEN, PROD
import bot

from flask import Flask, request, url_for
import hmac
from hashlib import sha1


app = Flask(__name__)


def calculate_hmac(payload):
    hashed = hmac.new(GH_SECRET_TOKEN, payload, sha1)
    return "sha1=" + hashed.hexdigest()


def check_hmac(request):
    request_body = request.data
    expected_hmac = calculate_hmac(request_body)
    print expected_hmac
    request_hmac = request.headers.get("X-Hub-Signature")
    print request_hmac
    return expected_hmac == request_hmac


@app.route('/comment-webhook', methods=["POST"])
def issue_comment_webhook():
    print "Recieved webhook call"
    if check_hmac(request):
        issue_comment = request.get_json()
        bot.issue_comment_created(issue_comment)
	print "Webhook success"
        return "Success"
    print "Webhook failure"
    return "Failure"


if __name__ == "__main__":
    debug = not PROD
    app.run(host='0.0.0.0', debug=debug)
