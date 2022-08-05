from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class MyUserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')

        if username is None:
            raise ValueError('Users must have a username.')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class MyUser(AbstractBaseUser):
    username = models.CharField(max_length=50, verbose_name='Имя')
    email = models.EmailField(
        verbose_name='Емайл',
        max_length=255,
        unique=True,
    )
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Создание')
    number_of_posts = models.IntegerField(default=0, verbose_name='Количество постов')
    is_active = models.BooleanField(default=True, verbose_name='Активен')
    is_admin = models.BooleanField(default=False, verbose_name='Админ')

    objects = MyUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    class Meta:
        verbose_name = 'Пользователь'  # название в админ-панели
        verbose_name_plural = 'Пользователи'  # для множественного числа
        ordering = ['username', 'time_create', 'number_of_posts']   # сортировка

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Post(models.Model):
    title = models.CharField(max_length=100, verbose_name='Заголовок', unique=True)
    content = models.TextField(verbose_name='Контент')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Создание')
    author = models.ForeignKey(MyUser, related_name='get_posts',
                                 on_delete=models.CASCADE, verbose_name='Автор')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Пост'  # название в админ-панели
        verbose_name_plural = 'Посты'  # для множественного числа
        ordering = ['title', 'time_create']   # сортировка


class Subscriptions(models.Model):
    user = models.ForeignKey(MyUser, related_name='subs',
                                 on_delete=models.CASCADE, verbose_name='Юзер')
    post = models.ForeignKey(Post, related_name='+',
                                 on_delete=models.CASCADE, verbose_name='Пост')
    readed = models.BooleanField(default=False, verbose_name='Прочитан')

    class Meta:
        verbose_name = 'Подписка'  # название в админ-панели
        verbose_name_plural = 'Подписки'  # для множественного числа
        ordering = ['user', 'post']   # сортировка
