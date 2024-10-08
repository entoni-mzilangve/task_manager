from typing import cast
import django_filters
from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework_extensions.mixins import NestedViewSetMixin
from main.services.single_resource import SingleResourceMixin, SingleResourceUpdateMixin
from .models import Tag, Task, User
from .serializers import TagSerializer, TaskSerializer, UserSerializer


class DeleteAdminOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        if request.method == "DELETE":
            return bool(request.user and request.user.is_staff)
        return True


class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(field_name="username", lookup_expr="icontains")

    class Meta:
        model = User
        fields = ("username",)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.order_by("id")
    serializer_class = UserSerializer
    filterset_class = UserFilter


class CurrentUserViewSet(
    SingleResourceMixin, SingleResourceUpdateMixin, viewsets.ModelViewSet
):
    serializer_class = UserSerializer
    queryset = User.objects.order_by("id")

    def get_object(self) -> User:
        return cast(User, self.request.user)


class UserTasksViewSet(NestedViewSetMixin, viewsets.ReadOnlyModelViewSet):
    queryset = (
        Task.objects.order_by("id")
        .select_related("author", "executor")
        .prefetch_related("tags")
    )
    serializer_class = TaskSerializer


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.order_by("id")
    serializer_class = TagSerializer
    permission_classes = (
        DeleteAdminOnly,
        IsAuthenticated,
    )


class TaskTagsViewSet(viewsets.ModelViewSet):
    serializer_class = TagSerializer
    
    def get_queryset(self):
        task_id = self.kwargs["parent_lookup_task_id"]
        return Task.objects.get(pk=task_id).tags.all()


class TaskFilter(django_filters.FilterSet):
    state = django_filters.CharFilter(lookup_expr="iexact")
    tags = django_filters.CharFilter(field_name="tags__name", lookup_expr="in")
    executor = django_filters.CharFilter(
        field_name="executor__username",
        lookup_expr="icontains",
    )
    author = django_filters.CharFilter(
        field_name="author__username",
        lookup_expr="icontains",
    )

    class Meta:
        model = Task
        fields = ("state", "tags", "executor", "author")


class TaskViewSet(viewsets.ModelViewSet):
    queryset = (
        Task.objects.select_related("author", "executor")
        .prefetch_related("tags")
        .order_by("id")
    )
    serializer_class = TaskSerializer
    filterset_class = TaskFilter
    permission_classes = (
        DeleteAdminOnly,
        IsAuthenticated,
    )
