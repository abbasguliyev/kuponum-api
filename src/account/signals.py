from django.db.models.signals import post_migrate, post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from django.contrib.auth import get_user_model
from account.api.utils import generate_referral_code
from account.api.selectors import user_list

User = get_user_model()

GROUPS = ['ADMIN', 'SELLER', 'CUSTOMER']

@receiver(post_migrate)
def create_groups(sender, **kwargs):
    if getattr(sender, "label", "") != "account":
        return
    for name in GROUPS:
        Group.objects.get_or_create(name=name)

@receiver(post_save, sender=User)
def assign_referral_code_signal(sender, instance, created, **kwargs):
    if created and not instance.referral_code:
        if not instance.referral_code:
            code = generate_referral_code()
            while user_list().filter(referral_code=code).exists():
                code = generate_referral_code()
            instance.referral_code = code
            instance.save(update_fields=["referral_code"])