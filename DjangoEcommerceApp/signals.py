# from django.db.models.signals import post_save
# from .models import CustomUser,AdminUser, MerchantUser,StaffUser
# from django.dispatch import receiver


# @receiver(post_save,sender=CustomUser)
# def create_user_profile(sender, instance, created, **kwargs):
#     if created:
#         if instance.user_type==1:
#             AdminUser.objects.create(auth_user_id=instance)
#         if instance.user_type==2:
#             StaffUser.objects.create(auth_user_id=instance)
#         if instance.user_type==3:
#             MerchantUser.objects.create(auth_user_id=instance,company_name="",gst_details="",address="")
#         if instance.user_type==4:
#             CustomUser.objects.create(auth_user_id=instance)

# @receiver(post_save,sender=CustomUser)
# def save_user_profile(sender, instance,**kwargs):
#     if instance.user_type==1:
#         instance.adminuser.save()
#     if instance.user_type==2:
#         instance.staffuser.save()
#     if instance.user_type==3:
#         instance.merchantuser.save()
#     if instance.user_type==4:
#         instance.customuser.save()

