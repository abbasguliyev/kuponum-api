from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser, BaseUserManager
from account.api.utils import generate_referral_code

class CustomUserManager(BaseUserManager):
    def create_user(self, email, phone=None, password=None, **extra_fields):
        if not email:
            raise ValueError(_('The Email field must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, phone=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, phone, password, **extra_fields)

class User(AbstractUser):
    username = None
    email = models.EmailField(_('e-poçt'), unique=True)
    phone = models.CharField(_('telefon'), max_length=32, null=True, blank=True, unique=False)
    referral_code = models.CharField(_('referal kodu'), max_length=16, unique=True, editable=False)
    referred_by = models.ForeignKey('self', verbose_name=_('referal edən'), on_delete=models.SET_NULL, null=True, blank=True, related_name='referrals')
    region = models.ForeignKey('regions.Region', verbose_name=_('region'), on_delete=models.SET_NULL, null=True, blank=True, related_name='users')
    is_guest = models.BooleanField(_('qonaq'), default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        db_table = 'users'
        verbose_name = _('user')
        verbose_name_plural = _('users')

        indexes = [
            models.Index(fields=['referral_code'], name='user_referral_code_idx'),
            models.Index(fields=['referred_by'], name='user_referred_by_idx'),
        ]

        constraints = [
            models.UniqueConstraint(fields=["phone"], name="unique_phone", condition=~models.Q(phone=None)),
            models.CheckConstraint(
                check=models.Q(referred_by__isnull=True) | ~models.Q(pk=models.F("referred_by")),
                name="no_self_referral",
            ),
        ]