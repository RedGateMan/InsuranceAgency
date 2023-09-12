from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from MyAuth.models import User


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=50, help_text="Required")

	class Meta:
		model = User
		fields = ('email', 'username', 'phone', 'password1', 'password2', 'name', 'surname', 'patronymic')

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			user = User.objects.get(email=email)
		except Exception as e:
			return email
		raise forms.ValidationError(f'Email: {email} is already in use.')

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			user = User.objects.get(username=username)
		except Exception as e:
			return username
		raise forms.ValidationError(f'Username: {username} is already in use.')


class LoginForm(forms.ModelForm):
	email = forms.EmailField(max_length=50, help_text="Required", widget=forms.EmailInput)
	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = User
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid Login")
