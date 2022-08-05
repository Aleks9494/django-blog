from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError

from .models import MyUser, Post, Subscriptions


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = MyUser
        fields = ('email', 'username')

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = MyUser
        fields = ('email', 'password', 'username', 'is_active', 'is_admin')

    def clean_password(self):
        return self.initial["password"]


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('username', 'email', 'time_create', 'number_of_posts', 'is_active', 'is_admin')  # показывать на странице категории в admin
    search_fields = ('email',)  # поиск по имени сверху
    list_filter = ('email',)  # поиск по фильтрам справа
    list_editable = ('number_of_posts', 'is_active', 'is_admin', )
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'number_of_posts')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),
        }),
    )


admin.site.register(MyUser, UserAdmin)
admin.site.unregister(Group)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'content', 'time_create', 'author')  # показывать на странице категории в admin
    search_fields = ('title', 'author',)  # поиск по имени сверху
    list_filter = ('title', 'author',)  # поиск по фильтрам справа


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'get_author_of_post_email', 'readed')  # показывать на странице категории в admin
    search_fields = ('user', 'post',)  # поиск по имени сверху
    list_filter = ('user', 'post',)  # поиск по фильтрам справа

    @staticmethod
    def get_author_of_post_email(obj):
        return obj.post.author.email
