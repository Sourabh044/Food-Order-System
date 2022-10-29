from django.db.models.signals import post_save, pre_save
from .models import User, UserProfile
from django.dispatch import receiver


@receiver(post_save, sender=User)
def post_save_create_profile(sender, instance, created, **kwargs):
    print(created)
    if created:
        UserProfile.objects.create(user=instance)
        print("Created User Profile")
    else:
        try:
            profile = UserProfile.objects.get(user=instance)
            profile.save()
            print("user is updated!!!!!!!!!!!!!!!")
        except:
            # creating new user profile
            UserProfile.objects.create(user=instance)
            print("profile created!.")


@receiver(pre_save, sender=User)
def pre_save_profile_reciever(sender, instance, **kwargs):
    print(instance.username, "user is being saved")


# post_save.connect(post_save_create_profile, sender=User)
