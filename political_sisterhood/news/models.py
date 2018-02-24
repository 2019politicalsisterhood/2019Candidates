from django.db import models
from political_sisterhood.candidate.models import Candidate
from ckeditor.fields import RichTextField
from model_utils import Choices
from model_utils.fields import StatusField


class NewsStoryQueryset(models.QuerySet):
    def published(self):
        return self.filter(stage='Published')


# Create your models here.
class NewsStory(models.Model):
    STAGES = Choices('Unpublished', 'Published')
    stage = StatusField(choices_name='STAGES')
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name="news")
    title = models.CharField(max_length=255, blank=True)
    teaser = RichTextField(blank=True)
    link = models.CharField(max_length=255, blank=True)
    image = models.ImageField(blank=True)
    date = models.DateField(blank=True)

    objects = NewsStoryQueryset.as_manager()

    class Meta:
        verbose_name_plural = "News Stories"

    def __str__(self):
        return self.title

    @property
    def meta(self):
        if self.date:
            return True

    @property
    def image_url(self):
        if self.image:
            return self.image.url
        return None