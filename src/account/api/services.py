from dataclasses import dataclass
from typing import Optional
from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils.translation import gettext_lazy as _
from account.api.selectors import user_list
from regions.models import Region

User = get_user_model()

@dataclass(frozen=True)
class UserCreateInput:
    email: str
    password: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    referred_by_code: Optional[str] = None
    region: Optional[str] = None

@dataclass(frozen=True)
class UpdateUserInput:
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    phone: Optional[str] = None
    region: Optional[Region] = None


@transaction.atomic
def create_user(user_input: UserCreateInput) -> User: # type: ignore
    if user_list().filter(email=user_input.email).exists():
        raise ValueError(_("Bu email ilə istifadəçi artıq mövcuddur."))

    referred_by = None
    if user_input.referred_by_code:
        try:
            referred_by = user_list().get(referral_code=user_input.referred_by_code)
        except User.DoesNotExist:
            raise ValueError(_("Yanlış referal kod"))
    
    user = User.objects.create_user(
        email=user_input.email,
        password=user_input.password,
        first_name=user_input.first_name,
        last_name=user_input.last_name,
        phone=user_input.phone,
        region=user_input.region,
        referred_by=referred_by
    )
    return user

@transaction.atomic
def update_user(user, user_input: UpdateUserInput) -> User: # type: ignore
    update_fields = []
    if user_input.first_name is not None:
        user.first_name = user_input.first_name
        update_fields.append('first_name')
    if user_input.last_name is not None:
        user.last_name = user_input.last_name
        update_fields.append('last_name')
    if user_input.phone is not None:
        user.phone = user_input.phone
        update_fields.append('phone')
    if user_input.region is not None:
        user.region = user_input.region
        update_fields.append('region')
    user.save(update_fields=update_fields)
    return user

@transaction.atomic
def change_password(user: User, old_password: str, new_password: str) -> User: # type: ignore
    if not user.check_password(old_password):
        raise ValueError(_("Köhnə şifrə yanlışdır."))
    user.set_password(new_password)
    user.save()
    return user