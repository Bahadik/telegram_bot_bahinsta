import instagram_file_downloader
from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters

# You need to get your own token from @BotFather
TOKEN = 'YOUR TOKEN'
updater = Updater(token=TOKEN)
dispatcher = updater.dispatcher
login_post = {}

def start(bot, update):
    bot.sendMessage(chat_id=update.message.chat_id, text="I'm a bot that downloads instagram photos and videos. \
To download from private accounts you need to sign in. To do this use /login username password. \
Or you can download public photos and videos without signing in just sending me the url.")

def download(bot, update):
    url_start_index = update.message.text.find('http')
    if url_start_index == -1:
        bot.sendMessage(chat_id=update.message.chat_id, text="Please send url of instagram photo or video.")
        return
    text = update.message.text[url_start_index:]
    url = instagram_file_downloader.get_content_url(login_post, text)
    if url == '':
        bot.sendMessage(chat_id=update.message.chat_id, text="Some error happened! Check the url, your login and password, \
or you do not have an access to the account")
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text=url)

def login(bot, update, args):
    if len(args) > 1:
        username = args[0]
        password = args[1]
        global login_post
        login_post = {
            'username': username.lower(),
            'password': password
        }
        bot.sendMessage(chat_id=update.message.chat_id, text="Now you can send private url of photo or video of your private friends.")
    else:
        bot.sendMessage(chat_id=update.message.chat_id, text="Try again. Use /login username password.")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

download_handler = MessageHandler(Filters.text, download)
dispatcher.add_handler(download_handler)

login_handler = CommandHandler('login', login, pass_args=True)
dispatcher.add_handler(login_handler)

updater.start_polling()
updater.idle()
