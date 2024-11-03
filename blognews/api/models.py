from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True, default='General')

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name

class Article(models.Model):
    title = models.CharField(max_length=200)
    body = RichTextUploadingField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="articles", default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="articles", default=1)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)
    comments = models.ManyToManyField('Comment', related_name='article_comments', blank=True)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return f'/articles/{self.id}/'
    
    def get_author(self):
        return self.author.username

class Image(models.Model):
    article = models.ForeignKey(Article, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/')

    def __str__(self):
        return f"Image for {self.article.title}"

class Comment(models.Model):
    article = models.ForeignKey(Article, related_name='article_comments', on_delete=models.CASCADE, default=1)
    author = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    body = models.TextField(default='No content')
    created_at = models.DateTimeField(auto_now_add=True, editable=False)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.article.title}"