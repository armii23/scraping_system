from django.db import models

# class Resource(models.Model):
#     title = models.CharField(max_length = 255)
#     url = models.TextField(blank = True)
#     created_at = models.DateTimeField(auto_now_add = True)
#
#     def __str__(self):
#         return self.title


class Category(models.Model):
    title = models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Internship(models.Model):
    title = models.CharField(max_length = 255)
    description = models.TextField(blank = True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['created_at']


# class User(models.Model):
#     firstname = models.CharField(max_length = 50)
#     last_name = models.CharField(max_length=50)
#     email = models.EmailField(unique=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     internships = models.ManyToManyField(Internship)
#
#     def __str__(self):
#         return self.firstname