import telebot
import dropbox

TOKEN = 'YOUR_BOT_TOKEN'
DROPBOX_ACCESS_TOKEN = 'YOUR_DROPBOX_ACESS_TOKEN'
DROPBOX_FILE_PATH = '/messages.txt'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    text = message.text

    write_to_dropbox(text, DROPBOX_ACCESS_TOKEN, DROPBOX_FILE_PATH)

    bot.send_message(chat_id, 'Сообщение успешно записано в Dropbox.')


def write_to_dropbox(message, access_token, file_path):
    dbx = dropbox.Dropbox(access_token)

    try:
        _, existing_data = dbx.files_download(file_path)
        existing_content = existing_data.content.decode('utf-8')

        new_content = existing_content + '\n' + message

        dbx.files_upload(new_content.encode('utf-8'), file_path,
                         mode=dropbox.files.WriteMode('overwrite'))
    except dropbox.exceptions.HttpError as e:
        print(f"Ошибка Dropbox API: {e}")


bot.polling(none_stop=True)
