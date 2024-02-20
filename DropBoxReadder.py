import dropbox
import time
import psutil
import os

DROPBOX_ACCESS_TOKEN = 'YOUR_DROPBOX_ACCESS_TOKEN'
DROPBOX_FILE_PATH = '/messages.txt'


f = open('D:/TT/start_sklad.bat', 'r')
lines = f.readlines()[1:2]
for line in lines:
    ttname = line[147:-6]


def read_dropbox_file(access_token, file_path):
    dbx = dropbox.Dropbox(access_token)

    while True:
        try:
            _, file_data = dbx.files_download(file_path)
            file_content = file_data.content.decode('utf-8')

            commands = file_content.split('\n')

            for command in commands:
                if 'ТВ ' + ttname in command:
                    for process in (process for process in psutil.process_iter() if process.name() == "TeamViewer.exe"):
                        process.kill()
                    os.startfile(
                        'C:/Program Files (x86)/TeamViewer/TeamViewer.exe')
                    dbx.files_upload("".encode('utf-8'), file_path,
                                     mode=dropbox.files.WriteMode('overwrite'))
            time.sleep(5)
        except dropbox.exceptions.HttpError as e:
            print(f"Ошибка Dropbox API: {e}")


read_dropbox_file(DROPBOX_ACCESS_TOKEN, DROPBOX_FILE_PATH)
