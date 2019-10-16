# import flask dependencies
from flask import Flask, request, jsonify
import os
import pymysql.cursors
import json
from datetime import date

# initialize the flask app
app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))
connection = pymysql.connect(host='db4free.net',
                             user='dedekarmawan',
                             password='Superdede',
                             db='snaptravelbot',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


# create a route for webhook
@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    intent_name = data.get("queryResult").get("intent").get("displayName")
    print(data)

    if intent_name == "salam":
        return salam(data)

    return jsonify(request.get_json())

def salam(data):
    id_user = data.get("originalDetectIntentRequest").get("payload").get("from").get("id")
    id_pesan = data.get("originalDetectIntentRequest").get("payload").get("message_id")
    pesan = data.get("originalDetectIntentRequest").get("payload").get("text")
    id_inbox = ""

    try:
        result = ""
        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_inbox (id_pesan, pesan, id_user, date) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (id_pesan, pesan, id_user, date.today().strftime("%Y-%m-%d")))
        connection.commit()

        response = {
            'fulfillmentMessages': [
                {
                    "card": {
                        "title": "Menu",
                        "subtitle": "Halo {}, Silahkan pilih menu di bawah",
                        "buttons": [
                            {
                                "text": "Cek Profil",
                                "postback": "cek profil"
                            },
                            {
                                "text": "Info Akademik",
                                "postback": "info akademik"
                            }
                        ]
                    }
                }
            ]
        }
        return response

    except Exception:
        response = {
            'fulfillmentText':"Hai, saya Tutlesbot. Chatbot yang akan membantu anda dalam mencari hotel ketika anda berlibur. Ketik booking untuk memilih opsi kamar hotel."
        }
        return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
