from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from regions.models import Region

User = get_user_model()

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    referred_by_code = serializers.CharField(required=False, allow_blank=True)
    region = serializers.PrimaryKeyRelatedField(queryset=Region.objects.all(), required=False)


    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone', 'region', 'password', 'referred_by_code']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'email', 'first_name', 'last_name', 'phone', 'referral_code', 
            'referred_by', 'is_guest', 'region', 'date_joined', 'last_login'
        ]
        read_only_fields = ['id', 'referral_code', 'date_joined', 'last_login']

class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone', 'region']


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True, min_length=6)

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError(_("Old password is incorrect."))
        return value

    def validate_new_password(self, value):
        if len(value) < 6:
            raise serializers.ValidationError(_("New password must be at least 6 characters long."))
        return value