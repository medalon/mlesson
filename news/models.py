from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager,
                    self).get_queryset().filter(status='published')


class News(models.Model):
    objects = models.Manager()
    published = PublishedManager()
    
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=150, unique_for_date='publish')
    author = models.ForeignKey(User,
                                on_delete=models.CASCADE,
                                related_name='news')
    txt = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10,
                                choices=STATUS_CHOICES,
                                default='draft')
    comments = GenericRelation(Comment)

    class Meta:
        ordering = ('-publish',)
        verbose_name = "Новость"
        verbose_name_plural = "Новости"

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('news:news_detail',
                        args=[self.publish.year,
                            self.publish.month,
                            self.publish.day, self.slug])


