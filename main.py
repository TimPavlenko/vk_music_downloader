# -*- coding: utf-8 -*-
'''
from tim with love for paranoia and music

'''
import vk_api
from vk_api import audio
import requests
import os


REQUEST_STATUS_CODE = 200

path = r"vk_music"

while(True):
    print('')
    login = input('Enter login:')
    password = input('Enter password:')
    id = input('Enter your VK id:')
    vk_session = vk_api.VkApi(login=login, password=password)
    try:
        vk_session.auth()
    except vk_api.exceptions.AuthError:
        print('')
        print('Data is incorrect, please try again')
        continue
    break


vk = vk_session.get_api()  # Теперь можно обращаться к методам API как к обычным классам
vk_audio = audio.VkAudio(vk_session)  # Получаем доступ к audio

if not os.path.exists(path):
    os.makedirs(path)

os.chdir(path)
print('wait, connect to vk...')
music = vk_audio.get(owner_id=id)
music_num = len(music)

score = 1
errors = 0
arr_errors = []
create_file = open("errors.txt", "w")
create_file.close()
f = open('errors.txt', 'w')
for i in music:
    try:
        r = requests.get(i["url"])
        if r.status_code == REQUEST_STATUS_CODE:
            with open(i["artist"] + '_' + i["title"] + '.mp3', 'wb') as output_file:
                print('[' + str(score) + '/' + str(music_num) + ']' + '  complete: ' + i["artist"] + '  |  ' + i["title"])
                output_file.write(r.content)
    except OSError:
        print('[' + str(score) + '/' + str(music_num) + ']' + '  ERROR: ' + i["artist"] + '  |  ' + i["title"])
        arr_errors.append(i["artist"] + '  |  ' + i["title"] + '\n')
        errors += 1
    score += 1
print('')
print('finish!')
print('your music is in the vk_music folder')
if(errors > 0):
    print('')
    print('some tracks could not be downloaded(please download them yourself):')
    for i in arr_errors:
        print(" " + i)
