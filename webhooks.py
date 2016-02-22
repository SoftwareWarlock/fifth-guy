from config import GH_SECRET_TOKEN, PROD
import bot

from flask import Flask, request, url_for
import hmac
from hashlib import sha1


app = Flask(__name__)


def calculate_hmac(payload):
    hashed = hmac.new(GH_SECRET_TOKEN, payload, sha1)
    return hashed.hexdigest().encode("base64").rstrip('\n')


def check_hmac(request):
    request_body = request.data
    print request_body
    expected_hmac = calculate_hmac(request_body)
    print expected_hmac
    request_hmac = request.headers.get("X-Hub-Signature")
    print request_hmac
    return expected_hmac == request_hmac


@app.route('/comment-webhook', methods=["POST"])
def pull_request_comment_webhook():
    print "Recieved webhook call"
    if check_hmac(request):
        pull_request_comment = request.get_json()
        bot.pull_request_comment_created(pull_request_comment)
	print "Webhook success"
        return "Success"
    print "Webhook failure"
    return "Failure"


if __name__ == "__main__":
    debug = not PROD
    app.run(host='0.0.0.0', debug=debug)
