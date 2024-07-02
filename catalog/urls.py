from django.urls import path


from catalog.views import (
    index,
    BookListView,
    BookDetailView,
    BookCreateView,
    BookUpdateView,
    AuthorListView,
    AuthorDetailView,
    AuthorCreateView,
    LiteraryFormatListView,
    LiteraryFormatCreateView,
    LiteraryFormatUpdateView,
    LiteraryFormatDeleteView,
)
urlpatterns = [
    path("", index, name="index"),
    path("literary-formats/", LiteraryFormatListView.as_view(), name="literary-formats-list"),
    path("literary-formats/create/", LiteraryFormatCreateView.as_view(), name="literary-formats-create"),
    path("literary-formats/<int:pk>/update/", LiteraryFormatUpdateView.as_view(), name="literary-formats-update"),
    path("literary-formats/<int:pk>/delete/", LiteraryFormatDeleteView.as_view(), name="literary-formats-delete"),
    path("books/", BookListView.as_view(), name="books-list"),
    path("books/create/", BookCreateView.as_view(), name="books-create"),
    path("books/<int:pk>/update/", BookUpdateView.as_view(), name="books-update"),
    path("books/<int:pk>/", BookDetailView.as_view(), name="books-detail"),
    path("authors/", AuthorListView.as_view(), name="authors-list"),
    path("authors/create/", AuthorCreateView.as_view(), name="authors-create"),
    path("authors/<int:pk>/", AuthorDetailView.as_view(), name="authors-detail"),
    # path("test-session/", test_session_view, name="test-session"),
]

app_name = "catalog"
