from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password

# Create your models here.


class User(AbstractUser):
    pass

    def save(self, *args, **kwargs):
        if self.pk is not None:  # Kiểm tra xem đã có ID (đã tồn tại trong cơ sở dữ liệu) hay chưa
            orig = User.objects.get(pk=self.pk)
            if orig.password != self.password:
                self.password = make_password(self.password)
        else:
            self.password = make_password(self.password)
        # url = self.avatar
        # if 'https://res.cloudinary.com/dyfzuigha/' not in self.avatar:
        #     self.avatar = 'https://res.cloudinary.com/dyfzuigha/' + url
        super().save(*args, **kwargs)


@receiver(post_migrate)
def create_superuser(sender, **kwargs):

    u, created = User.objects.get_or_create(username='admin', password='123', is_staff=True, is_superuser=True)