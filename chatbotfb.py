from flask import Flask, request, jsonify
import sys
import os
import json
import pymysql.cursors

app = Flask(__name__)


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


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
