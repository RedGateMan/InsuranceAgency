from django.forms import ModelForm

from django import forms

from MyAuth.models import User
from polls.models import Contract, Object


class ObjectCreateForm(ModelForm):
	class Meta:
		model = Object
		fields = ('object_type', 'description')


class ContractCreateForm(ModelForm):

	def __init__(self, *args, **kwargs):
		super(ContractCreateForm, self).__init__(*args, **kwargs)

		for key in self.fields:
			self.fields[key].required = True

	class Meta:
		model = Contract
		fields = ('insurance', 'cost')



class ProfileForm(ModelForm):
	def __init__(self, *args, **kwargs):
		super(ProfileForm, self).__init__(*args, **kwargs)

		for key in self.fields:
			self.fields[key].required = True
	class Meta:
		model = User
		fields = ('name', 'surname', 'patronymic', 'phone',)

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
