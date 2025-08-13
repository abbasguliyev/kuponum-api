from celery import shared_task
from django.contrib.auth import get_user_model
from account.api.utils import generate_referral_code
from account.api.selectors import user_list

User = get_user_model()

# @shared_task
# def assign_referral_code(user_id):
#     user = user_list().get(id=user_id)
#     if not user.referral_code:
#         code = generate_referral_code()
#         while user_list().filter(referral_code=code).exists():
#             code = generate_referral_code()
#         user.referral_code = code
#         user.save(update_fields=["referral_code"])