import requests


class YaDiskApi:
    url = "https://cloud-api.yandex.net/v1/disk/"

    def __init__(self, token):
        self.token = token

    def get_headers(self):
        headers = {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }
        return headers

    def create_dir(self, dir_name, dir_path='/'):
        url_create_dir = self.url + 'resources'
        res = requests.put(
            url=url_create_dir,
            params={'path': f'{dir_path.rstrip("/")}/{dir_name}'},
            headers=self.get_headers()
        )
        if res.status_code == 201 or res.status_code == 409:
            return 'OK'
        else:
            try:
                return f'Что-то пошло не так во время создания каталога {dir_name}: {res.json()["message"]}!'
            except:
                return f'Что-то пошло не так во время создания каталога {dir_name}!'

    def upload_photo_by_url(self, file_name, ir, file_url):
        url_get_upload_url = self.url + 'resources/upload'
        upload_url_info = requests.get(
            url=url_get_upload_url,
            params={'path': f'{ir}/{file_name}'},
            headers=self.get_headers()
        )
        if upload_url_info.status_code != 200:
            try:
                return f'Что-то пошло не так при получении URL-адреса загрузки: {upload_url_info.json()["message"]}!'
            except:
                return f'Что-то пошло не так во время загрузки URL-адреса!'
        upload_url = upload_url_info.json()['href']
        res = requests.put(
            url=upload_url,
            data=requests.get(file_url)
        )
        if res.status_code == 201:
            return 'OK'
        else:
            try:
                return f'Что-то пошло не так во время загрузки файла {file_name}:\n {res.json()["message"]}!'
            except:
                return f'Что-то пошло не так во время загрузки файла {file_name}!'
