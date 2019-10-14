from flask import Flask, request, jsonify
import sys
import os
import json
import pymysql.cursors

app = Flask(__name__)

# @app.route('/', methods=['POST'])
# def handle_verification():
#     if request.args.get('hub.verify_token', '') == VERIFY_TOKEN:
#         return request.args.get('hub.challenge', 200)
#     else:
#         return 'Error, wrong validation token'


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    intent_name = data.get("queryResult").get("intent").get("displayName")
    print(data)

    if intent_name == "salam":
        return salam(data)


    return jsonify(request.get_json())

def salam(data):
    response = {
        'fulfillmentText':"Hai, saya Tutlesbot. Chatbot yang akan membantu anda dalam mencari hotel ketika anda berlibur. Ketik booking untuk memilih opsi kamar hotel."
    }

    return jsonify(response)


# def send_message(recipient_id, message_text):
#     log("sending message to {recipient}: {text}".format(recipient=recipient_id, text=message_text))
#
#     params = {
#         "access_token": PAGE_ACCESS_TOKEN
#     }
#     headers = {
#         "Content-Type": "application/json"
#     }
#     data = json.dumps({
#         "recipient": {
#             "id": recipient_id
#         },
#         "message": {
#             "text": message_text
#         }
#     })
#     r = requests.post("https://graph.facebook.com/v2.6/me/messages", params=params, headers=headers, data=data)
#     if r.status_code != 200:
#         log(r.status_code)
#     log(r.text)


# def log(message):  # simple wrapper for logging to stdout on heroku
#     print(str(message))
#     sys.stdout.flush()


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
