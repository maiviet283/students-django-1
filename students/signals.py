import os
from django.db.models.signals import pre_save, post_delete
from django.dispatch import receiver
from .models import *

# Xóa ảnh cũ khi cập nhật ảnh mới
@receiver(pre_save, sender=Students)
def delete_old_avatar_on_update(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_avatar = Students.objects.get(pk=instance.pk).avata
        except Students.DoesNotExist:
            return
        new_avatar = instance.avata
        # So sánh nếu ảnh mới khác ảnh cũ, xóa ảnh cũ
        if old_avatar and old_avatar != new_avatar:
            if os.path.isfile(old_avatar.path):
                os.remove(old_avatar.path)

# Xóa ảnh khi xóa tài khoản
@receiver(post_delete, sender=Students)
def delete_avatar_on_delete(sender, instance, **kwargs):
    if instance.avata:
        if os.path.isfile(instance.avata.path):
            os.remove(instance.avata.path)

@receiver(pre_save, sender=Book)
def delete_old_avatar_on_update(sender, instance, **kwargs):
    if instance.pk:
        try:
            old_avatar = Book.objects.get(pk=instance.pk).avata
        except Book.DoesNotExist:
            return
        new_avatar = instance.avata
        # So sánh nếu ảnh mới khác ảnh cũ, xóa ảnh cũ
        if old_avatar and old_avatar != new_avatar:
            if os.path.isfile(old_avatar.path):
                os.remove(old_avatar.path)

# Xóa ảnh khi xóa tài khoản
@receiver(post_delete, sender=Book)
def delete_avatar_on_delete(sender, instance, **kwargs):
    if instance.avata:
        if os.path.isfile(instance.avata.path):
            os.remove(instance.avata.path)
