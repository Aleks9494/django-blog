import pytest

from blog.models import MyUser

# @pytest.mark.django_db
# def test_create_user():
#     MyUser.objects.create_user(username='user', email='user@mail.ru', password='password')
#     assert MyUser.objects.count() == 1

# def test_2(user):
#     print('user_2')
#     user = MyUser(username='Igor', email='a23111@mail.ru', password='654321')
#     user.save()
#
#     assert 1 == 1

# def test_register(client, db):
#     url = 'http://localhost:8000/api/v1/auth/users/'
#     data = {'email': 'a23@mail.ru', 'password': 'qwerty123654', 'username': 'Sveta'}
#     response = client.post(url, data=data)
#
#     assert response.status_code == 400
#
#     data = {'email': 'test@mail.ru', 'password': 'qwerty555555', 'username': 'Lena'}
#     response = client.post(url, data=data)
#
#     assert response.status_code == 201
#     assert response.json()['email'] == 'test@mail.ru'


# def test_3(client, db):
#     url = 'http://localhost:8000/api/v1/token/login/'
#     data = {'email': 'wrong@mail.ru', 'password': 'qwerty123654'}
#     response = client.post(url, data=data)
#
#     assert response.status_code == 400
#
#     data = {'email': 'a23@mail.ru', 'password': '654321'}
#     response = client.post(url, data=data)
#
#     assert 1 == 2

def test_register(client, db, register_user):
    url = 'http://localhost:8000/api/v1/auth/users/'
    data = {'email': 'test@mail.ru', 'password': 'qwerty654321', 'username': 'Sveta'}
    response = client.post(url, data=data)

    assert response.status_code == 400

def test_login(client, db, register_user):
    url = 'http://localhost:8000/api/v1/token/login/'
    data = {'email': 'wrong@mail.ru', 'password': 'qwerty123654'}
    response = client.post(url, data=data)

    assert response.status_code == 400

    data = {'email':'test@mail.ru', 'password':'qwerty654321'}
    response = client.post(url, data=data)

    assert response.status_code == 200
    assert response.json().get('auth_token')



