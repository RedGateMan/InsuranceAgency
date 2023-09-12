from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from MyAuth.utils import construct_errors_msg
from polls.forms import ContractCreateForm, ProfileForm, ObjectCreateForm
from polls.models import Office, Insurance, Agent, Contract, Object
from MyAuth.models import User


class OfficeListView(ListView):
	model = Office
	allow_empty = True

	def get_queryset(self):
		return Office.objects.all()


class InsuranceListView(ListView):
	model = Insurance
	allow_empty = True

	def get_queryset(self):
		return Insurance.objects.all()


class AgentsListView(ListView):
	model = Agent
	allow_empty = True

	def get_queryset(self):
		return Agent.objects.all()


class ContractListView(ListView):
	model = Contract
	allow_empty = True

	def get_queryset(self, *args, **kwargs):
		return Contract.objects.filter(**kwargs)


class OfficeView(View):
	model = Office
	allow_empty = True

	def get(self, request, *args, **kwargs):
		context = {}
		office_index = kwargs['office_id']
		agents = Agent.objects.filter(office__id=office_index)
		office = Office.objects.get(id=office_index)
		context['office'] = office
		context['agent_list'] = agents
		return render(request, 'office_detail.html', context)


class CreateObjectView(View):
	model = Object

	def get(self, request, *args, **kwargs):
		context = {}
		form = ObjectCreateForm()
		context['form'] = form
		context['agent_id'] = kwargs['agent_id']
		context['user_id'] = kwargs['user_id']
		return render(request, 'object.html', context)

	def post(self, request, *args, **kwargs):
		form = ObjectCreateForm(request.POST)

		if form.is_valid():
			user_object = Object(object_type=request.POST['object_type'], description=request.POST['description'])
			user_object.save()
			CreateContractView().post(
				request, agent_id=kwargs['agent_id'],
				user_id=kwargs['user_id'],
				object_id=user_object.id
			)
			return redirect('profile')


class CreateContractView(View):
	model = Contract

	def post(self, request, *args, **kwargs):
		user = request.user
		agent = Agent.objects.get(id=kwargs['agent_id'])
		object = Object.objects.get(id=kwargs['object_id'])
		contract = Contract(agent=agent, client=user, object=object)
		contract.save()
		# return render(request, 'contract.html', {'form': form})
		return redirect('profile')


class ContractView(View):
	model = Contract

	def get(self, request, new_context={}, *args, **kwargs):
		context = {}
		contract = Contract.objects.get(id=kwargs['contract_id'])
		form = ContractCreateForm()
		context['form'] = form
		context['contract'] = contract
		context.update(new_context)
		return render(request, 'contract.html', context)

	def post(self, request, *args, **kwargs):
		form = ContractCreateForm(request.POST)
		action = kwargs['action']
		if action is not 'DECLINED':
			contract = Contract.objects.get(id=kwargs['contract_id'])
			contract.status = action
			contract.insurance_id = request.POST['insurance']
			contract.cost = request.POST['cost']
			contract.save()
			return redirect('profile')
		else:
			if form.is_valid():
				contract = Contract.objects.get(id=kwargs['contract_id'])
				contract.status = action
				contract.insurance_id = request.POST['insurance']
				contract.cost = request.POST['cost']
				contract.save()
				return redirect('profile')
			else:
				context = {}
				context['errors'] = construct_errors_msg(form.errors)
				return self.get(request, new_context=context, contract_id=kwargs['contract_id'])


class ProfileView(View):
	model = Contract
	form_class = ProfileForm

	# @login_required(login_url='auth/login')
	def get(self, request, new_context={}, *args, **kwargs, ):
		user = request.user
		context = {}
		user_id = user.id
		salary = None
		if not user.is_staff:
			pending_contracts = ContractListView().get_queryset(client_id=user_id, status='PENDING')
			active_contracts = ContractListView().get_queryset(client_id=user_id, status="ACTIVE")
			declined_contracts = ContractListView().get_queryset(client_id=user_id, status="DECLINED")
		else:
			agent = Agent.objects.get(user_id=user_id)
			pending_contracts = ContractListView().get_queryset(agent_id=agent.id, status='PENDING')
			active_contracts = ContractListView().get_queryset(agent_id=agent.id, status="ACTIVE")
			declined_contracts = ContractListView().get_queryset(agent_id=agent.id, status="DECLINED")
			salary = agent.get_salary()
		context['pending_contracts'] = pending_contracts
		context['active_contracts'] = active_contracts
		context['declined_contracts'] = declined_contracts
		context['salary'] = salary
		context['form'] = ProfileForm(
			initial={'name': user.name, 'surname': user.surname, 'patronymic': user.patronymic, 'phone': user.phone, }
		)
		context.update(new_context)
		return render(request, 'profile.html', context)

	def post(self, request, *args, **kwargs):

		form = ProfileForm(request.POST)
		if form.is_valid():
			user = User.objects.get(id=request.user.id)
			user.name = request.POST['name']
			user.surname = request.POST['surname']
			user.patronymic = request.POST['patronymic']
			user.phone = request.POST['phone']
			user.save()
			return self.get(request, new_context={'success': True})
		else:
			context = {}
			context['errors'] = construct_errors_msg(form.errors)
			return self.get(request, new_context=context)
