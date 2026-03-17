"""
В этом задании вам нужно реализовать функцию delete_book, которая по id книги удаляет саму книгу из БД.

Чтобы проверить, работает ли ваш код, запустите runserver и сделайте POST-запрос
на 127.0.0.1:8000/book/<id книги>/delete/.
После удаления книги попробуйте получить описание удалённой книги с помощью ручки из предыдущего задания
и убедитесь, что книга удалена.
"""
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound, HttpResponseNotAllowed
from mypy.dmypy.client import request

from challenges.models import Book
from challenges.views.level_1.b_book_details import get_book


def delete_book(book_id: int) -> None:
    """Удаляет запись книги в БД по id или отдаёт ответ Not Found."""
    request_get = Book.objects.get(id=book_id)
    request_get.delete()
    # [17/Mar/2026 10:52:31] "POST /book/1/delete/ HTTP/1.1" 200 0

    # Not Found: /book/1/delete/
    # [17/Mar/2026 10:52:34] "POST /book/1/delete/ HTTP/1.1" 404 0


def delete_book_handler(request: HttpRequest, book_id: int) -> HttpResponse:
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"])

    book = get_book(book_id)

    if book is None:
        return HttpResponseNotFound()

    delete_book(book_id)

    return HttpResponse()
