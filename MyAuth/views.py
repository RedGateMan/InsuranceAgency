from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import CreateView

from MyAuth.forms import RegistrationForm, LoginForm
from MyAuth.models import User
from MyAuth.utils import construct_errors_msg


# Create your views here.

class RegistrationView(CreateView):
	model = User
	form_class = RegistrationForm
	template_name = 'MyAuth/register.html'

	def post(self, request, *args, **kwargs):
		user = request.user
		if user.is_authenticated:
			logout(request)

		context = {}

		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email').lower()
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(email=email, password=raw_password)
			login(request, user)
			return redirect('home')
		else:
			context['registration_form'] = form
			context['errors'] = construct_errors_msg(form.errors)
			return render(request, 'MyAuth/register.html', context)


class LogoutView(View):
	def get(self, request):
		logout(request)
		return redirect('home')


class LoginView(View):
	form_class = LoginForm

	def get(self, request, *args, **kwargs):
		user = request.user
		if user.is_authenticated:
			return redirect('home')
		else:
			return render(request, 'MyAuth/login.html')

	def post(self, request, *args, **kwargs):
		context = {}
		form = self.form_class(request.POST)

		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)
			if user:
				login(request, user)
				return redirect('home')
		else:
			context['login_form'] = form
			context['errors'] = construct_errors_msg(form.errors)
			return render(request, 'MyAuth/login.html', context)
