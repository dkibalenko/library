from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse, Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import generic
from django.core.paginator import Paginator

from .models import Book, Author, LiteraryFormat
from .forms import (
    AuthorCreationForm,
    BookForm,
    BookSearchForm
)


@login_required
def index(request: HttpRequest) -> HttpResponse:
    num_authors = Author.objects.all().count()
    num_books = Book.objects.all().count()
    num_literary_formats = LiteraryFormat.objects.all().count()
    num_visits = request.session.get("num_visits", 0)  # get current num visits
    request.session["num_visits"] = num_visits + 1  # increment num visits
    context = {
        "num_books": num_books,
        "num_authors": num_authors,
        "num_literary_formats": num_literary_formats,
        "num_visits": num_visits + 1,  # display as it is recorded to session object
    }
    return render(request, "catalog/index.html", context=context)


class LiteraryFormatListView(LoginRequiredMixin, generic.ListView):
    # this class only configured for rendering the LiteraryFormat objects
    model = LiteraryFormat  # since the model name consists of 2 words, we need to specify template name etc., below
    template_name = "catalog/literary_format_list.html"
    context_object_name = "literary_format_list"
    # queryset = LiteraryFormat.objects.filter(name__endswith="y")
    # we have more controlled function-based views, and less class-based.


class LiteraryFormatCreateView(LoginRequiredMixin, generic.CreateView):
    model = LiteraryFormat
    fields = "__all__"
    success_url = reverse_lazy("catalog:literary-formats-list")
    template_name = "catalog/literary_format_form.html"


class LiteraryFormatUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = LiteraryFormat
    fields = "__all__"
    success_url = reverse_lazy("catalog:literary-formats-list")
    template_name = "catalog/literary_format_form.html"
    # use the same attributes as for 'create' form (only form will be pre-filled)


class LiteraryFormatDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = LiteraryFormat
    success_url = reverse_lazy("catalog:literary-formats-list")
    template_name = "catalog/literary_format_confirm_delete.html"


class BookListView(LoginRequiredMixin, generic.ListView):
    model = Book  # one word model does not require to specify "template_name" etc.
    # queryset = Book.objects.select_related("format")  # here we don't have access to 'query params', since on the level of class attribute we yet dont' have a request object, and cannot get from it 'query params' for filtering in a search field
    paginate_by = 2

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(BookListView, self).get_context_data(**kwargs)
        title = self.request.GET.get("title", "")
        context["search_form"] = BookSearchForm(
            initial={"title": title}
        )
        return context

    def get_queryset(self):
        queryset = Book.objects.select_related("format")
        form = BookSearchForm(self.request.GET)  # GET attribute contains all 'query params' (GET is a dict) if there is no "title" it returns None
        if form.is_valid():
            return queryset.filter(title__icontains=form.cleaned_data["title"])
        return queryset


class BookDetailView(LoginRequiredMixin, generic.DetailView):
    model = Book


class BookCreateView(LoginRequiredMixin, generic.CreateView):
    model = Book
    form_class = BookForm


class BookUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = Book
    form_class = BookForm


class AuthorListView(LoginRequiredMixin, generic.ListView):
    model = Author
    paginate_by = 3


class AuthorDetailView(LoginRequiredMixin, generic.DetailView):
    model = Author


class AuthorCreateView(LoginRequiredMixin, generic.CreateView):
    model = Author
    form_class = AuthorCreationForm
    # template name is not necessary, it will be generated automatically (author_form)


# def test_session_view(request: HttpRequest) -> HttpResponse:
#     # request.session["book"] = "Test session book"  # create a new object session
#     return HttpResponse(
#         "<h1>Test Session</h1>"
#         f"<h4>Session data: {request.session['book']}</h4>",
#     )


# def listing(request: HttpRequest):  # if only for index.html needed, then put the logic in the index func
#     author_list = Author.objects.all()
#     paginator = Paginator(author_list, 1)
#     page_number = request.GET.get('page')
#     page_obj = paginator.get_page(page_number)
#     return render(request, "catalog/author_list.html", {"author_list": author_list, "page_obj": page_obj})


# def book_detail_view(request: HttpRequest, pk: int) -> HttpResponse:
#     try:
#         book = Book.objects.get(id=pk)  # using "select_related" has no much impact on a single object query with ".get()"
#     except Book.DoesNotExist:
#         raise Http404("Book not found")
#     context = {
#         "book": book,
#     }
#     return render(request, "catalog/book_detail.html", context=context)
