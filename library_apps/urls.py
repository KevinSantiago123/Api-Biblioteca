"""Library apps Urls."""


__author__ = 'kcastanedat'

# Django
from django.conf.urls import url


# Views
from library_apps.author.views import AuthorView
from library_apps.category.views import CategoryView
from library_apps.book.views import BookView
from library_apps.editorial.views import EditorialView
from library_apps.login.views import RegisterApi

urlpatterns = [
    #book
    url(r'^api/library_apps/category_book/v1.0', CategoryView.as_view()),
    url(r'^api/library_apps/author_book/v1.0', AuthorView.as_view()),
    url(r'^api/library_apps/editorial_book/v1.0', EditorialView.as_view()),
    url(r'^api/library_apps/book/v1.0', BookView.as_view()),
    url(r'^api/login/v1.0', RegisterApi.as_view()),
]
