from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    title = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['title']


class Internship(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    link = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)
    users = models.ManyToManyField(User)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_at']


class Keyword(models.Model):
    keyword = models.CharField(max_length=60)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.keyword

    class Meta:
        ordering = ['keyword']

