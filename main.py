import asyncio
import io
import os.path

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

global TOKEN
global q_number
global START_MESSAGE
global ROADMAP_MESSAGE
global INFORMATION_MESSAGE


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global START_MESSAGE
    await context.bot.send_message(chat_id=update.effective_chat.id,
                                   text=f'اهلا بك {update.message.from_user.first_name} في UST & IEEE بوت.\n {START_MESSAGE}')


async def roadmap(update: Update, context: ContextTypes.DEFAULT_TYPE):
    command: str = update.message.text.strip()
    response: str = await response_message_roadmap(command)
    if response == "": return
    await context.bot.send_message(chat_id=update.effective_chat.id, text=response)


async def response_message_roadmap(command: str):
    match command:
        case "/roadmap":
            return ROADMAP_MESSAGE
        case "/mobile_app":
            return await async_read_all_lines("mobile_app.txt")
        case "/desktop_app":
            return await async_read_all_lines("desktop_app.txt")
        case "/cyber_security":
            return await async_read_all_lines("cyber_security.txt")
        case "/Q_S":
            return await async_read_all_lines("Q_S.txt")
        case "/machine_learning":
            return await async_read_all_lines("machine_learning.txt")
        case _:
            return ""


async def ask(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text != "/ask":
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="شكرا على طرح سؤالك سوف يتم إضافته في القناة قريباً...")
        ask_message = await message_to_group(update=update, type_message='ask')
        await context.bot.send_message(chat_id="-960631449", text=ask_message)
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text='''اطرح اسئلة تقنية من خلال /ask بحيث 
        سوف يتم عرض هذا السؤال في القناة ويتم اضافة الحلول لسؤالك في التعليقات مثلاً: /ask كيف استطيع قراءة البار كود 
        بإستخدام Android studio java''')


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await context.bot.send_message(chat_id=update.effective_chat.id, text=INFORMATION_MESSAGE)


async def suggest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.text != "/suggest":
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="شكرا على المقترح 😊")
        suggest_message = await message_to_group(update=update, type_message='suggest')
        await context.bot.send_message(chat_id="-960631449", text=suggest_message)


async def message_to_group(update: Update, type_message: str):
    message = update.message.text
    username = update.message.from_user.username
    match type_message:
        case "ask":
            global q_number
            q_number = q_number + 1
            return f'المرسل: @{username}\nرقم السؤال: {q_number}\nالسؤال: {message[4: len(message)]}'
        case "suggest":
            return f'المرسل: @{username}\nالمقترح: {message[8: len(message)]}'
        case _:
            return ""


async def async_read_all_lines(file_name: str):
    text: str = ""
    if not os.path.exists(file_name): return text

    file = io.open(file_name, mode="r", encoding="utf-8")
    lines = file.readlines()
    for line in lines:
        text += line
    file.close()
    return text


def read_all_lines(file_name: str):
    text: str = ""
    if not os.path.exists(file_name): return text

    file = io.open(file_name, mode="r", encoding="utf-8")
    lines = file.readlines()
    for line in lines:
        text += line
    file.close()
    return text


def initialize_variables():
    global q_number, TOKEN, START_MESSAGE, INFORMATION_MESSAGE, ROADMAP_MESSAGE
    q_number = 5
    TOKEN = "6652492573:AAF2OJstWCigDLfOo5R8RYoaYVBEGbS7ciY"
    START_MESSAGE = read_all_lines("start_message.txt")
    INFORMATION_MESSAGE = read_all_lines("information_message.txt")
    ROADMAP_MESSAGE = read_all_lines("roadmap_message.txt")


if __name__ == '__main__':
    initialize_variables()
    application = ApplicationBuilder().token(TOKEN).build()

    start_handler = CommandHandler('start', start)
    roadmap_handler = CommandHandler(["roadmap",
                                      "mobile_app",
                                      "desktop_app",
                                      "cyber_security",
                                      "Q_S",
                                      "machine_learning"], roadmap)
    ask_handler = CommandHandler('ask', ask)
    info_handler = CommandHandler('info', info)
    suggest_handler = CommandHandler('suggest', suggest)

    application.add_handler(start_handler)
    application.add_handler(roadmap_handler)
    application.add_handler(ask_handler)
    application.add_handler(info_handler)
    application.add_handler(suggest_handler)

    application.run_polling()
