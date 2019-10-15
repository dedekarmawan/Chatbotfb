from flask import Flask, request, jsonify
import sys
import os
import json
import pymysql.cursors
from datetime import date

app = Flask(__name__)

@app.route('/', methods=['POST'])
def webhook():
    data = request.get_json()
    intent_name = data.get("queryResult").get("intent").get("displayName")
    inbox = data['queryResult']['queryText']
    print(data)
    connection = pymysql.connect(host='db4free.net',
                                 user='dedekarmawan',
                                 password='Superdede',
                                 db='snaptravelbot',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        #result = None
        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_inbox (pesan,date) VALUES (%s, %s)"
            cursor.execute(sql, (inbox, date.today().strftime("%Y-%m-%d")))
            idterakhir = cursor.lastrowid
            sql = "INSERT INTO tb_outbox(id_inbox, pesan, date) VALUES (%s, %s, %s)"
            cursor.execute(sql, (idterakhir, salam(data), date.today().strftime("%Y-%m-%d")))
        connection.commit()
    finally:
        connection.close()

    if intent_name == "salam":
        return salam(data)

            # result = cursor.fetchone()


    # return jsonify(request.get_json())

def salam(data):
    response = {
        'fulfillmentText':"Hai, saya Tutlesbot. Chatbot yang akan membantu anda dalam mencari hotel ketika anda berlibur. Ketik booking untuk memilih opsi kamar hotel."
    }

    return jsonify(response)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
