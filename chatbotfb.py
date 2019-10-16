from flask import Flask, request, jsonify
import os
import json
import pymysql.cursors
from datetime import date

app = Flask(__name__)

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
    cekUserID = data.get("originalDetectIntentRequest").get("payload").get("from").get("id")
    idPesan = data.get("originalDetectIntentRequest").get("payload").get("message_id")
    isiPesan = data.get("originalDetectIntentRequest").get("payload").get("text")
    id_inbox = ""

    try:
        result = ""
        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_inbox (id_pesan, pesan, id_user, date) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (idPesan, isiPesan, cekUserID, date.today().strftime("%Y-%m-%d")))
        connection.commit()

    except Exception:
        response = {
            'fulfillmentText':"Hai, saya Tutlesbot. Chatbot yang akan membantu anda dalam mencari hotel ketika anda berlibur. Ketik booking untuk memilih opsi kamar hotel."
        }
        return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
