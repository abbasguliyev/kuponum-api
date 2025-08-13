from django_filters import rest_framework as filters
from django.contrib.auth import get_user_model

User = get_user_model()

class UserFilter(filters.FilterSet):
    class Meta:
        model = User
        fields = {
            'email': ['exact', 'icontains'],
            'is_guest': ['exact'],
            'region': ['exact'],
            'referred_by': ['exact'],
        }