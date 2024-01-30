import telebot
import dropbox

TOKEN = '6228036250:AAG0ZyujGTT9nGcO7RP0oVRD2V8uWNdZcuk'
DROPBOX_ACCESS_TOKEN = 'sl.BupyeMefsMCU1PA2wiUiJ_VONyHaOIaD1VpAWMyNATJdSYCjNSWt28K1GMojdD-l0SsRjjgkoQn5-E5eXtNaWa-olxVv6puLbl9mSHGAZMvu0Nn_uiNGGCuAsnm36Qjva4qFar14ms7L'
DROPBOX_FILE_PATH = '/messages.txt'

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    chat_id = message.chat.id
    text = message.text

    # Запись нового сообщения в Dropbox
    write_to_dropbox(text, DROPBOX_ACCESS_TOKEN, DROPBOX_FILE_PATH)

    bot.send_message(chat_id, 'Сообщение успешно записано в Dropbox.')


def write_to_dropbox(message, access_token, file_path):
    dbx = dropbox.Dropbox(access_token)

    try:
        # Получение текущего содержимого файла
        _, existing_data = dbx.files_download(file_path)
        existing_content = existing_data.content.decode('utf-8')

        # Добавление нового сообщения
        new_content = existing_content + '\n' + message

        # Загрузка обновленного файла
        dbx.files_upload(new_content.encode('utf-8'), file_path,
                         mode=dropbox.files.WriteMode('overwrite'))
    except dropbox.exceptions.HttpError as e:
        print(f"Ошибка Dropbox API: {e}")


# Запуск бота
bot.polling(none_stop=True)
