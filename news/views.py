from django.shortcuts import render, redirect
from django.views import View
from django.views.generic import ListView

from MyAuth.models import User
from news.forms import ArticleCreateForm
from news.models import Article


class ArticleCreateView(View):
	model = Article

	def get(self, request, **kwargs):
		context = {}
		form = ArticleCreateForm()
		context['form'] = form
		#context['user_id'] = kwargs['user_id']
		return render(request, 'article_create.html', context)

	def post(self, request, *args, **kwargs):
		form = ArticleCreateForm(request.POST)

		if form.is_valid():
			# user = User.objects.get(id=kwargs['user_id'])
			user = request.user
			article = Article(title=request.POST['title'], content=request.POST['content'], author=user, )
			article.save()
			return redirect('home')


class LatestArticleView(ListView):
	model = Article
	allow_empty = True

	def get_queryset(self):
		return ArticleListView().get_queryset().order_by('-created_at')[:1]


class ArticleListView(ListView):
	model = Article
	allow_empty = True

	def get_queryset(self, *args, **kwargs):
		return Article.objects.all()


class NewsView(View):

	def get(self, request):
		context = {}
		articles_list = ArticleListView().get_queryset()
		return render(request, 'news.html', context={'article_list': articles_list})
