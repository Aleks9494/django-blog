import pytest
from django.conf import settings
from blog.models import MyUser, Post


@pytest.fixture(scope='session')
def django_db_setup():
    print ('DB')
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myblog',
        'USER': 'postgres',
        'PASSWORD': '12345',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }


# @pytest.fixture()
# def user(django_db_setup, db):
#     user = MyUser(username='Igor', email='a23@mail.ru', password='654321')
#     user.save()
#
#     return user
#
#
# @pytest.fixture()
# def post(django_db_setup, db, user):
#     post = Post(title='Post of Igor', content='DDDDDDDDDDDDDDDD', author=user)
#     post.save()
#
#     return post

@pytest.fixture()
def register_user(django_db_setup, db, client):
    url = 'http://localhost:8000/api/v1/auth/users/'
    data = {'email': 'test@mail.ru', 'password': 'qwerty654321', 'username': 'Sveta'}
    response = client.post(url, data=data)

    return response.json()