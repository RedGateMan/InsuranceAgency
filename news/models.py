from django.db import models

from MyAuth.models import User


# Create your models here.
class Article(models.Model):
	created_at = models.DateTimeField(auto_now_add=True)
	author = models.ForeignKey(User, null=False, blank=False, on_delete=models.CASCADE)
	title = models.TextField(max_length=150, default='Article Title')
	content = models.TextField()

	# @property
	# def first_sentence(self):
	# 	return

	# @classmethod
	# def create(cls, created_at, author, title, content):
	# 	article = cls(created_at=created_at, author=author, title=title, content=content)
	# 	return article
