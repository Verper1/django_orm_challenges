"""
В этом задании вам нужно реализовать функцию get_book, которая по id книги получает саму книгу из БД.
Не забудьте обработать случай, когда указан несуществующий id, тогда функция должна возвращать None,
а не выкидывать исключение.

Чтобы проверить, работает ли ваш код, запустите runserver и сделайте GET-запрос на 127.0.0.1:8000/book/<id книги>/.
Если всё отработало без ошибок и ручка возвращает вам описание книги в json-формате, задание выполнено.
Существующий id книги вы можете взять из предыдущего задания.

Сделать get-запрос вы можете как с помощью Postman, так и просто в браузере.
"""
from django.http import HttpRequest, HttpResponse, JsonResponse, HttpResponseNotFound

from challenges.models import Book


def get_book(book_id: int) -> Book | None:
    """Получает запись книги со всеми полями по id или отдаёт ответ Not Found."""
    try:
        return Book.objects.get(id=book_id)
    except Book.DoesNotExist:
        return None
    # Not Found: /book/3/
    # [17/Mar/2026 10:47:54] "GET /book/3/ HTTP/1.1" 404 0

    # [17/Mar/2026 10:48:16] "GET /book/1/ HTTP/1.1" 200 98
    # {
    #     "id": 1,
    #     "title": "title_test",
    #     "author_full_name": "author_full_name_test",
    #     "isbn": "isbn_test"
    # }


def book_details_handler(request: HttpRequest, book_id: int) -> HttpResponse:
    book = get_book(book_id)

    if book is None:
        return HttpResponseNotFound()

    return JsonResponse({
        "id": book.pk,
        "title": book.title,
        "author_full_name": book.author_full_name,
        "isbn": book.isbn,
    })
