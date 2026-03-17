"""
В этом задании вам нужно реализовать функцию create_book, которая создаёт в БД строку с новой книгой.

Чтобы проверить, работает ли ваш код, запустите runserver и сделайте POST-запрос на 127.0.0.1:8000/book/create/
с теми же параметрами. Если всё отработало без ошибок и ручка возвращает вам описание новой книги в json-формате,
задание выполнено.

Делать post-запрос я рекомендую с помощью Postman (https://www.postman.com/downloads/).
"""
from django.http import HttpRequest, HttpResponse, HttpResponseBadRequest, JsonResponse

from challenges.models import Book


def create_book(title_test: str, author_full_name_test: str, isbn_test: str) -> Book:
    """Создаёт запись в БД с введёнными полями."""
    return Book.objects.create(title=title_test,
                               author_full_name=author_full_name_test,
                               isbn=isbn_test)
    # [17/Mar/2026 10:36:16] "POST /book/create/ HTTP/1.1" 200 98
    # Надо было в тело запроса кидать то параметры, а не в адресную строку...



def create_book_handler(request: HttpRequest) -> HttpResponse:
    title = request.POST.get("title")
    author_full_name = request.POST.get("author_full_name")
    isbn = request.POST.get("isbn")
    if not all([title, author_full_name, isbn]):
        return HttpResponseBadRequest("One of required parameters are missing")

    book = create_book(title, author_full_name, isbn)

    return JsonResponse({
        "id": book.pk,
        "title": book.title,
        "author_full_name": book.author_full_name,
        "isbn": book.isbn,
    })
