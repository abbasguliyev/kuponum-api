from django.db.models import QuerySet, Prefetch
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

User = get_user_model()


def user_list() -> QuerySet[User]: # type: ignore
    return (
        User.objects.select_related('referred_by')
        .prefetch_related(Prefetch('groups', queryset=Group.objects.all()))
        .all()
    )