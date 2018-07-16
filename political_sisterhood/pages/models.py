from django.db import models
from ckeditor.fields import RichTextField


# Create your models here.
class Page(models.Model):
    title = models.CharField(max_length=255)
    content = RichTextField()
    slug = models.SlugField()

    def __str__(self):
        return self.title