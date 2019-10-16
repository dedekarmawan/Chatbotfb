from flask import Flask, request, jsonify
import os
import pymysql.cursors
import json
from datetime import date

app = Flask(__name__)
port = int(os.environ.get("PORT", 5000))
connection = pymysql.connect(host='db4free.net',
                             user='dedekarmawan',
                             password='Superdede',
                             db='snaptravelbot',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    intent_name = data.get("queryResult").get("intent").get("displayName")
    print(data)

    if intent_name == "salam":
        return salam(data)

    return jsonify(request.get_json())

def salam(data):
    id_user = data.get("originalDetectIntentRequest").get("payload").get("data").get("sender").get("id")
    id_pesan = data.get("originalDetectIntentRequest").get("payload").get("data").get("message").get("mid")
    pesan = data.get("originalDetectIntentRequest").get("payload").get("data").get("message").get("text")
    id_inbox = ""

    response = {
        'fulfillmentText': "Hai, saya Tutlesbot. Chatbot yang akan membantu anda dalam mencari hotel ketika anda berlibur. Ketik booking untuk memilih opsi kamar hotel."
    }

    with connection.cursor() as cursor:
        sql = "INSERT INTO tb_inbox (id_pesan, pesan, id_user, date) VALUES (%s, %s, %s, %s)"
        cursor.execute(sql, (id_pesan, pesan, id_user, date.today().strftime("%Y-%m-%d")))
        id_inbox = cursor.lastrowid
    connection.commit()

    # with connection.cursor() as cursor:
    #     sql = "INSERT INTO tb_outbox (id_inbox, respon) VALUES (%s, %s)"
    #     cursor.execute(sql, (id_inbox, "Hai, saya Tutlesbot. Chatbot yang akan membantu anda dalam mencari hotel ketika anda berlibur. Ketik booking untuk memilih opsi kamar hotel."))
    #     sql = "UPDATE tb_inbox SET tb_inbox.status = 1 WHERE tb_inbox.id = %s"
    #     cursor.execute(sql, (id_inbox))
    # connection.commit()

    return jsonify(response)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
