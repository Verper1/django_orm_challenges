"""
В этом задании вам предстоит работать с моделью ноутбука. У него есть бренд (один из нескольких вариантов),
год выпуска, количество оперативной памяти, объём жесткого диска, цена, количество этих ноутбуков на складе
и дата добавления.

Ваша задача:
- создать соответствующую модель (в models.py)
- создать и применить миграцию по созданию модели (миграцию нужно добавить в пул-реквест)
- заполнить вашу локальную базу несколькими ноутбуками для облегчения тестирования
  (я бы советовал использовать для этого shell)
- реализовать у модели метод to_json, который будет преобразовывать объект ноутбука в json-сериализуемый словарь
- по очереди реализовать каждую из вьюх в этом файле, проверяя правильность их работу в браузере
"""
from decimal import Decimal, InvalidOperation

from django.http import HttpRequest, JsonResponse, Http404, HttpResponse

from challenges.models import Laptop
from .utils import create_json_data_for_multiple_laptop, create_json_data_for_single_laptop
from django.shortcuts import get_object_or_404


def laptop_details_view(request: HttpRequest, laptop_id: int) -> JsonResponse | Http404:
    """
    В этой вьюхе вам нужно вернуть json-описание ноутбука по его id.
    Если такого id нет, вернуть 404.
    """
    laptop = get_object_or_404(Laptop, id=laptop_id)

    laptop_data = laptop.to_json()

    return JsonResponse(laptop_data)


def laptop_in_stock_list_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть json-описание всех ноутбуков, которых на складе больше нуля.
    Отсортируйте ноутбуки по дате добавления, сначала самый новый.
    """
    laptops = Laptop.objects.filter(available_amount__gt=0)
    laptops_data = [laptop.to_json() for laptop in laptops]

    return JsonResponse(laptops_data, safe=False)


def laptop_filter_view(request: HttpRequest) -> HttpResponse:
    """
    В этой вьюхе вам нужно вернуть список ноутбуков с указанным брендом и указанной минимальной ценой.
    Бренд и цену возьмите из get-параметров с названиями brand и min_price.
    Если бренд не входит в список доступных у вас на сайте или если цена отрицательная, верните 403.
    Отсортируйте ноутбуки по цене, сначала самый дешевый.
    """

    brand = request.GET.get("brand")
    min_price_raw = request.GET.get("min_price")
    brand_we_have = set(Laptop.objects.values_list("vendor", flat=True))

    if brand is None or min_price_raw is None:
        return HttpResponse(status=403)

    try:
        min_price = Decimal(min_price_raw)
    except InvalidOperation:
        return HttpResponse(status=403)

    if brand not in brand_we_have or min_price < 0:
        return HttpResponse(status=403)

    laptops = Laptop.objects.filter(vendor=brand, price__gte=min_price).order_by("price")
    laptops_data = [laptop.to_json() for laptop in laptops]

    return JsonResponse(laptops_data, safe=False)


def last_laptop_details_view(request: HttpRequest) -> JsonResponse | Http404:
    """
    В этой вьюхе вам нужно вернуть json-описание последнего созданного ноутбука.
    Если ноутбуков нет вообще, вернуть 404.
    """

    laptop = Laptop.objects.all().order_by("-created_at").first()

    if laptop is None:
        raise Http404()

    laptop_data = laptop.to_json()
    return JsonResponse(laptop_data)
