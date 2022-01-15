#Create the Custom Form here using the default UserCreationForm 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import fields
from user.models import  Profile, Review, UserDetail

class CustomUserCreationForm(forms.Form):
    username = forms.CharField(label='Enter Username', min_length=4, max_length=150)
    email = forms.EmailField(label='Enter email')
    password1 = forms.CharField(label='Enter password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

#  form.cleaned_data returns a dictionary of validated form input fields 
# and their values, where string primary keys are returned as objects.
    def clean_username(self):
        username = self.cleaned_data['username'].lower()
        r = User.objects.filter(username=username)
        if r.count():
            raise  ValidationError("Username already exists")
        return username

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise  ValidationError("Email already exists")
        return email

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise ValidationError("Password don't match")

        return password2

    def save(self, commit=True):
        user = User.objects.create_user(
            self.cleaned_data['username'],
            self.cleaned_data['email'],
            self.cleaned_data['password1'],
        )
        return user


class ProfileForm(forms.ModelForm)  :
    class Meta:
        model= Profile 
        fields=['balance']  


class ReviewForm(forms.ModelForm):
    class Meta:
        model =Review
        fields=['description']

class UserAddressForm(forms.ModelForm):
	# address = forms.CharField(widget=forms.TextInput(attrs={}))
	# locality = forms.CharField(required =True)
	# city = forms.CharField(required =True)
	# alternate_mobile = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Alternate Mobile No(optional)'}), required = False)
	# landmark = forms.CharField(widget=forms.TextInput(attrs={'placeholder':'Landmark(optional)'}), required = False)
	class Meta:
		model = UserDetail
		fields = [		
			'address',
			'pincode',
			'landmark',
			'locality',
			'city',
			'state',
		]        

class UpdateUserDetailForm(forms.ModelForm):
	class Meta:
		model = UserDetail
		fields = [
			'dob',
			'mobile',
		]        