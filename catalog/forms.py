from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm

from catalog.models import Author, Book


class AuthorCreationForm(UserCreationForm):

    class Meta(UserCreationForm.Meta):
        model = Author
        fields = UserCreationForm.Meta.fields + ("first_name", "last_name", "psuedonym",)


# create view for editing MultipleChoiceField
class BookForm(forms.ModelForm):
    authors = forms.ModelMultipleChoiceField(
        queryset=get_user_model().objects.all(),
        widget=forms.CheckboxSelectMultiple(),  # choose another widget
        required=False  # add books with no authors
    )

    class Meta:
        model = Book
        fields = "__all__"


class BookSearchForm(forms.Form):  # inherits from Form, since it doesn't interact with models directly
    title = forms.CharField(
        max_length=255,
        required=False,
        label="",
        widget=forms.TextInput(
            attrs={
                "placeholder": "Search by title"
            }
        )
    )
