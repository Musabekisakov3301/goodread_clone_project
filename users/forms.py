from django import forms
from django.core.mail import send_mail

from users.models import CustomUser

class UserCreateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'password')

    def save(self, commit=True):
        user = super().save(commit)
        user.set_password(self.cleaned_data['password'])
        user.save()
    
        return user

'''class UserCreateForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128)

    def save(self):
        username = self.changed_data['username']
        first_name = self.changed_data['first_name']
        last_name = self.changed_data['last_name']
        email = self.changed_data['email']
        password = self.changed_data['password']
            
        user = CustomUser.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email
        )
        user.set_password(password)
        user.save()

        return user'''

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'first_name', 'last_name', 'email', 'profile_picture')

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(max_length=128)