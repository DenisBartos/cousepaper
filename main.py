import json
import os
from vkapi import VkApi
from yadiskapi import YaDiskApi

CONFIG_FILENAME = 'config.txt'

if __name__ == '__main__':
    vk_token = None
    ya_disk_token = None

    if os.path.exists(CONFIG_FILENAME):
        try:
            with open(CONFIG_FILENAME, 'rt') as config_file:
                config = json.load(config_file)
                vk_token = config['vk token']
                try:
                    ya_disk_token = config['yandex disk token']
                except:
                    pass
        except Exception as config_err:
            print(f'Ошибка при чтении конфигурационного файла:\n{type(config_err)}\n{config_err}')
    else:
        print('Конфигурационный файл не найден. Смотрите "config_example.txt"')

    if vk_token is None:
        print('Не удалось загрузить токен VK из конфигурационного файла.')
        vk_token = input('Пожалуйста, введите значение токена VK: ')
        if not vk_token:
            print('Токен VK необходим для запуска программы!')
            exit()
    try:
        vk_user_id = int(input('Пожалуйста, введите идентификатор пользователя vk, '
                               'чтобы загрузить фотографии профиля: '))
    except:
        print('Идентификатор пользователя VK должен быть допустимым целым значением!')
        exit()
    ya_disk_token_input = input('Пожалуйста, введите Яндекс.Значение дискового токена '
                                '(оставьте его пустым, чтобы прочитать его с config.txt): ')
    if ya_disk_token_input:
        ya_disk_token = ya_disk_token_input
    if not ya_disk_token:
        print('Яндекс.Диск токен необходим для запуска программы! Он должен быть введен пользователем '
              'или загружен из файла конфигурации.')
        exit()

    user_vk_api = VkApi(vk_token)
    user_ya_disk_api = YaDiskApi(ya_disk_token)

    vk_album_id = str(input('Пожалуйста, введите идентификатор альбома (профиль по умолчанию): ') or 'profile')
    photos_cnt = int(input('Пожалуйста, введите количество фотографий для загрузки (по умолчанию 5): ') or 5)

    user_vk_api.save_photos_to_yadisk(user_id=vk_user_id, ya_disk_api=user_ya_disk_api, album=vk_album_id,
                                      count=photos_cnt)
