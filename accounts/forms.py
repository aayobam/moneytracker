from accounts.models import Profile
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm



class UserRegister(UserCreationForm):
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder":"Enter first name"}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder":"Enter last name"}))
    email = forms.EmailField(max_length=100, widget=forms.EmailInput(attrs={"placeholder":"Enter email"}))
    username = forms.CharField(max_length=150, min_length=8, widget=forms.TextInput(attrs={"placeholder":"Enter Username"}))
    password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={"placeholder":"Enter password"}))
    password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={"placeholder":"Re-enter password"}))
    
    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email", "password1", "password2"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].widget.attrs.update({"class":"registeration"})
        self.fields["last_name"].widget.attrs.update({"class":"registeration"})
        self.fields["email"].widget.attrs.update({"class":"registeration"})
        self.fields["username"].widget.attrs.update({"class":"registeration"})
        self.fields["password1"].widget.attrs.update({"class":"registeration"})
        self.fields["password2"].widget.attrs.update({"class":"registeration"})
   


class AccountUpdateForm(forms.ModelForm):
    email = forms.EmailField(max_length=150, widget=forms.EmailInput(attrs={"placeholder":"Enter email"}))
    username = forms.CharField(max_length=100, widget=forms.TextInput(attrs={"placeholder":"Enter username"}))
    
    class Meta:
        model = User
        fields = ["first_name", "last_name", "username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].disabled=True
        self.fields["last_name"].disabled=True


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ["profile_image",]
        exclude = ["user"]