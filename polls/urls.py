from django.contrib.auth.decorators import login_required
from django.urls import path

from polls.views import OfficeView, ContractView, ProfileView, CreateContractView, CreateObjectView

urlpatterns = [
	path('office/<int:office_id>', OfficeView.as_view(), name='office'),
	path('contract/create/<int:user_id>/<int:agent_id>', login_required(CreateContractView.as_view()),
		 name='create_contract'),
	path('object/<int:user_id>/<int:agent_id>', login_required(CreateObjectView.as_view(), login_url='/auth/login'),
		 name='object'),
	path('object/create/<int:user_id>/<int:agent_id>',
		 login_required(CreateObjectView.as_view(), login_url='/auth/login'),
		 name='create_object'),
	path('contract/<int:contract_id>', login_required(ContractView.as_view()), name='contract'),
	path('contract/update/<int:contract_id>/<str:action>', login_required(ContractView.as_view()), name='update_contract'),
	path('profile/', login_required(ProfileView.as_view(), login_url='/auth/login'), name='profile'),
	path('profile/update/', login_required(ProfileView.as_view(), login_url='/auth/login'), name='update_profile'),
]
