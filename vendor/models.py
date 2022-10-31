from django.db import models

from accounts.models import User, UserProfile

# Create your models here.

class Vendor(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    user_profile = models.OneToOneField(UserProfile,on_delete=models.CASCADE)
    vendor_name = models.CharField(max_length = 50)
    vendor_license = models.ImageField( upload_to='vendor/license')
    is_approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.vendor_name