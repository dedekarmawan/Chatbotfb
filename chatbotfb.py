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
    elif intent_name == "HotelMenu":
        return hotel_menu(data)
    elif intent_name == "cekKamarReady":
        return cek_kamar_ready(data)
    elif intent_name == "cekTipeKamar":
        return cek_tipe_kamar(data)
    elif intent_name == "bookingKamar":
        return booking_kamar(data)

    return jsonify(request.get_json())


def salam(data):
    id_user = data.get("originalDetectIntentRequest").get("payload").get("data").get("sender").get("id")
    id_pesan = data.get("originalDetectIntentRequest").get("payload").get("data").get("message").get("mid")
    pesan = data.get("originalDetectIntentRequest").get("payload").get("data").get("message").get("text")
    id_inbox = ""
    respon = "Hai, saya Tutlesbot. Chatbot yang akan membantu anda dalam mencari hotel ketika anda " \
             "berlibur. Ketik booking untuk memilih opsi kamar hotel."

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_inbox (id_pesan, pesan, id_user, date) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (id_pesan, pesan, id_user, date.today().strftime("%Y-%m-%d")))
            id_inbox = cursor.lastrowid
        connection.commit()

        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_outbox (id_inbox, respon) VALUES (%s, %s)"
            cursor.execute(sql, (id_inbox, respon))
            sql = "UPDATE tb_inbox SET tb_inbox.status = '1' WHERE tb_inbox.id = %s"
            cursor.execute(sql, (id_inbox))
        connection.commit()

        response = {
            'fulfillmentText': respon
        }

        return jsonify(response)
    except Exception as error:
        print(error)


def hotel_menu(data):
    id_user = data.get("originalDetectIntentRequest").get("payload").get("data").get("sender").get("id")
    id_pesan = data.get("originalDetectIntentRequest").get("payload").get("data").get("message").get("mid")
    pesan = data.get("originalDetectIntentRequest").get("payload").get("data").get("message").get("text")
    id_inbox = ""
    respon = "Tutlesbot akan membantu anda dalam menentukan pilihan kamar yang sesuai dengan keinginan anda. " \
             "Pilih salah satu opsi dibawah ini.\n1. Cek tipe kamar\n2. Cek kamar yang tersedia\n3. Pesan kamar"

    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_inbox (id_pesan, pesan, id_user, date) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (id_pesan, pesan, id_user, date.today().strftime("%Y-%m-%d")))
            id_inbox = cursor.lastrowid
        connection.commit()

        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_outbox (id_inbox, respon) VALUES (%s, %s)"
            cursor.execute(sql, (id_inbox, respon))
            sql = "UPDATE tb_inbox SET tb_inbox.status = '1' WHERE tb_inbox.id = %s"
            cursor.execute(sql, (id_inbox))
        connection.commit()

        response = {
            'fulfillmentText': respon
        }

        return jsonify(response)
    except Exception as error:
        print(error)


def cek_kamar_ready(data):
    print(data)


def cek_tipe_kamar(data):
    id_user = data.get("originalDetectIntentRequest").get("payload").get("data").get("sender").get("id")
    id_pesan = data.get("originalDetectIntentRequest").get("payload").get("data").get("message").get("mid")
    pesan = data.get("originalDetectIntentRequest").get("payload").get("data").get("message").get("text")
    id_inbox = ""
    print("cek_tipe_kamar")
    try:
        result = None

        with connection.cursor() as cursor:
            sql = "SELECT * FROM tb_tipe_kamar"
            cursor.execute(sql)
            result = cursor.fetchall()

        with connection.cursor() as cursor:
            sql = "INSERT INTO tb_inbox (id_pesan, pesan, id_user, date) VALUES (%s, %s, %s, %s)"
            cursor.execute(sql, (id_pesan, pesan, id_user, date.today().strftime("%Y-%m-%d")))
            id_inbox = cursor.lastrowid
        connection.commit()

        with connection.cursor() as cursor:
            for tipe_kamar in result:
                sql = "INSERT INTO tb_outbox (id_inbox, respon) VALUES (%s, %s)"
                cursor.execute(sql, (id_inbox, tipe_kamar['id_tipe_kamar']))
            sql = "UPDATE tb_inbox SET tb_inbox.status = '1' WHERE tb_inbox.id = %s"
            cursor.execute(sql, (id_inbox))
        connection.commit()

        fulfillmentText = ""

        for tipe_kamar in result:
            fulfillmentText += "Tipe Kamar: {}\nHarga: {}\n\n".format(tipe_kamar['size_kamar'],
                                                                      str(tipe_kamar['harga']))

        fulfillmentText += "Pilih salah satu opsi dibawah ini.\n" \
                           "1. Cek harga sewa kamar\n2. Cek kamar yang tersedia\n3. Pesan kamar"
        return jsonify({'fulfillmentText': fulfillmentText})
    except Exception as error:
        print(error)


def booking_kamar(data):
    print(data)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=port)
