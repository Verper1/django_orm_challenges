"""
В этом задании вам предстоит работать с моделью поста в блоге. У него есть название, текст, имя автора, статус
(опубликован/не опубликован/забанен), дата создания, дата публикации, категория (одна из нескольких вариантов).

Ваша задача:
- создать соответствующую модель (в models.py)
- создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
- заполнить вашу локальную базу несколькими ноутбуками для облегчения тестирования
- реализовать у модели метод to_json, который будет преобразовывать объект книги в json-сериализуемый словарь
- по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""
from datetime import timedelta

from django.http import HttpRequest, HttpResponse, JsonResponse
from django.utils import timezone

from challenges.models import Post
from django.db.models import Q


def last_posts_list_view(request: HttpRequest) -> JsonResponse:
    """
    В этой вьюхе вам нужно вернуть 3 последних опубликованных поста.
    """
    posts = Post.objects.all()[:3]
    posts_json = [post.to_json() for post in posts]
    return JsonResponse(posts_json, safe=False)


def posts_search_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты, которые подходят под поисковый запрос.
    Сам запрос возьмите из get-параметра query.
    Подходящесть поста можете определять по вхождению запроса в название или текст поста, например.
    """
    query = request.GET.get("q")

    if not query:
        return JsonResponse([], safe=False)

    posts = Post.objects.filter(
        Q(title__icontains=query) | Q(text__icontains=query) | Q(author__icontains=query) |
        Q(status__icontains=query) | Q(category__icontains=query)
    )

    posts_json = [post.to_json() for post in posts]

    return JsonResponse(posts_json, safe=False)


def untagged_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты без категории, отсортируйте их по автору и дате создания.
    """
    posts = Post.objects.filter(category__isnull=True).order_by("author")

    posts_json = [post.to_json() for post in posts]
    return JsonResponse(posts_json, safe=False)


def categories_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть все посты, категория которых принадлежит одной из указанных.
    Возьмите get-параметр categories, в нём разделённый запятой список выбранных категорий.
    """
    categories_param = request.GET.get("categories", "")
    if not categories_param:
        return JsonResponse([], safe=False)

    categories_list = [c.strip() for c in categories_param.split(",") if c.strip()]

    posts = Post.objects.filter(category__in=categories_list).order_by("-created_at")
    posts_json = [post.to_json() for post in posts]

    return JsonResponse(posts_json, safe=False)


def last_days_posts_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть посты, опубликованные за последние last_days дней.
    Значение last_days возьмите из соответствующего get-параметра.
    """
    last_days_raw = request.GET.get("last_days")

    try:
        last_days = int(last_days_raw)
        if last_days < 0:
            raise ValueError
    except (TypeError, ValueError):
        return JsonResponse([], safe=False)

    since = timezone.now() - timedelta(days=last_days)

    posts = Post.objects.filter(
        posted_at__gte=since,
        status="Опуб"
    ).order_by("-posted_at")

    posts_json = [post.to_json() for post in posts]

    return JsonResponse(posts_json, safe=False)
