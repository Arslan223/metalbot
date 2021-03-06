#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import requests
global mutakabot


debug_mode = False
NUMBER_OF_VOTES = 1

import telebot, json, time
from datetime import datetime
# print(datetime.tzinfo)
bot = telebot.TeleBot(TOKEN)

if debug_mode:
	import logging

	logger = telebot.logger
	telebot.logger.setLevel(logging.DEBUG)
global timeStamp
timeStamp = "%H:%M %d.%m.%Y"
global tstam

tstam = "%H"
tstamd = "%d"
class Group():
	def __init__(self, participants = {}, url_of_channel = None, c_id = None, mutelist = [], gm = False):
		self.participants = participants
		self.url_of_channel = url_of_channel
		self.c_id = c_id
		self.mutelist = mutelist
		self.gm = gm

class Human():
	def __init__(self, discipline = None, adding_name = False, adding_description = False, adding_arguments = False, adding_time = False, adding_ok = False, giving_args = False, tasks = {}):
		self.discipline = discipline
		self.adding_name = adding_name
		self.adding_description = adding_description
		self.adding_arguments = adding_arguments
		self.adding_time = adding_time
		self.adding_ok = adding_ok
		self.giving_args = giving_args
		self.tasks = tasks

class GroupsEncoder(json.JSONEncoder):
	def default(self, obj):
		if isinstance(obj, Group):
			return obj.__dict__
		elif isinstance(obj, Human):
			return obj.__dict__
		elif isinstance(obj, telebot.types.Chat):
			return obj.__dict__
		elif isinstance(obj, telebot.types.User):
			return obj.__dict__
		elif isinstance(obj, telebot.types.Message):
			return obj.__dict__
		elif isinstance(obj, datetime):
			return obj.__dict__

		return json.JSONEncoder.default(self, obj)
'log_in'



def chstr(mutakabot, strmut, strob):
	return strmut if mutakabot else strob

def addowdo(message):
	return not(str(message.chat.id) in load().keys()) and isGroup(message.chat.type)

def nowtime():
	temp = int(datetime.today().strftime(tstam))+3
	if temp > 23:
		temp -= 24
		return (datetime.today()).replace(hour=temp, day=int(datetime.today().strftime(tstamd))+1)
	return (datetime.today()).replace(hour=temp)

def safe_show(array, index):
	return array[index] if index < len(array) else None

def isGroup(obj):
	return obj == 'group' or obj == 'supergroup'

def load():
	with open('data.json', 'r') as fp:
		return json.load(fp)

def update(obj):
	with open('data.json', 'w') as fp:
		json.dump(obj, fp, cls=GroupsEncoder)

def isaddingname(user_id):
	data = load()
	for i in data:
		group = data[i]
		if str(user_id) in Group(**group[1]).participants:
			if Human(**Group(**group[1]).participants[str(user_id)][1]).adding_name:
				return group
	return False

def isaddingdescription(user_id):
	data = load()
	for i in data:
		group = data[i]
		if str(user_id) in Group(**group[1]).participants:
			if Human(**Group(**group[1]).participants[str(user_id)][1]).adding_description:
				return group
	return False

def isaddingarguments(user_id):
	data = load()
	for i in data:
		group = data[i]
		if str(user_id) in Group(**group[1]).participants:
			if Human(**Group(**group[1]).participants[str(user_id)][1]).adding_arguments:
				return group
	return False

def isaddingtime(user_id):
	data = load()
	for i in data:
		group = data[i]
		if str(user_id) in Group(**group[1]).participants:
			if Human(**Group(**group[1]).participants[str(user_id)][1]).adding_time:
				return group
	return False

def isaddingok(user_id):
	data = load()
	for i in data:
		group = data[i]
		if str(user_id) in Group(**group[1]).participants:
			if Human(**Group(**group[1]).participants[str(user_id)][1]).adding_ok:
				return group
	return False

def isgivingargs(user_id):
	data = load()
	for i in data:
		group = data[i]
		if str(user_id) in Group(**group[1]).participants:
			if Human(**Group(**group[1]).participants[str(user_id)][1]).giving_args:
				print("YES")
				return group
	return False

def canUnMute():
	data = load()
	for i in data:
		for j in Group(**data[i][1]).participants:
			data = load()
			user = Group(**data[i][1]).participants[j]
			if Human(**user[1]).discipline:
				if nowtime() >= datetime.strptime(Human(**user[1]).discipline, timeStamp):
					data[i][1]['participants'][j][1]['discipline'] = None
					data[i][1]['mutelist'].remove(str(telebot.types.User(**Group(**data[i][1]).participants[j][0]).id))
					bot.send_message(f"{str(telebot.types.User(**Group(**data[i][1]).participants[j][0]).id)}", chstr(Group(**data[i][1]).gm, "Ты свободен, брат!\nТеперь вех!а отсюда", "Наказание закончено!"))
					update(data)

def canUnPost():
	data = load()
	for i in data:
		for j in Group(**data[i][1]).participants:
			for l in Group(**data[i][1]).participants[j][1]['tasks']:
				if len(Group(**data[i][1]).participants[j][1]['tasks'][l]) == 4:
					if datetime.strptime(Group(**data[i][1]).participants[j][1]['tasks'][l][3], timeStamp):
						if datetime.strptime(Group(**data[i][1]).participants[j][1]['tasks'][l][3], timeStamp) < nowtime():
							data = load()
							data[i][1]['participants'][j][1]['tasks'].pop(l)
							ts = "%d"
							data[i][1]['participants'][j][1]['discipline'] = (nowtime()).replace(day=int(nowtime().strftime(ts))+1).strftime(timeStamp)
							data[i][1]['mutelist'].append(j)
							bot.send_message(f"{str(telebot.types.User(**Group(**data[i][1]).participants[j][0]).id)}", chstr(Group(**data[i][1]).gm, "Задача не выполнена в заданный срок.\nТакой ты камень", "Задача не выполнена в заданный срок."))
							bot.send_message(data[i][0]['id'], chstr(Group(**data[i][1]).gm, f"{str(Group(**data[i][1]).participants[j][0]['first_name'])} не выполнил задачу в заданный срок.\nТакой он камень❌", f"{str(Group(**data[i][1]).participants[j][0]['first_name'])} не выполнил задачу в заданный срок❌"))
							bot.send_message(Group(**data[i][1]).c_id, chstr(Group(**data[i][1]).gm, f"{str(Group(**data[i][1]).participants[j][0]['first_name'])} не выполнил задачу в заданный срок.\nТакой он камень❌", f"{str(Group(**data[i][1]).participants[j][0]['first_name'])} не выполнил задачу в заданный срок❌"))
							update(data)
							showPanelManualy(str(telebot.types.User(**Group(**data[i][1]).participants[j][0]).id), str(telebot.types.User(**Group(**data[i][1]).participants[j][0]).id), str(data[i][0].id))
					

def makeVoting(photomess, group, taskkey, channel_id):
	fileid = photomess.photo[0].file_id
	userid = str(photomess.from_user.id)
	data = load()
	markup = telebot.types.InlineKeyboardMarkup()
	btn1 = telebot.types.InlineKeyboardButton("👍", callback_data=f"vyes&{str(telebot.types.Chat(**group[0]).id)}&{userid}&{taskkey}")
	btn2 = telebot.types.InlineKeyboardButton("👎", callback_data=f"vno&{str(telebot.types.Chat(**group[0]).id)}&{userid}&{taskkey}&{str(photomess.chat.id)}")
	markup.row(btn1, btn2)
	task = Group(**group[1]).participants[userid][1]['tasks'][taskkey]
	string = f"*{task[0]}*\n_{task[1]}_\n\n*Формат доказательства:*\n{task[2]}"
	data[str(telebot.types.Chat(**group[0]).id)][1]['participants'][userid][1]['tasks'][taskkey].append([[], []])
	update(data)
	bot.send_photo(Group(**group[1]).c_id, fileid, caption=string, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(func=lambda message: addowdo(message))
def addGroup(message):
	print(1)
	data = load()
	data.update({str(message.chat.id):[message.chat, Group(), None]})
	update(data)
	ch = False

@bot.message_handler(content_types=['photo'], func=lambda message: not(isGroup(message.chat.type)) and isgivingargs(str(message.from_user.id))!=False)
def getargss(message):
	print("THERE")
	data = load()
	group = isgivingargs(message.from_user.id)
	user = telebot.types.User(**(Group(**group[1]).participants[str(message.from_user.id)][0]))
	taskkey = data[str(telebot.types.Chat(**group[0]).id)][1]['participants'][str(user.id)][1]['giving_args']
	channel_id = Group(**group[1]).c_id
	bot.reply_to(message, chstr(group[1]['gm'], "гей", "принято"))
	makeVoting(message, group, taskkey, channel_id)
	showPanelManualy(str(message.chat.id), str(message.from_user.id), str(telebot.types.Chat(**group[0]).id))




def showPanelManualy(messagechatid, messagefrom_userid, chat_id):
	data = load()
	chat_id = str(chat_id)
	userdata = Group(**data[chat_id][1]).participants[str(messagefrom_userid)]
	markup = telebot.types.InlineKeyboardMarkup()
	btn1 = telebot.types.InlineKeyboardButton("Добавить задачу", callback_data="addtask"+chat_id)
	btn2 = telebot.types.InlineKeyboardButton("Мои задачи", callback_data="showtasks"+chat_id)
	btn3 = telebot.types.InlineKeyboardButton("Открыть канал", url=f"t.me/{Group(**data[chat_id][1]).url_of_channel[1:]}")
	markup.row(btn1)
	markup.row(btn2)
	markup.row(btn3)
	string = chstr(Group(**data[chat_id][1]).gm, f"Ассаламу алейкум ва рахматулахи тааля ва баракату, брат {telebot.types.User(**userdata[0]).first_name}!\n", f"Здравствуйте, {telebot.types.User(**userdata[0]).first_name}!\n")
	string+=chstr(Group(**data[chat_id][1]).gm, "\nТы чист, уцы", "У вас нет наказаний.") if Human(**userdata[1]).discipline == None else "\nТебе нельзя писать в чат до \n*"+Human(**userdata[1]).discipline+"*"
	bot.send_message(messagechatid, string, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['start'], func=lambda message: message.text[17:])
def showPanel(message):
	chat_id = message.text[16:]
	data = load()
	userdata = Group(**data[chat_id][1]).participants[str(message.from_user.id)]
	markup = telebot.types.InlineKeyboardMarkup()
	btn1 = telebot.types.InlineKeyboardButton("Добавить задачу", callback_data="addtask"+chat_id)
	btn2 = telebot.types.InlineKeyboardButton("Мои задачи", callback_data="showtasks"+chat_id)
	btn3 = telebot.types.InlineKeyboardButton("Открыть канал", url=f"t.me/{Group(**data[chat_id][1]).url_of_channel[1:]}")
	markup.row(btn1)
	markup.row(btn2)
	markup.row(btn3)
	string = chstr(Group(**data[chat_id][1]).gm, f"Ассаламу алейкум ва рахматулахи тааля ва баракату, брат {telebot.types.User(**userdata[0]).first_name}!\n", f"Здравствуйте, {telebot.types.User(**userdata[0]).first_name}!\n")
	string+=chstr(Group(**data[chat_id][1]).gm, "\nТы чист, уцы", "У вас нет наказаний.") if Human(**userdata[1]).discipline == None else "\nТебе нельзя писать в чат до \n*"+Human(**userdata[1]).discipline+"*"
	bot.send_message(message.chat.id, string, reply_markup=markup, parse_mode="Markdown")

@bot.message_handler(commands=['reg'])
def joinToGroup(message):
	data = load()
	print(Group(**data[str(message.chat.id)][1]).participants)
	data = load()
	print(1)
	if str(message.from_user.id) in Group(**data[str(message.chat.id)][1]).participants:
		markup = telebot.types.InlineKeyboardMarkup()
		itembtn = telebot.types.InlineKeyboardButton(chstr(Group(**data[str(message.chat.id)][1]).gm, "Зайти","Войти"), callback_data="login")
		markup.row(itembtn)
		print(2)
		bot.reply_to(message, chstr(Group(**data[str(message.chat.id)][1]).gm, "ты уже состоишь в нашем гей-клубе.","Вы уже зарегистрированы."), reply_markup=markup)
		update(data)
	else:
		markup = telebot.types.InlineKeyboardMarkup()
		itembtn = telebot.types.InlineKeyboardButton(chstr(Group(**data[str(message.chat.id)][1]).gm, "Зайти в ламбу","Зарегистрироваться"), callback_data="register")
		markup.row(itembtn)
		bot.reply_to(message, chstr(Group(**data[str(message.chat.id)][1]).gm, "Монету кинь да","Вы еще не зарегистрированы."), reply_markup=markup)
		update(data)

@bot.message_handler(commands=['addchannel'], func=lambda message: isGroup(message.chat.type))
def addchannel(message):
	data = load()
	if len(message.text)>11:
		if data:
			if not(Group(**data[str(message.chat.id)][1]).c_id):
				thegroup = Group(**data[str(message.chat.id)][1])
				channel_id = str(bot.get_chat(message.text[12:]).id)
				thegroup.c_id = str(channel_id)
				bot.reply_to(message, chstr(Group(**data[str(message.chat.id)][1]).gm, "Ай сау!","Успешно!"))
				thegroup.url_of_channel = message.text[12:]
				data[str(message.chat.id)][1] = thegroup
				update(data)
			else:
				markup = telebot.types.InlineKeyboardMarkup()
				itembtn = telebot.types.InlineKeyboardButton("Удалить ссылку", callback_data="changechannel")
				markup.row(itembtn)
				bot.reply_to(message, "Ссылка на канал уже указана!", reply_markup=markup)

@bot.message_handler(commands=['help'])
def showHelp(message):
	data = load()
	bot.send_message(message.chat.id, chstr(Group(**data[str(message.chat.id)][1]).gm, "Ассаламу алейкум.\nМеня сделали для того, чтобы смотреть аниме и помогать тебе ботать!\nКак добавить бота в свою группу - \nhttps://telegra.ph/Kak-dobavit-bota-v-svoyu-gruppu-03-22", "Здравствуйте.\nЯ предназначен для того что-бы помогать вам ставить перед собой задачи!\nКак добавить бота в свою группу - \nhttps://telegra.ph/Kak-dobavit-bota-v-svoyu-gruppu-03-22")+"\n\n/reg - _регистрация/вход в панель управления_\n/gaymode - _Вкл/Выкл режим Мутаэлума._", parse_mode="Markdown")

@bot.message_handler(commands=['gaymode'], func=lambda message: isGroup(message.chat.type))
def changeMode(message):
	data = load()
	if Group(**data[str(message.chat.id)][1]).gm:
		bot.reply_to(message, "Режим Мутаэлума отключен.")
		data[str(message.chat.id)][1]['gm'] = False
	else:
		bot.reply_to(message, "Режим Мутаэлума включен.")
		data[str(message.chat.id)][1]['gm'] = True
	update(data)


@bot.callback_query_handler(func=lambda query: "vyes" in list(map(str, query.data.split("&"))))
def voteyes(query):
	datas = list(map(str, query.data.split("&")))
	groupid = datas[1]
	userid1 = datas[2]
	taskkey = datas[3]
	channel_id = query.message.chat.id
	data = load()
	
	if not(str(query.from_user.id) in data[groupid][1]['participants'][userid1][1]['tasks'][taskkey][4][0] or str(query.from_user.id) in data[groupid][1]['participants'][userid1][1]['tasks'][taskkey][4][1]):
		bot.answer_callback_query(query.id, chstr(data[groupid][1]['gm'], "Харашо да э. Я понял","Учтено!"), show_alert=False)
		data[groupid][1]['participants'][userid1][1]['tasks'][taskkey][4][0].append(str(query.from_user.id))
		if len(data[groupid][1]['participants'][userid1][1]['tasks'][taskkey][4][0]) >= NUMBER_OF_VOTES:
			data[groupid][1]['participants'][userid1][1]['tasks'].pop(taskkey)
			bot.delete_message(query.message.chat.id, query.message.message_id)
			bot.send_message(query.message.chat.id, f"{data[groupid][1]['participants'][userid1][0]['first_name']} "+ chstr(data[groupid][1]['gm'], "успешно исполнил, циу✅","выполнил свою задачу✅"))
	else:
		bot.answer_callback_query(query.id, chstr(data[groupid][1]['gm'], "Ты хоть куда э, голосовал же уже🤬","Вы уже голосовали!"), show_alert=True)
	update(data)

@bot.callback_query_handler(func=lambda query: "vno" in list(map(str, query.data.split("&"))))
def voteno(query):
	datas = list(map(str, query.data.split("&")))
	groupid = datas[1]
	userid1 = datas[2]
	taskkey = datas[3]
	channel_id = query.message.chat.id
	data = load()
	
	if not(str(query.from_user.id) in data[groupid][1]['participants'][userid1][1]['tasks'][taskkey][4][0] or str(query.from_user.id) in data[groupid][1]['participants'][userid1][1]['tasks'][taskkey][4][1]):
		bot.answer_callback_query(query.id, chstr(data[groupid][1]['gm'], "Харашо да э. Я понял","Учтено!"), show_alert=False)
		data[groupid][1]['participants'][userid1][1]['tasks'][taskkey][4][1].append(str(query.from_user.id))
		if len(data[groupid][1]['participants'][userid1][1]['tasks'][taskkey][4][1]) >= NUMBER_OF_VOTES:
			data[groupid][1]['participants'][userid1][1]['tasks'].pop(taskkey)
			ts = "%d"
			data[groupid][1]['participants'][userid1][1]['discipline'] = (nowtime()).replace(day=int(nowtime().strftime(ts))+1).strftime(timeStamp)
			data[groupid][1]['mutelist'].append(userid1)
			update(data)
			bot.delete_message(query.message.chat.id, query.message.message_id)
			bot.send_message(query.message.chat.id, f"{data[groupid][1]['participants'][userid1][0]['first_name']} "+ chstr(data[groupid][1]['gm'], "сбалаболил, не пацан он❌","не выполнил свою задачу❌"))
			showPanelManualy(datas[4], userid1, groupid)
	else:
		bot.answer_callback_query(query.id, chstr(data[groupid][1]['gm'], "Ты хоть куда э, голосовал же уже🤬","Вы уже голосовали!"), show_alert=True)
	update(data)

@bot.callback_query_handler(func=lambda query: "didthetask" in query.data)
def didthetask(query):
	chat_id = query.data[:query.data.find('didthetask')]
	taskkey = query.data[len(chat_id)+10:]
	data = load()
	bot.send_message(query.message.chat.id, chstr(Group(**data[chat_id][1]).gm, "пруфы опусти","Отправьте фото-доказательство выполнения задачи"))
	
	data[chat_id][1]['participants'][str(query.from_user.id)][1]['giving_args'] = taskkey
	update(data)

@bot.callback_query_handler(func=lambda query: "addtask" in query.data)
def addtask(query):
	chat_id = query.data[7:]
	data = load()
	bot.send_message(query.message.chat.id, chstr(Group(**data[chat_id][1]).gm, "Введи название задачи, брат","Введите название задачи")+"\n*P.S. Одним словом до 12 букв*")
	
	data[chat_id][1]['participants'][str(query.from_user.id)][1]['adding_name'] = True
	update(data)

@bot.callback_query_handler(func=lambda query: "showtasks" in query.data)
def showtask(query):
	chat_id = query.data[9:]
	data = load()
	tasks = Human(**Group(**data[chat_id][1]).participants[str(query.from_user.id)][1]).tasks
	if tasks:
		bot.send_message(query.message.chat.id, chstr(Group(**data[chat_id][1]).gm, "Твои задачи, брат:","Ваши задачи:"))
		string = ""
		ch = True
		for i in list(tasks.keys()):
			if len(tasks[i]) == 4:
				string += f"_{tasks[i][0]}_\n\n"
				string += f"*Описание*:\n`{tasks[i][1]}`\n\n"
				string += f"*Доказательство*:\n`{tasks[i][2]}`\n\n"
				string += f"*Выполнить до*\n`{tasks[i][3]}`"
				markup = telebot.types.InlineKeyboardMarkup()
				itembtn = telebot.types.InlineKeyboardButton("Выполнено", callback_data=chat_id+"didthetask"+i)
				markup.row(itembtn)
				bot.send_message(query.message.chat.id, string, reply_markup=markup, parse_mode="Markdown")
				string = ""
				ch = False
		if ch:
			markup = telebot.types.InlineKeyboardMarkup()
			itembtn = telebot.types.InlineKeyboardButton("Добавить", callback_data="addtask"+chat_id)
			markup.row(itembtn)
			bot.send_message(query.message.chat.id, chstr(Group(**data[chat_id][1]).gm, "У тебя нет задач, гей","У вас нет задач!"), reply_markup=markup)


	else:
		markup = telebot.types.InlineKeyboardMarkup()
		itembtn = telebot.types.InlineKeyboardButton("Добавить", callback_data="addtask"+chat_id)
		markup.row(itembtn)
		bot.send_message(query.message.chat.id, chstr(Group(**data[chat_id][1]).gm, "У тебя нет задач, гей","У вас нет задач!"), reply_markup=markup)


@bot.message_handler(func=lambda message: not(isGroup(message.chat.type)) and isaddingname(message.from_user.id))
def getname(message):
	data = load()
	group = isaddingname(message.from_user.id)
	user = telebot.types.User(**(Group(**group[1]).participants[str(message.from_user.id)][0]))
	if len(message.text)<=12:
		data[str(telebot.types.Chat(**group[0]).id)][1]['participants'][str(user.id)][1]['adding_name'] = False
		data[str(telebot.types.Chat(**group[0]).id)][1]['participants'][str(user.id)][1]['adding_description'] = True
		data[str(telebot.types.Chat(**group[0]).id)][1]['participants'][str(user.id)][1]['tasks'].update({message.text:[message.text, None, None, None]})
		bot.send_message(message.chat.id, chstr(Group(**group[1]).gm, "Введите описание","Введите описание"))
	else:
		data[str(telebot.types.Chat(**group[0]).id)][1]['participants'][str(message.from_user.id)][1]['adding_name'] = False
		bot.send_message(message.chat.id, chstr(Group(**group[1]).gm, "Слишком многа букав","Превышена допустимая длина"))
		showPanelManualy(str(message.chat.id), str(message.from_user.id), telebot.types.Chat(**group[0]).id)

	update(data)

@bot.message_handler(func=lambda message: not(isGroup(message.chat.type)) and isaddingdescription(message.from_user.id))
def getdesc(message):
	data = load()
	group = isaddingdescription(message.from_user.id)
	user = telebot.types.User(**(Group(**group[1]).participants[str(message.from_user.id)][0]))
	data[str(telebot.types.Chat(**group[0]).id)][1]['participants'][str(user.id)][1]['adding_description'] = False
	data[str(telebot.types.Chat(**group[0]).id)][1]['participants'][str(user.id)][1]['adding_arguments'] = True
	task = Human(**Group(**data[str(telebot.types.Chat(**group[0]).id)][1]).participants[str(user.id)][1]).tasks
	data[str(telebot.types.Chat(**group[0]).id)][1]['participants'][str(user.id)][1]['tasks'][list(task.keys())[-1]][1] = message.text
	bot.send_message(message.chat.id, chstr(Group(**group[1]).gm, "Опиши доказательство выполнения задачи","Опишите доказательство выполнения задачи"))
	update(data)

@bot.message_handler(func=lambda message: not(isGroup(message.chat.type)) and isaddingarguments(message.from_user.id))
def getargs(message):
	data = load()
	group = isaddingarguments(message.from_user.id)
	user = telebot.types.User(**(Group(**group[1]).participants[str(message.from_user.id)][0]))
	data[str(telebot.types.Chat(**group[0]).id)][1]['participants'][str(user.id)][1]['adding_arguments'] = False
	data[str(telebot.types.Chat(**group[0]).id)][1]['participants'][str(user.id)][1]['adding_time'] = True
	task = Human(**Group(**data[str(telebot.types.Chat(**group[0]).id)][1]).participants[str(user.id)][1]).tasks
	data[str(telebot.types.Chat(**group[0]).id)][1]['participants'][str(user.id)][1]['tasks'][list(task.keys())[-1]][2] = message.text
	bot.send_message(message.chat.id, chstr(Group(**group[1]).gm, "До скольки справишься?","Введите время, до которого вы выполните задачу в формате")+"\nXX:XX XX.XX.XXXX")
	update(data)

@bot.message_handler(func=lambda message: not(isGroup(message.chat.type)) and isaddingtime(message.from_user.id))
def gettime(message):
	data = load()
	group = isaddingtime(message.from_user.id)
	user = telebot.types.User(**(Group(**group[1]).participants[str(message.from_user.id)][0]))
	data[str(telebot.types.Chat(**group[0]).id)][1]['participants'][str(user.id)][1]['adding_time'] = False
	data[str(telebot.types.Chat(**group[0]).id)][1]['participants'][str(user.id)][1]['adding_ok'] = True
	task = Human(**Group(**data[str(telebot.types.Chat(**group[0]).id)][1]).participants[str(user.id)][1]).tasks
	ch = True
	try:
		data[str(telebot.types.Chat(**group[0]).id)][1]['participants'][str(user.id)][1]['tasks'][list(task.keys())[-1]][3] = datetime.strptime(message.text, timeStamp)
	except ValueError:
		data[str(telebot.types.Chat(**group[0]).id)][1]['participants'][str(user.id)][1]['tasks'].pop(list(task.keys())[-1])
		data[str(telebot.types.Chat(**group[0]).id)][1]['participants'][str(user.id)][1]['adding_ok'] = False
		bot.send_message(message.chat.id, chstr(Group(**group[1]).gm, "Иди нахуй","Неправильный формат времени"))
		showPanelManualy(str(message.chat.id), str(message.from_user.id), telebot.types.Chat(**group[0]).id)
		ch = False
		update(data)

	"XX:XX XX.XX.XXXX"
	"%H:%M %d.%m.%Y"

	
	if ch:
		data[str(telebot.types.Chat(**group[0]).id)][1]['participants'][str(user.id)][1]['tasks'][list(task.keys())[-1]][3] = message.text
		update(data)
		markup = telebot.types.InlineKeyboardMarkup()
		btn1 = telebot.types.InlineKeyboardButton(chstr(Group(**group[1]).gm, "Все четко, брат","Все правильно"), callback_data="taskdone"+str(telebot.types.Chat(**group[0]).id))
		btn2 = telebot.types.InlineKeyboardButton("Отмена", callback_data="canceltask"+str(telebot.types.Chat(**group[0]).id))
		markup.row(btn1, btn2)
		bot.send_message(message.chat.id, "Проверьте правильность введенных данных:", reply_markup=markup)

# @bot.message_handler(func=lambda message: not(isGroup(message.chat.type)) and isaddingok(message.from_user.id))
# def getok(message):
# 	data = load()
# 	group = isaddingok(message.from_user.id)
# 	user = telebot.types.User(**(Group(**group[1]).participants[str(message.from_user.id)][0]))
	
	
@bot.callback_query_handler(func=lambda query: "canceltask" in query.data)
def canceltask(query):
	data = load()
	chat_id = query.data[10:]
	group = data[chat_id]
	user = telebot.types.User(**Group(**group[1]).participants[str(query.from_user.id)][0])
	task = Human(**Group(**data[str(telebot.types.Chat(**group[0]).id)][1]).participants[str(user.id)][1]).tasks
	data[str(telebot.types.Chat(**group[0]).id)][1]['participants'][str(user.id)][1]['tasks'].pop(list(task.keys())[-1])
	update(data)
	bot.edit_message_text("Действие отменено.", chat_id=query.message.chat.id, message_id=query.message.message_id)
	bot.answer_callback_query(query.id, "Действие отменено.", url="t.me/mutakabot?start=showpanel"+str(chat_id))

@bot.callback_query_handler(func=lambda query: "taskdone" in query.data)
def donetask(query):
	chat_id = query.data[8:]
	bot.edit_message_text("Задача добавлена.", chat_id=query.message.chat.id, message_id=query.message.message_id)
	bot.answer_callback_query(query.id, "Задача добавлена.", url="t.me/mutakabot?start=showpanel"+str(chat_id))

@bot.callback_query_handler(func=lambda query: query.data == "changechannel")
def changechannel(query):
	data = load()
	if data[str(query.message.chat.id)][2]:
		data[str(query.message.chat.id)][2] = 0
		update(data)
		bot.edit_message_text("Ссылка на канал удалена.", chat_id=query.message.chat.id, message_id=query.message.message_id)
		bot.answer_callback_query(query.id, "Ссылка удалена.", show_alert=False)

	else:
		bot.answer_callback_query(query.id, "Ссылка уже удалена!", show_alert=True)


@bot.callback_query_handler(func=lambda query: query.data == "login")
def login(query):
	data = load()
	if str(query.from_user.id) in Group(**data[str(query.message.chat.id)][1]).participants:
		bot.answer_callback_query(query.id, url="t.me/mutakabot?start=showpanel"+str(query.message.chat.id))
	else:
		bot.answer_callback_query(query.id, chstr(Group(**data[str(query.message.chat.id)][1]).gm, "Ты не зареган да э","Вы не зарегистрированы!"), show_alert=True)







@bot.callback_query_handler(func=lambda query: query.data == "register")
def register(query):
	data = load()
	if str(query.from_user.id) in Group(**data[str(query.message.chat.id)][1]).participants:
		bot.answer_callback_query(query.id, chstr(Group(**data[str(query.message.chat.id)][1]).gm, "Куда гонишь, машина? Зареган уже.","Вы уже зарегистрированы!"), show_alert=True)
	else:
		Group(**data[str(query.message.chat.id)][1]).participants.update({str(query.from_user.id):[query.from_user, Human()]})
		update(data)
		bot.answer_callback_query(query.id, chstr(Group(**data[str(query.message.chat.id)][1]).gm, "Заявка на вступление в гей-клуб одобрена","Регистрация успешно завершена!"), show_alert=True)
		bot.edit_message_text(chstr(Group(**data[str(query.message.chat.id)][1]).gm, "Ты в клубе(гей)","Вы зарегистрированы."), chat_id=query.message.chat.id, message_id=query.message.message_id)
		markup = telebot.types.InlineKeyboardMarkup()
		itembtn = telebot.types.InlineKeyboardButton(chstr(Group(**data[str(query.message.chat.id)][1]).gm, "Зайти","Войти"), callback_data="login")
		markup.row(itembtn)
		bot.edit_message_reply_markup(reply_markup=markup, chat_id=query.message.chat.id, message_id=query.message.message_id)

# @bot.message_handler(command=['start'], func=lambda message: safe_show(message.text, 7))
# def onStart(message):
# 	data = load()
@bot.message_handler(func=lambda message: isGroup(message.chat.type))
def deleteMess(message):
	print(nowtime().strftime(timeStamp))
	if load():
		if isGroup(message.chat.type) and str(message.from_user.id) in dict(load())[str(message.chat.id)][1]['mutelist']:
			bot.delete_message(message.chat.id, message.message_id)

		canUnMute()
		canUnPost()

content_types=['photo']

@bot.message_handler(content_types=['photo'],func=lambda message: isGroup(message.chat.type))
def deleteMess(message):
	print(nowtime().strftime(timeStamp))
	if load():
		if isGroup(message.chat.type) and str(message.from_user.id) in dict(load())[str(message.chat.id)][1]['mutelist']:
			bot.delete_message(message.chat.id, message.message_id)

		canUnMute()
		canUnPost()

@bot.message_handler(content_types=['audio'],func=lambda message: isGroup(message.chat.type))
def deleteMesssss(message):
	print(nowtime().strftime(timeStamp))
	if load():
		if isGroup(message.chat.type) and str(message.from_user.id) in dict(load())[str(message.chat.id)][1]['mutelist']:
			bot.delete_message(message.chat.id, message.message_id)

		canUnMute()
		canUnPost()

@bot.message_handler(content_types=['voice'],func=lambda message: isGroup(message.chat.type))
def deleteMessss(message):
	print(nowtime().strftime(timeStamp))
	if load():
		if isGroup(message.chat.type) and str(message.from_user.id) in dict(load())[str(message.chat.id)][1]['mutelist']:
			bot.delete_message(message.chat.id, message.message_id)

		canUnMute()
		canUnPost()

@bot.message_handler(content_types=['sticker'],func=lambda message: isGroup(message.chat.type))
def deleteMesss(message):
	print(nowtime().strftime(timeStamp))
	if load():
		if isGroup(message.chat.type) and str(message.from_user.id) in dict(load())[str(message.chat.id)][1]['mutelist']:
			bot.delete_message(message.chat.id, message.message_id)

		canUnMute()
		canUnPost()

bot.polling(none_stop=True)


	