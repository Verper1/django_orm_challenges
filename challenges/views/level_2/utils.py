from django.db.models import QuerySet

from challenges.models import Laptop


def create_json_data_for_multiple_laptop(laptops: QuerySet) -> list[dict]:
    """Превращает QuerySet в список со словарями для дальнейшей отдачи в json формате."""

    laptops_data = []

    for laptop in laptops:
        data = {
            "id": laptop.pk,
            "vendor": laptop.vendor,
            "release_year": laptop.release_year,
            "amount_ram": laptop.amount_ram,
            "space_on_disk": laptop.space_on_disk,
            "price": laptop.price,
            "available_amount": laptop.available_amount,
            "created_at": laptop.created_at
        }

        laptops_data.append(data)

    return laptops_data

def create_json_data_for_single_laptop(laptop: Laptop) -> dict:
    """Превращает данные экземпляра класса Laptop в словарь для дальнейшей отдачи в json формате."""

    laptop_data = {
        "id": laptop.pk,
        "vendor": laptop.vendor,
        "release_year": laptop.release_year,
        "amount_ram": laptop.amount_ram,
        "space_on_disk": laptop.space_on_disk,
        "price": laptop.price,
        "available_amount": laptop.available_amount,
        "created_at": laptop.created_at
    }

    return laptop_data

