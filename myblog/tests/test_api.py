import pytest
from rest_framework.test import APIClient
from blog.models import MyUser, Post, Subscriptions


def test_register(client, register_user_1):
    # повтороное добавление в БД уже существующего юзера
    url = 'http://localhost:8000/api/v1/auth/users/'
    data = {'email': 'test@mail.ru', 'password': 'qwerty654321', 'username': 'Sveta'}
    response = client.post(url, data=data)

    assert response.status_code == 400

def test_login(client, register_user_1, register_user_2):
    # авторизация несуществующего юзера
    url = 'http://localhost:8000/api/v1/token/login/'
    data = {'email': 'wrong@mail.ru', 'password': 'qwerty123654'}
    response = client.post(url, data=data)

    assert response.status_code == 400
    assert response.json()['non_field_errors'] == ['Невозможно войти с предоставленными учетными данными.']

    # авторизация существующих юзеров
    data = {'email':'test@mail.ru', 'password':'qwerty654321'}
    response = client.post(url, data=data)

    assert response.status_code == 200
    assert response.json().get('auth_token')

    data = {'email': 'test_2@mail.ru', 'password': 'qwerty08060402'}
    response = client.post(url, data=data)

    assert response.status_code == 200
    assert response.json().get('auth_token')


def test_logout(client, register_user_1, register_user_2, login_user_2):
    # выход юзера с запросом без заголовка авторизации
    client = APIClient()
    url = 'http://localhost:8000/api/v1/token/logout/'

    response = client.post(url)

    assert response.status_code == 403
    assert response.json()['detail'] == 'Учетные данные не были предоставлены.'

    client.credentials(HTTP_AUTHORIZATION='Token ' + login_user_2)

    # выход юзера с запросом с заголовком авторизации
    response = client.post(url)

    assert response.status_code == 204


def test_posts(register_user_2, login_user_2, register_user_1, post_user_1):
    user = MyUser.objects.get(pk=register_user_1['id'])
    post = Post(title='PRIVET_TESTUSER_1_AGAIN', content='CONTENT_2', author=user)
    post.save()

    url = 'http://localhost:8000/api/v1/posts'

    client = APIClient()

    # просмотр постов с запросом без заголовка авторизации
    response = client.get(url)

    assert response.status_code == 403
    assert response.json()['detail'] == 'Учетные данные не были предоставлены.'

    client.credentials(HTTP_AUTHORIZATION='Token ' + login_user_2)

    # просмотр постов с запросом с заголовом авторизации
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.json()) != 0
    assert response.json()[0]['title'] == 'PRIVET_TESTUSER_1_AGAIN'
    assert response.json()[1]['title'] == 'PRIVET_TESTUSER_1'

    # добавление поста
    data = {'title': 'Post_user_test_2@mail.ru', 'content': 'Content of Post of User test_2@mail.ru'}
    url = 'http://localhost:8000/api/v1/posts'
    response = client.post(url, data=data)

    assert response.status_code == 201
    assert response.json()['title'] == "Post_user_test_2@mail.ru"

    # добавление уже существующего поста
    response = client.post(url, data=data)

    assert response.status_code == 400

    # добавление поста без обязательного поля
    data = {'title': 'Post_user_test_2@mail.ru again'}
    response = client.post(url, data=data)

    assert response.status_code == 400


def test_users(register_user_2, login_user_2, register_user_1):
    user = MyUser.objects.get(pk=register_user_1['id'])
    user.number_of_posts = 2
    user.save()

    user = MyUser(username='Third_User', email='third_user@mail.ru')
    user.save()

    client = APIClient()

    url = 'http://localhost:8000/api/v1/users'

    # просмотр других юзеров с запросом без заголовка авторизации
    response = client.get(url)

    assert response.status_code == 403
    assert response.json()['detail'] == 'Учетные данные не были предоставлены.'

    client.credentials(HTTP_AUTHORIZATION='Token ' + login_user_2)

    # просмотр других юзеров с запросом с заголовом авторизации
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.json()) != 0

    # просмотр других юзеров с сортировкой по количеству постов
    url = 'http://localhost:8000/api/v1/users?ordering=number_of_posts'
    response = client.get(url)

    assert response.status_code == 200
    assert len(response.json()) != 0
    assert response.json()[0]['username'] == 'Third_User'


def test_add_del_post_to_sub(register_user_2, login_user_2, post_user_1):
    client = APIClient()

    url = 'http://localhost:8000/api/v1/posts/' + f'{post_user_1.id}'

    # добавление поста в ленту подписок с запросом без заголовка авторизации
    response = client.get(url)

    assert response.status_code == 403
    assert response.json()['detail'] == 'Учетные данные не были предоставлены.'

    client.credentials(HTTP_AUTHORIZATION='Token ' + login_user_2)

    # добавление поста в ленту подписок с запросом с заголовом авторизации
    response = client.get(url)

    assert response.status_code == 200
    assert response.json()['message'] == "Post PRIVET_TESTUSER_1 was added to your's subscriptions!!"
    assert len(Subscriptions.objects.filter(user__id=register_user_2['id'])) != 0

    # добавление поста в ленту подписок, если он там уже есть
    response = client.get(url)

    assert response.status_code == 400
    assert response.json()['message'] == "You are already subscribed to this post!!"

    # добавление поста из ленты подписок
    response = client.delete(url)

    assert response.status_code == 200
    assert response.json()['message'] == "Post PRIVET_TESTUSER_1 was deleted from your's subscriptions!!"
    assert len(Subscriptions.objects.filter(user__id=register_user_2['id'])) == 0

    # добавление поста из ленты подписок,если его нет в ленте
    response = client.delete(url)

    assert response.status_code == 404
    assert response.json()['message'] == "Subscriptions matching query does not exist."


def test_user_subs_list(register_user_2, login_user_2, register_user_1):
    user_1 = MyUser.objects.get(pk=register_user_1['id'])
    user_2 = MyUser.objects.get(pk=register_user_2['id'])

    post = Post(title='User_1', content='User_1_Content', author=user_1)
    post.save()

    sub = Subscriptions(user=user_2, post=post, readed=True)
    sub.save()

    post = Post(title='User_1_Again', content='User_1_Content_Again', author=user_1)
    post.save()

    sub = Subscriptions(user=user_2, post=post)
    sub.save()

    client = APIClient()

    url = 'http://localhost:8000/api/v1/subs'

    # просмотр ленты подписок с запросом без заголовка авторизации
    response = client.get(url)

    assert response.status_code == 403
    assert response.json()['detail'] == 'Учетные данные не были предоставлены.'

    client.credentials(HTTP_AUTHORIZATION='Token ' + login_user_2)

    # просмотр ленты подписок с запросом с заголовом авторизации
    response = client.get(url)

    assert response.status_code == 200
    assert response.json()['results'][0]['post']['title'] == 'User_1_Again'
    assert response.json()['results'][0]['readed'] == False

    url = 'http://localhost:8000/api/v1/subs?readed=True'

    # просмотр ленты подписок с только прочитанными постами
    response = client.get(url)

    assert response.status_code == 200
    assert response.json()['results'][0]['post']['title'] == 'User_1'
    assert response.json()['results'][0]['readed'] == True


def test_read_sub_and_mark_readed(register_user_2, login_user_2, sub_user_2):
    client = APIClient()

    url = 'http://localhost:8000/api/v1/subs/' + f'{sub_user_2.id}'

    # просмотр подписки и связанного с ней поста с запросом без заголовка авторизации
    response = client.get(url)

    assert response.status_code == 403
    assert response.json()['detail'] == 'Учетные данные не были предоставлены.'

    client.credentials(HTTP_AUTHORIZATION='Token ' + login_user_2)

    # просмотр подписки и связанного с ней поста с запросом с заголовком авторизации
    response = client.get(url)

    assert response.status_code == 200
    assert response.json()['post']['title'] == 'PRIVET_TESTUSER_1'
    assert response.json()['readed'] == False

    # отметка о прочтении поста
    data = {'readed': True}
    response = client.put(url, data=data)

    assert response.status_code == 200
    assert response.json()['post']['title'] == 'PRIVET_TESTUSER_1'
    assert response.json()['readed'] == True

    # попытка изменить данные поста
    data = {'title': 'Wrong'}
    response = client.put(url, data=data)

    assert response.status_code == 200
    assert response.json()['post']['title'] == 'PRIVET_TESTUSER_1'
    assert response.json()['readed'] == False
