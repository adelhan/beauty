from django.db import models
from account.models import User


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, primary_key=True)
    parent = models.ForeignKey('self',
                               related_name='children',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True)

    def __str__(self):
        if self.parent:
            return f'{self.parent} -> self.title'
        return self.title


class Place(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, primary_key=True)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    categories = models.ManyToManyField(Category)
    parent = models.ForeignKey('self',
                               related_name='children',
                               on_delete=models.CASCADE,
                               null=True,
                               blank=True)

    def __str__(self):
        if self.parent:
            return f'{self.parent} -> self.title'
        return self.title


class Master(models.Model):
    name = models.CharField(max_length=255, unique=True)
    surname = models.CharField(max_length=255, null=False)
    places = models.ForeignKey(Place, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class MasterImage(models.Model):
    master = models.ForeignKey(Master, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='masters', null=True, blank=True)


class Application(models.Model):
    master = models .ForeignKey(Master, on_delete=models.CASCADE)
    time = models.DateTimeField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=User)

    def __str__(self):
        return self.user


class Comment(models.Model):
    master = models.ForeignKey(Master, on_delete=models.CASCADE)
    text = models.CharField(max_length=100)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.author}: {self.text}"
