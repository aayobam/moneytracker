from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    profile_image = models.ImageField(default="blankimage1.jpeg")

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=User)
def create_profile(instance, created, *args, **kwargs):
    if created:
        Profile.objects.get_or_create(user=instance)
        print("Profile Created")


@receiver(post_save, sender=User)
def update_profile(instance, created, *args, **kwargs):
    if created == False:
        instance.profile.save()
        print("Profile Updated")
