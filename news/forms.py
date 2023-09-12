from django.forms import ModelForm

from news.models import Article


class ArticleCreateForm(ModelForm):
	class Meta:
		model = Article
		fields = ('title', 'content',)
