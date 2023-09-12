from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from django.urls import path

from Lab_4 import settings
from news.views import ArticleCreateView, NewsView
from polls.views import OfficeView, ContractView, ProfileView, CreateContractView, CreateObjectView

urlpatterns = [
	path('create/', login_required(ArticleCreateView.as_view(), login_url='/auth/login'),
		 name='create_article'),
	path('', NewsView.as_view(), name='news'),
]
