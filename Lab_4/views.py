from django.http import HttpResponse
from django.shortcuts import render
from django.views import View

from Lab_4.utils import get_joke_of_the_day
from news.views import LatestArticleView
from polls.views import OfficeListView, InsuranceListView, AgentsListView


class HomeView(View):
	def get(self, request, *args, **kwargs):
		office_list = OfficeListView().get_queryset()
		insurance_list = InsuranceListView().get_queryset()
		agent_list = AgentsListView().get_queryset()
		article = LatestArticleView().get_queryset()
		joke_of_the_day = get_joke_of_the_day()
		return render(request, 'home.html',
					  context={
						  'office_list': office_list,
						  'insurance_list': insurance_list,
						  'agent_list': agent_list,
						  'joke': joke_of_the_day,
						  'article': article,
					  })


def custom_page_not_found_view(request, exception):
	return render(request, "404.html", {})


def custom_500_view(request, exception=None):
	return render(request, "500.html", {})
