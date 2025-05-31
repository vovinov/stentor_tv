from django.db import models

from utils.models import TimeWrappedModel
from users.models import User


class News(TimeWrappedModel):

	title = models.CharField(max_length=255, null=False, unique=True)
	content = models.TextField()
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.ForeignKey("Category", on_delete=models.DO_NOTHING,  default="Main")

	def __str__(self):
		return self.title

	class Meta:
		verbose_name = "Новость"
		verbose_name_plural = "Новости"


class Category(TimeWrappedModel):

	title = models.CharField(max_length=255, blank=True, null=True)

	def __str__(self):
		return self.attr_name

	class Meta:
		verbose_name = "Категория"
		verbose_name_plural = "Категории"
