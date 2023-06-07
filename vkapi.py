import json
from datetime import datetime
from pprint import pprint
import requests
from tqdm import tqdm
from yadiskapi import YaDiskApi


class VkApi:
    url = 'https://api.vk.com/method/'

    def __init__(self, token, version='5.131'):
        self.params = {
            'access_token': token,
            'v': version
        }

    def get_photos(self, user_id, album='profile'):
        photos_url = self.url + 'photos.get'
        photos_params = {
            'owner_id': user_id,
            'album_id': album,
            'extended': 1,
            'photo_sizes': 1
        }
        req = requests.get(photos_url, params={**self.params, **photos_params}).json()
        return req

    def save_photos_to_yadisk(self, user_id, ya_disk_api: YaDiskApi, album='profile', count=5):
        if not isinstance(ya_disk_api, YaDiskApi):
            print('Ошибка! Параметр "ya_disk_api" должен быть экземпляром "YaDiskApi".')
            return

        try:
            photos = self.get_photos(user_id, album)
        except:
            print('Не удалось загрузить список фотографий из VK!')
            return

        dir_name = f'photos_{user_id}'
        if album != 'profile':
            dir_name += f'_{album}'
        dir_creating_status = ya_disk_api.create_dir(dir_name)
        if dir_creating_status != 'OK':
            print(f'Не удалось создать каталог для загрузки фотографий!\n{dir_creating_status}')
            return

        try:
            photos_list = photos['response']['items'][:min(count, photos['response']['count'])]
        except:
            try:
                print(f'Не удалось обработать список фотографий из VK: {photos["error"]["error_msg"]}!')
            except:
                print('Не удалось обработать список фотографий из VK!')
            return

        likes_cnt_list = [photo["likes"]["count"] for photo in photos_list]
        dup_likes_cnt = set(likes_cnt for likes_cnt in likes_cnt_list if likes_cnt_list.count(likes_cnt) > 1)

        photos_info = []
        photos_info_err = []
        for photo in (pbar := tqdm(photos_list, desc='Uploading photos from VK to Yandex.Disk')):
            likes_count = photo["likes"]["count"]
            if likes_count in dup_likes_cnt:
                file_name = f'{likes_count}_{datetime.fromtimestamp(photo["date"]):%Y%m%d_%H%M%S}.jpg'
            else:
                file_name = f'{likes_count}.jpg'
            pbar.set_postfix_str(file_name)

            size = photo['sizes'][-1]['type']

            res = ya_disk_api.upload_photo_by_url(file_name, dir_name, photo['sizes'][-1]['url'])
            if res == 'OK':
                photos_info.append({'file_name': file_name, 'size': size})
            else:
                photos_info_err.append({'file_name': file_name, 'size': size, 'error': res})
                tqdm.write(res)

        if photos_info:
            print(f'Информация о загруженных фотографиях (загружены {len(photos_info)} фото):')
            pprint(photos_info)
        else:
            print('Не удалось загрузить фото!')
        if photos_info_err:
            print(f'Не удалось загрузить следующие {len(photos_info_err)} фото:')
            pprint(photos_info_err)

        with open('uploaded_photos_info.json', 'w') as json_file:
            json.dump(photos_info, json_file, indent=2)
