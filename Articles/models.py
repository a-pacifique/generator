# models.py
from django.db import models
from django.utils.text import slugify
from django.urls import reverse


class Article(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='news_images/', blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    pcode = models.CharField(max_length=50, blank=True, null=True)


    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # Assuming you have an 'article_detail' view for displaying the article
        return reverse('article_detail', args=[str(self.slug)])

    def __str__(self):
        return self.title
