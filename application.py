
import telebot
import os
from telebot import types
from flask import Flask, request
from textmsg import adminmsg, startmsg, buymsg, demomsg,
import random
import re

token=''

server = Flask(__name__)


bot = telebot.TeleBot(token)

keyboard = types.ReplyKeyboardMarkup(row_width=2)
buttonAdmin = types.KeyboardButton("Админ")
buttonBuy = types.KeyboardButton("Купить")
buttonDemo = types.KeyboardButton("Получить пробник")
buttonHelp = types.KeyboardButton("Помощь")

keyboard.add(buttonAdmin,buttonBuy,buttonDemo,buttonHelp)


@bot.message_handler(commands=['start'])
def start(message):
	bot.send_message(message.chat.id, startmsg, parse_mode='HTML', reply_markup=keyboard)

@bot.message_handler(lambda message: message.text == "Админ")
	def admin(message):
		bot.send_message(message.chat.id, adminmsg, parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(lambda message: message.text == "Купить")
	def admin(message):
		bot.send_message(message.chat.id, buymsg, parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(lambda message: message.text == "Получить пробник")
	def admin(message):
		bot.send_message(message.chat.id, demomsg, parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())

@bot.message_handler(lambda message: message.text == "Помощь")
	def admin(message):
		bot.send_message(message.chat.id, helpmsg2, parse_mode='HTML', reply_markup=types.ReplyKeyboardRemove())


@bot.message_handler(commands=['help'])
def help(message):
	msg = bot.send_message(message.chat.id, helpmsg)
	bot.register_next_step_handler(msg, start)


@bot.message_handler(regexp="^/check")
def wait(message):
	bot.send_message(message.chat.id, u'\U0000231B'+ '<b>Ожидание поступления платежа...</b>')



@server.route('/' + token, methods=['POST'])
def get_message():
	bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
	return "POST", 200

#@bot.message_handler(func=lambda message: True, content_types=['text'])
#def echo_message(message):
#    bot.send_message(message.chat.id, message.text)

@server.route('/')
def web_hook():
	bot.remove_webhook()
	bot.set_webhook(url='https://buyer69.herokuapp.com/'+token)
	return "CONNECTED", 200

server.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
