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

    list_display = ('username', 'email', 'time_create', 'number_of_posts', 'is_active', 'is_admin')
    search_fields = ('email',)
    list_filter = ('email',)
    list_editable = ('is_active', 'is_admin', )
    filter_horizontal = ()

    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username', 'number_of_posts')}),
        ('Permissions', {'fields': ('is_admin',)}),
    )

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
    list_display = ('title', 'content', 'time_create', 'author')
    search_fields = ('title', 'author__email',)
    list_filter = ('author__email',)


@admin.register(Subscriptions)
class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'get_author_of_post_email', 'readed')
    search_fields = ('user__email', 'post__title',)
    list_filter = ('user__email', 'post__title',)

    @staticmethod
    def get_author_of_post_email(obj):
        return obj.post.author.email
