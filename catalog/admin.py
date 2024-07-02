from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from catalog.models import LiteraryFormat, Book, Author


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    # list_display refers to displaying of the list of objects in an admin panel
    list_display = ("title", "price", "format")
    list_filter = ("format",)
    search_fields = ("title",)


@admin.register(Author)
class AuthorAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ("psuedonym",)
    fieldsets = UserAdmin.fieldsets + (("Additional info", {"fields": ("psuedonym",)}),)  # adding a section with a field
    add_fieldsets = UserAdmin.add_fieldsets + (("Additional info", {"fields": ("first_name", "last_name", "psuedonym",)}),)  # adding a section with not mandatory fields for adding data


admin.site.register(LiteraryFormat)
# admin.site.register(Book, BookAdmin)  this can be replaced with decorator
# admin.site.register(Author, UserAdmin)  replaced with decorator
