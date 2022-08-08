import pytest
from django.conf import settings
from blog.models import MyUser, Post, Subscriptions


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myblog',
        'USER': 'postgres',
        'PASSWORD': '12345',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }


@pytest.fixture()
def register_user_1(django_db_setup, client, db):
    url = 'http://localhost:8000/api/v1/auth/users/'
    data = {'email': 'test@mail.ru', 'password': 'qwerty654321', 'username': 'Sveta'}
    response = client.post(url, data=data)

    return response.json()


@pytest.fixture()
def login_user_1(django_db_setup, client, register_user_1):
    url = 'http://localhost:8000/api/v1/token/login/'
    data = {'email': 'test@mail.ru', 'password': 'qwerty654321'}
    response = client.post(url, data=data)
    token = response.json()['auth_token']

    return token


@pytest.fixture()
def register_user_2(django_db_setup, client, db):
    url = 'http://localhost:8000/api/v1/auth/users/'
    data = {'email': 'test_2@mail.ru', 'password': 'qwerty08060402', 'username': 'Borya'}
    response = client.post(url, data=data)

    return response.json()


@pytest.fixture()
def login_user_2(django_db_setup, client, register_user_2):
    url = 'http://localhost:8000/api/v1/token/login/'
    data = {'email': 'test_2@mail.ru', 'password': 'qwerty08060402'}
    response = client.post(url, data=data)
    token = response.json()['auth_token']

    return token


@pytest.fixture()
def post_user_1(django_db_setup, register_user_1):
    user = MyUser.objects.get(pk=register_user_1['id'])
    post = Post(title='PRIVET_TESTUSER_1', content='CONTENT', author=user)
    post.save()

    return post


@pytest.fixture()
def sub_user_2(django_db_setup, post_user_1, register_user_2):
    user = MyUser.objects.get(pk=register_user_2['id'])

    sub = Subscriptions(user=user, post=post_user_1)
    sub.save()

    return sub
