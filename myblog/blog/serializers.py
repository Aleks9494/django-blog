from rest_framework import serializers

from .models import Post, MyUser, Subscriptions


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'username', 'email', 'time_create', 'number_of_posts')


class PostSerializer(serializers.ModelSerializer):
    author_email = serializers.CharField(read_only=True, source="author.email")
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Post
        fields = ('id', 'title', 'content', 'time_create', 'author', 'author_email')

    def create(self, validated_data):
        user = MyUser.objects.get(email=validated_data['author'])
        user.number_of_posts += 1
        user.save()

        return Post.objects.create(**validated_data)


class SubscriptionSerializer(serializers.ModelSerializer):
    post = PostSerializer(read_only=True)

    class Meta:
        model = Subscriptions
        fields = ('id', 'post', 'readed')
