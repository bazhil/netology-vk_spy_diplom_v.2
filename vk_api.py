from urllib.parse import urlencode
import  requests
import time
from pprint import pprint
import json


class VK:
    """
    Описание класса
    """

    default_token = '7b23e40ad10e08d3b7a8ec0956f2c57910c455e886b480b7d9fb59859870658c4a0b8fdc4dd494db19099'
    target_uid = '5030613'
    api_version = '5.73'
    base_url = 'https://api.vk.com/method/'

    def __init__(self, token=None):
        """
        Метод инициализации класса
        :param token: уникальный токен для доступа в Вконтакте
        """
        self.friends_id = []
        self.default_token = '7b23e40ad10e08d3b7a8ec0956f2c57910c455e886b480b7d9fb59859870658c4a0b8fdc4dd494db19099'
        self.token = token or self.default_token
        self.api_version ='5.73'
        self.base_url = 'https://api.vk.com/method/'

    def find_friends(self, target_uid):
        """
        Метод поиска друзей
        :param target_uid: ID целевого пользователя в Вконтакте
        """

        params = {
            'access_token': self.token,
            'target_uid': target_uid,
            'v': self.api_version
        }

        url = self.base_url + 'friends.get'
        response = requests.get(url, params)
        if response.status_code == 200:
            self.friends_id = response.json()['response']['items']


    def find_groups(self, target_uid):
        """
        Метод поиска групп в которых состоит пользователь
        :param target_uid: ID целевого пользователя в Вконтакте
        :return: возвращает словарь групп пользователя с ключами идентификатор группы значениями имя группы
        """
        user_groups = {}
        params = {
            'access_token': self.token,
            'user_id': target_uid,
            'v': self.api_version,
            'extended': 1
        }

        url = self.base_url + 'groups.get'
        response = requests.get(url, params)

        if response.status_code == 200:
            try:
                items_from_groups = response.json()['response']['items']
                user_groups = {item['id']: item['name'] for item in items_from_groups}
                time.sleep(0.4)
                print('.')
            except KeyError:
                pass
        return user_groups

    def get_members(self, group_id):
        """
        Метод определяющий количество участников в группах
        :param group_id: идентификатор группы
        :return: возвращает количество участников группы с ключами
        """
        users_in_group = 0
        params = {
            'access_token': self.token,
            'group_id': group_id,
            'v': self.api_version
        }

        url = self.base_url + 'groups.getMembers'
        response = requests.get(url, params)
        if response.status_code == 200:
            try:
                users_in_group = response.json()['response']['count']
                time.sleep(0.4)
                print('.')
            except:
                pass
        return users_in_group

def group_analyse(friends_id, user_groups):
    """
    Метод анализирующий группы пользователя
    :param friends_id: список друзей пользователя
    :param user_groups: список групп пользователя
    :return: возвращает список групп пользователя в которых не состоит ни один из друзей пользователя
    """
    vk = VK()
    friend_groups = []
    for friend in friends_id:
        friend_groups += list(vk.find_groups(friend).keys())
    return set(user_groups.keys()) - set(friend_groups)

def end_analyse():
    """
    анализируем группы и сохраняем результат в файле groups.json
    """
    group_info = []
    user_id = input('Введите id целевого пользователя: ')
    if not user_id:
        print('Ошибка: не введен идентификатор')
    vk = VK()
    vk.find_friends(user_id)
    groups = vk.find_groups(user_id)
    unique_groups = group_analyse(vk.friends_id, groups)
    for group in unique_groups:
        count = vk.get_members(group)
        group_info.append(dict(name=groups[group], gid=group, members_count=count))
    with open('groups.json', 'w', encoding='utf-8') as f:
        json.dump(group_info, f, ensure_ascii=False, indent=2)

end_analyse()



