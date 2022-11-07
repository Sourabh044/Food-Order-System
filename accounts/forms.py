from django import forms
from .models import User, UserProfile

from .validators import allow_only_images
class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = [
            "first_name",
            "last_name",
            "username",
            "email",
            "phone_number",
            "password",
            "confirm_password",
        ]

    def clean(self):
        cleaned_data = super(UserRegisterForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")
        if not password == confirm_password:
            raise forms.ValidationError("Password does not match!")


class UserProfileForm(forms.ModelForm):
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_images,])
    cover_photo = forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_images,])
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Start Typing...','required':'required'}))
    # latitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    # longitude = forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model = UserProfile
        fields = [
            "profile_picture",
            "cover_photo",
            "address",
            "country",
            "state",
            "city",
            "pincode",
            "latitude",
            "longitude",
        ]

    def __init__(self, *args, **kwargs) :
        super(UserProfileForm,self).__init__(*args,**kwargs)    
        for field in self.fields:
            if field == 'longitude' or field == 'latitude':
                self.fields[field].widget.attrs['readonly'] = 'readonly'
