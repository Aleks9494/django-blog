from django.db.models import Q
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from .models import Post, MyUser, Subscriptions
from .serializers import PostSerializer, UsersSerializer, SubscriptionSerializer
from rest_framework.filters import OrderingFilter


# просмотр постов (не своих), отсортированных по дате создание сначала свежие, создание поста
class PostsApiView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return Post.objects.filter(~Q(author__id=self.request.user.id)).order_by('-time_create')


# просмотр пользователей, кроме себя и админа, с возможностью сортировки по количеству постов
# /api/v1/users?ordering=number_of_posts - сортировка
class UsersApiView(generics.ListAPIView):
    serializer_class = UsersSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = [OrderingFilter]
    ordering_fields = ['number_of_posts']  # сортировка по количеству постов

    def get_queryset(self):
        return MyUser.objects.filter(~Q(pk=self.request.user.id) & Q(is_admin=False))
        # id не равно id аутентифицорованного юзера и не админ


class SubsriptionUserApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        try:
            post = Post.objects.get(pk=self.kwargs['pk'])
            user = MyUser.objects.get(pk=self.request.user.id)
            sub = Subscriptions.objects.filter(user=user, post=post).exists()
            if sub:
                return JsonResponse({'message': "You are already subscribed to this post!!"},
                                    status=status.HTTP_400_BAD_REQUEST)

            sub = Subscriptions(user=user, post=post)
            sub.save()
        except Exception as e:
            return JsonResponse({'message': f'{e}'}, status=status.HTTP_404_NOT_FOUND)

        return JsonResponse({'message': f"Post {post.title} was added to your's subscriptions!!"})

    def delete(self, request, **kwargs):
        try:
            sub = Subscriptions.objects.get(post__id=self.kwargs['pk'], user_id=self.request.user.id)
            sub.delete()
        except Exception as e:
            return JsonResponse({'message': f'{e}'}, status=status.HTTP_404_NOT_FOUND)

        return JsonResponse({'message': f"Post {sub.post} was deleted from your's subscriptions!!"})


class SubscriptionsListApiViewPagination(PageNumberPagination):
    page_size = 10 # количество на странице по умолчанию
    page_size_query_param = 'page_size' # параметр в запросе для изменения количества
    max_page_size = 100  # максомальная величина для параметра page_size


# /api/v1/subs?readed=True - фильтрация
class SubscriptionsListApiView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SubscriptionSerializer
    pagination_class = SubscriptionsListApiViewPagination
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['readed']

    def get_queryset(self):
        if getattr(self, "swagger_fake_view", False):
            return Subscriptions.objects.none()
        return Subscriptions.objects.filter(user=self.request.user).order_by('-post__time_create')


# GET - просмотр подписки и поста, PUT - отметка о прочтении
class SubApiView(generics.RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = SubscriptionSerializer
    queryset = Subscriptions.objects.all()

    def get_object(self):
        if getattr(self, "swagger_fake_view", False):
            return Subscriptions.objects.none()
        return get_object_or_404(Subscriptions, pk=self.kwargs['pk'], user=self.request.user)


