from flask_restful import request, url_for, fields, marshal_with, reqparse, Resource
import requests

from ..api import api

post_parser = reqparse.RequestParser()


class Mail(Resource):
    def post(self):
        grata = request.form['grata']
        contact = request.form['contact']
        name = request.form['name']
        num = request.form['num']
        text = request.form['text']
        try:
            if int(grata) != int(num):
                return {"result": False,
                        "text": "Вы неправильно ввели число проверки на человечность, напишите  пожалуйста админу info@it-anthill.ru"}
        except:
            return {"result": False,
                    "text": "Вы неправильно ввели число проверки на человечность, напишите пожалуйста админу info@it-anthill.ru"}

        send_message = "Сообщение от:\n%s\nТелефон:\n%s\nСообщение:\n%s" % (name, contact, text)
        url_chat = "https://api.telegram.org/bot666520047:AAGdxJqhsqYakM9kFgvR9DX9Xx9QZDlonoY/sendMessage?chat_id=-1001228931701&text="
        proxies = {
            'http': 'http://suka:vneq9t4DSW3d@205.204.87.15:1490',
            'https': 'https://suka:vneq9t4DSW3d@205.204.87.15:1490'
        }
        try:
            requests.get(url_chat + send_message, proxies=proxies, timeout=10)
        except Exception as e:
            print("Что то пошло не так ам43енп4ацуйв")
            return {"result": False, "text": "Что то пошло на сайте напишите пожалуйста админу: info@it-anthill.ru"}
        return {"result": True, "text": "Good_job"}


api.add_resource(Mail, '/mail')
