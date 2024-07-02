from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse


class LiteraryFormat(models.Model):
    name = models.CharField(max_length=63)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return self.name

""" make so, that authors are customers(users) of our service, the site, where
each author can come in and look through all books and formats, add new author,
add a new book to author"""
class Author(AbstractUser):
    psuedonym = models.CharField(max_length=63, null=True, blank=True)
    class Meta:
        ordering = ("username",)
    # when reimplement built-in User model django point about it
    # in settings: AUTH_USER_MODEL = "catalog.Author"

    def __str__(self):
        return f"{self.username}: ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("catalog:authors-detail", args=[str(self.id)])


class Book(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    format = models.ForeignKey(
        LiteraryFormat, on_delete=models.CASCADE, related_name="books"
    )
    authors = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="books")

    class Meta:
        ordering = ("title",)

    def __str__(self) -> str:
        return f"{self.title} (price: {self.price}, format: {self.format.name})"

    def get_absolute_url(self):
        return reverse("catalog:books-detail", args=[str(self.id)])
