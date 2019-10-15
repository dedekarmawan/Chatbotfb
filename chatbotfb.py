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
    inbox = data['queryResult']['queryText']
    print(data)

    if intent_name == "salam":
        return salam(data)
    elif intent_name == "booking":
        return booking(data)

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_inbox (pesan,date) VALUES (%s, %s)"
            cursor.execute(sql, (inbox, date.today().strftime("%Y-%m-%d")))
            idterakhir = cursor.lastrowid
            sql = "INSERT INTO tb_outbox(id_inbox, pesan, date) VALUES (%s, %s, %s)"
            cursor.execute(sql, (idterakhir, salam(data), date.today().strftime("%Y-%m-%d")))
        connection.commit()

    finally:
           connection.close()

    # return jsonify(request.get_json())

def salam(data):
    response = {
        'fulfillmentText':"Hai, saya Tutlesbot. Chatbot yang akan membantu anda dalam mencari hotel ketika anda berlibur. Ketik booking untuk memilih opsi kamar hotel."
    }

    return jsonify(response)

def booking(data):
    respon = {
        'fulfillmentText':"Tutlesbot akan membantu anda dalam menentukan pilihan kamar yang sesuai dengan keinginan anda. Pilih salah satu opsi dibawah ini.1. Cek harga sewa kamar2. Cek kamar yang tersedia3. Pesan kamar"
    }

    return  jsonify(respon)


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
